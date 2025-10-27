#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración ACE con CAG DynamicContext y setup RQ para procesamiento background.
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import asyncio
import json

from .generator import ACEGenerator
from .reflector import ACEReflector
from .curator import ACECurator
from core.cag.dynamic_context import DynamicContext

logger = logging.getLogger(__name__)


class ACEIntegration:
    """Integra ACE Framework con CAG DynamicContext."""
    
    def __init__(self, 
                 playbooks_dir: str = "backend/data/playbooks",
                 max_context_tokens: int = 4000,
                 reflection_sampling_rate: float = 0.1):
        self.generator = ACEGenerator(playbooks_dir, max_context_tokens)
        self.reflector = ACEReflector(sampling_rate=reflection_sampling_rate)
        self.curator = ACECurator(playbooks_dir)
        
        self.integration_stats = {
            'total_queries': 0,
            'ace_context_generated': 0,
            'reflections_performed': 0,
            'playbooks_updated': 0,
            'avg_context_quality': 0.0
        }
        
        logger.info("ACEIntegration inicializado")
    
    def integrate_with_dynamic_context(self, dynamic_context: DynamicContext):
        """Integra ACE con DynamicContext como proveedor de contexto."""
        
        def ace_context_provider(query: str, history: List[Dict[str, Any]] = None) -> str:
            """Proveedor de contexto ACE para DynamicContext."""
            try:
                # Generar contexto usando ACE
                result = self.generator.generate_context(query, history)
                
                if result.get('success', False):
                    self.integration_stats['ace_context_generated'] += 1
                    return result.get('context', '')
                else:
                    logger.warning(f"ACE context generation failed: {result.get('error', 'Unknown error')}")
                    return ""
                    
            except Exception as e:
                logger.error(f"Error en ACE context provider: {e}")
                return ""
        
        # Registrar proveedor ACE
        dynamic_context.register_provider('ace', ace_context_provider)
        logger.info("Proveedor ACE registrado en DynamicContext")
    
    def process_query_with_ace(self, 
                              query: str, 
                              response: str,
                              context: str = "",
                              domain: str = "general",
                              user_feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una query completa con el ciclo ACE.
        
        Args:
            query: Query del usuario
            response: Respuesta generada
            context: Contexto utilizado
            domain: Dominio de la interacción
            user_feedback: Feedback del usuario (opcional)
            
        Returns:
            Dict con resultado del procesamiento ACE
        """
        start_time = datetime.now()
        logger.debug(f"Procesando query con ACE: '{query[:100]}...'")
        
        try:
            result = {
                'success': True,
                'query': query,
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'ace_cycle': {}
            }
            
            # 1. Generar contexto (ya se hizo en el flujo principal)
            context_result = {
                'context_generated': bool(context),
                'context_length': len(context) if context else 0
            }
            result['ace_cycle']['context_generation'] = context_result
            
            # 2. Reflexión
            reflection_result = self.reflector.reflect(
                query=query,
                response=response,
                context=context,
                domain=domain,
                user_feedback=user_feedback
            )
            result['ace_cycle']['reflection'] = reflection_result
            
            if reflection_result.get('success', False) and not reflection_result.get('skipped', False):
                self.integration_stats['reflections_performed'] += 1
            
            # 3. Curaduría (actualizar playbooks)
            if reflection_result.get('should_add_to_playbook', False):
                curation_result = self.curator.update_playbook(
                    reflection=reflection_result,
                    query=query,
                    response=response,
                    domain=domain
                )
                result['ace_cycle']['curation'] = curation_result
                
                if curation_result.get('success', False):
                    self.integration_stats['playbooks_updated'] += 1
            
            # 4. Actualizar estadísticas
            self._update_integration_stats(reflection_result)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            result['processing_time_ms'] = processing_time
            
            logger.info(f"Query procesada con ACE: reflection={reflection_result.get('success', False)}, "
                       f"curation={result['ace_cycle'].get('curation', {}).get('success', False)}, "
                       f"{processing_time:.1f}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando query con ACE: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'domain': domain,
                'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            }
    
    def _update_integration_stats(self, reflection_result: Dict[str, Any]):
        """Actualiza estadísticas de integración."""
        self.integration_stats['total_queries'] += 1
        
        if reflection_result.get('success', False) and not reflection_result.get('skipped', False):
            # Actualizar calidad promedio del contexto
            final_score = reflection_result.get('final_score', 0)
            current_avg = self.integration_stats['avg_context_quality']
            total_queries = self.integration_stats['total_queries']
            
            self.integration_stats['avg_context_quality'] = (
                (current_avg * (total_queries - 1) + final_score) / total_queries
            )
    
    def get_ace_context(self, 
                       query: str, 
                       history: List[Dict[str, Any]] = None,
                       domain: str = "general") -> Dict[str, Any]:
        """Obtiene contexto generado por ACE."""
        return self.generator.generate_context(query, history, domain)
    
    def add_pattern_manually(self, 
                           domain: str, 
                           query_pattern: str, 
                           context_template: str) -> str:
        """Agrega un patrón manualmente al playbook."""
        return self.generator.add_pattern(domain, query_pattern, context_template)
    
    def add_feedback_manually(self, 
                            pattern_id: str, 
                            domain: str, 
                            is_helpful: bool):
        """Agrega feedback manual a un patrón."""
        self.generator.add_feedback(pattern_id, domain, is_helpful)
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de integración."""
        return {
            'integration_stats': self.integration_stats,
            'generator_stats': self.generator.get_stats(),
            'reflector_stats': self.reflector.get_stats(),
            'curator_stats': self.curator.get_curation_stats()
        }
    
    def cleanup_low_value_patterns(self, domain: str = None):
        """Limpia patrones de bajo valor."""
        self.curator.force_cleanup(domain)
    
    def export_playbook(self, domain: str, filepath: str):
        """Exporta un playbook."""
        self.curator.export_playbook(domain, filepath)
    
    def import_playbook(self, filepath: str, domain: str = None):
        """Importa un playbook."""
        self.curator.import_playbook(filepath, domain)


class ACEBackgroundProcessor:
    """Procesador background para tareas ACE usando RQ."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.ace_integration = ACEIntegration()
        
        # Setup RQ (si está disponible)
        try:
            from rq import Queue, Connection
            from redis import Redis
            
            self.redis_conn = Redis.from_url(redis_url)
            self.reflection_queue = Queue('ace_reflection', connection=self.redis_conn)
            self.curation_queue = Queue('ace_curation', connection=self.redis_conn)
            
            logger.info("ACEBackgroundProcessor inicializado con RQ")
        except ImportError:
            logger.warning("RQ no disponible, usando procesamiento síncrono")
            self.redis_conn = None
            self.reflection_queue = None
            self.curation_queue = None
    
    def enqueue_reflection(self, 
                          query: str, 
                          response: str,
                          context: str = "",
                          domain: str = "general",
                          user_feedback: Optional[Dict[str, Any]] = None):
        """Encola reflexión para procesamiento background."""
        if self.reflection_queue:
            # Encolar en RQ
            job = self.reflection_queue.enqueue(
                'backend.ace.integration.process_reflection_background',
                query, response, context, domain, user_feedback,
                timeout=300  # 5 minutos timeout
            )
            logger.info(f"Reflexión encolada: {job.id}")
            return job.id
        else:
            # Procesar síncronamente
            return self._process_reflection_sync(query, response, context, domain, user_feedback)
    
    def enqueue_curation(self, 
                        reflection_result: Dict[str, Any],
                        query: str,
                        response: str,
                        domain: str = "general"):
        """Encola curaduría para procesamiento background."""
        if self.curation_queue:
            # Encolar en RQ
            job = self.curation_queue.enqueue(
                'backend.ace.integration.process_curation_background',
                reflection_result, query, response, domain,
                timeout=600  # 10 minutos timeout
            )
            logger.info(f"Curaduría encolada: {job.id}")
            return job.id
        else:
            # Procesar síncronamente
            return self._process_curation_sync(reflection_result, query, response, domain)
    
    def _process_reflection_sync(self, 
                               query: str, 
                               response: str,
                               context: str,
                               domain: str,
                               user_feedback: Optional[Dict[str, Any]]) -> str:
        """Procesa reflexión síncronamente."""
        result = self.ace_integration.reflector.reflect(
            query, response, context, domain, user_feedback
        )
        logger.info(f"Reflexión procesada síncronamente: {result.get('success', False)}")
        return "sync_processed"
    
    def _process_curation_sync(self, 
                             reflection_result: Dict[str, Any],
                             query: str,
                             response: str,
                             domain: str) -> str:
        """Procesa curaduría síncronamente."""
        result = self.ace_integration.curator.update_playbook(
            reflection_result, query, response, domain
        )
        logger.info(f"Curaduría procesada síncronamente: {result.get('success', False)}")
        return "sync_processed"
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de las colas."""
        if not self.reflection_queue or not self.curation_queue:
            return {'queues_available': False}
        
        return {
            'queues_available': True,
            'reflection_queue': {
                'length': len(self.reflection_queue),
                'failed_jobs': len(self.reflection_queue.failed_job_registry),
                'finished_jobs': len(self.reflection_queue.finished_job_registry)
            },
            'curation_queue': {
                'length': len(self.curation_queue),
                'failed_jobs': len(self.curation_queue.failed_job_registry),
                'finished_jobs': len(self.curation_queue.finished_job_registry)
            }
        }


# Funciones para RQ workers
def process_reflection_background(query: str, 
                                response: str,
                                context: str,
                                domain: str,
                                user_feedback: Optional[Dict[str, Any]] = None):
    """Función para procesar reflexión en background con RQ."""
    ace_integration = ACEIntegration()
    result = ace_integration.reflector.reflect(
        query, response, context, domain, user_feedback
    )
    logger.info(f"Reflexión background completada: {result.get('success', False)}")
    return result


def process_curation_background(reflection_result: Dict[str, Any],
                              query: str,
                              response: str,
                              domain: str):
    """Función para procesar curaduría en background con RQ."""
    ace_integration = ACEIntegration()
    result = ace_integration.curator.update_playbook(
        reflection_result, query, response, domain
    )
    logger.info(f"Curaduría background completada: {result.get('success', False)}")
    return result


if __name__ == "__main__":
    # Test de integración ACE
    logging.basicConfig(level=logging.INFO)
    
    # Crear integración
    ace_integration = ACEIntegration()
    
    # Test de generación de contexto
    context_result = ace_integration.get_ace_context(
        "How to create a Python function?",
        domain="python"
    )
    
    print(f"Context generation:")
    print(f"Success: {context_result.get('success', False)}")
    print(f"Domain: {context_result.get('domain', 'unknown')}")
    print(f"Patterns used: {context_result.get('patterns_used', 0)}")
    
    # Test de procesamiento completo
    processing_result = ace_integration.process_query_with_ace(
        query="How to create a Python function?",
        response="Use the 'def' keyword followed by the function name...",
        context="Python function context",
        domain="python"
    )
    
    print(f"\nACE processing:")
    print(f"Success: {processing_result.get('success', False)}")
    print(f"Reflection success: {processing_result.get('ace_cycle', {}).get('reflection', {}).get('success', False)}")
    print(f"Curation success: {processing_result.get('ace_cycle', {}).get('curation', {}).get('success', False)}")
    
    # Mostrar estadísticas
    stats = ace_integration.get_integration_stats()
    print(f"\nIntegration stats: {json.dumps(stats, indent=2)}")
    
    # Test de procesador background
    background_processor = ACEBackgroundProcessor()
    queue_stats = background_processor.get_queue_stats()
    print(f"\nQueue stats: {json.dumps(queue_stats, indent=2)}")
