#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metadata System - Sistema completo de captura y procesamiento de metadata.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

from .metrics_collector import MetricsCollector, MetricType
from .metrics_integration import MetricsIntegration
from .timescaledb_manager import TimescaleDBManager
from .metrics_pipeline import MetricsPipeline

logger = logging.getLogger(__name__)


class MetadataSystem:
    """Sistema completo de metadata del sistema Capibara6."""
    
    def __init__(self, 
                 timescaledb_config: Dict[str, Any] = None,
                 collector_config: Dict[str, Any] = None):
        # Configuración por defecto
        self.timescaledb_config = timescaledb_config or {
            'host': os.getenv('TIMESCALEDB_HOST', 'localhost'),
            'port': int(os.getenv('TIMESCALEDB_PORT', '5432')),
            'database': os.getenv('TIMESCALEDB_DATABASE', 'capibara6_metrics'),
            'username': os.getenv('TIMESCALEDB_USERNAME', 'postgres'),
            'password': os.getenv('TIMESCALEDB_PASSWORD', 'password')
        }
        
        self.collector_config = collector_config or {
            'buffer_size': int(os.getenv('METRICS_BUFFER_SIZE', '10000')),
            'flush_interval': int(os.getenv('METRICS_FLUSH_INTERVAL', '30')),
            'enable_system_metrics': os.getenv('ENABLE_SYSTEM_METRICS', 'true').lower() == 'true'
        }
        
        # Inicializar componentes
        self.timescaledb_manager = None
        self.metrics_collector = None
        self.metrics_integration = None
        self.metrics_pipeline = None
        
        self.is_initialized = False
        self.is_running = False
        
        # Estadísticas del sistema
        self.system_stats = {
            'total_metrics_collected': 0,
            'total_metrics_stored': 0,
            'total_anomalies_detected': 0,
            'total_reports_generated': 0,
            'system_uptime_seconds': 0,
            'last_health_check': None,
            'health_status': 'unknown'
        }
        
        logger.info("MetadataSystem inicializado")
    
    async def initialize(self) -> bool:
        """Inicializa el sistema de metadata."""
        try:
            logger.info("Inicializando sistema de metadata...")
            
            # Inicializar TimescaleDB Manager
            self.timescaledb_manager = TimescaleDBManager(**self.timescaledb_config)
            
            if not self.timescaledb_manager.connect():
                logger.error("Error conectando a TimescaleDB")
                return False
            
            # Inicializar Metrics Collector
            self.metrics_collector = MetricsCollector(**self.collector_config)
            self.metrics_collector.start()
            
            # Inicializar Metrics Integration
            self.metrics_integration = MetricsIntegration(self.metrics_collector)
            
            # Inicializar Metrics Pipeline
            self.metrics_pipeline = MetricsPipeline(self.timescaledb_manager)
            
            self.is_initialized = True
            self.system_stats['last_health_check'] = datetime.now()
            self.system_stats['health_status'] = 'healthy'
            
            logger.info("Sistema de metadata inicializado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando sistema de metadata: {e}")
            self.system_stats['health_status'] = 'error'
            return False
    
    async def start(self) -> bool:
        """Inicia el sistema de metadata."""
        if not self.is_initialized:
            if not await self.initialize():
                return False
        
        if self.is_running:
            logger.warning("Sistema de metadata ya está ejecutándose")
            return True
        
        try:
            self.is_running = True
            logger.info("Sistema de metadata iniciado")
            return True
            
        except Exception as e:
            logger.error(f"Error iniciando sistema de metadata: {e}")
            self.is_running = False
            return False
    
    async def stop(self) -> bool:
        """Detiene el sistema de metadata."""
        if not self.is_running:
            return True
        
        try:
            # Detener collector
            if self.metrics_collector:
                self.metrics_collector.stop()
            
            # Desconectar de TimescaleDB
            if self.timescaledb_manager:
                self.timescaledb_manager.disconnect()
            
            self.is_running = False
            logger.info("Sistema de metadata detenido")
            return True
            
        except Exception as e:
            logger.error(f"Error deteniendo sistema de metadata: {e}")
            return False
    
    # ===== MÉTODOS DE INTEGRACIÓN =====
    
    def track_routing_decision(self, 
                             query_id: str,
                             complexity_score: float,
                             confidence_score: float,
                             model_selected: str,
                             routing_time_ms: int,
                             domain_detected: str = ""):
        """Track de decisión de routing."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_router_decision(
            query_id, complexity_score, confidence_score, 
            model_selected, routing_time_ms, domain_detected
        )
    
    def track_memory_operation(self,
                             agent_id: str,
                             memory_type: str,
                             operation: str,
                             memory_size_bytes: int,
                             memory_tokens: int,
                             operation_time_ms: int,
                             cache_hit: bool = False,
                             compression_ratio: float = 0.0,
                             importance_score: float = 0.5):
        """Track de operación de memoria."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_memory_operation(
            agent_id, memory_type, operation, memory_size_bytes,
            memory_tokens, operation_time_ms, cache_hit, compression_ratio, importance_score
        )
    
    def track_compute_operation(self,
                              model_id: str,
                              operation_type: str,
                              batch_size: int,
                              sequence_length: int,
                              tokens_processed: int,
                              computation_time_ms: int,
                              gpu_utilization_percent: float = 0.0,
                              gpu_memory_used_mb: float = 0.0,
                              throughput_tokens_per_sec: float = 0.0,
                              latency_p95_ms: float = 0.0):
        """Track de operación de cómputo."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_compute_operation(
            model_id, operation_type, batch_size, sequence_length,
            tokens_processed, computation_time_ms, gpu_utilization_percent,
            gpu_memory_used_mb, throughput_tokens_per_sec, latency_p95_ms
        )
    
    def track_execution(self,
                       execution_id: str,
                       agent_id: str,
                       language: str,
                       code_length: int,
                       execution_time_ms: int,
                       memory_used_mb: float,
                       cpu_used_percent: float,
                       success: bool,
                       error_type: str = "",
                       corrections_applied: int = 0):
        """Track de ejecución E2B."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_execution(
            execution_id, agent_id, language, code_length,
            execution_time_ms, memory_used_mb, cpu_used_percent,
            success, error_type, corrections_applied
        )
    
    def track_agent_evolution(self,
                            agent_id: str,
                            domain: str,
                            evolution_event: str,
                            interactions_count: int,
                            success_rate: float,
                            graduation_score: float,
                            memory_utilization: float,
                            domain_expertise: float):
        """Track de evolución de agente."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_agent_evolution(
            agent_id, domain, evolution_event, interactions_count,
            success_rate, graduation_score, memory_utilization, domain_expertise
        )
    
    def track_rag_operation(self,
                          query_id: str,
                          rag_type: str,
                          query_text: str,
                          retrieval_time_ms: int,
                          documents_retrieved: int,
                          documents_relevant: int,
                          relevance_score: float,
                          context_length: int,
                          context_tokens: int):
        """Track de operación RAG."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_rag_operation(
            query_id, rag_type, query_text, retrieval_time_ms,
            documents_retrieved, documents_relevant, relevance_score,
            context_length, context_tokens
        )
    
    def track_system_metrics(self,
                           cpu_usage_percent: float = 0.0,
                           memory_usage_percent: float = 0.0,
                           disk_usage_percent: float = 0.0,
                           active_agents: int = 0,
                           total_requests: int = 0,
                           error_rate: float = 0.0,
                           response_time_avg_ms: float = 0.0):
        """Track de métricas del sistema."""
        if not self.is_running or not self.metrics_integration:
            return False
        
        return self.metrics_integration.track_system_metrics(
            cpu_usage_percent=cpu_usage_percent,
            memory_usage_percent=memory_usage_percent,
            disk_usage_percent=disk_usage_percent,
            active_agents=active_agents,
            total_requests=total_requests,
            error_rate=error_rate,
            response_time_avg_ms=response_time_avg_ms
        )
    
    # ===== MÉTODOS DE PIPELINE =====
    
    async def run_daily_aggregation(self, target_date: Optional[datetime] = None) -> bool:
        """Ejecuta agregación diaria de métricas."""
        if not self.is_running or not self.metrics_pipeline:
            return False
        
        return await self.metrics_pipeline.run_pipeline(target_date)
    
    async def generate_daily_report(self, target_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Genera reporte diario de métricas."""
        if not self.is_running or not self.metrics_pipeline:
            return {}
        
        return await self.metrics_pipeline.aggregator.generate_daily_report(target_date)
    
    # ===== MÉTODOS DE CONSULTA =====
    
    def query_metrics(self, 
                     table_name: str,
                     start_time: datetime,
                     end_time: datetime,
                     filters: Dict[str, Any] = None,
                     limit: int = 1000) -> List[Dict[str, Any]]:
        """Consulta métricas de una tabla específica."""
        if not self.is_running or not self.timescaledb_manager:
            return []
        
        return self.timescaledb_manager.query_metrics(table_name, start_time, end_time, filters, limit)
    
    def get_aggregated_metrics(self,
                             table_name: str,
                             start_time: datetime,
                             end_time: datetime,
                             group_by: str = "1 hour",
                             aggregation: str = "avg") -> List[Dict[str, Any]]:
        """Obtiene métricas agregadas."""
        if not self.is_running or not self.timescaledb_manager:
            return []
        
        return self.timescaledb_manager.get_aggregated_metrics(table_name, start_time, end_time, group_by, aggregation)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la base de datos."""
        if not self.is_running or not self.timescaledb_manager:
            return {}
        
        return self.timescaledb_manager.get_database_stats()
    
    # ===== MÉTODOS DE MONITOREO =====
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica la salud del sistema de metadata."""
        try:
            health_status = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'components': {},
                'metrics': {}
            }
            
            # Verificar TimescaleDB
            if self.timescaledb_manager and self.timescaledb_manager.is_connected:
                health_status['components']['timescaledb'] = 'healthy'
            else:
                health_status['components']['timescaledb'] = 'unhealthy'
                health_status['status'] = 'degraded'
            
            # Verificar Metrics Collector
            if self.metrics_collector and self.metrics_collector.is_running:
                health_status['components']['metrics_collector'] = 'healthy'
            else:
                health_status['components']['metrics_collector'] = 'unhealthy'
                health_status['status'] = 'degraded'
            
            # Verificar Metrics Integration
            if self.metrics_integration:
                health_status['components']['metrics_integration'] = 'healthy'
            else:
                health_status['components']['metrics_integration'] = 'unhealthy'
                health_status['status'] = 'degraded'
            
            # Verificar Metrics Pipeline
            if self.metrics_pipeline:
                health_status['components']['metrics_pipeline'] = 'healthy'
            else:
                health_status['components']['metrics_pipeline'] = 'unhealthy'
                health_status['status'] = 'degraded'
            
            # Métricas del sistema
            health_status['metrics'] = {
                'total_metrics_collected': self.system_stats['total_metrics_collected'],
                'total_metrics_stored': self.system_stats['total_metrics_stored'],
                'total_anomalies_detected': self.system_stats['total_anomalies_detected'],
                'system_uptime_seconds': self.system_stats['system_uptime_seconds']
            }
            
            self.system_stats['last_health_check'] = datetime.now()
            self.system_stats['health_status'] = health_status['status']
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de metadata."""
        stats = self.system_stats.copy()
        
        # Agregar estadísticas de componentes
        if self.metrics_collector:
            stats['collector_stats'] = self.metrics_collector.get_collector_stats()
        
        if self.metrics_integration:
            stats['integration_stats'] = self.metrics_integration.get_integration_stats()
        
        if self.metrics_pipeline:
            stats['pipeline_stats'] = self.metrics_pipeline.get_pipeline_stats()
        
        if self.timescaledb_manager:
            stats['timescaledb_stats'] = self.timescaledb_manager.get_manager_stats()
        
        return stats
    
    def get_metrics_summary(self, 
                          metric_type: Optional[MetricType] = None,
                          time_range_minutes: int = 60) -> Dict[str, Any]:
        """Retorna resumen de métricas."""
        if not self.is_running or not self.metrics_collector:
            return {}
        
        return self.metrics_collector.get_metrics_summary(metric_type, time_range_minutes)
    
    # ===== MÉTODOS DE UTILIDAD =====
    
    def is_healthy(self) -> bool:
        """Verifica si el sistema está saludable."""
        return (self.is_running and 
                self.is_initialized and 
                self.system_stats['health_status'] == 'healthy')
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado del sistema."""
        return {
            'is_initialized': self.is_initialized,
            'is_running': self.is_running,
            'health_status': self.system_stats['health_status'],
            'last_health_check': self.system_stats['last_health_check'],
            'uptime_seconds': self.system_stats['system_uptime_seconds']
        }


# Instancia global del sistema de metadata
_metadata_system = None


def get_metadata_system() -> Optional[MetadataSystem]:
    """Obtiene la instancia global del sistema de metadata."""
    return _metadata_system


def initialize_metadata_system(timescaledb_config: Dict[str, Any] = None,
                             collector_config: Dict[str, Any] = None) -> MetadataSystem:
    """Inicializa la instancia global del sistema de metadata."""
    global _metadata_system
    
    if _metadata_system is None:
        _metadata_system = MetadataSystem(timescaledb_config, collector_config)
    
    return _metadata_system


async def start_metadata_system() -> bool:
    """Inicia el sistema de metadata global."""
    global _metadata_system
    
    if _metadata_system is None:
        _metadata_system = MetadataSystem()
    
    return await _metadata_system.start()


async def stop_metadata_system() -> bool:
    """Detiene el sistema de metadata global."""
    global _metadata_system
    
    if _metadata_system is not None:
        return await _metadata_system.stop()
    
    return True


if __name__ == "__main__":
    # Test del MetadataSystem
    logging.basicConfig(level=logging.INFO)
    
    async def test_metadata_system():
        # Crear sistema de metadata
        metadata_system = MetadataSystem()
        
        # Inicializar
        success = await metadata_system.initialize()
        print(f"Sistema inicializado: {'exitoso' if success else 'fallido'}")
        
        if success:
            # Iniciar
            success = await metadata_system.start()
            print(f"Sistema iniciado: {'exitoso' if success else 'fallido'}")
            
            if success:
                # Test de tracking
                metadata_system.track_routing_decision(
                    "test_query_001", 0.8, 0.9, "120B", 50, "python"
                )
                
                metadata_system.track_memory_operation(
                    "test_agent_001", "knowledge", "write", 1024, 256, 10
                )
                
                metadata_system.track_compute_operation(
                    "120B", "inference", 1, 1000, 1000, 2000, 85.0, 8000.0, 500.0, 2200.0
                )
                
                # Health check
                health = await metadata_system.health_check()
                print(f"Health check: {health}")
                
                # Estadísticas
                stats = metadata_system.get_system_stats()
                print(f"Estadísticas: {stats}")
                
                # Detener
                await metadata_system.stop()
    
    # Ejecutar test
    asyncio.run(test_metadata_system())
