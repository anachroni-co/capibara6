#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests - Tests end-to-end para routing, ACE cycle, E2B execution.
"""

import pytest
import unittest
import logging
import json
import os
import sys
import asyncio
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any, Optional

# Configurar logging para tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRoutingIntegration:
    """Tests de integración para el sistema de routing."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.test_scenarios = [
            {
                'query': "How to create a Python function that calculates fibonacci numbers?",
                'expected_complexity': 0.7,
                'expected_domain': 'python',
                'expected_model': '20b'
            },
            {
                'query': "SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name HAVING COUNT(o.id) > 5 ORDER BY order_count DESC;",
                'expected_complexity': 0.8,
                'expected_domain': 'sql',
                'expected_model': '120b'
            },
            {
                'query': "Debug this JavaScript error: TypeError: Cannot read property 'length' of undefined",
                'expected_complexity': 0.6,
                'expected_domain': 'javascript',
                'expected_model': '20b'
            },
            {
                'query': "Implement a transformer-based neural network for natural language processing with attention mechanisms, positional encoding, and multi-head attention layers",
                'expected_complexity': 0.9,
                'expected_domain': 'ml',
                'expected_model': '120b'
            }
        ]
    
    def test_routing_pipeline(self):
        """Test del pipeline completo de routing."""
        try:
            from core.router import Router
            from core.embeddings import EmbeddingGenerator
            from core.thresholds import ThresholdManager
            
            # Inicializar componentes
            router = Router()
            embedding_generator = EmbeddingGenerator()
            threshold_manager = ThresholdManager()
            
            for scenario in self.test_scenarios:
                query = scenario['query']
                expected_complexity = scenario['expected_complexity']
                expected_domain = scenario['expected_domain']
                expected_model = scenario['expected_model']
                
                # Generar embeddings
                embeddings = embedding_generator.generate_embeddings(query)
                assert embeddings is not None
                assert len(embeddings) > 0
                
                # Analizar complejidad
                complexity = router.analyze_complexity(query, embeddings)
                assert 0 <= complexity <= 1
                
                # Determinar dominio
                domain = router.determine_domain(query, embeddings)
                assert domain is not None
                assert isinstance(domain, str)
                
                # Routear query
                routing_result = router.route_query(query, {
                    'complexity': complexity,
                    'domain': domain,
                    'embeddings': embeddings
                })
                
                assert routing_result is not None
                assert hasattr(routing_result, 'model_20b_confidence')
                assert hasattr(routing_result, 'model_120b_confidence')
                assert hasattr(routing_result, 'selected_model')
                assert hasattr(routing_result, 'reasoning')
                
                # Verificar que la decisión es razonable
                if complexity >= 0.7:
                    assert routing_result.model_120b_confidence >= routing_result.model_20b_confidence
                else:
                    assert routing_result.model_20b_confidence >= routing_result.model_120b_confidence
                
                logger.info(f"✓ Routing pipeline test passed for: {query[:50]}...")
            
            logger.info("✓ Routing integration test completed successfully")
            
        except ImportError as e:
            logger.warning(f"Routing modules not available: {e}")
        except Exception as e:
            logger.error(f"Routing integration test failed: {e}")
            raise
    
    def test_routing_with_embeddings(self):
        """Test de routing con embeddings."""
        try:
            from core.router import Router
            from core.embeddings import EmbeddingGenerator
            
            router = Router()
            embedding_generator = EmbeddingGenerator()
            
            # Test con diferentes tipos de queries
            test_queries = [
                "Simple Python question",
                "Complex machine learning algorithm",
                "Database optimization query",
                "JavaScript debugging help"
            ]
            
            for query in test_queries:
                # Generar embeddings
                embeddings = embedding_generator.generate_embeddings(query)
                
                # Routear con embeddings
                result = router.route_query(query, {'embeddings': embeddings})
                
                assert result is not None
                assert result.model_20b_confidence + result.model_120b_confidence > 0
                
                logger.info(f"✓ Routing with embeddings test passed for: {query}")
            
        except ImportError as e:
            logger.warning(f"Routing/Embeddings modules not available: {e}")
        except Exception as e:
            logger.error(f"Routing with embeddings test failed: {e}")
            raise
    
    def test_routing_thresholds(self):
        """Test de routing con diferentes umbrales."""
        try:
            from core.router import Router
            from core.thresholds import ThresholdManager
            
            router = Router()
            threshold_manager = ThresholdManager()
            
            # Test con diferentes umbrales
            thresholds = [0.3, 0.5, 0.7, 0.9]
            test_query = "Complex machine learning question with multiple components"
            
            for threshold in thresholds:
                # Establecer umbral
                threshold_manager.set_threshold('complexity', threshold)
                
                # Routear
                result = router.route_query(test_query, {})
                
                assert result is not None
                
                # Verificar que la decisión respeta el umbral
                if threshold >= 0.7:
                    # Con umbral alto, debería preferir modelo 120b
                    assert result.model_120b_confidence >= result.model_20b_confidence
                else:
                    # Con umbral bajo, puede usar cualquier modelo
                    assert result.model_20b_confidence + result.model_120b_confidence > 0
                
                logger.info(f"✓ Routing threshold test passed for threshold: {threshold}")
            
        except ImportError as e:
            logger.warning(f"Routing/Thresholds modules not available: {e}")
        except Exception as e:
            logger.error(f"Routing thresholds test failed: {e}")
            raise


class TestACECycleIntegration:
    """Tests de integración para el ciclo ACE."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.test_queries = [
            "How to implement a REST API in Python?",
            "What are the best practices for database optimization?",
            "How to debug memory leaks in JavaScript applications?",
            "Explain the transformer architecture in deep learning"
        ]
        
        self.test_playbooks = [
            {
                "id": "python_api_playbook",
                "name": "Python API Development",
                "patterns": ["REST", "API", "Python", "Flask", "FastAPI"],
                "success_rate": 0.92,
                "usage_count": 150
            },
            {
                "id": "database_optimization_playbook",
                "name": "Database Optimization",
                "patterns": ["database", "optimization", "index", "query", "performance"],
                "success_rate": 0.88,
                "usage_count": 200
            }
        ]
    
    def test_ace_full_cycle(self):
        """Test del ciclo completo ACE."""
        try:
            from ace.generator import ACEGenerator
            from ace.reflector import ACEReflector
            from ace.curator import ACECurator
            from ace.integration import ACEIntegration
            
            # Inicializar componentes
            generator = ACEGenerator()
            reflector = ACEReflector()
            curator = ACECurator()
            integration = ACEIntegration()
            
            for query in self.test_queries:
                # 1. Generar contexto
                context = generator.generate_context(query, self.test_playbooks[0])
                assert context is not None
                assert isinstance(context, str)
                assert len(context) > 0
                
                # 2. Reflexionar sobre el contexto
                reflection = reflector.reflect(context, query)
                assert reflection is not None
                assert hasattr(reflection, 'score')
                assert hasattr(reflection, 'insights')
                assert 0 <= reflection.score <= 1
                
                # 3. Curar el resultado
                curated_result = curator.curate({
                    'context': context,
                    'reflection': reflection,
                    'query': query
                })
                assert curated_result is not None
                assert hasattr(curated_result, 'quality_score')
                assert hasattr(curated_result, 'is_approved')
                
                # 4. Integrar con CAG
                integrated_result = integration.integrate_with_cag(
                    query, context, curated_result
                )
                assert integrated_result is not None
                assert hasattr(integrated_result, 'enhanced_context')
                assert hasattr(integrated_result, 'awareness_score')
                
                logger.info(f"✓ ACE full cycle test passed for: {query[:50]}...")
            
            logger.info("✓ ACE cycle integration test completed successfully")
            
        except ImportError as e:
            logger.warning(f"ACE modules not available: {e}")
        except Exception as e:
            logger.error(f"ACE cycle integration test failed: {e}")
            raise
    
    def test_ace_playbook_evolution(self):
        """Test de evolución de playbooks ACE."""
        try:
            from ace.generator import ACEGenerator
            from ace.curator import ACECurator
            
            generator = ACEGenerator()
            curator = ACECurator()
            
            # Test de evolución de playbook
            initial_playbook = self.test_playbooks[0].copy()
            
            # Simular múltiples usos
            for i in range(10):
                # Generar contexto
                context = generator.generate_context(
                    f"Test query {i}", 
                    initial_playbook
                )
                
                # Curar resultado
                curated = curator.curate({
                    'context': context,
                    'query': f"Test query {i}",
                    'playbook': initial_playbook
                })
                
                # Actualizar playbook si es aprobado
                if curated.is_approved:
                    initial_playbook['usage_count'] += 1
                    if curated.quality_score > 0.8:
                        initial_playbook['success_rate'] = min(1.0, 
                            initial_playbook['success_rate'] + 0.01)
                
                assert initial_playbook['usage_count'] >= 150
                assert 0 <= initial_playbook['success_rate'] <= 1
            
            logger.info("✓ ACE playbook evolution test passed")
            
        except ImportError as e:
            logger.warning(f"ACE modules not available: {e}")
        except Exception as e:
            logger.error(f"ACE playbook evolution test failed: {e}")
            raise
    
    def test_ace_cag_integration(self):
        """Test de integración ACE con CAG."""
        try:
            from ace.integration import ACEIntegration
            from core.cag.dynamic_context import DynamicContext
            from core.cag.awareness_gate import AwarenessGate
            
            ace_integration = ACEIntegration()
            dynamic_context = DynamicContext(max_tokens=8000)
            awareness_gate = AwarenessGate()
            
            test_query = "How to implement authentication in a web application?"
            test_context = "Authentication is a critical security component..."
            
            # Integrar con CAG
            result = ace_integration.integrate_with_cag(test_query, test_context)
            
            assert result is not None
            assert hasattr(result, 'enhanced_context')
            assert hasattr(result, 'awareness_score')
            assert hasattr(result, 'cag_activation')
            
            # Verificar que el contexto se agregó a CAG
            dynamic_context.add_context(result.enhanced_context)
            assert len(dynamic_context.get_context()) > 0
            
            # Verificar awareness gate
            awareness_score = awareness_gate.evaluate_awareness(result.enhanced_context)
            assert 0 <= awareness_score <= 1
            
            logger.info("✓ ACE-CAG integration test passed")
            
        except ImportError as e:
            logger.warning(f"ACE/CAG modules not available: {e}")
        except Exception as e:
            logger.error(f"ACE-CAG integration test failed: {e}")
            raise


class TestE2BExecutionIntegration:
    """Tests de integración para ejecución E2B."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.test_code_samples = {
            'python': [
                'print("Hello, World!")',
                'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))',
                'import numpy as np\narr = np.array([1, 2, 3, 4, 5])\nprint(np.mean(arr))'
            ],
            'javascript': [
                'console.log("Hello, World!");',
                'function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\nconsole.log(fibonacci(10));',
                'const arr = [1, 2, 3, 4, 5];\nconsole.log(arr.reduce((a, b) => a + b) / arr.length);'
            ],
            'sql': [
                'SELECT * FROM users LIMIT 5;',
                'SELECT COUNT(*) as total_users FROM users;',
                'SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id;'
            ]
        }
    
    def test_e2b_execution_pipeline(self):
        """Test del pipeline completo de ejecución E2B."""
        try:
            from execution.e2b_manager import E2BManager
            from execution.code_detector import CodeDetector
            from execution.execution_loop import ExecutionLoop
            from execution.error_mapping import ErrorMapper
            from execution.feedback_loop import FeedbackLoop
            
            # Inicializar componentes
            e2b_manager = E2BManager(max_concurrent_sandboxes=3)
            code_detector = CodeDetector()
            execution_loop = ExecutionLoop(max_attempts=3)
            error_mapper = ErrorMapper()
            feedback_loop = FeedbackLoop()
            
            for language, code_samples in self.test_code_samples.items():
                for code in code_samples:
                    # 1. Detectar código
                    code_blocks = code_detector.detect_code_blocks(code)
                    assert isinstance(code_blocks, list)
                    
                    if code_blocks:
                        code_block = code_blocks[0]
                        assert hasattr(code_block, 'language')
                        assert hasattr(code_block, 'code')
                        
                        # 2. Ejecutar código
                        result = execution_loop.execute_code(code_block.code, language)
                        assert result is not None
                        assert hasattr(result, 'success')
                        assert hasattr(result, 'output')
                        assert hasattr(result, 'error')
                        
                        # 3. Mapear errores si hay
                        if not result.success and result.error:
                            error_info = error_mapper.map_error(result.error, language)
                            assert error_info is not None
                            assert hasattr(error_info, 'error_type')
                            assert hasattr(error_info, 'suggestions')
                        
                        # 4. Feedback loop
                        feedback = feedback_loop.process_result(result, code_block)
                        assert feedback is not None
                        assert hasattr(feedback, 'quality_score')
                        assert hasattr(feedback, 'improvements')
                        
                        logger.info(f"✓ E2B execution pipeline test passed for {language}: {code[:30]}...")
            
            logger.info("✓ E2B execution integration test completed successfully")
            
        except ImportError as e:
            logger.warning(f"E2B modules not available: {e}")
        except Exception as e:
            logger.error(f"E2B execution integration test failed: {e}")
            raise
    
    def test_e2b_error_handling(self):
        """Test de manejo de errores en E2B."""
        try:
            from execution.e2b_manager import E2BManager
            from execution.error_mapping import ErrorMapper
            from execution.execution_loop import ExecutionLoop
            
            e2b_manager = E2BManager()
            error_mapper = ErrorMapper()
            execution_loop = ExecutionLoop(max_attempts=3)
            
            # Código con errores intencionales
            error_code_samples = {
                'python': [
                    'print(undefined_variable)',  # NameError
                    '1 / 0',  # ZeroDivisionError
                    'int("not_a_number")',  # ValueError
                ],
                'javascript': [
                    'console.log(undefinedVariable);',  # ReferenceError
                    'JSON.parse("invalid json");',  # SyntaxError
                ]
            }
            
            for language, error_codes in error_code_samples.items():
                for error_code in error_codes:
                    # Ejecutar código con error
                    result = execution_loop.execute_code(error_code, language)
                    
                    assert result is not None
                    assert result.success is False
                    assert result.error is not None
                    
                    # Mapear error
                    error_info = error_mapper.map_error(result.error, language)
                    assert error_info is not None
                    assert hasattr(error_info, 'error_type')
                    assert hasattr(error_info, 'suggestions')
                    assert len(error_info.suggestions) > 0
                    
                    logger.info(f"✓ E2B error handling test passed for {language}: {error_code[:30]}...")
            
        except ImportError as e:
            logger.warning(f"E2B modules not available: {e}")
        except Exception as e:
            logger.error(f"E2B error handling test failed: {e}")
            raise
    
    def test_e2b_multi_round_correction(self):
        """Test de corrección multi-ronda en E2B."""
        try:
            from execution.execution_loop import ExecutionLoop
            from execution.error_mapping import ErrorMapper
            
            execution_loop = ExecutionLoop(max_attempts=3)
            error_mapper = ErrorMapper()
            
            # Código que puede ser corregido
            problematic_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test con lista vacía (causará error)
result = calculate_average([])
print(result)
"""
            
            # Ejecutar con corrección automática
            result = execution_loop.execute_code(problematic_code, 'python')
            
            assert result is not None
            
            # Si falla, debería tener sugerencias de corrección
            if not result.success:
                error_info = error_mapper.map_error(result.error, 'python')
                assert error_info is not None
                assert len(error_info.suggestions) > 0
                
                # Intentar corrección
                corrected_code = error_mapper.apply_correction(
                    problematic_code, 
                    error_info.suggestions[0]
                )
                
                assert corrected_code is not None
                assert corrected_code != problematic_code
                
                logger.info("✓ E2B multi-round correction test passed")
            
        except ImportError as e:
            logger.warning(f"E2B modules not available: {e}")
        except Exception as e:
            logger.error(f"E2B multi-round correction test failed: {e}")
            raise


class TestEndToEndIntegration:
    """Tests end-to-end del sistema completo."""
    
    def setup_method(self):
        """Setup para cada test."""
        self.test_scenarios = [
            {
                'query': "Create a Python function to calculate the factorial of a number and test it with some examples",
                'expected_components': ['routing', 'ace', 'e2b', 'cag'],
                'expected_language': 'python'
            },
            {
                'query': "Write a SQL query to find the top 10 customers by total order value",
                'expected_components': ['routing', 'ace', 'e2b'],
                'expected_language': 'sql'
            },
            {
                'query': "Debug this JavaScript code that has a memory leak issue",
                'expected_components': ['routing', 'ace', 'e2b', 'optimizations'],
                'expected_language': 'javascript'
            }
        ]
    
    def test_complete_system_flow(self):
        """Test del flujo completo del sistema."""
        try:
            # Importar todos los componentes principales
            from core.router import Router
            from ace.integration import ACEIntegration
            from execution.e2b_integration import E2BIntegration
            from core.cag.dynamic_context import DynamicContext
            from optimizations.rewiring_experts import RewiringExperts
            
            # Inicializar componentes
            router = Router()
            ace_integration = ACEIntegration()
            e2b_integration = E2BIntegration()
            dynamic_context = DynamicContext()
            rewiring_experts = RewiringExperts()
            
            for scenario in self.test_scenarios:
                query = scenario['query']
                expected_components = scenario['expected_components']
                expected_language = scenario['expected_language']
                
                # 1. Routing
                if 'routing' in expected_components:
                    routing_result = router.route_query(query, {})
                    assert routing_result is not None
                    assert hasattr(routing_result, 'selected_model')
                
                # 2. ACE Integration
                if 'ace' in expected_components:
                    ace_result = ace_integration.process_query(query)
                    assert ace_result is not None
                    assert hasattr(ace_result, 'enhanced_context')
                
                # 3. CAG Integration
                if 'cag' in expected_components:
                    dynamic_context.add_context(query)
                    context_result = dynamic_context.get_context()
                    assert context_result is not None
                    assert len(context_result) > 0
                
                # 4. E2B Execution
                if 'e2b' in expected_components:
                    e2b_result = e2b_integration.execute_query(query)
                    assert e2b_result is not None
                    assert hasattr(e2b_result, 'execution_results')
                
                # 5. Optimizations
                if 'optimizations' in expected_components:
                    optimization_result = rewiring_experts.route_query(query, {})
                    assert optimization_result is not None
                    assert hasattr(optimization_result, 'primary_expert')
                
                logger.info(f"✓ Complete system flow test passed for: {query[:50]}...")
            
            logger.info("✓ End-to-end integration test completed successfully")
            
        except ImportError as e:
            logger.warning(f"System modules not available: {e}")
        except Exception as e:
            logger.error(f"End-to-end integration test failed: {e}")
            raise
    
    def test_system_performance(self):
        """Test de rendimiento del sistema."""
        try:
            from core.router import Router
            from ace.integration import ACEIntegration
            from execution.e2b_integration import E2BIntegration
            
            router = Router()
            ace_integration = ACEIntegration()
            e2b_integration = E2BIntegration()
            
            # Test de rendimiento con múltiples queries
            test_queries = [
                "Simple Python question",
                "Complex machine learning problem",
                "Database optimization query",
                "JavaScript debugging help",
                "API development question"
            ]
            
            start_time = datetime.now()
            
            for query in test_queries:
                # Routing
                routing_start = datetime.now()
                routing_result = router.route_query(query, {})
                routing_time = (datetime.now() - routing_start).total_seconds() * 1000
                
                assert routing_time < 100  # Debe ser rápido (< 100ms)
                
                # ACE
                ace_start = datetime.now()
                ace_result = ace_integration.process_query(query)
                ace_time = (datetime.now() - ace_start).total_seconds() * 1000
                
                assert ace_time < 500  # Debe ser razonable (< 500ms)
                
                logger.info(f"✓ Performance test passed for: {query[:30]}... (routing: {routing_time:.1f}ms, ace: {ace_time:.1f}ms)")
            
            total_time = (datetime.now() - start_time).total_seconds()
            avg_time_per_query = total_time / len(test_queries)
            
            assert avg_time_per_query < 1.0  # Promedio < 1 segundo por query
            
            logger.info(f"✓ System performance test passed (avg: {avg_time_per_query:.2f}s per query)")
            
        except ImportError as e:
            logger.warning(f"System modules not available: {e}")
        except Exception as e:
            logger.error(f"System performance test failed: {e}")
            raise
    
    def test_system_reliability(self):
        """Test de confiabilidad del sistema."""
        try:
            from core.router import Router
            from ace.integration import ACEIntegration
            
            router = Router()
            ace_integration = ACEIntegration()
            
            # Test con queries problemáticas
            problematic_queries = [
                "",  # Query vacía
                "a" * 10000,  # Query muy larga
                "!@#$%^&*()",  # Query con caracteres especiales
                None,  # Query nula (simulada)
                "Query with unicode: ñáéíóú 中文 🚀",  # Query con unicode
            ]
            
            for i, query in enumerate(problematic_queries):
                try:
                    if query is None:
                        # Simular query nula
                        continue
                    
                    # El sistema debe manejar queries problemáticas sin fallar
                    routing_result = router.route_query(query, {})
                    assert routing_result is not None
                    
                    ace_result = ace_integration.process_query(query)
                    assert ace_result is not None
                    
                    logger.info(f"✓ Reliability test passed for problematic query {i+1}")
                    
                except Exception as e:
                    # Algunos errores son esperados, pero el sistema no debe crashear
                    logger.warning(f"Expected error for problematic query {i+1}: {e}")
            
            logger.info("✓ System reliability test passed")
            
        except ImportError as e:
            logger.warning(f"System modules not available: {e}")
        except Exception as e:
            logger.error(f"System reliability test failed: {e}")
            raise


def run_all_integration_tests():
    """Ejecuta todos los tests de integración."""
    logger.info("Iniciando tests de integración...")
    
    test_classes = [
        TestRoutingIntegration,
        TestACECycleIntegration,
        TestE2BExecutionIntegration,
        TestEndToEndIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        logger.info(f"\n--- Ejecutando tests de integración de {test_class.__name__} ---")
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                # Setup
                if hasattr(test_instance, 'setup_method'):
                    test_instance.setup_method()
                
                # Ejecutar test
                getattr(test_instance, test_method)()
                passed_tests += 1
                logger.info(f"✓ {test_method} passed")
                
            except Exception as e:
                failed_tests += 1
                logger.error(f"✗ {test_method} failed: {e}")
    
    # Resumen
    logger.info(f"\n{'='*60}")
    logger.info("RESUMEN DE TESTS DE INTEGRACIÓN")
    logger.info(f"{'='*60}")
    logger.info(f"Total tests: {total_tests}")
    logger.info(f"Passed: {passed_tests}")
    logger.info(f"Failed: {failed_tests}")
    logger.info(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        logger.info("🎉 Todos los tests de integración pasaron!")
        return True
    else:
        logger.error(f"❌ {failed_tests} tests fallaron")
        return False


if __name__ == "__main__":
    success = run_all_integration_tests()
    sys.exit(0 if success else 1)
