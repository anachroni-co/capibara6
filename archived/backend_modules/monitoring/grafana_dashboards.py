#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grafana Dashboards - Sistema de dashboards para Grafana.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class DashboardPanel:
    """Panel de dashboard de Grafana."""
    id: int
    title: str
    type: str
    targets: List[Dict[str, Any]]
    gridPos: Dict[str, int]
    options: Optional[Dict[str, Any]] = None

@dataclass
class Dashboard:
    """Dashboard de Grafana."""
    id: Optional[int]
    title: str
    description: str
    panels: List[DashboardPanel]
    tags: List[str]
    timezone: str = "browser"
    refresh: str = "30s"
    time: Dict[str, str] = None

class GrafanaDashboardManager:
    """Gestor de dashboards de Grafana."""
    
    def __init__(self):
        self.dashboards: Dict[str, Dashboard] = {}
        self._initialize_default_dashboards()
        
        logger.info("GrafanaDashboardManager inicializado")
    
    def _initialize_default_dashboards(self):
        """Inicializa dashboards por defecto."""
        
        # Dashboard de Sistema
        system_dashboard = self._create_system_dashboard()
        self.dashboards["system"] = system_dashboard
        
        # Dashboard de API
        api_dashboard = self._create_api_dashboard()
        self.dashboards["api"] = api_dashboard
        
        # Dashboard de Routing
        routing_dashboard = self._create_routing_dashboard()
        self.dashboards["routing"] = routing_dashboard
        
        # Dashboard de ACE
        ace_dashboard = self._create_ace_dashboard()
        self.dashboards["ace"] = ace_dashboard
        
        # Dashboard de E2B
        e2b_dashboard = self._create_e2b_dashboard()
        self.dashboards["e2b"] = e2b_dashboard
        
        # Dashboard de RAG
        rag_dashboard = self._create_rag_dashboard()
        self.dashboards["rag"] = rag_dashboard
        
        # Dashboard de Agentes
        agents_dashboard = self._create_agents_dashboard()
        self.dashboards["agents"] = agents_dashboard
        
        # Dashboard de Optimizaciones
        optimizations_dashboard = self._create_optimizations_dashboard()
        self.dashboards["optimizations"] = optimizations_dashboard
        
        # Dashboard de Negocio
        business_dashboard = self._create_business_dashboard()
        self.dashboards["business"] = business_dashboard
        
        # Dashboard de Costos
        costs_dashboard = self._create_costs_dashboard()
        self.dashboards["costs"] = costs_dashboard
        
        logger.info(f"Inicializados {len(self.dashboards)} dashboards por defecto")
    
    def _create_system_dashboard(self) -> Dashboard:
        """Crea dashboard del sistema."""
        panels = [
            DashboardPanel(
                id=1,
                title="CPU Usage",
                type="stat",
                targets=[{
                    "expr": "capibara6_system_cpu_usage_percent",
                    "legendFormat": "CPU Usage %"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0},
                options={"colorMode": "value", "graphMode": "area"}
            ),
            DashboardPanel(
                id=2,
                title="Memory Usage",
                type="stat",
                targets=[{
                    "expr": "capibara6_system_memory_usage_bytes",
                    "legendFormat": "Memory Usage"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0},
                options={"colorMode": "value", "graphMode": "area"}
            ),
            DashboardPanel(
                id=3,
                title="Disk Usage",
                type="stat",
                targets=[{
                    "expr": "capibara6_system_disk_usage_bytes",
                    "legendFormat": "Disk Usage"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0},
                options={"colorMode": "value", "graphMode": "area"}
            ),
            DashboardPanel(
                id=4,
                title="System Metrics Over Time",
                type="timeseries",
                targets=[
                    {
                        "expr": "capibara6_system_cpu_usage_percent",
                        "legendFormat": "CPU %"
                    },
                    {
                        "expr": "capibara6_system_memory_usage_bytes / 1024 / 1024 / 1024",
                        "legendFormat": "Memory GB"
                    }
                ],
                gridPos={"h": 8, "w": 18, "x": 0, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="System Overview",
            description="Métricas del sistema Capibara6",
            panels=panels,
            tags=["system", "infrastructure"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_api_dashboard(self) -> Dashboard:
        """Crea dashboard de API."""
        panels = [
            DashboardPanel(
                id=1,
                title="API Requests Total",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_api_requests_total[5m]))",
                    "legendFormat": "Requests/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="API Response Time",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_api_request_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="API Error Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_api_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(capibara6_api_requests_total[5m])) * 100",
                    "legendFormat": "Error Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Active Connections",
                type="stat",
                targets=[{
                    "expr": "capibara6_api_active_connections",
                    "legendFormat": "Active Connections"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="API Requests by Endpoint",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_api_requests_total[5m])) by (endpoint)",
                    "legendFormat": "{{endpoint}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="API Response Time Distribution",
                type="timeseries",
                targets=[
                    {
                        "expr": "histogram_quantile(0.50, rate(capibara6_api_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "50th percentile"
                    },
                    {
                        "expr": "histogram_quantile(0.95, rate(capibara6_api_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "95th percentile"
                    },
                    {
                        "expr": "histogram_quantile(0.99, rate(capibara6_api_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "99th percentile"
                    }
                ],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="API Performance",
            description="Métricas de rendimiento de la API",
            panels=panels,
            tags=["api", "performance"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_routing_dashboard(self) -> Dashboard:
        """Crea dashboard de routing."""
        panels = [
            DashboardPanel(
                id=1,
                title="Routing Requests",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_routing_requests_total[5m]))",
                    "legendFormat": "Requests/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="Model Selection Distribution",
                type="piechart",
                targets=[{
                    "expr": "sum(rate(capibara6_routing_requests_total[5m])) by (model_selected)",
                    "legendFormat": "{{model_selected}}"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Routing Confidence",
                type="stat",
                targets=[{
                    "expr": "avg(capibara6_routing_confidence)",
                    "legendFormat": "Avg Confidence"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Routing Duration",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_routing_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="Routing Requests by Model",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_routing_requests_total[5m])) by (model_selected)",
                    "legendFormat": "{{model_selected}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Routing Confidence Over Time",
                type="timeseries",
                targets=[{
                    "expr": "avg(capibara6_routing_confidence) by (model_selected)",
                    "legendFormat": "{{model_selected}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="Intelligent Routing",
            description="Métricas del sistema de routing inteligente",
            panels=panels,
            tags=["routing", "intelligence"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_ace_dashboard(self) -> Dashboard:
        """Crea dashboard de ACE."""
        panels = [
            DashboardPanel(
                id=1,
                title="ACE Cycles",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_ace_cycles_total[5m]))",
                    "legendFormat": "Cycles/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="ACE Processing Duration",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_ace_processing_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="ACE Awareness Score",
                type="stat",
                targets=[{
                    "expr": "avg(capibara6_ace_awareness_score)",
                    "legendFormat": "Avg Awareness"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="ACE Success Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_ace_cycles_total{status=\"success\"}[5m])) / sum(rate(capibara6_ace_cycles_total[5m])) * 100",
                    "legendFormat": "Success Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="ACE Cycles by Component",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_ace_cycles_total[5m])) by (component)",
                    "legendFormat": "{{component}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="ACE Awareness Score by Component",
                type="timeseries",
                targets=[{
                    "expr": "avg(capibara6_ace_awareness_score) by (component)",
                    "legendFormat": "{{component}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="ACE Framework",
            description="Métricas del framework ACE (Adaptive Context Evolution)",
            panels=panels,
            tags=["ace", "context", "evolution"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_e2b_dashboard(self) -> Dashboard:
        """Crea dashboard de E2B."""
        panels = [
            DashboardPanel(
                id=1,
                title="E2B Executions",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_e2b_executions_total[5m]))",
                    "legendFormat": "Executions/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="E2B Success Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_e2b_executions_total{status=\"success\"}[5m])) / sum(rate(capibara6_e2b_executions_total[5m])) * 100",
                    "legendFormat": "Success Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="E2B Execution Duration",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_e2b_execution_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Active Sandboxes",
                type="stat",
                targets=[{
                    "expr": "sum(capibara6_e2b_sandbox_count)",
                    "legendFormat": "Active Sandboxes"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="E2B Executions by Language",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_e2b_executions_total[5m])) by (language)",
                    "legendFormat": "{{language}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="E2B Execution Duration by Language",
                type="timeseries",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_e2b_execution_duration_seconds_bucket[5m])) by (language)",
                    "legendFormat": "{{language}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="E2B Execution",
            description="Métricas del sistema E2B (Execution-to-Browser)",
            panels=panels,
            tags=["e2b", "execution", "sandbox"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_rag_dashboard(self) -> Dashboard:
        """Crea dashboard de RAG."""
        panels = [
            DashboardPanel(
                id=1,
                title="RAG Searches",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_rag_searches_total[5m]))",
                    "legendFormat": "Searches/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="RAG Search Duration",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_rag_search_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Vector Count",
                type="stat",
                targets=[{
                    "expr": "sum(capibara6_rag_vector_count)",
                    "legendFormat": "Total Vectors"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="RAG Success Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_rag_searches_total{status=\"success\"}[5m])) / sum(rate(capibara6_rag_searches_total[5m])) * 100",
                    "legendFormat": "Success Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="RAG Searches by Type",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_rag_searches_total[5m])) by (search_type)",
                    "legendFormat": "{{search_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Vector Count by Index Type",
                type="timeseries",
                targets=[{
                    "expr": "sum(capibara6_rag_vector_count) by (index_type)",
                    "legendFormat": "{{index_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="RAG System",
            description="Métricas del sistema RAG (Retrieval-Augmented Generation)",
            panels=panels,
            tags=["rag", "retrieval", "generation"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_agents_dashboard(self) -> Dashboard:
        """Crea dashboard de agentes."""
        panels = [
            DashboardPanel(
                id=1,
                title="Total Agents",
                type="stat",
                targets=[{
                    "expr": "sum(capibara6_agents_total)",
                    "legendFormat": "Total Agents"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="Agent Graduations",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_agent_graduations_total[5m]))",
                    "legendFormat": "Graduations/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Agent Memory Usage",
                type="stat",
                targets=[{
                    "expr": "sum(capibara6_agent_memory_usage_bytes) / 1024 / 1024 / 1024",
                    "legendFormat": "Memory GB"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Graduation Success Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_agent_graduations_total{success=\"true\"}[5m])) / sum(rate(capibara6_agent_graduations_total[5m])) * 100",
                    "legendFormat": "Success Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="Agents by Domain",
                type="piechart",
                targets=[{
                    "expr": "sum(capibara6_agents_total) by (domain)",
                    "legendFormat": "{{domain}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Agent Memory Usage by Type",
                type="timeseries",
                targets=[{
                    "expr": "sum(capibara6_agent_memory_usage_bytes) by (memory_type)",
                    "legendFormat": "{{memory_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="Persistent Agents",
            description="Métricas de los agentes persistentes",
            panels=panels,
            tags=["agents", "persistent", "memory"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_optimizations_dashboard(self) -> Dashboard:
        """Crea dashboard de optimizaciones."""
        panels = [
            DashboardPanel(
                id=1,
                title="Optimization Operations",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_optimization_operations_total[5m]))",
                    "legendFormat": "Operations/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="Cache Hit Rate",
                type="stat",
                targets=[{
                    "expr": "avg(capibara6_cache_hit_rate)",
                    "legendFormat": "Hit Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Batch Processing Duration",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_batch_processing_duration_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Optimization Success Rate",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_optimization_operations_total{status=\"success\"}[5m])) / sum(rate(capibara6_optimization_operations_total[5m])) * 100",
                    "legendFormat": "Success Rate %"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="Cache Hit Rate by Type",
                type="timeseries",
                targets=[{
                    "expr": "avg(capibara6_cache_hit_rate) by (cache_type)",
                    "legendFormat": "{{cache_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Optimization Operations by Type",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_optimization_operations_total[5m])) by (operation_type)",
                    "legendFormat": "{{operation_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="System Optimizations",
            description="Métricas de las optimizaciones del sistema",
            panels=panels,
            tags=["optimizations", "performance", "cache"],
            time={"from": "now-1h", "to": "now"}
        )
    
    def _create_business_dashboard(self) -> Dashboard:
        """Crea dashboard de negocio."""
        panels = [
            DashboardPanel(
                id=1,
                title="Business Queries",
                type="stat",
                targets=[{
                    "expr": "sum(rate(capibara6_business_queries_total[5m]))",
                    "legendFormat": "Queries/sec"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="Business Response Time",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_business_response_time_seconds_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Satisfaction Score",
                type="stat",
                targets=[{
                    "expr": "avg(capibara6_business_satisfaction_score)",
                    "legendFormat": "Satisfaction Score"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Queries by User Tier",
                type="piechart",
                targets=[{
                    "expr": "sum(rate(capibara6_business_queries_total[5m])) by (user_tier)",
                    "legendFormat": "{{user_tier}}"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="Business Queries by Type",
                type="timeseries",
                targets=[{
                    "expr": "sum(rate(capibara6_business_queries_total[5m])) by (query_type)",
                    "legendFormat": "{{query_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Satisfaction Score Over Time",
                type="timeseries",
                targets=[{
                    "expr": "avg(capibara6_business_satisfaction_score) by (metric_type)",
                    "legendFormat": "{{metric_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="Business Metrics",
            description="Métricas de negocio y satisfacción del usuario",
            panels=panels,
            tags=["business", "satisfaction", "kpi"],
            time={"from": "now-24h", "to": "now"}
        )
    
    def _create_costs_dashboard(self) -> Dashboard:
        """Crea dashboard de costos."""
        panels = [
            DashboardPanel(
                id=1,
                title="Daily Cost Total",
                type="stat",
                targets=[{
                    "expr": "sum(capibara6_daily_cost_total_usd)",
                    "legendFormat": "Daily Cost USD"
                }],
                gridPos={"h": 8, "w": 6, "x": 0, "y": 0}
            ),
            DashboardPanel(
                id=2,
                title="Cost per Query",
                type="stat",
                targets=[{
                    "expr": "histogram_quantile(0.95, rate(capibara6_cost_per_query_usd_bucket[5m]))",
                    "legendFormat": "95th percentile"
                }],
                gridPos={"h": 8, "w": 6, "x": 6, "y": 0}
            ),
            DashboardPanel(
                id=3,
                title="Cost by Model Type",
                type="piechart",
                targets=[{
                    "expr": "sum(rate(capibara6_cost_per_query_usd_sum[5m])) by (model_type)",
                    "legendFormat": "{{model_type}}"
                }],
                gridPos={"h": 8, "w": 6, "x": 12, "y": 0}
            ),
            DashboardPanel(
                id=4,
                title="Cost by Query Complexity",
                type="piechart",
                targets=[{
                    "expr": "sum(rate(capibara6_cost_per_query_usd_sum[5m])) by (query_complexity)",
                    "legendFormat": "{{query_complexity}}"
                }],
                gridPos={"h": 8, "w": 6, "x": 18, "y": 0}
            ),
            DashboardPanel(
                id=5,
                title="Daily Cost Over Time",
                type="timeseries",
                targets=[{
                    "expr": "sum(capibara6_daily_cost_total_usd) by (cost_type)",
                    "legendFormat": "{{cost_type}}"
                }],
                gridPos={"h": 8, "w": 12, "x": 0, "y": 8}
            ),
            DashboardPanel(
                id=6,
                title="Cost per Query Distribution",
                type="timeseries",
                targets=[
                    {
                        "expr": "histogram_quantile(0.50, rate(capibara6_cost_per_query_usd_bucket[5m]))",
                        "legendFormat": "50th percentile"
                    },
                    {
                        "expr": "histogram_quantile(0.95, rate(capibara6_cost_per_query_usd_bucket[5m]))",
                        "legendFormat": "95th percentile"
                    },
                    {
                        "expr": "histogram_quantile(0.99, rate(capibara6_cost_per_query_usd_bucket[5m]))",
                        "legendFormat": "99th percentile"
                    }
                ],
                gridPos={"h": 8, "w": 12, "x": 12, "y": 8}
            )
        ]
        
        return Dashboard(
            id=None,
            title="Cost Tracking",
            description="Métricas de costos y optimización de recursos",
            panels=panels,
            tags=["costs", "optimization", "resources"],
            time={"from": "now-7d", "to": "now"}
        )
    
    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        """Obtiene un dashboard por ID."""
        return self.dashboards.get(dashboard_id)
    
    def get_all_dashboards(self) -> Dict[str, Dashboard]:
        """Obtiene todos los dashboards."""
        return self.dashboards
    
    def export_dashboard(self, dashboard_id: str) -> Optional[Dict[str, Any]]:
        """Exporta un dashboard en formato JSON de Grafana."""
        dashboard = self.get_dashboard(dashboard_id)
        if not dashboard:
            return None
        
        # Convertir a formato de Grafana
        grafana_dashboard = {
            "dashboard": {
                "id": dashboard.id,
                "title": dashboard.title,
                "description": dashboard.description,
                "tags": dashboard.tags,
                "timezone": dashboard.timezone,
                "refresh": dashboard.refresh,
                "time": dashboard.time or {"from": "now-1h", "to": "now"},
                "panels": []
            },
            "overwrite": True
        }
        
        # Convertir panels
        for panel in dashboard.panels:
            grafana_panel = {
                "id": panel.id,
                "title": panel.title,
                "type": panel.type,
                "targets": panel.targets,
                "gridPos": panel.gridPos,
                "options": panel.options or {}
            }
            grafana_dashboard["dashboard"]["panels"].append(grafana_panel)
        
        return grafana_dashboard
    
    def export_all_dashboards(self) -> Dict[str, Dict[str, Any]]:
        """Exporta todos los dashboards."""
        exported = {}
        for dashboard_id in self.dashboards.keys():
            exported[dashboard_id] = self.export_dashboard(dashboard_id)
        return exported
    
    def save_dashboards_to_files(self, output_dir: str = "backend/deployment/grafana/dashboards"):
        """Guarda todos los dashboards en archivos JSON."""
        os.makedirs(output_dir, exist_ok=True)
        
        for dashboard_id, dashboard_data in self.export_all_dashboards().items():
            if dashboard_data:
                filename = f"{dashboard_id}_dashboard.json"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(dashboard_data, f, indent=2)
                
                logger.info(f"Dashboard guardado: {filepath}")


# Instancia global
grafana_dashboard_manager = GrafanaDashboardManager()


def get_grafana_dashboard_manager() -> GrafanaDashboardManager:
    """Obtiene la instancia global del gestor de dashboards."""
    return grafana_dashboard_manager


if __name__ == "__main__":
    # Test del sistema de dashboards
    import os
    
    logging.basicConfig(level=logging.INFO)
    
    manager = GrafanaDashboardManager()
    
    # Exportar todos los dashboards
    manager.save_dashboards_to_files()
    
    # Mostrar información de dashboards
    dashboards = manager.get_all_dashboards()
    print(f"Dashboards disponibles: {len(dashboards)}")
    
    for dashboard_id, dashboard in dashboards.items():
        print(f"- {dashboard_id}: {dashboard.title} ({len(dashboard.panels)} panels)")
    
    print("Sistema de dashboards de Grafana funcionando correctamente!")
