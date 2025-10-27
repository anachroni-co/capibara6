#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para E2B real con API key.
"""

import sys
import os
import logging
import asyncio
from datetime import datetime

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from execution.e2b_manager import E2BManager
from execution.e2b_integration import E2BIntegration
from config.cloud_config import cloud_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_e2b_real():
    """Test de E2B con API key real."""
    try:
        logger.info("=== Test E2B Real ===")
        
        # Mostrar configuración
        e2b_config = cloud_config.get_e2b_config()
        print(f"E2B API Key: {e2b_config['api_key'][:10]}...")
        print(f"Timeout: {e2b_config['timeout']}s")
        print(f"Memory Limit: {e2b_config['memory_limit_mb']}MB")
        
        # Crear E2BManager
        manager = E2BManager(
            max_concurrent_sandboxes=2,
            api_key=e2b_config['api_key']
        )
        
        # Test ejecución simple
        print("\n--- Test Ejecución Simple ---")
        result = await manager.execute_code(
            code="print('Hello from E2B!')",
            language="python"
        )
        
        print(f"Success: {result['success']}")
        print(f"Output: {result.get('output', 'N/A')}")
        print(f"Error: {result.get('error', 'None')}")
        print(f"Execution time: {result['execution_time']:.2f}s")
        
        # Test ejecución con error
        print("\n--- Test Ejecución con Error ---")
        error_result = await manager.execute_code(
            code="print('Hello, World!'",  # Syntax error
            language="python"
        )
        
        print(f"Success: {error_result['success']}")
        print(f"Error type: {error_result.get('error_type', 'N/A')}")
        print(f"Error message: {error_result.get('error', 'N/A')}")
        
        # Test ejecución con cálculo
        print("\n--- Test Ejecución con Cálculo ---")
        calc_result = await manager.execute_code(
            code="""
import math
result = math.sqrt(16) + math.pi
print(f"Result: {result}")
print(f"Type: {type(result)}")
""",
            language="python"
        )
        
        print(f"Success: {calc_result['success']}")
        print(f"Output: {calc_result.get('output', 'N/A')}")
        
        # Mostrar estadísticas
        stats = manager.get_stats()
        print(f"\n--- Estadísticas ---")
        print(f"Total executions: {stats['execution_stats']['total_executions']}")
        print(f"Successful: {stats['execution_stats']['successful_executions']}")
        print(f"Failed: {stats['execution_stats']['failed_executions']}")
        print(f"Success rate: {stats['success_rate']:.2%}")
        
        # Limpiar
        await manager.cleanup()
        
        logger.info("PASS - E2B Real test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test E2B Real: {e}")
        return False


async def test_e2b_integration_real():
    """Test de integración E2B completa con API real."""
    try:
        logger.info("=== Test E2B Integration Real ===")
        
        # Crear integración
        integration = E2BIntegration()
        
        # Test con respuesta que contiene código
        test_response = """
        Aquí tienes un ejemplo de función en Python:
        
        ```python
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        # Calcular los primeros 10 números de Fibonacci
        for i in range(10):
            print(f"F({i}) = {fibonacci(i)}")
        ```
        
        También puedes usar JavaScript:
        
        ```javascript
        function factorial(n) {
            if (n <= 1) return 1;
            return n * factorial(n - 1);
        }
        
        console.log("Factorial de 5:", factorial(5));
        ```
        """
        
        # Procesar respuesta
        result = await integration.process_response_with_code(
            response=test_response,
            query="Show me examples of recursive functions",
            context="Programming examples",
            user_intent="Learn about recursive functions"
        )
        
        print(f"Procesamiento completado:")
        print(f"Success: {result['success']}")
        print(f"Code blocks detected: {result['code_analysis']['total_blocks']}")
        print(f"Execution candidates: {result['code_analysis']['execution_candidates']}")
        print(f"Executions completed: {len(result['execution_results'])}")
        print(f"Feedback sent: {result['feedback_sent']}")
        
        # Mostrar resultados de ejecución
        for i, exec_result in enumerate(result['execution_results']):
            print(f"\nEjecución {i+1}:")
            print(f"  Success: {exec_result['success']}")
            print(f"  Language: {exec_result.get('language', 'N/A')}")
            print(f"  Attempts: {exec_result.get('total_attempts', 0)}")
            print(f"  Corrections: {exec_result.get('corrections_applied', 0)}")
            if exec_result.get('final_result', {}).get('output'):
                output = exec_result['final_result']['output'][:200]
                print(f"  Output: {output}...")
        
        # Test ejecución directa
        print(f"\n--- Test Ejecución Directa ---")
        direct_result = await integration.execute_code_directly(
            code="""
import datetime
now = datetime.datetime.now()
print(f"Current time: {now}")
print(f"Timestamp: {now.timestamp()}")
""",
            language="python",
            context="Direct execution test",
            user_intent="Test direct execution with datetime"
        )
        
        print(f"Ejecución directa:")
        print(f"Success: {direct_result['success']}")
        print(f"Output: {direct_result.get('final_result', {}).get('output', 'N/A')}")
        
        # Mostrar estadísticas
        stats = integration.get_integration_stats()
        print(f"\n--- Estadísticas de Integración ---")
        print(f"Total queries: {stats['integration_stats']['total_queries_processed']}")
        print(f"Code blocks detected: {stats['integration_stats']['code_blocks_detected']}")
        print(f"Code blocks executed: {stats['integration_stats']['code_blocks_executed']}")
        print(f"Successful executions: {stats['integration_stats']['successful_executions']}")
        print(f"Failed executions: {stats['integration_stats']['failed_executions']}")
        print(f"Success rate: {stats['success_rate']:.2%}")
        
        # Mostrar insights
        insights = integration.get_insights()
        print(f"\n--- Insights ---")
        print(f"Performance summary: {insights['performance_summary']}")
        print(f"Recommendations: {insights['recommendations']}")
        
        # Limpiar
        await integration.cleanup()
        
        logger.info("PASS - E2B Integration Real test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test E2B Integration Real: {e}")
        return False


async def main():
    """Ejecuta todos los tests de E2B real."""
    logger.info("Iniciando tests de E2B Real")
    
    tests = [
        ("E2B Real", test_e2b_real),
        ("E2B Integration Real", test_e2b_integration_real)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"Ejecutando test: {test_name}")
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    logger.info("\n" + "="*50)
    logger.info("RESUMEN DE TESTS E2B REAL")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name:25} {status}")
        if success:
            passed += 1
    
    logger.info("-" * 50)
    logger.info(f"Total: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("Todos los tests de E2B Real pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
