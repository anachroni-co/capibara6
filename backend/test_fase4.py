#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para FASE 4: Persistent Agent Memory
"""

import sys
import os
import logging
from datetime import datetime, timedelta

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.database import DatabaseManager, Agent, AgentStatus, AgentInteraction, MemoryType
from agents.memory_manager import MemoryManager
from agents.graduation_system import GraduationSystem, GraduationCriteria
from agents.domain_system import DomainManager, CollaborationManager, DomainType, CollaborationType
from agents.agent_system import AgentSystem, PersistentAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_manager():
    """Test del DatabaseManager."""
    try:
        logger.info("=== Test Database Manager ===")
        
        db_manager = DatabaseManager("backend/data/test_agents.db")
        
        # Crear agente de prueba
        agent = Agent(
            id="test_db_agent",
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
        retrieved_agent = db_manager.get_agent("test_db_agent")
        print(f"Agente obtenido: {retrieved_agent.id if retrieved_agent else 'None'}")
        
        # Obtener agentes por dominio
        python_agents = db_manager.get_agents_by_domain("python")
        print(f"Agentes Python: {len(python_agents)}")
        
        # Obtener agentes por estado
        training_agents = db_manager.get_agents_by_status(AgentStatus.TRAINING)
        print(f"Agentes en entrenamiento: {len(training_agents)}")
        
        # Mostrar estadísticas
        stats = db_manager.get_database_stats()
        print(f"Estadísticas de BD: {stats}")
        
        logger.info("PASS - Database Manager test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Database Manager: {e}")
        return False


def test_memory_manager():
    """Test del MemoryManager."""
    try:
        logger.info("=== Test Memory Manager ===")
        
        db_manager = DatabaseManager("backend/data/test_agents.db")
        memory_manager = MemoryManager(db_manager)
        
        # Crear agente de prueba
        agent = Agent(
            id="test_memory_agent",
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
            agent_id="test_memory_agent",
            memory_type=MemoryType.CONVERSATION,
            content="User asked about Python functions. Explained def keyword, parameters, and return statements.",
            importance_score=0.8
        )
        
        memory_manager.add_memory(
            agent_id="test_memory_agent",
            memory_type=MemoryType.KNOWLEDGE,
            content="Python functions are defined using the 'def' keyword followed by the function name and parameters.",
            importance_score=0.9
        )
        
        memory_manager.add_memory(
            agent_id="test_memory_agent",
            memory_type=MemoryType.SKILL,
            content="To create a Python function: 1. Use 'def' keyword 2. Add function name 3. Add parameters 4. Add colon 5. Write function body",
            importance_score=0.7
        )
        
        # Obtener memorias
        memories = memory_manager.get_agent_memories("test_memory_agent")
        print(f"Memorias obtenidas: {len(memories)}")
        
        # Obtener memorias por tipo
        knowledge_memories = memory_manager.get_agent_memories("test_memory_agent", MemoryType.KNOWLEDGE)
        print(f"Memorias de conocimiento: {len(knowledge_memories)}")
        
        # Obtener memorias relevantes
        relevant = memory_manager.get_relevant_memories("test_memory_agent", "Python functions")
        print(f"Memorias relevantes: {len(relevant)}")
        
        # Mostrar estadísticas
        stats = memory_manager.get_manager_stats()
        print(f"Estadísticas de memoria: {stats}")
        
        logger.info("PASS - Memory Manager test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Memory Manager: {e}")
        return False


def test_graduation_system():
    """Test del GraduationSystem."""
    try:
        logger.info("=== Test Graduation System ===")
        
        db_manager = DatabaseManager("backend/data/test_agents.db")
        memory_manager = MemoryManager(db_manager)
        graduation_system = GraduationSystem(db_manager, memory_manager)
        
        # Crear agente de prueba con muchas interacciones
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
        
        # Agregar memorias
        for i in range(20):
            memory_manager.add_memory(
                agent_id="test_graduation_agent",
                memory_type=MemoryType.KNOWLEDGE,
                content=f"Knowledge item {i} about Python programming",
                importance_score=0.8
            )
        
        # Evaluar agente
        results = graduation_system.evaluate_all_agents()
        print(f"Evaluación completada: {len(results)} agentes evaluados")
        
        if results:
            evaluation = results[0]
            print(f"Agente elegible: {evaluation.eligible}")
            print(f"Score de graduación: {evaluation.graduation_score:.2f}")
            print(f"Criterios cumplidos: {evaluation.criteria_met}")
            print(f"Recomendaciones: {evaluation.recommendations}")
        
        # Mostrar estadísticas
        stats = graduation_system.get_graduation_stats()
        print(f"Estadísticas de graduación: {stats}")
        
        logger.info("PASS - Graduation System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Graduation System: {e}")
        return False


def test_domain_system():
    """Test del DomainSystem."""
    try:
        logger.info("=== Test Domain System ===")
        
        db_manager = DatabaseManager("backend/data/test_agents.db")
        domain_manager = DomainManager(db_manager)
        collaboration_manager = CollaborationManager(db_manager, domain_manager)
        
        # Test de prompts por dominio
        for domain in DomainType:
            prompt = domain_manager.get_domain_prompt(domain, 'system_prompt')
            print(f"{domain.value}: {prompt[:100]}...")
        
        # Test de generación de prompt
        generation_prompt = domain_manager.get_domain_prompt(
            DomainType.PYTHON, 'generation_prompt', "How to create a function?"
        )
        print(f"Prompt de generación: {generation_prompt[:100]}...")
        
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
        
        # Mostrar estadísticas de colaboración
        collab_stats = collaboration_manager.get_collaboration_stats()
        print(f"Estadísticas de colaboración: {collab_stats}")
        
        logger.info("PASS - Domain System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Domain System: {e}")
        return False


def test_agent_system():
    """Test del AgentSystem completo."""
    try:
        logger.info("=== Test Agent System ===")
        
        agent_system = AgentSystem("backend/data/test_agents.db")
        
        # Crear agente de prueba
        agent = agent_system.create_agent(DomainType.PYTHON, "test_system_agent")
        print(f"Agente creado: {agent.agent_id}")
        
        # Procesar múltiples queries
        test_queries = [
            "How to create a Python function?",
            "What are Python decorators?",
            "How to handle exceptions in Python?",
            "Explain Python list comprehensions",
            "How to work with Python dictionaries?"
        ]
        
        for query in test_queries:
            result = agent.process_query(
                query=query,
                context="Learning Python programming",
                user_intent="Learn Python concepts"
            )
            
            print(f"Query: {query}")
            print(f"  Success: {result['success']}")
            print(f"  Quality: {result['quality_score']:.1f}")
            print(f"  Time: {result['execution_time_ms']}ms")
        
        # Obtener información del agente
        agent_info = agent.get_agent_info()
        print(f"\nInformación del agente:")
        print(f"  ID: {agent_info['agent_id']}")
        print(f"  Domain: {agent_info['domain']}")
        print(f"  Status: {agent_info['status']}")
        print(f"  Interactions: {agent_info['total_interactions']}")
        print(f"  Success rate: {agent_info['success_rate']:.2%}")
        print(f"  Graduation score: {agent_info['graduation_score']:.2f}")
        
        # Obtener memorias
        memories = agent.get_memories(limit=5)
        print(f"\nMemorias del agente: {len(memories)}")
        
        # Obtener interacciones
        interactions = agent.get_interactions(limit=5)
        print(f"Interacciones del agente: {len(interactions)}")
        
        # Test de colaboración
        result_with_collab = agent.process_query(
            query="Advanced Python optimization techniques",
            context="Performance optimization",
            user_intent="Learn advanced techniques",
            require_collaboration=True
        )
        
        print(f"\nQuery con colaboración:")
        print(f"  Success: {result_with_collab['success']}")
        print(f"  Collaboration used: {result_with_collab['collaboration_used']}")
        
        # Mostrar estadísticas del sistema
        stats = agent_system.get_system_stats()
        print(f"\nEstadísticas del sistema: {stats}")
        
        logger.info("PASS - Agent System test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Agent System: {e}")
        return False


def test_graduation_evaluation():
    """Test de evaluación de graduación."""
    try:
        logger.info("=== Test Graduation Evaluation ===")
        
        agent_system = AgentSystem("backend/data/test_agents.db")
        
        # Crear agente con muchas interacciones exitosas
        agent = agent_system.create_agent(DomainType.PYTHON, "test_graduation_eval")
        
        # Simular muchas interacciones exitosas
        for i in range(200):
            result = agent.process_query(
                query=f"Python question {i}",
                context="Learning Python",
                user_intent="Learn Python"
            )
            
            # Simular alta calidad
            if result['success']:
                # Actualizar score de calidad manualmente (simulación)
                pass
        
        # Evaluar para graduación
        evaluation_results = agent_system.evaluate_graduations()
        print(f"Evaluaciones de graduación: {len(evaluation_results)}")
        
        for result in evaluation_results:
            if result['agent_id'] == "test_graduation_eval":
                print(f"Agente: {result['agent_id']}")
                print(f"Elegible: {result['eligible']}")
                print(f"Score: {result['graduation_score']:.2f}")
                print(f"Criterios: {result['criteria_met']}")
                print(f"Recomendaciones: {result['recommendations']}")
                break
        
        logger.info("PASS - Graduation Evaluation test completado")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Error en test Graduation Evaluation: {e}")
        return False


def main():
    """Ejecuta todos los tests de FASE 4."""
    logger.info("Iniciando tests de FASE 4: Persistent Agent Memory")
    
    tests = [
        ("Database Manager", test_database_manager),
        ("Memory Manager", test_memory_manager),
        ("Graduation System", test_graduation_system),
        ("Domain System", test_domain_system),
        ("Agent System", test_agent_system),
        ("Graduation Evaluation", test_graduation_evaluation)
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
    logger.info("RESUMEN DE TESTS FASE 4")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        logger.info(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    logger.info("-" * 50)
    logger.info(f"Total: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("Todos los tests de FASE 4 pasaron exitosamente!")
        return True
    else:
        logger.error(f"{total - passed} tests fallaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
