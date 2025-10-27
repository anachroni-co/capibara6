#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fase 6 - Fine-tuning Pipeline
"""

import logging
import json
import os
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_playbook_consolidator():
    """Test del PlaybookConsolidator."""
    logger.info("=== Test PlaybookConsolidator ===")
    
    try:
        from finetuning.playbook_consolidator import PlaybookConsolidator, AgentFilter
        
        # Crear consolidator
        consolidator = PlaybookConsolidator(top_k=100)
        
        # Crear filtro de agentes
        agent_filter = AgentFilter(
            min_graduation_score=0.8,
            min_interactions=50,
            min_success_rate=0.8,
            min_domain_expertise=0.7,
            max_age_days=30,
            required_domains=['python', 'sql']
        )
        
        # Consolidar playbooks
        consolidated = consolidator.consolidate_playbooks(agent_filter=agent_filter)
        
        logger.info(f"Playbooks consolidados: {len(consolidated)}")
        
        # Mostrar estadísticas
        stats = consolidator.get_consolidation_stats()
        logger.info(f"Estadísticas: {stats}")
        
        # Analizar calidad
        analysis = consolidator.analyze_playbook_quality('python')
        logger.info(f"Análisis de calidad Python: {analysis}")
        
        logger.info("PASS - PlaybookConsolidator")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - PlaybookConsolidator: {e}")
        return False

def test_e2b_log_processor():
    """Test del E2BLogProcessor."""
    logger.info("=== Test E2BLogProcessor ===")
    
    try:
        from finetuning.e2b_log_processor import E2BLogProcessor
        
        # Crear processor
        processor = E2BLogProcessor(min_success_rate=0.7)
        
        # Procesar logs
        processed_data = processor.process_e2b_logs(
            time_range_days=7,
            languages=['python', 'javascript'],
            min_quality_score=0.6
        )
        
        logger.info(f"Datos procesados: {len(processed_data)} lenguajes")
        
        # Mostrar estadísticas
        stats = processor.get_processing_stats()
        logger.info(f"Estadísticas: {stats}")
        
        logger.info("PASS - E2BLogProcessor")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - E2BLogProcessor: {e}")
        return False

def test_moe_dataset_generator():
    """Test del MoEDatasetGenerator."""
    logger.info("=== Test MoEDatasetGenerator ===")
    
    try:
        from finetuning.moe_dataset_generator import MoEDatasetGenerator
        
        # Crear generator
        generator = MoEDatasetGenerator()
        
        # Generar datasets MoE
        moe_datasets = generator.generate_moe_datasets(
            domains=['python', 'sql', 'javascript'],
            include_routing=True
        )
        
        logger.info(f"Datasets MoE generados: {len(moe_datasets)}")
        
        # Mostrar estadísticas
        stats = generator.get_generation_stats()
        logger.info(f"Estadísticas: {stats}")
        
        # Analizar calidad
        for domain in moe_datasets.keys():
            analysis = generator.analyze_dataset_quality(domain)
            logger.info(f"Análisis {domain}: {analysis.get('total_examples', 0)} ejemplos")
        
        logger.info("PASS - MoEDatasetGenerator")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - MoEDatasetGenerator: {e}")
        return False

def test_lora_config():
    """Test del LoRAConfigManager."""
    logger.info("=== Test LoRAConfigManager ===")
    
    try:
        from finetuning.lora_config import LoRAConfigManager, LoRATaskType
        
        # Crear manager
        manager = LoRAConfigManager()
        
        # Listar configuraciones predefinidas
        presets = manager.list_preset_configs()
        logger.info(f"Configuraciones predefinidas: {presets}")
        
        # Obtener configuración 20B QLoRA
        config_20b = manager.get_preset_config("20b_qlora")
        if config_20b:
            logger.info(f"Configuración 20B: {config_20b.config_name}")
            logger.info(f"LoRA r: {config_20b.lora_config.r}")
            logger.info(f"Learning rate: {config_20b.training_config.learning_rate}")
            
            # Guardar configuración
            saved = manager.save_config(config_20b)
            logger.info(f"Configuración guardada: {saved}")
            
            # Generar script
            script_saved = manager.save_training_script(config_20b)
            logger.info(f"Script generado: {script_saved}")
        
        # Crear configuración personalizada
        custom_config = manager.create_custom_config(
            config_name="test_custom",
            model_name="microsoft/DialoGPT-medium",
            dataset_path="backend/data/moe_datasets",
            output_dir="backend/models/test_custom",
            use_qlora=True,
            r=8,
            lora_alpha=16,
            learning_rate=1e-4
        )
        
        logger.info(f"Configuración personalizada: {custom_config.config_name}")
        
        logger.info("PASS - LoRAConfigManager")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - LoRAConfigManager: {e}")
        return False

def test_distributed_training():
    """Test del DistributedTrainingManager."""
    logger.info("=== Test DistributedTrainingManager ===")
    
    try:
        from finetuning.distributed_training import (
            DistributedTrainingManager, 
            InfrastructureType, 
            TrainingBackend
        )
        
        # Crear manager
        manager = DistributedTrainingManager()
        
        # Crear configuración distribuida
        dist_config = manager.create_distributed_config(
            model_size="20b",
            infrastructure=InfrastructureType.GOOGLE_CLOUD,
            backend=TrainingBackend.DEEPSPEED
        )
        
        logger.info(f"Configuración distribuida: {dist_config.world_size} GPUs")
        logger.info(f"Backend: {dist_config.backend.value}")
        logger.info(f"Master: {dist_config.master_addr}:{dist_config.master_port}")
        
        # Crear job de entrenamiento
        job = manager.create_training_job(
            config_name="test_20b",
            distributed_config=dist_config,
            training_script_path="backend/scripts/train_test_20b.py"
        )
        
        logger.info(f"Job creado: {job.job_id}")
        logger.info(f"Estado: {job.status}")
        
        # Simular monitoreo
        status = manager.monitor_training_job(job.job_id)
        logger.info(f"Estado del job: {status['status']}")
        
        # Mostrar estadísticas
        stats = manager.get_training_stats()
        logger.info(f"Estadísticas: {stats}")
        
        logger.info("PASS - DistributedTrainingManager")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - DistributedTrainingManager: {e}")
        return False

def test_integration():
    """Test de integración completa."""
    logger.info("=== Test Integración Fase 6 ===")
    
    try:
        # Crear directorios necesarios
        os.makedirs("backend/data/playbooks", exist_ok=True)
        os.makedirs("backend/data/e2b_logs", exist_ok=True)
        os.makedirs("backend/data/consolidated_playbooks", exist_ok=True)
        os.makedirs("backend/data/training_datasets", exist_ok=True)
        os.makedirs("backend/data/moe_datasets", exist_ok=True)
        os.makedirs("backend/data/finetuning_configs", exist_ok=True)
        os.makedirs("backend/data/training_jobs", exist_ok=True)
        os.makedirs("backend/scripts", exist_ok=True)
        
        logger.info("Directorios creados")
        
        # Test completo del pipeline
        from finetuning.playbook_consolidator import PlaybookConsolidator
        from finetuning.e2b_log_processor import E2BLogProcessor
        from finetuning.moe_dataset_generator import MoEDatasetGenerator
        from finetuning.lora_config import LoRAConfigManager
        from finetuning.distributed_training import DistributedTrainingManager, InfrastructureType, TrainingBackend
        
        # 1. Consolidar playbooks
        consolidator = PlaybookConsolidator()
        consolidated_playbooks = consolidator.consolidate_playbooks()
        logger.info(f"1. Playbooks consolidados: {len(consolidated_playbooks)}")
        
        # 2. Procesar logs E2B
        processor = E2BLogProcessor()
        processed_logs = processor.process_e2b_logs()
        logger.info(f"2. Logs procesados: {len(processed_logs)} lenguajes")
        
        # 3. Generar datasets MoE
        generator = MoEDatasetGenerator()
        moe_datasets = generator.generate_moe_datasets()
        logger.info(f"3. Datasets MoE generados: {len(moe_datasets)}")
        
        # 4. Configurar LoRA
        lora_manager = LoRAConfigManager()
        config_20b = lora_manager.get_preset_config("20b_qlora")
        if config_20b:
            lora_manager.save_config(config_20b)
            lora_manager.save_training_script(config_20b)
            logger.info("4. Configuración LoRA guardada")
        
        # 5. Configurar entrenamiento distribuido
        dist_manager = DistributedTrainingManager()
        dist_config = dist_manager.create_distributed_config(
            model_size="20b",
            infrastructure=InfrastructureType.GOOGLE_CLOUD,
            backend=TrainingBackend.DEEPSPEED
        )
        
        job = dist_manager.create_training_job(
            config_name="20b_qlora",
            distributed_config=dist_config,
            training_script_path="backend/scripts/train_20b_qlora.py"
        )
        
        logger.info(f"5. Job de entrenamiento creado: {job.job_id}")
        
        logger.info("PASS - Integración Fase 6")
        return True
        
    except Exception as e:
        logger.error(f"FAIL - Integración Fase 6: {e}")
        return False

def main():
    """Función principal de test."""
    logger.info("Iniciando tests de Fase 6 - Fine-tuning Pipeline")
    
    tests = [
        ("PlaybookConsolidator", test_playbook_consolidator),
        ("E2BLogProcessor", test_e2b_log_processor),
        ("MoEDatasetGenerator", test_moe_dataset_generator),
        ("LoRAConfigManager", test_lora_config),
        ("DistributedTrainingManager", test_distributed_training),
        ("Integración Completa", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Ejecutando test: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error ejecutando test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    logger.info(f"\n{'='*50}")
    logger.info("RESUMEN DE TESTS - FASE 6")
    logger.info(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nResultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        logger.info("🎉 Todos los tests de Fase 6 pasaron exitosamente!")
        return True
    else:
        logger.error(f"❌ {total - passed} tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
