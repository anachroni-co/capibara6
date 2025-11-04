#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graduation System - Sistema de graduación de agentes (85% success rate).
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from .database import DatabaseManager, Agent, AgentStatus, AgentInteraction, MemoryType
from .memory_manager import MemoryManager

logger = logging.getLogger(__name__)


@dataclass
class GraduationCriteria:
    """Criterios de graduación para agentes."""
    min_success_rate: float = 0.85  # 85% success rate
    min_interactions: int = 100     # Mínimo 100 interacciones
    min_quality_score: float = 7.0  # Mínimo 7.0 de calidad
    min_memory_utilization: float = 0.3  # 30% de memoria utilizada
    max_graduation_time_days: int = 30   # Máximo 30 días para graduarse
    min_domain_expertise: float = 0.8    # 80% de expertise en dominio


@dataclass
class GraduationResult:
    """Resultado de evaluación de graduación."""
    agent_id: str
    eligible: bool
    graduation_score: float
    criteria_met: Dict[str, bool]
    scores: Dict[str, float]
    recommendations: List[str]
    evaluation_date: datetime


class GraduationEvaluator:
    """Evalúa si un agente está listo para graduarse."""
    
    def __init__(self, criteria: GraduationCriteria = None):
        self.criteria = criteria or GraduationCriteria()
        self.evaluation_stats = {
            'total_evaluations': 0,
            'eligible_agents': 0,
            'graduated_agents': 0,
            'avg_graduation_score': 0.0
        }
        
        logger.info("GraduationEvaluator inicializado")
    
    def evaluate_agent(self, 
                      agent: Agent, 
                      interactions: List[AgentInteraction],
                      memories: List[Any]) -> GraduationResult:
        """Evalúa si un agente está listo para graduarse."""
        logger.debug(f"Evaluando agente {agent.id} para graduación")
        
        try:
            # Calcular métricas
            metrics = self._calculate_metrics(agent, interactions, memories)
            
            # Evaluar criterios
            criteria_met = self._evaluate_criteria(metrics)
            
            # Calcular score de graduación
            graduation_score = self._calculate_graduation_score(metrics, criteria_met)
            
            # Determinar elegibilidad
            eligible = all(criteria_met.values())
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(metrics, criteria_met)
            
            result = GraduationResult(
                agent_id=agent.id,
                eligible=eligible,
                graduation_score=graduation_score,
                criteria_met=criteria_met,
                scores=metrics,
                recommendations=recommendations,
                evaluation_date=datetime.now()
            )
            
            # Actualizar estadísticas
            self._update_evaluation_stats(result)
            
            logger.info(f"Evaluación completada para agente {agent.id}: "
                       f"eligible={eligible}, score={graduation_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error evaluando agente {agent.id}: {e}")
            return GraduationResult(
                agent_id=agent.id,
                eligible=False,
                graduation_score=0.0,
                criteria_met={},
                scores={},
                recommendations=[f"Error en evaluación: {str(e)}"],
                evaluation_date=datetime.now()
            )
    
    def _calculate_metrics(self, 
                          agent: Agent, 
                          interactions: List[AgentInteraction],
                          memories: List[Any]) -> Dict[str, float]:
        """Calcula métricas del agente."""
        metrics = {}
        
        # Métricas básicas
        metrics['success_rate'] = agent.success_rate
        metrics['total_interactions'] = agent.total_interactions
        metrics['memory_utilization'] = agent.memory_tokens / agent.max_memory_tokens
        
        # Métricas de calidad
        if interactions:
            quality_scores = [i.quality_score for i in interactions if i.quality_score > 0]
            metrics['avg_quality_score'] = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            
            execution_times = [i.execution_time_ms for i in interactions]
            metrics['avg_execution_time'] = sum(execution_times) / len(execution_times)
            
            corrections = [i.corrections_applied for i in interactions]
            metrics['avg_corrections'] = sum(corrections) / len(corrections)
        else:
            metrics['avg_quality_score'] = 0.0
            metrics['avg_execution_time'] = 0.0
            metrics['avg_corrections'] = 0.0
        
        # Métricas de memoria
        if memories:
            importance_scores = [m.importance_score for m in memories]
            metrics['avg_memory_importance'] = sum(importance_scores) / len(importance_scores)
            
            access_counts = [m.access_count for m in memories]
            metrics['avg_memory_access'] = sum(access_counts) / len(access_counts)
        else:
            metrics['avg_memory_importance'] = 0.0
            metrics['avg_memory_access'] = 0.0
        
        # Métricas de tiempo
        days_active = (datetime.now() - agent.created_at).days
        metrics['days_active'] = days_active
        
        # Métricas de dominio (simuladas)
        metrics['domain_expertise'] = self._calculate_domain_expertise(agent, interactions)
        
        return metrics
    
    def _calculate_domain_expertise(self, agent: Agent, interactions: List[AgentInteraction]) -> float:
        """Calcula expertise en el dominio del agente."""
        if not interactions:
            return 0.0
        
        # Análisis simple basado en éxito y calidad
        successful_interactions = [i for i in interactions if i.success]
        if not successful_interactions:
            return 0.0
        
        # Calcular expertise basado en éxito y calidad
        success_rate = len(successful_interactions) / len(interactions)
        avg_quality = sum(i.quality_score for i in successful_interactions) / len(successful_interactions)
        
        # Normalizar a 0-1
        expertise = (success_rate * 0.6) + (avg_quality / 10.0 * 0.4)
        return min(1.0, expertise)
    
    def _evaluate_criteria(self, metrics: Dict[str, float]) -> Dict[str, bool]:
        """Evalúa si se cumplen los criterios de graduación."""
        criteria = self.criteria
        
        return {
            'success_rate': metrics['success_rate'] >= criteria.min_success_rate,
            'min_interactions': metrics['total_interactions'] >= criteria.min_interactions,
            'quality_score': metrics['avg_quality_score'] >= criteria.min_quality_score,
            'memory_utilization': metrics['memory_utilization'] >= criteria.min_memory_utilization,
            'time_limit': metrics['days_active'] <= criteria.max_graduation_time_days,
            'domain_expertise': metrics['domain_expertise'] >= criteria.min_domain_expertise
        }
    
    def _calculate_graduation_score(self, 
                                  metrics: Dict[str, float], 
                                  criteria_met: Dict[str, bool]) -> float:
        """Calcula el score de graduación."""
        # Pesos para diferentes métricas
        weights = {
            'success_rate': 0.25,
            'quality_score': 0.20,
            'domain_expertise': 0.20,
            'memory_utilization': 0.15,
            'interactions': 0.10,
            'time_efficiency': 0.10
        }
        
        # Calcular scores normalizados
        scores = {}
        
        # Success rate (0-1)
        scores['success_rate'] = metrics['success_rate']
        
        # Quality score (0-1)
        scores['quality_score'] = metrics['avg_quality_score'] / 10.0
        
        # Domain expertise (0-1)
        scores['domain_expertise'] = metrics['domain_expertise']
        
        # Memory utilization (0-1)
        scores['memory_utilization'] = min(1.0, metrics['memory_utilization'] / 0.5)  # 50% = 1.0
        
        # Interactions (0-1)
        scores['interactions'] = min(1.0, metrics['total_interactions'] / 200.0)  # 200 = 1.0
        
        # Time efficiency (0-1) - menos tiempo = mejor
        time_score = max(0.0, 1.0 - (metrics['days_active'] / 30.0))
        scores['time_efficiency'] = time_score
        
        # Calcular score ponderado
        graduation_score = sum(scores[metric] * weights[metric] for metric in weights)
        
        # Bonus por cumplir todos los criterios
        if all(criteria_met.values()):
            graduation_score = min(1.0, graduation_score + 0.1)
        
        return graduation_score
    
    def _generate_recommendations(self, 
                                metrics: Dict[str, float], 
                                criteria_met: Dict[str, bool]) -> List[str]:
        """Genera recomendaciones para mejorar el agente."""
        recommendations = []
        
        if not criteria_met['success_rate']:
            recommendations.append(f"Increase success rate from {metrics['success_rate']:.1%} to {self.criteria.min_success_rate:.1%}")
        
        if not criteria_met['min_interactions']:
            recommendations.append(f"Need {self.criteria.min_interactions - metrics['total_interactions']} more interactions")
        
        if not criteria_met['quality_score']:
            recommendations.append(f"Improve quality score from {metrics['avg_quality_score']:.1f} to {self.criteria.min_quality_score}")
        
        if not criteria_met['memory_utilization']:
            recommendations.append(f"Increase memory utilization from {metrics['memory_utilization']:.1%} to {self.criteria.min_memory_utilization:.1%}")
        
        if not criteria_met['domain_expertise']:
            recommendations.append(f"Improve domain expertise from {metrics['domain_expertise']:.1%} to {self.criteria.min_domain_expertise:.1%}")
        
        if criteria_met['time_limit'] and metrics['days_active'] > 20:
            recommendations.append("Consider accelerating learning to graduate within time limit")
        
        if not recommendations:
            recommendations.append("Agent is ready for graduation!")
        
        return recommendations
    
    def _update_evaluation_stats(self, result: GraduationResult):
        """Actualiza estadísticas de evaluación."""
        self.evaluation_stats['total_evaluations'] += 1
        
        if result.eligible:
            self.evaluation_stats['eligible_agents'] += 1
        
        # Actualizar score promedio
        current_avg = self.evaluation_stats['avg_graduation_score']
        total_evals = self.evaluation_stats['total_evaluations']
        
        self.evaluation_stats['avg_graduation_score'] = (
            (current_avg * (total_evals - 1) + result.graduation_score) / total_evals
        )
    
    def get_evaluation_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de evaluación."""
        return self.evaluation_stats.copy()


class GraduationSystem:
    """Sistema completo de graduación de agentes."""
    
    def __init__(self, 
                 db_manager: DatabaseManager,
                 memory_manager: MemoryManager,
                 criteria: GraduationCriteria = None):
        self.db_manager = db_manager
        self.memory_manager = memory_manager
        self.evaluator = GraduationEvaluator(criteria)
        
        self.system_stats = {
            'total_graduations': 0,
            'successful_graduations': 0,
            'failed_graduations': 0,
            'agents_evaluated': 0,
            'playbooks_created': 0
        }
        
        logger.info("GraduationSystem inicializado")
    
    def evaluate_all_agents(self) -> List[GraduationResult]:
        """Evalúa todos los agentes activos para graduación."""
        logger.info("Evaluando todos los agentes para graduación")
        
        try:
            # Obtener agentes activos
            active_agents = self.db_manager.get_agents_by_status(AgentStatus.ACTIVE)
            training_agents = self.db_manager.get_agents_by_status(AgentStatus.TRAINING)
            all_agents = active_agents + training_agents
            
            results = []
            
            for agent in all_agents:
                # Obtener interacciones y memorias
                interactions = self.db_manager.get_agent_interactions(agent.id, limit=1000)
                memories = self.memory_manager.get_agent_memories(agent.id)
                
                # Evaluar agente
                result = self.evaluator.evaluate_agent(agent, interactions, memories)
                results.append(result)
                
                # Actualizar score de graduación en el agente
                agent.graduation_score = result.graduation_score
                agent.last_updated = datetime.now()
                self.db_manager.update_agent(agent)
                
                self.system_stats['agents_evaluated'] += 1
            
            logger.info(f"Evaluación completada: {len(results)} agentes evaluados")
            return results
            
        except Exception as e:
            logger.error(f"Error evaluando agentes: {e}")
            return []
    
    def graduate_agent(self, agent_id: str) -> bool:
        """Gradua un agente si cumple los criterios."""
        try:
            # Obtener agente
            agent = self.db_manager.get_agent(agent_id)
            if not agent:
                logger.error(f"Agente {agent_id} no encontrado")
                return False
            
            # Obtener interacciones y memorias
            interactions = self.db_manager.get_agent_interactions(agent_id, limit=1000)
            memories = self.memory_manager.get_agent_memories(agent_id)
            
            # Evaluar para graduación
            result = self.evaluator.evaluate_agent(agent, interactions, memories)
            
            if not result.eligible:
                logger.warning(f"Agente {agent_id} no es elegible para graduación")
                return False
            
            # Graduar agente
            agent.status = AgentStatus.GRADUATED
            agent.graduation_score = result.graduation_score
            agent.last_updated = datetime.now()
            
            success = self.db_manager.update_agent(agent)
            
            if success:
                # Registrar graduación
                self._record_graduation(agent, result, interactions, memories)
                
                # Crear playbook
                playbook_created = self._create_playbook_from_agent(agent, interactions, memories)
                
                self.system_stats['total_graduations'] += 1
                self.system_stats['successful_graduations'] += 1
                
                if playbook_created:
                    self.system_stats['playbooks_created'] += 1
                
                logger.info(f"Agente {agent_id} graduado exitosamente con score {result.graduation_score:.2f}")
                return True
            else:
                self.system_stats['failed_graduations'] += 1
                return False
                
        except Exception as e:
            logger.error(f"Error graduando agente {agent_id}: {e}")
            self.system_stats['failed_graduations'] += 1
            return False
    
    def _record_graduation(self, 
                          agent: Agent, 
                          result: GraduationResult,
                          interactions: List[AgentInteraction],
                          memories: List[Any]):
        """Registra la graduación en la base de datos."""
        try:
            # Calcular métricas de graduación
            total_interactions = len(interactions)
            successful_interactions = len([i for i in interactions if i.success])
            success_rate = successful_interactions / max(1, total_interactions)
            
            # Calcular ratio de compresión de memoria
            total_memory_tokens = sum(memory.tokens for memory in memories)
            memory_compression_ratio = total_memory_tokens / agent.max_memory_tokens
            
            # Contar contribuciones al playbook
            playbook_contributions = len([i for i in interactions if i.quality_score >= 8.0])
            
            # Insertar registro de graduación
            with self.db_manager.db_path as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO agent_graduations (
                        id, agent_id, graduation_date, final_score,
                        interactions_count, success_rate, memory_compression_ratio,
                        playbook_contributions, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"grad_{agent.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    agent.id,
                    datetime.now().isoformat(),
                    result.graduation_score,
                    total_interactions,
                    success_rate,
                    memory_compression_ratio,
                    playbook_contributions,
                    json.dumps({
                        'criteria_met': result.criteria_met,
                        'scores': result.scores,
                        'recommendations': result.recommendations
                    })
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error registrando graduación del agente {agent.id}: {e}")
    
    def _create_playbook_from_agent(self, 
                                  agent: Agent,
                                  interactions: List[AgentInteraction],
                                  memories: List[Any]) -> bool:
        """Crea un playbook basado en las experiencias del agente."""
        try:
            # Filtrar interacciones de alta calidad
            high_quality_interactions = [
                i for i in interactions 
                if i.success and i.quality_score >= 8.0
            ]
            
            if not high_quality_interactions:
                logger.warning(f"No hay interacciones de alta calidad para crear playbook del agente {agent.id}")
                return False
            
            # Crear playbook (implementación simplificada)
            playbook_data = {
                'agent_id': agent.id,
                'domain': agent.domain,
                'graduation_score': agent.graduation_score,
                'total_interactions': len(interactions),
                'high_quality_interactions': len(high_quality_interactions),
                'patterns': self._extract_patterns(high_quality_interactions),
                'knowledge': self._extract_knowledge(memories),
                'created_at': datetime.now().isoformat()
            }
            
            # Guardar playbook (implementación simplificada)
            playbook_path = f"backend/data/playbooks/agent_{agent.id}_playbook.json"
            os.makedirs(os.path.dirname(playbook_path), exist_ok=True)
            
            with open(playbook_path, 'w', encoding='utf-8') as f:
                json.dump(playbook_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Playbook creado para agente {agent.id}: {playbook_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creando playbook para agente {agent.id}: {e}")
            return False
    
    def _extract_patterns(self, interactions: List[AgentInteraction]) -> List[Dict[str, Any]]:
        """Extrae patrones de interacciones exitosas."""
        patterns = []
        
        for interaction in interactions[:10]:  # Top 10 interacciones
            pattern = {
                'query_pattern': interaction.query[:100] + "..." if len(interaction.query) > 100 else interaction.query,
                'response_template': interaction.response[:200] + "..." if len(interaction.response) > 200 else interaction.response,
                'quality_score': interaction.quality_score,
                'execution_time': interaction.execution_time_ms,
                'corrections_applied': interaction.corrections_applied
            }
            patterns.append(pattern)
        
        return patterns
    
    def _extract_knowledge(self, memories: List[Any]) -> List[Dict[str, Any]]:
        """Extrae conocimiento de las memorias."""
        knowledge = []
        
        for memory in memories:
            if memory.memory_type == MemoryType.KNOWLEDGE and memory.importance_score >= 0.7:
                knowledge_item = {
                    'content': memory.content[:300] + "..." if len(memory.content) > 300 else memory.content,
                    'importance_score': memory.importance_score,
                    'access_count': memory.access_count
                }
                knowledge.append(knowledge_item)
        
        return knowledge
    
    def get_graduation_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de graduación."""
        evaluator_stats = self.evaluator.get_evaluation_stats()
        
        return {
            'system_stats': self.system_stats,
            'evaluator_stats': evaluator_stats,
            'criteria': {
                'min_success_rate': self.evaluator.criteria.min_success_rate,
                'min_interactions': self.evaluator.criteria.min_interactions,
                'min_quality_score': self.evaluator.criteria.min_quality_score,
                'min_memory_utilization': self.evaluator.criteria.min_memory_utilization,
                'max_graduation_time_days': self.evaluator.criteria.max_graduation_time_days,
                'min_domain_expertise': self.evaluator.criteria.min_domain_expertise
            }
        }


if __name__ == "__main__":
    # Test del GraduationSystem
    logging.basicConfig(level=logging.INFO)
    
    from .database import DatabaseManager
    from .memory_manager import MemoryManager
    
    db_manager = DatabaseManager()
    memory_manager = MemoryManager(db_manager)
    graduation_system = GraduationSystem(db_manager, memory_manager)
    
    # Crear agente de prueba
    from .database import Agent, AgentStatus, AgentInteraction
    agent = Agent(
        id="test_graduation_agent",
        domain="python",
        status=AgentStatus.ACTIVE,
        created_at=datetime.now() - timedelta(days=5),
        last_updated=datetime.now(),
        total_interactions=150,
        success_rate=0.87,
        graduation_score=0.0,
        memory_tokens=50000
    )
    
    db_manager.create_agent(agent)
    
    # Agregar interacciones de prueba
    for i in range(150):
        interaction = AgentInteraction(
            id=f"interaction_{i}",
            agent_id="test_graduation_agent",
            query=f"Test query {i}",
            response=f"Test response {i}",
            success=i < 130,  # 87% success rate
            quality_score=8.5 if i < 130 else 5.0,
            execution_time_ms=1000 + (i % 500),
            corrections_applied=0 if i < 130 else 1,
            context_used="test context",
            created_at=datetime.now() - timedelta(hours=i)
        )
        db_manager.add_interaction(interaction)
    
    # Evaluar agente
    result = graduation_system.evaluate_all_agents()
    print(f"Evaluación completada: {len(result)} agentes evaluados")
    
    if result:
        evaluation = result[0]
        print(f"Agente elegible: {evaluation.eligible}")
        print(f"Score de graduación: {evaluation.graduation_score:.2f}")
        print(f"Criterios cumplidos: {evaluation.criteria_met}")
        print(f"Recomendaciones: {evaluation.recommendations}")
    
    # Mostrar estadísticas
    stats = graduation_system.get_graduation_stats()
    print(f"Estadísticas: {stats}")
