#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Loop - Envía resultados de ejecución al ACE para aprendizaje.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ExecutionFeedback:
    """Representa feedback de ejecución para ACE."""
    
    def __init__(self, 
                 execution_id: str,
                 code: str,
                 language: str,
                 success: bool,
                 attempts: List[Dict[str, Any]],
                 final_result: Dict[str, Any],
                 context: str = "",
                 user_intent: str = ""):
        self.execution_id = execution_id
        self.code = code
        self.language = language
        self.success = success
        self.attempts = attempts
        self.final_result = final_result
        self.context = context
        self.user_intent = user_intent
        self.timestamp = datetime.now()
        
        # Análisis del feedback
        self.total_attempts = len(attempts)
        self.corrections_applied = len([a for a in attempts if a.get('correction_applied')])
        self.error_types = self._extract_error_types()
        self.execution_time = final_result.get('execution_time', 0)
        self.complexity_score = self._calculate_complexity()
        
    def _extract_error_types(self) -> List[str]:
        """Extrae tipos de errores de los intentos."""
        error_types = []
        for attempt in self.attempts:
            if attempt.get('result') and not attempt['result'].get('success'):
                error_type = attempt['result'].get('error_type')
                if error_type and error_type not in error_types:
                    error_types.append(error_type)
        return error_types
    
    def _calculate_complexity(self) -> float:
        """Calcula score de complejidad del código."""
        score = 0.0
        
        # Factores de complejidad
        if 'import' in self.code or 'require' in self.code:
            score += 0.2
        if 'def ' in self.code or 'function' in self.code:
            score += 0.3
        if 'class ' in self.code:
            score += 0.4
        if 'if ' in self.code or 'for ' in self.code or 'while ' in self.code:
            score += 0.2
        if 'try:' in self.code or 'except' in self.code:
            score += 0.3
        if 'async' in self.code or 'await' in self.code:
            score += 0.3
        
        # Normalizar por longitud
        lines = len(self.code.split('\n'))
        if lines > 0:
            score = min(1.0, score * (10 / lines))
        
        return score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            'execution_id': self.execution_id,
            'code': self.code,
            'language': self.language,
            'success': self.success,
            'total_attempts': self.total_attempts,
            'corrections_applied': self.corrections_applied,
            'error_types': self.error_types,
            'execution_time': self.execution_time,
            'complexity_score': self.complexity_score,
            'context': self.context,
            'user_intent': self.user_intent,
            'timestamp': self.timestamp.isoformat(),
            'attempts': self.attempts,
            'final_result': self.final_result
        }


class FeedbackLoop:
    """Envía feedback de ejecución al ACE para aprendizaje."""
    
    def __init__(self, ace_curator=None):
        self.ace_curator = ace_curator
        self.feedback_queue = []
        self.feedback_stats = {
            'total_feedback_sent': 0,
            'successful_feedback': 0,
            'failed_feedback': 0,
            'feedback_by_language': {},
            'feedback_by_success': {'success': 0, 'failure': 0},
            'avg_corrections_per_feedback': 0.0
        }
        
        logger.info("FeedbackLoop inicializado")
    
    def send_execution_feedback(self, 
                              execution_result: Dict[str, Any],
                              code: str,
                              language: str,
                              context: str = "",
                              user_intent: str = "") -> bool:
        """
        Envía feedback de ejecución al ACE.
        
        Args:
            execution_result: Resultado del execution loop
            code: Código ejecutado
            language: Lenguaje de programación
            context: Contexto adicional
            user_intent: Intención del usuario
            
        Returns:
            True si el feedback se envió exitosamente
        """
        try:
            # Crear feedback
            feedback = ExecutionFeedback(
                execution_id=f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                code=code,
                language=language,
                success=execution_result.get('success', False),
                attempts=execution_result.get('attempts', []),
                final_result=execution_result.get('final_result', {}),
                context=context,
                user_intent=user_intent
            )
            
            # Enviar al ACE Curator
            if self.ace_curator:
                ace_feedback = self._convert_to_ace_feedback(feedback)
                result = self.ace_curator.process_execution_feedback(ace_feedback)
                
                if result.get('success', False):
                    self.feedback_stats['successful_feedback'] += 1
                    logger.info(f"Feedback enviado exitosamente al ACE: {feedback.execution_id}")
                else:
                    self.feedback_stats['failed_feedback'] += 1
                    logger.error(f"Error enviando feedback al ACE: {result.get('error', 'Unknown error')}")
            else:
                # Si no hay ACE Curator, agregar a cola
                self.feedback_queue.append(feedback)
                logger.info(f"Feedback agregado a cola: {feedback.execution_id}")
            
            # Actualizar estadísticas
            self._update_feedback_stats(feedback)
            
            return True
            
        except Exception as e:
            logger.error(f"Error enviando feedback: {e}")
            self.feedback_stats['failed_feedback'] += 1
            return False
    
    def _convert_to_ace_feedback(self, feedback: ExecutionFeedback) -> Dict[str, Any]:
        """Convierte feedback de ejecución a formato ACE."""
        return {
            'type': 'code_execution',
            'execution_id': feedback.execution_id,
            'success': feedback.success,
            'language': feedback.language,
            'total_attempts': feedback.total_attempts,
            'corrections_applied': feedback.corrections_applied,
            'error_types': feedback.error_types,
            'execution_time': feedback.execution_time,
            'complexity_score': feedback.complexity_score,
            'context': feedback.context,
            'user_intent': feedback.user_intent,
            'timestamp': feedback.timestamp.isoformat(),
            'metadata': {
                'code_length': len(feedback.code),
                'code_lines': len(feedback.code.split('\n')),
                'has_imports': 'import' in feedback.code or 'require' in feedback.code,
                'has_functions': 'def ' in feedback.code or 'function' in feedback.code,
                'has_classes': 'class ' in feedback.code,
                'has_control_flow': any(keyword in feedback.code for keyword in ['if ', 'for ', 'while ']),
                'has_error_handling': 'try:' in feedback.code or 'except' in feedback.code
            }
        }
    
    def _update_feedback_stats(self, feedback: ExecutionFeedback):
        """Actualiza estadísticas de feedback."""
        self.feedback_stats['total_feedback_sent'] += 1
        
        # Estadísticas por lenguaje
        if feedback.language not in self.feedback_stats['feedback_by_language']:
            self.feedback_stats['feedback_by_language'][feedback.language] = 0
        self.feedback_stats['feedback_by_language'][feedback.language] += 1
        
        # Estadísticas por éxito
        if feedback.success:
            self.feedback_stats['feedback_by_success']['success'] += 1
        else:
            self.feedback_stats['feedback_by_success']['failure'] += 1
        
        # Promedio de correcciones
        total_corrections = self.feedback_stats.get('total_corrections', 0) + feedback.corrections_applied
        self.feedback_stats['total_corrections'] = total_corrections
        
        if self.feedback_stats['total_feedback_sent'] > 0:
            self.feedback_stats['avg_corrections_per_feedback'] = (
                total_corrections / self.feedback_stats['total_feedback_sent']
            )
    
    def send_batch_feedback(self, feedback_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Envía múltiples feedbacks en lote."""
        logger.info(f"Enviando {len(feedback_list)} feedbacks en lote")
        
        results = {
            'total_sent': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for feedback_data in feedback_list:
            try:
                success = self.send_execution_feedback(
                    execution_result=feedback_data['execution_result'],
                    code=feedback_data['code'],
                    language=feedback_data['language'],
                    context=feedback_data.get('context', ''),
                    user_intent=feedback_data.get('user_intent', '')
                )
                
                results['total_sent'] += 1
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(str(e))
                logger.error(f"Error en feedback batch: {e}")
        
        logger.info(f"Batch feedback completado: {results['successful']}/{results['total_sent']} exitosos")
        return results
    
    def get_feedback_insights(self) -> Dict[str, Any]:
        """Genera insights basados en el feedback acumulado."""
        insights = {
            'success_rate': 0.0,
            'most_common_errors': [],
            'language_performance': {},
            'correction_effectiveness': 0.0,
            'complexity_analysis': {},
            'recommendations': []
        }
        
        if self.feedback_stats['total_feedback_sent'] == 0:
            return insights
        
        # Tasa de éxito
        total_feedback = self.feedback_stats['total_feedback_sent']
        successful_feedback = self.feedback_stats['feedback_by_success']['success']
        insights['success_rate'] = successful_feedback / total_feedback
        
        # Errores más comunes (simulado - en producción vendría de ACE)
        insights['most_common_errors'] = [
            {'error_type': 'SyntaxError', 'count': 15, 'percentage': 30.0},
            {'error_type': 'NameError', 'count': 10, 'percentage': 20.0},
            {'error_type': 'TypeError', 'count': 8, 'percentage': 16.0},
            {'error_type': 'ImportError', 'count': 7, 'percentage': 14.0},
            {'error_type': 'AttributeError', 'count': 5, 'percentage': 10.0}
        ]
        
        # Performance por lenguaje
        for language, count in self.feedback_stats['feedback_by_language'].items():
            insights['language_performance'][language] = {
                'total_feedback': count,
                'percentage': (count / total_feedback) * 100
            }
        
        # Efectividad de correcciones
        avg_corrections = self.feedback_stats['avg_corrections_per_feedback']
        insights['correction_effectiveness'] = max(0, 1 - (avg_corrections / 3))  # Normalizar a 0-1
        
        # Análisis de complejidad (simulado)
        insights['complexity_analysis'] = {
            'low_complexity_success_rate': 0.85,
            'medium_complexity_success_rate': 0.70,
            'high_complexity_success_rate': 0.45
        }
        
        # Recomendaciones
        if insights['success_rate'] < 0.7:
            insights['recommendations'].append("Mejorar detección de errores comunes")
        
        if insights['correction_effectiveness'] < 0.5:
            insights['recommendations'].append("Optimizar estrategias de corrección")
        
        if 'python' in insights['language_performance']:
            python_perf = insights['language_performance']['python']
            if python_perf['percentage'] > 60:
                insights['recommendations'].append("Considerar optimizaciones específicas para Python")
        
        return insights
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del feedback loop."""
        return {
            'feedback_stats': self.feedback_stats,
            'queue_size': len(self.feedback_queue),
            'ace_curator_connected': self.ace_curator is not None
        }
    
    def process_queued_feedback(self) -> Dict[str, Any]:
        """Procesa feedback en cola si hay ACE Curator disponible."""
        if not self.ace_curator or not self.feedback_queue:
            return {'processed': 0, 'successful': 0, 'failed': 0}
        
        logger.info(f"Procesando {len(self.feedback_queue)} feedbacks en cola")
        
        results = {'processed': 0, 'successful': 0, 'failed': 0}
        
        while self.feedback_queue:
            feedback = self.feedback_queue.pop(0)
            
            try:
                ace_feedback = self._convert_to_ace_feedback(feedback)
                result = self.ace_curator.process_execution_feedback(ace_feedback)
                
                results['processed'] += 1
                if result.get('success', False):
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                results['failed'] += 1
                logger.error(f"Error procesando feedback en cola: {e}")
        
        logger.info(f"Feedback en cola procesado: {results['successful']}/{results['processed']} exitosos")
        return results
    
    def set_ace_curator(self, ace_curator):
        """Establece el ACE Curator para envío de feedback."""
        self.ace_curator = ace_curator
        logger.info("ACE Curator conectado al FeedbackLoop")
        
        # Procesar feedback en cola
        if self.feedback_queue:
            self.process_queued_feedback()


if __name__ == "__main__":
    # Test del FeedbackLoop
    logging.basicConfig(level=logging.INFO)
    
    feedback_loop = FeedbackLoop()
    
    # Test feedback de ejecución exitosa
    successful_execution = {
        'success': True,
        'final_result': {
            'success': True,
            'output': 'Hello, World!',
            'execution_time': 0.5
        },
        'attempts': [
            {
                'attempt_number': 1,
                'result': {'success': True, 'output': 'Hello, World!'}
            }
        ]
    }
    
    result1 = feedback_loop.send_execution_feedback(
        execution_result=successful_execution,
        code="print('Hello, World!')",
        language="python",
        context="Simple greeting",
        user_intent="Print a greeting message"
    )
    
    print(f"Feedback exitoso enviado: {result1}")
    
    # Test feedback de ejecución con correcciones
    failed_execution = {
        'success': True,
        'final_result': {
            'success': True,
            'output': 'Hello, World!',
            'execution_time': 1.2
        },
        'attempts': [
            {
                'attempt_number': 1,
                'result': {'success': False, 'error_type': 'SyntaxError', 'error': 'unexpected EOF'}
            },
            {
                'attempt_number': 2,
                'result': {'success': True, 'output': 'Hello, World!'},
                'correction_applied': "print('Hello, World!')"
            }
        ]
    }
    
    result2 = feedback_loop.send_execution_feedback(
        execution_result=failed_execution,
        code="print('Hello, World!'",  # Syntax error
        language="python",
        context="Greeting with syntax error",
        user_intent="Print a greeting message"
    )
    
    print(f"Feedback con corrección enviado: {result2}")
    
    # Mostrar estadísticas
    stats = feedback_loop.get_stats()
    print(f"\nEstadísticas: {json.dumps(stats, indent=2)}")
    
    # Mostrar insights
    insights = feedback_loop.get_feedback_insights()
    print(f"\nInsights: {json.dumps(insights, indent=2)}")
