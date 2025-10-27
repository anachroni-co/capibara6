#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cost Tracking - Sistema de tracking de costos para Capibara6.
"""

import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import os

logger = logging.getLogger(__name__)

class CostType(Enum):
    """Tipos de costo."""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    API_CALLS = "api_calls"
    MODEL_INFERENCE = "model_inference"
    TRAINING = "training"
    E2B_EXECUTION = "e2b_execution"
    EXTERNAL_APIS = "external_apis"

class CostCategory(Enum):
    """Categorías de costo."""
    INFRASTRUCTURE = "infrastructure"
    MODELS = "models"
    SERVICES = "services"
    EXTERNAL = "external"
    OPERATIONS = "operations"

@dataclass
class CostEntry:
    """Entrada de costo."""
    id: str
    timestamp: datetime
    cost_type: CostType
    cost_category: CostCategory
    amount_usd: float
    resource_id: str
    resource_type: str
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    region: Optional[str] = None
    provider: Optional[str] = None

@dataclass
class CostBudget:
    """Presupuesto de costo."""
    id: str
    name: str
    cost_type: CostType
    cost_category: CostCategory
    daily_limit_usd: float
    monthly_limit_usd: float
    alert_threshold_percent: float
    enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class CostAlert:
    """Alerta de costo."""
    id: str
    budget_id: str
    alert_type: str  # "threshold", "limit_exceeded", "anomaly"
    severity: str    # "low", "medium", "high", "critical"
    message: str
    current_amount_usd: float
    limit_amount_usd: float
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None

class CostTracker:
    """Tracker de costos para Capibara6."""
    
    def __init__(self):
        self.cost_entries: List[CostEntry] = []
        self.cost_budgets: Dict[str, CostBudget] = {}
        self.cost_alerts: List[CostAlert] = []
        
        # Configuración de costos por recurso
        self.cost_config = {
            # Modelos
            "capibara6-20b": {
                "inference_cost_per_1k_tokens": 0.002,
                "training_cost_per_hour": 5.0
            },
            "capibara6-120b": {
                "inference_cost_per_1k_tokens": 0.008,
                "training_cost_per_hour": 15.0
            },
            
            # E2B
            "e2b-sandbox": {
                "execution_cost_per_second": 0.0001,
                "memory_cost_per_gb_hour": 0.05
            },
            
            # Infraestructura
            "gcp-arm-axion": {
                "compute_cost_per_hour": 0.5,
                "memory_cost_per_gb_hour": 0.02
            },
            "nvidia-h100": {
                "compute_cost_per_hour": 3.0,
                "memory_cost_per_gb_hour": 0.1
            },
            "tpu-v5e-64": {
                "compute_cost_per_hour": 8.0,
                "memory_cost_per_gb_hour": 0.05
            },
            
            # Servicios
            "postgresql": {
                "storage_cost_per_gb_month": 0.1,
                "compute_cost_per_hour": 0.2
            },
            "redis": {
                "storage_cost_per_gb_month": 0.15,
                "compute_cost_per_hour": 0.1
            },
            "timescaledb": {
                "storage_cost_per_gb_month": 0.12,
                "compute_cost_per_hour": 0.25
            }
        }
        
        # Inicializar presupuestos por defecto
        self._initialize_default_budgets()
        
        # Iniciar monitor de costos
        self._start_cost_monitor()
        
        logger.info("CostTracker inicializado")
    
    def _initialize_default_budgets(self):
        """Inicializa presupuestos por defecto."""
        default_budgets = [
            CostBudget(
                id="daily_compute_budget",
                name="Daily Compute Budget",
                cost_type=CostType.COMPUTE,
                cost_category=CostCategory.INFRASTRUCTURE,
                daily_limit_usd=50.0,
                monthly_limit_usd=1500.0,
                alert_threshold_percent=80.0,
                created_at=datetime.now()
            ),
            CostBudget(
                id="daily_model_inference_budget",
                name="Daily Model Inference Budget",
                cost_type=CostType.MODEL_INFERENCE,
                cost_category=CostCategory.MODELS,
                daily_limit_usd=100.0,
                monthly_limit_usd=3000.0,
                alert_threshold_percent=85.0,
                created_at=datetime.now()
            ),
            CostBudget(
                id="daily_e2b_budget",
                name="Daily E2B Execution Budget",
                cost_type=CostType.E2B_EXECUTION,
                cost_category=CostCategory.SERVICES,
                daily_limit_usd=20.0,
                monthly_limit_usd=600.0,
                alert_threshold_percent=90.0,
                created_at=datetime.now()
            ),
            CostBudget(
                id="daily_storage_budget",
                name="Daily Storage Budget",
                cost_type=CostType.STORAGE,
                cost_category=CostCategory.INFRASTRUCTURE,
                daily_limit_usd=10.0,
                monthly_limit_usd=300.0,
                alert_threshold_percent=75.0,
                created_at=datetime.now()
            ),
            CostBudget(
                id="daily_external_apis_budget",
                name="Daily External APIs Budget",
                cost_type=CostType.EXTERNAL_APIS,
                cost_category=CostCategory.EXTERNAL,
                daily_limit_usd=30.0,
                monthly_limit_usd=900.0,
                alert_threshold_percent=80.0,
                created_at=datetime.now()
            )
        ]
        
        for budget in default_budgets:
            self.cost_budgets[budget.id] = budget
        
        logger.info(f"Inicializados {len(default_budgets)} presupuestos por defecto")
    
    def _start_cost_monitor(self):
        """Inicia el monitor de costos en background."""
        self._monitor_thread = threading.Thread(target=self._cost_monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def _cost_monitor_loop(self):
        """Loop principal del monitor de costos."""
        while True:
            try:
                self._check_budget_alerts()
                time.sleep(300)  # Verificar cada 5 minutos
            except Exception as e:
                logger.error(f"Error en monitor de costos: {e}")
                time.sleep(600)
    
    def _check_budget_alerts(self):
        """Verifica alertas de presupuesto."""
        current_time = datetime.now()
        today = current_time.date()
        
        for budget_id, budget in self.cost_budgets.items():
            if not budget.enabled:
                continue
            
            # Calcular costos del día
            daily_cost = self._calculate_daily_cost(budget.cost_type, today)
            
            # Verificar umbral de alerta
            if daily_cost >= budget.daily_limit_usd * (budget.alert_threshold_percent / 100):
                # Crear alerta si no existe una activa
                if not self._has_active_alert(budget_id, "threshold"):
                    alert = CostAlert(
                        id=f"{budget_id}_threshold_{int(time.time())}",
                        budget_id=budget_id,
                        alert_type="threshold",
                        severity="medium" if daily_cost < budget.daily_limit_usd else "high",
                        message=f"Presupuesto {budget.name} alcanzó {budget.alert_threshold_percent}% del límite diario",
                        current_amount_usd=daily_cost,
                        limit_amount_usd=budget.daily_limit_usd,
                        timestamp=current_time
                    )
                    
                    self.cost_alerts.append(alert)
                    logger.warning(f"Alerta de presupuesto: {alert.message}")
            
            # Verificar límite excedido
            if daily_cost > budget.daily_limit_usd:
                if not self._has_active_alert(budget_id, "limit_exceeded"):
                    alert = CostAlert(
                        id=f"{budget_id}_exceeded_{int(time.time())}",
                        budget_id=budget_id,
                        alert_type="limit_exceeded",
                        severity="critical",
                        message=f"Presupuesto {budget.name} excedió el límite diario",
                        current_amount_usd=daily_cost,
                        limit_amount_usd=budget.daily_limit_usd,
                        timestamp=current_time
                    )
                    
                    self.cost_alerts.append(alert)
                    logger.critical(f"Límite de presupuesto excedido: {alert.message}")
    
    def _has_active_alert(self, budget_id: str, alert_type: str) -> bool:
        """Verifica si existe una alerta activa."""
        for alert in self.cost_alerts:
            if (alert.budget_id == budget_id and 
                alert.alert_type == alert_type and 
                not alert.acknowledged and
                (datetime.now() - alert.timestamp).total_seconds() < 3600):  # 1 hora
                return True
        return False
    
    def _calculate_daily_cost(self, cost_type: CostType, date) -> float:
        """Calcula el costo diario para un tipo específico."""
        start_time = datetime.combine(date, datetime.min.time())
        end_time = start_time + timedelta(days=1)
        
        daily_entries = [
            entry for entry in self.cost_entries
            if (entry.cost_type == cost_type and 
                start_time <= entry.timestamp < end_time)
        ]
        
        return sum(entry.amount_usd for entry in daily_entries)
    
    # Métodos públicos para registrar costos
    def record_model_inference_cost(self, 
                                   model_name: str, 
                                   tokens_used: int, 
                                   user_id: Optional[str] = None,
                                   request_id: Optional[str] = None) -> str:
        """Registra costo de inferencia de modelo."""
        if model_name not in self.cost_config:
            logger.warning(f"Configuración de costo no encontrada para modelo: {model_name}")
            return None
        
        cost_per_1k_tokens = self.cost_config[model_name]["inference_cost_per_1k_tokens"]
        amount_usd = (tokens_used / 1000) * cost_per_1k_tokens
        
        cost_entry = CostEntry(
            id=f"model_inf_{int(time.time() * 1000)}",
            timestamp=datetime.now(),
            cost_type=CostType.MODEL_INFERENCE,
            cost_category=CostCategory.MODELS,
            amount_usd=amount_usd,
            resource_id=model_name,
            resource_type="model",
            user_id=user_id,
            request_id=request_id,
            metadata={"tokens_used": tokens_used, "cost_per_1k_tokens": cost_per_1k_tokens}
        )
        
        self.cost_entries.append(cost_entry)
        return cost_entry.id
    
    def record_e2b_execution_cost(self, 
                                 execution_time_seconds: float,
                                 memory_used_gb: float,
                                 user_id: Optional[str] = None,
                                 request_id: Optional[str] = None) -> str:
        """Registra costo de ejecución E2B."""
        execution_cost = execution_time_seconds * self.cost_config["e2b-sandbox"]["execution_cost_per_second"]
        memory_cost = (memory_used_gb * execution_time_seconds / 3600) * self.cost_config["e2b-sandbox"]["memory_cost_per_gb_hour"]
        amount_usd = execution_cost + memory_cost
        
        cost_entry = CostEntry(
            id=f"e2b_exec_{int(time.time() * 1000)}",
            timestamp=datetime.now(),
            cost_type=CostType.E2B_EXECUTION,
            cost_category=CostCategory.SERVICES,
            amount_usd=amount_usd,
            resource_id="e2b-sandbox",
            resource_type="sandbox",
            user_id=user_id,
            request_id=request_id,
            metadata={
                "execution_time_seconds": execution_time_seconds,
                "memory_used_gb": memory_used_gb
            }
        )
        
        self.cost_entries.append(cost_entry)
        return cost_entry.id
    
    def record_compute_cost(self, 
                           resource_type: str,
                           hours_used: float,
                           user_id: Optional[str] = None) -> str:
        """Registra costo de cómputo."""
        if resource_type not in self.cost_config:
            logger.warning(f"Configuración de costo no encontrada para recurso: {resource_type}")
            return None
        
        cost_per_hour = self.cost_config[resource_type]["compute_cost_per_hour"]
        amount_usd = hours_used * cost_per_hour
        
        cost_entry = CostEntry(
            id=f"compute_{int(time.time() * 1000)}",
            timestamp=datetime.now(),
            cost_type=CostType.COMPUTE,
            cost_category=CostCategory.INFRASTRUCTURE,
            amount_usd=amount_usd,
            resource_id=resource_type,
            resource_type="compute",
            user_id=user_id,
            metadata={"hours_used": hours_used, "cost_per_hour": cost_per_hour}
        )
        
        self.cost_entries.append(cost_entry)
        return cost_entry.id
    
    def record_storage_cost(self, 
                           storage_type: str,
                           gb_used: float,
                           days: int = 1) -> str:
        """Registra costo de almacenamiento."""
        if storage_type not in self.cost_config:
            logger.warning(f"Configuración de costo no encontrada para almacenamiento: {storage_type}")
            return None
        
        cost_per_gb_month = self.cost_config[storage_type]["storage_cost_per_gb_month"]
        amount_usd = (gb_used * cost_per_gb_month * days) / 30  # Convertir a días
        
        cost_entry = CostEntry(
            id=f"storage_{int(time.time() * 1000)}",
            timestamp=datetime.now(),
            cost_type=CostType.STORAGE,
            cost_category=CostCategory.INFRASTRUCTURE,
            amount_usd=amount_usd,
            resource_id=storage_type,
            resource_type="storage",
            metadata={"gb_used": gb_used, "days": days, "cost_per_gb_month": cost_per_gb_month}
        )
        
        self.cost_entries.append(cost_entry)
        return cost_entry.id
    
    def record_external_api_cost(self, 
                                api_name: str,
                                calls_made: int,
                                cost_per_call: float,
                                user_id: Optional[str] = None,
                                request_id: Optional[str] = None) -> str:
        """Registra costo de APIs externas."""
        amount_usd = calls_made * cost_per_call
        
        cost_entry = CostEntry(
            id=f"external_api_{int(time.time() * 1000)}",
            timestamp=datetime.now(),
            cost_type=CostType.EXTERNAL_APIS,
            cost_category=CostCategory.EXTERNAL,
            amount_usd=amount_usd,
            resource_id=api_name,
            resource_type="external_api",
            user_id=user_id,
            request_id=request_id,
            metadata={"calls_made": calls_made, "cost_per_call": cost_per_call}
        )
        
        self.cost_entries.append(cost_entry)
        return cost_entry.id
    
    # Métodos de consulta
    def get_daily_costs(self, date: Optional[datetime] = None) -> Dict[str, float]:
        """Obtiene costos diarios por tipo."""
        if date is None:
            date = datetime.now().date()
        
        daily_costs = {}
        for cost_type in CostType:
            daily_costs[cost_type.value] = self._calculate_daily_cost(cost_type, date)
        
        return daily_costs
    
    def get_monthly_costs(self, year: int, month: int) -> Dict[str, float]:
        """Obtiene costos mensuales por tipo."""
        start_date = datetime(year, month, 1).date()
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        monthly_costs = {}
        for cost_type in CostType:
            total_cost = 0.0
            current_date = start_date
            
            while current_date <= end_date:
                total_cost += self._calculate_daily_cost(cost_type, current_date)
                current_date += timedelta(days=1)
            
            monthly_costs[cost_type.value] = total_cost
        
        return monthly_costs
    
    def get_user_costs(self, user_id: str, days: int = 30) -> Dict[str, float]:
        """Obtiene costos por usuario."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        user_entries = [
            entry for entry in self.cost_entries
            if entry.user_id == user_id and entry.timestamp >= cutoff_date
        ]
        
        user_costs = {}
        for cost_type in CostType:
            user_costs[cost_type.value] = sum(
                entry.amount_usd for entry in user_entries
                if entry.cost_type == cost_type
            )
        
        return user_costs
    
    def get_cost_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de costos."""
        if not self.cost_entries:
            return {
                "total_entries": 0,
                "total_cost_usd": 0.0,
                "daily_average": 0.0,
                "cost_by_type": {},
                "cost_by_category": {},
                "top_users": [],
                "cost_trend": []
            }
        
        # Costo total
        total_cost = sum(entry.amount_usd for entry in self.cost_entries)
        
        # Costo por tipo
        cost_by_type = {}
        for cost_type in CostType:
            cost_by_type[cost_type.value] = sum(
                entry.amount_usd for entry in self.cost_entries
                if entry.cost_type == cost_type
            )
        
        # Costo por categoría
        cost_by_category = {}
        for cost_category in CostCategory:
            cost_by_category[cost_category.value] = sum(
                entry.amount_usd for entry in self.cost_entries
                if entry.cost_category == cost_category
            )
        
        # Top usuarios
        user_costs = {}
        for entry in self.cost_entries:
            if entry.user_id:
                user_costs[entry.user_id] = user_costs.get(entry.user_id, 0) + entry.amount_usd
        
        top_users = sorted(user_costs.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Tendencia de costos (últimos 7 días)
        cost_trend = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).date()
            daily_total = sum(self._calculate_daily_cost(cost_type, date) for cost_type in CostType)
            cost_trend.append({
                "date": date.isoformat(),
                "cost_usd": daily_total
            })
        
        cost_trend.reverse()  # Más antiguo primero
        
        # Promedio diario
        if self.cost_entries:
            date_range = (max(entry.timestamp for entry in self.cost_entries) - 
                         min(entry.timestamp for entry in self.cost_entries)).days + 1
            daily_average = total_cost / date_range if date_range > 0 else 0
        else:
            daily_average = 0
        
        return {
            "total_entries": len(self.cost_entries),
            "total_cost_usd": total_cost,
            "daily_average": daily_average,
            "cost_by_type": cost_by_type,
            "cost_by_category": cost_by_category,
            "top_users": top_users,
            "cost_trend": cost_trend
        }
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Obtiene estado de los presupuestos."""
        today = datetime.now().date()
        budget_status = {}
        
        for budget_id, budget in self.cost_budgets.items():
            daily_cost = self._calculate_daily_cost(budget.cost_type, today)
            
            budget_status[budget_id] = {
                "name": budget.name,
                "cost_type": budget.cost_type.value,
                "daily_limit_usd": budget.daily_limit_usd,
                "monthly_limit_usd": budget.monthly_limit_usd,
                "current_daily_cost_usd": daily_cost,
                "daily_usage_percent": (daily_cost / budget.daily_limit_usd) * 100 if budget.daily_limit_usd > 0 else 0,
                "alert_threshold_percent": budget.alert_threshold_percent,
                "status": "ok" if daily_cost < budget.daily_limit_usd else "exceeded",
                "enabled": budget.enabled
            }
        
        return budget_status
    
    def get_active_alerts(self) -> List[CostAlert]:
        """Obtiene alertas activas."""
        return [alert for alert in self.cost_alerts if not alert.acknowledged]
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Reconoce una alerta."""
        for alert in self.cost_alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                logger.info(f"Alerta de costo reconocida: {alert_id} por {acknowledged_by}")
                return True
        return False


# Instancia global
cost_tracker = CostTracker()


def get_cost_tracker() -> CostTracker:
    """Obtiene la instancia global del tracker de costos."""
    return cost_tracker


if __name__ == "__main__":
    # Test del sistema de tracking de costos
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    tracker = CostTracker()
    
    # Simular algunos costos
    tracker.record_model_inference_cost("capibara6-20b", 1000, "user_123", "req_456")
    tracker.record_e2b_execution_cost(30.0, 2.0, "user_123", "req_789")
    tracker.record_compute_cost("gcp-arm-axion", 2.0, "user_123")
    tracker.record_storage_cost("postgresql", 100.0, 1)
    tracker.record_external_api_cost("openai", 10, 0.002, "user_123", "req_101")
    
    # Obtener estadísticas
    stats = tracker.get_cost_statistics()
    print("Estadísticas de costos:")
    print(json.dumps(stats, indent=2, default=str))
    
    # Obtener estado de presupuestos
    budget_status = tracker.get_budget_status()
    print("\nEstado de presupuestos:")
    print(json.dumps(budget_status, indent=2, default=str))
    
    # Obtener alertas activas
    active_alerts = tracker.get_active_alerts()
    print(f"\nAlertas activas: {len(active_alerts)}")
    
    print("Sistema de tracking de costos funcionando correctamente!")
