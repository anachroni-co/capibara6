#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fase 7 - Test de optimizaciones avanzadas.
"""

import logging
import json
import os
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_rewiring_experts():
    """Test del sistema Rewiring Experts."""
    logger.info("=== Test Rewiring Experts ===")
    
    try:
        from optimizations.rewiring_experts import (
            RewiringExperts, 
            RewiringStrategy, 
            ExpertType
        )
        
        # Crear sistema de rewiring
        rewiring_system = RewiringExperts(strategy=RewiringStrategy.ADAPTIVE)
        
        # Test de routing
        test_queries = [
            ("How to create a Python function?", {"domain": "python", "complexity": 0.3}),
            ("SELECT * FROM users WHERE age > 25", {"domain": "sql", "complexity": 0.5}),
            ("Debug this JavaScript error", {"domain": "javascript", "complexity": 0.7}),
            ("Train a machine learning model", {"domain": "ml", "complexity": 0.8}),
            ("Create a REST API endpoint", {"domain": "api", "complexity": 0.6})
        ]
        
        routing_decisions = []
        for query, features in test_queries:
            decision = rewiring_system.route_query(query, features)
            routing_decisions.append(decision)
            
            logger.info(f"Query: {query}")
            logger.info(f"Routed to: {decision.primary_expert}")
            logger.info(f"Confidence: {decision.confidence_score:.2f}")
            logger.info(f"Fallback: {decision.fallback_experts}")
        
        # Simular actualizaciones de rendimiento
        for decision in routing_decisions:
            rewiring_system.update_expert_performance(
                decision.primary_expert, 
                success=True, 
                latency_ms=50.0
            )
        
        # Mostrar métricas
        metrics = rewiring_system.get_expert_graph_metrics()
        logger.info(f"Métricas del grafo: {metrics}")
        
        # Mostrar estado de expertos
        status = rewiring_system.get_expert_status()
        logger.info(f"Estado de expertos: {len(status)} expertos activos")
        
        logger.info("PASS - Rewiring Experts")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Rewiring Experts: {e}")
        return False

def test_memagent():
    """Test del sistema MemAgent."""
    logger.info("=== Test MemAgent ===")
    
    try:
        from optimizations.memagent import (
            MemAgent, 
            MemoryType, 
            MemoryPriority, 
            MemoryQuery
        )
        
        # Crear MemAgent
        memagent = MemAgent(max_tokens=10000)  # 10K tokens para test
        
        # Almacenar memorias de prueba
        memories = [
            ("Python function to calculate fibonacci", MemoryType.PROCEDURAL, MemoryPriority.HIGH, ["python", "math"]),
            ("SQL query to find users by age", MemoryType.PROCEDURAL, MemoryPriority.MEDIUM, ["sql", "database"]),
            ("JavaScript error handling best practices", MemoryType.SEMANTIC, MemoryPriority.MEDIUM, ["javascript", "error"]),
            ("Machine learning model training steps", MemoryType.PROCEDURAL, MemoryPriority.HIGH, ["ml", "training"]),
            ("API endpoint design principles", MemoryType.SEMANTIC, MemoryPriority.LOW, ["api", "design"])
        ]
        
        chunk_ids = []
        for content, mem_type, priority, tags in memories:
            chunk_id = memagent.store_memory(content, mem_type, priority, tags)
            chunk_ids.append(chunk_id)
            logger.info(f"Memoria almacenada: {chunk_id}")
        
        # Consultar memoria
        query = MemoryQuery(
            query_id="test_query_001",
            query_text="How to create Python functions?",
            memory_types=[MemoryType.PROCEDURAL, MemoryType.SEMANTIC],
            max_tokens=1000,
            similarity_threshold=0.5,
            tags_filter=["python"]
        )
        
        result = memagent.retrieve_memory(query)
        logger.info(f"Consulta: {query.query_text}")
        logger.info(f"Chunks encontrados: {len(result.chunks)}")
        logger.info(f"Total tokens: {result.total_tokens}")
        logger.info(f"Tiempo de búsqueda: {result.search_time_ms:.2f}ms")
        
        # Mostrar estadísticas
        stats = memagent.get_memory_stats()
        logger.info(f"Estadísticas: {stats}")
        
        # Mostrar resumen
        summary = memagent.get_memory_summary()
        logger.info(f"Resumen: {summary}")
        
        logger.info("PASS - MemAgent")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - MemAgent: {e}")
        return False

def test_duo_attention():
    """Test del sistema DuoAttention."""
    logger.info("=== Test DuoAttention ===")
    
    try:
        from optimizations.duo_attention import (
            DuoAttention, 
            AttentionMode, 
            AttentionType, 
            AttentionQuery
        )
        
        # Crear DuoAttention
        duo_attention = DuoAttention(
            primary_dimension=768,
            secondary_dimension=512,
            num_heads=8,
            mode=AttentionMode.ADAPTIVE
        )
        
        # Test de atención
        test_queries = [
            AttentionQuery(
                query_id="test_001",
                input_tokens=["How", "to", "create", "a", "Python", "function"],
                context_tokens=["Python", "programming", "functions", "def"],
                attention_types=[AttentionType.SELF_ATTENTION, AttentionType.CROSS_ATTENTION],
                max_sequence_length=128,
                temperature=1.0,
                metadata={'complexity': 'medium'}
            ),
            AttentionQuery(
                query_id="test_002",
                input_tokens=["Debug", "this", "JavaScript", "error"],
                context_tokens=None,
                attention_types=[AttentionType.SELF_ATTENTION],
                max_sequence_length=64,
                temperature=0.8,
                metadata={'complexity': 'low'}
            )
        ]
        
        for query in test_queries:
            result = duo_attention.process_attention(query)
            logger.info(f"Query: {query.query_id}")
            logger.info(f"Quality Score: {result.quality_score:.3f}")
            logger.info(f"Processing Time: {result.processing_time_ms:.2f}ms")
            logger.info(f"Heads Used: {len(result.attention_heads_used)}")
            logger.info(f"Output Shape: {result.output_embeddings.shape}")
        
        # Mostrar estadísticas
        stats = duo_attention.get_attention_stats()
        logger.info(f"Estadísticas: {stats}")
        
        # Mostrar estado de cabezas
        head_status = duo_attention.get_head_status()
        logger.info(f"Estado de cabezas: {len(head_status)} cabezas activas")
        
        logger.info("PASS - DuoAttention")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - DuoAttention: {e}")
        return False

def test_budget_forcing():
    """Test del sistema Budget Forcing."""
    logger.info("=== Test Budget Forcing ===")
    
    try:
        from optimizations.budget_forcing import (
            BudgetForcing, 
            EnforcementLevel, 
            ResourceType, 
            BudgetType, 
            BudgetRequest
        )
        
        # Crear BudgetForcing
        budget_forcing = BudgetForcing(enforcement_level=EnforcementLevel.MEDIUM)
        
        # Crear presupuestos personalizados
        cpu_budget_id = budget_forcing.create_budget(
            ResourceType.CPU,
            BudgetType.PER_REQUEST,
            50.0,  # 50% CPU
            EnforcementLevel.HARD
        )
        
        memory_budget_id = budget_forcing.create_budget(
            ResourceType.MEMORY,
            BudgetType.PER_REQUEST,
            4.0,  # 4GB RAM
            EnforcementLevel.MEDIUM
        )
        
        # Test de solicitudes de presupuesto
        test_requests = [
            BudgetRequest(
                request_id="req_001",
                resource_type=ResourceType.CPU,
                requested_amount=30.0,
                priority=1,
                estimated_duration=300,
                requester_id="user_001",
                justification="Training model",
                created_at=datetime.now()
            ),
            BudgetRequest(
                request_id="req_002",
                resource_type=ResourceType.MEMORY,
                requested_amount=2.0,
                priority=2,
                estimated_duration=600,
                requester_id="user_002",
                justification="Data processing",
                created_at=datetime.now()
            ),
            BudgetRequest(
                request_id="req_003",
                resource_type=ResourceType.CPU,
                requested_amount=40.0,  # Excedería el límite
                priority=3,
                estimated_duration=200,
                requester_id="user_003",
                justification="Heavy computation",
                created_at=datetime.now()
            )
        ]
        
        # Procesar solicitudes
        approved_requests = 0
        for request in test_requests:
            approved, allocation_id, message = budget_forcing.request_budget(request)
            logger.info(f"Request {request.request_id}: {'Aprobado' if approved else 'Rechazado'}")
            logger.info(f"  Message: {message}")
            if allocation_id:
                logger.info(f"  Allocation ID: {allocation_id}")
                approved_requests += 1
        
        # Mostrar estado
        status = budget_forcing.get_budget_status()
        logger.info(f"Estado de presupuestos:")
        logger.info(f"  Asignaciones activas: {status['active_allocations']}")
        logger.info(f"  Violaciones totales: {status['total_violations']}")
        
        # Mostrar estadísticas
        stats = budget_forcing.get_budget_stats()
        logger.info(f"Estadísticas: {stats}")
        
        # Liberar presupuesto
        if status['active_allocations'] > 0:
            first_allocation = list(budget_forcing.active_allocations.keys())[0]
            released = budget_forcing.release_budget(first_allocation)
            logger.info(f"Presupuesto liberado: {released}")
        
        logger.info("PASS - Budget Forcing")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Budget Forcing: {e}")
        return False

def test_multi_round_thinking():
    """Test del sistema Multi-round Thinking."""
    logger.info("=== Test Multi-round Thinking ===")
    
    try:
        from optimizations.multi_round_thinking import (
            MultiRoundThinking, 
            ThinkingMode, 
            ReasoningType
        )
        
        # Crear MultiRoundThinking
        multi_round = MultiRoundThinking(max_rounds=3)
        
        # Iniciar sesión de pensamiento
        session_id = multi_round.start_thinking_session(
            "How can we improve the performance of our AI system?",
            "We have a system with 20B and 120B models, using T5X for training"
        )
        
        logger.info(f"Sesión iniciada: {session_id}")
        
        # Ejecutar rondas de pensamiento
        for round_num in range(3):
            thinking_round = multi_round.execute_thinking_round(
                session_id,
                thinking_mode=ThinkingMode.ANALYTICAL if round_num == 0 else ThinkingMode.ADAPTIVE,
                reasoning_type=ReasoningType.DEDUCTIVE
            )
            
            if thinking_round:
                logger.info(f"Ronda {thinking_round.round_number}:")
                logger.info(f"  Confianza: {thinking_round.confidence_score:.2f}")
                logger.info(f"  Calidad: {thinking_round.quality_score:.2f}")
                logger.info(f"  Pasos: {len(thinking_round.steps)}")
                logger.info(f"  Insights: {len(thinking_round.insights)}")
        
        # Completar sesión
        completed_session = multi_round.complete_thinking_session(session_id)
        
        if completed_session:
            logger.info(f"Sesión completada:")
            logger.info(f"  Confianza general: {completed_session.overall_confidence:.2f}")
            logger.info(f"  Calidad general: {completed_session.overall_quality:.2f}")
            logger.info(f"  Duración: {completed_session.total_duration_seconds:.2f}s")
            logger.info(f"  Rondas: {len(completed_session.rounds)}")
        
        # Mostrar estadísticas
        stats = multi_round.get_multi_round_stats()
        logger.info(f"Estadísticas: {stats}")
        
        logger.info("PASS - Multi-round Thinking")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Multi-round Thinking: {e}")
        return False

def test_integration_optimizations():
    """Test de integración de optimizaciones."""
    logger.info("=== Test Integración de Optimizaciones ===")
    
    try:
        # Crear directorios necesarios
        os.makedirs("backend/data/optimizations", exist_ok=True)
        os.makedirs("backend/data/memagent", exist_ok=True)
        
        logger.info("Directorios de optimizaciones creados")
        
        # Test completo del pipeline de optimizaciones
        from optimizations.rewiring_experts import RewiringExperts, RewiringStrategy
        from optimizations.memagent import MemAgent, MemoryType, MemoryPriority
        from optimizations.duo_attention import DuoAttention, AttentionMode, AttentionType
        from optimizations.budget_forcing import BudgetForcing, EnforcementLevel, ResourceType
        from optimizations.multi_round_thinking import MultiRoundThinking, ThinkingMode
        
        # 1. Inicializar sistemas
        rewiring_system = RewiringExperts(strategy=RewiringStrategy.ADAPTIVE)
        memagent = MemAgent(max_tokens=5000)
        duo_attention = DuoAttention(mode=AttentionMode.ADAPTIVE)
        budget_forcing = BudgetForcing(enforcement_level=EnforcementLevel.MEDIUM)
        multi_round = MultiRoundThinking(max_rounds=2)
        
        logger.info("1. Sistemas de optimización inicializados")
        
        # 2. Almacenar conocimiento en MemAgent
        knowledge_chunks = [
            ("Python optimization techniques", MemoryType.SEMANTIC, MemoryPriority.HIGH, ["python", "optimization"]),
            ("T5X training best practices", MemoryType.PROCEDURAL, MemoryPriority.HIGH, ["t5x", "training"]),
            ("TPU V5e-64 configuration", MemoryType.SEMANTIC, MemoryPriority.MEDIUM, ["tpu", "config"])
        ]
        
        for content, mem_type, priority, tags in knowledge_chunks:
            chunk_id = memagent.store_memory(content, mem_type, priority, tags)
            logger.info(f"2. Conocimiento almacenado: {chunk_id}")
        
        # 3. Solicitar presupuesto para procesamiento
        from optimizations.budget_forcing import BudgetRequest
        budget_request = BudgetRequest(
            request_id="opt_001",
            resource_type=ResourceType.CPU,
            requested_amount=25.0,
            priority=1,
            estimated_duration=300,
            requester_id="optimization_system",
            justification="Advanced optimization processing",
            created_at=datetime.now()
        )
        
        approved, allocation_id, message = budget_forcing.request_budget(budget_request)
        logger.info(f"3. Presupuesto {'aprobado' if approved else 'rechazado'}: {message}")
        
        if approved:
            # 4. Iniciar sesión de pensamiento
            session_id = multi_round.start_thinking_session(
                "How to optimize our AI system with the new components?",
                "We have Rewiring Experts, MemAgent, DuoAttention, and Budget Forcing"
            )
            logger.info(f"4. Sesión de pensamiento iniciada: {session_id}")
            
            # 5. Ejecutar ronda de pensamiento
            thinking_round = multi_round.execute_thinking_round(
                session_id,
                thinking_mode=ThinkingMode.ANALYTICAL,
                reasoning_type=ReasoningType.DEDUCTIVE
            )
            
            if thinking_round:
                logger.info(f"5. Ronda de pensamiento completada:")
                logger.info(f"   Confianza: {thinking_round.confidence_score:.2f}")
                logger.info(f"   Calidad: {thinking_round.quality_score:.2f}")
                logger.info(f"   Insights: {len(thinking_round.insights)}")
            
            # 6. Procesar con DuoAttention
            from optimizations.duo_attention import AttentionQuery
            attention_query = AttentionQuery(
                query_id="opt_attention_001",
                input_tokens=["optimize", "AI", "system", "performance"],
                context_tokens=["rewiring", "experts", "memagent", "attention"],
                attention_types=[AttentionType.SELF_ATTENTION, AttentionType.CROSS_ATTENTION],
                max_sequence_length=64,
                temperature=1.0,
                metadata={'optimization': True}
            )
            
            attention_result = duo_attention.process_attention(attention_query)
            logger.info(f"6. Atención procesada:")
            logger.info(f"   Quality Score: {attention_result.quality_score:.3f}")
            logger.info(f"   Processing Time: {attention_result.processing_time_ms:.2f}ms")
            
            # 7. Routear query con Rewiring Experts
            routing_decision = rewiring_system.route_query(
                "Optimize AI system performance",
                {"domain": "optimization", "complexity": 0.8}
            )
            logger.info(f"7. Query ruteada:")
            logger.info(f"   Primary Expert: {routing_decision.primary_expert}")
            logger.info(f"   Confidence: {routing_decision.confidence_score:.2f}")
            
            # 8. Completar sesión de pensamiento
            completed_session = multi_round.complete_thinking_session(session_id)
            if completed_session:
                logger.info(f"8. Sesión completada:")
                logger.info(f"   Confianza general: {completed_session.overall_confidence:.2f}")
                logger.info(f"   Calidad general: {completed_session.overall_quality:.2f}")
            
            # 9. Liberar presupuesto
            released = budget_forcing.release_budget(allocation_id)
            logger.info(f"9. Presupuesto liberado: {released}")
        
        # Mostrar estadísticas finales
        rewiring_stats = rewiring_system.get_expert_graph_metrics()
        memagent_stats = memagent.get_memory_stats()
        attention_stats = duo_attention.get_attention_stats()
        budget_stats = budget_forcing.get_budget_stats()
        thinking_stats = multi_round.get_multi_round_stats()
        
        logger.info(f"Estadísticas finales:")
        logger.info(f"  Rewiring: {rewiring_stats['performance_metrics']['total_queries_routed']} queries")
        logger.info(f"  MemAgent: {memagent_stats['current_tokens']} tokens utilizados")
        logger.info(f"  DuoAttention: {attention_stats['total_heads']} cabezas activas")
        logger.info(f"  Budget: {budget_stats['budget_stats']['approved_requests']} requests aprobados")
        logger.info(f"  Thinking: {thinking_stats['multi_round_stats']['completed_sessions']} sesiones completadas")
        
        logger.info("PASS - Integración de Optimizaciones")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Integración de Optimizaciones: {e}")
        return False

def main():
    """Función principal de test."""
    logger.info("Iniciando tests de Fase 7 - Advanced Optimizations")
    
    tests = [
        ("Rewiring Experts", test_rewiring_experts),
        ("MemAgent", test_memagent),
        ("DuoAttention", test_duo_attention),
        ("Budget Forcing", test_budget_forcing),
        ("Multi-round Thinking", test_multi_round_thinking),
        ("Integración de Optimizaciones", test_integration_optimizations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Ejecutando test: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    logger.info(f"\n{'='*60}")
    logger.info("RESUMEN DE TESTS - FASE 7")
    logger.info(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nResultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("🎉 Todos los tests de Fase 7 pasaron exitosamente!")
        logger.info("🚀 Sistema de optimizaciones avanzadas completamente funcional!")
        return True
    else:
        logger.error(f"❌ {total - passed} tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
