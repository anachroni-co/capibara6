#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fase 6 T5X - Test mejorado con integración T5X y optimizaciones TPU.
"""

import logging
import json
import os
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_t5x_integration():
    """Test de integración T5X."""
    logger.info("=== Test T5X Integration ===")
    
    try:
        from finetuning.t5x_integration import T5XManager, T5XModelSize, T5XBackend
        
        # Crear manager T5X
        manager = T5XManager()
        
        # Crear configuración T5X para modelo base
        t5x_config = manager.create_t5x_config(
            model_size=T5XModelSize.BASE,
            backend=T5XBackend.XMANAGER
        )
        
        logger.info(f"Configuración T5X creada: {t5x_config.model_size.value}")
        logger.info(f"Backend: {t5x_config.backend.value}")
        logger.info(f"TPU: {t5x_config.tpu_type} ({t5x_config.tpu_cores} cores)")
        
        # Crear job T5X
        job = manager.create_t5x_job(t5x_config, "test_t5x_base")
        
        logger.info(f"Job T5X creado: {job.job_id}")
        logger.info(f"Estado: {job.status}")
        
        # Crear configuración gin personalizada
        custom_config = {
            'mixture_or_task_name': 'capibara6_python_expert',
            'num_train_steps': 500000,
            'learning_rate': 0.0005,
            'batch_size': 16
        }
        
        gin_file = manager.create_custom_gin_config(
            job.job_id,
            T5XModelSize.BASE,
            custom_config
        )
        
        logger.info(f"Configuración gin personalizada: {gin_file}")
        
        # Simular monitoreo
        status = manager.monitor_t5x_job(job.job_id)
        logger.info(f"Estado del job: {status['status']}")
        
        # Mostrar estadísticas
        stats = manager.get_t5x_stats()
        logger.info(f"Estadísticas T5X: {stats}")
        
        logger.info("PASS - T5X Integration")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - T5X Integration: {e}")
        return False

def test_advanced_checkpointing():
    """Test del sistema de checkpointing avanzado."""
    logger.info("=== Test Advanced Checkpointing ===")
    
    try:
        from finetuning.advanced_checkpointing import (
            AdvancedCheckpointManager, 
            CheckpointConfig, 
            CheckpointFormat
        )
        import numpy as np
        
        # Crear manager de checkpointing
        config = CheckpointConfig(
            save_dir="backend/models/checkpoints_test",
            max_checkpoints=5,
            save_frequency=1000,
            compression=True,
            formats=[CheckpointFormat.T5X_NATIVE, CheckpointFormat.HUGGINGFACE]
        )
        
        manager = AdvancedCheckpointManager(config=config)
        
        # Crear checkpoint de prueba
        model_state = {
            'weights': np.random.randn(100, 100),
            'biases': np.random.randn(100),
            'config': {'hidden_size': 100, 'num_layers': 4}
        }
        
        optimizer_state = {
            'lr': 0.001,
            'momentum': 0.9,
            'step': 1000
        }
        
        training_state = {
            'epoch': 5,
            'best_loss': 0.5,
            'patience': 3
        }
        
        checkpoint_id = manager.save_checkpoint(
            model_state=model_state,
            optimizer_state=optimizer_state,
            training_state=training_state,
            step=1000,
            epoch=5,
            loss=0.5,
            learning_rate=0.001,
            model_name="test_model",
            tags=["test", "t5x"]
        )
        
        logger.info(f"Checkpoint guardado: {checkpoint_id}")
        
        # Listar checkpoints
        checkpoints = manager.list_checkpoints(limit=5)
        logger.info(f"Checkpoints disponibles: {len(checkpoints)}")
        
        # Cargar checkpoint
        loaded_data = manager.load_checkpoint(checkpoint_id, CheckpointFormat.T5X_NATIVE)
        if loaded_data:
            logger.info(f"Checkpoint cargado exitosamente")
            logger.info(f"Keys: {list(loaded_data.keys())}")
        
        # Mostrar estadísticas
        stats = manager.get_checkpoint_stats()
        logger.info(f"Estadísticas de checkpointing: {stats}")
        
        logger.info("PASS - Advanced Checkpointing")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Advanced Checkpointing: {e}")
        return False

def test_tpu_optimizer():
    """Test del optimizador TPU."""
    logger.info("=== Test TPU Optimizer ===")
    
    try:
        from finetuning.tpu_optimizer import (
            TPUOptimizer, 
            TPUType, 
            OptimizationLevel
        )
        
        # Crear optimizador TPU
        optimizer = TPUOptimizer()
        
        # Crear configuración TPU V5e-64
        tpu_config = optimizer.create_tpu_config(TPUType.V5E_64, OptimizationLevel.AGGRESSIVE)
        logger.info(f"Configuración TPU: {tpu_config.tpu_type.value} ({tpu_config.cores} cores)")
        
        # Crear optimización para modelo base
        optimization = optimizer.optimize_for_model(
            model_size='base',
            tpu_type=TPUType.V5E_64,
            target_throughput=200.0,  # TFLOPs
            memory_constraint=0.8     # 80% de memoria disponible
        )
        
        logger.info(f"Optimización creada: {optimization.optimization_id}")
        logger.info(f"Batch size: {optimization.batch_size}")
        logger.info(f"Learning rate: {optimization.learning_rate}")
        logger.info(f"Métricas: {optimization.performance_metrics}")
        
        # Generar configuración T5X
        t5x_config_file = optimizer.generate_t5x_config(optimization)
        logger.info(f"Configuración T5X: {t5x_config_file}")
        
        # Listar optimizaciones
        optimizations = optimizer.list_optimizations(limit=5)
        logger.info(f"Optimizaciones disponibles: {len(optimizations)}")
        
        # Mostrar estadísticas
        stats = optimizer.get_optimization_stats()
        logger.info(f"Estadísticas TPU: {stats}")
        
        logger.info("PASS - TPU Optimizer")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - TPU Optimizer: {e}")
        return False

def test_integration_t5x():
    """Test de integración completa con T5X."""
    logger.info("=== Test Integración Completa T5X ===")
    
    try:
        # Crear directorios necesarios
        os.makedirs("backend/data/t5x_configs", exist_ok=True)
        os.makedirs("backend/data/t5x_jobs", exist_ok=True)
        os.makedirs("backend/data/tpu_configs", exist_ok=True)
        os.makedirs("backend/data/tpu_optimizations", exist_ok=True)
        os.makedirs("backend/models/checkpoints", exist_ok=True)
        
        logger.info("Directorios T5X creados")
        
        # Test completo del pipeline T5X
        from finetuning.t5x_integration import T5XManager, T5XModelSize, T5XBackend
        from finetuning.tpu_optimizer import TPUOptimizer, TPUType, OptimizationLevel
        from finetuning.advanced_checkpointing import AdvancedCheckpointManager, CheckpointFormat
        from finetuning.playbook_consolidator import PlaybookConsolidator
        from finetuning.moe_dataset_generator import MoEDatasetGenerator
        
        # 1. Optimizar para TPU V5e-64
        tpu_optimizer = TPUOptimizer()
        optimization = tpu_optimizer.optimize_for_model(
            model_size='base',
            tpu_type=TPUType.V5E_64,
            target_throughput=200.0
        )
        logger.info(f"1. Optimización TPU creada: {optimization.optimization_id}")
        
        # 2. Crear configuración T5X
        t5x_manager = T5XManager()
        t5x_config = t5x_manager.create_t5x_config(
            model_size=T5XModelSize.BASE,
            backend=T5XBackend.XMANAGER
        )
        logger.info(f"2. Configuración T5X creada: {t5x_config.tpu_cores} cores")
        
        # 3. Crear job de entrenamiento
        job = t5x_manager.create_t5x_job(t5x_config, "capibara6_base_t5x")
        logger.info(f"3. Job T5X creado: {job.job_id}")
        
        # 4. Configurar checkpointing avanzado
        checkpoint_manager = AdvancedCheckpointManager()
        logger.info("4. Sistema de checkpointing configurado")
        
        # 5. Consolidar playbooks
        consolidator = PlaybookConsolidator()
        consolidated_playbooks = consolidator.consolidate_playbooks()
        logger.info(f"5. Playbooks consolidados: {len(consolidated_playbooks)}")
        
        # 6. Generar datasets MoE
        generator = MoEDatasetGenerator()
        moe_datasets = generator.generate_moe_datasets()
        logger.info(f"6. Datasets MoE generados: {len(moe_datasets)}")
        
        # 7. Generar configuración gin personalizada
        custom_config = {
            'mixture_or_task_name': 'capibara6_moe',
            'num_train_steps': 1000000,
            'learning_rate': optimization.learning_rate,
            'batch_size': optimization.batch_size
        }
        
        gin_file = t5x_manager.create_custom_gin_config(
            job.job_id,
            T5XModelSize.BASE,
            custom_config
        )
        logger.info(f"7. Configuración gin generada: {gin_file}")
        
        # 8. Simular entrenamiento
        status = t5x_manager.monitor_t5x_job(job.job_id)
        logger.info(f"8. Estado del entrenamiento: {status['status']}")
        
        # Mostrar estadísticas finales
        t5x_stats = t5x_manager.get_t5x_stats()
        tpu_stats = tpu_optimizer.get_optimization_stats()
        checkpoint_stats = checkpoint_manager.get_checkpoint_stats()
        
        logger.info(f"Estadísticas T5X: {t5x_stats}")
        logger.info(f"Estadísticas TPU: {tpu_stats}")
        logger.info(f"Estadísticas Checkpointing: {checkpoint_stats}")
        
        logger.info("PASS - Integración Completa T5X")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Integración Completa T5X: {e}")
        return False

def test_performance_benchmarks():
    """Test de benchmarks de rendimiento."""
    logger.info("=== Test Performance Benchmarks ===")
    
    try:
        from finetuning.tpu_optimizer import TPUOptimizer, TPUType
        from finetuning.t5x_integration import T5XManager, T5XModelSize
        
        # Crear optimizador
        optimizer = TPUOptimizer()
        
        # Benchmark diferentes tamaños de modelo
        model_sizes = ['small', 'base', 'large', 'xl']
        results = {}
        
        for model_size in model_sizes:
            optimization = optimizer.optimize_for_model(
                model_size=model_size,
                tpu_type=TPUType.V5E_64
            )
            
            results[model_size] = {
                'batch_size': optimization.batch_size,
                'throughput_tflops': optimization.performance_metrics.get('theoretical_throughput_tflops', 0),
                'memory_usage_gb': optimization.performance_metrics.get('memory_usage_gb', 0),
                'memory_efficiency': optimization.performance_metrics.get('memory_efficiency', 0),
                'estimated_speedup': optimization.performance_metrics.get('estimated_speedup', 1.0)
            }
            
            logger.info(f"Modelo {model_size}: {results[model_size]}")
        
        # Calcular métricas agregadas
        total_throughput = sum(r['throughput_tflops'] for r in results.values())
        avg_memory_efficiency = sum(r['memory_efficiency'] for r in results.values()) / len(results)
        avg_speedup = sum(r['estimated_speedup'] for r in results.values()) / len(results)
        
        logger.info(f"Throughput total: {total_throughput:.2f} TFLOPs")
        logger.info(f"Eficiencia de memoria promedio: {avg_memory_efficiency:.2f}")
        logger.info(f"Speedup promedio: {avg_speedup:.2f}x")
        
        logger.info("PASS - Performance Benchmarks")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Performance Benchmarks: {e}")
        return False

def main():
    """Función principal de test."""
    logger.info("Iniciando tests de Fase 6 T5X - Fine-tuning Pipeline Mejorado")
    
    tests = [
        ("T5X Integration", test_t5x_integration),
        ("Advanced Checkpointing", test_advanced_checkpointing),
        ("TPU Optimizer", test_tpu_optimizer),
        ("Integración Completa T5X", test_integration_t5x),
        ("Performance Benchmarks", test_performance_benchmarks)
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
    logger.info("RESUMEN DE TESTS - FASE 6 T5X")
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
        logger.info("🎉 Todos los tests de Fase 6 T5X pasaron exitosamente!")
        logger.info("🚀 Sistema de fine-tuning con T5X completamente funcional!")
        return True
    else:
        logger.error(f"❌ {total - passed} tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
