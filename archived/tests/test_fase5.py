#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para FASE 5: Metadata System
"""

import sys
import os
import logging
import asyncio
from datetime import datetime, timedelta

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metadata.metrics_collector import MetricsCollector, MetricType, MetricLevel, RoutingMetrics, MemoryMetrics, ComputeMetrics
from metadata.metrics_integration import MetricsIntegration
from metadata.timescaledb_manager import TimescaleDBManager
from metadata.metrics_pipeline import MetricsPipeline, MetricsAggregator
from metadata.metadata_system import MetadataSystem, initialize_metadata_system

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_metrics_collector():
    """Test del MetricsCollector."""
    try:
        logger.info("=== Test Metrics Collector ===")
        
        collector = MetricsCollector(buffer_size=1000, flush_interval=5)
        collector.start()
        
        # Test de métricas de routing
        routing_metrics = RoutingMetrics(
            query_id="test_query_001",
            query_text="How to optimize Python code?",
            complexity_score=0.8,
            confidence_score=0.9,
            model_selected="120B",
            routing_time_ms=50,
            embedding_time_ms=20,
            threshold_comparison_time_ms=5,
            total_routing_time_ms=75,
            tokens_estimated=1000,
            context_length=500,
            user_intent="optimization",
            domain_detected="python",
            timestamp=datetime.now()
        )
        
        success = collector.collect_routing_metrics(routing_metrics)
        print(f"Métricas de routing recolectadas: {success}")
        
        # Test de métricas de memoria
        memory_metrics = MemoryMetrics(
            agent_id="test_agent_001",
            memory_type="knowledge",
            memory_operation="write",
            memory_size_bytes=1024,
            memory_tokens=256,
            operation_time_ms=10,
            cache_hit=False,
            compression_ratio=0.0,
            importance_score=0.8,
            access_count=1,
            timestamp=datetime.now()
        )
        
        success = collector.collect_memory_metrics(memory_metrics)
        print(f"Métricas de memoria recolectadas: {success}")
        
        # Test de métricas de cómputo
        compute_metrics = ComputeMetrics(
            model_id="120B",
            operation_type="inference",
            batch_size=1,
            sequence_length=1000,
            tokens_processed=1000,
            computation_time_ms=2000,
            gpu_utilization_percent=85.0,
            gpu_memory_used_mb=8000.0,
            cpu_utilization_percent=20.0,
            cpu_memory_used_mb=2048.0,
            throughput_tokens_per_sec=500.0,
            latency_p50_ms=1800.0,
            latency_p95_ms=2200.0,
            latency_p99_ms=2500.0,
            timestamp=datetime.now()
        )
        
        success = collector.collect_compute_metrics(compute_metrics)
        print(f"Métricas de cómputo recolectadas: {success}")
        
        # Test de métricas individuales
        collector.collect_metric(
            MetricType.SYSTEM, "cpu_usage_percent", 75.5,
            MetricLevel.INFO, {"system": "capibara6"}
        )
        
        collector.collect_metric(
            MetricType.SYSTEM, "memory_usage_percent", 60.2,
            MetricLevel.INFO, {"system": "capibara6"}
        )
        
        # Esperar un poco para que se procesen las métricas
        import time
        time.sleep(6)
        
        # Mostrar estadísticas
        stats = collector.get_collector_stats()
        print(f"Estadísticas del collector: {stats}")
        
        # Detener collector
        collector.stop()
        
        logger.info("PASS - Metrics Collector test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Metrics Collector: {e}")
        return False


def test_metrics_integration():
    """Test del MetricsIntegration."""
    try:
        logger.info("=== Test Metrics Integration ===")
        
        collector = MetricsCollector(buffer_size=1000, flush_interval=5)
        collector.start()
        
        integration = MetricsIntegration(collector)
        
        # Test de tracking de routing
        with integration.track_routing("test_query_001", "How to optimize Python code?", "optimization"):
            import time
            time.sleep(0.1)  # Simular procesamiento
        
        # Test de tracking de memoria
        with integration.track_memory_read("test_agent_001", "knowledge") as cache_hit:
            time.sleep(0.05)  # Simular lectura
        
        # Test de tracking de cómputo
        with integration.track_model_inference("120B", batch_size=1) as (tokens, seq_len):
            tokens = 1000
            seq_len = 500
            time.sleep(0.2)  # Simular inferencia
        
        # Test de tracking de ejecución E2B
        with integration.track_e2b_execution("exec_001", "test_agent_001", "python", "print('Hello')") as (success, error, corrections, timeout):
            success = True
            time.sleep(0.1)  # Simular ejecución
        
        # Test de tracking de evolución de agente
        integration.track_agent_creation("test_agent_002", "python")
        integration.track_agent_graduation("test_agent_002", "python", 0.85, 150, 0.87)
        
        # Test de tracking de RAG
        with integration.track_rag_retrieval("rag_001", "mini_rag", "Python optimization") as (docs_ret, docs_rel, rel_score, ctx_len, ctx_tokens):
            docs_ret = 10
            docs_rel = 8
            rel_score = 0.8
            ctx_len = 500
            ctx_tokens = 200
            time.sleep(0.05)  # Simular retrieval
        
        # Test de métricas del sistema
        integration.track_system_metrics(
            cpu_usage_percent=25.0,
            memory_usage_percent=60.0,
            active_agents=5,
            total_requests=1000
        )
        
        # Esperar un poco para que se procesen las métricas
        time.sleep(6)
        
        # Mostrar estadísticas
        stats = integration.get_integration_stats()
        print(f"Estadísticas de integración: {stats}")
        
        collector_stats = collector.get_collector_stats()
        print(f"Estadísticas del collector: {collector_stats}")
        
        # Detener collector
        collector.stop()
        
        logger.info("PASS - Metrics Integration test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Metrics Integration: {e}")
        return False


def test_timescaledb_manager():
    """Test del TimescaleDBManager."""
    try:
        logger.info("=== Test TimescaleDB Manager ===")
        
        # Crear manager (sin conectar realmente)
        manager = TimescaleDBManager(
            host="localhost",
            port=5432,
            database="capibara6_metrics",
            username="postgres",
            password="password"
        )
        
        print(f"TimescaleDB Manager creado: {manager.host}:{manager.port}/{manager.database}")
        
        # Test de configuración de compresión
        print(f"Políticas de compresión: {manager.compression_policies}")
        
        # Test de estadísticas
        stats = manager.get_manager_stats()
        print(f"Estadísticas del manager: {stats}")
        
        # Simular inserción de métricas (sin conectar realmente)
        test_metrics = [
            {
                'time': datetime.now(),
                'query_id': 'test_001',
                'complexity_score': 0.8,
                'confidence_score': 0.9,
                'model_selected': '120B',
                'routing_time_ms': 50,
                'tags': {'test': 'true'},
                'metadata': {'source': 'test'}
            }
        ]
        
        print(f"Métricas de prueba preparadas: {len(test_metrics)}")
        
        logger.info("PASS - TimescaleDB Manager test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test TimescaleDB Manager: {e}")
        return False


async def test_metrics_pipeline():
    """Test del MetricsPipeline."""
    try:
        logger.info("=== Test Metrics Pipeline ===")
        
        # Crear manager de TimescaleDB (simulado)
        timescaledb_manager = TimescaleDBManager()
        
        # Crear pipeline
        pipeline = MetricsPipeline(timescaledb_manager)
        
        # Test de agregación diaria
        target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        success = await pipeline.run_pipeline(target_date)
        print(f"Pipeline ejecutado: {'exitoso' if success else 'fallido'}")
        
        # Test de generación de reporte
        report = await pipeline.aggregator.generate_daily_report(target_date)
        print(f"Reporte generado: {report.get('date', 'N/A')}")
        print(f"Resumen: {report.get('summary', {})}")
        
        # Mostrar estadísticas
        stats = pipeline.get_pipeline_stats()
        print(f"Estadísticas del pipeline: {stats}")
        
        logger.info("PASS - Metrics Pipeline test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Metrics Pipeline: {e}")
        return False


async def test_metadata_system():
    """Test del MetadataSystem completo."""
    try:
        logger.info("=== Test Metadata System ===")
        
        # Crear sistema de metadata
        metadata_system = MetadataSystem()
        
        # Inicializar (sin conectar realmente a TimescaleDB)
        print("Sistema de metadata creado")
        
        # Test de configuración
        print(f"Configuración TimescaleDB: {metadata_system.timescaledb_config}")
        print(f"Configuración Collector: {metadata_system.collector_config}")
        
        # Test de tracking (simulado)
        metadata_system.track_routing_decision(
            "test_query_001", 0.8, 0.9, "120B", 50, "python"
        )
        
        metadata_system.track_memory_operation(
            "test_agent_001", "knowledge", "write", 1024, 256, 10
        )
        
        metadata_system.track_compute_operation(
            "120B", "inference", 1, 1000, 1000, 2000, 85.0, 8000.0, 500.0, 2200.0
        )
        
        metadata_system.track_execution(
            "exec_001", "test_agent_001", "python", 100, 1000, 50.0, 25.0, True
        )
        
        metadata_system.track_agent_evolution(
            "test_agent_001", "python", "created", 0, 0.0, 0.0, 0.0, 0.0
        )
        
        metadata_system.track_rag_operation(
            "rag_001", "mini_rag", "Python optimization", 50, 10, 8, 0.8, 500, 200
        )
        
        metadata_system.track_system_metrics(
            cpu_usage_percent=25.0,
            memory_usage_percent=60.0,
            active_agents=5,
            total_requests=1000
        )
        
        print("Métricas de tracking simuladas")
        
        # Test de estado del sistema
        status = metadata_system.get_status()
        print(f"Estado del sistema: {status}")
        
        # Test de estadísticas
        stats = metadata_system.get_system_stats()
        print(f"Estadísticas del sistema: {stats}")
        
        # Test de health check
        health = await metadata_system.health_check()
        print(f"Health check: {health}")
        
        logger.info("PASS - Metadata System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Metadata System: {e}")
        return False


async def test_global_metadata_system():
    """Test del sistema global de metadata."""
    try:
        logger.info("=== Test Global Metadata System ===")
        
        # Inicializar sistema global
        metadata_system = initialize_metadata_system()
        print("Sistema global de metadata inicializado")
        
        # Test de funciones globales
        success = await start_metadata_system()
        print(f"Sistema global iniciado: {'exitoso' if success else 'fallido'}")
        
        # Obtener sistema global
        global_system = get_metadata_system()
        print(f"Sistema global obtenido: {global_system is not None}")
        
        if global_system:
            # Test de tracking
            global_system.track_routing_decision(
                "global_test_001", 0.7, 0.8, "20B", 30, "general"
            )
            
            global_system.track_system_metrics(
                cpu_usage_percent=30.0,
                memory_usage_percent=65.0,
                active_agents=3
            )
            
            print("Métricas globales simuladas")
            
            # Test de estado
            status = global_system.get_status()
            print(f"Estado global: {status}")
        
        # Detener sistema global
        success = await stop_metadata_system()
        print(f"Sistema global detenido: {'exitoso' if success else 'fallido'}")
        
        logger.info("PASS - Global Metadata System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Global Metadata System: {e}")
        return False


async def main():
    """Ejecuta todos los tests de FASE 5."""
    logger.info("Iniciando tests de FASE 5: Metadata System")
    
    tests = [
        ("Metrics Collector", test_metrics_collector),
        ("Metrics Integration", test_metrics_integration),
        ("TimescaleDB Manager", test_timescaledb_manager),
        ("Metrics Pipeline", test_metrics_pipeline),
        ("Metadata System", test_metadata_system),
        ("Global Metadata System", test_global_metadata_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"Ejecutando test: {test_name}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                success = await test_func()
            else:
                success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    logger.info("\n" + "="*50)
    logger.info("RESUMEN DE TESTS FASE 5")
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
        logger.info("Todos los tests de FASE 5 pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
