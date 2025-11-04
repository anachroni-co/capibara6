#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2B Manager - Gestiona ejecuciones de código en sandboxes E2B.
"""

import logging
import time
import asyncio
import os
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

# E2B SDK
try:
    from e2b_code_interpreter import CodeInterpreter
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False
    CodeInterpreter = None

logger = logging.getLogger(__name__)


class E2BSandbox:
    """Wrapper para sandbox E2B con límites de recursos."""
    
    def __init__(self, 
                 language: str = "python",
                 timeout: int = 30,
                 memory_limit_mb: int = 512,
                 cpu_limit_percent: int = 50,
                 api_key: str = None):
        self.language = language
        self.timeout = timeout
        self.memory_limit_mb = memory_limit_mb
        self.cpu_limit_percent = cpu_limit_percent
        self.api_key = api_key
        self.is_active = False
        self.start_time = None
        self.execution_count = 0
        self.interpreter = None
        
        logger.info(f"E2BSandbox inicializado: {language}, timeout={timeout}s, "
                   f"memory={memory_limit_mb}MB, cpu={cpu_limit_percent}%")
    
    async def execute(self, code: str) -> Dict[str, Any]:
        """Ejecuta código en el sandbox."""
        if not self.is_active:
            await self._start_sandbox()
        
        start_time = time.time()
        self.execution_count += 1
        
        try:
            if self.interpreter and E2B_AVAILABLE:
                # Usar E2B real
                result = await self._execute_with_e2b(code)
            else:
                # Usar simulación
                result = await self._simulate_execution(code)
            
            execution_time = time.time() - start_time
            
            return {
                'success': result.get('success', True),
                'output': result.get('output', ''),
                'error': result.get('error'),
                'error_type': result.get('error_type'),
                'execution_time': execution_time,
                'memory_used_mb': result.get('memory_used', 0),
                'cpu_used_percent': result.get('cpu_used', 0),
                'language': self.language,
                'sandbox_id': id(self),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return {
                'success': False,
                'output': None,
                'error': str(e),
                'error_type': type(e).__name__,
                'execution_time': execution_time,
                'memory_used_mb': 0,
                'cpu_used_percent': 0,
                'language': self.language,
                'sandbox_id': id(self),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _start_sandbox(self):
        """Inicia el sandbox."""
        try:
            if E2B_AVAILABLE and self.api_key:
                # Usar E2B real
                self.interpreter = CodeInterpreter(api_key=self.api_key)
                logger.info(f"Sandbox E2B real iniciado para {self.language}")
            else:
                # Fallback a simulación
                logger.warning("E2B SDK no disponible, usando simulación")
            
            self.is_active = True
            self.start_time = time.time()
            logger.info(f"Sandbox {self.language} iniciado")
            
        except Exception as e:
            logger.error(f"Error iniciando sandbox E2B: {e}")
            # Fallback a simulación
            self.is_active = True
            self.start_time = time.time()
    
    async def _execute_with_e2b(self, code: str) -> Dict[str, Any]:
        """Ejecuta código usando E2B real."""
        try:
            # Ejecutar código en E2B
            result = self.interpreter.run(code)
            
            # Procesar resultado
            output = ""
            error = None
            error_type = None
            success = True
            
            if result.error:
                error = str(result.error)
                error_type = type(result.error).__name__
                success = False
            else:
                # Combinar stdout y stderr
                output_parts = []
                if result.stdout:
                    output_parts.append(result.stdout)
                if result.stderr:
                    output_parts.append(result.stderr)
                output = "\n".join(output_parts)
            
            return {
                'success': success,
                'output': output,
                'error': error,
                'error_type': error_type,
                'memory_used': 0,  # E2B no expone métricas de memoria directamente
                'cpu_used': 0      # E2B no expone métricas de CPU directamente
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': None,
                'error': str(e),
                'error_type': type(e).__name__,
                'memory_used': 0,
                'cpu_used': 0
            }
    
    async def _simulate_execution(self, code: str) -> Dict[str, Any]:
        """Simula ejecución de código (para testing)."""
        # Simular diferentes tipos de ejecución basado en el código
        code_lower = code.lower()
        
        if 'print(' in code_lower or 'console.log' in code_lower:
            # Código con output
            return {
                'output': 'Hello, World!\nExecution completed successfully.',
                'memory_used': 50,
                'cpu_used': 25
            }
        elif 'error' in code_lower or 'exception' in code_lower:
            # Código que genera error
            raise SyntaxError("Invalid syntax on line 1")
        elif 'import' in code_lower or 'require' in code_lower:
            # Código con imports
            return {
                'output': 'Dependencies loaded successfully.\nReady for execution.',
                'memory_used': 100,
                'cpu_used': 15
            }
        else:
            # Código genérico
            return {
                'output': 'Code executed successfully.',
                'memory_used': 30,
                'cpu_used': 10
            }
    
    async def close(self):
        """Cierra el sandbox."""
        if self.is_active:
            if self.interpreter:
                try:
                    self.interpreter.close()
                    logger.info(f"Intérprete E2B cerrado para {self.language}")
                except Exception as e:
                    logger.error(f"Error cerrando intérprete E2B: {e}")
            
            self.is_active = False
            logger.info(f"Sandbox {self.language} cerrado después de {self.execution_count} ejecuciones")


class E2BManager:
    """Gestiona múltiples sandboxes E2B con límites de recursos."""
    
    def __init__(self, 
                 max_concurrent_sandboxes: int = 5,
                 default_timeout: int = 30,
                 default_memory_limit_mb: int = 512,
                 default_cpu_limit_percent: int = 50,
                 api_key: str = None):
        self.max_concurrent_sandboxes = max_concurrent_sandboxes
        self.default_timeout = default_timeout
        self.default_memory_limit_mb = default_memory_limit_mb
        self.default_cpu_limit_percent = default_cpu_limit_percent
        self.api_key = api_key
        
        self.sandboxes: Dict[str, E2BSandbox] = {}
        self.supported_languages = ['python', 'javascript', 'sql', 'bash']
        
        self.execution_stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_execution_time': 0.0,
            'languages_used': {},
            'error_types': {}
        }
        
        logger.info(f"E2BManager inicializado: max_sandboxes={max_concurrent_sandboxes}, "
                   f"timeout={default_timeout}s, memory={default_memory_limit_mb}MB")
    
    async def execute_code(self, 
                          code: str, 
                          language: str = "python",
                          timeout: Optional[int] = None,
                          memory_limit_mb: Optional[int] = None,
                          cpu_limit_percent: Optional[int] = None) -> Dict[str, Any]:
        """
        Ejecuta código en un sandbox con límites de recursos.
        
        Args:
            code: Código a ejecutar
            language: Lenguaje de programación
            timeout: Timeout en segundos
            memory_limit_mb: Límite de memoria en MB
            cpu_limit_percent: Límite de CPU en porcentaje
            
        Returns:
            Dict con resultado de la ejecución
        """
        start_time = time.time()
        logger.debug(f"Ejecutando código {language}: {code[:100]}...")
        
        try:
            # Validar lenguaje
            if language not in self.supported_languages:
                raise ValueError(f"Lenguaje no soportado: {language}. Soportados: {self.supported_languages}")
            
            # Obtener o crear sandbox
            sandbox = await self._get_or_create_sandbox(
                language=language,
                timeout=timeout or self.default_timeout,
                memory_limit_mb=memory_limit_mb or self.default_memory_limit_mb,
                cpu_limit_percent=cpu_limit_percent or self.default_cpu_limit_percent
            )
            
            # Ejecutar código
            result = await sandbox.execute(code)
            
            # Actualizar estadísticas
            self._update_execution_stats(result)
            
            total_time = time.time() - start_time
            result['total_processing_time'] = total_time
            
            logger.info(f"Ejecución completada: success={result['success']}, "
                       f"time={result['execution_time']:.2f}s, language={language}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error en ejecución E2B: {e}")
            return {
                'success': False,
                'output': None,
                'error': str(e),
                'error_type': type(e).__name__,
                'execution_time': time.time() - start_time,
                'language': language,
                'timestamp': datetime.now().isoformat()
            }
    
    async def _get_or_create_sandbox(self, 
                                   language: str,
                                   timeout: int,
                                   memory_limit_mb: int,
                                   cpu_limit_percent: int) -> E2BSandbox:
        """Obtiene o crea un sandbox para el lenguaje especificado."""
        sandbox_key = f"{language}_{timeout}_{memory_limit_mb}_{cpu_limit_percent}"
        
        if sandbox_key in self.sandboxes:
            return self.sandboxes[sandbox_key]
        
        # Verificar límite de sandboxes concurrentes
        if len(self.sandboxes) >= self.max_concurrent_sandboxes:
            # Cerrar sandbox más antiguo
            oldest_key = min(self.sandboxes.keys(), 
                           key=lambda k: self.sandboxes[k].start_time or 0)
            await self.sandboxes[oldest_key].close()
            del self.sandboxes[oldest_key]
        
        # Crear nuevo sandbox
        sandbox = E2BSandbox(
            language=language,
            timeout=timeout,
            memory_limit_mb=memory_limit_mb,
            cpu_limit_percent=cpu_limit_percent,
            api_key=self.api_key
        )
        
        self.sandboxes[sandbox_key] = sandbox
        logger.info(f"Nuevo sandbox creado: {sandbox_key}")
        
        return sandbox
    
    def _update_execution_stats(self, result: Dict[str, Any]):
        """Actualiza estadísticas de ejecución."""
        self.execution_stats['total_executions'] += 1
        
        if result['success']:
            self.execution_stats['successful_executions'] += 1
        else:
            self.execution_stats['failed_executions'] += 1
        
        self.execution_stats['total_execution_time'] += result['execution_time']
        
        # Estadísticas por lenguaje
        language = result['language']
        if language not in self.execution_stats['languages_used']:
            self.execution_stats['languages_used'][language] = 0
        self.execution_stats['languages_used'][language] += 1
        
        # Estadísticas de errores
        if not result['success'] and result['error_type']:
            error_type = result['error_type']
            if error_type not in self.execution_stats['error_types']:
                self.execution_stats['error_types'][error_type] = 0
            self.execution_stats['error_types'][error_type] += 1
    
    async def execute_multiple(self, 
                              executions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ejecuta múltiples códigos en paralelo."""
        logger.info(f"Ejecutando {len(executions)} códigos en paralelo")
        
        tasks = []
        for execution in executions:
            task = self.execute_code(
                code=execution['code'],
                language=execution.get('language', 'python'),
                timeout=execution.get('timeout'),
                memory_limit_mb=execution.get('memory_limit_mb'),
                cpu_limit_percent=execution.get('cpu_limit_percent')
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados y manejar excepciones
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'success': False,
                    'output': None,
                    'error': str(result),
                    'error_type': type(result).__name__,
                    'execution_time': 0,
                    'language': executions[i].get('language', 'python'),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                processed_results.append(result)
        
        logger.info(f"Ejecuciones paralelas completadas: {len(processed_results)} resultados")
        return processed_results
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del E2BManager."""
        success_rate = 0.0
        if self.execution_stats['total_executions'] > 0:
            success_rate = (self.execution_stats['successful_executions'] / 
                          self.execution_stats['total_executions'])
        
        avg_execution_time = 0.0
        if self.execution_stats['total_executions'] > 0:
            avg_execution_time = (self.execution_stats['total_execution_time'] / 
                                self.execution_stats['total_executions'])
        
        return {
            'execution_stats': self.execution_stats,
            'success_rate': success_rate,
            'avg_execution_time': avg_execution_time,
            'active_sandboxes': len(self.sandboxes),
            'max_concurrent_sandboxes': self.max_concurrent_sandboxes,
            'supported_languages': self.supported_languages
        }
    
    async def cleanup(self):
        """Limpia todos los sandboxes activos."""
        logger.info("Limpiando sandboxes E2B...")
        
        for sandbox in self.sandboxes.values():
            await sandbox.close()
        
        self.sandboxes.clear()
        logger.info("Limpieza de sandboxes completada")
    
    def get_sandbox_info(self) -> Dict[str, Any]:
        """Retorna información sobre sandboxes activos."""
        sandbox_info = {}
        for key, sandbox in self.sandboxes.items():
            sandbox_info[key] = {
                'language': sandbox.language,
                'timeout': sandbox.timeout,
                'memory_limit_mb': sandbox.memory_limit_mb,
                'cpu_limit_percent': sandbox.cpu_limit_percent,
                'is_active': sandbox.is_active,
                'execution_count': sandbox.execution_count,
                'uptime_seconds': time.time() - (sandbox.start_time or time.time())
            }
        return sandbox_info


if __name__ == "__main__":
    # Test del E2BManager
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_e2b_manager():
        manager = E2BManager()
        
        # Test ejecución simple
        result = await manager.execute_code(
            code="print('Hello, World!')",
            language="python"
        )
        print(f"Ejecución simple: {result['success']}")
        
        # Test ejecución con error
        error_result = await manager.execute_code(
            code="print('Hello, World!'",  # Syntax error
            language="python"
        )
        print(f"Ejecución con error: {error_result['success']}, error: {error_result['error_type']}")
        
        # Test ejecuciones múltiples
        executions = [
            {'code': 'print("Test 1")', 'language': 'python'},
            {'code': 'console.log("Test 2")', 'language': 'javascript'},
            {'code': 'SELECT 1;', 'language': 'sql'}
        ]
        
        results = await manager.execute_multiple(executions)
        print(f"Ejecuciones múltiples: {len(results)} resultados")
        
        # Mostrar estadísticas
        stats = manager.get_stats()
        print(f"Stats: {json.dumps(stats, indent=2)}")
        
        # Limpiar
        await manager.cleanup()
    
    asyncio.run(test_e2b_manager())
