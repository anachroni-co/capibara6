#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACE Curator - Actualiza y mantiene playbooks basado en reflexiones.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os

from .playbook import Playbook, PlaybookManager, PlaybookPattern
from .generator import ACEGenerator

logger = logging.getLogger(__name__)


class ACECurator:
    """Actualiza y mantiene playbooks basado en reflexiones."""
    
    def __init__(self, 
                 playbooks_dir: str = "backend/data/playbooks",
                 persistence_interval: int = 100,  # Cada N interacciones
                 filtering_threshold: float = 0.5,
                 max_patterns_per_domain: int = 1000):
        self.playbook_manager = PlaybookManager(playbooks_dir)
        self.generator = ACEGenerator(playbooks_dir)
        self.persistence_interval = persistence_interval
        self.filtering_threshold = filtering_threshold
        self.max_patterns_per_domain = max_patterns_per_domain
        
        self.interaction_count = 0
        self.curation_stats = {
            'total_interactions': 0,
            'patterns_added': 0,
            'patterns_removed': 0,
            'playbooks_updated': 0,
            'successful_curations': 0,
            'failed_curations': 0
        }
        
        logger.info(f"ACECurator inicializado con interval={persistence_interval}, "
                   f"threshold={filtering_threshold}, max_patterns={max_patterns_per_domain}")
    
    def update_playbook(self, 
                       reflection: Dict[str, Any], 
                       query: str, 
                       response: str,
                       domain: str = "general") -> Dict[str, Any]:
        """
        Actualiza playbook con nueva información basada en reflexión.
        
        Args:
            reflection: Resultado de la reflexión
            query: Query original
            response: Respuesta generada
            domain: Dominio de la interacción
            
        Returns:
            Dict con resultado de la actualización
        """
        start_time = datetime.now()
        logger.debug(f"Actualizando playbook para dominio: {domain}")
        
        try:
            result = {
                'success': True,
                'domain': domain,
                'patterns_added': 0,
                'patterns_removed': 0,
                'playbook_updated': False,
                'timestamp': datetime.now().isoformat()
            }
            
            # 1. Obtener o crear playbook
            playbook = self.playbook_manager.get_playbook_by_domain(domain)
            if not playbook:
                playbook = self.playbook_manager.create_playbook(domain)
                result['playbook_created'] = True
            
            # 2. Agregar patrón si la reflexión lo recomienda
            if reflection.get('should_add_to_playbook', False):
                pattern_added = self._add_pattern_from_reflection(
                    playbook, reflection, query, response
                )
                if pattern_added:
                    result['patterns_added'] = 1
                    result['playbook_updated'] = True
            
            # 3. Agregar feedback a patrones existentes
            self._add_feedback_to_existing_patterns(playbook, reflection, query)
            
            # 4. Actualizar contadores de interacción
            self._update_interaction_counters(playbook, reflection)
            
            # 5. Persistir si es necesario
            if self.interaction_count % self.persistence_interval == 0:
                self._persist_and_cleanup(playbook)
                result['persistence_triggered'] = True
            
            # 6. Guardar playbook
            self.playbook_manager.save_playbook(playbook)
            
            # 7. Actualizar estadísticas
            self._update_curation_stats(result)
            
            curation_time = (datetime.now() - start_time).total_seconds() * 1000
            result['curation_time_ms'] = curation_time
            
            logger.info(f"Playbook actualizado: {result['patterns_added']} patrones agregados, "
                       f"{result['patterns_removed']} removidos, {curation_time:.1f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error actualizando playbook: {e}")
            return {
                'success': False,
                'error': str(e),
                'domain': domain,
                'curation_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            }
    
    def _add_pattern_from_reflection(self, 
                                   playbook: Playbook,
                                   reflection: Dict[str, Any],
                                   query: str,
                                   response: str) -> bool:
        """Agrega un nuevo patrón basado en la reflexión."""
        try:
            # Extraer información del patrón
            pattern_extraction = reflection.get('pattern_extraction')
            if not pattern_extraction:
                # Crear patrón básico si no hay extracción
                query_pattern = self._extract_query_pattern(query)
                context_template = self._create_context_template(query, response)
            else:
                query_pattern = pattern_extraction.get('query_pattern', query)
                context_template = pattern_extraction.get('context_template', 
                                                         self._create_context_template(query, response))
            
            # Crear patrón
            pattern = PlaybookPattern(
                query_pattern=query_pattern,
                context_template=context_template
            )
            
            # Agregar feedback inicial basado en la reflexión
            main_analysis = reflection.get('main_analysis', {})
            overall_score = main_analysis.get('overall_score', 0)
            
            if overall_score >= 8.0:
                pattern.add_feedback(True)  # Helpful
                pattern.add_feedback(True)  # Helpful
            elif overall_score >= 6.0:
                pattern.add_feedback(True)  # Helpful
            else:
                pattern.add_feedback(False)  # Harmful
            
            # Agregar al playbook
            playbook.add_pattern(pattern)
            
            logger.info(f"Nuevo patrón agregado: {pattern.id} para dominio {playbook.domain}")
            return True
            
        except Exception as e:
            logger.error(f"Error agregando patrón: {e}")
            return False
    
    def _extract_query_pattern(self, query: str) -> str:
        """Extrae un patrón reutilizable de la query."""
        # Implementación simple: normalizar la query
        # En una implementación real, usaríamos NLP más sofisticado
        
        # Remover palabras específicas y mantener estructura
        words = query.lower().split()
        
        # Palabras a remover (específicas del usuario)
        stop_words = {'how', 'what', 'where', 'when', 'why', 'can', 'could', 'would', 'should'}
        filtered_words = [w for w in words if w not in stop_words]
        
        # Limitar longitud
        if len(filtered_words) > 10:
            filtered_words = filtered_words[:10]
        
        return ' '.join(filtered_words)
    
    def _create_context_template(self, query: str, response: str) -> str:
        """Crea un template de contexto basado en la query y respuesta."""
        # Extraer elementos clave de la respuesta
        response_lower = response.lower()
        
        # Identificar tipo de respuesta
        if '```' in response or 'def ' in response:
            response_type = "code_example"
        elif 'step' in response_lower or 'first' in response_lower:
            response_type = "step_by_step"
        elif 'example' in response_lower:
            response_type = "with_examples"
        else:
            response_type = "explanation"
        
        # Crear template basado en el tipo
        templates = {
            'code_example': f"Para {query.split()[0] if query else 'esta tarea'}, aquí tienes un ejemplo de código:",
            'step_by_step': f"Para {query.split()[0] if query else 'esta tarea'}, sigue estos pasos:",
            'with_examples': f"Para {query.split()[0] if query else 'esta tarea'}, aquí tienes una explicación con ejemplos:",
            'explanation': f"Para {query.split()[0] if query else 'esta tarea'}, aquí tienes una explicación:"
        }
        
        return templates.get(response_type, f"Contexto para {query}")
    
    def _add_feedback_to_existing_patterns(self, 
                                         playbook: Playbook,
                                         reflection: Dict[str, Any],
                                         query: str):
        """Agrega feedback a patrones existentes que coincidan."""
        # Buscar patrones que coincidan con la query
        matching_patterns = playbook.find_matching_patterns(query, max_patterns=3)
        
        if not matching_patterns:
            return
        
        # Determinar si el feedback es positivo o negativo
        main_analysis = reflection.get('main_analysis', {})
        overall_score = main_analysis.get('overall_score', 0)
        is_helpful = overall_score >= 6.0 and not main_analysis.get('has_hallucinations', False)
        
        # Agregar feedback a patrones coincidentes
        for pattern in matching_patterns:
            pattern.add_feedback(is_helpful)
            logger.debug(f"Feedback agregado al patrón {pattern.id}: helpful={is_helpful}")
    
    def _update_interaction_counters(self, playbook: Playbook, reflection: Dict[str, Any]):
        """Actualiza contadores de interacción."""
        self.interaction_count += 1
        
        # Agregar a respuestas exitosas o fallidas
        main_analysis = reflection.get('main_analysis', {})
        overall_score = main_analysis.get('overall_score', 0)
        
        if overall_score >= 6.0:
            # Agregar como respuesta exitosa (mock)
            playbook.add_successful_response(
                query="",  # Se llenaría con la query real
                response="",  # Se llenaría con la respuesta real
                context_used=""
            )
        else:
            # Agregar como respuesta fallida
            playbook.add_failed_response(
                query="",
                response="",
                error=f"Low quality response (score: {overall_score})"
            )
    
    def _persist_and_cleanup(self, playbook: Playbook):
        """Persiste cambios y limpia patrones de bajo valor."""
        logger.info(f"Ejecutando persistencia y limpieza para dominio {playbook.domain}")
        
        # 1. Limpiar patrones de bajo valor
        initial_count = len(playbook.patterns)
        playbook.patterns = [
            p for p in playbook.patterns 
            if p.is_valuable(self.filtering_threshold)
        ]
        removed_count = initial_count - len(playbook.patterns)
        
        if removed_count > 0:
            logger.info(f"Removidos {removed_count} patrones de bajo valor")
        
        # 2. Limitar número de patrones por dominio
        if len(playbook.patterns) > self.max_patterns_per_domain:
            # Mantener los mejores patrones
            playbook.patterns.sort(key=lambda p: p.get_success_rate(), reverse=True)
            playbook.patterns = playbook.patterns[:self.max_patterns_per_domain]
            logger.info(f"Limitados patrones a {self.max_patterns_per_domain}")
        
        # 3. Limpiar respuestas históricas antiguas
        cutoff_date = datetime.now() - timedelta(days=30)
        cutoff_iso = cutoff_date.isoformat()
        
        playbook.successful_responses = [
            r for r in playbook.successful_responses
            if r.get('timestamp', '') > cutoff_iso
        ]
        
        playbook.failed_responses = [
            r for r in playbook.failed_responses
            if r.get('timestamp', '') > cutoff_iso
        ]
        
        # 4. Actualizar metadata
        playbook._update_metadata()
    
    def _update_curation_stats(self, result: Dict[str, Any]):
        """Actualiza estadísticas de curaduría."""
        self.curation_stats['total_interactions'] += 1
        
        if result.get('success', False):
            self.curation_stats['successful_curations'] += 1
            self.curation_stats['patterns_added'] += result.get('patterns_added', 0)
            self.curation_stats['patterns_removed'] += result.get('patterns_removed', 0)
            
            if result.get('playbook_updated', False):
                self.curation_stats['playbooks_updated'] += 1
        else:
            self.curation_stats['failed_curations'] += 1
    
    def process_execution_feedback(self, feedback: Dict[str, Any]):
        """Procesa feedback de ejecución E2B."""
        logger.info(f"Procesando feedback de ejecución: {feedback.get('type', 'unknown')}")
        
        # Extraer información relevante
        success = feedback.get('success', False)
        error_type = feedback.get('error_type')
        corrections_needed = feedback.get('corrections_needed', 0)
        
        # Crear reflexión mock basada en feedback de ejecución
        execution_reflection = {
            'main_analysis': {
                'overall_score': 8.0 if success else 4.0,
                'has_hallucinations': False,
                'has_factual_errors': not success,
                'scores': {
                    'accuracy': 8.0 if success else 3.0,
                    'relevance': 7.0,
                    'clarity': 7.0,
                    'utility': 8.0 if success else 2.0,
                    'factual_correctness': 9.0 if success else 1.0
                }
            },
            'should_add_to_playbook': success and corrections_needed == 0,
            'pattern_extraction': {
                'query_pattern': f"code execution {error_type or 'success'}",
                'context_template': f"Code execution context for {error_type or 'successful execution'}",
                'confidence': 7.0
            }
        }
        
        # Actualizar playbook de ejecución
        domain = "code_execution"
        result = self.update_playbook(
            reflection=execution_reflection,
            query=f"Code execution feedback: {feedback.get('type', 'unknown')}",
            response=f"Execution result: {'success' if success else 'failure'}",
            domain=domain
        )
        
        logger.info(f"Feedback de ejecución procesado: {result.get('success', False)}")
        return result
    
    def get_curation_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de curaduría."""
        playbook_stats = self.playbook_manager.get_all_stats()
        
        return {
            'curation_stats': self.curation_stats,
            'playbook_stats': playbook_stats,
            'config': {
                'persistence_interval': self.persistence_interval,
                'filtering_threshold': self.filtering_threshold,
                'max_patterns_per_domain': self.max_patterns_per_domain
            }
        }
    
    def force_cleanup(self, domain: str = None):
        """Fuerza limpieza de patrones de bajo valor."""
        if domain:
            # Limpiar dominio específico
            playbook = self.playbook_manager.get_playbook_by_domain(domain)
            if playbook:
                self._persist_and_cleanup(playbook)
                self.playbook_manager.save_playbook(playbook)
                logger.info(f"Limpieza forzada completada para dominio: {domain}")
        else:
            # Limpiar todos los dominios
            for playbook in self.playbook_manager.playbooks.values():
                self._persist_and_cleanup(playbook)
                self.playbook_manager.save_playbook(playbook)
            logger.info("Limpieza forzada completada para todos los dominios")
    
    def export_playbook(self, domain: str, filepath: str):
        """Exporta un playbook a un archivo."""
        playbook = self.playbook_manager.get_playbook_by_domain(domain)
        if not playbook:
            raise ValueError(f"Playbook no encontrado para dominio: {domain}")
        
        playbook.save_to_file(filepath)
        logger.info(f"Playbook exportado: {domain} -> {filepath}")
    
    def import_playbook(self, filepath: str, domain: str = None):
        """Importa un playbook desde un archivo."""
        playbook = Playbook.load_from_file(filepath)
        
        if domain and playbook.domain != domain:
            playbook.domain = domain
        
        self.playbook_manager.save_playbook(playbook)
        logger.info(f"Playbook importado: {filepath} -> {playbook.domain}")


if __name__ == "__main__":
    # Test del ACECurator
    logging.basicConfig(level=logging.INFO)
    
    curator = ACECurator()
    
    # Test de actualización de playbook
    test_reflection = {
        'should_add_to_playbook': True,
        'main_analysis': {
            'overall_score': 8.5,
            'has_hallucinations': False,
            'has_factual_errors': False
        },
        'pattern_extraction': {
            'query_pattern': 'python function creation',
            'context_template': 'Python function context with examples',
            'confidence': 8.0
        }
    }
    
    result = curator.update_playbook(
        reflection=test_reflection,
        query="How to create a Python function?",
        response="Use the 'def' keyword...",
        domain="python"
    )
    
    print(f"Curation result:")
    print(f"Success: {result.get('success', False)}")
    print(f"Patterns added: {result.get('patterns_added', 0)}")
    print(f"Playbook updated: {result.get('playbook_updated', False)}")
    
    # Test de feedback de ejecución
    execution_feedback = {
        'type': 'code_execution',
        'success': True,
        'error_type': None,
        'corrections_needed': 0
    }
    
    execution_result = curator.process_execution_feedback(execution_feedback)
    print(f"\nExecution feedback processed: {execution_result.get('success', False)}")
    
    # Mostrar estadísticas
    stats = curator.get_curation_stats()
    print(f"\nStats: {json.dumps(stats, indent=2)}")
