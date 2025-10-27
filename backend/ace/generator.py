#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACE Generator - Construye contexto evolutivo basado en playbooks.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

from .playbook import Playbook, PlaybookManager, PlaybookPattern

logger = logging.getLogger(__name__)


class ACEGenerator:
    """Generador de contexto evolutivo basado en playbooks."""
    
    def __init__(self, 
                 playbooks_dir: str = "backend/data/playbooks",
                 max_context_tokens: int = 4000,
                 similarity_threshold: float = 0.3):
        self.playbook_manager = PlaybookManager(playbooks_dir)
        self.max_context_tokens = max_context_tokens
        self.similarity_threshold = similarity_threshold
        self.generation_stats = {
            'total_generations': 0,
            'successful_generations': 0,
            'patterns_used': 0,
            'avg_context_length': 0.0
        }
        logger.info(f"ACEGenerator inicializado con max_tokens={max_context_tokens}")
    
    def generate_context(self, 
                        query: str, 
                        history: List[Dict[str, Any]] = None,
                        domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Genera contexto evolutivo usando playbooks.
        
        Args:
            query: La query del usuario
            history: Historial de conversaciones
            domain: Dominio específico (opcional)
            
        Returns:
            Dict con contexto generado y metadata
        """
        start_time = datetime.now()
        logger.debug(f"Generando contexto para query: '{query[:100]}...'")
        
        try:
            # 1. Determinar dominio si no se especifica
            if not domain:
                domain = self._detect_domain(query)
            
            # 2. Obtener playbook del dominio
            playbook = self._get_or_create_playbook(domain)
            
            # 3. Encontrar patrones relevantes
            relevant_patterns = self._find_relevant_patterns(query, playbook)
            
            # 4. Construir contexto
            context = self._build_context_from_patterns(relevant_patterns, query, history)
            
            # 5. Actualizar estadísticas
            self._update_generation_stats(context, len(relevant_patterns))
            
            generation_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = {
                'context': context,
                'domain': domain,
                'patterns_used': len(relevant_patterns),
                'context_tokens': self._estimate_tokens(context),
                'generation_time_ms': generation_time,
                'playbook_id': playbook.id,
                'success': True
            }
            
            logger.info(f"Contexto generado exitosamente: {len(relevant_patterns)} patrones, "
                       f"{result['context_tokens']} tokens, {generation_time:.1f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generando contexto: {e}")
            return {
                'context': "",
                'domain': domain or 'general',
                'patterns_used': 0,
                'context_tokens': 0,
                'generation_time_ms': (datetime.now() - start_time).total_seconds() * 1000,
                'playbook_id': None,
                'success': False,
                'error': str(e)
            }
    
    def _detect_domain(self, query: str) -> str:
        """Detecta el dominio de la query."""
        query_lower = query.lower()
        
        # Mapeo de palabras clave a dominios
        domain_keywords = {
            'python': ['python', 'def', 'import', 'class', 'function', 'django', 'flask'],
            'sql': ['sql', 'select', 'from', 'where', 'join', 'database', 'query'],
            'javascript': ['javascript', 'js', 'node', 'react', 'function', 'var', 'let'],
            'debug': ['error', 'bug', 'debug', 'fix', 'troubleshoot', 'problem'],
            'ml': ['machine learning', 'ai', 'neural', 'model', 'training', 'tensorflow'],
            'api': ['api', 'rest', 'endpoint', 'http', 'request', 'response']
        }
        
        # Contar coincidencias por dominio
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                domain_scores[domain] = score
        
        # Retornar dominio con mayor score, o 'general' si no hay coincidencias
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
    def _get_or_create_playbook(self, domain: str) -> Playbook:
        """Obtiene o crea un playbook para el dominio."""
        playbook = self.playbook_manager.get_playbook_by_domain(domain)
        
        if not playbook:
            playbook = self.playbook_manager.create_playbook(domain)
            logger.info(f"Nuevo playbook creado para dominio: {domain}")
        
        return playbook
    
    def _find_relevant_patterns(self, query: str, playbook: Playbook) -> List[PlaybookPattern]:
        """Encuentra patrones relevantes para la query."""
        # Obtener patrones que coincidan
        matching_patterns = playbook.find_matching_patterns(query, max_patterns=10)
        
        # Filtrar por umbral de similitud (implementación simple)
        relevant_patterns = []
        for pattern in matching_patterns:
            similarity = self._calculate_similarity(query, pattern.query_pattern)
            if similarity >= self.similarity_threshold:
                relevant_patterns.append(pattern)
        
        # Ordenar por tasa de éxito y relevancia
        relevant_patterns.sort(key=lambda p: (p.get_success_rate(), self._calculate_similarity(query, p.query_pattern)), reverse=True)
        
        logger.debug(f"Encontrados {len(relevant_patterns)} patrones relevantes de {len(matching_patterns)} coincidencias")
        return relevant_patterns
    
    def _calculate_similarity(self, query: str, pattern: str) -> float:
        """Calcula similitud simple entre query y patrón."""
        # Implementación simple basada en palabras comunes
        # En una implementación real, usaríamos embeddings
        query_words = set(query.lower().split())
        pattern_words = set(pattern.lower().split())
        
        if not query_words or not pattern_words:
            return 0.0
        
        intersection = query_words.intersection(pattern_words)
        union = query_words.union(pattern_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _build_context_from_patterns(self, 
                                   patterns: List[PlaybookPattern], 
                                   query: str,
                                   history: List[Dict[str, Any]] = None) -> str:
        """Construye contexto a partir de patrones relevantes."""
        context_parts = []
        current_tokens = 0
        
        # 1. Agregar contexto de patrones
        for pattern in patterns:
            pattern_context = self._format_pattern_context(pattern, query)
            pattern_tokens = self._estimate_tokens(pattern_context)
            
            if current_tokens + pattern_tokens <= self.max_context_tokens:
                context_parts.append(pattern_context)
                current_tokens += pattern_tokens
            else:
                # Truncar si excede límite
                remaining_tokens = self.max_context_tokens - current_tokens
                if remaining_tokens > 100:  # Solo si queda espacio significativo
                    truncated_context = self._truncate_to_tokens(pattern_context, remaining_tokens)
                    context_parts.append(truncated_context)
                break
        
        # 2. Agregar contexto histórico si hay espacio
        if history and current_tokens < self.max_context_tokens * 0.8:
            historical_context = self._build_historical_context(history)
            historical_tokens = self._estimate_tokens(historical_context)
            
            if current_tokens + historical_tokens <= self.max_context_tokens:
                context_parts.append(historical_context)
        
        # 3. Combinar contexto
        full_context = "\n\n".join(context_parts)
        
        logger.debug(f"Contexto construido: {len(context_parts)} partes, {current_tokens} tokens")
        return full_context
    
    def _format_pattern_context(self, pattern: PlaybookPattern, query: str) -> str:
        """Formatea el contexto de un patrón."""
        # Personalizar el template basado en la query
        context = pattern.context_template
        
        # Reemplazar placeholders si existen
        context = context.replace("{query}", query)
        context = context.replace("{domain}", "programming")  # Simplificado
        
        # Agregar metadata del patrón
        success_rate = pattern.get_success_rate()
        metadata = f"[Patrón con {success_rate:.1%} de éxito, usado {pattern.helpful_count + pattern.harmful_count} veces]"
        
        return f"{metadata}\n{context}"
    
    def _build_historical_context(self, history: List[Dict[str, Any]]) -> str:
        """Construye contexto histórico."""
        if not history:
            return ""
        
        # Tomar las últimas 3 conversaciones
        recent_history = history[-3:]
        
        context_parts = ["[Contexto Histórico]"]
        for entry in recent_history:
            if 'query' in entry and 'response' in entry:
                context_parts.append(f"Q: {entry['query']}")
                context_parts.append(f"A: {entry['response'][:200]}...")
        
        return "\n".join(context_parts)
    
    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Trunca texto a un número máximo de tokens."""
        words = text.split()
        if len(words) <= max_tokens:
            return text
        
        truncated_words = words[:max_tokens]
        return " ".join(truncated_words) + "..."
    
    def _estimate_tokens(self, text: str) -> int:
        """Estima el número de tokens en un texto."""
        # Aproximación simple: 1 token ≈ 4 caracteres
        return len(text) // 4
    
    def _update_generation_stats(self, context: str, patterns_used: int):
        """Actualiza estadísticas de generación."""
        self.generation_stats['total_generations'] += 1
        self.generation_stats['successful_generations'] += 1
        self.generation_stats['patterns_used'] += patterns_used
        
        # Actualizar promedio de longitud de contexto
        current_avg = self.generation_stats['avg_context_length']
        total_gens = self.generation_stats['total_generations']
        new_length = self._estimate_tokens(context)
        
        self.generation_stats['avg_context_length'] = (
            (current_avg * (total_gens - 1) + new_length) / total_gens
        )
    
    def add_pattern(self, 
                   domain: str, 
                   query_pattern: str, 
                   context_template: str) -> str:
        """Agrega un nuevo patrón al playbook del dominio."""
        playbook = self._get_or_create_playbook(domain)
        
        pattern = PlaybookPattern(
            query_pattern=query_pattern,
            context_template=context_template
        )
        
        playbook.add_pattern(pattern)
        self.playbook_manager.save_playbook(playbook)
        
        logger.info(f"Nuevo patrón agregado al dominio {domain}: {pattern.id}")
        return pattern.id
    
    def add_feedback(self, 
                    pattern_id: str, 
                    domain: str, 
                    is_helpful: bool):
        """Agrega feedback a un patrón."""
        playbook = self.playbook_manager.get_playbook_by_domain(domain)
        if not playbook:
            logger.warning(f"Playbook no encontrado para dominio: {domain}")
            return
        
        # Buscar patrón por ID
        for pattern in playbook.patterns:
            if pattern.id == pattern_id:
                pattern.add_feedback(is_helpful)
                self.playbook_manager.save_playbook(playbook)
                logger.info(f"Feedback agregado al patrón {pattern_id}: helpful={is_helpful}")
                return
        
        logger.warning(f"Patrón no encontrado: {pattern_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del generador."""
        playbook_stats = self.playbook_manager.get_all_stats()
        
        return {
            'generation_stats': self.generation_stats,
            'playbook_stats': playbook_stats,
            'config': {
                'max_context_tokens': self.max_context_tokens,
                'similarity_threshold': self.similarity_threshold
            }
        }
    
    def cleanup_low_value_patterns(self, domain: str, threshold: float = 0.3):
        """Limpia patrones de bajo valor del playbook."""
        playbook = self.playbook_manager.get_playbook_by_domain(domain)
        if not playbook:
            return
        
        initial_count = len(playbook.patterns)
        playbook.patterns = [p for p in playbook.patterns if p.is_valuable(threshold)]
        removed_count = initial_count - len(playbook.patterns)
        
        if removed_count > 0:
            self.playbook_manager.save_playbook(playbook)
            logger.info(f"Removidos {removed_count} patrones de bajo valor del dominio {domain}")


if __name__ == "__main__":
    # Test del ACEGenerator
    logging.basicConfig(level=logging.INFO)
    
    generator = ACEGenerator()
    
    # Generar contexto para diferentes queries
    test_queries = [
        "How to create a Python function?",
        "What is SQL SELECT statement?",
        "How to debug JavaScript errors?",
        "Explain machine learning basics"
    ]
    
    for query in test_queries:
        result = generator.generate_context(query)
        print(f"\nQuery: {query}")
        print(f"Domain: {result['domain']}")
        print(f"Patterns used: {result['patterns_used']}")
        print(f"Context tokens: {result['context_tokens']}")
        print(f"Success: {result['success']}")
        if result['context']:
            print(f"Context preview: {result['context'][:200]}...")
    
    # Mostrar estadísticas
    stats = generator.get_stats()
    print(f"\nStats: {stats}")
