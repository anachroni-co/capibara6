#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2B Integration - Integración completa del sistema E2B con ACE.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .e2b_manager import E2BManager
from .code_detector import CodeDetector, CodeBlock
from .execution_loop import ExecutionLoop
from .error_mapping import ErrorMapper
from .feedback_loop import FeedbackLoop
from config.cloud_config import cloud_config

logger = logging.getLogger(__name__)


class E2BIntegration:
    """Integración completa del sistema E2B con ACE."""
    
    def __init__(self, 
                 ace_curator=None,
                 max_concurrent_sandboxes: int = 5,
                 max_attempts: int = 3):
        # Usar configuración de cloud
        e2b_config = cloud_config.get_e2b_config()
        
        self.e2b_manager = E2BManager(
            max_concurrent_sandboxes=max_concurrent_sandboxes,
            default_timeout=e2b_config['timeout'],
            default_memory_limit_mb=e2b_config['memory_limit_mb'],
            default_cpu_limit_percent=e2b_config['cpu_limit_percent'],
            api_key=e2b_config['api_key']
        )
        self.code_detector = CodeDetector()
        self.error_mapper = ErrorMapper()
        self.feedback_loop = FeedbackLoop(ace_curator)
        self.execution_loop = ExecutionLoop(
            e2b_manager=self.e2b_manager,
            max_attempts=max_attempts
        )
        
        self.integration_stats = {
            'total_queries_processed': 0,
            'code_blocks_detected': 0,
            'code_blocks_executed': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_corrections_applied': 0,
            'feedback_sent_to_ace': 0
        }
        
        logger.info("E2BIntegration inicializado")
    
    async def process_response_with_code(self, 
                                       response: str,
                                       query: str = "",
                                       context: str = "",
                                       user_intent: str = "",
                                       execute_code: bool = True) -> Dict[str, Any]:
        """
        Procesa una respuesta que puede contener código.
        
        Args:
            response: Respuesta que puede contener código
            query: Query original del usuario
            context: Contexto adicional
            user_intent: Intención del usuario
            execute_code: Si ejecutar el código detectado
            
        Returns:
            Dict con resultado del procesamiento
        """
        start_time = datetime.now()
        logger.debug(f"Procesando respuesta con código: {len(response)} caracteres")
        
        try:
            result = {
                'success': True,
                'response': response,
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'code_analysis': {},
                'execution_results': [],
                'feedback_sent': False
            }
            
            # 1. Detectar bloques de código
            code_blocks = self.code_detector.detect_code_blocks(response)
            result['code_analysis'] = {
                'total_blocks': len(code_blocks),
                'execution_candidates': len([b for b in code_blocks if b.requires_execution]),
                'languages_detected': list(set(b.language for b in code_blocks)),
                'blocks': [block.to_dict() for block in code_blocks]
            }
            
            self.integration_stats['code_blocks_detected'] += len(code_blocks)
            
            # 2. Ejecutar código si se solicita
            if execute_code and code_blocks:
                execution_results = await self._execute_code_blocks(
                    code_blocks, query, context, user_intent
                )
                result['execution_results'] = execution_results
                
                # 3. Enviar feedback al ACE
                feedback_sent = self._send_feedback_to_ace(execution_results, query, context, user_intent)
                result['feedback_sent'] = feedback_sent
            
            # 4. Actualizar estadísticas
            self._update_integration_stats(result)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            result['processing_time_ms'] = processing_time
            
            logger.info(f"Respuesta procesada: {len(code_blocks)} bloques, "
                       f"{len(result['execution_results'])} ejecuciones, {processing_time:.1f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando respuesta con código: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': response,
                'query': query,
                'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            }
    
    async def _execute_code_blocks(self, 
                                 code_blocks: List[CodeBlock],
                                 query: str,
                                 context: str,
                                 user_intent: str) -> List[Dict[str, Any]]:
        """Ejecuta bloques de código detectados."""
        execution_results = []
        
        for block in code_blocks:
            if not block.requires_execution:
                continue
            
            logger.info(f"Ejecutando bloque {block.language}: {block.code[:50]}...")
            
            try:
                # Ejecutar con loop de corrección
                execution_result = await self.execution_loop.execute_with_correction(
                    code=block.code,
                    language=block.language,
                    context=f"{context}\n{block.context}",
                    user_intent=user_intent
                )
                
                # Agregar información del bloque
                execution_result['block_info'] = {
                    'start_line': block.start_line,
                    'end_line': block.end_line,
                    'complexity_score': block.complexity_score,
                    'context': block.context
                }
                
                execution_results.append(execution_result)
                self.integration_stats['code_blocks_executed'] += 1
                
                if execution_result['success']:
                    self.integration_stats['successful_executions'] += 1
                else:
                    self.integration_stats['failed_executions'] += 1
                
                self.integration_stats['total_corrections_applied'] += execution_result.get('corrections_applied', 0)
                
            except Exception as e:
                logger.error(f"Error ejecutando bloque de código: {e}")
                execution_results.append({
                    'success': False,
                    'error': str(e),
                    'block_info': {
                        'start_line': block.start_line,
                        'end_line': block.end_line,
                        'complexity_score': block.complexity_score
                    }
                })
                self.integration_stats['failed_executions'] += 1
        
        return execution_results
    
    def _send_feedback_to_ace(self, 
                            execution_results: List[Dict[str, Any]],
                            query: str,
                            context: str,
                            user_intent: str) -> bool:
        """Envía feedback de ejecución al ACE."""
        feedback_sent = False
        
        for result in execution_results:
            if 'block_info' in result:
                # Extraer código del resultado
                code = ""
                for attempt in result.get('attempts', []):
                    if attempt.get('code'):
                        code = attempt['code']
                        break
                
                if code:
                    success = self.feedback_loop.send_execution_feedback(
                        execution_result=result,
                        code=code,
                        language=result.get('language', 'python'),
                        context=context,
                        user_intent=user_intent
                    )
                    
                    if success:
                        feedback_sent = True
                        self.integration_stats['feedback_sent_to_ace'] += 1
        
        return feedback_sent
    
    def _update_integration_stats(self, result: Dict[str, Any]):
        """Actualiza estadísticas de integración."""
        self.integration_stats['total_queries_processed'] += 1
    
    async def execute_code_directly(self, 
                                  code: str,
                                  language: str = "python",
                                  context: str = "",
                                  user_intent: str = "") -> Dict[str, Any]:
        """Ejecuta código directamente sin detección."""
        logger.info(f"Ejecutando código directamente: {language}, {len(code)} caracteres")
        
        try:
            # Ejecutar con loop de corrección
            execution_result = await self.execution_loop.execute_with_correction(
                code=code,
                language=language,
                context=context,
                user_intent=user_intent
            )
            
            # Enviar feedback al ACE
            feedback_sent = self.feedback_loop.send_execution_feedback(
                execution_result=execution_result,
                code=code,
                language=language,
                context=context,
                user_intent=user_intent
            )
            
            execution_result['feedback_sent'] = feedback_sent
            
            # Actualizar estadísticas
            self.integration_stats['code_blocks_executed'] += 1
            if execution_result['success']:
                self.integration_stats['successful_executions'] += 1
            else:
                self.integration_stats['failed_executions'] += 1
            
            self.integration_stats['total_corrections_applied'] += execution_result.get('corrections_applied', 0)
            
            if feedback_sent:
                self.integration_stats['feedback_sent_to_ace'] += 1
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Error ejecutando código directamente: {e}")
            return {
                'success': False,
                'error': str(e),
                'code': code,
                'language': language
            }
    
    def get_code_analysis(self, text: str) -> Dict[str, Any]:
        """Analiza texto para detectar código sin ejecutarlo."""
        code_blocks = self.code_detector.detect_code_blocks(text)
        
        return {
            'total_blocks': len(code_blocks),
            'execution_candidates': len([b for b in code_blocks if b.requires_execution]),
            'languages_detected': list(set(b.language for b in code_blocks)),
            'blocks': [block.to_dict() for block in code_blocks],
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de integración."""
        # Calcular métricas derivadas
        success_rate = 0.0
        if self.integration_stats['code_blocks_executed'] > 0:
            success_rate = (self.integration_stats['successful_executions'] / 
                          self.integration_stats['code_blocks_executed'])
        
        avg_corrections = 0.0
        if self.integration_stats['code_blocks_executed'] > 0:
            avg_corrections = (self.integration_stats['total_corrections_applied'] / 
                             self.integration_stats['code_blocks_executed'])
        
        return {
            'integration_stats': self.integration_stats,
            'success_rate': success_rate,
            'avg_corrections_per_execution': avg_corrections,
            'e2b_manager_stats': self.e2b_manager.get_stats(),
            'code_detector_stats': self.code_detector.get_stats(),
            'execution_loop_stats': self.execution_loop.get_stats(),
            'error_mapper_stats': self.error_mapper.get_error_statistics(),
            'feedback_loop_stats': self.feedback_loop.get_stats()
        }
    
    def get_insights(self) -> Dict[str, Any]:
        """Retorna insights del sistema E2B."""
        stats = self.get_integration_stats()
        feedback_insights = self.feedback_loop.get_feedback_insights()
        error_insights = self.error_mapper.get_most_common_errors(5)
        
        return {
            'performance_summary': {
                'total_queries': stats['integration_stats']['total_queries_processed'],
                'code_detection_rate': stats['integration_stats']['code_blocks_detected'] / max(1, stats['integration_stats']['total_queries_processed']),
                'execution_success_rate': stats['success_rate'],
                'avg_corrections': stats['avg_corrections_per_execution']
            },
            'code_analysis': {
                'most_common_languages': list(stats['code_detector_stats']['detection_stats']['languages_detected'].keys()),
                'execution_candidates_rate': stats['integration_stats']['code_blocks_executed'] / max(1, stats['integration_stats']['code_blocks_detected'])
            },
            'error_analysis': {
                'most_common_errors': error_insights,
                'correction_effectiveness': feedback_insights.get('correction_effectiveness', 0.0)
            },
            'recommendations': self._generate_recommendations(stats, feedback_insights)
        }
    
    def _generate_recommendations(self, stats: Dict[str, Any], feedback_insights: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en estadísticas."""
        recommendations = []
        
        # Recomendaciones de performance
        if stats['success_rate'] < 0.7:
            recommendations.append("Mejorar estrategias de corrección de código")
        
        if stats['avg_corrections_per_execution'] > 2:
            recommendations.append("Optimizar detección de errores para reducir correcciones")
        
        # Recomendaciones de feedback
        if feedback_insights.get('success_rate', 0) < 0.8:
            recommendations.append("Revisar patrones de error más comunes")
        
        # Recomendaciones de recursos
        e2b_stats = stats['e2b_manager_stats']
        if e2b_stats['active_sandboxes'] >= e2b_stats['max_concurrent_sandboxes'] * 0.8:
            recommendations.append("Considerar aumentar límite de sandboxes concurrentes")
        
        return recommendations
    
    async def cleanup(self):
        """Limpia recursos del sistema E2B."""
        logger.info("Limpiando recursos E2B...")
        await self.e2b_manager.cleanup()
        logger.info("Limpieza E2B completada")
    
    def set_ace_curator(self, ace_curator):
        """Establece el ACE Curator para feedback."""
        self.feedback_loop.set_ace_curator(ace_curator)
        logger.info("ACE Curator conectado a E2BIntegration")


if __name__ == "__main__":
    # Test de E2BIntegration
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_e2b_integration():
        integration = E2BIntegration()
        
        # Test con respuesta que contiene código
        test_response = """
        Aquí tienes un ejemplo de función en Python:
        
        ```python
        def greet(name):
            print(f"Hello, {name}!")
            return f"Greeting sent to {name}"
        
        # Uso de la función
        result = greet("World")
        ```
        
        También puedes usar JavaScript:
        
        ```javascript
        function calculateSum(a, b) {
            return a + b;
        }
        
        console.log(calculateSum(5, 3));
        ```
        """
        
        # Procesar respuesta
        result = await integration.process_response_with_code(
            response=test_response,
            query="Show me examples of functions",
            context="Programming examples",
            user_intent="Learn about functions"
        )
        
        print(f"Procesamiento completado:")
        print(f"Success: {result['success']}")
        print(f"Code blocks detected: {result['code_analysis']['total_blocks']}")
        print(f"Execution candidates: {result['code_analysis']['execution_candidates']}")
        print(f"Executions completed: {len(result['execution_results'])}")
        print(f"Feedback sent: {result['feedback_sent']}")
        
        # Test ejecución directa
        direct_result = await integration.execute_code_directly(
            code="print('Hello from direct execution!')",
            language="python",
            context="Direct execution test",
            user_intent="Test direct execution"
        )
        
        print(f"\nEjecución directa:")
        print(f"Success: {direct_result['success']}")
        print(f"Output: {direct_result.get('final_result', {}).get('output', 'N/A')}")
        
        # Mostrar estadísticas
        stats = integration.get_integration_stats()
        print(f"\nEstadísticas: {json.dumps(stats, indent=2)}")
        
        # Mostrar insights
        insights = integration.get_insights()
        print(f"\nInsights: {json.dumps(insights, indent=2)}")
        
        # Limpiar
        await integration.cleanup()
    
    asyncio.run(test_e2b_integration())
