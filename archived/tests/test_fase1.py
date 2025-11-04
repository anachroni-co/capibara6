#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para FASE 1: Componentes Core
"""

import logging
import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_router():
    """Test del RouterModel20B."""
    try:
        from core.router import RouterModel20B
        
        logger.info("=== Test RouterModel20B ===")
        
        # Crear router
        router = RouterModel20B()
        
        # Test queries
        test_queries = [
            "¿Qué es Python?",
            "Explica la teoría de cuerdas y su relación con la física cuántica",
            "¿Cómo implementar un algoritmo de machine learning distribuido?",
            "Ayuda con mi código",
            "Compara las arquitecturas de microservicios vs monolíticas"
        ]
        
        for query in test_queries:
            decision = router.should_escalate(query)
            print(f"Query: {query[:50]}...")
            print(f"Decisión: {'120B' if decision else '20B'}")
            print("-" * 50)
        
        # Test estadísticas
        stats = router.get_routing_stats()
        print(f"Estadísticas del router: {stats}")
        
        logger.info("PASS - RouterModel20B test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test RouterModel20B: {e}")
        return False


def test_embeddings():
    """Test del modelo de embeddings."""
    try:
        from core.embeddings import EmbeddingModel, DomainEmbeddingAnalyzer
        
        logger.info("=== Test EmbeddingModel ===")
        
        # Crear modelo de embeddings
        model = EmbeddingModel()
        
        # Test similitud
        text1 = "¿Cómo implementar una API REST en Python?"
        text2 = "Crear un endpoint web con Flask"
        similarity = model.similarity(text1, text2)
        print(f"Similitud: {similarity:.3f}")
        
        # Test búsqueda de similares
        candidates = [
            "Python es un lenguaje de programación",
            "JavaScript se usa para desarrollo web",
            "SQL es para bases de datos"
        ]
        results = model.find_most_similar(text1, candidates, top_k=2)
        print(f"Resultados similares: {len(results)}")
        
        # Test analizador de dominios
        analyzer = DomainEmbeddingAnalyzer(model)
        domain, confidence = analyzer.get_primary_domain(text1)
        print(f"Dominio: {domain}, Confianza: {confidence:.3f}")
        
        # Test estadísticas
        stats = model.get_cache_stats()
        print(f"Estadísticas del modelo: {stats}")
        
        logger.info("PASS - EmbeddingModel test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test EmbeddingModel: {e}")
        return False


def test_thresholds():
    """Test del sistema de umbrales."""
    try:
        from core.thresholds import ThresholdManager, AdaptiveThresholds
        
        logger.info("=== Test ThresholdManager ===")
        
        # Crear gestor de umbrales
        manager = ThresholdManager()
        
        # Mostrar información
        info = manager.get_threshold_info()
        print("Umbrales actuales:")
        for name, details in list(info.items())[:3]:  # Solo primeros 3
            print(f"  {name}: {details['value']}")
        
        # Test adaptativo
        adaptive = AdaptiveThresholds(manager)
        
        # Simular algunos registros de performance
        for i in range(5):
            adaptive.record_performance(
                complexity=0.5 + i * 0.1,
                domain_conf=0.6 + i * 0.05,
                success=True,
                latency_ms=1000 + i * 100,
                model_used='20B' if i % 2 == 0 else '120B'
            )
        
        print("Umbrales después de adaptación:")
        updated_info = manager.get_threshold_info()
        for name, details in list(updated_info.items())[:3]:
            print(f"  {name}: {details['value']}")
        
        logger.info("PASS - ThresholdManager test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ThresholdManager: {e}")
        return False


def test_cag():
    """Test del sistema CAG."""
    try:
        from core.cag.static_cache import StaticCache
        from core.cag.dynamic_context import DynamicContext
        from core.cag.awareness_gate import AwarenessGate
        from core.cag.mini_cag import MiniCAG
        from core.cag.full_cag import FullCAG
        
        logger.info("=== Test CAG System ===")
        
        # Crear componentes CAG
        static_cache = StaticCache()
        dynamic_context = DynamicContext()
        awareness_gate = AwarenessGate()
        
        # Test StaticCache
        context = static_cache.retrieve("python programming", max_tokens=200)
        print(f"StaticCache: {len(context)} caracteres recuperados")
        
        # Test DynamicContext
        dynamic_context.add_context(
            "Python es un lenguaje de programación interpretado",
            source="test",
            metadata={"category": "programming"}
        )
        dynamic_result = dynamic_context.get_context("python", max_tokens=100)
        print(f"DynamicContext: {len(dynamic_result)} caracteres")
        
        # Test AwarenessGate
        decision = awareness_gate.decide_sources("¿Qué es Python?", 1000)
        print(f"AwarenessGate: {decision['sources']}")
        
        # Test MiniCAG
        mini_cag = MiniCAG(static_cache, dynamic_context, awareness_gate)
        mini_result = mini_cag.generate_context("¿Qué es Python?")
        print(f"MiniCAG: {mini_result['tokens_used']} tokens, {mini_result['latency_ms']:.1f}ms")
        
        # Test FullCAG
        full_cag = FullCAG(static_cache, dynamic_context, awareness_gate)
        full_result = full_cag.generate_context("¿Qué es Python?")
        print(f"FullCAG: {full_result['tokens_used']} tokens, {full_result['latency_ms']:.1f}ms")
        
        logger.info("PASS - CAG System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test CAG System: {e}")
        return False


def test_rag():
    """Test del sistema RAG."""
    try:
        from core.rag.vector_store import VectorStore, Document
        from core.rag.mini_rag import MiniRAG
        from core.rag.full_rag import FullRAG
        from core.rag.guided_search import GuidedSearch
        
        logger.info("=== Test RAG System ===")
        
        # Crear vector store
        vector_store = VectorStore("basic")  # Usar implementación básica
        
        # Crear documentos de prueba
        docs = [
            Document("Python es un lenguaje de programación interpretado", {"category": "programming"}),
            Document("JavaScript se usa para desarrollo web", {"category": "programming"}),
            Document("SQL es para bases de datos relacionales", {"category": "database"})
        ]
        
        # Embeddings simulados
        import numpy as np
        embeddings = np.random.rand(len(docs), 384)
        
        # Agregar documentos
        vector_store.add_documents(docs, embeddings)
        print(f"VectorStore: {len(docs)} documentos agregados")
        
        # Test MiniRAG
        mini_rag = MiniRAG(vector_store)
        mini_results = mini_rag.search("python programming", k=2)
        print(f"MiniRAG: {len(mini_results)} resultados")
        
        # Test FullRAG
        full_rag = FullRAG(vector_store, mini_rag=mini_rag)
        full_results = full_rag.search("python programming", mini_results)
        print(f"FullRAG: {len(full_results)} resultados")
        
        # Test GuidedSearch
        guided_search = GuidedSearch(mini_rag, full_rag)
        guided_result = guided_search.search("python programming")
        print(f"GuidedSearch: {guided_result['total_results']} resultados, "
              f"estrategia: {guided_result['search_strategy']}")
        
        logger.info("PASS - RAG System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test RAG System: {e}")
        return False


def test_logging():
    """Test del sistema de logging."""
    try:
        from utils.logging_config import setup_logging, get_logger
        
        logger.info("=== Test Logging System ===")
        
        # Setup logging
        main_logger = setup_logging("backend/logs", "INFO")
        
        # Test diferentes tipos de log
        router_logger = get_logger('router')
        router_logger.info("Test router logger")
        
        # Test logging de decisión
        main_logger.log_routing_decision(
            query_hash="abc123",
            complexity=0.8,
            domain_conf=0.6,
            decision="escalate",
            model_used="120B",
            latency_ms=1500,
            success=True
        )
        
        # Test stats
        stats = main_logger.get_log_stats()
        print(f"Log stats: {len(stats.get('log_files', []))} archivos")
        
        logger.info("PASS - Logging System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Logging System: {e}")
        return False


def main():
    """Ejecuta todos los tests de FASE 1."""
    logger.info("Iniciando tests de FASE 1: Componentes Core")
    
    tests = [
        ("Router", test_router),
        ("Embeddings", test_embeddings),
        ("Thresholds", test_thresholds),
        ("CAG", test_cag),
        ("RAG", test_rag),
        ("Logging", test_logging)
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
    logger.info("RESUMEN DE TESTS FASE 1")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name:15} {status}")
        if success:
            passed += 1
    
    logger.info("-" * 50)
    logger.info(f"Total: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("Todos los tests de FASE 1 pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
