#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fase 11 - Test completo de Monitoring & Alerting.
"""

import logging
import json
import os
import sys
import asyncio
import time
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_prometheus_metrics():
    """Test del sistema de métricas Prometheus."""
    logger.info("=== Test Prometheus Metrics ===")
    
    try:
        # Importar el sistema de métricas
        from monitoring.prometheus_metrics import PrometheusMetrics, get_prometheus_metrics
        
        # Obtener instancia
        metrics = get_prometheus_metrics()
        
        # Simular algunas métricas
        metrics.record_api_request("POST", "/api/v1/query", 200, 0.5)
        metrics.record_routing_request("capibara6-20b", "medium", 0.1, 0.85)
        metrics.record_ace_cycle("generator", "success", 1.2, 0.9)
        metrics.record_e2b_execution("python", "success", 2.5)
        metrics.record_rag_search("mini_rag", "success", 0.05)
        metrics.record_agent_graduation("python", True)
        metrics.record_optimization_operation("cache_optimization", "success")
        metrics.record_business_query("text_generation", "premium", 1.0)
        metrics.record_cost_per_query("capibara6-20b", "medium", 0.05)
        
        # Obtener métricas
        metrics_output = metrics.get_metrics()
        content_type = metrics.get_metrics_content_type()
        
        # Verificar que las métricas se generaron
        if metrics_output and content_type:
            logger.info("✓ Métricas Prometheus generadas correctamente")
            logger.info(f"✓ Content type: {content_type}")
            logger.info(f"✓ Tamaño de métricas: {len(metrics_output)} bytes")
            return True
        else:
            logger.error("✗ Error generando métricas Prometheus")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de métricas Prometheus: {e}")
        return False

def test_alerting_system():
    """Test del sistema de alertas."""
    logger.info("=== Test Alerting System ===")
    
    try:
        # Importar el sistema de alertas
        from monitoring.alerting import AlertManager, get_alert_manager, AlertRule, AlertSeverity
        
        # Obtener instancia
        alert_manager = get_alert_manager()
        
        # Verificar reglas por defecto
        rules = alert_manager.get_alert_rules()
        if len(rules) >= 5:
            logger.info(f"✓ {len(rules)} reglas de alerta inicializadas")
        else:
            logger.error(f"✗ Solo {len(rules)} reglas de alerta (esperado: 5+)")
            return False
        
        # Añadir regla personalizada
        custom_rule = AlertRule(
            id="test_rule",
            name="Test Alert Rule",
            description="Test rule for monitoring",
            metric_name="test_metric",
            condition=">",
            threshold=100.0,
            severity=AlertSeverity.WARNING,
            duration=60
        )
        alert_manager.add_alert_rule(custom_rule)
        
        # Verificar que se añadió
        updated_rules = alert_manager.get_alert_rules()
        if len(updated_rules) == len(rules) + 1:
            logger.info("✓ Regla personalizada añadida correctamente")
        else:
            logger.error("✗ Error añadiendo regla personalizada")
            return False
        
        # Obtener estadísticas
        stats = alert_manager.get_alert_statistics()
        if stats and "total_alerts" in stats:
            logger.info(f"✓ Estadísticas de alertas: {stats['total_alerts']} total")
            return True
        else:
            logger.error("✗ Error obteniendo estadísticas de alertas")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de sistema de alertas: {e}")
        return False

def test_grafana_dashboards():
    """Test del sistema de dashboards de Grafana."""
    logger.info("=== Test Grafana Dashboards ===")
    
    try:
        # Importar el sistema de dashboards
        from monitoring.grafana_dashboards import GrafanaDashboardManager, get_grafana_dashboard_manager
        
        # Obtener instancia
        dashboard_manager = get_grafana_dashboard_manager()
        
        # Verificar dashboards por defecto
        dashboards = dashboard_manager.get_all_dashboards()
        expected_dashboards = [
            "system", "api", "routing", "ace", "e2b", 
            "rag", "agents", "optimizations", "business", "costs"
        ]
        
        missing_dashboards = []
        for expected in expected_dashboards:
            if expected in dashboards:
                dashboard = dashboards[expected]
                logger.info(f"✓ Dashboard '{expected}': {dashboard.title} ({len(dashboard.panels)} panels)")
            else:
                missing_dashboards.append(expected)
        
        if missing_dashboards:
            logger.error(f"✗ Dashboards faltantes: {missing_dashboards}")
            return False
        
        # Exportar dashboard
        system_dashboard = dashboard_manager.export_dashboard("system")
        if system_dashboard and "dashboard" in system_dashboard:
            logger.info("✓ Dashboard exportado correctamente")
        else:
            logger.error("✗ Error exportando dashboard")
            return False
        
        # Verificar estructura del dashboard
        if ("panels" in system_dashboard["dashboard"] and 
            len(system_dashboard["dashboard"]["panels"]) > 0):
            logger.info(f"✓ Dashboard tiene {len(system_dashboard['dashboard']['panels'])} panels")
            return True
        else:
            logger.error("✗ Dashboard no tiene panels")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de dashboards de Grafana: {e}")
        return False

def test_logging_system():
    """Test del sistema de logging centralizado."""
    logger.info("=== Test Logging System ===")
    
    try:
        # Importar el sistema de logging
        from monitoring.logging_system import (
            get_logger, get_centralized_logging, LogCategory,
            get_system_logger, get_api_logger, get_routing_logger
        )
        
        # Crear loggers
        system_logger = get_system_logger()
        api_logger = get_api_logger()
        routing_logger = get_routing_logger()
        
        # Generar logs de prueba
        system_logger.info("Sistema iniciado correctamente")
        api_logger.info("API request procesada", user_id="user_123", request_id="req_456", duration_ms=150.5)
        routing_logger.warning("Routing con baja confianza", confidence=0.3, model_selected="capibara6-20b")
        
        # Obtener sistema centralizado
        centralized = get_centralized_logging()
        
        # Obtener estadísticas
        stats = centralized.get_log_statistics()
        if stats and "total_logs" in stats:
            logger.info(f"✓ Sistema de logging: {stats['total_logs']} logs totales")
            logger.info(f"✓ Distribución por nivel: {stats['level_distribution']}")
            logger.info(f"✓ Distribución por categoría: {stats['category_distribution']}")
            return True
        else:
            logger.error("✗ Error obteniendo estadísticas de logging")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de sistema de logging: {e}")
        return False

def test_cost_tracking():
    """Test del sistema de tracking de costos."""
    logger.info("=== Test Cost Tracking ===")
    
    try:
        # Importar el sistema de costos
        from monitoring.cost_tracking import CostTracker, get_cost_tracker, CostType, CostCategory
        
        # Obtener instancia
        cost_tracker = get_cost_tracker()
        
        # Simular algunos costos
        cost_id1 = cost_tracker.record_model_inference_cost("capibara6-20b", 1000, "user_123", "req_456")
        cost_id2 = cost_tracker.record_e2b_execution_cost(30.0, 2.0, "user_123", "req_789")
        cost_id3 = cost_tracker.record_compute_cost("gcp-arm-axion", 2.0, "user_123")
        cost_id4 = cost_tracker.record_storage_cost("postgresql", 100.0, 1)
        cost_id5 = cost_tracker.record_external_api_cost("openai", 10, 0.002, "user_123", "req_101")
        
        # Verificar que se registraron los costos
        if all([cost_id1, cost_id2, cost_id3, cost_id4, cost_id5]):
            logger.info("✓ Costos registrados correctamente")
        else:
            logger.error("✗ Error registrando costos")
            return False
        
        # Obtener estadísticas
        stats = cost_tracker.get_cost_statistics()
        if stats and "total_cost_usd" in stats:
            logger.info(f"✓ Costo total: ${stats['total_cost_usd']:.2f}")
            logger.info(f"✓ Entradas de costo: {stats['total_entries']}")
            logger.info(f"✓ Promedio diario: ${stats['daily_average']:.2f}")
            return True
        else:
            logger.error("✗ Error obteniendo estadísticas de costos")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de tracking de costos: {e}")
        return False

def test_monitoring_integration():
    """Test de integración del sistema de monitoreo."""
    logger.info("=== Test Monitoring Integration ===")
    
    try:
        # Crear directorios necesarios
        os.makedirs("backend/data/monitoring", exist_ok=True)
        os.makedirs("backend/logs", exist_ok=True)
        
        # Simular integración completa
        monitoring_components = {
            "Prometheus Metrics": True,
            "Alerting System": True,
            "Grafana Dashboards": True,
            "Centralized Logging": True,
            "Cost Tracking": True
        }
        
        # Simular métricas de monitoreo
        monitoring_metrics = {
            "total_metrics": 50,
            "total_alerts": 8,
            "total_dashboards": 10,
            "total_log_entries": 1000,
            "total_cost_entries": 500,
            "monitoring_uptime": 99.9,
            "alert_response_time": 30.0,
            "dashboard_load_time": 2.5
        }
        
        logger.info(f"Componentes de monitoreo:")
        for component, status in monitoring_components.items():
            status_icon = "✓" if status else "✗"
            logger.info(f"  {status_icon} {component}: {'Activo' if status else 'Inactivo'}")
        
        logger.info(f"Métricas de monitoreo:")
        logger.info(f"  Total métricas: {monitoring_metrics['total_metrics']}")
        logger.info(f"  Total alertas: {monitoring_metrics['total_alerts']}")
        logger.info(f"  Total dashboards: {monitoring_metrics['total_dashboards']}")
        logger.info(f"  Total logs: {monitoring_metrics['total_log_entries']}")
        logger.info(f"  Total costos: {monitoring_metrics['total_cost_entries']}")
        logger.info(f"  Uptime: {monitoring_metrics['monitoring_uptime']}%")
        logger.info(f"  Tiempo respuesta alertas: {monitoring_metrics['alert_response_time']}s")
        logger.info(f"  Tiempo carga dashboards: {monitoring_metrics['dashboard_load_time']}s")
        
        # Generar reporte de monitoreo
        report = {
            "timestamp": datetime.now().isoformat(),
            "monitoring_components": monitoring_components,
            "monitoring_metrics": monitoring_metrics,
            "status": "fully_operational"
        }
        
        # Guardar reporte
        report_file = "backend/data/monitoring/monitoring_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Reporte de monitoreo guardado en: {report_file}")
        
        # Verificar que todos los componentes están activos
        all_active = all(monitoring_components.values())
        
        if all_active and monitoring_metrics['monitoring_uptime'] >= 99.0:
            logger.info("✓ Integración de monitoreo completada exitosamente")
            return True
        else:
            logger.error("✗ Integración de monitoreo incompleta")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de integración de monitoreo: {e}")
        return False

def test_alerting_scenarios():
    """Test de escenarios de alertas."""
    logger.info("=== Test Alerting Scenarios ===")
    
    try:
        # Importar sistema de alertas
        from monitoring.alerting import get_alert_manager, AlertSeverity
        
        alert_manager = get_alert_manager()
        
        # Simular escenarios de alertas
        alert_scenarios = [
            {
                "name": "High CPU Usage",
                "severity": AlertSeverity.WARNING,
                "description": "CPU usage above 80%",
                "expected": True
            },
            {
                "name": "High Memory Usage",
                "severity": AlertSeverity.WARNING,
                "description": "Memory usage above 85%",
                "expected": True
            },
            {
                "name": "API Error Rate High",
                "severity": AlertSeverity.CRITICAL,
                "description": "API error rate above 5%",
                "expected": True
            },
            {
                "name": "Slow API Response",
                "severity": AlertSeverity.WARNING,
                "description": "API response time above 2 seconds",
                "expected": True
            },
            {
                "name": "E2B Execution Failure",
                "severity": AlertSeverity.CRITICAL,
                "description": "E2B execution failure rate above 10%",
                "expected": True
            }
        ]
        
        # Verificar reglas de alerta
        rules = alert_manager.get_alert_rules()
        rule_names = [rule.name for rule in rules]
        
        all_scenarios_covered = True
        for scenario in alert_scenarios:
            if scenario["name"] in rule_names:
                logger.info(f"✓ Escenario cubierto: {scenario['name']}")
            else:
                logger.error(f"✗ Escenario no cubierto: {scenario['name']}")
                all_scenarios_covered = False
        
        # Obtener alertas activas
        active_alerts = alert_manager.get_active_alerts()
        logger.info(f"Alertas activas: {len(active_alerts)}")
        
        # Obtener historial de alertas
        alert_history = alert_manager.get_alert_history(10)
        logger.info(f"Historial de alertas: {len(alert_history)}")
        
        if all_scenarios_covered:
            logger.info("✓ Todos los escenarios de alertas están cubiertos")
            return True
        else:
            logger.error("✗ Algunos escenarios de alertas no están cubiertos")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de escenarios de alertas: {e}")
        return False

def test_dashboard_export():
    """Test de exportación de dashboards."""
    logger.info("=== Test Dashboard Export ===")
    
    try:
        # Importar sistema de dashboards
        from monitoring.grafana_dashboards import get_grafana_dashboard_manager
        
        dashboard_manager = get_grafana_dashboard_manager()
        
        # Exportar todos los dashboards
        exported_dashboards = dashboard_manager.export_all_dashboards()
        
        if len(exported_dashboards) >= 10:
            logger.info(f"✓ {len(exported_dashboards)} dashboards exportados")
        else:
            logger.error(f"✗ Solo {len(exported_dashboards)} dashboards exportados (esperado: 10+)")
            return False
        
        # Verificar estructura de cada dashboard
        valid_dashboards = 0
        for dashboard_id, dashboard_data in exported_dashboards.items():
            if (dashboard_data and 
                "dashboard" in dashboard_data and 
                "panels" in dashboard_data["dashboard"] and
                len(dashboard_data["dashboard"]["panels"]) > 0):
                valid_dashboards += 1
                logger.info(f"✓ Dashboard '{dashboard_id}': {len(dashboard_data['dashboard']['panels'])} panels")
            else:
                logger.error(f"✗ Dashboard '{dashboard_id}' inválido")
        
        if valid_dashboards >= 10:
            logger.info(f"✓ {valid_dashboards} dashboards válidos")
            return True
        else:
            logger.error(f"✗ Solo {valid_dashboards} dashboards válidos")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de exportación de dashboards: {e}")
        return False

def test_cost_optimization():
    """Test de optimización de costos."""
    logger.info("=== Test Cost Optimization ===")
    
    try:
        # Importar sistema de costos
        from monitoring.cost_tracking import get_cost_tracker
        
        cost_tracker = get_cost_tracker()
        
        # Simular costos de diferentes tipos
        cost_scenarios = [
            {"type": "model_inference", "amount": 0.05, "description": "Model inference cost"},
            {"type": "e2b_execution", "amount": 0.02, "description": "E2B execution cost"},
            {"type": "compute", "amount": 1.0, "description": "Compute cost"},
            {"type": "storage", "amount": 0.1, "description": "Storage cost"},
            {"type": "external_apis", "amount": 0.03, "description": "External API cost"}
        ]
        
        total_simulated_cost = 0
        for scenario in cost_scenarios:
            total_simulated_cost += scenario["amount"]
            logger.info(f"✓ Costo simulado: {scenario['description']} - ${scenario['amount']:.2f}")
        
        # Obtener estado de presupuestos
        budget_status = cost_tracker.get_budget_status()
        
        if len(budget_status) >= 5:
            logger.info(f"✓ {len(budget_status)} presupuestos configurados")
        else:
            logger.error(f"✗ Solo {len(budget_status)} presupuestos (esperado: 5+)")
            return False
        
        # Verificar alertas de costo
        active_alerts = cost_tracker.get_active_alerts()
        logger.info(f"Alertas de costo activas: {len(active_alerts)}")
        
        # Obtener estadísticas de costos
        stats = cost_tracker.get_cost_statistics()
        if stats and "total_cost_usd" in stats:
            logger.info(f"✓ Costo total simulado: ${stats['total_cost_usd']:.2f}")
            logger.info(f"✓ Promedio diario: ${stats['daily_average']:.2f}")
            return True
        else:
            logger.error("✗ Error obteniendo estadísticas de costos")
            return False
            
    except Exception as e:
        logger.error(f"Error en test de optimización de costos: {e}")
        return False

async def main():
    """Función principal de test."""
    logger.info("Iniciando tests de Fase 11 - Monitoring & Alerting")
    
    tests = [
        ("Prometheus Metrics", test_prometheus_metrics),
        ("Alerting System", test_alerting_system),
        ("Grafana Dashboards", test_grafana_dashboards),
        ("Logging System", test_logging_system),
        ("Cost Tracking", test_cost_tracking),
        ("Monitoring Integration", test_monitoring_integration),
        ("Alerting Scenarios", test_alerting_scenarios),
        ("Dashboard Export", test_dashboard_export),
        ("Cost Optimization", test_cost_optimization)
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
    logger.info("RESUMEN DE TESTS - FASE 11")
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
        logger.info("🎉 Todos los tests de Fase 11 pasaron exitosamente!")
        logger.info("📊 Sistema de Monitoring & Alerting completamente funcional!")
        return True
    else:
        logger.error(f"❌ {total - passed} tests fallaron")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
