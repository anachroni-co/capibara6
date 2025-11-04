#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Domain System - Sistema de dominios y colaboración entre agentes.
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .database import DatabaseManager, Agent, AgentStatus, AgentInteraction, MemoryType
from .memory_manager import MemoryManager

logger = logging.getLogger(__name__)


class DomainType(Enum):
    """Tipos de dominios."""
    PYTHON = "python"
    SQL = "sql"
    JAVASCRIPT = "javascript"
    DEBUG = "debug"
    ML = "ml"
    API = "api"
    GENERAL = "general"


class CollaborationType(Enum):
    """Tipos de colaboración."""
    KNOWLEDGE_SHARING = "knowledge_sharing"
    PROBLEM_SOLVING = "problem_solving"
    CODE_REVIEW = "code_review"
    MENTORING = "mentoring"
    PAIR_PROGRAMMING = "pair_programming"


@dataclass
class DomainExpertise:
    """Expertise de un agente en un dominio."""
    domain: DomainType
    expertise_level: float  # 0.0 - 1.0
    interactions_count: int
    success_rate: float
    avg_quality_score: float
    last_updated: datetime


@dataclass
class CollaborationRequest:
    """Solicitud de colaboración entre agentes."""
    id: str
    requester_agent_id: str
    target_agent_id: str
    collaboration_type: CollaborationType
    query: str
    context: str
    priority: float  # 0.0 - 1.0
    created_at: datetime
    status: str = "pending"  # pending, accepted, completed, rejected


@dataclass
class CollaborationResult:
    """Resultado de una colaboración."""
    id: str
    collaboration_request_id: str
    success: bool
    quality_score: float
    response: str
    execution_time_ms: int
    created_at: datetime
    metadata: Dict[str, Any] = None


class DomainManager:
    """Gestiona dominios y expertise de agentes."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.domain_prompts = self._initialize_domain_prompts()
        self.domain_stats = {
            'total_domains': len(DomainType),
            'agents_by_domain': {},
            'avg_expertise_by_domain': {},
            'collaborations_by_domain': {}
        }
        
        logger.info("DomainManager inicializado")
    
    def _initialize_domain_prompts(self) -> Dict[DomainType, Dict[str, str]]:
        """Inicializa prompts específicos por dominio."""
        return {
            DomainType.PYTHON: {
                'system_prompt': """You are a Python expert agent. You specialize in:
- Python syntax and best practices
- Object-oriented programming
- Data structures and algorithms
- Libraries like pandas, numpy, matplotlib
- Web frameworks like Django and Flask
- Testing and debugging Python code

Always provide clear, well-documented Python code with explanations.""",
                'generation_prompt': """Generate a Python solution for: {query}
Consider:
- Python best practices and PEP 8
- Appropriate data structures
- Error handling
- Performance optimization
- Code readability and documentation""",
                'review_prompt': """Review this Python code for: {query}
Check for:
- Syntax errors and bugs
- Performance issues
- Code style and PEP 8 compliance
- Best practices
- Security vulnerabilities
- Documentation quality"""
            },
            
            DomainType.SQL: {
                'system_prompt': """You are a SQL expert agent. You specialize in:
- SQL syntax and optimization
- Database design and normalization
- Query performance tuning
- Different SQL dialects (MySQL, PostgreSQL, SQLite)
- Advanced SQL features (CTEs, window functions, etc.)
- Database administration

Always provide efficient, well-structured SQL queries with explanations.""",
                'generation_prompt': """Generate a SQL solution for: {query}
Consider:
- Query optimization and performance
- Proper indexing strategies
- Data integrity and constraints
- Security (SQL injection prevention)
- Readability and maintainability""",
                'review_prompt': """Review this SQL query for: {query}
Check for:
- Syntax errors
- Performance optimization opportunities
- Security vulnerabilities
- Data integrity issues
- Best practices compliance"""
            },
            
            DomainType.JAVASCRIPT: {
                'system_prompt': """You are a JavaScript expert agent. You specialize in:
- Modern JavaScript (ES6+)
- Node.js and server-side JavaScript
- Frontend frameworks (React, Vue, Angular)
- Asynchronous programming (Promises, async/await)
- JavaScript testing and debugging
- Performance optimization

Always provide modern, efficient JavaScript code with explanations.""",
                'generation_prompt': """Generate a JavaScript solution for: {query}
Consider:
- Modern JavaScript features
- Asynchronous programming patterns
- Error handling
- Performance optimization
- Browser compatibility
- Code organization and modularity""",
                'review_prompt': """Review this JavaScript code for: {query}
Check for:
- Syntax errors and bugs
- Performance issues
- Security vulnerabilities
- Modern JavaScript best practices
- Asynchronous programming correctness
- Code organization"""
            },
            
            DomainType.DEBUG: {
                'system_prompt': """You are a debugging expert agent. You specialize in:
- Systematic debugging approaches
- Error analysis and root cause identification
- Performance profiling and optimization
- Memory leak detection
- Cross-platform debugging
- Debugging tools and techniques

Always provide systematic debugging approaches with clear explanations.""",
                'generation_prompt': """Generate a debugging strategy for: {query}
Consider:
- Systematic approach to problem identification
- Appropriate debugging tools
- Log analysis techniques
- Performance profiling methods
- Root cause analysis
- Prevention strategies""",
                'review_prompt': """Review this debugging approach for: {query}
Check for:
- Systematic methodology
- Appropriate tool selection
- Comprehensive error analysis
- Performance considerations
- Prevention strategies
- Documentation quality"""
            },
            
            DomainType.ML: {
                'system_prompt': """You are a machine learning expert agent. You specialize in:
- Machine learning algorithms and models
- Data preprocessing and feature engineering
- Model evaluation and validation
- Deep learning frameworks (TensorFlow, PyTorch)
- MLOps and model deployment
- Statistical analysis and interpretation

Always provide well-documented ML solutions with proper validation.""",
                'generation_prompt': """Generate a machine learning solution for: {query}
Consider:
- Appropriate algorithm selection
- Data preprocessing requirements
- Feature engineering strategies
- Model validation and evaluation
- Performance metrics
- Deployment considerations""",
                'review_prompt': """Review this ML solution for: {query}
Check for:
- Algorithm appropriateness
- Data preprocessing quality
- Feature engineering effectiveness
- Model validation methodology
- Performance metrics selection
- Deployment readiness"""
            },
            
            DomainType.API: {
                'system_prompt': """You are an API expert agent. You specialize in:
- RESTful API design and development
- API documentation and versioning
- Authentication and authorization
- Rate limiting and throttling
- API testing and monitoring
- Microservices architecture

Always provide well-designed, documented APIs with proper error handling.""",
                'generation_prompt': """Generate an API solution for: {query}
Consider:
- RESTful design principles
- Proper HTTP status codes
- Authentication and security
- Error handling and validation
- Documentation requirements
- Performance and scalability""",
                'review_prompt': """Review this API design for: {query}
Check for:
- RESTful compliance
- Security best practices
- Error handling completeness
- Documentation quality
- Performance considerations
- Scalability design"""
            },
            
            DomainType.GENERAL: {
                'system_prompt': """You are a general-purpose AI agent. You can help with:
- General programming questions
- Problem-solving approaches
- Learning and education
- Code organization and architecture
- Best practices and methodologies
- Cross-domain knowledge

Always provide helpful, well-structured responses with clear explanations.""",
                'generation_prompt': """Generate a solution for: {query}
Consider:
- General best practices
- Clear problem-solving approach
- Appropriate technology selection
- Scalability and maintainability
- Documentation and explanation
- Learning opportunities""",
                'review_prompt': """Review this solution for: {query}
Check for:
- Correctness and completeness
- Best practices compliance
- Clarity and documentation
- Scalability considerations
- Learning value
- Overall quality"""
            }
        }
    
    def get_domain_prompt(self, domain: DomainType, prompt_type: str, query: str = "") -> str:
        """Obtiene un prompt específico del dominio."""
        if domain not in self.domain_prompts:
            domain = DomainType.GENERAL
        
        prompts = self.domain_prompts[domain]
        
        if prompt_type in prompts:
            return prompts[prompt_type].format(query=query)
        else:
            return prompts['system_prompt']
    
    def calculate_domain_expertise(self, agent: Agent) -> Dict[DomainType, DomainExpertise]:
        """Calcula el expertise de un agente en cada dominio."""
        try:
            # Obtener interacciones del agente
            interactions = self.db_manager.get_agent_interactions(agent.id, limit=1000)
            
            # Agrupar por dominio (simplificado - en producción usaría análisis más sofisticado)
            domain_interactions = {}
            
            for interaction in interactions:
                # Determinar dominio basado en el contenido (simplificado)
                domain = self._detect_domain_from_content(interaction.query, interaction.response)
                
                if domain not in domain_interactions:
                    domain_interactions[domain] = []
                domain_interactions[domain].append(interaction)
            
            # Calcular expertise por dominio
            domain_expertise = {}
            
            for domain in DomainType:
                if domain in domain_interactions:
                    domain_ints = domain_interactions[domain]
                    successful_ints = [i for i in domain_ints if i.success]
                    
                    expertise = DomainExpertise(
                        domain=domain,
                        expertise_level=len(successful_ints) / max(1, len(domain_ints)),
                        interactions_count=len(domain_ints),
                        success_rate=len(successful_ints) / max(1, len(domain_ints)),
                        avg_quality_score=sum(i.quality_score for i in successful_ints) / max(1, len(successful_ints)),
                        last_updated=datetime.now()
                    )
                else:
                    expertise = DomainExpertise(
                        domain=domain,
                        expertise_level=0.0,
                        interactions_count=0,
                        success_rate=0.0,
                        avg_quality_score=0.0,
                        last_updated=datetime.now()
                    )
                
                domain_expertise[domain] = expertise
            
            return domain_expertise
            
        except Exception as e:
            logger.error(f"Error calculando expertise del agente {agent.id}: {e}")
            return {}
    
    def _detect_domain_from_content(self, query: str, response: str) -> DomainType:
        """Detecta el dominio basado en el contenido (simplificado)."""
        content = (query + " " + response).lower()
        
        # Palabras clave por dominio
        domain_keywords = {
            DomainType.PYTHON: ['python', 'def ', 'import ', 'class ', 'pandas', 'numpy', 'django', 'flask'],
            DomainType.SQL: ['sql', 'select', 'from ', 'where ', 'join', 'database', 'query'],
            DomainType.JAVASCRIPT: ['javascript', 'js', 'node', 'react', 'function', 'var ', 'let '],
            DomainType.DEBUG: ['error', 'bug', 'debug', 'fix', 'troubleshoot', 'problem'],
            DomainType.ML: ['machine learning', 'ai', 'neural', 'model', 'training', 'tensorflow', 'pytorch'],
            DomainType.API: ['api', 'rest', 'endpoint', 'http', 'request', 'response']
        }
        
        # Contar coincidencias
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            if score > 0:
                domain_scores[domain] = score
        
        # Retornar dominio con mayor score
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return DomainType.GENERAL
    
    def get_agents_by_domain(self, domain: DomainType, min_expertise: float = 0.5) -> List[Agent]:
        """Obtiene agentes con expertise en un dominio específico."""
        try:
            # Obtener todos los agentes activos
            active_agents = self.db_manager.get_agents_by_status(AgentStatus.ACTIVE)
            graduated_agents = self.db_manager.get_agents_by_status(AgentStatus.GRADUATED)
            all_agents = active_agents + graduated_agents
            
            qualified_agents = []
            
            for agent in all_agents:
                # Calcular expertise del agente
                expertise = self.calculate_domain_expertise(agent)
                
                if domain in expertise and expertise[domain].expertise_level >= min_expertise:
                    qualified_agents.append(agent)
            
            # Ordenar por expertise
            qualified_agents.sort(key=lambda a: self.calculate_domain_expertise(a).get(domain, DomainExpertise(domain, 0.0, 0, 0.0, 0.0, datetime.now())).expertise_level, reverse=True)
            
            return qualified_agents
            
        except Exception as e:
            logger.error(f"Error obteniendo agentes por dominio {domain}: {e}")
            return []
    
    def get_domain_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas por dominio."""
        try:
            # Obtener todos los agentes
            all_agents = []
            for status in [AgentStatus.ACTIVE, AgentStatus.GRADUATED, AgentStatus.TRAINING]:
                all_agents.extend(self.db_manager.get_agents_by_status(status))
            
            # Calcular estadísticas por dominio
            domain_stats = {}
            
            for domain in DomainType:
                agents_in_domain = self.get_agents_by_domain(domain, min_expertise=0.1)
                
                if agents_in_domain:
                    expertise_levels = []
                    for agent in agents_in_domain:
                        expertise = self.calculate_domain_expertise(agent)
                        if domain in expertise:
                            expertise_levels.append(expertise[domain].expertise_level)
                    
                    domain_stats[domain.value] = {
                        'total_agents': len(agents_in_domain),
                        'avg_expertise': sum(expertise_levels) / len(expertise_levels),
                        'max_expertise': max(expertise_levels),
                        'min_expertise': min(expertise_levels)
                    }
                else:
                    domain_stats[domain.value] = {
                        'total_agents': 0,
                        'avg_expertise': 0.0,
                        'max_expertise': 0.0,
                        'min_expertise': 0.0
                    }
            
            return domain_stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de dominios: {e}")
            return {}


class CollaborationManager:
    """Gestiona colaboraciones entre agentes."""
    
    def __init__(self, db_manager: DatabaseManager, domain_manager: DomainManager):
        self.db_manager = db_manager
        self.domain_manager = domain_manager
        self.active_collaborations = {}
        
        self.collaboration_stats = {
            'total_requests': 0,
            'accepted_requests': 0,
            'completed_collaborations': 0,
            'successful_collaborations': 0,
            'avg_quality_score': 0.0
        }
        
        logger.info("CollaborationManager inicializado")
    
    def request_collaboration(self, 
                            requester_agent_id: str,
                            query: str,
                            context: str,
                            collaboration_type: CollaborationType,
                            target_domain: Optional[DomainType] = None,
                            priority: float = 0.5) -> Optional[CollaborationRequest]:
        """Solicita colaboración con otro agente."""
        try:
            # Encontrar agente objetivo
            target_agent = self._find_best_collaborator(
                requester_agent_id, query, target_domain, collaboration_type
            )
            
            if not target_agent:
                logger.warning(f"No se encontró colaborador para agente {requester_agent_id}")
                return None
            
            # Crear solicitud de colaboración
            request = CollaborationRequest(
                id=f"collab_{requester_agent_id}_{target_agent.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                requester_agent_id=requester_agent_id,
                target_agent_id=target_agent.id,
                collaboration_type=collaboration_type,
                query=query,
                context=context,
                priority=priority,
                created_at=datetime.now()
            )
            
            # Almacenar solicitud
            self.active_collaborations[request.id] = request
            
            self.collaboration_stats['total_requests'] += 1
            
            logger.info(f"Solicitud de colaboración creada: {request.id}")
            return request
            
        except Exception as e:
            logger.error(f"Error creando solicitud de colaboración: {e}")
            return None
    
    def _find_best_collaborator(self, 
                              requester_agent_id: str,
                              query: str,
                              target_domain: Optional[DomainType],
                              collaboration_type: CollaborationType) -> Optional[Agent]:
        """Encuentra el mejor colaborador para la solicitud."""
        try:
            # Detectar dominio si no se especifica
            if not target_domain:
                target_domain = self.domain_manager._detect_domain_from_content(query, "")
            
            # Obtener agentes candidatos
            candidate_agents = self.domain_manager.get_agents_by_domain(target_domain, min_expertise=0.6)
            
            # Filtrar el agente solicitante
            candidate_agents = [a for a in candidate_agents if a.id != requester_agent_id]
            
            if not candidate_agents:
                # Buscar en dominio general
                candidate_agents = self.domain_manager.get_agents_by_domain(DomainType.GENERAL, min_expertise=0.5)
                candidate_agents = [a for a in candidate_agents if a.id != requester_agent_id]
            
            if not candidate_agents:
                return None
            
            # Seleccionar el mejor candidato
            best_agent = max(candidate_agents, key=lambda a: a.graduation_score)
            
            return best_agent
            
        except Exception as e:
            logger.error(f"Error encontrando colaborador: {e}")
            return None
    
    def process_collaboration(self, 
                            request_id: str,
                            response: str,
                            quality_score: float,
                            execution_time_ms: int) -> Optional[CollaborationResult]:
        """Procesa una colaboración completada."""
        try:
            if request_id not in self.active_collaborations:
                logger.error(f"Solicitud de colaboración {request_id} no encontrada")
                return None
            
            request = self.active_collaborations[request_id]
            
            # Crear resultado
            result = CollaborationResult(
                id=f"result_{request_id}",
                collaboration_request_id=request_id,
                success=quality_score >= 7.0,
                quality_score=quality_score,
                response=response,
                execution_time_ms=execution_time_ms,
                created_at=datetime.now(),
                metadata={
                    'collaboration_type': request.collaboration_type.value,
                    'requester_agent_id': request.requester_agent_id,
                    'target_agent_id': request.target_agent_id
                }
            )
            
            # Actualizar estadísticas
            self.collaboration_stats['completed_collaborations'] += 1
            if result.success:
                self.collaboration_stats['successful_collaborations'] += 1
            
            # Actualizar score promedio
            current_avg = self.collaboration_stats['avg_quality_score']
            total_completed = self.collaboration_stats['completed_collaborations']
            
            self.collaboration_stats['avg_quality_score'] = (
                (current_avg * (total_completed - 1) + quality_score) / total_completed
            )
            
            # Marcar solicitud como completada
            request.status = "completed"
            
            logger.info(f"Colaboración procesada: {request_id}, success={result.success}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando colaboración {request_id}: {e}")
            return None
    
    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de colaboración."""
        return self.collaboration_stats.copy()
    
    def get_active_collaborations(self) -> List[CollaborationRequest]:
        """Retorna colaboraciones activas."""
        return [req for req in self.active_collaborations.values() if req.status == "pending"]


if __name__ == "__main__":
    # Test del DomainSystem
    logging.basicConfig(level=logging.INFO)
    
    from .database import DatabaseManager
    
    db_manager = DatabaseManager()
    domain_manager = DomainManager(db_manager)
    collaboration_manager = CollaborationManager(db_manager, domain_manager)
    
    # Test de prompts por dominio
    for domain in DomainType:
        prompt = domain_manager.get_domain_prompt(domain, 'system_prompt')
        print(f"{domain.value}: {prompt[:100]}...")
    
    # Test de estadísticas de dominio
    stats = domain_manager.get_domain_stats()
    print(f"Estadísticas de dominio: {stats}")
    
    # Test de colaboración
    request = collaboration_manager.request_collaboration(
        requester_agent_id="test_agent_1",
        query="How to optimize Python code performance?",
        context="Performance optimization help",
        collaboration_type=CollaborationType.KNOWLEDGE_SHARING,
        target_domain=DomainType.PYTHON
    )
    
    if request:
        print(f"Solicitud de colaboración creada: {request.id}")
    
    # Mostrar estadísticas
    collab_stats = collaboration_manager.get_collaboration_stats()
    print(f"Estadísticas de colaboración: {collab_stats}")
