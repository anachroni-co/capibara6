#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Manager - Gestión inteligente de memoria de agentes con compresión.
"""

import logging
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import re

from .database import DatabaseManager, Agent, AgentMemory, MemoryType, AgentStatus

logger = logging.getLogger(__name__)


class MemoryCompressor:
    """Compresor inteligente de memoria."""
    
    def __init__(self, max_tokens: int = 128000):
        self.max_tokens = max_tokens
        self.compression_stats = {
            'total_compressions': 0,
            'tokens_saved': 0,
            'memories_merged': 0,
            'memories_pruned': 0
        }
        
        logger.info(f"MemoryCompressor inicializado con max_tokens={max_tokens}")
    
    def compress_memories(self, memories: List[AgentMemory]) -> List[AgentMemory]:
        """Comprime memorias para mantener el límite de tokens."""
        if not memories:
            return memories
        
        # Calcular tokens totales
        total_tokens = sum(memory.tokens for memory in memories)
        
        if total_tokens <= self.max_tokens:
            return memories
        
        logger.info(f"Compresión necesaria: {total_tokens} tokens > {self.max_tokens}")
        
        # Ordenar por importancia y acceso
        sorted_memories = sorted(memories, key=lambda m: (
            m.importance_score,
            m.last_accessed,
            m.access_count
        ), reverse=True)
        
        compressed_memories = []
        current_tokens = 0
        
        # Mantener memorias más importantes
        for memory in sorted_memories:
            if current_tokens + memory.tokens <= self.max_tokens:
                compressed_memories.append(memory)
                current_tokens += memory.tokens
            else:
                # Intentar comprimir memoria
                compressed = self._compress_single_memory(memory)
                if compressed and current_tokens + compressed.tokens <= self.max_tokens:
                    compressed_memories.append(compressed)
                    current_tokens += compressed.tokens
                    self.compression_stats['memories_merged'] += 1
                else:
                    # Prunear memoria menos importante
                    self.compression_stats['memories_pruned'] += 1
        
        tokens_saved = total_tokens - current_tokens
        self.compression_stats['tokens_saved'] += tokens_saved
        self.compression_stats['total_compressions'] += 1
        
        logger.info(f"Compresión completada: {len(compressed_memories)} memorias, "
                   f"{tokens_saved} tokens ahorrados")
        
        return compressed_memories
    
    def _compress_single_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime una memoria individual."""
        try:
            # Estrategias de compresión por tipo
            if memory.memory_type == MemoryType.CONVERSATION:
                return self._compress_conversation_memory(memory)
            elif memory.memory_type == MemoryType.KNOWLEDGE:
                return self._compress_knowledge_memory(memory)
            elif memory.memory_type == MemoryType.SKILL:
                return self._compress_skill_memory(memory)
            elif memory.memory_type == MemoryType.EXPERIENCE:
                return self._compress_experience_memory(memory)
            elif memory.memory_type == MemoryType.PATTERN:
                return self._compress_pattern_memory(memory)
            
            return None
        except Exception as e:
            logger.error(f"Error comprimiendo memoria {memory.id}: {e}")
            return None
    
    def _compress_conversation_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime memoria de conversación."""
        # Extraer puntos clave de la conversación
        content = memory.content
        
        # Buscar patrones importantes
        important_patterns = [
            r'error[:\s]+([^.\n]+)',
            r'solution[:\s]+([^.\n]+)',
            r'result[:\s]+([^.\n]+)',
            r'key[:\s]+([^.\n]+)',
            r'important[:\s]+([^.\n]+)'
        ]
        
        key_points = []
        for pattern in important_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            key_points.extend(matches)
        
        if key_points:
            compressed_content = "Key points: " + "; ".join(key_points[:5])  # Máximo 5 puntos
            compressed_tokens = len(compressed_content.split()) * 1.3  # Aproximación
            
            return AgentMemory(
                id=memory.id + "_compressed",
                agent_id=memory.agent_id,
                memory_type=memory.memory_type,
                content=compressed_content,
                tokens=int(compressed_tokens),
                importance_score=memory.importance_score,
                created_at=memory.created_at,
                last_accessed=datetime.now(),
                access_count=memory.access_count,
                metadata={**memory.metadata, 'compressed': True, 'original_tokens': memory.tokens}
            )
        
        return None
    
    def _compress_knowledge_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime memoria de conocimiento."""
        content = memory.content
        
        # Extraer definiciones y conceptos clave
        sentences = content.split('.')
        key_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Filtrar oraciones muy cortas
                # Priorizar oraciones con palabras clave
                if any(keyword in sentence.lower() for keyword in ['define', 'concept', 'principle', 'rule', 'method']):
                    key_sentences.append(sentence)
        
        if key_sentences:
            compressed_content = ". ".join(key_sentences[:3]) + "."  # Máximo 3 oraciones
            compressed_tokens = len(compressed_content.split()) * 1.3
            
            return AgentMemory(
                id=memory.id + "_compressed",
                agent_id=memory.agent_id,
                memory_type=memory.memory_type,
                content=compressed_content,
                tokens=int(compressed_tokens),
                importance_score=memory.importance_score,
                created_at=memory.created_at,
                last_accessed=datetime.now(),
                access_count=memory.access_count,
                metadata={**memory.metadata, 'compressed': True, 'original_tokens': memory.tokens}
            )
        
        return None
    
    def _compress_skill_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime memoria de habilidades."""
        content = memory.content
        
        # Extraer pasos y técnicas
        steps = re.findall(r'\d+\.\s*([^.\n]+)', content)
        techniques = re.findall(r'technique[:\s]+([^.\n]+)', content, re.IGNORECASE)
        
        compressed_parts = []
        if steps:
            compressed_parts.append("Steps: " + "; ".join(steps[:3]))
        if techniques:
            compressed_parts.append("Techniques: " + "; ".join(techniques[:2]))
        
        if compressed_parts:
            compressed_content = " | ".join(compressed_parts)
            compressed_tokens = len(compressed_content.split()) * 1.3
            
            return AgentMemory(
                id=memory.id + "_compressed",
                agent_id=memory.agent_id,
                memory_type=memory.memory_type,
                content=compressed_content,
                tokens=int(compressed_tokens),
                importance_score=memory.importance_score,
                created_at=memory.created_at,
                last_accessed=datetime.now(),
                access_count=memory.access_count,
                metadata={**memory.metadata, 'compressed': True, 'original_tokens': memory.tokens}
            )
        
        return None
    
    def _compress_experience_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime memoria de experiencia."""
        content = memory.content
        
        # Extraer resultados y lecciones aprendidas
        results = re.findall(r'result[:\s]+([^.\n]+)', content, re.IGNORECASE)
        lessons = re.findall(r'learn[:\s]+([^.\n]+)', content, re.IGNORECASE)
        
        compressed_parts = []
        if results:
            compressed_parts.append("Results: " + "; ".join(results[:2]))
        if lessons:
            compressed_parts.append("Lessons: " + "; ".join(lessons[:2]))
        
        if compressed_parts:
            compressed_content = " | ".join(compressed_parts)
            compressed_tokens = len(compressed_content.split()) * 1.3
            
            return AgentMemory(
                id=memory.id + "_compressed",
                agent_id=memory.agent_id,
                memory_type=memory.memory_type,
                content=compressed_content,
                tokens=int(compressed_tokens),
                importance_score=memory.importance_score,
                created_at=memory.created_at,
                last_accessed=datetime.now(),
                access_count=memory.access_count,
                metadata={**memory.metadata, 'compressed': True, 'original_tokens': memory.tokens}
            )
        
        return None
    
    def _compress_pattern_memory(self, memory: AgentMemory) -> Optional[AgentMemory]:
        """Comprime memoria de patrones."""
        content = memory.content
        
        # Extraer patrones y ejemplos
        patterns = re.findall(r'pattern[:\s]+([^.\n]+)', content, re.IGNORECASE)
        examples = re.findall(r'example[:\s]+([^.\n]+)', content, re.IGNORECASE)
        
        compressed_parts = []
        if patterns:
            compressed_parts.append("Patterns: " + "; ".join(patterns[:2]))
        if examples:
            compressed_parts.append("Examples: " + "; ".join(examples[:1]))
        
        if compressed_parts:
            compressed_content = " | ".join(compressed_parts)
            compressed_tokens = len(compressed_content.split()) * 1.3
            
            return AgentMemory(
                id=memory.id + "_compressed",
                agent_id=memory.agent_id,
                memory_type=memory.memory_type,
                content=compressed_content,
                tokens=int(compressed_tokens),
                importance_score=memory.importance_score,
                created_at=memory.created_at,
                last_accessed=datetime.now(),
                access_count=memory.access_count,
                metadata={**memory.metadata, 'compressed': True, 'original_tokens': memory.tokens}
            )
        
        return None
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de compresión."""
        return self.compression_stats.copy()


class MemoryManager:
    """Gestiona la memoria de agentes con compresión inteligente."""
    
    def __init__(self, db_manager: DatabaseManager, max_tokens: int = 128000):
        self.db_manager = db_manager
        self.compressor = MemoryCompressor(max_tokens)
        self.memory_cache = {}  # Cache de memorias por agente
        
        self.manager_stats = {
            'total_memories_added': 0,
            'total_memories_retrieved': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'compressions_performed': 0
        }
        
        logger.info(f"MemoryManager inicializado con max_tokens={max_tokens}")
    
    def add_memory(self, 
                   agent_id: str,
                   memory_type: MemoryType,
                   content: str,
                   importance_score: float = 0.5,
                   metadata: Dict[str, Any] = None) -> bool:
        """Agrega una memoria al agente."""
        try:
            # Calcular tokens (aproximación simple)
            tokens = len(content.split()) * 1.3
            
            # Crear memoria
            memory = AgentMemory(
                id=self._generate_memory_id(agent_id, content),
                agent_id=agent_id,
                memory_type=memory_type,
                content=content,
                tokens=int(tokens),
                importance_score=importance_score,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=0,
                metadata=metadata or {}
            )
            
            # Agregar a la base de datos
            success = self.db_manager.add_memory(memory)
            
            if success:
                # Invalidar cache
                if agent_id in self.memory_cache:
                    del self.memory_cache[agent_id]
                
                # Verificar límite de tokens y comprimir si es necesario
                self._check_and_compress_memory(agent_id)
                
                self.manager_stats['total_memories_added'] += 1
                logger.info(f"Memoria agregada: {memory.id} para agente {agent_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error agregando memoria al agente {agent_id}: {e}")
            return False
    
    def get_agent_memories(self, 
                          agent_id: str, 
                          memory_type: Optional[MemoryType] = None,
                          limit: int = 50) -> List[AgentMemory]:
        """Obtiene memorias de un agente."""
        try:
            # Verificar cache
            cache_key = f"{agent_id}_{memory_type.value if memory_type else 'all'}_{limit}"
            if cache_key in self.memory_cache:
                self.manager_stats['cache_hits'] += 1
                return self.memory_cache[cache_key]
            
            self.manager_stats['cache_misses'] += 1
            
            # Obtener de la base de datos
            memories = self.db_manager.get_agent_memories(agent_id, memory_type)
            
            # Limitar resultados
            if limit > 0:
                memories = memories[:limit]
            
            # Actualizar acceso
            for memory in memories:
                memory.last_accessed = datetime.now()
                memory.access_count += 1
            
            # Cachear resultados
            self.memory_cache[cache_key] = memories
            
            self.manager_stats['total_memories_retrieved'] += len(memories)
            
            return memories
            
        except Exception as e:
            logger.error(f"Error obteniendo memorias del agente {agent_id}: {e}")
            return []
    
    def get_relevant_memories(self, 
                            agent_id: str,
                            query: str,
                            memory_type: Optional[MemoryType] = None,
                            limit: int = 10) -> List[AgentMemory]:
        """Obtiene memorias relevantes para una query."""
        try:
            memories = self.get_agent_memories(agent_id, memory_type, limit * 2)
            
            # Filtrar por relevancia (implementación simple)
            relevant_memories = []
            query_words = set(query.lower().split())
            
            for memory in memories:
                content_words = set(memory.content.lower().split())
                overlap = len(query_words.intersection(content_words))
                
                if overlap > 0:
                    # Calcular score de relevancia
                    relevance_score = overlap / len(query_words)
                    memory.metadata['relevance_score'] = relevance_score
                    relevant_memories.append(memory)
            
            # Ordenar por relevancia y importancia
            relevant_memories.sort(key=lambda m: (
                m.metadata.get('relevance_score', 0),
                m.importance_score
            ), reverse=True)
            
            return relevant_memories[:limit]
            
        except Exception as e:
            logger.error(f"Error obteniendo memorias relevantes para agente {agent_id}: {e}")
            return []
    
    def _check_and_compress_memory(self, agent_id: str):
        """Verifica y comprime memoria si excede el límite."""
        try:
            agent = self.db_manager.get_agent(agent_id)
            if not agent:
                return
            
            memories = self.db_manager.get_agent_memories(agent_id)
            total_tokens = sum(memory.tokens for memory in memories)
            
            if total_tokens > agent.max_memory_tokens:
                logger.info(f"Compresión necesaria para agente {agent_id}: {total_tokens} tokens")
                
                # Comprimir memorias
                compressed_memories = self.compressor.compress_memories(memories)
                
                # Actualizar en la base de datos (implementación simplificada)
                new_total_tokens = sum(memory.tokens for memory in compressed_memories)
                agent.memory_tokens = new_total_tokens
                agent.last_updated = datetime.now()
                
                self.db_manager.update_agent(agent)
                self.manager_stats['compressions_performed'] += 1
                
                logger.info(f"Compresión completada para agente {agent_id}: {new_total_tokens} tokens")
                
        except Exception as e:
            logger.error(f"Error comprimiendo memoria del agente {agent_id}: {e}")
    
    def _generate_memory_id(self, agent_id: str, content: str) -> str:
        """Genera un ID único para la memoria."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"mem_{agent_id}_{timestamp}_{content_hash}"
    
    def clear_cache(self, agent_id: Optional[str] = None):
        """Limpia el cache de memorias."""
        if agent_id:
            # Limpiar cache específico del agente
            keys_to_remove = [key for key in self.memory_cache.keys() if key.startswith(agent_id)]
            for key in keys_to_remove:
                del self.memory_cache[key]
        else:
            # Limpiar todo el cache
            self.memory_cache.clear()
        
        logger.info(f"Cache limpiado para agente: {agent_id or 'todos'}")
    
    def get_manager_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del manager."""
        return {
            'manager_stats': self.manager_stats,
            'compressor_stats': self.compressor.get_compression_stats(),
            'cache_size': len(self.memory_cache)
        }


if __name__ == "__main__":
    # Test del MemoryManager
    logging.basicConfig(level=logging.INFO)
    
    from .database import DatabaseManager
    
    db_manager = DatabaseManager()
    memory_manager = MemoryManager(db_manager)
    
    # Crear agente de prueba
    from .database import Agent, AgentStatus
    agent = Agent(
        id="test_agent_memory",
        domain="python",
        status=AgentStatus.TRAINING,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        total_interactions=0,
        success_rate=0.0,
        graduation_score=0.0,
        memory_tokens=0
    )
    
    db_manager.create_agent(agent)
    
    # Agregar memorias
    memory_manager.add_memory(
        agent_id="test_agent_memory",
        memory_type=MemoryType.CONVERSATION,
        content="User asked about Python functions. Explained def keyword, parameters, and return statements. User understood the concept.",
        importance_score=0.8
    )
    
    memory_manager.add_memory(
        agent_id="test_agent_memory",
        memory_type=MemoryType.KNOWLEDGE,
        content="Python functions are defined using the 'def' keyword followed by the function name and parameters. They can return values using the 'return' statement.",
        importance_score=0.9
    )
    
    # Obtener memorias
    memories = memory_manager.get_agent_memories("test_agent_memory")
    print(f"Memorias obtenidas: {len(memories)}")
    
    # Obtener memorias relevantes
    relevant = memory_manager.get_relevant_memories("test_agent_memory", "Python functions")
    print(f"Memorias relevantes: {len(relevant)}")
    
    # Mostrar estadísticas
    stats = memory_manager.get_manager_stats()
    print(f"Estadísticas: {stats}")
