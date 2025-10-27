#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Batching - Sistema de batching dinámico para optimización de throughput.
"""

import logging
import json
import os
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np
import heapq

logger = logging.getLogger(__name__)


class BatchStrategy(Enum):
    """Estrategias de batching."""
    FIXED_SIZE = "fixed_size"
    TIME_BASED = "time_based"
    ADAPTIVE = "adaptive"
    PRIORITY_BASED = "priority_based"
    LOAD_BALANCED = "load_balanced"


class RequestPriority(Enum):
    """Prioridades de request."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class BatchStatus(Enum):
    """Estados de batch."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class BatchRequest:
    """Request en batch."""
    request_id: str
    content: str
    priority: RequestPriority
    max_wait_time_ms: int
    created_at: datetime
    metadata: Dict[str, Any]
    callback: Optional[Callable] = None


@dataclass
class Batch:
    """Batch de requests."""
    batch_id: str
    requests: List[BatchRequest]
    strategy: BatchStrategy
    max_batch_size: int
    max_wait_time_ms: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    status: BatchStatus
    processing_time_ms: float
    throughput_tokens_per_second: float
    metadata: Dict[str, Any]


@dataclass
class BatchMetrics:
    """Métricas de batching."""
    total_batches: int
    total_requests: int
    average_batch_size: float
    average_processing_time_ms: float
    average_throughput_tokens_per_second: float
    average_wait_time_ms: float
    batch_efficiency: float
    queue_length: int
    processing_rate: float


class BatchQueue:
    """Cola de batching."""
    
    def __init__(self, 
                 max_queue_size: int = 10000,
                 priority_queues: bool = True):
        self.max_queue_size = max_queue_size
        self.priority_queues = priority_queues
        
        # Colas por prioridad
        if priority_queues:
            self.queues = {
                RequestPriority.CRITICAL: [],
                RequestPriority.HIGH: [],
                RequestPriority.MEDIUM: [],
                RequestPriority.LOW: [],
                RequestPriority.BACKGROUND: []
            }
        else:
            self.queues = {RequestPriority.MEDIUM: []}  # Cola única
        
        # Estadísticas
        self.queue_stats = {
            'total_requests_enqueued': 0,
            'total_requests_dequeued': 0,
            'current_queue_size': 0,
            'max_queue_size_reached': 0
        }
        
        logger.info(f"BatchQueue inicializada: max_size={max_queue_size}, priority_queues={priority_queues}")
    
    def enqueue(self, request: BatchRequest) -> bool:
        """Agrega request a la cola."""
        try:
            if self.queue_stats['current_queue_size'] >= self.max_queue_size:
                logger.warning(f"Cola llena, rechazando request {request.request_id}")
                return False
            
            # Agregar a cola apropiada
            if self.priority_queues:
                priority_queue = self.queues[request.priority]
            else:
                priority_queue = self.queues[RequestPriority.MEDIUM]
            
            # Usar timestamp como tie-breaker para orden
            heapq.heappush(priority_queue, (request.created_at.timestamp(), request))
            
            # Actualizar estadísticas
            self.queue_stats['total_requests_enqueued'] += 1
            self.queue_stats['current_queue_size'] += 1
            self.queue_stats['max_queue_size_reached'] = max(
                self.queue_stats['max_queue_size_reached'],
                self.queue_stats['current_queue_size']
            )
            
            logger.debug(f"Request {request.request_id} agregado a cola de prioridad {request.priority.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error agregando request a cola: {e}")
            return False
    
    def dequeue_batch(self, 
                     max_batch_size: int,
                     max_wait_time_ms: int = 1000) -> List[BatchRequest]:
        """Extrae batch de requests de la cola."""
        try:
            batch = []
            current_time = datetime.now()
            
            # Recorrer colas por prioridad
            for priority in [RequestPriority.CRITICAL, RequestPriority.HIGH, 
                           RequestPriority.MEDIUM, RequestPriority.LOW, 
                           RequestPriority.BACKGROUND]:
                
                if priority not in self.queues:
                    continue
                
                priority_queue = self.queues[priority]
                
                # Extraer requests de esta prioridad
                while priority_queue and len(batch) < max_batch_size:
                    timestamp, request = heapq.heappop(priority_queue)
                    
                    # Verificar timeout
                    wait_time = (current_time - request.created_at).total_seconds() * 1000
                    if wait_time > request.max_wait_time_ms:
                        logger.warning(f"Request {request.request_id} timeout después de {wait_time:.0f}ms")
                        continue
                    
                    batch.append(request)
                    self.queue_stats['total_requests_dequeued'] += 1
                    self.queue_stats['current_queue_size'] -= 1
            
            logger.debug(f"Batch extraído: {len(batch)} requests")
            return batch
            
        except Exception as e:
            logger.error(f"Error extrayendo batch: {e}")
            return []
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Obtiene estado de las colas."""
        status = {
            'queue_stats': self.queue_stats.copy(),
            'queue_sizes': {},
            'total_queued': 0
        }
        
        for priority, queue in self.queues.items():
            queue_size = len(queue)
            status['queue_sizes'][priority.name] = queue_size
            status['total_queued'] += queue_size
        
        return status


class DynamicBatcher:
    """Sistema de batching dinámico."""
    
    def __init__(self, 
                 strategy: BatchStrategy = BatchStrategy.ADAPTIVE,
                 max_batch_size: int = 32,
                 max_wait_time_ms: int = 100,
                 min_batch_size: int = 1,
                 target_throughput: float = 1000.0):
        self.strategy = strategy
        self.max_batch_size = max_batch_size
        self.max_wait_time_ms = max_wait_time_ms
        self.min_batch_size = min_batch_size
        self.target_throughput = target_throughput
        
        # Cola de batching
        self.batch_queue = BatchQueue()
        
        # Historial de batches
        self.batch_history: deque = deque(maxlen=1000)
        
        # Métricas de rendimiento
        self.performance_history: deque = deque(maxlen=100)
        
        # Configuración adaptativa
        self.adaptive_config = {
            'current_batch_size': max_batch_size,
            'current_wait_time': max_wait_time_ms,
            'throughput_window': deque(maxlen=10),
            'latency_window': deque(maxlen=10),
            'adjustment_factor': 0.1
        }
        
        # Estadísticas
        self.batcher_stats = {
            'total_batches_created': 0,
            'total_requests_processed': 0,
            'average_batch_size': 0.0,
            'average_processing_time_ms': 0.0,
            'average_throughput_tokens_per_second': 0.0,
            'batch_efficiency': 0.0,
            'queue_utilization': 0.0
        }
        
        # Thread de procesamiento
        self.processing_task = None
        self.is_processing = False
        
        logger.info(f"DynamicBatcher inicializado: strategy={strategy.value}, max_batch_size={max_batch_size}")
    
    async def start_processing(self):
        """Inicia procesamiento de batches."""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.processing_task = asyncio.create_task(self._processing_loop())
        
        logger.info("Procesamiento de batches iniciado")
    
    async def stop_processing(self):
        """Detiene procesamiento de batches."""
        self.is_processing = False
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Procesamiento de batches detenido")
    
    async def _processing_loop(self):
        """Loop principal de procesamiento."""
        while self.is_processing:
            try:
                # Determinar tamaño de batch
                batch_size = self._determine_batch_size()
                
                # Extraer batch de la cola
                batch_requests = self.batch_queue.dequeue_batch(
                    batch_size, 
                    self.adaptive_config['current_wait_time']
                )
                
                if batch_requests:
                    # Procesar batch
                    await self._process_batch(batch_requests)
                else:
                    # No hay requests, esperar un poco
                    await asyncio.sleep(0.001)  # 1ms
                
            except Exception as e:
                logger.error(f"Error en loop de procesamiento: {e}")
                await asyncio.sleep(0.01)  # 10ms
    
    def _determine_batch_size(self) -> int:
        """Determina tamaño de batch basado en estrategia."""
        if self.strategy == BatchStrategy.FIXED_SIZE:
            return self.max_batch_size
        elif self.strategy == BatchStrategy.TIME_BASED:
            return self._calculate_time_based_batch_size()
        elif self.strategy == BatchStrategy.ADAPTIVE:
            return self._calculate_adaptive_batch_size()
        elif self.strategy == BatchStrategy.PRIORITY_BASED:
            return self._calculate_priority_based_batch_size()
        elif self.strategy == BatchStrategy.LOAD_BALANCED:
            return self._calculate_load_balanced_batch_size()
        else:
            return self.max_batch_size
    
    def _calculate_time_based_batch_size(self) -> int:
        """Calcula tamaño de batch basado en tiempo."""
        # Ajustar tamaño basado en tiempo de espera
        queue_status = self.batch_queue.get_queue_status()
        total_queued = queue_status['total_queued']
        
        if total_queued > self.max_batch_size * 2:
            return self.max_batch_size  # Procesar batches grandes
        elif total_queued > self.max_batch_size:
            return self.max_batch_size // 2  # Procesar batches medianos
        else:
            return max(self.min_batch_size, total_queued)  # Procesar lo que hay
    
    def _calculate_adaptive_batch_size(self) -> int:
        """Calcula tamaño de batch adaptativo."""
        # Usar configuración adaptativa
        current_size = self.adaptive_config['current_batch_size']
        
        # Ajustar basado en throughput reciente
        if len(self.adaptive_config['throughput_window']) >= 3:
            recent_throughput = np.mean(list(self.adaptive_config['throughput_window'])[-3:])
            
            if recent_throughput < self.target_throughput * 0.8:
                # Throughput bajo, aumentar batch size
                current_size = min(self.max_batch_size, 
                                 int(current_size * (1 + self.adaptive_config['adjustment_factor'])))
            elif recent_throughput > self.target_throughput * 1.2:
                # Throughput alto, reducir batch size para mejor latencia
                current_size = max(self.min_batch_size, 
                                 int(current_size * (1 - self.adaptive_config['adjustment_factor'])))
        
        self.adaptive_config['current_batch_size'] = current_size
        return current_size
    
    def _calculate_priority_based_batch_size(self) -> int:
        """Calcula tamaño de batch basado en prioridad."""
        queue_status = self.batch_queue.get_queue_status()
        
        # Priorizar requests críticos y de alta prioridad
        critical_count = queue_status['queue_sizes'].get('CRITICAL', 0)
        high_count = queue_status['queue_sizes'].get('HIGH', 0)
        
        if critical_count > 0:
            return min(self.max_batch_size, critical_count)
        elif high_count > 0:
            return min(self.max_batch_size, high_count)
        else:
            return self.max_batch_size
    
    def _calculate_load_balanced_batch_size(self) -> int:
        """Calcula tamaño de batch para balance de carga."""
        # Balancear entre throughput y latencia
        queue_status = self.batch_queue.get_queue_status()
        total_queued = queue_status['total_queued']
        
        if total_queued == 0:
            return self.min_batch_size
        
        # Calcular tamaño óptimo basado en carga
        optimal_size = min(self.max_batch_size, max(self.min_batch_size, total_queued // 4))
        
        return optimal_size
    
    async def _process_batch(self, batch_requests: List[BatchRequest]):
        """Procesa un batch de requests."""
        try:
            batch_id = f"batch_{int(time.time() * 1000)}"
            start_time = datetime.now()
            
            # Crear batch
            batch = Batch(
                batch_id=batch_id,
                requests=batch_requests,
                strategy=self.strategy,
                max_batch_size=self.max_batch_size,
                max_wait_time_ms=self.max_wait_time_ms,
                created_at=start_time,
                started_at=start_time,
                completed_at=None,
                status=BatchStatus.PROCESSING,
                processing_time_ms=0.0,
                throughput_tokens_per_second=0.0,
                metadata={'batch_size': len(batch_requests)}
            )
            
            logger.info(f"Procesando batch {batch_id} con {len(batch_requests)} requests")
            
            # Simular procesamiento
            processing_time = await self._simulate_batch_processing(batch_requests)
            
            # Calcular métricas
            total_tokens = sum(len(req.content.split()) for req in batch_requests)
            throughput = (total_tokens / processing_time) * 1000 if processing_time > 0 else 0
            
            # Actualizar batch
            batch.completed_at = datetime.now()
            batch.status = BatchStatus.COMPLETED
            batch.processing_time_ms = processing_time
            batch.throughput_tokens_per_second = throughput
            
            # Agregar al historial
            self.batch_history.append(batch)
            
            # Actualizar configuración adaptativa
            self._update_adaptive_config(batch)
            
            # Actualizar estadísticas
            self._update_stats(batch)
            
            # Ejecutar callbacks
            for request in batch_requests:
                if request.callback:
                    try:
                        await request.callback(request.request_id, batch_id)
                    except Exception as e:
                        logger.error(f"Error en callback para request {request.request_id}: {e}")
            
            logger.info(f"Batch {batch_id} completado en {processing_time:.1f}ms, throughput: {throughput:.0f} tokens/s")
            
        except Exception as e:
            logger.error(f"Error procesando batch: {e}")
    
    async def _simulate_batch_processing(self, batch_requests: List[BatchRequest]) -> float:
        """Simula procesamiento de batch."""
        # Simular tiempo de procesamiento basado en tamaño del batch
        base_time = 10.0  # 10ms base
        batch_size_factor = len(batch_requests) * 2.0  # 2ms por request
        content_length_factor = sum(len(req.content) for req in batch_requests) * 0.001  # 0.001ms por carácter
        
        total_time = base_time + batch_size_factor + content_length_factor
        
        # Agregar variación aleatoria
        variation = np.random.normal(0, total_time * 0.1)
        total_time = max(1.0, total_time + variation)
        
        # Simular procesamiento asíncrono
        await asyncio.sleep(total_time / 1000.0)  # Convertir a segundos
        
        return total_time
    
    def _update_adaptive_config(self, batch: Batch):
        """Actualiza configuración adaptativa."""
        # Actualizar ventanas de métricas
        self.adaptive_config['throughput_window'].append(batch.throughput_tokens_per_second)
        self.adaptive_config['latency_window'].append(batch.processing_time_ms)
        
        # Ajustar parámetros si es necesario
        if len(self.adaptive_config['throughput_window']) >= 5:
            avg_throughput = np.mean(list(self.adaptive_config['throughput_window'])[-5:])
            avg_latency = np.mean(list(self.adaptive_config['latency_window'])[-5:])
            
            # Ajustar wait time basado en latencia
            if avg_latency > self.max_wait_time_ms * 1.5:
                self.adaptive_config['current_wait_time'] = max(
                    10, int(self.adaptive_config['current_wait_time'] * 0.9)
                )
            elif avg_latency < self.max_wait_time_ms * 0.5:
                self.adaptive_config['current_wait_time'] = min(
                    self.max_wait_time_ms, int(self.adaptive_config['current_wait_time'] * 1.1)
                )
    
    def _update_stats(self, batch: Batch):
        """Actualiza estadísticas."""
        self.batcher_stats['total_batches_created'] += 1
        self.batcher_stats['total_requests_processed'] += len(batch.requests)
        
        # Actualizar promedios
        total_batches = self.batcher_stats['total_batches_created']
        
        # Promedio de tamaño de batch
        current_avg = self.batcher_stats['average_batch_size']
        new_avg = ((current_avg * (total_batches - 1)) + len(batch.requests)) / total_batches
        self.batcher_stats['average_batch_size'] = new_avg
        
        # Promedio de tiempo de procesamiento
        current_avg = self.batcher_stats['average_processing_time_ms']
        new_avg = ((current_avg * (total_batches - 1)) + batch.processing_time_ms) / total_batches
        self.batcher_stats['average_processing_time_ms'] = new_avg
        
        # Promedio de throughput
        current_avg = self.batcher_stats['average_throughput_tokens_per_second']
        new_avg = ((current_avg * (total_batches - 1)) + batch.throughput_tokens_per_second) / total_batches
        self.batcher_stats['average_throughput_tokens_per_second'] = new_avg
        
        # Eficiencia de batch (utilización del tamaño máximo)
        batch_efficiency = len(batch.requests) / self.max_batch_size
        current_avg = self.batcher_stats['batch_efficiency']
        new_avg = ((current_avg * (total_batches - 1)) + batch_efficiency) / total_batches
        self.batcher_stats['batch_efficiency'] = new_avg
    
    async def submit_request(self, 
                           content: str,
                           priority: RequestPriority = RequestPriority.MEDIUM,
                           max_wait_time_ms: int = 1000,
                           metadata: Optional[Dict[str, Any]] = None,
                           callback: Optional[Callable] = None) -> str:
        """Envía request para procesamiento."""
        try:
            request_id = f"req_{int(time.time() * 1000)}_{len(content)}"
            
            request = BatchRequest(
                request_id=request_id,
                content=content,
                priority=priority,
                max_wait_time_ms=max_wait_time_ms,
                created_at=datetime.now(),
                metadata=metadata or {},
                callback=callback
            )
            
            # Agregar a cola
            success = self.batch_queue.enqueue(request)
            
            if success:
                logger.debug(f"Request {request_id} enviado para procesamiento")
                return request_id
            else:
                logger.warning(f"Request {request_id} rechazado por cola llena")
                return ""
                
        except Exception as e:
            logger.error(f"Error enviando request: {e}")
            return ""
    
    def get_batch_metrics(self) -> BatchMetrics:
        """Obtiene métricas de batching."""
        queue_status = self.batch_queue.get_queue_status()
        
        # Calcular tiempo de espera promedio
        avg_wait_time = 0.0
        if self.batch_history:
            wait_times = []
            for batch in list(self.batch_history)[-10:]:  # Últimos 10 batches
                for request in batch.requests:
                    wait_time = (batch.started_at - request.created_at).total_seconds() * 1000
                    wait_times.append(wait_time)
            
            if wait_times:
                avg_wait_time = np.mean(wait_times)
        
        # Calcular tasa de procesamiento
        processing_rate = 0.0
        if self.batch_history:
            recent_batches = list(self.batch_history)[-10:]
            if recent_batches:
                total_requests = sum(len(batch.requests) for batch in recent_batches)
                total_time = sum(batch.processing_time_ms for batch in recent_batches)
                if total_time > 0:
                    processing_rate = (total_requests / total_time) * 1000  # requests por segundo
        
        return BatchMetrics(
            total_batches=self.batcher_stats['total_batches_created'],
            total_requests=self.batcher_stats['total_requests_processed'],
            average_batch_size=self.batcher_stats['average_batch_size'],
            average_processing_time_ms=self.batcher_stats['average_processing_time_ms'],
            average_throughput_tokens_per_second=self.batcher_stats['average_throughput_tokens_per_second'],
            average_wait_time_ms=avg_wait_time,
            batch_efficiency=self.batcher_stats['batch_efficiency'],
            queue_length=queue_status['queue_stats']['current_queue_size'],
            processing_rate=processing_rate
        )
    
    def get_batcher_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del batcher."""
        return {
            'batcher_stats': self.batcher_stats,
            'adaptive_config': self.adaptive_config,
            'queue_status': self.batch_queue.get_queue_status(),
            'strategy': self.strategy.value,
            'is_processing': self.is_processing
        }
    
    def get_batch_history(self, limit: int = 10) -> List[Batch]:
        """Obtiene historial de batches."""
        return list(self.batch_history)[-limit:]


if __name__ == "__main__":
    # Test del DynamicBatcher
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_dynamic_batcher():
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
        print(f"Batch Metrics:")
        print(f"  Total Batches: {metrics.total_batches}")
        print(f"  Total Requests: {metrics.total_requests}")
        print(f"  Average Batch Size: {metrics.average_batch_size:.1f}")
        print(f"  Average Processing Time: {metrics.average_processing_time_ms:.1f}ms")
        print(f"  Average Throughput: {metrics.average_throughput_tokens_per_second:.0f} tokens/s")
        print(f"  Average Wait Time: {metrics.average_wait_time_ms:.1f}ms")
        print(f"  Batch Efficiency: {metrics.batch_efficiency:.2f}")
        print(f"  Queue Length: {metrics.queue_length}")
        print(f"  Processing Rate: {metrics.processing_rate:.1f} req/s")
        
        # Mostrar estadísticas
        stats = batcher.get_batcher_stats()
        print(f"\nBatcher Stats: {stats}")
        
        # Detener procesamiento
        await batcher.stop_processing()
    
    # Ejecutar test
    asyncio.run(test_dynamic_batcher())
