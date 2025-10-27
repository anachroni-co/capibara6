#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rewiring Experts - Sistema de rewiring dinámico de expertos para optimización de routing.
"""

import logging
import json
import os
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import heapq

logger = logging.getLogger(__name__)


class ExpertType(Enum):
    """Tipos de expertos."""
    PYTHON = "python"
    SQL = "sql"
    JAVASCRIPT = "javascript"
    DEBUG = "debug"
    ML = "ml"
    API = "api"
    GENERAL = "general"


class RewiringStrategy(Enum):
    """Estrategias de rewiring."""
    PERFORMANCE_BASED = "performance_based"
    LOAD_BALANCED = "load_balanced"
    ADAPTIVE = "adaptive"
    PREDICTIVE = "predictive"


@dataclass
class ExpertNode:
    """Nodo de experto en el grafo de rewiring."""
    expert_id: str
    expert_type: ExpertType
    capacity: int
    current_load: int
    performance_score: float
    latency_ms: float
    success_rate: float
    last_used: datetime
    connections: Set[str]  # IDs de expertos conectados
    metadata: Dict[str, Any]


@dataclass
class RoutingDecision:
    """Decisión de routing."""
    query_id: str
    primary_expert: str
    fallback_experts: List[str]
    confidence_score: float
    estimated_latency_ms: float
    reasoning: str
    timestamp: datetime


@dataclass
class RewiringEvent:
    """Evento de rewiring."""
    event_id: str
    event_type: str  # add_connection, remove_connection, update_weight
    from_expert: str
    to_expert: str
    weight: float
    reason: str
    timestamp: datetime
    impact_score: float


class ExpertGraph:
    """Grafo de expertos para rewiring dinámico."""
    
    def __init__(self):
        self.nodes: Dict[str, ExpertNode] = {}
        self.edges: Dict[Tuple[str, str], float] = {}  # (from, to) -> weight
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)
        
        # Métricas del grafo
        self.graph_metrics = {
            'total_nodes': 0,
            'total_edges': 0,
            'average_degree': 0.0,
            'clustering_coefficient': 0.0,
            'diameter': 0,
            'density': 0.0
        }
        
        logger.info("ExpertGraph inicializado")
    
    def add_expert(self, expert: ExpertNode):
        """Agrega experto al grafo."""
        self.nodes[expert.expert_id] = expert
        self.adjacency[expert.expert_id] = set()
        self._update_graph_metrics()
        
        logger.info(f"Experto agregado: {expert.expert_id} ({expert.expert_type.value})")
    
    def add_connection(self, from_expert: str, to_expert: str, weight: float = 1.0):
        """Agrega conexión entre expertos."""
        if from_expert in self.nodes and to_expert in self.nodes:
            self.edges[(from_expert, to_expert)] = weight
            self.adjacency[from_expert].add(to_expert)
            self._update_graph_metrics()
            
            logger.debug(f"Conexión agregada: {from_expert} -> {to_expert} (weight: {weight})")
    
    def remove_connection(self, from_expert: str, to_expert: str):
        """Remueve conexión entre expertos."""
        if (from_expert, to_expert) in self.edges:
            del self.edges[(from_expert, to_expert)]
            self.adjacency[from_expert].discard(to_expert)
            self._update_graph_metrics()
            
            logger.debug(f"Conexión removida: {from_expert} -> {to_expert}")
    
    def get_neighbors(self, expert_id: str) -> List[str]:
        """Obtiene vecinos de un experto."""
        return list(self.adjacency[expert_id])
    
    def get_connection_weight(self, from_expert: str, to_expert: str) -> float:
        """Obtiene peso de conexión."""
        return self.edges.get((from_expert, to_expert), 0.0)
    
    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """Encuentra el camino más corto entre dos expertos."""
        if start not in self.nodes or end not in self.nodes:
            return None
        
        # Dijkstra's algorithm
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current == end:
                # Reconstruir camino
                path = []
                while current is not None:
                    path.append(current)
                    current = previous.get(current)
                return path[::-1]
            
            if current_dist > distances[current]:
                continue
            
            for neighbor in self.adjacency[current]:
                weight = self.get_connection_weight(current, neighbor)
                new_dist = current_dist + (1.0 / weight) if weight > 0 else float('inf')
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return None
    
    def _update_graph_metrics(self):
        """Actualiza métricas del grafo."""
        self.graph_metrics['total_nodes'] = len(self.nodes)
        self.graph_metrics['total_edges'] = len(self.edges)
        
        if self.graph_metrics['total_nodes'] > 0:
            total_degree = sum(len(neighbors) for neighbors in self.adjacency.values())
            self.graph_metrics['average_degree'] = total_degree / self.graph_metrics['total_nodes']
            
            max_possible_edges = self.graph_metrics['total_nodes'] * (self.graph_metrics['total_nodes'] - 1)
            self.graph_metrics['density'] = self.graph_metrics['total_edges'] / max_possible_edges if max_possible_edges > 0 else 0.0


class RewiringExperts:
    """Sistema de rewiring dinámico de expertos."""
    
    def __init__(self, 
                 strategy: RewiringStrategy = RewiringStrategy.ADAPTIVE,
                 rewire_threshold: float = 0.1,
                 max_connections_per_expert: int = 5):
        self.strategy = strategy
        self.rewire_threshold = rewire_threshold
        self.max_connections_per_expert = max_connections_per_expert
        
        # Grafo de expertos
        self.expert_graph = ExpertGraph()
        
        # Historial de decisiones de routing
        self.routing_history: deque = deque(maxlen=10000)
        
        # Historial de eventos de rewiring
        self.rewiring_history: deque = deque(maxlen=1000)
        
        # Métricas de rendimiento
        self.performance_metrics = {
            'total_queries_routed': 0,
            'successful_routings': 0,
            'failed_routings': 0,
            'average_latency_ms': 0.0,
            'rewiring_events': 0,
            'performance_improvement': 0.0
        }
        
        # Configuración de expertos por defecto
        self._initialize_default_experts()
        
        logger.info(f"RewiringExperts inicializado: strategy={strategy.value}")
    
    def _initialize_default_experts(self):
        """Inicializa expertos por defecto."""
        default_experts = [
            ExpertNode(
                expert_id="python_expert_001",
                expert_type=ExpertType.PYTHON,
                capacity=100,
                current_load=0,
                performance_score=0.9,
                latency_ms=50.0,
                success_rate=0.95,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'data_science', 'version': '1.0'}
            ),
            ExpertNode(
                expert_id="sql_expert_001",
                expert_type=ExpertType.SQL,
                capacity=80,
                current_load=0,
                performance_score=0.88,
                latency_ms=30.0,
                success_rate=0.92,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'analytics', 'version': '1.0'}
            ),
            ExpertNode(
                expert_id="javascript_expert_001",
                expert_type=ExpertType.JAVASCRIPT,
                capacity=90,
                current_load=0,
                performance_score=0.85,
                latency_ms=60.0,
                success_rate=0.90,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'frontend', 'version': '1.0'}
            ),
            ExpertNode(
                expert_id="debug_expert_001",
                expert_type=ExpertType.DEBUG,
                capacity=70,
                current_load=0,
                performance_score=0.87,
                latency_ms=40.0,
                success_rate=0.88,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'error_analysis', 'version': '1.0'}
            ),
            ExpertNode(
                expert_id="ml_expert_001",
                expert_type=ExpertType.ML,
                capacity=60,
                current_load=0,
                performance_score=0.92,
                latency_ms=80.0,
                success_rate=0.94,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'deep_learning', 'version': '1.0'}
            ),
            ExpertNode(
                expert_id="api_expert_001",
                expert_type=ExpertType.API,
                capacity=85,
                current_load=0,
                performance_score=0.83,
                latency_ms=35.0,
                success_rate=0.89,
                last_used=datetime.now(),
                connections=set(),
                metadata={'specialization': 'rest_apis', 'version': '1.0'}
            )
        ]
        
        for expert in default_experts:
            self.expert_graph.add_expert(expert)
        
        # Crear conexiones iniciales basadas en compatibilidad
        self._create_initial_connections()
    
    def _create_initial_connections(self):
        """Crea conexiones iniciales entre expertos."""
        # Conexiones basadas en compatibilidad de dominios
        connections = [
            ("python_expert_001", "ml_expert_001", 0.9),
            ("python_expert_001", "debug_expert_001", 0.7),
            ("sql_expert_001", "python_expert_001", 0.8),
            ("sql_expert_001", "debug_expert_001", 0.6),
            ("javascript_expert_001", "api_expert_001", 0.8),
            ("javascript_expert_001", "debug_expert_001", 0.7),
            ("ml_expert_001", "python_expert_001", 0.9),
            ("api_expert_001", "debug_expert_001", 0.6),
            ("debug_expert_001", "python_expert_001", 0.7),
            ("debug_expert_001", "sql_expert_001", 0.6)
        ]
        
        for from_expert, to_expert, weight in connections:
            self.expert_graph.add_connection(from_expert, to_expert, weight)
    
    def route_query(self, 
                   query: str, 
                   query_features: Dict[str, Any],
                   query_id: Optional[str] = None) -> RoutingDecision:
        """Rutea query usando rewiring dinámico."""
        try:
            query_id = query_id or f"query_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Determinar experto primario
            primary_expert = self._select_primary_expert(query, query_features)
            
            # Determinar expertos de fallback
            fallback_experts = self._select_fallback_experts(primary_expert, query_features)
            
            # Calcular confianza y latencia estimada
            confidence_score = self._calculate_confidence(primary_expert, query_features)
            estimated_latency = self._estimate_latency(primary_expert, query_features)
            
            # Crear decisión de routing
            decision = RoutingDecision(
                query_id=query_id,
                primary_expert=primary_expert,
                fallback_experts=fallback_experts,
                confidence_score=confidence_score,
                estimated_latency_ms=estimated_latency,
                reasoning=self._generate_routing_reasoning(primary_expert, query_features),
                timestamp=datetime.now()
            )
            
            # Actualizar métricas
            self._update_routing_metrics(decision)
            
            # Agregar al historial
            self.routing_history.append(decision)
            
            # Evaluar necesidad de rewiring
            self._evaluate_rewiring_need()
            
            logger.info(f"Query {query_id} ruteada a {primary_expert} (confianza: {confidence_score:.2f})")
            return decision
            
        except Exception as e:
            logger.error(f"Error routing query {query_id}: {e}")
            # Fallback a experto general
            return self._create_fallback_decision(query_id)
    
    def _select_primary_expert(self, query: str, query_features: Dict[str, Any]) -> str:
        """Selecciona experto primario basado en estrategia."""
        if self.strategy == RewiringStrategy.PERFORMANCE_BASED:
            return self._select_by_performance(query_features)
        elif self.strategy == RewiringStrategy.LOAD_BALANCED:
            return self._select_by_load_balance(query_features)
        elif self.strategy == RewiringStrategy.ADAPTIVE:
            return self._select_adaptive(query_features)
        elif self.strategy == RewiringStrategy.PREDICTIVE:
            return self._select_predictive(query_features)
        else:
            return self._select_by_performance(query_features)
    
    def _select_by_performance(self, query_features: Dict[str, Any]) -> str:
        """Selecciona experto basado en rendimiento."""
        best_expert = None
        best_score = -1.0
        
        for expert_id, expert in self.expert_graph.nodes.items():
            # Calcular score combinado
            performance_score = expert.performance_score
            success_score = expert.success_rate
            latency_score = max(0, 1.0 - (expert.latency_ms / 1000.0))  # Normalizar latencia
            
            combined_score = (performance_score * 0.4 + 
                            success_score * 0.4 + 
                            latency_score * 0.2)
            
            if combined_score > best_score:
                best_score = combined_score
                best_expert = expert_id
        
        return best_expert or "python_expert_001"
    
    def _select_by_load_balance(self, query_features: Dict[str, Any]) -> str:
        """Selecciona experto basado en balance de carga."""
        best_expert = None
        best_load_ratio = float('inf')
        
        for expert_id, expert in self.expert_graph.nodes.items():
            load_ratio = expert.current_load / expert.capacity if expert.capacity > 0 else 1.0
            
            if load_ratio < best_load_ratio:
                best_load_ratio = load_ratio
                best_expert = expert_id
        
        return best_expert or "python_expert_001"
    
    def _select_adaptive(self, query_features: Dict[str, Any]) -> str:
        """Selecciona experto usando estrategia adaptativa."""
        # Combinar performance y load balancing
        performance_expert = self._select_by_performance(query_features)
        load_expert = self._select_by_load_balance(query_features)
        
        # Si son el mismo, usarlo
        if performance_expert == load_expert:
            return performance_expert
        
        # Si son diferentes, elegir basado en historial reciente
        recent_performance = self._get_recent_performance(performance_expert)
        recent_load = self._get_recent_load(load_expert)
        
        if recent_performance > recent_load:
            return performance_expert
        else:
            return load_expert
    
    def _select_predictive(self, query_features: Dict[str, Any]) -> str:
        """Selecciona experto usando predicción."""
        # Implementación simplificada - en producción usaría ML
        predicted_domain = query_features.get('predicted_domain', 'python')
        
        # Buscar experto del dominio predicho
        for expert_id, expert in self.expert_graph.nodes.items():
            if expert.expert_type.value == predicted_domain:
                return expert_id
        
        # Fallback a performance
        return self._select_by_performance(query_features)
    
    def _select_fallback_experts(self, primary_expert: str, query_features: Dict[str, Any]) -> List[str]:
        """Selecciona expertos de fallback."""
        fallback_experts = []
        
        # Obtener vecinos del experto primario
        neighbors = self.expert_graph.get_neighbors(primary_expert)
        
        # Ordenar por peso de conexión
        neighbor_weights = []
        for neighbor in neighbors:
            weight = self.expert_graph.get_connection_weight(primary_expert, neighbor)
            neighbor_weights.append((neighbor, weight))
        
        neighbor_weights.sort(key=lambda x: x[1], reverse=True)
        
        # Seleccionar top 3 como fallback
        for expert_id, weight in neighbor_weights[:3]:
            if weight > 0.5:  # Solo expertos con buena conexión
                fallback_experts.append(expert_id)
        
        return fallback_experts
    
    def _calculate_confidence(self, expert_id: str, query_features: Dict[str, Any]) -> float:
        """Calcula confianza en la decisión de routing."""
        if expert_id not in self.expert_graph.nodes:
            return 0.0
        
        expert = self.expert_graph.nodes[expert_id]
        
        # Factores de confianza
        performance_factor = expert.performance_score
        success_factor = expert.success_rate
        load_factor = 1.0 - (expert.current_load / expert.capacity) if expert.capacity > 0 else 0.0
        
        # Confianza combinada
        confidence = (performance_factor * 0.4 + 
                     success_factor * 0.4 + 
                     load_factor * 0.2)
        
        return min(1.0, max(0.0, confidence))
    
    def _estimate_latency(self, expert_id: str, query_features: Dict[str, Any]) -> float:
        """Estima latencia para el routing."""
        if expert_id not in self.expert_graph.nodes:
            return 1000.0  # Latencia alta por defecto
        
        expert = self.expert_graph.nodes[expert_id]
        base_latency = expert.latency_ms
        
        # Ajustar por carga actual
        load_factor = expert.current_load / expert.capacity if expert.capacity > 0 else 0.0
        adjusted_latency = base_latency * (1.0 + load_factor * 0.5)
        
        return adjusted_latency
    
    def _generate_routing_reasoning(self, expert_id: str, query_features: Dict[str, Any]) -> str:
        """Genera explicación del routing."""
        if expert_id not in self.expert_graph.nodes:
            return "Fallback routing due to expert not found"
        
        expert = self.expert_graph.nodes[expert_id]
        
        reasoning_parts = [
            f"Selected {expert_id} ({expert.expert_type.value})",
            f"Performance score: {expert.performance_score:.2f}",
            f"Success rate: {expert.success_rate:.2f}",
            f"Current load: {expert.current_load}/{expert.capacity}",
            f"Strategy: {self.strategy.value}"
        ]
        
        return " | ".join(reasoning_parts)
    
    def _create_fallback_decision(self, query_id: str) -> RoutingDecision:
        """Crea decisión de fallback."""
        return RoutingDecision(
            query_id=query_id,
            primary_expert="python_expert_001",
            fallback_experts=["debug_expert_001", "general_expert_001"],
            confidence_score=0.5,
            estimated_latency_ms=100.0,
            reasoning="Fallback routing due to error",
            timestamp=datetime.now()
        )
    
    def _update_routing_metrics(self, decision: RoutingDecision):
        """Actualiza métricas de routing."""
        self.performance_metrics['total_queries_routed'] += 1
        
        # Actualizar carga del experto primario
        if decision.primary_expert in self.expert_graph.nodes:
            expert = self.expert_graph.nodes[decision.primary_expert]
            expert.current_load = min(expert.capacity, expert.current_load + 1)
            expert.last_used = datetime.now()
    
    def _evaluate_rewiring_need(self):
        """Evalúa si se necesita rewiring."""
        if len(self.routing_history) < 100:  # Necesitamos suficiente historial
            return
        
        # Analizar rendimiento reciente
        recent_decisions = list(self.routing_history)[-100:]
        success_rate = sum(1 for d in recent_decisions if d.confidence_score > 0.7) / len(recent_decisions)
        
        if success_rate < 0.8:  # Si el éxito es bajo, considerar rewiring
            self._perform_rewiring()
    
    def _perform_rewiring(self):
        """Realiza rewiring del grafo de expertos."""
        try:
            # Analizar patrones de fallo
            failed_routings = [d for d in self.routing_history if d.confidence_score < 0.6]
            
            if not failed_routings:
                return
            
            # Identificar expertos problemáticos
            problematic_experts = defaultdict(int)
            for decision in failed_routings:
                problematic_experts[decision.primary_expert] += 1
            
            # Crear nuevas conexiones para expertos problemáticos
            for expert_id, failure_count in problematic_experts.items():
                if failure_count > 5:  # Umbral de fallos
                    self._rewire_expert(expert_id)
            
            self.performance_metrics['rewiring_events'] += 1
            logger.info(f"Rewiring realizado: {len(problematic_experts)} expertos problemáticos identificados")
            
        except Exception as e:
            logger.error(f"Error en rewiring: {e}")
    
    def _rewire_expert(self, expert_id: str):
        """Reconecta un experto específico."""
        if expert_id not in self.expert_graph.nodes:
            return
        
        expert = self.expert_graph.nodes[expert_id]
        
        # Encontrar expertos con mejor rendimiento
        best_experts = sorted(
            self.expert_graph.nodes.items(),
            key=lambda x: x[1].performance_score,
            reverse=True
        )
        
        # Crear conexiones con los mejores expertos
        connections_added = 0
        for other_expert_id, other_expert in best_experts[:3]:
            if (other_expert_id != expert_id and 
                other_expert_id not in self.expert_graph.get_neighbors(expert_id)):
                
                # Calcular peso basado en compatibilidad
                weight = self._calculate_connection_weight(expert, other_expert)
                
                if weight > 0.5:
                    self.expert_graph.add_connection(expert_id, other_expert_id, weight)
                    
                    # Crear evento de rewiring
                    event = RewiringEvent(
                        event_id=f"rewire_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                        event_type="add_connection",
                        from_expert=expert_id,
                        to_expert=other_expert_id,
                        weight=weight,
                        reason=f"Performance improvement for {expert_id}",
                        timestamp=datetime.now(),
                        impact_score=weight
                    )
                    
                    self.rewiring_history.append(event)
                    connections_added += 1
        
        logger.info(f"Rewiring completado para {expert_id}: {connections_added} conexiones agregadas")
    
    def _calculate_connection_weight(self, expert1: ExpertNode, expert2: ExpertNode) -> float:
        """Calcula peso de conexión entre dos expertos."""
        # Factores de compatibilidad
        type_compatibility = 0.5  # Base
        if expert1.expert_type == expert2.expert_type:
            type_compatibility = 1.0
        elif self._are_compatible_types(expert1.expert_type, expert2.expert_type):
            type_compatibility = 0.8
        
        performance_factor = (expert1.performance_score + expert2.performance_score) / 2.0
        success_factor = (expert1.success_rate + expert2.success_rate) / 2.0
        
        weight = (type_compatibility * 0.4 + 
                 performance_factor * 0.3 + 
                 success_factor * 0.3)
        
        return weight
    
    def _are_compatible_types(self, type1: ExpertType, type2: ExpertType) -> bool:
        """Verifica si dos tipos de expertos son compatibles."""
        compatible_pairs = [
            (ExpertType.PYTHON, ExpertType.ML),
            (ExpertType.PYTHON, ExpertType.DEBUG),
            (ExpertType.SQL, ExpertType.PYTHON),
            (ExpertType.JAVASCRIPT, ExpertType.API),
            (ExpertType.API, ExpertType.DEBUG)
        ]
        
        return (type1, type2) in compatible_pairs or (type2, type1) in compatible_pairs
    
    def _get_recent_performance(self, expert_id: str) -> float:
        """Obtiene rendimiento reciente de un experto."""
        if expert_id not in self.expert_graph.nodes:
            return 0.0
        
        expert = self.expert_graph.nodes[expert_id]
        return expert.performance_score
    
    def _get_recent_load(self, expert_id: str) -> float:
        """Obtiene carga reciente de un experto."""
        if expert_id not in self.expert_graph.nodes:
            return 1.0
        
        expert = self.expert_graph.nodes[expert_id]
        return expert.current_load / expert.capacity if expert.capacity > 0 else 1.0
    
    def get_expert_graph_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del grafo de expertos."""
        return {
            'graph_metrics': self.expert_graph.graph_metrics,
            'performance_metrics': self.performance_metrics,
            'total_experts': len(self.expert_graph.nodes),
            'total_connections': len(self.expert_graph.edges),
            'rewiring_events': len(self.rewiring_history),
            'routing_decisions': len(self.routing_history)
        }
    
    def get_expert_status(self) -> Dict[str, Any]:
        """Obtiene estado de todos los expertos."""
        expert_status = {}
        
        for expert_id, expert in self.expert_graph.nodes.items():
            expert_status[expert_id] = {
                'type': expert.expert_type.value,
                'capacity': expert.capacity,
                'current_load': expert.current_load,
                'load_percentage': (expert.current_load / expert.capacity * 100) if expert.capacity > 0 else 0,
                'performance_score': expert.performance_score,
                'latency_ms': expert.latency_ms,
                'success_rate': expert.success_rate,
                'connections': len(self.expert_graph.get_neighbors(expert_id)),
                'last_used': expert.last_used.isoformat()
            }
        
        return expert_status
    
    def update_expert_performance(self, expert_id: str, success: bool, latency_ms: float):
        """Actualiza rendimiento de un experto."""
        if expert_id not in self.expert_graph.nodes:
            return
        
        expert = self.expert_graph.nodes[expert_id]
        
        # Actualizar métricas
        if success:
            expert.success_rate = min(1.0, expert.success_rate + 0.01)
            expert.performance_score = min(1.0, expert.performance_score + 0.005)
        else:
            expert.success_rate = max(0.0, expert.success_rate - 0.02)
            expert.performance_score = max(0.0, expert.performance_score - 0.01)
        
        # Actualizar latencia (promedio móvil)
        expert.latency_ms = (expert.latency_ms * 0.9) + (latency_ms * 0.1)
        
        # Reducir carga
        expert.current_load = max(0, expert.current_load - 1)
        
        logger.debug(f"Rendimiento actualizado para {expert_id}: success={success}, latency={latency_ms}ms")


if __name__ == "__main__":
    # Test del RewiringExperts
    logging.basicConfig(level=logging.INFO)
    
    rewiring_system = RewiringExperts(strategy=RewiringStrategy.ADAPTIVE)
    
    # Test de routing
    test_queries = [
        ("How to create a Python function?", {"domain": "python", "complexity": 0.3}),
        ("SELECT * FROM users WHERE age > 25", {"domain": "sql", "complexity": 0.5}),
        ("Debug this JavaScript error", {"domain": "javascript", "complexity": 0.7}),
        ("Train a machine learning model", {"domain": "ml", "complexity": 0.8}),
        ("Create a REST API endpoint", {"domain": "api", "complexity": 0.6})
    ]
    
    for query, features in test_queries:
        decision = rewiring_system.route_query(query, features)
        print(f"Query: {query}")
        print(f"Routed to: {decision.primary_expert}")
        print(f"Confidence: {decision.confidence_score:.2f}")
        print(f"Fallback: {decision.fallback_experts}")
        print(f"Reasoning: {decision.reasoning}")
        print("-" * 50)
    
    # Mostrar métricas
    metrics = rewiring_system.get_expert_graph_metrics()
    print(f"Métricas del grafo: {metrics}")
    
    # Mostrar estado de expertos
    status = rewiring_system.get_expert_status()
    print(f"Estado de expertos: {status}")
