#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para FASE 2: ACE Framework
"""

import sys
import os
import logging
import json
from datetime import datetime

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logging_config import setup_logging
from ace.playbook import Playbook, PlaybookManager, PlaybookPattern
from ace.generator import ACEGenerator
from ace.reflector import ACEReflector
from ace.curator import ACECurator
from ace.integration import ACEIntegration, ACEBackgroundProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_playbook_system():
    """Test del sistema de playbooks."""
    try:
        logger.info("=== Test Playbook System ===")
        
        # Crear manager
        manager = PlaybookManager("backend/data/playbooks")
        
        # Crear playbook de prueba
        playbook = manager.create_playbook("python")
        
        # Agregar patrón
        pattern = PlaybookPattern(
            query_pattern="python function",
            context_template="Python functions are defined using the 'def' keyword..."
        )
        playbook.add_pattern(pattern)
        
        # Agregar feedback
        pattern.add_feedback(True)  # Helpful
        pattern.add_feedback(True)  # Helpful
        pattern.add_feedback(False) # Harmful
        
        # Test búsqueda de patrones
        matching_patterns = playbook.find_matching_patterns("python function creation")
        print(f"Patrones encontrados: {len(matching_patterns)}")
        
        # Test estadísticas
        stats = playbook.get_stats()
        print(f"Stats del playbook: {json.dumps(stats, indent=2)}")
        
        # Guardar
        manager.save_playbook(playbook)
        
        # Test stats generales
        all_stats = manager.get_all_stats()
        print(f"Stats generales: {all_stats['total_playbooks']} playbooks, {all_stats['total_patterns']} patrones")
        
        logger.info("PASS - Playbook System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Playbook System: {e}")
        return False


def test_ace_generator():
    """Test del ACE Generator."""
    try:
        logger.info("=== Test ACE Generator ===")
        
        generator = ACEGenerator(max_context_tokens=2000)
        
        # Test generación de contexto
        result = generator.generate_context(
            query="How to create a Python function?",
            history=[],
            domain="python"
        )
        
        print(f"Contexto generado: {result['success']}")
        print(f"Dominio detectado: {result['domain']}")
        print(f"Patrones usados: {result['patterns_used']}")
        print(f"Tokens de contexto: {result['context_tokens']}")
        
        # Test agregar patrón manualmente
        pattern_id = generator.add_pattern(
            domain="python",
            query_pattern="python function creation",
            context_template="Python function context with examples"
        )
        print(f"Patrón agregado: {pattern_id}")
        
        # Test estadísticas
        stats = generator.get_stats()
        print(f"Stats del generador: {stats['generation_stats']['total_generations']} generaciones")
        
        logger.info("PASS - ACE Generator test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ACE Generator: {e}")
        return False


def test_ace_reflector():
    """Test del ACE Reflector."""
    try:
        logger.info("=== Test ACE Reflector ===")
        
        reflector = ACEReflector(sampling_rate=1.0)  # 100% sampling para test
        
        # Test reflexión
        result = reflector.reflect(
            query="How to create a Python function?",
            response="Use the 'def' keyword followed by the function name and parameters...",
            context="Python function context",
            domain="python"
        )
        
        print(f"Reflexión exitosa: {result.get('success', False)}")
        print(f"Score final: {result.get('final_score', 0):.1f}")
        print(f"Agregar a playbook: {result.get('should_add_to_playbook', False)}")
        print(f"Recomendaciones: {len(result.get('recommendations', []))}")
        
        # Test estadísticas
        stats = reflector.get_stats()
        print(f"Stats del reflector: {stats['reflection_stats']['total_reflections']} reflexiones")
        
        logger.info("PASS - ACE Reflector test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ACE Reflector: {e}")
        return False


def test_ace_curator():
    """Test del ACE Curator."""
    try:
        logger.info("=== Test ACE Curator ===")
        
        curator = ACECurator(persistence_interval=10)  # Intervalo bajo para test
        
        # Test reflexión mock
        reflection = {
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
        
        # Test actualización de playbook
        result = curator.update_playbook(
            reflection=reflection,
            query="How to create a Python function?",
            response="Use the 'def' keyword...",
            domain="python"
        )
        
        print(f"Curaduría exitosa: {result.get('success', False)}")
        print(f"Patrones agregados: {result.get('patterns_added', 0)}")
        print(f"Playbook actualizado: {result.get('playbook_updated', False)}")
        
        # Test feedback de ejecución
        execution_feedback = {
            'type': 'code_execution',
            'success': True,
            'error_type': None,
            'corrections_needed': 0
        }
        
        execution_result = curator.process_execution_feedback(execution_feedback)
        print(f"Feedback de ejecución procesado: {execution_result.get('success', False)}")
        
        # Test estadísticas
        stats = curator.get_curation_stats()
        print(f"Stats del curator: {stats['curation_stats']['total_interactions']} interacciones")
        
        logger.info("PASS - ACE Curator test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ACE Curator: {e}")
        return False


def test_ace_integration():
    """Test de la integración ACE completa."""
    try:
        logger.info("=== Test ACE Integration ===")
        
        integration = ACEIntegration()
        
        # Test generación de contexto
        context_result = integration.get_ace_context(
            query="How to create a Python function?",
            domain="python"
        )
        
        print(f"Contexto ACE generado: {context_result.get('success', False)}")
        print(f"Dominio: {context_result.get('domain', 'unknown')}")
        print(f"Patrones usados: {context_result.get('patterns_used', 0)}")
        
        # Test procesamiento completo
        processing_result = integration.process_query_with_ace(
            query="How to create a Python function?",
            response="Use the 'def' keyword followed by the function name and parameters...",
            context="Python function context",
            domain="python"
        )
        
        print(f"Procesamiento ACE exitoso: {processing_result.get('success', False)}")
        print(f"Reflexión exitosa: {processing_result.get('ace_cycle', {}).get('reflection', {}).get('success', False)}")
        print(f"Curaduría exitosa: {processing_result.get('ace_cycle', {}).get('curation', {}).get('success', False)}")
        
        # Test estadísticas
        stats = integration.get_integration_stats()
        print(f"Stats de integración: {stats['integration_stats']['total_queries']} queries procesadas")
        
        logger.info("PASS - ACE Integration test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ACE Integration: {e}")
        return False


def test_ace_background_processor():
    """Test del procesador background ACE."""
    try:
        logger.info("=== Test ACE Background Processor ===")
        
        processor = ACEBackgroundProcessor()
        
        # Test estadísticas de colas
        queue_stats = processor.get_queue_stats()
        print(f"Colas disponibles: {queue_stats.get('queues_available', False)}")
        
        if queue_stats.get('queues_available', False):
            print(f"Cola de reflexión: {queue_stats['reflection_queue']['length']} jobs")
            print(f"Cola de curaduría: {queue_stats['curation_queue']['length']} jobs")
        
        # Test encolado (síncrono si RQ no está disponible)
        reflection_job_id = processor.enqueue_reflection(
            query="How to create a Python function?",
            response="Use the 'def' keyword...",
            domain="python"
        )
        print(f"Reflexión encolada: {reflection_job_id}")
        
        logger.info("PASS - ACE Background Processor test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test ACE Background Processor: {e}")
        return False


def main():
    """Ejecuta todos los tests de FASE 2."""
    logger.info("Iniciando tests de FASE 2: ACE Framework")
    
    tests = [
        ("Playbook System", test_playbook_system),
        ("ACE Generator", test_ace_generator),
        ("ACE Reflector", test_ace_reflector),
        ("ACE Curator", test_ace_curator),
        ("ACE Integration", test_ace_integration),
        ("ACE Background Processor", test_ace_background_processor)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"Ejecutando test: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    logger.info("\n" + "="*50)
    logger.info("RESUMEN DE TESTS FASE 2")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name:25} {status}")
        if success:
            passed += 1
    
    logger.info("-" * 50)
    logger.info(f"Total: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("Todos los tests de FASE 2 pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
