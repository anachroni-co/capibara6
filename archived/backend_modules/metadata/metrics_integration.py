#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metrics Integration - Integración de métricas con todos los componentes del sistema.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from contextlib import contextmanager

from .metrics_collector import (
    MetricsCollector, MetricType, MetricLevel,
    RoutingMetrics, MemoryMetrics, ComputeMetrics, 
    ExecutionMetrics, AgentEvolutionMetrics, RAGMetrics, SystemMetrics
)

logger = logging.getLogger(__name__)


class MetricsIntegration:
    """Integración de métricas con todos los componentes del sistema."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.integration_stats = {
            'routing_metrics_collected': 0,
            'memory_metrics_collected': 0,
            'compute_metrics_collected': 0,
            'execution_metrics_collected': 0,
            'agent_evolution_metrics_collected': 0,
            'rag_metrics_collected': 0,
            'system_metrics_collected': 0,
            'integration_errors': 0
        }
        
        logger.info("MetricsIntegration inicializado")
    
    # ===== INTEGRACIÓN CON ROUTING =====
    
    @contextmanager
    def track_routing(self, query_id: str, query_text: str, user_intent: str = ""):
        """Context manager para tracking de routing."""
        start_time = time.time()
        routing_metrics = None
        
        try:
            yield routing_metrics
        finally:
            # Calcular métricas de routing
            total_time_ms = int((time.time() - start_time) * 1000)
            
            # Simular métricas de routing (en producción vendrían del router real)
            routing_metrics = RoutingMetrics(
                query_id=query_id,
                query_text=query_text,
                complexity_score=0.7,  # Simulado
                confidence_score=0.8,  # Simulado
                model_selected="20B",  # Simulado
                routing_time_ms=total_time_ms,
                embedding_time_ms=int(total_time_ms * 0.3),
                threshold_comparison_time_ms=int(total_time_ms * 0.1),
                total_routing_time_ms=total_time_ms,
                tokens_estimated=len(query_text.split()) * 1.3,
                context_length=len(query_text),
                user_intent=user_intent,
                domain_detected="general",  # Simulado
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_routing_metrics(routing_metrics)
            if success:
                self.integration_stats['routing_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
    
    def track_router_decision(self, 
                            query_id: str,
                            complexity_score: float,
                            confidence_score: float,
                            model_selected: str,
                            routing_time_ms: int,
                            domain_detected: str = ""):
        """Track de decisión del router."""
        try:
            routing_metrics = RoutingMetrics(
                query_id=query_id,
                query_text="",  # No disponible en este punto
                complexity_score=complexity_score,
                confidence_score=confidence_score,
                model_selected=model_selected,
                routing_time_ms=routing_time_ms,
                embedding_time_ms=0,
                threshold_comparison_time_ms=0,
                total_routing_time_ms=routing_time_ms,
                tokens_estimated=0,
                context_length=0,
                user_intent="",
                domain_detected=domain_detected,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_routing_metrics(routing_metrics)
            if success:
                self.integration_stats['routing_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking router decision: {e}")
            self.integration_stats['integration_errors'] += 1
    
    # ===== INTEGRACIÓN CON MEMORIA =====
    
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
        try:
            memory_metrics = MemoryMetrics(
                agent_id=agent_id,
                memory_type=memory_type,
                memory_operation=operation,
                memory_size_bytes=memory_size_bytes,
                memory_tokens=memory_tokens,
                operation_time_ms=operation_time_ms,
                cache_hit=cache_hit,
                compression_ratio=compression_ratio,
                importance_score=importance_score,
                access_count=1,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_memory_metrics(memory_metrics)
            if success:
                self.integration_stats['memory_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking memory operation: {e}")
            self.integration_stats['integration_errors'] += 1
    
    @contextmanager
    def track_memory_read(self, agent_id: str, memory_type: str):
        """Context manager para tracking de lectura de memoria."""
        start_time = time.time()
        cache_hit = False  # Simulado
        
        try:
            yield cache_hit
        finally:
            operation_time_ms = int((time.time() - start_time) * 1000)
            
            self.track_memory_operation(
                agent_id=agent_id,
                memory_type=memory_type,
                operation="read",
                memory_size_bytes=0,  # No disponible
                memory_tokens=0,  # No disponible
                operation_time_ms=operation_time_ms,
                cache_hit=cache_hit
            )
    
    @contextmanager
    def track_memory_write(self, agent_id: str, memory_type: str):
        """Context manager para tracking de escritura de memoria."""
        start_time = time.time()
        memory_size_bytes = 0
        memory_tokens = 0
        
        try:
            yield (memory_size_bytes, memory_tokens)
        finally:
            operation_time_ms = int((time.time() - start_time) * 1000)
            
            self.track_memory_operation(
                agent_id=agent_id,
                memory_type=memory_type,
                operation="write",
                memory_size_bytes=memory_size_bytes,
                memory_tokens=memory_tokens,
                operation_time_ms=operation_time_ms
            )
    
    # ===== INTEGRACIÓN CON CÓMPUTO =====
    
    def track_compute_operation(self,
                              model_id: str,
                              operation_type: str,
                              batch_size: int,
                              sequence_length: int,
                              tokens_processed: int,
                              computation_time_ms: int,
                              gpu_utilization_percent: float = 0.0,
                              gpu_memory_used_mb: float = 0.0,
                              cpu_utilization_percent: float = 0.0,
                              cpu_memory_used_mb: float = 0.0,
                              throughput_tokens_per_sec: float = 0.0,
                              latency_p50_ms: float = 0.0,
                              latency_p95_ms: float = 0.0,
                              latency_p99_ms: float = 0.0):
        """Track de operación de cómputo."""
        try:
            compute_metrics = ComputeMetrics(
                model_id=model_id,
                operation_type=operation_type,
                batch_size=batch_size,
                sequence_length=sequence_length,
                tokens_processed=tokens_processed,
                computation_time_ms=computation_time_ms,
                gpu_utilization_percent=gpu_utilization_percent,
                gpu_memory_used_mb=gpu_memory_used_mb,
                cpu_utilization_percent=cpu_utilization_percent,
                cpu_memory_used_mb=cpu_memory_used_mb,
                throughput_tokens_per_sec=throughput_tokens_per_sec,
                latency_p50_ms=latency_p50_ms,
                latency_p95_ms=latency_p95_ms,
                latency_p99_ms=latency_p99_ms,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_compute_metrics(compute_metrics)
            if success:
                self.integration_stats['compute_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking compute operation: {e}")
            self.integration_stats['integration_errors'] += 1
    
    @contextmanager
    def track_model_inference(self, model_id: str, batch_size: int = 1):
        """Context manager para tracking de inferencia del modelo."""
        start_time = time.time()
        tokens_processed = 0
        sequence_length = 0
        
        try:
            yield (tokens_processed, sequence_length)
        finally:
            computation_time_ms = int((time.time() - start_time) * 1000)
            
            # Calcular throughput
            throughput_tokens_per_sec = (tokens_processed / computation_time_ms * 1000) if computation_time_ms > 0 else 0
            
            self.track_compute_operation(
                model_id=model_id,
                operation_type="inference",
                batch_size=batch_size,
                sequence_length=sequence_length,
                tokens_processed=tokens_processed,
                computation_time_ms=computation_time_ms,
                throughput_tokens_per_sec=throughput_tokens_per_sec,
                latency_p50_ms=computation_time_ms,
                latency_p95_ms=computation_time_ms * 1.2,
                latency_p99_ms=computation_time_ms * 1.5
            )
    
    # ===== INTEGRACIÓN CON E2B =====
    
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
                       corrections_applied: int = 0,
                       sandbox_id: str = "",
                       timeout_occurred: bool = False):
        """Track de ejecución E2B."""
        try:
            execution_metrics = ExecutionMetrics(
                execution_id=execution_id,
                agent_id=agent_id,
                language=language,
                code_length=code_length,
                execution_time_ms=execution_time_ms,
                memory_used_mb=memory_used_mb,
                cpu_used_percent=cpu_used_percent,
                success=success,
                error_type=error_type,
                corrections_applied=corrections_applied,
                sandbox_id=sandbox_id,
                timeout_occurred=timeout_occurred,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_execution_metrics(execution_metrics)
            if success:
                self.integration_stats['execution_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking execution: {e}")
            self.integration_stats['integration_errors'] += 1
    
    @contextmanager
    def track_e2b_execution(self, execution_id: str, agent_id: str, language: str, code: str):
        """Context manager para tracking de ejecución E2B."""
        start_time = time.time()
        success = True
        error_type = ""
        corrections_applied = 0
        timeout_occurred = False
        
        try:
            yield (success, error_type, corrections_applied, timeout_occurred)
        finally:
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            self.track_execution(
                execution_id=execution_id,
                agent_id=agent_id,
                language=language,
                code_length=len(code),
                execution_time_ms=execution_time_ms,
                memory_used_mb=0.0,  # Simulado
                cpu_used_percent=0.0,  # Simulado
                success=success,
                error_type=error_type,
                corrections_applied=corrections_applied,
                timeout_occurred=timeout_occurred
            )
    
    # ===== INTEGRACIÓN CON EVOLUCIÓN DE AGENTES =====
    
    def track_agent_evolution(self,
                            agent_id: str,
                            domain: str,
                            evolution_event: str,
                            interactions_count: int,
                            success_rate: float,
                            graduation_score: float,
                            memory_utilization: float,
                            domain_expertise: float,
                            collaboration_count: int = 0,
                            playbook_contributions: int = 0,
                            learning_rate: float = 0.0):
        """Track de evolución de agente."""
        try:
            evolution_metrics = AgentEvolutionMetrics(
                agent_id=agent_id,
                domain=domain,
                evolution_event=evolution_event,
                interactions_count=interactions_count,
                success_rate=success_rate,
                graduation_score=graduation_score,
                memory_utilization=memory_utilization,
                domain_expertise=domain_expertise,
                collaboration_count=collaboration_count,
                playbook_contributions=playbook_contributions,
                learning_rate=learning_rate,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_agent_evolution_metrics(evolution_metrics)
            if success:
                self.integration_stats['agent_evolution_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking agent evolution: {e}")
            self.integration_stats['integration_errors'] += 1
    
    def track_agent_creation(self, agent_id: str, domain: str):
        """Track de creación de agente."""
        self.track_agent_evolution(
            agent_id=agent_id,
            domain=domain,
            evolution_event="created",
            interactions_count=0,
            success_rate=0.0,
            graduation_score=0.0,
            memory_utilization=0.0,
            domain_expertise=0.0
        )
    
    def track_agent_graduation(self, agent_id: str, domain: str, graduation_score: float, interactions_count: int, success_rate: float):
        """Track de graduación de agente."""
        self.track_agent_evolution(
            agent_id=agent_id,
            domain=domain,
            evolution_event="graduated",
            interactions_count=interactions_count,
            success_rate=success_rate,
            graduation_score=graduation_score,
            memory_utilization=0.5,  # Simulado
            domain_expertise=0.8  # Simulado
        )
    
    # ===== INTEGRACIÓN CON RAG =====
    
    def track_rag_operation(self,
                          query_id: str,
                          rag_type: str,
                          query_text: str,
                          retrieval_time_ms: int,
                          documents_retrieved: int,
                          documents_relevant: int,
                          relevance_score: float,
                          context_length: int,
                          context_tokens: int,
                          search_strategy: str = "",
                          vector_search_time_ms: int = 0,
                          reranking_time_ms: int = 0):
        """Track de operación RAG."""
        try:
            rag_metrics = RAGMetrics(
                query_id=query_id,
                rag_type=rag_type,
                query_text=query_text,
                retrieval_time_ms=retrieval_time_ms,
                documents_retrieved=documents_retrieved,
                documents_relevant=documents_relevant,
                relevance_score=relevance_score,
                context_length=context_length,
                context_tokens=context_tokens,
                search_strategy=search_strategy,
                vector_search_time_ms=vector_search_time_ms,
                reranking_time_ms=reranking_time_ms,
                total_rag_time_ms=retrieval_time_ms + vector_search_time_ms + reranking_time_ms,
                timestamp=datetime.now()
            )
            
            success = self.metrics_collector.collect_rag_metrics(rag_metrics)
            if success:
                self.integration_stats['rag_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking RAG operation: {e}")
            self.integration_stats['integration_errors'] += 1
    
    @contextmanager
    def track_rag_retrieval(self, query_id: str, rag_type: str, query_text: str):
        """Context manager para tracking de retrieval RAG."""
        start_time = time.time()
        documents_retrieved = 0
        documents_relevant = 0
        relevance_score = 0.0
        context_length = 0
        context_tokens = 0
        
        try:
            yield (documents_retrieved, documents_relevant, relevance_score, context_length, context_tokens)
        finally:
            retrieval_time_ms = int((time.time() - start_time) * 1000)
            
            self.track_rag_operation(
                query_id=query_id,
                rag_type=rag_type,
                query_text=query_text,
                retrieval_time_ms=retrieval_time_ms,
                documents_retrieved=documents_retrieved,
                documents_relevant=documents_relevant,
                relevance_score=relevance_score,
                context_length=context_length,
                context_tokens=context_tokens
            )
    
    # ===== INTEGRACIÓN CON SISTEMA =====
    
    def track_system_metrics(self,
                           system_id: str = "capibara6",
                           cpu_usage_percent: float = 0.0,
                           memory_usage_percent: float = 0.0,
                           disk_usage_percent: float = 0.0,
                           network_io_bytes: int = 0,
                           active_connections: int = 0,
                           active_agents: int = 0,
                           total_requests: int = 0,
                           error_rate: float = 0.0,
                           response_time_avg_ms: float = 0.0,
                           throughput_requests_per_sec: float = 0.0):
        """Track de métricas del sistema."""
        try:
            system_metrics = SystemMetrics(
                system_id=system_id,
                cpu_usage_percent=cpu_usage_percent,
                memory_usage_percent=memory_usage_percent,
                disk_usage_percent=disk_usage_percent,
                network_io_bytes=network_io_bytes,
                active_connections=active_connections,
                active_agents=active_agents,
                total_requests=total_requests,
                error_rate=error_rate,
                response_time_avg_ms=response_time_avg_ms,
                throughput_requests_per_sec=throughput_requests_per_sec,
                timestamp=datetime.now()
            )
            
            # Enviar métrica individual
            success = self.metrics_collector.collect_metric(
                MetricType.SYSTEM, "system_metrics", system_metrics.__dict__,
                tags={"system_id": system_id}
            )
            
            if success:
                self.integration_stats['system_metrics_collected'] += 1
            else:
                self.integration_stats['integration_errors'] += 1
                
        except Exception as e:
            logger.error(f"Error tracking system metrics: {e}")
            self.integration_stats['integration_errors'] += 1
    
    # ===== MÉTODOS DE UTILIDAD =====
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de integración."""
        return self.integration_stats.copy()
    
    def reset_stats(self):
        """Resetea estadísticas de integración."""
        for key in self.integration_stats:
            self.integration_stats[key] = 0
        logger.info("Estadísticas de integración reseteadas")


if __name__ == "__main__":
    # Test del MetricsIntegration
    logging.basicConfig(level=logging.INFO)
    
    from .metrics_collector import MetricsCollector
    
    collector = MetricsCollector(buffer_size=1000, flush_interval=5)
    collector.start()
    
    integration = MetricsIntegration(collector)
    
    # Test de tracking de routing
    with integration.track_routing("test_query_001", "How to optimize Python code?", "optimization"):
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
