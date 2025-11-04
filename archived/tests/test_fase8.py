#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fase 8 - Test de escalabilidad y rendimiento.
"""

import logging
import json
import os
import sys
import asyncio
import numpy as np
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_quantization():
    """Test del sistema de cuantización."""
    logger.info("=== Test Quantization ===")
    
    try:
        from scalability.quantization import (
            QuantizationManager, 
            QuantizationMethod, 
            QuantizationConfig,
            QuantizationLevel
        )
        
        # Crear manager de cuantización
        manager = QuantizationManager()
        
        # Test de cuantización GPTQ
        test_model_path = "backend/models/capibara6_20b"
        gptq_result = manager.quantize_model(
            test_model_path,
            QuantizationMethod.GPTQ,
            config_name="gptq_4bit"
        )
        
        logger.info(f"GPTQ Result:")
        logger.info(f"  Compression Ratio: {gptq_result.compression_ratio:.1f}x")
        logger.info(f"  Speedup Factor: {gptq_result.speedup_factor:.1f}x")
        logger.info(f"  Accuracy Loss: {gptq_result.accuracy_loss:.3f}")
        logger.info(f"  Memory Reduction: {gptq_result.memory_reduction:.1%}")
        
        # Test de cuantización AWQ
        awq_result = manager.quantize_model(
            test_model_path,
            QuantizationMethod.AWQ,
            config_name="awq_4bit"
        )
        
        logger.info(f"AWQ Result:")
        logger.info(f"  Compression Ratio: {awq_result.compression_ratio:.1f}x")
        logger.info(f"  Speedup Factor: {awq_result.speedup_factor:.1f}x")
        logger.info(f"  Accuracy Loss: {awq_result.accuracy_loss:.3f}")
        logger.info(f"  Memory Reduction: {awq_result.memory_reduction:.1%}")
        
        # Test de benchmark
        test_data = [
            "How to optimize Python code?",
            "What is machine learning?",
            "Explain neural networks.",
            "How does attention work?",
            "What is quantization?"
        ]
        
        gptq_benchmark = manager.benchmark_quantized_model(gptq_result, test_data)
        logger.info(f"GPTQ Benchmark:")
        logger.info(f"  Inference Time: {gptq_benchmark.inference_time_ms:.1f}ms")
        logger.info(f"  Memory Usage: {gptq_benchmark.memory_usage_mb:.0f}MB")
        logger.info(f"  Throughput: {gptq_benchmark.throughput_tokens_per_second:.0f} tokens/s")
        logger.info(f"  Accuracy: {gptq_benchmark.accuracy_score:.3f}")
        
        # Test de comparación
        comparison = manager.compare_quantization_methods(test_model_path, test_data)
        logger.info(f"Comparison Results:")
        logger.info(f"  Best Balanced: {comparison['best_balanced']}")
        logger.info(f"  Best Compression: {comparison['best_compression']}")
        logger.info(f"  Best Speedup: {comparison['best_speedup']}")
        
        # Mostrar estadísticas
        stats = manager.get_quantization_stats()
        logger.info(f"Statistics: {stats}")
        
        logger.info("PASS - Quantization")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Quantization: {e}")
        return False

async def test_dynamic_batching():
    """Test del sistema de dynamic batching."""
    logger.info("=== Test Dynamic Batching ===")
    
    try:
        from scalability.dynamic_batching import (
            DynamicBatcher, 
            BatchStrategy, 
            RequestPriority
        )
        
        # Crear batcher
        batcher = DynamicBatcher(
            strategy=BatchStrategy.ADAPTIVE,
            max_batch_size=8,
            max_wait_time_ms=100
        )
        
        # Iniciar procesamiento
        await batcher.start_processing()
        
        # Enviar requests de prueba
        test_requests = [
            ("How to optimize Python code?", RequestPriority.HIGH),
            ("What is machine learning?", RequestPriority.MEDIUM),
            ("Explain neural networks.", RequestPriority.MEDIUM),
            ("How does attention work?", RequestPriority.LOW),
            ("What is quantization?", RequestPriority.HIGH),
            ("Optimize this algorithm.", RequestPriority.CRITICAL),
            ("Debug this code.", RequestPriority.HIGH),
            ("Train a model.", RequestPriority.MEDIUM)
        ]
        
        request_ids = []
        for content, priority in test_requests:
            request_id = await batcher.submit_request(
                content=content,
                priority=priority,
                max_wait_time_ms=500
            )
            request_ids.append(request_id)
            await asyncio.sleep(0.01)  # 10ms entre requests
        
        # Esperar procesamiento
        await asyncio.sleep(2.0)
        
        # Mostrar métricas
        metrics = batcher.get_batch_metrics()
        logger.info(f"Batch Metrics:")
        logger.info(f"  Total Batches: {metrics.total_batches}")
        logger.info(f"  Total Requests: {metrics.total_requests}")
        logger.info(f"  Average Batch Size: {metrics.average_batch_size:.1f}")
        logger.info(f"  Average Processing Time: {metrics.average_processing_time_ms:.1f}ms")
        logger.info(f"  Average Throughput: {metrics.average_throughput_tokens_per_second:.0f} tokens/s")
        logger.info(f"  Average Wait Time: {metrics.average_wait_time_ms:.1f}ms")
        logger.info(f"  Batch Efficiency: {metrics.batch_efficiency:.2f}")
        logger.info(f"  Queue Length: {metrics.queue_length}")
        logger.info(f"  Processing Rate: {metrics.processing_rate:.1f} req/s")
        
        # Mostrar estadísticas
        stats = batcher.get_batcher_stats()
        logger.info(f"Batcher Stats: {stats}")
        
        # Detener procesamiento
        await batcher.stop_processing()
        
        logger.info("PASS - Dynamic Batching")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Dynamic Batching: {e}")
        return False

def test_aggressive_caching():
    """Test del sistema de aggressive caching."""
    logger.info("=== Test Aggressive Caching ===")
    
    try:
        from scalability.aggressive_caching import (
            AggressiveCache, 
            CacheStrategy, 
            CacheType
        )
        
        # Crear caché
        cache = AggressiveCache(
            l1_size_mb=100,  # 100MB para test
            l2_size_mb=500,  # 500MB para test
            strategy=CacheStrategy.ADAPTIVE
        )
        
        # Test de operaciones básicas
        test_data = {
            "query_1": "How to optimize Python code?",
            "query_2": "What is machine learning?",
            "embedding_1": np.random.randn(768),
            "computation_1": {"result": 42, "metadata": {"time": 1.5}},
            "metadata_1": {"version": "1.0", "timestamp": datetime.now().isoformat()}
        }
        
        # Establecer valores
        for key, value in test_data.items():
            cache_type = CacheType.QUERY_RESULT
            if "embedding" in key:
                cache_type = CacheType.EMBEDDING
            elif "computation" in key:
                cache_type = CacheType.COMPUTATION
            elif "metadata" in key:
                cache_type = CacheType.METADATA
            
            success = cache.set(key, value, cache_type)
            logger.info(f"Set {key}: {'Success' if success else 'Failed'}")
        
        # Obtener valores
        for key in test_data.keys():
            value = cache.get(key)
            logger.info(f"Get {key}: {'Found' if value is not None else 'Not found'}")
        
        # Test de generación de clave
        cache_key = cache.generate_cache_key("test_function", arg1="value1", arg2=42)
        logger.info(f"Generated cache key: {cache_key}")
        
        # Mostrar estadísticas
        stats = cache.get_cache_stats()
        logger.info(f"Cache Statistics:")
        logger.info(f"  Overall Hit Rate: {stats['overall']['overall_hit_rate']:.2%}")
        logger.info(f"  L1 Hit Rate: {stats['overall']['l1_hit_rate']:.2%}")
        logger.info(f"  L2 Hit Rate: {stats['overall']['l2_hit_rate']:.2%}")
        logger.info(f"  Average Access Time: {stats['overall']['average_access_time_ms']:.2f}ms")
        logger.info(f"  L1 Utilization: {stats['l1_cache']['utilization_percentage']:.1f}%")
        logger.info(f"  L2 Utilization: {stats['l2_cache']['utilization_percentage']:.1f}%")
        
        # Cerrar caché
        cache.shutdown()
        
        logger.info("PASS - Aggressive Caching")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Aggressive Caching: {e}")
        return False

def test_rag_index_optimization():
    """Test del sistema de RAG index optimization."""
    logger.info("=== Test RAG Index Optimization ===")
    
    try:
        from scalability.rag_index_optimization import (
            RAGIndexOptimizer, 
            OptimizationStrategy
        )
        
        # Crear optimizador
        optimizer = RAGIndexOptimizer()
        
        # Generar datos de prueba
        num_vectors = 1000  # Reducido para test
        dimension = 768
        vectors = np.random.randn(num_vectors, dimension).astype(np.float32)
        
        logger.info(f"Generados {num_vectors} vectores de dimensión {dimension}")
        
        # Construir diferentes tipos de índices
        index_configs = [
            ("flat_index", OptimizationStrategy.ACCURACY),
            ("ivf_index", OptimizationStrategy.SPEED),
            ("hnsw_index", OptimizationStrategy.BALANCED),
            ("pq_index", OptimizationStrategy.MEMORY)
        ]
        
        built_indices = []
        for index_name, strategy in index_configs:
            try:
                result = optimizer.build_optimized_index(vectors, index_name, strategy)
                built_indices.append(result)
                logger.info(f"Índice {index_name} construido exitosamente")
            except Exception as e:
                logger.error(f"Error construyendo {index_name}: {e}")
        
        # Comparar índices
        if len(built_indices) > 1:
            test_vectors = vectors[:50]  # Usar primeros 50 vectores para test
            comparison = optimizer.compare_indices(built_indices, test_vectors, num_queries=20)
            
            logger.info(f"Comparación de índices:")
            for index_name, data in comparison['results'].items():
                logger.info(f"  {index_name}:")
                logger.info(f"    Tiempo de búsqueda: {data['average_search_time_ms']:.2f}ms")
                logger.info(f"    Precisión: {data['average_accuracy']:.3f}")
                logger.info(f"    Throughput: {data['throughput_queries_per_second']:.1f} queries/s")
            
            logger.info(f"Análisis:")
            for recommendation in comparison['analysis']['recommendations']:
                logger.info(f"  - {recommendation}")
        
        # Test de búsqueda
        if built_indices:
            test_query = vectors[0]  # Usar primer vector como query
            result = optimizer.search(test_query, built_indices[0], k=5)
            
            logger.info(f"Resultado de búsqueda:")
            logger.info(f"  Query ID: {result.query_id}")
            logger.info(f"  Tiempo: {result.search_time_ms:.2f}ms")
            logger.info(f"  Resultados: {len(result.results)}")
            for i, (idx, dist) in enumerate(result.results):
                logger.info(f"    {i+1}. ID: {idx}, Distancia: {dist:.3f}")
        
        # Mostrar estadísticas
        stats = optimizer.get_optimizer_stats()
        logger.info(f"Estadísticas del optimizador:")
        logger.info(f"  Índices construidos: {stats['optimizer_stats']['total_indices_built']}")
        logger.info(f"  Vectores indexados: {stats['optimizer_stats']['total_vectors_indexed']}")
        logger.info(f"  Tiempo promedio de construcción: {stats['optimizer_stats']['average_build_time_seconds']:.2f}s")
        logger.info(f"  Tiempo promedio de búsqueda: {stats['optimizer_stats']['average_search_time_ms']:.2f}ms")
        
        logger.info("PASS - RAG Index Optimization")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - RAG Index Optimization: {e}")
        return False

async def test_integration_scalability():
    """Test de integración de escalabilidad."""
    logger.info("=== Test Integración de Escalabilidad ===")
    
    try:
        # Crear directorios necesarios
        os.makedirs("backend/data/scalability", exist_ok=True)
        os.makedirs("backend/models", exist_ok=True)
        os.makedirs("backend/data/cache", exist_ok=True)
        os.makedirs("backend/data/rag_indices", exist_ok=True)
        
        logger.info("Directorios de escalabilidad creados")
        
        # Test completo del pipeline de escalabilidad
        from scalability.quantization import QuantizationManager, QuantizationMethod
        from scalability.dynamic_batching import DynamicBatcher, BatchStrategy, RequestPriority
        from scalability.aggressive_caching import AggressiveCache, CacheStrategy, CacheType
        from scalability.rag_index_optimization import RAGIndexOptimizer, OptimizationStrategy
        
        # 1. Inicializar sistemas
        quantization_manager = QuantizationManager()
        batcher = DynamicBatcher(strategy=BatchStrategy.ADAPTIVE, max_batch_size=4)
        cache = AggressiveCache(l1_size_mb=50, l2_size_mb=200, strategy=CacheStrategy.ADAPTIVE)
        rag_optimizer = RAGIndexOptimizer()
        
        logger.info("1. Sistemas de escalabilidad inicializados")
        
        # 2. Cuantizar modelo
        test_model_path = "backend/models/capibara6_20b"
        quantized_result = quantization_manager.quantize_model(
            test_model_path,
            QuantizationMethod.GPTQ,
            config_name="gptq_4bit"
        )
        
        logger.info(f"2. Modelo cuantizado:")
        logger.info(f"   Compression Ratio: {quantized_result.compression_ratio:.1f}x")
        logger.info(f"   Speedup Factor: {quantized_result.speedup_factor:.1f}x")
        logger.info(f"   Memory Reduction: {quantized_result.memory_reduction:.1%}")
        
        # 3. Almacenar en caché
        cache_key = cache.generate_cache_key("quantized_model", model_path=test_model_path)
        cache_success = cache.set(
            cache_key, 
            {"model_path": quantized_result.quantized_model_path, "config": "gptq_4bit"}, 
            CacheType.MODEL_OUTPUT
        )
        
        logger.info(f"3. Modelo cuantizado almacenado en caché: {'Success' if cache_success else 'Failed'}")
        
        # 4. Iniciar batching
        await batcher.start_processing()
        
        # 5. Enviar requests de procesamiento
        processing_requests = [
            ("Process query: How to optimize AI models?", RequestPriority.HIGH),
            ("Process query: What is quantization?", RequestPriority.MEDIUM),
            ("Process query: Explain dynamic batching", RequestPriority.MEDIUM),
            ("Process query: How does caching work?", RequestPriority.LOW)
        ]
        
        request_ids = []
        for content, priority in processing_requests:
            request_id = await batcher.submit_request(
                content=content,
                priority=priority,
                max_wait_time_ms=1000
            )
            request_ids.append(request_id)
            await asyncio.sleep(0.01)
        
        logger.info(f"4. {len(request_ids)} requests enviados para procesamiento")
        
        # 6. Crear índice RAG optimizado
        num_vectors = 500  # Reducido para test
        dimension = 768
        vectors = np.random.randn(num_vectors, dimension).astype(np.float32)
        
        rag_index_name = rag_optimizer.build_optimized_index(
            vectors, 
            "scalability_test_index", 
            OptimizationStrategy.BALANCED
        )
        
        logger.info(f"5. Índice RAG optimizado creado: {rag_index_name}")
        
        # 7. Test de búsqueda en índice
        test_query = vectors[0]
        search_result = rag_optimizer.search(test_query, rag_index_name, k=3)
        
        logger.info(f"6. Búsqueda en índice RAG:")
        logger.info(f"   Tiempo: {search_result.search_time_ms:.2f}ms")
        logger.info(f"   Resultados: {len(search_result.results)}")
        
        # 8. Esperar procesamiento de batches
        await asyncio.sleep(1.0)
        
        # 9. Mostrar métricas finales
        batch_metrics = batcher.get_batch_metrics()
        cache_stats = cache.get_cache_stats()
        rag_stats = rag_optimizer.get_optimizer_stats()
        quant_stats = quantization_manager.get_quantization_stats()
        
        logger.info(f"7. Métricas finales:")
        logger.info(f"   Batches procesados: {batch_metrics.total_batches}")
        logger.info(f"   Requests procesados: {batch_metrics.total_requests}")
        logger.info(f"   Cache hit rate: {cache_stats['overall']['overall_hit_rate']:.2%}")
        logger.info(f"   Índices RAG: {rag_stats['total_active_indices']}")
        logger.info(f"   Modelos cuantizados: {quant_stats['total_models_quantized']}")
        
        # 10. Limpiar
        await batcher.stop_processing()
        cache.shutdown()
        
        logger.info("PASS - Integración de Escalabilidad")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Integración de Escalabilidad: {e}")
        return False

async def main():
    """Función principal de test."""
    logger.info("Iniciando tests de Fase 8 - Scalability & Performance")
    
    tests = [
        ("Quantization", test_quantization),
        ("Dynamic Batching", test_dynamic_batching),
        ("Aggressive Caching", test_aggressive_caching),
        ("RAG Index Optimization", test_rag_index_optimization),
        ("Integración de Escalabilidad", test_integration_scalability)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Ejecutando test: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    logger.info(f"\n{'='*60}")
    logger.info("RESUMEN DE TESTS - FASE 8")
    logger.info(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nResultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("🎉 Todos los tests de Fase 8 pasaron exitosamente!")
        logger.info("🚀 Sistema de escalabilidad y rendimiento completamente funcional!")
        return True
    else:
        logger.error(f"❌ {total - passed} tests fallaron")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
