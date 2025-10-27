#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prometheus Metrics - Sistema de métricas para Prometheus.
"""

import logging
import time
from typing import Dict, Any, Optional
from prometheus_client import (
    Counter, Histogram, Gauge, Summary, Info,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)
from prometheus_client.core import REGISTRY
import threading

logger = logging.getLogger(__name__)

class PrometheusMetrics:
    """Gestor de métricas Prometheus para Capibara6."""
    
    def __init__(self):
        self.registry = REGISTRY
        self._initialize_metrics()
        self._start_background_collectors()
        
        logger.info("PrometheusMetrics inicializado")
    
    def _initialize_metrics(self):
        """Inicializa todas las métricas."""
        
        # Métricas de API
        self.api_requests_total = Counter(
            'capibara6_api_requests_total',
            'Total number of API requests',
            ['method', 'endpoint', 'status_code']
        )
        
        self.api_request_duration = Histogram(
            'capibara6_api_request_duration_seconds',
            'API request duration in seconds',
            ['method', 'endpoint'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        )
        
        self.api_active_connections = Gauge(
            'capibara6_api_active_connections',
            'Number of active API connections'
        )
        
        # Métricas de Routing
        self.routing_requests_total = Counter(
            'capibara6_routing_requests_total',
            'Total number of routing requests',
            ['model_selected', 'complexity_level']
        )
        
        self.routing_duration = Histogram(
            'capibara6_routing_duration_seconds',
            'Routing decision duration in seconds',
            ['model_selected'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
        )
        
        self.routing_confidence = Histogram(
            'capibara6_routing_confidence',
            'Routing confidence scores',
            ['model_selected'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        )
        
        # Métricas de ACE
        self.ace_cycles_total = Counter(
            'capibara6_ace_cycles_total',
            'Total number of ACE cycles',
            ['component', 'status']
        )
        
        self.ace_processing_duration = Histogram(
            'capibara6_ace_processing_duration_seconds',
            'ACE processing duration in seconds',
            ['component'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        self.ace_awareness_score = Histogram(
            'capibara6_ace_awareness_score',
            'ACE awareness scores',
            ['component'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        )
        
        # Métricas de E2B
        self.e2b_executions_total = Counter(
            'capibara6_e2b_executions_total',
            'Total number of E2B executions',
            ['language', 'status']
        )
        
        self.e2b_execution_duration = Histogram(
            'capibara6_e2b_execution_duration_seconds',
            'E2B execution duration in seconds',
            ['language'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )
        
        self.e2b_sandbox_count = Gauge(
            'capibara6_e2b_sandbox_count',
            'Number of active E2B sandboxes',
            ['language']
        )
        
        # Métricas de RAG
        self.rag_searches_total = Counter(
            'capibara6_rag_searches_total',
            'Total number of RAG searches',
            ['search_type', 'status']
        )
        
        self.rag_search_duration = Histogram(
            'capibara6_rag_search_duration_seconds',
            'RAG search duration in seconds',
            ['search_type'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
        )
        
        self.rag_vector_count = Gauge(
            'capibara6_rag_vector_count',
            'Number of vectors in RAG index',
            ['index_type']
        )
        
        # Métricas de Agentes
        self.agents_total = Gauge(
            'capibara6_agents_total',
            'Total number of agents',
            ['status', 'domain']
        )
        
        self.agent_graduations_total = Counter(
            'capibara6_agent_graduations_total',
            'Total number of agent graduations',
            ['domain', 'success']
        )
        
        self.agent_memory_usage = Gauge(
            'capibara6_agent_memory_usage_bytes',
            'Agent memory usage in bytes',
            ['agent_id', 'memory_type']
        )
        
        # Métricas de Optimizaciones
        self.optimization_operations_total = Counter(
            'capibara6_optimization_operations_total',
            'Total number of optimization operations',
            ['operation_type', 'status']
        )
        
        self.cache_hit_rate = Gauge(
            'capibara6_cache_hit_rate',
            'Cache hit rate percentage',
            ['cache_type']
        )
        
        self.batch_processing_duration = Histogram(
            'capibara6_batch_processing_duration_seconds',
            'Batch processing duration in seconds',
            ['batch_type'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )
        
        # Métricas de Sistema
        self.system_cpu_usage = Gauge(
            'capibara6_system_cpu_usage_percent',
            'System CPU usage percentage'
        )
        
        self.system_memory_usage = Gauge(
            'capibara6_system_memory_usage_bytes',
            'System memory usage in bytes'
        )
        
        self.system_disk_usage = Gauge(
            'capibara6_system_disk_usage_bytes',
            'System disk usage in bytes',
            ['mount_point']
        )
        
        # Métricas de Negocio
        self.business_queries_total = Counter(
            'capibara6_business_queries_total',
            'Total number of business queries',
            ['query_type', 'user_tier']
        )
        
        self.business_response_time = Histogram(
            'capibara6_business_response_time_seconds',
            'Business response time in seconds',
            ['query_type'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        self.business_satisfaction_score = Gauge(
            'capibara6_business_satisfaction_score',
            'Business satisfaction score',
            ['metric_type']
        )
        
        # Métricas de Costos
        self.cost_per_query = Histogram(
            'capibara6_cost_per_query_usd',
            'Cost per query in USD',
            ['model_type', 'query_complexity'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
        )
        
        self.daily_cost_total = Gauge(
            'capibara6_daily_cost_total_usd',
            'Total daily cost in USD',
            ['cost_type']
        )
        
        # Información del sistema
        self.system_info = Info(
            'capibara6_system_info',
            'System information'
        )
        self.system_info.info({
            'version': '1.0.0',
            'environment': 'production',
            'deployment': 'kubernetes'
        })
    
    def _start_background_collectors(self):
        """Inicia colectores en background."""
        self._collector_thread = threading.Thread(target=self._background_collector, daemon=True)
        self._collector_thread.start()
    
    def _background_collector(self):
        """Colector en background para métricas del sistema."""
        while True:
            try:
                # Simular métricas del sistema
                import psutil
                
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.system_cpu_usage.set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.system_memory_usage.set(memory.used)
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.system_disk_usage.labels(mount_point='/').set(disk.used)
                
                time.sleep(30)  # Colectar cada 30 segundos
                
            except ImportError:
                # psutil no disponible, usar valores simulados
                self.system_cpu_usage.set(25.0)
                self.system_memory_usage.set(1024 * 1024 * 1024)  # 1GB
                self.system_disk_usage.labels(mount_point='/').set(10 * 1024 * 1024 * 1024)  # 10GB
                time.sleep(30)
            except Exception as e:
                logger.error(f"Error en background collector: {e}")
                time.sleep(30)
    
    # Métodos para registrar métricas de API
    def record_api_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Registra una request de API."""
        self.api_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code)
        ).inc()
        
        self.api_request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    def set_active_connections(self, count: int):
        """Establece el número de conexiones activas."""
        self.api_active_connections.set(count)
    
    # Métodos para registrar métricas de Routing
    def record_routing_request(self, model_selected: str, complexity_level: str, duration: float, confidence: float):
        """Registra una request de routing."""
        self.routing_requests_total.labels(
            model_selected=model_selected,
            complexity_level=complexity_level
        ).inc()
        
        self.routing_duration.labels(
            model_selected=model_selected
        ).observe(duration)
        
        self.routing_confidence.labels(
            model_selected=model_selected
        ).observe(confidence)
    
    # Métodos para registrar métricas de ACE
    def record_ace_cycle(self, component: str, status: str, duration: float, awareness_score: float):
        """Registra un ciclo de ACE."""
        self.ace_cycles_total.labels(
            component=component,
            status=status
        ).inc()
        
        self.ace_processing_duration.labels(
            component=component
        ).observe(duration)
        
        self.ace_awareness_score.labels(
            component=component
        ).observe(awareness_score)
    
    # Métodos para registrar métricas de E2B
    def record_e2b_execution(self, language: str, status: str, duration: float):
        """Registra una ejecución de E2B."""
        self.e2b_executions_total.labels(
            language=language,
            status=status
        ).inc()
        
        self.e2b_execution_duration.labels(
            language=language
        ).observe(duration)
    
    def set_sandbox_count(self, language: str, count: int):
        """Establece el número de sandboxes activos."""
        self.e2b_sandbox_count.labels(language=language).set(count)
    
    # Métodos para registrar métricas de RAG
    def record_rag_search(self, search_type: str, status: str, duration: float):
        """Registra una búsqueda de RAG."""
        self.rag_searches_total.labels(
            search_type=search_type,
            status=status
        ).inc()
        
        self.rag_search_duration.labels(
            search_type=search_type
        ).observe(duration)
    
    def set_vector_count(self, index_type: str, count: int):
        """Establece el número de vectores en el índice."""
        self.rag_vector_count.labels(index_type=index_type).set(count)
    
    # Métodos para registrar métricas de Agentes
    def set_agent_count(self, status: str, domain: str, count: int):
        """Establece el número de agentes."""
        self.agents_total.labels(status=status, domain=domain).set(count)
    
    def record_agent_graduation(self, domain: str, success: bool):
        """Registra una graduación de agente."""
        self.agent_graduations_total.labels(
            domain=domain,
            success=str(success)
        ).inc()
    
    def set_agent_memory_usage(self, agent_id: str, memory_type: str, usage_bytes: int):
        """Establece el uso de memoria de un agente."""
        self.agent_memory_usage.labels(
            agent_id=agent_id,
            memory_type=memory_type
        ).set(usage_bytes)
    
    # Métodos para registrar métricas de Optimizaciones
    def record_optimization_operation(self, operation_type: str, status: str):
        """Registra una operación de optimización."""
        self.optimization_operations_total.labels(
            operation_type=operation_type,
            status=status
        ).inc()
    
    def set_cache_hit_rate(self, cache_type: str, hit_rate: float):
        """Establece la tasa de acierto del caché."""
        self.cache_hit_rate.labels(cache_type=cache_type).set(hit_rate)
    
    def record_batch_processing(self, batch_type: str, duration: float):
        """Registra el procesamiento de un batch."""
        self.batch_processing_duration.labels(batch_type=batch_type).observe(duration)
    
    # Métodos para registrar métricas de Negocio
    def record_business_query(self, query_type: str, user_tier: str, response_time: float):
        """Registra una query de negocio."""
        self.business_queries_total.labels(
            query_type=query_type,
            user_tier=user_tier
        ).inc()
        
        self.business_response_time.labels(query_type=query_type).observe(response_time)
    
    def set_business_satisfaction_score(self, metric_type: str, score: float):
        """Establece el score de satisfacción del negocio."""
        self.business_satisfaction_score.labels(metric_type=metric_type).set(score)
    
    # Métodos para registrar métricas de Costos
    def record_cost_per_query(self, model_type: str, query_complexity: str, cost_usd: float):
        """Registra el costo por query."""
        self.cost_per_query.labels(
            model_type=model_type,
            query_complexity=query_complexity
        ).observe(cost_usd)
    
    def set_daily_cost(self, cost_type: str, cost_usd: float):
        """Establece el costo diario."""
        self.daily_cost_total.labels(cost_type=cost_type).set(cost_usd)
    
    def get_metrics(self) -> str:
        """Obtiene las métricas en formato Prometheus."""
        return generate_latest(self.registry)
    
    def get_metrics_content_type(self) -> str:
        """Obtiene el content type para las métricas."""
        return CONTENT_TYPE_LATEST


# Instancia global
prometheus_metrics = PrometheusMetrics()


def get_prometheus_metrics() -> PrometheusMetrics:
    """Obtiene la instancia global de métricas Prometheus."""
    return prometheus_metrics


if __name__ == "__main__":
    # Test del sistema de métricas
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    metrics = PrometheusMetrics()
    
    # Simular algunas métricas
    metrics.record_api_request("POST", "/api/v1/query", 200, 0.5)
    metrics.record_routing_request("capibara6-20b", "medium", 0.1, 0.85)
    metrics.record_ace_cycle("generator", "success", 1.2, 0.9)
    metrics.record_e2b_execution("python", "success", 2.5)
    metrics.record_rag_search("mini_rag", "success", 0.05)
    
    # Obtener métricas
    metrics_output = metrics.get_metrics()
    print("Métricas Prometheus:")
    print(metrics_output.decode('utf-8'))
    
    print("Sistema de métricas Prometheus funcionando correctamente!")
