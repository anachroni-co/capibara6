#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metrics Collector - Captura completa de metadata del sistema.
"""

import logging
import time
import psutil
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Tipos de métricas."""
    ROUTING = "routing"
    MEMORY = "memory"
    ATTENTION = "attention"
    COMPUTE = "compute"
    EXECUTION = "execution"
    AGENT_EVOLUTION = "agent_evolution"
    RAG = "rag"
    SYSTEM = "system"


class MetricLevel(Enum):
    """Niveles de métricas."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class MetricPoint:
    """Punto de métrica individual."""
    metric_type: MetricType
    metric_name: str
    value: Union[float, int, str, bool, Dict[str, Any]]
    timestamp: datetime
    level: MetricLevel = MetricLevel.INFO
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RoutingMetrics:
    """Métricas de routing inteligente."""
    query_id: str
    query_text: str
    complexity_score: float
    confidence_score: float
    model_selected: str  # 20B or 120B
    routing_time_ms: int
    embedding_time_ms: int
    threshold_comparison_time_ms: int
    total_routing_time_ms: int
    tokens_estimated: int
    context_length: int
    user_intent: str
    domain_detected: str
    timestamp: datetime


@dataclass
class MemoryMetrics:
    """Métricas de memoria de agentes."""
    agent_id: str
    memory_type: str
    memory_operation: str  # read, write, compress, prune
    memory_size_bytes: int
    memory_tokens: int
    operation_time_ms: int
    cache_hit: bool
    compression_ratio: float
    importance_score: float
    access_count: int
    timestamp: datetime


@dataclass
class AttentionMetrics:
    """Métricas de atención del modelo."""
    model_id: str
    layer_id: int
    attention_heads: int
    attention_pattern: str
    attention_entropy: float
    attention_focus: float
    attention_diversity: float
    computation_time_ms: int
    memory_usage_mb: float
    timestamp: datetime


@dataclass
class ComputeMetrics:
    """Métricas de cómputo."""
    model_id: str
    operation_type: str  # inference, training, fine-tuning
    batch_size: int
    sequence_length: int
    tokens_processed: int
    computation_time_ms: int
    gpu_utilization_percent: float
    gpu_memory_used_mb: float
    cpu_utilization_percent: float
    cpu_memory_used_mb: float
    throughput_tokens_per_sec: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    timestamp: datetime


@dataclass
class ExecutionMetrics:
    """Métricas de ejecución E2B."""
    execution_id: str
    agent_id: str
    language: str
    code_length: int
    execution_time_ms: int
    memory_used_mb: float
    cpu_used_percent: float
    success: bool
    error_type: str
    corrections_applied: int
    sandbox_id: str
    timeout_occurred: bool
    timestamp: datetime


@dataclass
class AgentEvolutionMetrics:
    """Métricas de evolución de agentes."""
    agent_id: str
    domain: str
    evolution_event: str  # created, trained, graduated, retired
    interactions_count: int
    success_rate: float
    graduation_score: float
    memory_utilization: float
    domain_expertise: float
    collaboration_count: int
    playbook_contributions: int
    learning_rate: float
    timestamp: datetime


@dataclass
class RAGMetrics:
    """Métricas de RAG."""
    query_id: str
    rag_type: str  # mini_rag, full_rag, guided_search
    query_text: str
    retrieval_time_ms: int
    documents_retrieved: int
    documents_relevant: int
    relevance_score: float
    context_length: int
    context_tokens: int
    search_strategy: str
    vector_search_time_ms: int
    reranking_time_ms: int
    total_rag_time_ms: int
    timestamp: datetime


@dataclass
class SystemMetrics:
    """Métricas del sistema."""
    system_id: str
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_io_bytes: int
    active_connections: int
    active_agents: int
    total_requests: int
    error_rate: float
    response_time_avg_ms: float
    throughput_requests_per_sec: float
    timestamp: datetime


class MetricsCollector:
    """Recolector de métricas del sistema."""
    
    def __init__(self, 
                 buffer_size: int = 10000,
                 flush_interval: int = 30,
                 enable_system_metrics: bool = True):
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.enable_system_metrics = enable_system_metrics
        
        self.metrics_buffer = queue.Queue(maxsize=buffer_size)
        self.collectors = {}
        self.is_running = False
        self.flush_thread = None
        
        # Estadísticas del collector
        self.collector_stats = {
            'total_metrics_collected': 0,
            'total_metrics_flushed': 0,
            'buffer_overflows': 0,
            'collection_errors': 0,
            'last_flush_time': None
        }
        
        # Inicializar collectors específicos
        self._initialize_collectors()
        
        logger.info(f"MetricsCollector inicializado: buffer_size={buffer_size}, flush_interval={flush_interval}s")
    
    def _initialize_collectors(self):
        """Inicializa los collectors específicos."""
        self.collectors = {
            MetricType.ROUTING: self._collect_routing_metrics,
            MetricType.MEMORY: self._collect_memory_metrics,
            MetricType.ATTENTION: self._collect_attention_metrics,
            MetricType.COMPUTE: self._collect_compute_metrics,
            MetricType.EXECUTION: self._collect_execution_metrics,
            MetricType.AGENT_EVOLUTION: self._collect_agent_evolution_metrics,
            MetricType.RAG: self._collect_rag_metrics,
            MetricType.SYSTEM: self._collect_system_metrics
        }
    
    def start(self):
        """Inicia el collector de métricas."""
        if self.is_running:
            logger.warning("MetricsCollector ya está ejecutándose")
            return
        
        self.is_running = True
        
        # Iniciar thread de flush
        self.flush_thread = threading.Thread(target=self._flush_worker, daemon=True)
        self.flush_thread.start()
        
        logger.info("MetricsCollector iniciado")
    
    def stop(self):
        """Detiene el collector de métricas."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Esperar a que termine el flush thread
        if self.flush_thread and self.flush_thread.is_alive():
            self.flush_thread.join(timeout=5)
        
        # Flush final
        self._flush_metrics()
        
        logger.info("MetricsCollector detenido")
    
    def collect_metric(self, 
                      metric_type: MetricType,
                      metric_name: str,
                      value: Union[float, int, str, bool, Dict[str, Any]],
                      level: MetricLevel = MetricLevel.INFO,
                      tags: Dict[str, str] = None,
                      metadata: Dict[str, Any] = None) -> bool:
        """Recolecta una métrica individual."""
        try:
            metric_point = MetricPoint(
                metric_type=metric_type,
                metric_name=metric_name,
                value=value,
                timestamp=datetime.now(),
                level=level,
                tags=tags or {},
                metadata=metadata or {}
            )
            
            # Agregar al buffer
            try:
                self.metrics_buffer.put_nowait(metric_point)
                self.collector_stats['total_metrics_collected'] += 1
                return True
            except queue.Full:
                self.collector_stats['buffer_overflows'] += 1
                logger.warning("Buffer de métricas lleno, descartando métrica")
                return False
                
        except Exception as e:
            self.collector_stats['collection_errors'] += 1
            logger.error(f"Error recolectando métrica {metric_name}: {e}")
            return False
    
    def collect_routing_metrics(self, metrics: RoutingMetrics) -> bool:
        """Recolecta métricas de routing."""
        try:
            # Métricas individuales
            self.collect_metric(
                MetricType.ROUTING, "routing_time_ms", metrics.routing_time_ms,
                tags={"model": metrics.model_selected, "query_id": metrics.query_id}
            )
            
            self.collect_metric(
                MetricType.ROUTING, "complexity_score", metrics.complexity_score,
                tags={"model": metrics.model_selected, "domain": metrics.domain_detected}
            )
            
            self.collect_metric(
                MetricType.ROUTING, "confidence_score", metrics.confidence_score,
                tags={"model": metrics.model_selected, "domain": metrics.domain_detected}
            )
            
            self.collect_metric(
                MetricType.ROUTING, "tokens_estimated", metrics.tokens_estimated,
                tags={"model": metrics.model_selected, "query_id": metrics.query_id}
            )
            
            # Métrica compuesta
            self.collect_metric(
                MetricType.ROUTING, "routing_decision", {
                    "model_selected": metrics.model_selected,
                    "complexity_score": metrics.complexity_score,
                    "confidence_score": metrics.confidence_score,
                    "routing_time_ms": metrics.routing_time_ms,
                    "domain_detected": metrics.domain_detected
                },
                tags={"query_id": metrics.query_id, "model": metrics.model_selected}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de routing: {e}")
            return False
    
    def collect_memory_metrics(self, metrics: MemoryMetrics) -> bool:
        """Recolecta métricas de memoria."""
        try:
            self.collect_metric(
                MetricType.MEMORY, "memory_operation_time_ms", metrics.operation_time_ms,
                tags={"agent_id": metrics.agent_id, "operation": metrics.memory_operation}
            )
            
            self.collect_metric(
                MetricType.MEMORY, "memory_size_bytes", metrics.memory_size_bytes,
                tags={"agent_id": metrics.agent_id, "type": metrics.memory_type}
            )
            
            self.collect_metric(
                MetricType.MEMORY, "memory_tokens", metrics.memory_tokens,
                tags={"agent_id": metrics.agent_id, "type": metrics.memory_type}
            )
            
            self.collect_metric(
                MetricType.MEMORY, "cache_hit", metrics.cache_hit,
                tags={"agent_id": metrics.agent_id, "operation": metrics.memory_operation}
            )
            
            if metrics.memory_operation == "compress":
                self.collect_metric(
                    MetricType.MEMORY, "compression_ratio", metrics.compression_ratio,
                    tags={"agent_id": metrics.agent_id, "type": metrics.memory_type}
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de memoria: {e}")
            return False
    
    def collect_compute_metrics(self, metrics: ComputeMetrics) -> bool:
        """Recolecta métricas de cómputo."""
        try:
            self.collect_metric(
                MetricType.COMPUTE, "computation_time_ms", metrics.computation_time_ms,
                tags={"model_id": metrics.model_id, "operation": metrics.operation_type}
            )
            
            self.collect_metric(
                MetricType.COMPUTE, "gpu_utilization_percent", metrics.gpu_utilization_percent,
                tags={"model_id": metrics.model_id, "operation": metrics.operation_type}
            )
            
            self.collect_metric(
                MetricType.COMPUTE, "gpu_memory_used_mb", metrics.gpu_memory_used_mb,
                tags={"model_id": metrics.model_id, "operation": metrics.operation_type}
            )
            
            self.collect_metric(
                MetricType.COMPUTE, "throughput_tokens_per_sec", metrics.throughput_tokens_per_sec,
                tags={"model_id": metrics.model_id, "operation": metrics.operation_type}
            )
            
            self.collect_metric(
                MetricType.COMPUTE, "latency_p95_ms", metrics.latency_p95_ms,
                tags={"model_id": metrics.model_id, "operation": metrics.operation_type}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de cómputo: {e}")
            return False
    
    def collect_execution_metrics(self, metrics: ExecutionMetrics) -> bool:
        """Recolecta métricas de ejecución E2B."""
        try:
            self.collect_metric(
                MetricType.EXECUTION, "execution_time_ms", metrics.execution_time_ms,
                tags={"agent_id": metrics.agent_id, "language": metrics.language, "success": str(metrics.success)}
            )
            
            self.collect_metric(
                MetricType.EXECUTION, "memory_used_mb", metrics.memory_used_mb,
                tags={"agent_id": metrics.agent_id, "language": metrics.language}
            )
            
            self.collect_metric(
                MetricType.EXECUTION, "success_rate", 1.0 if metrics.success else 0.0,
                tags={"agent_id": metrics.agent_id, "language": metrics.language}
            )
            
            if not metrics.success:
                self.collect_metric(
                    MetricType.EXECUTION, "error_type", metrics.error_type,
                    tags={"agent_id": metrics.agent_id, "language": metrics.language}
                )
            
            if metrics.corrections_applied > 0:
                self.collect_metric(
                    MetricType.EXECUTION, "corrections_applied", metrics.corrections_applied,
                    tags={"agent_id": metrics.agent_id, "language": metrics.language}
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de ejecución: {e}")
            return False
    
    def collect_agent_evolution_metrics(self, metrics: AgentEvolutionMetrics) -> bool:
        """Recolecta métricas de evolución de agentes."""
        try:
            self.collect_metric(
                MetricType.AGENT_EVOLUTION, "interactions_count", metrics.interactions_count,
                tags={"agent_id": metrics.agent_id, "domain": metrics.domain, "event": metrics.evolution_event}
            )
            
            self.collect_metric(
                MetricType.AGENT_EVOLUTION, "success_rate", metrics.success_rate,
                tags={"agent_id": metrics.agent_id, "domain": metrics.domain, "event": metrics.evolution_event}
            )
            
            self.collect_metric(
                MetricType.AGENT_EVOLUTION, "graduation_score", metrics.graduation_score,
                tags={"agent_id": metrics.agent_id, "domain": metrics.domain, "event": metrics.evolution_event}
            )
            
            self.collect_metric(
                MetricType.AGENT_EVOLUTION, "domain_expertise", metrics.domain_expertise,
                tags={"agent_id": metrics.agent_id, "domain": metrics.domain, "event": metrics.evolution_event}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de evolución de agentes: {e}")
            return False
    
    def collect_rag_metrics(self, metrics: RAGMetrics) -> bool:
        """Recolecta métricas de RAG."""
        try:
            self.collect_metric(
                MetricType.RAG, "retrieval_time_ms", metrics.retrieval_time_ms,
                tags={"rag_type": metrics.rag_type, "query_id": metrics.query_id}
            )
            
            self.collect_metric(
                MetricType.RAG, "documents_retrieved", metrics.documents_retrieved,
                tags={"rag_type": metrics.rag_type, "query_id": metrics.query_id}
            )
            
            self.collect_metric(
                MetricType.RAG, "relevance_score", metrics.relevance_score,
                tags={"rag_type": metrics.rag_type, "query_id": metrics.query_id}
            )
            
            self.collect_metric(
                MetricType.RAG, "total_rag_time_ms", metrics.total_rag_time_ms,
                tags={"rag_type": metrics.rag_type, "query_id": metrics.query_id}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error recolectando métricas de RAG: {e}")
            return False
    
    def _collect_routing_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de routing."""
        pass  # Implementación específica si es necesaria
    
    def _collect_memory_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de memoria."""
        pass  # Implementación específica si es necesaria
    
    def _collect_attention_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de atención."""
        pass  # Implementación específica si es necesaria
    
    def _collect_compute_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de cómputo."""
        pass  # Implementación específica si es necesaria
    
    def _collect_execution_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de ejecución."""
        pass  # Implementación específica si es necesaria
    
    def _collect_agent_evolution_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de evolución de agentes."""
        pass  # Implementación específica si es necesaria
    
    def _collect_rag_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas de RAG."""
        pass  # Implementación específica si es necesaria
    
    def _collect_system_metrics(self, metric_point: MetricPoint):
        """Collector específico para métricas del sistema."""
        pass  # Implementación específica si es necesaria
    
    def _flush_worker(self):
        """Worker thread para flush periódico de métricas."""
        while self.is_running:
            try:
                time.sleep(self.flush_interval)
                if self.is_running:
                    self._flush_metrics()
            except Exception as e:
                logger.error(f"Error en flush worker: {e}")
    
    def _flush_metrics(self):
        """Flush de métricas del buffer."""
        try:
            metrics_to_flush = []
            
            # Extraer métricas del buffer
            while not self.metrics_buffer.empty():
                try:
                    metric = self.metrics_buffer.get_nowait()
                    metrics_to_flush.append(metric)
                except queue.Empty:
                    break
            
            if metrics_to_flush:
                # Procesar métricas (en producción se enviarían a TimescaleDB)
                self._process_metrics(metrics_to_flush)
                
                self.collector_stats['total_metrics_flushed'] += len(metrics_to_flush)
                self.collector_stats['last_flush_time'] = datetime.now()
                
                logger.debug(f"Flush completado: {len(metrics_to_flush)} métricas procesadas")
            
        except Exception as e:
            logger.error(f"Error en flush de métricas: {e}")
    
    def _process_metrics(self, metrics: List[MetricPoint]):
        """Procesa métricas (implementación específica)."""
        # En producción, aquí se enviarían a TimescaleDB
        # Por ahora, solo loggeamos las métricas
        for metric in metrics:
            logger.debug(f"Métrica procesada: {metric.metric_type.value}.{metric.metric_name} = {metric.value}")
    
    def get_collector_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del collector."""
        return {
            'collector_stats': self.collector_stats,
            'buffer_size': self.metrics_buffer.qsize(),
            'is_running': self.is_running,
            'flush_interval': self.flush_interval
        }
    
    def get_metrics_summary(self, 
                          metric_type: Optional[MetricType] = None,
                          time_range_minutes: int = 60) -> Dict[str, Any]:
        """Retorna resumen de métricas."""
        # Implementación simplificada - en producción consultaría TimescaleDB
        return {
            'metric_type': metric_type.value if metric_type else 'all',
            'time_range_minutes': time_range_minutes,
            'total_metrics': self.collector_stats['total_metrics_collected'],
            'flushed_metrics': self.collector_stats['total_metrics_flushed'],
            'buffer_overflows': self.collector_stats['buffer_overflows'],
            'collection_errors': self.collector_stats['collection_errors']
        }


if __name__ == "__main__":
    # Test del MetricsCollector
    logging.basicConfig(level=logging.INFO)
    
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
    
    collector.collect_routing_metrics(routing_metrics)
    
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
    
    collector.collect_memory_metrics(memory_metrics)
    
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
    
    collector.collect_compute_metrics(compute_metrics)
    
    # Esperar un poco para que se procesen las métricas
    time.sleep(6)
    
    # Mostrar estadísticas
    stats = collector.get_collector_stats()
    print(f"Estadísticas del collector: {stats}")
    
    # Detener collector
    collector.stop()
