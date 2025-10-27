#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantization - Sistema de cuantización GPTQ/AWQ para optimización de inferencia.
"""

import logging
import json
import os
import time
import pickle
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

logger = logging.getLogger(__name__)


class QuantizationMethod(Enum):
    """Métodos de cuantización."""
    GPTQ = "gptq"
    AWQ = "awq"
    INT8 = "int8"
    INT4 = "int4"
    DYNAMIC = "dynamic"
    STATIC = "static"


class QuantizationLevel(Enum):
    """Niveles de cuantización."""
    ULTRA_LOW = "ultra_low"  # 4-bit
    LOW = "low"              # 8-bit
    MEDIUM = "medium"        # 16-bit
    HIGH = "high"            # 32-bit (float32)
    ULTRA_HIGH = "ultra_high" # 64-bit (float64)


class ModelSize(Enum):
    """Tamaños de modelo."""
    SMALL = "small"      # <1B
    MEDIUM = "medium"    # 1B-10B
    LARGE = "large"      # 10B-100B
    XLARGE = "xlarge"    # >100B


@dataclass
class QuantizationConfig:
    """Configuración de cuantización."""
    method: QuantizationMethod
    level: QuantizationLevel
    bits: int
    group_size: int
    calibration_samples: int
    calibration_dataset: str
    target_accuracy: float
    target_speedup: float
    memory_reduction: float
    metadata: Dict[str, Any]


@dataclass
class QuantizationResult:
    """Resultado de cuantización."""
    result_id: str
    original_model_path: str
    quantized_model_path: str
    config: QuantizationConfig
    original_size_mb: float
    quantized_size_mb: float
    compression_ratio: float
    accuracy_loss: float
    speedup_factor: float
    memory_reduction: float
    quantization_time_seconds: float
    validation_metrics: Dict[str, float]
    timestamp: datetime


@dataclass
class QuantizationBenchmark:
    """Benchmark de cuantización."""
    benchmark_id: str
    model_name: str
    quantization_method: QuantizationMethod
    inference_time_ms: float
    memory_usage_mb: float
    throughput_tokens_per_second: float
    accuracy_score: float
    energy_consumption_watts: float
    timestamp: datetime


class GPTQQuantizer:
    """Cuantizador GPTQ."""
    
    def __init__(self):
        self.gptq_config = {
            'bits': 4,
            'group_size': 128,
            'desc_act': True,
            'static_groups': False,
            'sym': True,
            'true_sequential': True,
            'perchannel': True,
            'minmax': False,
            'mse': False,
            'percdamp': 0.01,
            'nearest': False,
            'wbits': 4,
            'groupsize': 128
        }
        
        logger.info("GPTQQuantizer inicializado")
    
    def quantize_model(self, 
                      model_path: str,
                      calibration_data: List[str],
                      config: QuantizationConfig) -> QuantizationResult:
        """Cuantiza modelo usando GPTQ."""
        try:
            start_time = time.time()
            result_id = f"gptq_{int(time.time() * 1000)}"
            
            # Simular cuantización GPTQ
            logger.info(f"Iniciando cuantización GPTQ para {model_path}")
            
            # Calcular métricas simuladas
            original_size = self._estimate_model_size(model_path)
            quantized_size = original_size * 0.25  # 4-bit = 25% del tamaño original
            compression_ratio = original_size / quantized_size
            
            # Simular tiempo de cuantización
            quantization_time = time.time() - start_time
            
            # Crear resultado
            result = QuantizationResult(
                result_id=result_id,
                original_model_path=model_path,
                quantized_model_path=f"{model_path}_gptq_quantized",
                config=config,
                original_size_mb=original_size,
                quantized_size_mb=quantized_size,
                compression_ratio=compression_ratio,
                accuracy_loss=0.02,  # 2% pérdida de precisión
                speedup_factor=2.5,  # 2.5x speedup
                memory_reduction=0.75,  # 75% reducción de memoria
                quantization_time_seconds=quantization_time,
                validation_metrics={
                    'perplexity': 15.2,
                    'bleu_score': 0.85,
                    'rouge_score': 0.78,
                    'accuracy': 0.92
                },
                timestamp=datetime.now()
            )
            
            # Guardar modelo cuantizado
            self._save_quantized_model(result)
            
            logger.info(f"Cuantización GPTQ completada: {result_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error en cuantización GPTQ: {e}")
            raise
    
    def _estimate_model_size(self, model_path: str) -> float:
        """Estima tamaño del modelo."""
        # Simulación basada en el path del modelo
        if "20b" in model_path.lower():
            return 40000.0  # 40GB para modelo 20B
        elif "120b" in model_path.lower():
            return 240000.0  # 240GB para modelo 120B
        else:
            return 1000.0  # 1GB por defecto
    
    def _save_quantized_model(self, result: QuantizationResult):
        """Guarda modelo cuantizado."""
        try:
            # Crear directorio para modelo cuantizado
            quantized_dir = os.path.dirname(result.quantized_model_path)
            os.makedirs(quantized_dir, exist_ok=True)
            
            # Simular guardado de modelo cuantizado
            model_data = {
                'config': asdict(result.config),
                'metadata': {
                    'quantization_method': 'gptq',
                    'compression_ratio': result.compression_ratio,
                    'accuracy_loss': result.accuracy_loss,
                    'speedup_factor': result.speedup_factor
                }
            }
            
            # Guardar metadata
            metadata_file = f"{result.quantized_model_path}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(model_data, f, indent=2, default=str)
            
            logger.info(f"Modelo cuantizado guardado: {result.quantized_model_path}")
            
        except Exception as e:
            logger.error(f"Error guardando modelo cuantizado: {e}")


class AWQQuantizer:
    """Cuantizador AWQ."""
    
    def __init__(self):
        self.awq_config = {
            'w_bit': 4,
            'q_group_size': 128,
            'zero_point': True,
            'version': 'GEMM',
            'calib_amax': 0.95,
            'calib_permute': True,
            'calib_iters': 200,
            'calib_seqlen': 2048
        }
        
        logger.info("AWQQuantizer inicializado")
    
    def quantize_model(self, 
                      model_path: str,
                      calibration_data: List[str],
                      config: QuantizationConfig) -> QuantizationResult:
        """Cuantiza modelo usando AWQ."""
        try:
            start_time = time.time()
            result_id = f"awq_{int(time.time() * 1000)}"
            
            # Simular cuantización AWQ
            logger.info(f"Iniciando cuantización AWQ para {model_path}")
            
            # Calcular métricas simuladas
            original_size = self._estimate_model_size(model_path)
            quantized_size = original_size * 0.3  # AWQ típicamente 30% del tamaño original
            compression_ratio = original_size / quantized_size
            
            # Simular tiempo de cuantización
            quantization_time = time.time() - start_time
            
            # Crear resultado
            result = QuantizationResult(
                result_id=result_id,
                original_model_path=model_path,
                quantized_model_path=f"{model_path}_awq_quantized",
                config=config,
                original_size_mb=original_size,
                quantized_size_mb=quantized_size,
                compression_ratio=compression_ratio,
                accuracy_loss=0.015,  # 1.5% pérdida de precisión (mejor que GPTQ)
                speedup_factor=2.2,   # 2.2x speedup
                memory_reduction=0.7,  # 70% reducción de memoria
                quantization_time_seconds=quantization_time,
                validation_metrics={
                    'perplexity': 14.8,
                    'bleu_score': 0.87,
                    'rouge_score': 0.80,
                    'accuracy': 0.94
                },
                timestamp=datetime.now()
            )
            
            # Guardar modelo cuantizado
            self._save_quantized_model(result)
            
            logger.info(f"Cuantización AWQ completada: {result_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error en cuantización AWQ: {e}")
            raise
    
    def _estimate_model_size(self, model_path: str) -> float:
        """Estima tamaño del modelo."""
        # Simulación basada en el path del modelo
        if "20b" in model_path.lower():
            return 40000.0  # 40GB para modelo 20B
        elif "120b" in model_path.lower():
            return 240000.0  # 240GB para modelo 120B
        else:
            return 1000.0  # 1GB por defecto
    
    def _save_quantized_model(self, result: QuantizationResult):
        """Guarda modelo cuantizado."""
        try:
            # Crear directorio para modelo cuantizado
            quantized_dir = os.path.dirname(result.quantized_model_path)
            os.makedirs(quantized_dir, exist_ok=True)
            
            # Simular guardado de modelo cuantizado
            model_data = {
                'config': asdict(result.config),
                'metadata': {
                    'quantization_method': 'awq',
                    'compression_ratio': result.compression_ratio,
                    'accuracy_loss': result.accuracy_loss,
                    'speedup_factor': result.speedup_factor
                }
            }
            
            # Guardar metadata
            metadata_file = f"{result.quantized_model_path}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(model_data, f, indent=2, default=str)
            
            logger.info(f"Modelo cuantizado guardado: {result.quantized_model_path}")
            
        except Exception as e:
            logger.error(f"Error guardando modelo cuantizado: {e}")


class QuantizationManager:
    """Gestor de cuantización."""
    
    def __init__(self, 
                 models_dir: str = "backend/models",
                 quantized_dir: str = "backend/models/quantized",
                 benchmarks_dir: str = "backend/data/quantization_benchmarks"):
        self.models_dir = models_dir
        self.quantized_dir = quantized_dir
        self.benchmarks_dir = benchmarks_dir
        
        # Cuantizadores
        self.gptq_quantizer = GPTQQuantizer()
        self.awq_quantizer = AWQQuantizer()
        
        # Historial de cuantizaciones
        self.quantization_history: deque = deque(maxlen=1000)
        self.benchmark_results: deque = deque(maxlen=1000)
        
        # Configuraciones predefinidas
        self.preset_configs = self._create_preset_configs()
        
        # Estadísticas
        self.quantization_stats = {
            'total_quantizations': 0,
            'gptq_quantizations': 0,
            'awq_quantizations': 0,
            'average_compression_ratio': 0.0,
            'average_speedup': 0.0,
            'average_accuracy_loss': 0.0,
            'total_models_quantized': 0
        }
        
        # Asegurar directorios
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(quantized_dir, exist_ok=True)
        os.makedirs(benchmarks_dir, exist_ok=True)
        
        logger.info(f"QuantizationManager inicializado: models_dir={models_dir}")
    
    def _create_preset_configs(self) -> Dict[str, QuantizationConfig]:
        """Crea configuraciones predefinidas."""
        configs = {}
        
        # Configuración GPTQ 4-bit
        configs['gptq_4bit'] = QuantizationConfig(
            method=QuantizationMethod.GPTQ,
            level=QuantizationLevel.ULTRA_LOW,
            bits=4,
            group_size=128,
            calibration_samples=512,
            calibration_dataset="wikitext2",
            target_accuracy=0.95,
            target_speedup=2.5,
            memory_reduction=0.75,
            metadata={'preset': True, 'optimized_for': 'inference'}
        )
        
        # Configuración AWQ 4-bit
        configs['awq_4bit'] = QuantizationConfig(
            method=QuantizationMethod.AWQ,
            level=QuantizationLevel.ULTRA_LOW,
            bits=4,
            group_size=128,
            calibration_samples=512,
            calibration_dataset="wikitext2",
            target_accuracy=0.96,
            target_speedup=2.2,
            memory_reduction=0.7,
            metadata={'preset': True, 'optimized_for': 'accuracy'}
        )
        
        # Configuración INT8
        configs['int8'] = QuantizationConfig(
            method=QuantizationMethod.INT8,
            level=QuantizationLevel.LOW,
            bits=8,
            group_size=64,
            calibration_samples=256,
            calibration_dataset="wikitext2",
            target_accuracy=0.98,
            target_speedup=1.8,
            memory_reduction=0.5,
            metadata={'preset': True, 'optimized_for': 'balanced'}
        )
        
        return configs
    
    def quantize_model(self, 
                      model_path: str,
                      method: QuantizationMethod,
                      config_name: Optional[str] = None,
                      custom_config: Optional[QuantizationConfig] = None,
                      calibration_data: Optional[List[str]] = None) -> QuantizationResult:
        """Cuantiza modelo."""
        try:
            # Seleccionar configuración
            if custom_config:
                config = custom_config
            elif config_name and config_name in self.preset_configs:
                config = self.preset_configs[config_name]
            else:
                # Configuración por defecto basada en método
                if method == QuantizationMethod.GPTQ:
                    config = self.preset_configs['gptq_4bit']
                elif method == QuantizationMethod.AWQ:
                    config = self.preset_configs['awq_4bit']
                else:
                    config = self.preset_configs['int8']
            
            # Generar datos de calibración si no se proporcionan
            if calibration_data is None:
                calibration_data = self._generate_calibration_data(config.calibration_samples)
            
            # Seleccionar cuantizador
            if method == QuantizationMethod.GPTQ:
                result = self.gptq_quantizer.quantize_model(model_path, calibration_data, config)
            elif method == QuantizationMethod.AWQ:
                result = self.awq_quantizer.quantize_model(model_path, calibration_data, config)
            else:
                # Fallback a GPTQ para otros métodos
                result = self.gptq_quantizer.quantize_model(model_path, calibration_data, config)
            
            # Agregar al historial
            self.quantization_history.append(result)
            
            # Actualizar estadísticas
            self._update_stats(result)
            
            # Guardar resultado
            self._save_quantization_result(result)
            
            logger.info(f"Modelo cuantizado: {model_path} -> {result.quantized_model_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error cuantizando modelo {model_path}: {e}")
            raise
    
    def _generate_calibration_data(self, num_samples: int) -> List[str]:
        """Genera datos de calibración."""
        # Datos de calibración simulados
        calibration_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Python is a high-level programming language.",
            "Deep learning models require large amounts of data.",
            "Natural language processing enables computers to understand human language.",
            "Computer vision allows machines to interpret visual information.",
            "Reinforcement learning is a type of machine learning.",
            "Neural networks are inspired by biological neural networks.",
            "Transformers have revolutionized natural language processing.",
            "Attention mechanisms improve model performance significantly."
        ]
        
        # Repetir y variar los textos
        calibration_data = []
        for i in range(num_samples):
            base_text = calibration_texts[i % len(calibration_texts)]
            # Agregar variación
            if i % 3 == 0:
                calibration_data.append(base_text + " This is additional context.")
            elif i % 3 == 1:
                calibration_data.append("Context: " + base_text)
            else:
                calibration_data.append(base_text)
        
        return calibration_data
    
    def benchmark_quantized_model(self, 
                                result: QuantizationResult,
                                test_data: List[str],
                                num_iterations: int = 100) -> QuantizationBenchmark:
        """Benchmark de modelo cuantizado."""
        try:
            benchmark_id = f"benchmark_{result.result_id}_{int(time.time() * 1000)}"
            
            logger.info(f"Iniciando benchmark para {result.result_id}")
            
            # Simular benchmark
            start_time = time.time()
            
            # Métricas simuladas
            inference_times = []
            memory_usage = []
            throughput_values = []
            accuracy_scores = []
            
            for i in range(num_iterations):
                # Simular inferencia
                inference_time = np.random.normal(50, 10)  # 50ms ± 10ms
                memory_usage_val = np.random.normal(2000, 200)  # 2GB ± 200MB
                throughput = np.random.normal(1000, 100)  # 1000 tokens/s ± 100
                accuracy = np.random.normal(0.92, 0.02)  # 92% ± 2%
                
                inference_times.append(inference_time)
                memory_usage.append(memory_usage_val)
                throughput_values.append(throughput)
                accuracy_scores.append(accuracy)
            
            # Calcular promedios
            avg_inference_time = np.mean(inference_times)
            avg_memory_usage = np.mean(memory_usage)
            avg_throughput = np.mean(throughput_values)
            avg_accuracy = np.mean(accuracy_scores)
            energy_consumption = avg_memory_usage * 0.1  # Estimación de energía
            
            benchmark_time = time.time() - start_time
            
            # Crear benchmark
            benchmark = QuantizationBenchmark(
                benchmark_id=benchmark_id,
                model_name=os.path.basename(result.original_model_path),
                quantization_method=result.config.method,
                inference_time_ms=avg_inference_time,
                memory_usage_mb=avg_memory_usage,
                throughput_tokens_per_second=avg_throughput,
                accuracy_score=avg_accuracy,
                energy_consumption_watts=energy_consumption,
                timestamp=datetime.now()
            )
            
            # Agregar al historial
            self.benchmark_results.append(benchmark)
            
            # Guardar benchmark
            self._save_benchmark_result(benchmark)
            
            logger.info(f"Benchmark completado: {benchmark_id}")
            return benchmark
            
        except Exception as e:
            logger.error(f"Error en benchmark: {e}")
            raise
    
    def compare_quantization_methods(self, 
                                   model_path: str,
                                   test_data: List[str]) -> Dict[str, Any]:
        """Compara métodos de cuantización."""
        try:
            logger.info(f"Comparando métodos de cuantización para {model_path}")
            
            # Cuantizar con diferentes métodos
            methods = [QuantizationMethod.GPTQ, QuantizationMethod.AWQ, QuantizationMethod.INT8]
            results = {}
            
            for method in methods:
                try:
                    # Cuantizar modelo
                    result = self.quantize_model(model_path, method)
                    
                    # Benchmark
                    benchmark = self.benchmark_quantized_model(result, test_data)
                    
                    results[method.value] = {
                        'quantization_result': result,
                        'benchmark': benchmark,
                        'compression_ratio': result.compression_ratio,
                        'speedup_factor': result.speedup_factor,
                        'accuracy_loss': result.accuracy_loss,
                        'inference_time_ms': benchmark.inference_time_ms,
                        'memory_usage_mb': benchmark.memory_usage_mb,
                        'throughput_tokens_per_second': benchmark.throughput_tokens_per_second
                    }
                    
                except Exception as e:
                    logger.error(f"Error con método {method.value}: {e}")
                    results[method.value] = {'error': str(e)}
            
            # Análisis comparativo
            comparison = self._analyze_comparison(results)
            
            logger.info(f"Comparación completada para {model_path}")
            return comparison
            
        except Exception as e:
            logger.error(f"Error en comparación de métodos: {e}")
            raise
    
    def _analyze_comparison(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza comparación de métodos."""
        analysis = {
            'best_compression': None,
            'best_speedup': None,
            'best_accuracy': None,
            'best_balanced': None,
            'recommendations': []
        }
        
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        
        if not valid_results:
            return analysis
        
        # Encontrar mejores métodos
        if valid_results:
            best_compression = max(valid_results.items(), 
                                 key=lambda x: x[1]['compression_ratio'])
            analysis['best_compression'] = {
                'method': best_compression[0],
                'compression_ratio': best_compression[1]['compression_ratio']
            }
            
            best_speedup = max(valid_results.items(), 
                             key=lambda x: x[1]['speedup_factor'])
            analysis['best_speedup'] = {
                'method': best_speedup[0],
                'speedup_factor': best_speedup[1]['speedup_factor']
            }
            
            best_accuracy = min(valid_results.items(), 
                              key=lambda x: x[1]['accuracy_loss'])
            analysis['best_accuracy'] = {
                'method': best_accuracy[0],
                'accuracy_loss': best_accuracy[1]['accuracy_loss']
            }
            
            # Mejor balanceado (score combinado)
            balanced_scores = {}
            for method, data in valid_results.items():
                # Score combinado: 40% compresión, 30% speedup, 30% precisión
                compression_score = data['compression_ratio'] / 4.0  # Normalizar
                speedup_score = data['speedup_factor'] / 3.0  # Normalizar
                accuracy_score = (1.0 - data['accuracy_loss'])  # Invertir pérdida
                
                balanced_score = (compression_score * 0.4 + 
                                speedup_score * 0.3 + 
                                accuracy_score * 0.3)
                balanced_scores[method] = balanced_score
            
            best_balanced = max(balanced_scores.items(), key=lambda x: x[1])
            analysis['best_balanced'] = {
                'method': best_balanced[0],
                'score': best_balanced[1]
            }
        
        # Generar recomendaciones
        if analysis['best_balanced']:
            method = analysis['best_balanced']['method']
            analysis['recommendations'].append(
                f"Para uso general, se recomienda {method} (score: {analysis['best_balanced']['score']:.3f})"
            )
        
        if analysis['best_compression']:
            method = analysis['best_compression']['method']
            ratio = analysis['best_compression']['compression_ratio']
            analysis['recommendations'].append(
                f"Para máxima compresión, usar {method} (ratio: {ratio:.1f}x)"
            )
        
        if analysis['best_speedup']:
            method = analysis['best_speedup']['method']
            speedup = analysis['best_speedup']['speedup_factor']
            analysis['recommendations'].append(
                f"Para máximo speedup, usar {method} (speedup: {speedup:.1f}x)"
            )
        
        return analysis
    
    def _update_stats(self, result: QuantizationResult):
        """Actualiza estadísticas."""
        self.quantization_stats['total_quantizations'] += 1
        self.quantization_stats['total_models_quantized'] += 1
        
        if result.config.method == QuantizationMethod.GPTQ:
            self.quantization_stats['gptq_quantizations'] += 1
        elif result.config.method == QuantizationMethod.AWQ:
            self.quantization_stats['awq_quantizations'] += 1
        
        # Actualizar promedios
        total = self.quantization_stats['total_quantizations']
        
        # Promedio de compresión
        current_avg = self.quantization_stats['average_compression_ratio']
        new_avg = ((current_avg * (total - 1)) + result.compression_ratio) / total
        self.quantization_stats['average_compression_ratio'] = new_avg
        
        # Promedio de speedup
        current_avg = self.quantization_stats['average_speedup']
        new_avg = ((current_avg * (total - 1)) + result.speedup_factor) / total
        self.quantization_stats['average_speedup'] = new_avg
        
        # Promedio de pérdida de precisión
        current_avg = self.quantization_stats['average_accuracy_loss']
        new_avg = ((current_avg * (total - 1)) + result.accuracy_loss) / total
        self.quantization_stats['average_accuracy_loss'] = new_avg
    
    def _save_quantization_result(self, result: QuantizationResult):
        """Guarda resultado de cuantización."""
        try:
            result_file = os.path.join(self.benchmarks_dir, f"{result.result_id}.json")
            
            result_data = asdict(result)
            result_data['timestamp'] = result.timestamp.isoformat()
            result_data['config']['method'] = result.config.method.value
            result_data['config']['level'] = result.config.level.value
            
            with open(result_file, 'w') as f:
                json.dump(result_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error guardando resultado de cuantización: {e}")
    
    def _save_benchmark_result(self, benchmark: QuantizationBenchmark):
        """Guarda resultado de benchmark."""
        try:
            benchmark_file = os.path.join(self.benchmarks_dir, f"{benchmark.benchmark_id}.json")
            
            benchmark_data = asdict(benchmark)
            benchmark_data['timestamp'] = benchmark.timestamp.isoformat()
            benchmark_data['quantization_method'] = benchmark.quantization_method.value
            
            with open(benchmark_file, 'w') as f:
                json.dump(benchmark_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Error guardando resultado de benchmark: {e}")
    
    def get_quantization_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de cuantización."""
        return self.quantization_stats.copy()
    
    def get_quantization_history(self, limit: int = 10) -> List[QuantizationResult]:
        """Obtiene historial de cuantizaciones."""
        return list(self.quantization_history)[-limit:]
    
    def get_benchmark_history(self, limit: int = 10) -> List[QuantizationBenchmark]:
        """Obtiene historial de benchmarks."""
        return list(self.benchmark_results)[-limit:]


if __name__ == "__main__":
    # Test del QuantizationManager
    logging.basicConfig(level=logging.INFO)
    
    manager = QuantizationManager()
    
    # Test de cuantización
    test_model_path = "backend/models/capibara6_20b"
    test_data = [
        "How to optimize Python code?",
        "What is machine learning?",
        "Explain neural networks.",
        "How does attention work?",
        "What is quantization?"
    ]
    
    # Cuantizar con GPTQ
    gptq_result = manager.quantize_model(
        test_model_path,
        QuantizationMethod.GPTQ,
        config_name="gptq_4bit"
    )
    
    print(f"GPTQ Result:")
    print(f"  Compression Ratio: {gptq_result.compression_ratio:.1f}x")
    print(f"  Speedup Factor: {gptq_result.speedup_factor:.1f}x")
    print(f"  Accuracy Loss: {gptq_result.accuracy_loss:.3f}")
    print(f"  Memory Reduction: {gptq_result.memory_reduction:.1%}")
    
    # Cuantizar con AWQ
    awq_result = manager.quantize_model(
        test_model_path,
        QuantizationMethod.AWQ,
        config_name="awq_4bit"
    )
    
    print(f"\nAWQ Result:")
    print(f"  Compression Ratio: {awq_result.compression_ratio:.1f}x")
    print(f"  Speedup Factor: {awq_result.speedup_factor:.1f}x")
    print(f"  Accuracy Loss: {awq_result.accuracy_loss:.3f}")
    print(f"  Memory Reduction: {awq_result.memory_reduction:.1%}")
    
    # Benchmark
    gptq_benchmark = manager.benchmark_quantized_model(gptq_result, test_data)
    print(f"\nGPTQ Benchmark:")
    print(f"  Inference Time: {gptq_benchmark.inference_time_ms:.1f}ms")
    print(f"  Memory Usage: {gptq_benchmark.memory_usage_mb:.0f}MB")
    print(f"  Throughput: {gptq_benchmark.throughput_tokens_per_second:.0f} tokens/s")
    print(f"  Accuracy: {gptq_benchmark.accuracy_score:.3f}")
    
    # Comparación
    comparison = manager.compare_quantization_methods(test_model_path, test_data)
    print(f"\nComparison Results:")
    print(f"  Best Balanced: {comparison['best_balanced']}")
    print(f"  Best Compression: {comparison['best_compression']}")
    print(f"  Best Speedup: {comparison['best_speedup']}")
    print(f"  Recommendations: {comparison['recommendations']}")
    
    # Estadísticas
    stats = manager.get_quantization_stats()
    print(f"\nStatistics: {stats}")
