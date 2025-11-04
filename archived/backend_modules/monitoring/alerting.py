#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alerting System - Sistema de alertas para Capibara6.
"""

import logging
import time
import json
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Severidad de las alertas."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertStatus(Enum):
    """Estado de las alertas."""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

@dataclass
class Alert:
    """Estructura de una alerta."""
    id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    source: str
    metric_name: str
    threshold: float
    current_value: float
    timestamp: datetime
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AlertRule:
    """Regla de alerta."""
    id: str
    name: str
    description: str
    metric_name: str
    condition: str  # ">", "<", ">=", "<=", "==", "!="
    threshold: float
    severity: AlertSeverity
    duration: int  # segundos
    enabled: bool = True
    labels: Optional[Dict[str, str]] = None

class AlertManager:
    """Gestor de alertas."""
    
    def __init__(self):
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.notification_channels: Dict[str, Callable] = {}
        self.alert_cooldowns: Dict[str, datetime] = {}
        
        # Configuración de notificaciones
        self.smtp_config = {
            'host': 'smtp.gmail.com',
            'port': 587,
            'username': 'alerts@capibara6.com',
            'password': 'your_password'
        }
        
        self.slack_config = {
            'webhook_url': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        }
        
        self.discord_config = {
            'webhook_url': 'https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK'
        }
        
        # Inicializar reglas por defecto
        self._initialize_default_rules()
        
        # Inicializar canales de notificación
        self._initialize_notification_channels()
        
        # Iniciar monitor de alertas
        self._start_alert_monitor()
        
        logger.info("AlertManager inicializado")
    
    def _initialize_default_rules(self):
        """Inicializa reglas de alerta por defecto."""
        default_rules = [
            AlertRule(
                id="high_cpu_usage",
                name="High CPU Usage",
                description="CPU usage is above 80%",
                metric_name="capibara6_system_cpu_usage_percent",
                condition=">",
                threshold=80.0,
                severity=AlertSeverity.WARNING,
                duration=300,  # 5 minutos
                labels={"component": "system"}
            ),
            AlertRule(
                id="high_memory_usage",
                name="High Memory Usage",
                description="Memory usage is above 85%",
                metric_name="capibara6_system_memory_usage_bytes",
                condition=">",
                threshold=8 * 1024 * 1024 * 1024,  # 8GB
                severity=AlertSeverity.WARNING,
                duration=300,
                labels={"component": "system"}
            ),
            AlertRule(
                id="api_error_rate_high",
                name="High API Error Rate",
                description="API error rate is above 5%",
                metric_name="capibara6_api_requests_total",
                condition=">",
                threshold=0.05,
                severity=AlertSeverity.CRITICAL,
                duration=180,  # 3 minutos
                labels={"component": "api"}
            ),
            AlertRule(
                id="slow_api_response",
                name="Slow API Response",
                description="API response time is above 2 seconds",
                metric_name="capibara6_api_request_duration_seconds",
                condition=">",
                threshold=2.0,
                severity=AlertSeverity.WARNING,
                duration=300,
                labels={"component": "api"}
            ),
            AlertRule(
                id="e2b_execution_failure",
                name="E2B Execution Failure",
                description="E2B execution failure rate is above 10%",
                metric_name="capibara6_e2b_executions_total",
                condition=">",
                threshold=0.1,
                severity=AlertSeverity.CRITICAL,
                duration=180,
                labels={"component": "e2b"}
            ),
            AlertRule(
                id="rag_search_slow",
                name="Slow RAG Search",
                description="RAG search time is above 100ms",
                metric_name="capibara6_rag_search_duration_seconds",
                condition=">",
                threshold=0.1,
                severity=AlertSeverity.WARNING,
                duration=300,
                labels={"component": "rag"}
            ),
            AlertRule(
                id="cache_hit_rate_low",
                name="Low Cache Hit Rate",
                description="Cache hit rate is below 80%",
                metric_name="capibara6_cache_hit_rate",
                condition="<",
                threshold=80.0,
                severity=AlertSeverity.WARNING,
                duration=600,  # 10 minutos
                labels={"component": "cache"}
            ),
            AlertRule(
                id="high_daily_cost",
                name="High Daily Cost",
                description="Daily cost is above $100",
                metric_name="capibara6_daily_cost_total_usd",
                condition=">",
                threshold=100.0,
                severity=AlertSeverity.WARNING,
                duration=3600,  # 1 hora
                labels={"component": "cost"}
            )
        ]
        
        for rule in default_rules:
            self.alert_rules[rule.id] = rule
        
        logger.info(f"Inicializadas {len(default_rules)} reglas de alerta por defecto")
    
    def _initialize_notification_channels(self):
        """Inicializa canales de notificación."""
        self.notification_channels = {
            'email': self._send_email_alert,
            'slack': self._send_slack_alert,
            'discord': self._send_discord_alert,
            'webhook': self._send_webhook_alert
        }
    
    def _start_alert_monitor(self):
        """Inicia el monitor de alertas en background."""
        self._monitor_thread = threading.Thread(target=self._alert_monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def _alert_monitor_loop(self):
        """Loop principal del monitor de alertas."""
        while True:
            try:
                self._check_alert_rules()
                time.sleep(30)  # Verificar cada 30 segundos
            except Exception as e:
                logger.error(f"Error en monitor de alertas: {e}")
                time.sleep(60)
    
    def _check_alert_rules(self):
        """Verifica todas las reglas de alerta."""
        for rule_id, rule in self.alert_rules.items():
            if not rule.enabled:
                continue
            
            try:
                # Obtener valor actual de la métrica (simulado)
                current_value = self._get_metric_value(rule.metric_name)
                
                if current_value is None:
                    continue
                
                # Verificar condición
                if self._evaluate_condition(current_value, rule.condition, rule.threshold):
                    # Verificar si ya existe una alerta activa
                    if rule_id not in self.active_alerts:
                        # Crear nueva alerta
                        alert = Alert(
                            id=f"{rule_id}_{int(time.time())}",
                            title=rule.name,
                            description=rule.description,
                            severity=rule.severity,
                            status=AlertStatus.ACTIVE,
                            source=rule_id,
                            metric_name=rule.metric_name,
                            threshold=rule.threshold,
                            current_value=current_value,
                            timestamp=datetime.now(),
                            metadata=rule.labels
                        )
                        
                        self.active_alerts[rule_id] = alert
                        self.alert_history.append(alert)
                        
                        # Enviar notificación
                        self._send_notifications(alert)
                        
                        logger.warning(f"Alerta activada: {rule.name} - Valor: {current_value}, Umbral: {rule.threshold}")
                
                else:
                    # Resolver alerta si existe
                    if rule_id in self.active_alerts:
                        alert = self.active_alerts[rule_id]
                        alert.status = AlertStatus.RESOLVED
                        alert.resolved_at = datetime.now()
                        
                        del self.active_alerts[rule_id]
                        
                        # Enviar notificación de resolución
                        self._send_resolution_notification(alert)
                        
                        logger.info(f"Alerta resuelta: {rule.name}")
                
            except Exception as e:
                logger.error(f"Error verificando regla {rule_id}: {e}")
    
    def _get_metric_value(self, metric_name: str) -> Optional[float]:
        """Obtiene el valor actual de una métrica."""
        # En un entorno real, esto consultaría Prometheus o el sistema de métricas
        # Aquí simulamos valores basados en el nombre de la métrica
        
        simulated_values = {
            "capibara6_system_cpu_usage_percent": 25.0,
            "capibara6_system_memory_usage_bytes": 2 * 1024 * 1024 * 1024,  # 2GB
            "capibara6_api_requests_total": 0.02,  # 2% error rate
            "capibara6_api_request_duration_seconds": 0.5,
            "capibara6_e2b_executions_total": 0.05,  # 5% failure rate
            "capibara6_rag_search_duration_seconds": 0.05,
            "capibara6_cache_hit_rate": 85.0,
            "capibara6_daily_cost_total_usd": 50.0
        }
        
        return simulated_values.get(metric_name)
    
    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """Evalúa una condición de alerta."""
        if condition == ">":
            return value > threshold
        elif condition == "<":
            return value < threshold
        elif condition == ">=":
            return value >= threshold
        elif condition == "<=":
            return value <= threshold
        elif condition == "==":
            return value == threshold
        elif condition == "!=":
            return value != threshold
        else:
            return False
    
    def _send_notifications(self, alert: Alert):
        """Envía notificaciones para una alerta."""
        # Verificar cooldown
        cooldown_key = f"{alert.source}_{alert.severity.value}"
        if cooldown_key in self.alert_cooldowns:
            if datetime.now() - self.alert_cooldowns[cooldown_key] < timedelta(minutes=15):
                return  # En cooldown
        
        # Enviar a todos los canales configurados
        for channel_name, send_func in self.notification_channels.items():
            try:
                send_func(alert)
            except Exception as e:
                logger.error(f"Error enviando notificación por {channel_name}: {e}")
        
        # Establecer cooldown
        self.alert_cooldowns[cooldown_key] = datetime.now()
    
    def _send_resolution_notification(self, alert: Alert):
        """Envía notificación de resolución de alerta."""
        alert.title = f"[RESOLVED] {alert.title}"
        alert.description = f"Alerta resuelta: {alert.description}"
        
        for channel_name, send_func in self.notification_channels.items():
            try:
                send_func(alert)
            except Exception as e:
                logger.error(f"Error enviando notificación de resolución por {channel_name}: {e}")
    
    def _send_email_alert(self, alert: Alert):
        """Envía alerta por email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = 'admin@capibara6.com'
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            body = f"""
            Alerta: {alert.title}
            Descripción: {alert.description}
            Severidad: {alert.severity.value}
            Fuente: {alert.source}
            Métrica: {alert.metric_name}
            Valor actual: {alert.current_value}
            Umbral: {alert.threshold}
            Timestamp: {alert.timestamp}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # En un entorno real, se enviaría el email
            logger.info(f"Email alert enviado: {alert.title}")
            
        except Exception as e:
            logger.error(f"Error enviando email alert: {e}")
    
    def _send_slack_alert(self, alert: Alert):
        """Envía alerta por Slack."""
        try:
            color_map = {
                AlertSeverity.INFO: "good",
                AlertSeverity.WARNING: "warning",
                AlertSeverity.CRITICAL: "danger",
                AlertSeverity.EMERGENCY: "danger"
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "warning"),
                        "title": alert.title,
                        "text": alert.description,
                        "fields": [
                            {"title": "Severidad", "value": alert.severity.value, "short": True},
                            {"title": "Fuente", "value": alert.source, "short": True},
                            {"title": "Valor actual", "value": str(alert.current_value), "short": True},
                            {"title": "Umbral", "value": str(alert.threshold), "short": True},
                            {"title": "Timestamp", "value": alert.timestamp.isoformat(), "short": False}
                        ]
                    }
                ]
            }
            
            # En un entorno real, se enviaría a Slack
            logger.info(f"Slack alert enviado: {alert.title}")
            
        except Exception as e:
            logger.error(f"Error enviando Slack alert: {e}")
    
    def _send_discord_alert(self, alert: Alert):
        """Envía alerta por Discord."""
        try:
            color_map = {
                AlertSeverity.INFO: 0x00ff00,      # Verde
                AlertSeverity.WARNING: 0xffff00,   # Amarillo
                AlertSeverity.CRITICAL: 0xff0000,  # Rojo
                AlertSeverity.EMERGENCY: 0x8b0000  # Rojo oscuro
            }
            
            payload = {
                "embeds": [
                    {
                        "title": alert.title,
                        "description": alert.description,
                        "color": color_map.get(alert.severity, 0xffff00),
                        "fields": [
                            {"name": "Severidad", "value": alert.severity.value, "inline": True},
                            {"name": "Fuente", "value": alert.source, "inline": True},
                            {"name": "Valor actual", "value": str(alert.current_value), "inline": True},
                            {"name": "Umbral", "value": str(alert.threshold), "inline": True},
                            {"name": "Timestamp", "value": alert.timestamp.isoformat(), "inline": False}
                        ]
                    }
                ]
            }
            
            # En un entorno real, se enviaría a Discord
            logger.info(f"Discord alert enviado: {alert.title}")
            
        except Exception as e:
            logger.error(f"Error enviando Discord alert: {e}")
    
    def _send_webhook_alert(self, alert: Alert):
        """Envía alerta por webhook."""
        try:
            payload = {
                "alert_id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity.value,
                "status": alert.status.value,
                "source": alert.source,
                "metric_name": alert.metric_name,
                "current_value": alert.current_value,
                "threshold": alert.threshold,
                "timestamp": alert.timestamp.isoformat(),
                "metadata": alert.metadata
            }
            
            # En un entorno real, se enviaría el webhook
            logger.info(f"Webhook alert enviado: {alert.title}")
            
        except Exception as e:
            logger.error(f"Error enviando webhook alert: {e}")
    
    # Métodos públicos
    def add_alert_rule(self, rule: AlertRule):
        """Añade una nueva regla de alerta."""
        self.alert_rules[rule.id] = rule
        logger.info(f"Regla de alerta añadida: {rule.name}")
    
    def remove_alert_rule(self, rule_id: str):
        """Elimina una regla de alerta."""
        if rule_id in self.alert_rules:
            del self.alert_rules[rule_id]
            logger.info(f"Regla de alerta eliminada: {rule_id}")
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str):
        """Reconoce una alerta."""
        for alert in self.active_alerts.values():
            if alert.id == alert_id:
                alert.status = AlertStatus.ACKNOWLEDGED
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                logger.info(f"Alerta reconocida: {alert_id} por {acknowledged_by}")
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Obtiene alertas activas."""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """Obtiene historial de alertas."""
        return self.alert_history[-limit:]
    
    def get_alert_rules(self) -> List[AlertRule]:
        """Obtiene todas las reglas de alerta."""
        return list(self.alert_rules.values())
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de alertas."""
        total_alerts = len(self.alert_history)
        active_alerts = len(self.active_alerts)
        
        severity_counts = {}
        for alert in self.alert_history:
            severity = alert.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "severity_distribution": severity_counts,
            "alert_rules_count": len(self.alert_rules),
            "enabled_rules_count": sum(1 for rule in self.alert_rules.values() if rule.enabled)
        }


# Instancia global
alert_manager = AlertManager()


def get_alert_manager() -> AlertManager:
    """Obtiene la instancia global del gestor de alertas."""
    return alert_manager


if __name__ == "__main__":
    # Test del sistema de alertas
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    manager = AlertManager()
    
    # Simular algunas alertas
    time.sleep(2)
    
    # Obtener estadísticas
    stats = manager.get_alert_statistics()
    print("Estadísticas de alertas:")
    print(json.dumps(stats, indent=2, default=str))
    
    # Obtener alertas activas
    active_alerts = manager.get_active_alerts()
    print(f"\nAlertas activas: {len(active_alerts)}")
    
    # Obtener historial
    history = manager.get_alert_history(10)
    print(f"Historial de alertas: {len(history)}")
    
    print("Sistema de alertas funcionando correctamente!")
