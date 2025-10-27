#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Budget Forcing - Sistema de control de recursos y presupuesto para optimización.
"""

import logging
import json
import os
import time
import threading
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Tipos de recursos."""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    TPU = "tpu"
    NETWORK = "network"
    STORAGE = "storage"
    API_CALLS = "api_calls"
    TOKENS = "tokens"


class BudgetType(Enum):
    """Tipos de presupuesto."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    PER_REQUEST = "per_request"
    PER_SESSION = "per_session"


class EnforcementLevel(Enum):
    """Niveles de enforcement."""
    SOFT = "soft"  # Advertencias
    MEDIUM = "medium"  # Limitaciones
    HARD = "hard"  # Bloqueo completo


@dataclass
class ResourceBudget:
    """Presupuesto de recurso."""
    resource_type: ResourceType
    budget_type: BudgetType
    limit: float
    current_usage: float
    unit: str
    enforcement_level: EnforcementLevel
    reset_time: datetime
    metadata: Dict[str, Any]


@dataclass
class BudgetAllocation:
    """Asignación de presupuesto."""
    allocation_id: str
    resource_type: ResourceType
    amount: float
    priority: int
    duration_seconds: int
    allocated_at: datetime
    expires_at: datetime
    is_active: bool
    metadata: Dict[str, Any]


@dataclass
class BudgetRequest:
    """Solicitud de presupuesto."""
    request_id: str
    resource_type: ResourceType
    requested_amount: float
    priority: int
    estimated_duration: int
    requester_id: str
    justification: str
    created_at: datetime


@dataclass
class BudgetViolation:
    """Violación de presupuesto."""
    violation_id: str
    resource_type: ResourceType
    requested_amount: float
    available_amount: float
    violation_type: str
    severity: str
    timestamp: datetime
    requester_id: str
    action_taken: str


class ResourceMonitor:
    """Monitor de recursos."""
    
    def __init__(self):
        self.resource_usage: Dict[ResourceType, float] = defaultdict(float)
        self.resource_limits: Dict[ResourceType, float] = {}
        self.usage_history: Dict[ResourceType, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Métricas de rendimiento
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'blocked_requests': 0,
            'average_response_time_ms': 0.0,
            'resource_utilization': defaultdict(float)
        }
        
        logger.info("ResourceMonitor inicializado")
    
    def get_resource_usage(self, resource_type: ResourceType) -> float:
        """Obtiene uso actual de recurso."""
        return self.resource_usage[resource_type]
    
    def set_resource_limit(self, resource_type: ResourceType, limit: float):
        """Establece límite de recurso."""
        self.resource_limits[resource_type] = limit
        logger.info(f"Límite establecido para {resource_type.value}: {limit}")
    
    def update_resource_usage(self, resource_type: ResourceType, usage: float):
        """Actualiza uso de recurso."""
        self.resource_usage[resource_type] = usage
        self.usage_history[resource_type].append({
            'timestamp': datetime.now(),
            'usage': usage
        })
        
        # Actualizar métricas
        if resource_type in self.resource_limits:
            utilization = usage / self.resource_limits[resource_type]
            self.performance_metrics['resource_utilization'][resource_type.value] = utilization
    
    def check_resource_availability(self, resource_type: ResourceType, requested_amount: float) -> bool:
        """Verifica disponibilidad de recurso."""
        current_usage = self.resource_usage[resource_type]
        limit = self.resource_limits.get(resource_type, float('inf'))
        
        return (current_usage + requested_amount) <= limit
    
    def get_resource_status(self) -> Dict[str, Any]:
        """Obtiene estado de recursos."""
        status = {}
        
        for resource_type in ResourceType:
            current_usage = self.resource_usage[resource_type]
            limit = self.resource_limits.get(resource_type, 0)
            utilization = (current_usage / limit * 100) if limit > 0 else 0
            
            status[resource_type.value] = {
                'current_usage': current_usage,
                'limit': limit,
                'utilization_percentage': utilization,
                'available': limit - current_usage,
                'is_over_limit': current_usage > limit
            }
        
        return status


class BudgetForcing:
    """Sistema de control de presupuesto y recursos."""
    
    def __init__(self, 
                 enforcement_level: EnforcementLevel = EnforcementLevel.MEDIUM,
                 monitoring_interval: int = 60):
        self.enforcement_level = enforcement_level
        self.monitoring_interval = monitoring_interval
        
        # Componentes
        self.resource_monitor = ResourceMonitor()
        
        # Presupuestos
        self.budgets: Dict[str, ResourceBudget] = {}
        
        # Asignaciones activas
        self.active_allocations: Dict[str, BudgetAllocation] = {}
        
        # Historial
        self.budget_requests: deque = deque(maxlen=10000)
        self.budget_violations: deque = deque(maxlen=1000)
        
        # Configuración
        self.default_limits = {
            ResourceType.CPU: 80.0,  # 80% CPU
            ResourceType.MEMORY: 8.0,  # 8GB RAM
            ResourceType.GPU: 1.0,  # 1 GPU
            ResourceType.TPU: 0.0,  # 0 TPU por defecto
            ResourceType.NETWORK: 1000.0,  # 1000 MB/s
            ResourceType.STORAGE: 100.0,  # 100GB
            ResourceType.API_CALLS: 1000.0,  # 1000 calls/hour
            ResourceType.TOKENS: 100000.0  # 100K tokens/hour
        }
        
        # Estadísticas
        self.budget_stats = {
            'total_requests': 0,
            'approved_requests': 0,
            'rejected_requests': 0,
            'total_violations': 0,
            'total_allocations': 0,
            'average_allocation_time_seconds': 0.0
        }
        
        # Thread de monitoreo
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Inicializar presupuestos por defecto
        self._initialize_default_budgets()
        
        logger.info(f"BudgetForcing inicializado: enforcement={enforcement_level.value}")
    
    def _initialize_default_budgets(self):
        """Inicializa presupuestos por defecto."""
        for resource_type, limit in self.default_limits.items():
            budget = ResourceBudget(
                resource_type=resource_type,
                budget_type=BudgetType.PER_REQUEST,
                limit=limit,
                current_usage=0.0,
                unit=self._get_resource_unit(resource_type),
                enforcement_level=self.enforcement_level,
                reset_time=datetime.now() + timedelta(hours=1),
                metadata={'auto_created': True}
            )
            
            budget_id = f"default_{resource_type.value}"
            self.budgets[budget_id] = budget
            
            # Establecer límite en monitor
            self.resource_monitor.set_resource_limit(resource_type, limit)
    
    def _get_resource_unit(self, resource_type: ResourceType) -> str:
        """Obtiene unidad de recurso."""
        units = {
            ResourceType.CPU: "%",
            ResourceType.MEMORY: "GB",
            ResourceType.GPU: "units",
            ResourceType.TPU: "cores",
            ResourceType.NETWORK: "MB/s",
            ResourceType.STORAGE: "GB",
            ResourceType.API_CALLS: "calls",
            ResourceType.TOKENS: "tokens"
        }
        return units.get(resource_type, "units")
    
    def request_budget(self, request: BudgetRequest) -> Tuple[bool, Optional[str], str]:
        """Solicita presupuesto."""
        try:
            self.budget_stats['total_requests'] += 1
            self.budget_requests.append(request)
            
            # Verificar disponibilidad
            is_available, allocation_id, message = self._check_budget_availability(request)
            
            if is_available:
                # Crear asignación
                allocation = self._create_allocation(request, allocation_id)
                self.active_allocations[allocation_id] = allocation
                
                # Actualizar uso de recursos
                self._update_resource_usage(request.resource_type, request.requested_amount)
                
                self.budget_stats['approved_requests'] += 1
                self.budget_stats['total_allocations'] += 1
                
                logger.info(f"Presupuesto aprobado: {allocation_id} ({request.requested_amount} {self._get_resource_unit(request.resource_type)})")
                return True, allocation_id, message
            else:
                # Crear violación si es necesario
                if self.enforcement_level in [EnforcementLevel.MEDIUM, EnforcementLevel.HARD]:
                    self._create_violation(request, "insufficient_budget")
                
                self.budget_stats['rejected_requests'] += 1
                
                logger.warning(f"Presupuesto rechazado: {request.request_id} - {message}")
                return False, None, message
                
        except Exception as e:
            logger.error(f"Error solicitando presupuesto: {e}")
            return False, None, f"Error interno: {e}"
    
    def _check_budget_availability(self, request: BudgetRequest) -> Tuple[bool, Optional[str], str]:
        """Verifica disponibilidad de presupuesto."""
        resource_type = request.resource_type
        requested_amount = request.requested_amount
        
        # Verificar límites del monitor
        if not self.resource_monitor.check_resource_availability(resource_type, requested_amount):
            current_usage = self.resource_monitor.get_resource_usage(resource_type)
            limit = self.resource_monitor.resource_limits.get(resource_type, 0)
            available = max(0, limit - current_usage)
            
            return False, None, f"Recurso {resource_type.value} insuficiente. Disponible: {available}, Solicitado: {requested_amount}"
        
        # Verificar presupuestos específicos
        for budget_id, budget in self.budgets.items():
            if budget.resource_type == resource_type:
                if budget.current_usage + requested_amount > budget.limit:
                    available = max(0, budget.limit - budget.current_usage)
                    
                    if budget.enforcement_level == EnforcementLevel.HARD:
                        return False, None, f"Presupuesto {budget_id} excedido. Disponible: {available}, Solicitado: {requested_amount}"
                    elif budget.enforcement_level == EnforcementLevel.MEDIUM:
                        # Permitir pero con advertencia
                        logger.warning(f"Presupuesto {budget_id} cerca del límite")
        
        # Generar ID de asignación
        allocation_id = f"alloc_{request.request_id}_{int(time.time())}"
        
        return True, allocation_id, "Presupuesto disponible"
    
    def _create_allocation(self, request: BudgetRequest, allocation_id: str) -> BudgetAllocation:
        """Crea asignación de presupuesto."""
        allocation = BudgetAllocation(
            allocation_id=allocation_id,
            resource_type=request.resource_type,
            amount=request.requested_amount,
            priority=request.priority,
            duration_seconds=request.estimated_duration,
            allocated_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=request.estimated_duration),
            is_active=True,
            metadata={
                'requester_id': request.requester_id,
                'justification': request.justification,
                'request_id': request.request_id
            }
        )
        
        return allocation
    
    def _update_resource_usage(self, resource_type: ResourceType, amount: float):
        """Actualiza uso de recursos."""
        current_usage = self.resource_monitor.get_resource_usage(resource_type)
        new_usage = current_usage + amount
        self.resource_monitor.update_resource_usage(resource_type, new_usage)
        
        # Actualizar presupuestos
        for budget in self.budgets.values():
            if budget.resource_type == resource_type:
                budget.current_usage += amount
    
    def _create_violation(self, request: BudgetRequest, violation_type: str):
        """Crea violación de presupuesto."""
        violation = BudgetViolation(
            violation_id=f"violation_{request.request_id}_{int(time.time())}",
            resource_type=request.resource_type,
            requested_amount=request.requested_amount,
            available_amount=self._get_available_amount(request.resource_type),
            violation_type=violation_type,
            severity=self._determine_severity(request),
            timestamp=datetime.now(),
            requester_id=request.requester_id,
            action_taken=self._determine_action(violation_type)
        )
        
        self.budget_violations.append(violation)
        self.budget_stats['total_violations'] += 1
        
        logger.warning(f"Violación de presupuesto: {violation.violation_id} - {violation_type}")
    
    def _get_available_amount(self, resource_type: ResourceType) -> float:
        """Obtiene cantidad disponible de recurso."""
        current_usage = self.resource_monitor.get_resource_usage(resource_type)
        limit = self.resource_monitor.resource_limits.get(resource_type, 0)
        return max(0, limit - current_usage)
    
    def _determine_severity(self, request: BudgetRequest) -> str:
        """Determina severidad de violación."""
        if request.priority <= 2:
            return "high"
        elif request.priority <= 4:
            return "medium"
        else:
            return "low"
    
    def _determine_action(self, violation_type: str) -> str:
        """Determina acción a tomar."""
        if self.enforcement_level == EnforcementLevel.HARD:
            return "blocked"
        elif self.enforcement_level == EnforcementLevel.MEDIUM:
            return "limited"
        else:
            return "warned"
    
    def release_budget(self, allocation_id: str) -> bool:
        """Libera presupuesto asignado."""
        try:
            if allocation_id not in self.active_allocations:
                logger.warning(f"Asignación no encontrada: {allocation_id}")
                return False
            
            allocation = self.active_allocations[allocation_id]
            
            # Marcar como inactiva
            allocation.is_active = False
            
            # Liberar recursos
            self._release_resource_usage(allocation.resource_type, allocation.amount)
            
            # Remover de asignaciones activas
            del self.active_allocations[allocation_id]
            
            logger.info(f"Presupuesto liberado: {allocation_id} ({allocation.amount} {self._get_resource_unit(allocation.resource_type)})")
            return True
            
        except Exception as e:
            logger.error(f"Error liberando presupuesto: {e}")
            return False
    
    def _release_resource_usage(self, resource_type: ResourceType, amount: float):
        """Libera uso de recursos."""
        current_usage = self.resource_monitor.get_resource_usage(resource_type)
        new_usage = max(0, current_usage - amount)
        self.resource_monitor.update_resource_usage(resource_type, new_usage)
        
        # Actualizar presupuestos
        for budget in self.budgets.values():
            if budget.resource_type == resource_type:
                budget.current_usage = max(0, budget.current_usage - amount)
    
    def create_budget(self, 
                     resource_type: ResourceType,
                     budget_type: BudgetType,
                     limit: float,
                     enforcement_level: EnforcementLevel = None,
                     reset_time: Optional[datetime] = None) -> str:
        """Crea nuevo presupuesto."""
        try:
            budget_id = f"budget_{resource_type.value}_{budget_type.value}_{int(time.time())}"
            
            if reset_time is None:
                if budget_type == BudgetType.DAILY:
                    reset_time = datetime.now() + timedelta(days=1)
                elif budget_type == BudgetType.WEEKLY:
                    reset_time = datetime.now() + timedelta(weeks=1)
                elif budget_type == BudgetType.MONTHLY:
                    reset_time = datetime.now() + timedelta(days=30)
                else:
                    reset_time = datetime.now() + timedelta(hours=1)
            
            budget = ResourceBudget(
                resource_type=resource_type,
                budget_type=budget_type,
                limit=limit,
                current_usage=0.0,
                unit=self._get_resource_unit(resource_type),
                enforcement_level=enforcement_level or self.enforcement_level,
                reset_time=reset_time,
                metadata={'created_at': datetime.now().isoformat()}
            )
            
            self.budgets[budget_id] = budget
            
            # Actualizar límite en monitor si es mayor
            current_limit = self.resource_monitor.resource_limits.get(resource_type, 0)
            if limit > current_limit:
                self.resource_monitor.set_resource_limit(resource_type, limit)
            
            logger.info(f"Presupuesto creado: {budget_id} ({limit} {budget.unit})")
            return budget_id
            
        except Exception as e:
            logger.error(f"Error creando presupuesto: {e}")
            return ""
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Obtiene estado de presupuestos."""
        status = {
            'budgets': {},
            'active_allocations': len(self.active_allocations),
            'total_violations': len(self.budget_violations),
            'resource_status': self.resource_monitor.get_resource_status()
        }
        
        for budget_id, budget in self.budgets.items():
            utilization = (budget.current_usage / budget.limit * 100) if budget.limit > 0 else 0
            
            status['budgets'][budget_id] = {
                'resource_type': budget.resource_type.value,
                'budget_type': budget.budget_type.value,
                'limit': budget.limit,
                'current_usage': budget.current_usage,
                'utilization_percentage': utilization,
                'available': budget.limit - budget.current_usage,
                'enforcement_level': budget.enforcement_level.value,
                'reset_time': budget.reset_time.isoformat(),
                'is_over_limit': budget.current_usage > budget.limit
            }
        
        return status
    
    def get_budget_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de presupuesto."""
        return {
            'budget_stats': self.budget_stats,
            'performance_metrics': self.resource_monitor.performance_metrics,
            'total_budgets': len(self.budgets),
            'active_allocations': len(self.active_allocations),
            'recent_violations': len([v for v in self.budget_violations if (datetime.now() - v.timestamp).total_seconds() < 3600])
        }
    
    def start_monitoring(self):
        """Inicia monitoreo de presupuestos."""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("Monitoreo de presupuestos iniciado")
    
    def stop_monitoring(self):
        """Detiene monitoreo de presupuestos."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("Monitoreo de presupuestos detenido")
    
    def _monitoring_loop(self):
        """Loop de monitoreo."""
        while self.is_monitoring:
            try:
                # Limpiar asignaciones expiradas
                self._cleanup_expired_allocations()
                
                # Resetear presupuestos si es necesario
                self._reset_budgets_if_needed()
                
                # Actualizar métricas
                self._update_monitoring_metrics()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error en loop de monitoreo: {e}")
                time.sleep(self.monitoring_interval)
    
    def _cleanup_expired_allocations(self):
        """Limpia asignaciones expiradas."""
        current_time = datetime.now()
        expired_allocations = []
        
        for allocation_id, allocation in self.active_allocations.items():
            if current_time > allocation.expires_at:
                expired_allocations.append(allocation_id)
        
        for allocation_id in expired_allocations:
            self.release_budget(allocation_id)
            logger.info(f"Asignación expirada liberada: {allocation_id}")
    
    def _reset_budgets_if_needed(self):
        """Resetea presupuestos si es necesario."""
        current_time = datetime.now()
        
        for budget in self.budgets.values():
            if current_time >= budget.reset_time:
                budget.current_usage = 0.0
                
                # Recalcular tiempo de reset
                if budget.budget_type == BudgetType.DAILY:
                    budget.reset_time = current_time + timedelta(days=1)
                elif budget.budget_type == BudgetType.WEEKLY:
                    budget.reset_time = current_time + timedelta(weeks=1)
                elif budget.budget_type == BudgetType.MONTHLY:
                    budget.reset_time = current_time + timedelta(days=30)
                else:
                    budget.reset_time = current_time + timedelta(hours=1)
                
                logger.info(f"Presupuesto reseteado: {budget.resource_type.value}")
    
    def _update_monitoring_metrics(self):
        """Actualiza métricas de monitoreo."""
        # Actualizar tiempo promedio de asignación
        if self.active_allocations:
            total_time = sum(
                (datetime.now() - alloc.allocated_at).total_seconds()
                for alloc in self.active_allocations.values()
            )
            avg_time = total_time / len(self.active_allocations)
            self.budget_stats['average_allocation_time_seconds'] = avg_time


if __name__ == "__main__":
    # Test del BudgetForcing
    logging.basicConfig(level=logging.INFO)
    
    budget_forcing = BudgetForcing(enforcement_level=EnforcementLevel.MEDIUM)
    
    # Crear presupuestos personalizados
    cpu_budget_id = budget_forcing.create_budget(
        ResourceType.CPU,
        BudgetType.PER_REQUEST,
        50.0,  # 50% CPU
        EnforcementLevel.HARD
    )
    
    memory_budget_id = budget_forcing.create_budget(
        ResourceType.MEMORY,
        BudgetType.PER_REQUEST,
        4.0,  # 4GB RAM
        EnforcementLevel.MEDIUM
    )
    
    # Test de solicitudes de presupuesto
    test_requests = [
        BudgetRequest(
            request_id="req_001",
            resource_type=ResourceType.CPU,
            requested_amount=30.0,
            priority=1,
            estimated_duration=300,
            requester_id="user_001",
            justification="Training model",
            created_at=datetime.now()
        ),
        BudgetRequest(
            request_id="req_002",
            resource_type=ResourceType.MEMORY,
            requested_amount=2.0,
            priority=2,
            estimated_duration=600,
            requester_id="user_002",
            justification="Data processing",
            created_at=datetime.now()
        ),
        BudgetRequest(
            request_id="req_003",
            resource_type=ResourceType.CPU,
            requested_amount=40.0,  # Excedería el límite
            priority=3,
            estimated_duration=200,
            requester_id="user_003",
            justification="Heavy computation",
            created_at=datetime.now()
        )
    ]
    
    # Procesar solicitudes
    for request in test_requests:
        approved, allocation_id, message = budget_forcing.request_budget(request)
        print(f"Request {request.request_id}: {'Aprobado' if approved else 'Rechazado'}")
        print(f"  Message: {message}")
        if allocation_id:
            print(f"  Allocation ID: {allocation_id}")
        print("-" * 50)
    
    # Mostrar estado
    status = budget_forcing.get_budget_status()
    print(f"Estado de presupuestos:")
    print(f"  Asignaciones activas: {status['active_allocations']}")
    print(f"  Violaciones totales: {status['total_violations']}")
    
    # Mostrar estadísticas
    stats = budget_forcing.get_budget_stats()
    print(f"Estadísticas: {stats}")
    
    # Liberar presupuesto
    if status['active_allocations'] > 0:
        first_allocation = list(budget_forcing.active_allocations.keys())[0]
        released = budget_forcing.release_budget(first_allocation)
        print(f"Presupuesto liberado: {released}")
    
    # Detener monitoreo
    budget_forcing.stop_monitoring()
