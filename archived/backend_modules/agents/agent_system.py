#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent System - Sistema completo de agentes persistentes.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from .database import DatabaseManager, Agent, AgentStatus, AgentInteraction, MemoryType
from .memory_manager import MemoryManager
from .graduation_system import GraduationSystem, GraduationCriteria
from .domain_system import DomainManager, CollaborationManager, DomainType, CollaborationType

logger = logging.getLogger(__name__)


class PersistentAgent:
    """Agente persistente con memoria y capacidades de aprendizaje."""
    
    def __init__(self, 
                 agent_id: str,
                 domain: DomainType,
                 db_manager: DatabaseManager,
                 memory_manager: MemoryManager,
                 domain_manager: DomainManager,
                 collaboration_manager: CollaborationManager):
        self.agent_id = agent_id
        self.domain = domain
        self.db_manager = db_manager
        self.memory_manager = memory_manager
        self.domain_manager = domain_manager
        self.collaboration_manager = collaboration_manager
        
        # Cargar o crear agente
        self.agent = self._load_or_create_agent()
        
        self.agent_stats = {
            'total_interactions': 0,
            'successful_interactions': 0,
            'collaborations_requested': 0,
            'collaborations_completed': 0,
            'memories_created': 0
        }
        
        logger.info(f"PersistentAgent inicializado: {agent_id} en dominio {domain.value}")
    
    def _load_or_create_agent(self) -> Agent:
        """Carga o crea el agente en la base de datos."""
        agent = self.db_manager.get_agent(self.agent_id)
        
        if not agent:
            # Crear nuevo agente
            agent = Agent(
                id=self.agent_id,
                domain=self.domain.value,
                status=AgentStatus.TRAINING,
                created_at=datetime.now(),
                last_updated=datetime.now(),
                total_interactions=0,
                success_rate=0.0,
                graduation_score=0.0,
                memory_tokens=0
            )
            
            success = self.db_manager.create_agent(agent)
            if not success:
                raise Exception(f"Error creando agente {self.agent_id}")
            
            logger.info(f"Nuevo agente creado: {self.agent_id}")
        
        return agent
    
    def process_query(self, 
                     query: str,
                     context: str = "",
                     user_intent: str = "",
                     require_collaboration: bool = False) -> Dict[str, Any]:
        """Procesa una query del usuario."""
        start_time = datetime.now()
        logger.debug(f"Procesando query para agente {self.agent_id}: {query[:100]}...")
        
        try:
            # Obtener contexto de memoria
            relevant_memories = self.memory_manager.get_relevant_memories(
                self.agent_id, query, limit=5
            )
            
            # Construir contexto enriquecido
            enriched_context = self._build_enriched_context(query, context, relevant_memories)
            
            # Generar respuesta
            if require_collaboration:
                response = self._generate_response_with_collaboration(query, enriched_context)
            else:
                response = self._generate_response(query, enriched_context)
            
            # Evaluar calidad de la respuesta
            quality_score = self._evaluate_response_quality(query, response, user_intent)
            
            # Crear interacción
            interaction = AgentInteraction(
                id=f"interaction_{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                agent_id=self.agent_id,
                query=query,
                response=response,
                success=quality_score >= 7.0,
                quality_score=quality_score,
                execution_time_ms=int((datetime.now() - start_time).total_seconds() * 1000),
                corrections_applied=0,
                context_used=enriched_context,
                created_at=datetime.now(),
                metadata={
                    'user_intent': user_intent,
                    'memories_used': len(relevant_memories),
                    'collaboration_used': require_collaboration
                }
            )
            
            # Guardar interacción
            self.db_manager.add_interaction(interaction)
            
            # Agregar a memoria
            self._add_to_memory(query, response, quality_score, relevant_memories)
            
            # Actualizar estadísticas del agente
            self._update_agent_stats(interaction)
            
            result = {
                'success': True,
                'response': response,
                'quality_score': quality_score,
                'execution_time_ms': interaction.execution_time_ms,
                'memories_used': len(relevant_memories),
                'collaboration_used': require_collaboration,
                'agent_id': self.agent_id,
                'domain': self.domain.value,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Query procesada exitosamente: quality={quality_score:.1f}, "
                       f"time={interaction.execution_time_ms}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando query para agente {self.agent_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent_id': self.agent_id,
                'domain': self.domain.value,
                'timestamp': datetime.now().isoformat()
            }
    
    def _build_enriched_context(self, 
                               query: str, 
                               context: str, 
                               memories: List[Any]) -> str:
        """Construye contexto enriquecido con memorias relevantes."""
        enriched_parts = []
        
        # Contexto original
        if context:
            enriched_parts.append(f"Context: {context}")
        
        # Memorias relevantes
        if memories:
            memory_context = "Relevant memories:\n"
            for i, memory in enumerate(memories[:3]):  # Máximo 3 memorias
                memory_context += f"{i+1}. {memory.content[:200]}...\n"
            enriched_parts.append(memory_context)
        
        # Prompt del dominio
        domain_prompt = self.domain_manager.get_domain_prompt(self.domain, 'system_prompt')
        enriched_parts.append(f"Domain expertise: {domain_prompt}")
        
        return "\n\n".join(enriched_parts)
    
    def _generate_response(self, query: str, context: str) -> str:
        """Genera respuesta usando el prompt del dominio."""
        # Obtener prompt de generación del dominio
        generation_prompt = self.domain_manager.get_domain_prompt(
            self.domain, 'generation_prompt', query
        )
        
        # Simular generación de respuesta (en producción usaría el modelo real)
        response = f"Based on my expertise in {self.domain.value}, here's my response to: {query}\n\n"
        response += f"Context: {context[:200]}...\n\n"
        response += f"Response: This is a simulated response from agent {self.agent_id} "
        response += f"specializing in {self.domain.value}. In a real implementation, "
        response += "this would be generated by the actual language model."
        
        return response
    
    def _generate_response_with_collaboration(self, query: str, context: str) -> str:
        """Genera respuesta con colaboración de otros agentes."""
        try:
            # Solicitar colaboración
            collaboration_request = self.collaboration_manager.request_collaboration(
                requester_agent_id=self.agent_id,
                query=query,
                context=context,
                collaboration_type=CollaborationType.KNOWLEDGE_SHARING,
                target_domain=self.domain
            )
            
            if collaboration_request:
                self.agent_stats['collaborations_requested'] += 1
                
                # Simular respuesta de colaboración
                collaboration_response = f"Collaboration with {collaboration_request.target_agent_id}: "
                collaboration_response += f"Here's additional insight for: {query}"
                
                # Procesar colaboración
                result = self.collaboration_manager.process_collaboration(
                    collaboration_request.id,
                    collaboration_response,
                    quality_score=8.0,
                    execution_time_ms=1000
                )
                
                if result:
                    self.agent_stats['collaborations_completed'] += 1
                    return f"Response with collaboration:\n\n{self._generate_response(query, context)}\n\nCollaboration insight: {collaboration_response}"
            
            # Fallback a respuesta normal
            return self._generate_response(query, context)
            
        except Exception as e:
            logger.error(f"Error en colaboración para agente {self.agent_id}: {e}")
            return self._generate_response(query, context)
    
    def _evaluate_response_quality(self, query: str, response: str, user_intent: str) -> float:
        """Evalúa la calidad de la respuesta."""
        # Métricas simples de calidad
        quality_score = 5.0  # Base score
        
        # Longitud de respuesta
        if len(response) > 100:
            quality_score += 1.0
        
        # Relevancia (palabras clave en común)
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        overlap = len(query_words.intersection(response_words))
        if overlap > 0:
            quality_score += min(2.0, overlap * 0.5)
        
        # Estructura (párrafos, listas, etc.)
        if '\n' in response or '•' in response or '1.' in response:
            quality_score += 1.0
        
        # Especificidad del dominio
        domain_keywords = {
            DomainType.PYTHON: ['python', 'code', 'function', 'class'],
            DomainType.SQL: ['sql', 'query', 'database', 'table'],
            DomainType.JAVASCRIPT: ['javascript', 'js', 'function', 'async'],
            DomainType.DEBUG: ['debug', 'error', 'fix', 'problem'],
            DomainType.ML: ['machine learning', 'model', 'algorithm', 'data'],
            DomainType.API: ['api', 'endpoint', 'request', 'response']
        }
        
        if self.domain in domain_keywords:
            domain_words = domain_keywords[self.domain]
            domain_overlap = sum(1 for word in domain_words if word in response.lower())
            quality_score += min(1.0, domain_overlap * 0.3)
        
        return min(10.0, quality_score)
    
    def _add_to_memory(self, 
                      query: str, 
                      response: str, 
                      quality_score: float,
                      relevant_memories: List[Any]):
        """Agrega información a la memoria del agente."""
        try:
            # Determinar tipo de memoria basado en la calidad
            if quality_score >= 8.0:
                memory_type = MemoryType.KNOWLEDGE
                importance_score = 0.9
            elif quality_score >= 6.0:
                memory_type = MemoryType.EXPERIENCE
                importance_score = 0.7
            else:
                memory_type = MemoryType.CONVERSATION
                importance_score = 0.5
            
            # Crear contenido de memoria
            memory_content = f"Query: {query}\nResponse: {response}\nQuality: {quality_score:.1f}"
            
            # Agregar a memoria
            success = self.memory_manager.add_memory(
                agent_id=self.agent_id,
                memory_type=memory_type,
                content=memory_content,
                importance_score=importance_score,
                metadata={
                    'quality_score': quality_score,
                    'domain': self.domain.value,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            if success:
                self.agent_stats['memories_created'] += 1
            
        except Exception as e:
            logger.error(f"Error agregando a memoria del agente {self.agent_id}: {e}")
    
    def _update_agent_stats(self, interaction: AgentInteraction):
        """Actualiza estadísticas del agente."""
        self.agent_stats['total_interactions'] += 1
        
        if interaction.success:
            self.agent_stats['successful_interactions'] += 1
        
        # Actualizar agente en la base de datos
        self.agent.total_interactions += 1
        self.agent.last_updated = datetime.now()
        
        # Recalcular success rate
        if self.agent.total_interactions > 0:
            self.agent.success_rate = self.agent_stats['successful_interactions'] / self.agent_stats['total_interactions']
        
        self.db_manager.update_agent(self.agent)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Retorna información del agente."""
        return {
            'agent_id': self.agent_id,
            'domain': self.domain.value,
            'status': self.agent.status.value,
            'total_interactions': self.agent.total_interactions,
            'success_rate': self.agent.success_rate,
            'graduation_score': self.agent.graduation_score,
            'memory_tokens': self.agent.memory_tokens,
            'created_at': self.agent.created_at.isoformat(),
            'last_updated': self.agent.last_updated.isoformat(),
            'stats': self.agent_stats
        }
    
    def get_memories(self, memory_type: Optional[MemoryType] = None, limit: int = 10) -> List[Any]:
        """Obtiene memorias del agente."""
        return self.memory_manager.get_agent_memories(self.agent_id, memory_type, limit)
    
    def get_interactions(self, limit: int = 10) -> List[AgentInteraction]:
        """Obtiene interacciones del agente."""
        return self.db_manager.get_agent_interactions(self.agent_id, limit)


class AgentSystem:
    """Sistema completo de agentes persistentes."""
    
    def __init__(self, db_path: str = "backend/data/agents.db"):
        self.db_manager = DatabaseManager(db_path)
        self.memory_manager = MemoryManager(self.db_manager)
        self.domain_manager = DomainManager(self.db_manager)
        self.collaboration_manager = CollaborationManager(self.db_manager, self.domain_manager)
        self.graduation_system = GraduationSystem(self.db_manager, self.memory_manager)
        
        self.active_agents = {}
        self.system_stats = {
            'total_agents_created': 0,
            'active_agents': 0,
            'graduated_agents': 0,
            'total_interactions': 0,
            'total_collaborations': 0
        }
        
        logger.info("AgentSystem inicializado")
    
    def create_agent(self, domain: DomainType, agent_id: Optional[str] = None) -> PersistentAgent:
        """Crea un nuevo agente persistente."""
        if not agent_id:
            agent_id = f"agent_{domain.value}_{uuid.uuid4().hex[:8]}"
        
        try:
            agent = PersistentAgent(
                agent_id=agent_id,
                domain=domain,
                db_manager=self.db_manager,
                memory_manager=self.memory_manager,
                domain_manager=self.domain_manager,
                collaboration_manager=self.collaboration_manager
            )
            
            self.active_agents[agent_id] = agent
            self.system_stats['total_agents_created'] += 1
            self.system_stats['active_agents'] += 1
            
            logger.info(f"Agente creado: {agent_id} en dominio {domain.value}")
            return agent
            
        except Exception as e:
            logger.error(f"Error creando agente {agent_id}: {e}")
            raise
    
    def get_agent(self, agent_id: str) -> Optional[PersistentAgent]:
        """Obtiene un agente por ID."""
        if agent_id in self.active_agents:
            return self.active_agents[agent_id]
        
        # Intentar cargar desde la base de datos
        agent_data = self.db_manager.get_agent(agent_id)
        if agent_data:
            try:
                domain = DomainType(agent_data.domain)
                agent = PersistentAgent(
                    agent_id=agent_id,
                    domain=domain,
                    db_manager=self.db_manager,
                    memory_manager=self.memory_manager,
                    domain_manager=self.domain_manager,
                    collaboration_manager=self.collaboration_manager
                )
                
                self.active_agents[agent_id] = agent
                return agent
                
            except Exception as e:
                logger.error(f"Error cargando agente {agent_id}: {e}")
        
        return None
    
    def get_agents_by_domain(self, domain: DomainType) -> List[PersistentAgent]:
        """Obtiene agentes por dominio."""
        agents = []
        
        # Agentes activos
        for agent in self.active_agents.values():
            if agent.domain == domain:
                agents.append(agent)
        
        # Agentes de la base de datos
        db_agents = self.db_manager.get_agents_by_domain(domain.value)
        for db_agent in db_agents:
            if db_agent.id not in self.active_agents:
                try:
                    persistent_agent = PersistentAgent(
                        agent_id=db_agent.id,
                        domain=domain,
                        db_manager=self.db_manager,
                        memory_manager=self.memory_manager,
                        domain_manager=self.domain_manager,
                        collaboration_manager=self.collaboration_manager
                    )
                    agents.append(persistent_agent)
                except Exception as e:
                    logger.error(f"Error cargando agente {db_agent.id}: {e}")
        
        return agents
    
    def evaluate_graduations(self) -> List[Dict[str, Any]]:
        """Evalúa todos los agentes para graduación."""
        results = self.graduation_system.evaluate_all_agents()
        
        graduation_results = []
        for result in results:
            graduation_results.append({
                'agent_id': result.agent_id,
                'eligible': result.eligible,
                'graduation_score': result.graduation_score,
                'criteria_met': result.criteria_met,
                'recommendations': result.recommendations
            })
        
        return graduation_results
    
    def graduate_agent(self, agent_id: str) -> bool:
        """Gradua un agente."""
        return self.graduation_system.graduate_agent(agent_id)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema."""
        db_stats = self.db_manager.get_database_stats()
        memory_stats = self.memory_manager.get_manager_stats()
        domain_stats = self.domain_manager.get_domain_stats()
        collaboration_stats = self.collaboration_manager.get_collaboration_stats()
        graduation_stats = self.graduation_system.get_graduation_stats()
        
        return {
            'system_stats': self.system_stats,
            'database_stats': db_stats,
            'memory_stats': memory_stats,
            'domain_stats': domain_stats,
            'collaboration_stats': collaboration_stats,
            'graduation_stats': graduation_stats,
            'active_agents_count': len(self.active_agents)
        }


if __name__ == "__main__":
    # Test del AgentSystem
    logging.basicConfig(level=logging.INFO)
    
    agent_system = AgentSystem()
    
    # Crear agente de prueba
    agent = agent_system.create_agent(DomainType.PYTHON, "test_python_agent")
    
    # Procesar query
    result = agent.process_query(
        query="How to create a Python function?",
        context="Learning Python basics",
        user_intent="Learn about functions"
    )
    
    print(f"Query procesada:")
    print(f"Success: {result['success']}")
    print(f"Quality score: {result['quality_score']}")
    print(f"Response: {result['response'][:200]}...")
    
    # Obtener información del agente
    agent_info = agent.get_agent_info()
    print(f"\nInformación del agente: {agent_info}")
    
    # Mostrar estadísticas del sistema
    stats = agent_system.get_system_stats()
    print(f"\nEstadísticas del sistema: {stats}")
