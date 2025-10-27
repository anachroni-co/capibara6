#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para FASE 3: E2B Integration
"""

import sys
import os
import logging
import json
import asyncio
from datetime import datetime

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from execution.e2b_manager import E2BManager, E2BSandbox
from execution.code_detector import CodeDetector, CodeBlock
from execution.execution_loop import ExecutionLoop
from execution.error_mapping import ErrorMapper, ErrorCategory, ErrorSeverity
from execution.feedback_loop import FeedbackLoop, ExecutionFeedback
from execution.e2b_integration import E2BIntegration

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_e2b_manager():
    """Test del E2BManager."""
    try:
        logger.info("=== Test E2B Manager ===")
        
        async def run_test():
            manager = E2BManager(max_concurrent_sandboxes=3)
            
            # Test ejecución simple
            result = await manager.execute_code(
                code="print('Hello, World!')",
                language="python"
            )
            
            print(f"Ejecución simple: {result['success']}")
            print(f"Output: {result.get('output', 'N/A')}")
            print(f"Execution time: {result['execution_time']:.2f}s")
            
            # Test ejecución con error
            error_result = await manager.execute_code(
                code="print('Hello, World!'",  # Syntax error
                language="python"
            )
            
            print(f"Ejecución con error: {error_result['success']}")
            print(f"Error type: {error_result.get('error_type', 'N/A')}")
            
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
            print(f"Stats del manager: {stats['execution_stats']['total_executions']} ejecuciones")
            
            # Limpiar
            await manager.cleanup()
        
        asyncio.run(run_test())
        
        logger.info("PASS - E2B Manager test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test E2B Manager: {e}")
        return False


def test_code_detector():
    """Test del CodeDetector."""
    try:
        logger.info("=== Test Code Detector ===")
        
        detector = CodeDetector()
        
        # Test con texto que contiene código
        test_text = """
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
        
        Y aquí una consulta SQL:
        
        ```sql
        SELECT name, email 
        FROM users 
        WHERE active = true;
        ```
        
        También hay código inline como `print("test")` y `SELECT * FROM table`.
        """
        
        # Detectar bloques
        blocks = detector.detect_code_blocks(test_text)
        
        print(f"Bloques detectados: {len(blocks)}")
        for i, block in enumerate(blocks):
            print(f"  Bloque {i+1}: {block.language}, líneas {block.start_line}-{block.end_line}")
            print(f"    Complejidad: {block.complexity_score:.2f}")
            print(f"    Ejecutar: {block.requires_execution}")
        
        # Candidatos para ejecución
        candidates = detector.get_execution_candidates(test_text)
        print(f"Candidatos para ejecución: {len(candidates)}")
        
        # Estadísticas
        stats = detector.get_stats()
        print(f"Stats del detector: {stats['detection_stats']['total_detections']} detecciones")
        
        logger.info("PASS - Code Detector test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Code Detector: {e}")
        return False


def test_execution_loop():
    """Test del ExecutionLoop."""
    try:
        logger.info("=== Test Execution Loop ===")
        
        async def run_test():
            e2b_manager = E2BManager()
            execution_loop = ExecutionLoop(e2b_manager, max_attempts=3)
            
            # Test con código que tiene error
            result = await execution_loop.execute_with_correction(
                code="print('Hello, World!'",  # Syntax error - falta paréntesis
                language="python",
                context="Simple greeting function",
                user_intent="Print a greeting message"
            )
            
            print(f"Loop result:")
            print(f"Success: {result['success']}")
            print(f"Total attempts: {result['total_attempts']}")
            print(f"Corrections applied: {result['corrections_applied']}")
            print(f"Loop time: {result['loop_time']:.2f}s")
            
            # Mostrar intentos
            for i, attempt in enumerate(result['attempts']):
                print(f"  Attempt {i+1}:")
                print(f"    Code: {attempt['code'][:50]}...")
                print(f"    Success: {attempt['result']['success']}")
                if attempt.get('correction_applied'):
                    print(f"    Correction: {attempt['correction_applied'][:50]}...")
            
            # Estadísticas
            stats = execution_loop.get_stats()
            print(f"Stats del loop: {stats['loop_stats']['total_loops']} loops")
            
            # Limpiar
            await e2b_manager.cleanup()
        
        asyncio.run(run_test())
        
        logger.info("PASS - Execution Loop test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Execution Loop: {e}")
        return False


def test_error_mapping():
    """Test del ErrorMapper."""
    try:
        logger.info("=== Test Error Mapping ===")
        
        mapper = ErrorMapper()
        
        # Test de mapeo de errores
        test_errors = [
            ("SyntaxError", "unexpected EOF while parsing"),
            ("NameError", "name 'x' is not defined"),
            ("TypeError", "can only concatenate str (not 'int') to str"),
            ("IndentationError", "expected an indented block"),
            ("ImportError", "No module named 'numpy'"),
            ("AttributeError", "'NoneType' object has no attribute 'append'"),
            ("IndexError", "list index out of range"),
            ("KeyError", "'username'")
        ]
        
        for error_type, error_message in test_errors:
            pattern = mapper.map_error(error_message, error_type, "", "python")
            if pattern:
                strategy = mapper.get_correction_strategy(error_message, error_type, "", "python")
                print(f"{error_type}: {error_message}")
                print(f"  Pattern: {pattern.error_type}")
                print(f"  Strategy: {strategy['name'] if strategy else 'None'}")
                print(f"  Confidence: {strategy['confidence'] if strategy else 'N/A'}")
        
        # Estadísticas
        stats = mapper.get_error_statistics()
        print(f"Stats del mapper: {stats['mapping_stats']['total_errors_mapped']} errores mapeados")
        
        # Errores más comunes
        common_errors = mapper.get_most_common_errors(5)
        print(f"Errores más comunes: {len(common_errors)}")
        
        logger.info("PASS - Error Mapping test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Error Mapping: {e}")
        return False


def test_feedback_loop():
    """Test del FeedbackLoop."""
    try:
        logger.info("=== Test Feedback Loop ===")
        
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
        
        # Estadísticas
        stats = feedback_loop.get_stats()
        print(f"Stats del feedback: {stats['feedback_stats']['total_feedback_sent']} feedbacks enviados")
        
        # Insights
        insights = feedback_loop.get_feedback_insights()
        print(f"Insights: {insights['success_rate']:.2f} success rate")
        
        logger.info("PASS - Feedback Loop test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Feedback Loop: {e}")
        return False


def test_e2b_integration():
    """Test de la integración E2B completa."""
    try:
        logger.info("=== Test E2B Integration ===")
        
        async def run_test():
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
            
            print(f"Ejecución directa:")
            print(f"Success: {direct_result['success']}")
            print(f"Output: {direct_result.get('final_result', {}).get('output', 'N/A')}")
            
            # Estadísticas
            stats = integration.get_integration_stats()
            print(f"Stats de integración: {stats['integration_stats']['total_queries_processed']} queries procesadas")
            
            # Insights
            insights = integration.get_insights()
            print(f"Insights: {insights['performance_summary']['execution_success_rate']:.2f} success rate")
            
            # Limpiar
            await integration.cleanup()
        
        asyncio.run(run_test())
        
        logger.info("PASS - E2B Integration test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test E2B Integration: {e}")
        return False


def main():
    """Ejecuta todos los tests de FASE 3."""
    logger.info("Iniciando tests de FASE 3: E2B Integration")
    
    tests = [
        ("E2B Manager", test_e2b_manager),
        ("Code Detector", test_code_detector),
        ("Execution Loop", test_execution_loop),
        ("Error Mapping", test_error_mapping),
        ("Feedback Loop", test_feedback_loop),
        ("E2B Integration", test_e2b_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"Ejecutando test: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    logger.info("\n" + "="*50)
    logger.info("RESUMEN DE TESTS FASE 3")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    logger.info("-" * 50)
    logger.info(f"Total: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("Todos los tests de FASE 3 pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
