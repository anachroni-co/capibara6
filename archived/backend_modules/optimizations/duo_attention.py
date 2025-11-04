#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DuoAttention - Sistema de atención dual para optimización de procesamiento.
"""

import logging
import json
import os
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import math

logger = logging.getLogger(__name__)


class AttentionType(Enum):
    """Tipos de atención."""
    SELF_ATTENTION = "self_attention"
    CROSS_ATTENTION = "cross_attention"
    HIERARCHICAL_ATTENTION = "hierarchical_attention"
    TEMPORAL_ATTENTION = "temporal_attention"
    SPATIAL_ATTENTION = "spatial_attention"


class AttentionMode(Enum):
    """Modos de atención."""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    ADAPTIVE = "adaptive"
    HIERARCHICAL = "hierarchical"


@dataclass
class AttentionHead:
    """Cabeza de atención."""
    head_id: str
    attention_type: AttentionType
    dimension: int
    num_heads: int
    dropout_rate: float
    temperature: float
    is_active: bool
    performance_score: float
    last_used: datetime
    metadata: Dict[str, Any]


@dataclass
class AttentionLayer:
    """Capa de atención."""
    layer_id: str
    heads: List[AttentionHead]
    mode: AttentionMode
    input_dimension: int
    output_dimension: int
    residual_connection: bool
    layer_norm: bool
    dropout_rate: float
    performance_metrics: Dict[str, float]


@dataclass
class AttentionQuery:
    """Query de atención."""
    query_id: str
    input_tokens: List[str]
    context_tokens: Optional[List[str]]
    attention_types: List[AttentionType]
    max_sequence_length: int
    temperature: float
    mask: Optional[np.ndarray]
    metadata: Dict[str, Any]


@dataclass
class AttentionResult:
    """Resultado de atención."""
    query_id: str
    attention_weights: np.ndarray
    output_embeddings: np.ndarray
    attention_heads_used: List[str]
    processing_time_ms: float
    memory_usage_mb: float
    quality_score: float


class AttentionMechanism:
    """Mecanismo de atención base."""
    
    def __init__(self, dimension: int, num_heads: int = 8):
        self.dimension = dimension
        self.num_heads = num_heads
        self.head_dimension = dimension // num_heads
        
        # Parámetros de atención
        self.temperature = 1.0
        self.dropout_rate = 0.1
        
        # Cache de atención
        self.attention_cache: Dict[str, np.ndarray] = {}
        
        logger.info(f"AttentionMechanism inicializado: dim={dimension}, heads={num_heads}")
    
    def scaled_dot_product_attention(self, 
                                   query: np.ndarray, 
                                   key: np.ndarray, 
                                   value: np.ndarray,
                                   mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Atención de producto punto escalado."""
        try:
            # Calcular scores de atención
            scores = np.matmul(query, key.transpose(-2, -1)) / math.sqrt(self.head_dimension)
            
            # Aplicar máscara si existe
            if mask is not None:
                scores = np.where(mask == 0, -1e9, scores)
            
            # Aplicar temperatura
            scores = scores / self.temperature
            
            # Softmax
            attention_weights = self._softmax(scores, axis=-1)
            
            # Aplicar dropout (simulado)
            if self.dropout_rate > 0:
                attention_weights = self._apply_dropout(attention_weights, self.dropout_rate)
            
            # Calcular output
            output = np.matmul(attention_weights, value)
            
            return output, attention_weights
            
        except Exception as e:
            logger.error(f"Error en scaled_dot_product_attention: {e}")
            # Retornar valores por defecto
            batch_size, seq_len, _ = query.shape
            attention_weights = np.ones((batch_size, seq_len, seq_len)) / seq_len
            output = np.zeros_like(query)
            return output, attention_weights
    
    def multi_head_attention(self, 
                           query: np.ndarray, 
                           key: np.ndarray, 
                           value: np.ndarray,
                           mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Atención multi-cabeza."""
        try:
            batch_size, seq_len, _ = query.shape
            
            # Reshape para múltiples cabezas
            query_heads = query.reshape(batch_size, seq_len, self.num_heads, self.head_dimension)
            key_heads = key.reshape(batch_size, seq_len, self.num_heads, self.head_dimension)
            value_heads = value.reshape(batch_size, seq_len, self.num_heads, self.head_dimension)
            
            # Transponer para procesamiento por cabeza
            query_heads = query_heads.transpose(0, 2, 1, 3)
            key_heads = key_heads.transpose(0, 2, 1, 3)
            value_heads = value_heads.transpose(0, 2, 1, 3)
            
            # Procesar cada cabeza
            attention_outputs = []
            attention_weights_list = []
            
            for head in range(self.num_heads):
                head_query = query_heads[:, head, :, :]
                head_key = key_heads[:, head, :, :]
                head_value = value_heads[:, head, :, :]
                
                head_output, head_weights = self.scaled_dot_product_attention(
                    head_query, head_key, head_value, mask
                )
                
                attention_outputs.append(head_output)
                attention_weights_list.append(head_weights)
            
            # Concatenar cabezas
            concatenated = np.concatenate(attention_outputs, axis=-1)
            
            # Reshape de vuelta
            output = concatenated.reshape(batch_size, seq_len, self.dimension)
            
            # Promedio de pesos de atención
            attention_weights = np.mean(attention_weights_list, axis=0)
            
            return output, attention_weights
            
        except Exception as e:
            logger.error(f"Error en multi_head_attention: {e}")
            # Retornar valores por defecto
            batch_size, seq_len, _ = query.shape
            attention_weights = np.ones((batch_size, seq_len, seq_len)) / seq_len
            output = np.zeros_like(query)
            return output, attention_weights
    
    def _softmax(self, x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Implementación de softmax."""
        # Estabilización numérica
        x_max = np.max(x, axis=axis, keepdims=True)
        x_stable = x - x_max
        
        exp_x = np.exp(x_stable)
        sum_exp = np.sum(exp_x, axis=axis, keepdims=True)
        
        return exp_x / sum_exp
    
    def _apply_dropout(self, x: np.ndarray, dropout_rate: float) -> np.ndarray:
        """Aplica dropout (simulado)."""
        if dropout_rate == 0:
            return x
        
        # Simulación de dropout
        mask = np.random.random(x.shape) > dropout_rate
        return x * mask / (1 - dropout_rate)


class DuoAttention:
    """Sistema de atención dual."""
    
    def __init__(self, 
                 primary_dimension: int = 768,
                 secondary_dimension: int = 512,
                 num_heads: int = 8,
                 mode: AttentionMode = AttentionMode.ADAPTIVE):
        self.primary_dimension = primary_dimension
        self.secondary_dimension = secondary_dimension
        self.num_heads = num_heads
        self.mode = mode
        
        # Mecanismos de atención
        self.primary_attention = AttentionMechanism(primary_dimension, num_heads)
        self.secondary_attention = AttentionMechanism(secondary_dimension, num_heads)
        
        # Capas de atención
        self.attention_layers: Dict[str, AttentionLayer] = {}
        
        # Configuración de cabezas
        self.attention_heads: Dict[str, AttentionHead] = {}
        
        # Estadísticas
        self.attention_stats = {
            'total_queries_processed': 0,
            'average_processing_time_ms': 0.0,
            'average_quality_score': 0.0,
            'attention_head_usage': defaultdict(int),
            'mode_switches': 0
        }
        
        # Cache de resultados
        self.result_cache: Dict[str, AttentionResult] = {}
        self.cache_max_size = 1000
        
        # Inicializar cabezas de atención
        self._initialize_attention_heads()
        
        logger.info(f"DuoAttention inicializado: primary={primary_dimension}, secondary={secondary_dimension}, mode={mode.value}")
    
    def _initialize_attention_heads(self):
        """Inicializa cabezas de atención."""
        attention_types = [
            AttentionType.SELF_ATTENTION,
            AttentionType.CROSS_ATTENTION,
            AttentionType.HIERARCHICAL_ATTENTION,
            AttentionType.TEMPORAL_ATTENTION
        ]
        
        for i, attention_type in enumerate(attention_types):
            # Cabeza primaria
            primary_head = AttentionHead(
                head_id=f"primary_{attention_type.value}_{i}",
                attention_type=attention_type,
                dimension=self.primary_dimension,
                num_heads=self.num_heads,
                dropout_rate=0.1,
                temperature=1.0,
                is_active=True,
                performance_score=0.8,
                last_used=datetime.now(),
                metadata={'layer': 'primary', 'index': i}
            )
            
            # Cabeza secundaria
            secondary_head = AttentionHead(
                head_id=f"secondary_{attention_type.value}_{i}",
                attention_type=attention_type,
                dimension=self.secondary_dimension,
                num_heads=self.num_heads,
                dropout_rate=0.1,
                temperature=1.0,
                is_active=True,
                performance_score=0.7,
                last_used=datetime.now(),
                metadata={'layer': 'secondary', 'index': i}
            )
            
            self.attention_heads[primary_head.head_id] = primary_head
            self.attention_heads[secondary_head.head_id] = secondary_head
    
    def process_attention(self, query: AttentionQuery) -> AttentionResult:
        """Procesa query usando atención dual."""
        try:
            start_time = datetime.now()
            
            # Verificar cache
            cache_key = self._generate_cache_key(query)
            if cache_key in self.result_cache:
                return self.result_cache[cache_key]
            
            # Seleccionar cabezas de atención
            selected_heads = self._select_attention_heads(query)
            
            # Procesar según el modo
            if self.mode == AttentionMode.PARALLEL:
                result = self._process_parallel_attention(query, selected_heads)
            elif self.mode == AttentionMode.SEQUENTIAL:
                result = self._process_sequential_attention(query, selected_heads)
            elif self.mode == AttentionMode.ADAPTIVE:
                result = self._process_adaptive_attention(query, selected_heads)
            elif self.mode == AttentionMode.HIERARCHICAL:
                result = self._process_hierarchical_attention(query, selected_heads)
            else:
                result = self._process_parallel_attention(query, selected_heads)
            
            # Calcular métricas
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            result.processing_time_ms = processing_time
            result.attention_heads_used = [head.head_id for head in selected_heads]
            
            # Actualizar estadísticas
            self._update_stats(result)
            
            # Actualizar cache
            self._update_cache(cache_key, result)
            
            logger.info(f"Atención procesada: {query.query_id}, {len(selected_heads)} cabezas, {processing_time:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error procesando atención: {e}")
            return self._create_fallback_result(query)
    
    def _select_attention_heads(self, query: AttentionQuery) -> List[AttentionHead]:
        """Selecciona cabezas de atención basado en la query."""
        selected_heads = []
        
        # Filtrar por tipo de atención requerido
        for head_id, head in self.attention_heads.items():
            if (head.attention_type in query.attention_types and 
                head.is_active and 
                head.performance_score > 0.5):
                selected_heads.append(head)
        
        # Ordenar por rendimiento
        selected_heads.sort(key=lambda x: x.performance_score, reverse=True)
        
        # Limitar número de cabezas
        max_heads = min(4, len(selected_heads))
        return selected_heads[:max_heads]
    
    def _process_parallel_attention(self, query: AttentionQuery, heads: List[AttentionHead]) -> AttentionResult:
        """Procesa atención en paralelo."""
        try:
            # Preparar embeddings de entrada
            input_embeddings = self._prepare_input_embeddings(query.input_tokens)
            context_embeddings = self._prepare_context_embeddings(query.context_tokens) if query.context_tokens else None
            
            # Procesar con cada cabeza en paralelo
            attention_outputs = []
            attention_weights_list = []
            
            for head in heads:
                if 'primary' in head.head_id:
                    mechanism = self.primary_attention
                    embeddings = input_embeddings
                else:
                    mechanism = self.secondary_attention
                    embeddings = self._project_to_secondary(input_embeddings)
                
                # Aplicar atención
                if head.attention_type == AttentionType.SELF_ATTENTION:
                    output, weights = mechanism.multi_head_attention(
                        embeddings, embeddings, embeddings, query.mask
                    )
                elif head.attention_type == AttentionType.CROSS_ATTENTION and context_embeddings is not None:
                    output, weights = mechanism.multi_head_attention(
                        embeddings, context_embeddings, context_embeddings, query.mask
                    )
                else:
                    # Fallback a self-attention
                    output, weights = mechanism.multi_head_attention(
                        embeddings, embeddings, embeddings, query.mask
                    )
                
                attention_outputs.append(output)
                attention_weights_list.append(weights)
            
            # Combinar outputs
            combined_output = self._combine_attention_outputs(attention_outputs, heads)
            combined_weights = np.mean(attention_weights_list, axis=0)
            
            # Calcular calidad
            quality_score = self._calculate_attention_quality(combined_output, combined_weights)
            
            return AttentionResult(
                query_id=query.query_id,
                attention_weights=combined_weights,
                output_embeddings=combined_output,
                attention_heads_used=[],
                processing_time_ms=0.0,
                memory_usage_mb=0.0,
                quality_score=quality_score
            )
            
        except Exception as e:
            logger.error(f"Error en atención paralela: {e}")
            return self._create_fallback_result(query)
    
    def _process_sequential_attention(self, query: AttentionQuery, heads: List[AttentionHead]) -> AttentionResult:
        """Procesa atención secuencialmente."""
        try:
            # Preparar embeddings
            current_embeddings = self._prepare_input_embeddings(query.input_tokens)
            context_embeddings = self._prepare_context_embeddings(query.context_tokens) if query.context_tokens else None
            
            attention_weights_list = []
            
            # Procesar secuencialmente
            for head in heads:
                if 'primary' in head.head_id:
                    mechanism = self.primary_attention
                else:
                    mechanism = self.secondary_attention
                    current_embeddings = self._project_to_secondary(current_embeddings)
                
                # Aplicar atención
                if head.attention_type == AttentionType.SELF_ATTENTION:
                    output, weights = mechanism.multi_head_attention(
                        current_embeddings, current_embeddings, current_embeddings, query.mask
                    )
                elif head.attention_type == AttentionType.CROSS_ATTENTION and context_embeddings is not None:
                    output, weights = mechanism.multi_head_attention(
                        current_embeddings, context_embeddings, context_embeddings, query.mask
                    )
                else:
                    output, weights = mechanism.multi_head_attention(
                        current_embeddings, current_embeddings, current_embeddings, query.mask
                    )
                
                # Actualizar embeddings para siguiente iteración
                current_embeddings = output
                attention_weights_list.append(weights)
            
            # Calcular calidad
            quality_score = self._calculate_attention_quality(current_embeddings, attention_weights_list[-1])
            
            return AttentionResult(
                query_id=query.query_id,
                attention_weights=attention_weights_list[-1],
                output_embeddings=current_embeddings,
                attention_heads_used=[],
                processing_time_ms=0.0,
                memory_usage_mb=0.0,
                quality_score=quality_score
            )
            
        except Exception as e:
            logger.error(f"Error en atención secuencial: {e}")
            return self._create_fallback_result(query)
    
    def _process_adaptive_attention(self, query: AttentionQuery, heads: List[AttentionHead]) -> AttentionResult:
        """Procesa atención de forma adaptativa."""
        try:
            # Evaluar complejidad de la query
            complexity = self._evaluate_query_complexity(query)
            
            # Seleccionar estrategia basada en complejidad
            if complexity < 0.3:
                # Query simple - usar atención paralela
                return self._process_parallel_attention(query, heads[:2])
            elif complexity < 0.7:
                # Query moderada - usar atención secuencial
                return self._process_sequential_attention(query, heads[:3])
            else:
                # Query compleja - usar atención jerárquica
                return self._process_hierarchical_attention(query, heads)
                
        except Exception as e:
            logger.error(f"Error en atención adaptativa: {e}")
            return self._create_fallback_result(query)
    
    def _process_hierarchical_attention(self, query: AttentionQuery, heads: List[AttentionHead]) -> AttentionResult:
        """Procesa atención jerárquica."""
        try:
            # Dividir en niveles jerárquicos
            input_embeddings = self._prepare_input_embeddings(query.input_tokens)
            
            # Nivel 1: Atención local
            local_heads = [h for h in heads if h.attention_type == AttentionType.SELF_ATTENTION]
            local_output, local_weights = self._process_attention_level(input_embeddings, local_heads, "local")
            
            # Nivel 2: Atención global
            global_heads = [h for h in heads if h.attention_type == AttentionType.CROSS_ATTENTION]
            global_output, global_weights = self._process_attention_level(local_output, global_heads, "global")
            
            # Combinar niveles
            combined_output = self._combine_hierarchical_outputs(local_output, global_output)
            combined_weights = np.concatenate([local_weights, global_weights], axis=-1)
            
            # Calcular calidad
            quality_score = self._calculate_attention_quality(combined_output, combined_weights)
            
            return AttentionResult(
                query_id=query.query_id,
                attention_weights=combined_weights,
                output_embeddings=combined_output,
                attention_heads_used=[],
                processing_time_ms=0.0,
                memory_usage_mb=0.0,
                quality_score=quality_score
            )
            
        except Exception as e:
            logger.error(f"Error en atención jerárquica: {e}")
            return self._create_fallback_result(query)
    
    def _process_attention_level(self, embeddings: np.ndarray, heads: List[AttentionHead], level: str) -> Tuple[np.ndarray, np.ndarray]:
        """Procesa un nivel de atención jerárquica."""
        if not heads:
            return embeddings, np.ones((embeddings.shape[0], embeddings.shape[1], embeddings.shape[1])) / embeddings.shape[1]
        
        attention_outputs = []
        attention_weights_list = []
        
        for head in heads:
            if 'primary' in head.head_id:
                mechanism = self.primary_attention
            else:
                mechanism = self.secondary_attention
                embeddings = self._project_to_secondary(embeddings)
            
            output, weights = mechanism.multi_head_attention(embeddings, embeddings, embeddings)
            attention_outputs.append(output)
            attention_weights_list.append(weights)
        
        # Combinar outputs del nivel
        combined_output = np.mean(attention_outputs, axis=0)
        combined_weights = np.mean(attention_weights_list, axis=0)
        
        return combined_output, combined_weights
    
    def _prepare_input_embeddings(self, tokens: List[str]) -> np.ndarray:
        """Prepara embeddings de entrada."""
        # Implementación simplificada - en producción usaría un modelo de embeddings real
        seq_len = len(tokens)
        embedding_dim = self.primary_dimension
        
        # Generar embeddings aleatorios normalizados
        embeddings = np.random.randn(1, seq_len, embedding_dim)
        embeddings = embeddings / np.linalg.norm(embeddings, axis=-1, keepdims=True)
        
        return embeddings
    
    def _prepare_context_embeddings(self, tokens: List[str]) -> np.ndarray:
        """Prepara embeddings de contexto."""
        return self._prepare_input_embeddings(tokens)
    
    def _project_to_secondary(self, embeddings: np.ndarray) -> np.ndarray:
        """Proyecta embeddings a dimensión secundaria."""
        if embeddings.shape[-1] == self.secondary_dimension:
            return embeddings
        
        # Proyección lineal simplificada
        projection_matrix = np.random.randn(embeddings.shape[-1], self.secondary_dimension)
        projection_matrix = projection_matrix / np.linalg.norm(projection_matrix, axis=0, keepdims=True)
        
        projected = np.matmul(embeddings, projection_matrix)
        return projected
    
    def _combine_attention_outputs(self, outputs: List[np.ndarray], heads: List[AttentionHead]) -> np.ndarray:
        """Combina outputs de atención."""
        if not outputs:
            return np.zeros((1, 1, self.primary_dimension))
        
        # Ponderar por rendimiento de las cabezas
        weights = np.array([head.performance_score for head in heads])
        weights = weights / np.sum(weights)
        
        # Combinar ponderadamente
        combined = np.zeros_like(outputs[0])
        for output, weight in zip(outputs, weights):
            combined += output * weight
        
        return combined
    
    def _combine_hierarchical_outputs(self, local_output: np.ndarray, global_output: np.ndarray) -> np.ndarray:
        """Combina outputs jerárquicos."""
        # Proyección a dimensión común
        if local_output.shape[-1] != global_output.shape[-1]:
            global_output = self._project_to_secondary(global_output)
        
        # Combinar con pesos
        alpha = 0.7  # Peso para output local
        beta = 0.3   # Peso para output global
        
        combined = alpha * local_output + beta * global_output
        return combined
    
    def _evaluate_query_complexity(self, query: AttentionQuery) -> float:
        """Evalúa complejidad de la query."""
        # Factores de complejidad
        token_count = len(query.input_tokens)
        context_presence = 1.0 if query.context_tokens else 0.0
        attention_types_count = len(query.attention_types)
        
        # Normalizar factores
        token_complexity = min(1.0, token_count / 100.0)
        context_complexity = context_presence * 0.3
        type_complexity = min(1.0, attention_types_count / 4.0)
        
        # Combinar
        complexity = (token_complexity * 0.5 + 
                     context_complexity * 0.3 + 
                     type_complexity * 0.2)
        
        return complexity
    
    def _calculate_attention_quality(self, output: np.ndarray, weights: np.ndarray) -> float:
        """Calcula calidad de la atención."""
        try:
            # Factores de calidad
            output_norm = np.linalg.norm(output)
            weight_entropy = self._calculate_entropy(weights)
            weight_concentration = np.max(weights, axis=-1).mean()
            
            # Normalizar factores
            norm_quality = min(1.0, output_norm / 10.0)
            entropy_quality = min(1.0, weight_entropy / 5.0)
            concentration_quality = weight_concentration
            
            # Combinar
            quality = (norm_quality * 0.3 + 
                      entropy_quality * 0.3 + 
                      concentration_quality * 0.4)
            
            return min(1.0, max(0.0, quality))
            
        except Exception as e:
            logger.error(f"Error calculando calidad de atención: {e}")
            return 0.5
    
    def _calculate_entropy(self, weights: np.ndarray) -> float:
        """Calcula entropía de los pesos de atención."""
        try:
            # Evitar log(0)
            weights_safe = np.where(weights == 0, 1e-9, weights)
            entropy = -np.sum(weights_safe * np.log(weights_safe), axis=-1)
            return np.mean(entropy)
        except:
            return 0.0
    
    def _create_fallback_result(self, query: AttentionQuery) -> AttentionResult:
        """Crea resultado de fallback."""
        seq_len = len(query.input_tokens)
        fallback_weights = np.ones((1, seq_len, seq_len)) / seq_len
        fallback_output = np.zeros((1, seq_len, self.primary_dimension))
        
        return AttentionResult(
            query_id=query.query_id,
            attention_weights=fallback_weights,
            output_embeddings=fallback_output,
            attention_heads_used=[],
            processing_time_ms=0.0,
            memory_usage_mb=0.0,
            quality_score=0.3
        )
    
    def _generate_cache_key(self, query: AttentionQuery) -> str:
        """Genera clave de cache."""
        key_data = {
            'input_tokens': query.input_tokens,
            'context_tokens': query.context_tokens,
            'attention_types': [t.value for t in query.attention_types],
            'max_sequence_length': query.max_sequence_length,
            'temperature': query.temperature
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _update_cache(self, cache_key: str, result: AttentionResult):
        """Actualiza cache."""
        if len(self.result_cache) >= self.cache_max_size:
            # Remover entrada más antigua
            oldest_key = min(self.result_cache.keys())
            del self.result_cache[oldest_key]
        
        self.result_cache[cache_key] = result
    
    def _update_stats(self, result: AttentionResult):
        """Actualiza estadísticas."""
        self.attention_stats['total_queries_processed'] += 1
        
        # Actualizar tiempo promedio
        total_queries = self.attention_stats['total_queries_processed']
        current_avg = self.attention_stats['average_processing_time_ms']
        new_avg = ((current_avg * (total_queries - 1)) + result.processing_time_ms) / total_queries
        self.attention_stats['average_processing_time_ms'] = new_avg
        
        # Actualizar calidad promedio
        current_quality = self.attention_stats['average_quality_score']
        new_quality = ((current_quality * (total_queries - 1)) + result.quality_score) / total_queries
        self.attention_stats['average_quality_score'] = new_quality
        
        # Actualizar uso de cabezas
        for head_id in result.attention_heads_used:
            self.attention_stats['attention_head_usage'][head_id] += 1
    
    def update_head_performance(self, head_id: str, success: bool, quality_score: float):
        """Actualiza rendimiento de una cabeza de atención."""
        if head_id in self.attention_heads:
            head = self.attention_heads[head_id]
            
            if success:
                head.performance_score = min(1.0, head.performance_score + 0.01)
            else:
                head.performance_score = max(0.0, head.performance_score - 0.02)
            
            head.last_used = datetime.now()
            
            logger.debug(f"Rendimiento actualizado para {head_id}: {head.performance_score:.3f}")
    
    def get_attention_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de atención."""
        return {
            'attention_stats': dict(self.attention_stats),
            'total_heads': len(self.attention_heads),
            'active_heads': sum(1 for h in self.attention_heads.values() if h.is_active),
            'cache_size': len(self.result_cache),
            'mode': self.mode.value
        }
    
    def get_head_status(self) -> Dict[str, Any]:
        """Obtiene estado de las cabezas de atención."""
        head_status = {}
        
        for head_id, head in self.attention_heads.items():
            head_status[head_id] = {
                'type': head.attention_type.value,
                'dimension': head.dimension,
                'num_heads': head.num_heads,
                'performance_score': head.performance_score,
                'is_active': head.is_active,
                'last_used': head.last_used.isoformat(),
                'usage_count': self.attention_stats['attention_head_usage'].get(head_id, 0)
            }
        
        return head_status


if __name__ == "__main__":
    # Test del DuoAttention
    logging.basicConfig(level=logging.INFO)
    
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
        print(f"Query: {query.query_id}")
        print(f"Quality Score: {result.quality_score:.3f}")
        print(f"Processing Time: {result.processing_time_ms:.2f}ms")
        print(f"Heads Used: {len(result.attention_heads_used)}")
        print(f"Output Shape: {result.output_embeddings.shape}")
        print("-" * 50)
    
    # Mostrar estadísticas
    stats = duo_attention.get_attention_stats()
    print(f"Estadísticas: {stats}")
    
    # Mostrar estado de cabezas
    head_status = duo_attention.get_head_status()
    print(f"Estado de cabezas: {len(head_status)} cabezas activas")
