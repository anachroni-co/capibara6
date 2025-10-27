#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Schema and Management for Persistent Agent Memory.
"""

import logging
import sqlite3
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Estado del agente."""
    TRAINING = "training"
    ACTIVE = "active"
    GRADUATED = "graduated"
    RETIRED = "retired"
    FAILED = "failed"


class MemoryType(Enum):
    """Tipo de memoria."""
    CONVERSATION = "conversation"
    KNOWLEDGE = "knowledge"
    SKILL = "skill"
    EXPERIENCE = "experience"
    PATTERN = "pattern"


@dataclass
class Agent:
    """Representa un agente persistente."""
    id: str
    domain: str
    status: AgentStatus
    created_at: datetime
    last_updated: datetime
    total_interactions: int
    success_rate: float
    graduation_score: float
    memory_tokens: int
    max_memory_tokens: int = 128000  # 128K tokens
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentMemory:
    """Representa una entrada de memoria del agente."""
    id: str
    agent_id: str
    memory_type: MemoryType
    content: str
    tokens: int
    importance_score: float
    created_at: datetime
    last_accessed: datetime
    access_count: int
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentInteraction:
    """Representa una interacción del agente."""
    id: str
    agent_id: str
    query: str
    response: str
    success: bool
    quality_score: float
    execution_time_ms: int
    corrections_applied: int
    context_used: str
    created_at: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DatabaseManager:
    """Gestiona la base de datos de agentes persistentes."""
    
    def __init__(self, db_path: str = "backend/data/agents.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
        
        logger.info(f"DatabaseManager inicializado: {db_path}")
    
    def _ensure_directory(self):
        """Asegura que el directorio de la base de datos existe."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        """Inicializa la base de datos con el esquema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de agentes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    domain TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    last_updated TIMESTAMP NOT NULL,
                    total_interactions INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    graduation_score REAL DEFAULT 0.0,
                    memory_tokens INTEGER DEFAULT 0,
                    max_memory_tokens INTEGER DEFAULT 128000,
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            # Tabla de memorias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_memories (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tokens INTEGER NOT NULL,
                    importance_score REAL NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    last_accessed TIMESTAMP NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (agent_id) REFERENCES agents (id)
                )
            """)
            
            # Tabla de interacciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_interactions (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    quality_score REAL NOT NULL,
                    execution_time_ms INTEGER NOT NULL,
                    corrections_applied INTEGER DEFAULT 0,
                    context_used TEXT,
                    created_at TIMESTAMP NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (agent_id) REFERENCES agents (id)
                )
            """)
            
            # Tabla de graduaciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_graduations (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    graduation_date TIMESTAMP NOT NULL,
                    final_score REAL NOT NULL,
                    interactions_count INTEGER NOT NULL,
                    success_rate REAL NOT NULL,
                    memory_compression_ratio REAL,
                    playbook_contributions INTEGER DEFAULT 0,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (agent_id) REFERENCES agents (id)
                )
            """)
            
            # Tabla de colaboraciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_collaborations (
                    id TEXT PRIMARY KEY,
                    primary_agent_id TEXT NOT NULL,
                    secondary_agent_id TEXT NOT NULL,
                    collaboration_type TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    quality_score REAL NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (primary_agent_id) REFERENCES agents (id),
                    FOREIGN KEY (secondary_agent_id) REFERENCES agents (id)
                )
            """)
            
            # Índices para optimización
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_domain ON agents (domain)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_status ON agents (status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_graduation_score ON agents (graduation_score)")
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_agent_id ON agent_memories (agent_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_type ON agent_memories (memory_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_importance ON agent_memories (importance_score)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_accessed ON agent_memories (last_accessed)")
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_agent_id ON agent_interactions (agent_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_success ON agent_interactions (success)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_created ON agent_interactions (created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_quality ON agent_interactions (quality_score)")
            
            conn.commit()
            logger.info("Esquema de base de datos inicializado")
    
    def create_agent(self, agent: Agent) -> bool:
        """Crea un nuevo agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO agents (
                        id, domain, status, created_at, last_updated,
                        total_interactions, success_rate, graduation_score,
                        memory_tokens, max_memory_tokens, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    agent.id, agent.domain, agent.status.value,
                    agent.created_at.isoformat(), agent.last_updated.isoformat(),
                    agent.total_interactions, agent.success_rate, agent.graduation_score,
                    agent.memory_tokens, agent.max_memory_tokens, json.dumps(agent.metadata)
                ))
                conn.commit()
                logger.info(f"Agente creado: {agent.id} en dominio {agent.domain}")
                return True
        except Exception as e:
            logger.error(f"Error creando agente {agent.id}: {e}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Obtiene un agente por ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
                row = cursor.fetchone()
                
                if row:
                    return Agent(
                        id=row[0],
                        domain=row[1],
                        status=AgentStatus(row[2]),
                        created_at=datetime.fromisoformat(row[3]),
                        last_updated=datetime.fromisoformat(row[4]),
                        total_interactions=row[5],
                        success_rate=row[6],
                        graduation_score=row[7],
                        memory_tokens=row[8],
                        max_memory_tokens=row[9],
                        metadata=json.loads(row[10])
                    )
                return None
        except Exception as e:
            logger.error(f"Error obteniendo agente {agent_id}: {e}")
            return None
    
    def update_agent(self, agent: Agent) -> bool:
        """Actualiza un agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE agents SET
                        status = ?, last_updated = ?, total_interactions = ?,
                        success_rate = ?, graduation_score = ?, memory_tokens = ?,
                        metadata = ?
                    WHERE id = ?
                """, (
                    agent.status.value, agent.last_updated.isoformat(),
                    agent.total_interactions, agent.success_rate,
                    agent.graduation_score, agent.memory_tokens,
                    json.dumps(agent.metadata), agent.id
                ))
                conn.commit()
                logger.debug(f"Agente actualizado: {agent.id}")
                return True
        except Exception as e:
            logger.error(f"Error actualizando agente {agent.id}: {e}")
            return False
    
    def get_agents_by_domain(self, domain: str) -> List[Agent]:
        """Obtiene agentes por dominio."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM agents WHERE domain = ? ORDER BY graduation_score DESC", (domain,))
                rows = cursor.fetchall()
                
                agents = []
                for row in rows:
                    agents.append(Agent(
                        id=row[0],
                        domain=row[1],
                        status=AgentStatus(row[2]),
                        created_at=datetime.fromisoformat(row[3]),
                        last_updated=datetime.fromisoformat(row[4]),
                        total_interactions=row[5],
                        success_rate=row[6],
                        graduation_score=row[7],
                        memory_tokens=row[8],
                        max_memory_tokens=row[9],
                        metadata=json.loads(row[10])
                    ))
                return agents
        except Exception as e:
            logger.error(f"Error obteniendo agentes del dominio {domain}: {e}")
            return []
    
    def get_agents_by_status(self, status: AgentStatus) -> List[Agent]:
        """Obtiene agentes por estado."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM agents WHERE status = ? ORDER BY graduation_score DESC", (status.value,))
                rows = cursor.fetchall()
                
                agents = []
                for row in rows:
                    agents.append(Agent(
                        id=row[0],
                        domain=row[1],
                        status=AgentStatus(row[2]),
                        created_at=datetime.fromisoformat(row[3]),
                        last_updated=datetime.fromisoformat(row[4]),
                        total_interactions=row[5],
                        success_rate=row[6],
                        graduation_score=row[7],
                        memory_tokens=row[8],
                        max_memory_tokens=row[9],
                        metadata=json.loads(row[10])
                    ))
                return agents
        except Exception as e:
            logger.error(f"Error obteniendo agentes con estado {status}: {e}")
            return []
    
    def add_memory(self, memory: AgentMemory) -> bool:
        """Agrega una memoria al agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO agent_memories (
                        id, agent_id, memory_type, content, tokens,
                        importance_score, created_at, last_accessed,
                        access_count, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    memory.id, memory.agent_id, memory.memory_type.value,
                    memory.content, memory.tokens, memory.importance_score,
                    memory.created_at.isoformat(), memory.last_accessed.isoformat(),
                    memory.access_count, json.dumps(memory.metadata)
                ))
                conn.commit()
                logger.debug(f"Memoria agregada: {memory.id} para agente {memory.agent_id}")
                return True
        except Exception as e:
            logger.error(f"Error agregando memoria {memory.id}: {e}")
            return False
    
    def get_agent_memories(self, agent_id: str, memory_type: Optional[MemoryType] = None) -> List[AgentMemory]:
        """Obtiene memorias de un agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute("""
                        SELECT * FROM agent_memories 
                        WHERE agent_id = ? AND memory_type = ?
                        ORDER BY importance_score DESC, last_accessed DESC
                    """, (agent_id, memory_type.value))
                else:
                    cursor.execute("""
                        SELECT * FROM agent_memories 
                        WHERE agent_id = ?
                        ORDER BY importance_score DESC, last_accessed DESC
                    """, (agent_id,))
                
                rows = cursor.fetchall()
                
                memories = []
                for row in rows:
                    memories.append(AgentMemory(
                        id=row[0],
                        agent_id=row[1],
                        memory_type=MemoryType(row[2]),
                        content=row[3],
                        tokens=row[4],
                        importance_score=row[5],
                        created_at=datetime.fromisoformat(row[6]),
                        last_accessed=datetime.fromisoformat(row[7]),
                        access_count=row[8],
                        metadata=json.loads(row[9])
                    ))
                return memories
        except Exception as e:
            logger.error(f"Error obteniendo memorias del agente {agent_id}: {e}")
            return []
    
    def add_interaction(self, interaction: AgentInteraction) -> bool:
        """Agrega una interacción del agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO agent_interactions (
                        id, agent_id, query, response, success,
                        quality_score, execution_time_ms, corrections_applied,
                        context_used, created_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction.id, interaction.agent_id, interaction.query,
                    interaction.response, interaction.success, interaction.quality_score,
                    interaction.execution_time_ms, interaction.corrections_applied,
                    interaction.context_used, interaction.created_at.isoformat(),
                    json.dumps(interaction.metadata)
                ))
                conn.commit()
                logger.debug(f"Interacción agregada: {interaction.id} para agente {interaction.agent_id}")
                return True
        except Exception as e:
            logger.error(f"Error agregando interacción {interaction.id}: {e}")
            return False
    
    def get_agent_interactions(self, agent_id: str, limit: int = 100) -> List[AgentInteraction]:
        """Obtiene interacciones de un agente."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM agent_interactions 
                    WHERE agent_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (agent_id, limit))
                
                rows = cursor.fetchall()
                
                interactions = []
                for row in rows:
                    interactions.append(AgentInteraction(
                        id=row[0],
                        agent_id=row[1],
                        query=row[2],
                        response=row[3],
                        success=bool(row[4]),
                        quality_score=row[5],
                        execution_time_ms=row[6],
                        corrections_applied=row[7],
                        context_used=row[8],
                        created_at=datetime.fromisoformat(row[9]),
                        metadata=json.loads(row[10])
                    ))
                return interactions
        except Exception as e:
            logger.error(f"Error obteniendo interacciones del agente {agent_id}: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de la base de datos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Estadísticas de agentes
                cursor.execute("SELECT COUNT(*) FROM agents")
                total_agents = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'graduated'")
                graduated_agents = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(success_rate) FROM agents")
                avg_success_rate = cursor.fetchone()[0] or 0.0
                
                cursor.execute("SELECT AVG(graduation_score) FROM agents WHERE status = 'graduated'")
                avg_graduation_score = cursor.fetchone()[0] or 0.0
                
                # Estadísticas de memorias
                cursor.execute("SELECT COUNT(*) FROM agent_memories")
                total_memories = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(tokens) FROM agent_memories")
                total_memory_tokens = cursor.fetchone()[0] or 0
                
                # Estadísticas de interacciones
                cursor.execute("SELECT COUNT(*) FROM agent_interactions")
                total_interactions = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM agent_interactions WHERE success = 1")
                successful_interactions = cursor.fetchone()[0]
                
                return {
                    'agents': {
                        'total': total_agents,
                        'graduated': graduated_agents,
                        'avg_success_rate': avg_success_rate,
                        'avg_graduation_score': avg_graduation_score
                    },
                    'memories': {
                        'total': total_memories,
                        'total_tokens': total_memory_tokens
                    },
                    'interactions': {
                        'total': total_interactions,
                        'successful': successful_interactions,
                        'success_rate': successful_interactions / max(1, total_interactions)
                    }
                }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de la base de datos: {e}")
            return {}


if __name__ == "__main__":
    # Test del DatabaseManager
    logging.basicConfig(level=logging.INFO)
    
    db_manager = DatabaseManager()
    
    # Crear agente de prueba
    agent = Agent(
        id="test_agent_001",
        domain="python",
        status=AgentStatus.TRAINING,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        total_interactions=0,
        success_rate=0.0,
        graduation_score=0.0,
        memory_tokens=0
    )
    
    # Crear agente
    success = db_manager.create_agent(agent)
    print(f"Agente creado: {success}")
    
    # Obtener agente
    retrieved_agent = db_manager.get_agent("test_agent_001")
    print(f"Agente obtenido: {retrieved_agent.id if retrieved_agent else 'None'}")
    
    # Mostrar estadísticas
    stats = db_manager.get_database_stats()
    print(f"Estadísticas: {stats}")
