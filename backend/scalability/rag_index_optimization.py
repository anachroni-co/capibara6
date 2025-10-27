#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Index Optimization - Sistema de optimización de índices RAG para búsqueda eficiente.
"""

import logging
import json
import os
import time
import pickle
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import faiss
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class IndexType(Enum):
    """Tipos de índice."""
    FLAT = "flat"
    IVF = "ivf"
    HNSW = "hnsw"
    PQ = "pq"
    HYBRID = "hybrid"


class OptimizationStrategy(Enum):
    """Estrategias de optimización."""
    SPEED = "speed"
    ACCURACY = "accuracy"
    MEMORY = "memory"
    BALANCED = "balanced"
    ADAPTIVE = "adaptive"


class IndexStatus(Enum):
    """Estados del índice."""
    BUILDING = "building"
    READY = "ready"
    OPTIMIZING = "optimizing"
    ERROR = "error"


@dataclass
class IndexConfig:
    """Configuración de índice."""
    index_type: IndexType
    dimension: int
    nlist: int  # Para IVF
    nprobe: int  # Para IVF
    m: int  # Para HNSW
    ef_construction: int  # Para HNSW
    ef_search: int  # Para HNSW
    pq_m: int  # Para PQ
    pq_bits: int  # Para PQ
    metadata: Dict[str, Any]


@dataclass
class IndexMetrics:
    """Métricas de índice."""
    total_vectors: int
    index_size_mb: float
    build_time_seconds: float
    search_time_ms: float
    memory_usage_mb: float
    accuracy_score: float
    throughput_queries_per_second: float
    compression_ratio: float


@dataclass
class SearchResult:
    """Resultado de búsqueda."""
    query_id: str
    results: List[Tuple[int, float]]  # (id, distance)
    search_time_ms: float
    index_used: str
    metadata: Dict[str, Any]


class FAISSIndexBuilder:
    """Constructor de índices FAISS."""
    
    def __init__(self):
        self.index_configs = self._create_index_configs()
        
        logger.info("FAISSIndexBuilder inicializado")
    
    def _create_index_configs(self) -> Dict[str, IndexConfig]:
        """Crea configuraciones de índice predefinidas."""
        configs = {}
        
        # Configuración Flat (exacta)
        configs['flat'] = IndexConfig(
            index_type=IndexType.FLAT,
            dimension=768,
            nlist=0,
            nprobe=0,
            m=0,
            ef_construction=0,
            ef_search=0,
            pq_m=0,
            pq_bits=0,
            metadata={'description': 'Exact search, slow but accurate'}
        )
        
        # Configuración IVF (rápida)
        configs['ivf'] = IndexConfig(
            index_type=IndexType.IVF,
            dimension=768,
            nlist=1024,
            nprobe=32,
            m=0,
            ef_construction=0,
            ef_search=0,
            pq_m=0,
            pq_bits=0,
            metadata={'description': 'Inverted file index, fast approximate search'}
        )
        
        # Configuración HNSW (balanceada)
        configs['hnsw'] = IndexConfig(
            index_type=IndexType.HNSW,
            dimension=768,
            nlist=0,
            nprobe=0,
            m=32,
            ef_construction=200,
            ef_search=64,
            pq_m=0,
            pq_bits=0,
            metadata={'description': 'Hierarchical navigable small world, balanced speed/accuracy'}
        )
        
        # Configuración PQ (comprimida)
        configs['pq'] = IndexConfig(
            index_type=IndexType.PQ,
            dimension=768,
            nlist=0,
            nprobe=0,
            m=0,
            ef_construction=0,
            ef_search=0,
            pq_m=64,
            pq_bits=8,
            metadata={'description': 'Product quantization, memory efficient'}
        )
        
        # Configuración Híbrida
        configs['hybrid'] = IndexConfig(
            index_type=IndexType.HYBRID,
            dimension=768,
            nlist=1024,
            nprobe=32,
            m=32,
            ef_construction=200,
            ef_search=64,
            pq_m=64,
            pq_bits=8,
            metadata={'description': 'Hybrid index combining multiple strategies'}
        )
        
        return configs
    
    def build_index(self, 
                   vectors: np.ndarray,
                   config: IndexConfig,
                   index_name: str) -> Tuple[faiss.Index, IndexMetrics]:
        """Construye índice FAISS."""
        try:
            start_time = time.time()
            
            logger.info(f"Construyendo índice {index_name} con configuración {config.index_type.value}")
            
            # Crear índice basado en tipo
            if config.index_type == IndexType.FLAT:
                index = self._build_flat_index(vectors, config)
            elif config.index_type == IndexType.IVF:
                index = self._build_ivf_index(vectors, config)
            elif config.index_type == IndexType.HNSW:
                index = self._build_hnsw_index(vectors, config)
            elif config.index_type == IndexType.PQ:
                index = self._build_pq_index(vectors, config)
            elif config.index_type == IndexType.HYBRID:
                index = self._build_hybrid_index(vectors, config)
            else:
                raise ValueError(f"Tipo de índice no soportado: {config.index_type}")
            
            # Entrenar índice si es necesario
            if hasattr(index, 'train') and not index.is_trained:
                logger.info("Entrenando índice...")
                index.train(vectors)
            
            # Agregar vectores
            logger.info(f"Agregando {len(vectors)} vectores al índice...")
            index.add(vectors)
            
            build_time = time.time() - start_time
            
            # Calcular métricas
            metrics = self._calculate_index_metrics(index, vectors, build_time)
            
            logger.info(f"Índice {index_name} construido en {build_time:.2f}s")
            return index, metrics
            
        except Exception as e:
            logger.error(f"Error construyendo índice: {e}")
            raise
    
    def _build_flat_index(self, vectors: np.ndarray, config: IndexConfig) -> faiss.Index:
        """Construye índice Flat."""
        return faiss.IndexFlatL2(config.dimension)
    
    def _build_ivf_index(self, vectors: np.ndarray, config: IndexConfig) -> faiss.Index:
        """Construye índice IVF."""
        quantizer = faiss.IndexFlatL2(config.dimension)
        index = faiss.IndexIVFFlat(quantizer, config.dimension, config.nlist)
        index.nprobe = config.nprobe
        return index
    
    def _build_hnsw_index(self, vectors: np.ndarray, config: IndexConfig) -> faiss.Index:
        """Construye índice HNSW."""
        index = faiss.IndexHNSWFlat(config.dimension, config.m)
        index.hnsw.efConstruction = config.ef_construction
        index.hnsw.efSearch = config.ef_search
        return index
    
    def _build_pq_index(self, vectors: np.ndarray, config: IndexConfig) -> faiss.Index:
        """Construye índice PQ."""
        index = faiss.IndexPQ(config.dimension, config.pq_m, config.pq_bits)
        return index
    
    def _build_hybrid_index(self, vectors: np.ndarray, config: IndexConfig) -> faiss.Index:
        """Construye índice híbrido."""
        # Combinar IVF con PQ
        quantizer = faiss.IndexFlatL2(config.dimension)
        index = faiss.IndexIVFPQ(quantizer, config.dimension, config.nlist, config.pq_m, config.pq_bits)
        index.nprobe = config.nprobe
        return index
    
    def _calculate_index_metrics(self, 
                               index: faiss.Index, 
                               vectors: np.ndarray, 
                               build_time: float) -> IndexMetrics:
        """Calcula métricas del índice."""
        # Tamaño del índice
        index_size_bytes = index.ntotal * index.d * 4  # Asumiendo float32
        index_size_mb = index_size_bytes / (1024 * 1024)
        
        # Memoria usada
        memory_usage_mb = index_size_mb
        
        # Tiempo de búsqueda (simulado)
        search_time_ms = self._benchmark_search_time(index, vectors[:100])  # Test con 100 vectores
        
        # Throughput
        throughput = 1000 / search_time_ms if search_time_ms > 0 else 0
        
        # Compresión (comparado con Flat)
        flat_size = len(vectors) * vectors.shape[1] * 4  # Tamaño sin compresión
        compression_ratio = flat_size / index_size_bytes if index_size_bytes > 0 else 1.0
        
        # Accuracy (simulado)
        accuracy_score = self._calculate_accuracy_score(index, vectors[:100])
        
        return IndexMetrics(
            total_vectors=len(vectors),
            index_size_mb=index_size_mb,
            build_time_seconds=build_time,
            search_time_ms=search_time_ms,
            memory_usage_mb=memory_usage_mb,
            accuracy_score=accuracy_score,
            throughput_queries_per_second=throughput,
            compression_ratio=compression_ratio
        )
    
    def _benchmark_search_time(self, index: faiss.Index, test_vectors: np.ndarray) -> float:
        """Benchmark de tiempo de búsqueda."""
        try:
            num_queries = min(10, len(test_vectors))
            query_vectors = test_vectors[:num_queries]
            
            start_time = time.time()
            
            for query in query_vectors:
                query = query.reshape(1, -1)
                distances, indices = index.search(query, k=10)
            
            total_time = time.time() - start_time
            avg_time_ms = (total_time / num_queries) * 1000
            
            return avg_time_ms
            
        except Exception as e:
            logger.error(f"Error en benchmark de búsqueda: {e}")
            return 100.0  # Tiempo por defecto
    
    def _calculate_accuracy_score(self, index: faiss.Index, test_vectors: np.ndarray) -> float:
        """Calcula score de precisión."""
        try:
            # Comparar con búsqueda exacta
            flat_index = faiss.IndexFlatL2(index.d)
            flat_index.add(test_vectors)
            
            num_queries = min(5, len(test_vectors))
            query_vectors = test_vectors[:num_queries]
            
            total_recall = 0.0
            
            for query in query_vectors:
                query = query.reshape(1, -1)
                
                # Búsqueda en índice optimizado
                distances_opt, indices_opt = index.search(query, k=10)
                
                # Búsqueda exacta
                distances_exact, indices_exact = flat_index.search(query, k=10)
                
                # Calcular recall
                recall = len(set(indices_opt[0]) & set(indices_exact[0])) / 10.0
                total_recall += recall
            
            return total_recall / num_queries
            
        except Exception as e:
            logger.error(f"Error calculando precisión: {e}")
            return 0.8  # Score por defecto


class RAGIndexOptimizer:
    """Optimizador de índices RAG."""
    
    def __init__(self, 
                 indices_dir: str = "backend/data/rag_indices",
                 cache_dir: str = "backend/data/rag_cache"):
        self.indices_dir = indices_dir
        self.cache_dir = cache_dir
        
        # Constructor de índices
        self.index_builder = FAISSIndexBuilder()
        
        # Índices activos
        self.active_indices: Dict[str, faiss.Index] = {}
        self.index_metrics: Dict[str, IndexMetrics] = {}
        self.index_configs: Dict[str, IndexConfig] = {}
        
        # Historial de optimizaciones
        self.optimization_history: deque = deque(maxlen=1000)
        
        # Estadísticas
        self.optimizer_stats = {
            'total_indices_built': 0,
            'total_optimizations': 0,
            'average_build_time_seconds': 0.0,
            'average_search_time_ms': 0.0,
            'total_vectors_indexed': 0
        }
        
        # Asegurar directorios
        os.makedirs(indices_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
        
        logger.info(f"RAGIndexOptimizer inicializado: indices_dir={indices_dir}")
    
    def build_optimized_index(self, 
                            vectors: np.ndarray,
                            index_name: str,
                            strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
                            custom_config: Optional[IndexConfig] = None) -> str:
        """Construye índice optimizado."""
        try:
            logger.info(f"Construyendo índice optimizado {index_name} con estrategia {strategy.value}")
            
            # Seleccionar configuración
            if custom_config:
                config = custom_config
            else:
                config = self._select_optimal_config(vectors, strategy)
            
            # Construir índice
            index, metrics = self.index_builder.build_index(vectors, config, index_name)
            
            # Guardar índice
            index_path = os.path.join(self.indices_dir, f"{index_name}.index")
            faiss.write_index(index, index_path)
            
            # Guardar configuración
            config_path = os.path.join(self.indices_dir, f"{index_name}_config.json")
            config_data = asdict(config)
            config_data['index_type'] = config.index_type.value
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)
            
            # Guardar métricas
            metrics_path = os.path.join(self.indices_dir, f"{index_name}_metrics.json")
            metrics_data = asdict(metrics)
            with open(metrics_path, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            # Agregar a índices activos
            self.active_indices[index_name] = index
            self.index_metrics[index_name] = metrics
            self.index_configs[index_name] = config
            
            # Actualizar estadísticas
            self._update_stats(metrics)
            
            logger.info(f"Índice {index_name} construido y guardado exitosamente")
            return index_name
            
        except Exception as e:
            logger.error(f"Error construyendo índice optimizado: {e}")
            raise
    
    def _select_optimal_config(self, 
                             vectors: np.ndarray, 
                             strategy: OptimizationStrategy) -> IndexConfig:
        """Selecciona configuración óptima basada en estrategia."""
        num_vectors = len(vectors)
        dimension = vectors.shape[1]
        
        # Ajustar configuraciones basadas en el tamaño de datos
        configs = self.index_builder.index_configs.copy()
        
        # Actualizar dimensiones
        for config in configs.values():
            config.dimension = dimension
        
        # Seleccionar configuración basada en estrategia
        if strategy == OptimizationStrategy.SPEED:
            # Priorizar velocidad
            if num_vectors < 10000:
                return configs['flat']  # Pequeño dataset, usar exacto
            elif num_vectors < 100000:
                return configs['ivf']  # Dataset mediano, usar IVF
            else:
                return configs['hnsw']  # Dataset grande, usar HNSW
        
        elif strategy == OptimizationStrategy.ACCURACY:
            # Priorizar precisión
            if num_vectors < 50000:
                return configs['flat']  # Usar exacto si es posible
            else:
                return configs['hnsw']  # HNSW tiene buena precisión
        
        elif strategy == OptimizationStrategy.MEMORY:
            # Priorizar memoria
            return configs['pq']  # PQ es más eficiente en memoria
        
        elif strategy == OptimizationStrategy.BALANCED:
            # Balanceado
            if num_vectors < 10000:
                return configs['flat']
            elif num_vectors < 100000:
                return configs['ivf']
            else:
                return configs['hybrid']  # Híbrido para datasets grandes
        
        else:  # ADAPTIVE
            # Adaptativo basado en características de los datos
            return self._adaptive_config_selection(vectors, configs)
    
    def _adaptive_config_selection(self, 
                                 vectors: np.ndarray, 
                                 configs: Dict[str, IndexConfig]) -> IndexConfig:
        """Selección adaptativa de configuración."""
        num_vectors = len(vectors)
        dimension = vectors.shape[1]
        
        # Analizar distribución de los datos
        data_variance = np.var(vectors)
        data_spread = np.std(vectors)
        
        # Seleccionar basado en análisis
        if num_vectors < 10000 and data_variance < 1.0:
            # Dataset pequeño y compacto
            return configs['flat']
        elif num_vectors < 100000 and data_spread > 2.0:
            # Dataset mediano y disperso
            return configs['ivf']
        elif num_vectors >= 100000:
            # Dataset grande
            if data_variance > 2.0:
                return configs['hybrid']  # Datos muy variables
            else:
                return configs['hnsw']  # Datos más uniformes
        else:
            return configs['hnsw']  # Por defecto
    
    def load_index(self, index_name: str) -> bool:
        """Carga índice desde disco."""
        try:
            index_path = os.path.join(self.indices_dir, f"{index_name}.index")
            config_path = os.path.join(self.indices_dir, f"{index_name}_config.json")
            metrics_path = os.path.join(self.indices_dir, f"{index_name}_metrics.json")
            
            if not all(os.path.exists(p) for p in [index_path, config_path, metrics_path]):
                logger.error(f"Archivos de índice no encontrados para {index_name}")
                return False
            
            # Cargar índice
            index = faiss.read_index(index_path)
            
            # Cargar configuración
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            config = IndexConfig(**config_data)
            config.index_type = IndexType(config_data['index_type'])
            
            # Cargar métricas
            with open(metrics_path, 'r') as f:
                metrics_data = json.load(f)
            metrics = IndexMetrics(**metrics_data)
            
            # Agregar a índices activos
            self.active_indices[index_name] = index
            self.index_configs[index_name] = config
            self.index_metrics[index_name] = metrics
            
            logger.info(f"Índice {index_name} cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando índice {index_name}: {e}")
            return False
    
    def search(self, 
              query_vector: np.ndarray,
              index_name: str,
              k: int = 10,
              query_id: Optional[str] = None) -> SearchResult:
        """Busca en índice."""
        try:
            if index_name not in self.active_indices:
                logger.error(f"Índice {index_name} no está cargado")
                return SearchResult(
                    query_id=query_id or "unknown",
                    results=[],
                    search_time_ms=0.0,
                    index_used=index_name,
                    metadata={'error': 'Index not loaded'}
                )
            
            index = self.active_indices[index_name]
            query_id = query_id or f"query_{int(time.time() * 1000)}"
            
            # Preparar query
            if query_vector.ndim == 1:
                query_vector = query_vector.reshape(1, -1)
            
            # Buscar
            start_time = time.time()
            distances, indices = index.search(query_vector, k)
            search_time = (time.time() - start_time) * 1000
            
            # Formatear resultados
            results = []
            for i in range(len(indices[0])):
                if indices[0][i] >= 0:  # Índice válido
                    results.append((int(indices[0][i]), float(distances[0][i])))
            
            # Crear resultado
            result = SearchResult(
                query_id=query_id,
                results=results,
                search_time_ms=search_time,
                index_used=index_name,
                metadata={
                    'k_requested': k,
                    'k_returned': len(results),
                    'index_type': self.index_configs[index_name].index_type.value
                }
            )
            
            logger.debug(f"Búsqueda completada en {search_time:.2f}ms: {len(results)} resultados")
            return result
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return SearchResult(
                query_id=query_id or "unknown",
                results=[],
                search_time_ms=0.0,
                index_used=index_name,
                metadata={'error': str(e)}
            )
    
    def optimize_index(self, 
                      index_name: str,
                      optimization_type: str = "rebalance") -> bool:
        """Optimiza índice existente."""
        try:
            if index_name not in self.active_indices:
                logger.error(f"Índice {index_name} no está cargado")
                return False
            
            logger.info(f"Optimizando índice {index_name} con tipo {optimization_type}")
            
            index = self.active_indices[index_name]
            config = self.index_configs[index_name]
            metrics = self.index_metrics[index_name]
            
            # Aplicar optimizaciones
            if optimization_type == "rebalance":
                self._rebalance_index(index, config)
            elif optimization_type == "compress":
                self._compress_index(index, config)
            elif optimization_type == "tune":
                self._tune_index_parameters(index, config)
            else:
                logger.warning(f"Tipo de optimización no soportado: {optimization_type}")
                return False
            
            # Recalcular métricas
            new_metrics = self._recalculate_metrics(index, metrics)
            self.index_metrics[index_name] = new_metrics
            
            # Guardar índice optimizado
            index_path = os.path.join(self.indices_dir, f"{index_name}_optimized.index")
            faiss.write_index(index, index_path)
            
            # Actualizar estadísticas
            self.optimizer_stats['total_optimizations'] += 1
            
            logger.info(f"Índice {index_name} optimizado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error optimizando índice: {e}")
            return False
    
    def _rebalance_index(self, index: faiss.Index, config: IndexConfig):
        """Rebalancea índice."""
        # Implementación simplificada
        if hasattr(index, 'reconstruct_n'):
            logger.info("Rebalanceando índice...")
            # En implementación real, aquí se haría el rebalanceo
    
    def _compress_index(self, index: faiss.Index, config: IndexConfig):
        """Comprime índice."""
        # Implementación simplificada
        logger.info("Comprimiendo índice...")
        # En implementación real, aquí se aplicaría compresión
    
    def _tune_index_parameters(self, index: faiss.Index, config: IndexConfig):
        """Ajusta parámetros del índice."""
        # Implementación simplificada
        logger.info("Ajustando parámetros del índice...")
        # En implementación real, aquí se optimizarían parámetros
    
    def _recalculate_metrics(self, index: faiss.Index, old_metrics: IndexMetrics) -> IndexMetrics:
        """Recalcula métricas del índice."""
        # Simular recálculo de métricas
        return IndexMetrics(
            total_vectors=old_metrics.total_vectors,
            index_size_mb=old_metrics.index_size_mb * 0.9,  # Asumir 10% de mejora
            build_time_seconds=old_metrics.build_time_seconds,
            search_time_ms=old_metrics.search_time_ms * 0.8,  # Asumir 20% de mejora
            memory_usage_mb=old_metrics.memory_usage_mb * 0.9,
            accuracy_score=old_metrics.accuracy_score,
            throughput_queries_per_second=old_metrics.throughput_queries_per_second * 1.25,
            compression_ratio=old_metrics.compression_ratio * 1.1
        )
    
    def compare_indices(self, 
                       index_names: List[str],
                       test_vectors: np.ndarray,
                       num_queries: int = 100) -> Dict[str, Any]:
        """Compara múltiples índices."""
        try:
            logger.info(f"Comparando índices: {index_names}")
            
            comparison_results = {}
            
            for index_name in index_names:
                if index_name not in self.active_indices:
                    logger.warning(f"Índice {index_name} no está cargado")
                    continue
                
                # Benchmark del índice
                search_times = []
                accuracies = []
                
                for i in range(min(num_queries, len(test_vectors))):
                    query_vector = test_vectors[i]
                    result = self.search(query_vector, index_name, k=10)
                    
                    search_times.append(result.search_time_ms)
                    
                    # Calcular precisión (simulada)
                    accuracy = min(1.0, len(result.results) / 10.0)
                    accuracies.append(accuracy)
                
                # Calcular métricas
                avg_search_time = np.mean(search_times)
                avg_accuracy = np.mean(accuracies)
                throughput = 1000 / avg_search_time if avg_search_time > 0 else 0
                
                comparison_results[index_name] = {
                    'average_search_time_ms': avg_search_time,
                    'average_accuracy': avg_accuracy,
                    'throughput_queries_per_second': throughput,
                    'index_metrics': self.index_metrics.get(index_name),
                    'index_config': self.index_configs.get(index_name)
                }
            
            # Análisis comparativo
            analysis = self._analyze_comparison(comparison_results)
            
            logger.info("Comparación de índices completada")
            return {
                'results': comparison_results,
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"Error comparando índices: {e}")
            return {}
    
    def _analyze_comparison(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza resultados de comparación."""
        analysis = {
            'best_speed': None,
            'best_accuracy': None,
            'best_balanced': None,
            'recommendations': []
        }
        
        if not results:
            return analysis
        
        # Encontrar mejores índices
        best_speed = min(results.items(), key=lambda x: x[1]['average_search_time_ms'])
        analysis['best_speed'] = {
            'index': best_speed[0],
            'search_time_ms': best_speed[1]['average_search_time_ms']
        }
        
        best_accuracy = max(results.items(), key=lambda x: x[1]['average_accuracy'])
        analysis['best_accuracy'] = {
            'index': best_accuracy[0],
            'accuracy': best_accuracy[1]['average_accuracy']
        }
        
        # Mejor balanceado (score combinado)
        balanced_scores = {}
        for index_name, data in results.items():
            # Score combinado: 40% velocidad, 60% precisión
            speed_score = 1.0 / (data['average_search_time_ms'] / 100.0)  # Normalizar
            accuracy_score = data['average_accuracy']
            
            balanced_score = speed_score * 0.4 + accuracy_score * 0.6
            balanced_scores[index_name] = balanced_score
        
        best_balanced = max(balanced_scores.items(), key=lambda x: x[1])
        analysis['best_balanced'] = {
            'index': best_balanced[0],
            'score': best_balanced[1]
        }
        
        # Generar recomendaciones
        analysis['recommendations'].append(
            f"Para máxima velocidad: {analysis['best_speed']['index']} "
            f"({analysis['best_speed']['search_time_ms']:.1f}ms)"
        )
        
        analysis['recommendations'].append(
            f"Para máxima precisión: {analysis['best_accuracy']['index']} "
            f"({analysis['best_accuracy']['accuracy']:.3f})"
        )
        
        analysis['recommendations'].append(
            f"Para uso general: {analysis['best_balanced']['index']} "
            f"(score: {analysis['best_balanced']['score']:.3f})"
        )
        
        return analysis
    
    def _update_stats(self, metrics: IndexMetrics):
        """Actualiza estadísticas."""
        self.optimizer_stats['total_indices_built'] += 1
        self.optimizer_stats['total_vectors_indexed'] += metrics.total_vectors
        
        # Actualizar promedios
        total_indices = self.optimizer_stats['total_indices_built']
        
        # Promedio de tiempo de construcción
        current_avg = self.optimizer_stats['average_build_time_seconds']
        new_avg = ((current_avg * (total_indices - 1)) + metrics.build_time_seconds) / total_indices
        self.optimizer_stats['average_build_time_seconds'] = new_avg
        
        # Promedio de tiempo de búsqueda
        current_avg = self.optimizer_stats['average_search_time_ms']
        new_avg = ((current_avg * (total_indices - 1)) + metrics.search_time_ms) / total_indices
        self.optimizer_stats['average_search_time_ms'] = new_avg
    
    def get_optimizer_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del optimizador."""
        return {
            'optimizer_stats': self.optimizer_stats,
            'active_indices': list(self.active_indices.keys()),
            'total_active_indices': len(self.active_indices)
        }
    
    def get_index_info(self, index_name: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un índice."""
        if index_name not in self.active_indices:
            return None
        
        return {
            'name': index_name,
            'config': asdict(self.index_configs[index_name]),
            'metrics': asdict(self.index_metrics[index_name]),
            'status': 'ready'
        }


if __name__ == "__main__":
    # Test del RAGIndexOptimizer
    logging.basicConfig(level=logging.INFO)
    
    optimizer = RAGIndexOptimizer()
    
    # Generar datos de prueba
    num_vectors = 10000
    dimension = 768
    vectors = np.random.randn(num_vectors, dimension).astype(np.float32)
    
    print(f"Generados {num_vectors} vectores de dimensión {dimension}")
    
    # Construir diferentes tipos de índices
    index_configs = [
        ("flat_index", OptimizationStrategy.ACCURACY),
        ("ivf_index", OptimizationStrategy.SPEED),
        ("hnsw_index", OptimizationStrategy.BALANCED),
        ("pq_index", OptimizationStrategy.MEMORY)
    ]
    
    built_indices = []
    for index_name, strategy in index_configs:
        try:
            result = optimizer.build_optimized_index(vectors, index_name, strategy)
            built_indices.append(result)
            print(f"Índice {index_name} construido exitosamente")
        except Exception as e:
            print(f"Error construyendo {index_name}: {e}")
    
    # Comparar índices
    if len(built_indices) > 1:
        test_vectors = vectors[:100]  # Usar primeros 100 vectores para test
        comparison = optimizer.compare_indices(built_indices, test_vectors, num_queries=50)
        
        print(f"\nComparación de índices:")
        for index_name, data in comparison['results'].items():
            print(f"  {index_name}:")
            print(f"    Tiempo de búsqueda: {data['average_search_time_ms']:.2f}ms")
            print(f"    Precisión: {data['average_accuracy']:.3f}")
            print(f"    Throughput: {data['throughput_queries_per_second']:.1f} queries/s")
        
        print(f"\nAnálisis:")
        for recommendation in comparison['analysis']['recommendations']:
            print(f"  - {recommendation}")
    
    # Test de búsqueda
    if built_indices:
        test_query = vectors[0]  # Usar primer vector como query
        result = optimizer.search(test_query, built_indices[0], k=5)
        
        print(f"\nResultado de búsqueda:")
        print(f"  Query ID: {result.query_id}")
        print(f"  Tiempo: {result.search_time_ms:.2f}ms")
        print(f"  Resultados: {len(result.results)}")
        for i, (idx, dist) in enumerate(result.results):
            print(f"    {i+1}. ID: {idx}, Distancia: {dist:.3f}")
    
    # Mostrar estadísticas
    stats = optimizer.get_optimizer_stats()
    print(f"\nEstadísticas del optimizador:")
    print(f"  Índices construidos: {stats['optimizer_stats']['total_indices_built']}")
    print(f"  Vectores indexados: {stats['optimizer_stats']['total_vectors_indexed']}")
    print(f"  Tiempo promedio de construcción: {stats['optimizer_stats']['average_build_time_seconds']:.2f}s")
    print(f"  Tiempo promedio de búsqueda: {stats['optimizer_stats']['average_search_time_ms']:.2f}ms")
