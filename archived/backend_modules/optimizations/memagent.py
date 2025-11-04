#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MemAgent - Sistema de memoria extendida (512K tokens) con gestión inteligente.
"""

import logging
import json
import os
import hashlib
import zlib
import pickle
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Tipos de memoria."""
    EPISODIC = "episodic"  # Eventos específicos
    SEMANTIC = "semantic"  # Conocimiento general
    PROCEDURAL = "procedural"  # Habilidades y procedimientos
    WORKING = "working"  # Memoria de trabajo
    LONG_TERM = "long_term"  # Memoria a largo plazo


class MemoryPriority(Enum):
    """Prioridades de memoria."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    TRIVIAL = 5


class CompressionMethod(Enum):
    """Métodos de compresión."""
    NONE = "none"
    GZIP = "gzip"
    LZ4 = "lz4"
    QUANTIZED = "quantized"


@dataclass
class MemoryChunk:
    """Chunk de memoria."""
    chunk_id: str
    memory_type: MemoryType
    priority: MemoryPriority
    content: str
    tokens: int
    compressed_size: int
    compression_method: CompressionMethod
    access_count: int
    last_accessed: datetime
    created_at: datetime
    expires_at: Optional[datetime]
    tags: List[str]
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None


@dataclass
class MemoryQuery:
    """Query de memoria."""
    query_id: str
    query_text: str
    memory_types: List[MemoryType]
    max_tokens: int
    similarity_threshold: float
    priority_filter: Optional[MemoryPriority]
    time_range: Optional[Tuple[datetime, datetime]]
    tags_filter: Optional[List[str]]


@dataclass
class MemoryResult:
    """Resultado de búsqueda en memoria."""
    query_id: str
    chunks: List[MemoryChunk]
    total_tokens: int
    similarity_scores: List[float]
    search_time_ms: float
    compression_ratio: float


class MemoryCompressor:
    """Compresor de memoria."""
    
    def __init__(self):
        self.compression_stats = {
            'total_compressions': 0,
            'total_decompressions': 0,
            'total_bytes_saved': 0,
            'average_compression_ratio': 0.0
        }
    
    def compress(self, content: str, method: CompressionMethod = CompressionMethod.GZIP) -> Tuple[bytes, float]:
        """Comprime contenido."""
        try:
            content_bytes = content.encode('utf-8')
            original_size = len(content_bytes)
            
            if method == CompressionMethod.NONE:
                compressed = content_bytes
            elif method == CompressionMethod.GZIP:
                compressed = zlib.compress(content_bytes, level=6)
            elif method == CompressionMethod.LZ4:
                # Implementación simplificada - en producción usaría lz4
                compressed = zlib.compress(content_bytes, level=1)
            elif method == CompressionMethod.QUANTIZED:
                # Compresión por cuantización de embeddings
                compressed = self._quantize_content(content)
            else:
                compressed = content_bytes
            
            compressed_size = len(compressed)
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            
            # Actualizar estadísticas
            self.compression_stats['total_compressions'] += 1
            self.compression_stats['total_bytes_saved'] += (original_size - compressed_size)
            
            return compressed, compression_ratio
            
        except Exception as e:
            logger.error(f"Error comprimiendo contenido: {e}")
            return content.encode('utf-8'), 1.0
    
    def decompress(self, compressed_data: bytes, method: CompressionMethod = CompressionMethod.GZIP) -> str:
        """Descomprime contenido."""
        try:
            if method == CompressionMethod.NONE:
                decompressed = compressed_data
            elif method == CompressionMethod.GZIP:
                decompressed = zlib.decompress(compressed_data)
            elif method == CompressionMethod.LZ4:
                # Implementación simplificada
                decompressed = zlib.decompress(compressed_data)
            elif method == CompressionMethod.QUANTIZED:
                decompressed = self._dequantize_content(compressed_data)
            else:
                decompressed = compressed_data
            
            self.compression_stats['total_decompressions'] += 1
            
            return decompressed.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error descomprimiendo contenido: {e}")
            return compressed_data.decode('utf-8', errors='ignore')
    
    def _quantize_content(self, content: str) -> bytes:
        """Cuantiza contenido para compresión."""
        # Implementación simplificada - en producción usaría técnicas más avanzadas
        return content.encode('utf-8')
    
    def _dequantize_content(self, compressed_data: bytes) -> bytes:
        """Descuantiza contenido."""
        return compressed_data


class MemoryIndex:
    """Índice de memoria para búsqueda eficiente."""
    
    def __init__(self):
        self.chunk_index: Dict[str, MemoryChunk] = {}
        self.type_index: Dict[MemoryType, Set[str]] = defaultdict(set)
        self.priority_index: Dict[MemoryPriority, Set[str]] = defaultdict(set)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.time_index: Dict[datetime, Set[str]] = defaultdict(set)
        self.embedding_index: Dict[str, np.ndarray] = {}
        
        logger.info("MemoryIndex inicializado")
    
    def add_chunk(self, chunk: MemoryChunk):
        """Agrega chunk al índice."""
        self.chunk_index[chunk.chunk_id] = chunk
        
        # Actualizar índices
        self.type_index[chunk.memory_type].add(chunk.chunk_id)
        self.priority_index[chunk.priority].add(chunk.chunk_id)
        
        for tag in chunk.tags:
            self.tag_index[tag].add(chunk.chunk_id)
        
        # Índice temporal (por día)
        day_key = chunk.created_at.date()
        self.time_index[day_key].add(chunk.chunk_id)
        
        # Índice de embeddings
        if chunk.embedding is not None:
            self.embedding_index[chunk.chunk_id] = chunk.embedding
    
    def remove_chunk(self, chunk_id: str):
        """Remueve chunk del índice."""
        if chunk_id not in self.chunk_index:
            return
        
        chunk = self.chunk_index[chunk_id]
        
        # Remover de índices
        self.type_index[chunk.memory_type].discard(chunk_id)
        self.priority_index[chunk.priority].discard(chunk_id)
        
        for tag in chunk.tags:
            self.tag_index[tag].discard(chunk_id)
        
        day_key = chunk.created_at.date()
        self.time_index[day_key].discard(chunk_id)
        
        if chunk_id in self.embedding_index:
            del self.embedding_index[chunk_id]
        
        del self.chunk_index[chunk_id]
    
    def search_by_type(self, memory_types: List[MemoryType]) -> Set[str]:
        """Busca chunks por tipo de memoria."""
        result = set()
        for memory_type in memory_types:
            result.update(self.type_index[memory_type])
        return result
    
    def search_by_priority(self, max_priority: MemoryPriority) -> Set[str]:
        """Busca chunks por prioridad."""
        result = set()
        for priority in MemoryPriority:
            if priority.value <= max_priority.value:
                result.update(self.priority_index[priority])
        return result
    
    def search_by_tags(self, tags: List[str]) -> Set[str]:
        """Busca chunks por tags."""
        if not tags:
            return set()
        
        result = self.tag_index[tags[0]]
        for tag in tags[1:]:
            result = result.intersection(self.tag_index[tag])
        return result
    
    def search_by_time_range(self, start_time: datetime, end_time: datetime) -> Set[str]:
        """Busca chunks por rango de tiempo."""
        result = set()
        current_date = start_time.date()
        end_date = end_time.date()
        
        while current_date <= end_date:
            result.update(self.time_index[current_date])
            current_date += timedelta(days=1)
        
        return result


class MemAgent:
    """Sistema de memoria extendida (512K tokens)."""
    
    def __init__(self, 
                 max_tokens: int = 512000,  # 512K tokens
                 compression_enabled: bool = True,
                 memory_dir: str = "backend/data/memagent"):
        self.max_tokens = max_tokens
        self.compression_enabled = compression_enabled
        self.memory_dir = memory_dir
        
        # Componentes
        self.compressor = MemoryCompressor()
        self.index = MemoryIndex()
        
        # Estado de memoria
        self.current_tokens = 0
        self.chunk_counter = 0
        
        # Configuración
        self.compression_threshold = 1000  # Comprimir chunks > 1000 tokens
        self.cleanup_threshold = 0.9  # Limpiar cuando se alcance 90% de capacidad
        
        # Estadísticas
        self.memory_stats = {
            'total_chunks_created': 0,
            'total_chunks_removed': 0,
            'total_queries_processed': 0,
            'average_query_time_ms': 0.0,
            'compression_savings_bytes': 0,
            'cache_hit_rate': 0.0
        }
        
        # Cache de consultas frecuentes
        self.query_cache: Dict[str, MemoryResult] = {}
        self.cache_max_size = 1000
        
        # Asegurar directorio
        os.makedirs(memory_dir, exist_ok=True)
        
        logger.info(f"MemAgent inicializado: max_tokens={max_tokens}, compression={compression_enabled}")
    
    def store_memory(self, 
                    content: str,
                    memory_type: MemoryType = MemoryType.SEMANTIC,
                    priority: MemoryPriority = MemoryPriority.MEDIUM,
                    tags: Optional[List[str]] = None,
                    expires_at: Optional[datetime] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> str:
        """Almacena memoria."""
        try:
            # Calcular tokens (aproximación)
            tokens = len(content.split())
            
            # Verificar capacidad
            if self.current_tokens + tokens > self.max_tokens:
                self._cleanup_memory()
            
            # Crear chunk
            chunk_id = self._generate_chunk_id()
            chunk = MemoryChunk(
                chunk_id=chunk_id,
                memory_type=memory_type,
                priority=priority,
                content=content,
                tokens=tokens,
                compressed_size=0,
                compression_method=CompressionMethod.NONE,
                access_count=0,
                last_accessed=datetime.now(),
                created_at=datetime.now(),
                expires_at=expires_at,
                tags=tags or [],
                metadata=metadata or {}
            )
            
            # Comprimir si es necesario
            if self.compression_enabled and tokens > self.compression_threshold:
                compressed_data, compression_ratio = self.compressor.compress(
                    content, CompressionMethod.GZIP
                )
                chunk.compressed_size = len(compressed_data)
                chunk.compression_method = CompressionMethod.GZIP
                
                # Guardar datos comprimidos
                self._save_compressed_chunk(chunk_id, compressed_data)
            
            # Agregar al índice
            self.index.add_chunk(chunk)
            
            # Actualizar contadores
            self.current_tokens += tokens
            self.chunk_counter += 1
            self.memory_stats['total_chunks_created'] += 1
            
            logger.info(f"Memoria almacenada: {chunk_id} ({tokens} tokens, {memory_type.value})")
            return chunk_id
            
        except Exception as e:
            logger.error(f"Error almacenando memoria: {e}")
            return ""
    
    def retrieve_memory(self, query: MemoryQuery) -> MemoryResult:
        """Recupera memoria basada en query."""
        try:
            start_time = datetime.now()
            
            # Verificar cache
            cache_key = self._generate_cache_key(query)
            if cache_key in self.query_cache:
                result = self.query_cache[cache_key]
                result.chunks = [self._load_chunk(chunk.chunk_id) for chunk in result.chunks]
                self.memory_stats['cache_hit_rate'] += 1
                return result
            
            # Buscar chunks relevantes
            candidate_chunks = self._find_candidate_chunks(query)
            
            # Filtrar y rankear
            relevant_chunks = self._rank_chunks(candidate_chunks, query)
            
            # Limitar por tokens
            selected_chunks = self._limit_by_tokens(relevant_chunks, query.max_tokens)
            
            # Calcular métricas
            total_tokens = sum(chunk.tokens for chunk in selected_chunks)
            search_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Crear resultado
            result = MemoryResult(
                query_id=query.query_id,
                chunks=selected_chunks,
                total_tokens=total_tokens,
                similarity_scores=[0.8] * len(selected_chunks),  # Simplificado
                search_time_ms=search_time,
                compression_ratio=self._calculate_compression_ratio(selected_chunks)
            )
            
            # Actualizar cache
            self._update_cache(cache_key, result)
            
            # Actualizar estadísticas
            self.memory_stats['total_queries_processed'] += 1
            self.memory_stats['average_query_time_ms'] = (
                (self.memory_stats['average_query_time_ms'] * (self.memory_stats['total_queries_processed'] - 1) + 
                 search_time) / self.memory_stats['total_queries_processed']
            )
            
            # Actualizar acceso a chunks
            for chunk in selected_chunks:
                chunk.access_count += 1
                chunk.last_accessed = datetime.now()
            
            logger.info(f"Memoria recuperada: {len(selected_chunks)} chunks, {total_tokens} tokens")
            return result
            
        except Exception as e:
            logger.error(f"Error recuperando memoria: {e}")
            return MemoryResult(
                query_id=query.query_id,
                chunks=[],
                total_tokens=0,
                similarity_scores=[],
                search_time_ms=0.0,
                compression_ratio=1.0
            )
    
    def _find_candidate_chunks(self, query: MemoryQuery) -> List[MemoryChunk]:
        """Encuentra chunks candidatos para la query."""
        candidate_ids = set()
        
        # Buscar por tipo de memoria
        if query.memory_types:
            type_ids = self.index.search_by_type(query.memory_types)
            candidate_ids.update(type_ids)
        else:
            candidate_ids.update(self.index.chunk_index.keys())
        
        # Filtrar por prioridad
        if query.priority_filter:
            priority_ids = self.index.search_by_priority(query.priority_filter)
            candidate_ids = candidate_ids.intersection(priority_ids)
        
        # Filtrar por tags
        if query.tags_filter:
            tag_ids = self.index.search_by_tags(query.tags_filter)
            candidate_ids = candidate_ids.intersection(tag_ids)
        
        # Filtrar por rango de tiempo
        if query.time_range:
            time_ids = self.index.search_by_time_range(query.time_range[0], query.time_range[1])
            candidate_ids = candidate_ids.intersection(time_ids)
        
        # Cargar chunks
        candidate_chunks = []
        for chunk_id in candidate_ids:
            chunk = self._load_chunk(chunk_id)
            if chunk and not self._is_expired(chunk):
                candidate_chunks.append(chunk)
        
        return candidate_chunks
    
    def _rank_chunks(self, chunks: List[MemoryChunk], query: MemoryQuery) -> List[MemoryChunk]:
        """Rankea chunks por relevancia."""
        # Implementación simplificada - en producción usaría embeddings
        def chunk_score(chunk: MemoryChunk) -> float:
            score = 0.0
            
            # Score por prioridad (inverso)
            score += (6 - chunk.priority.value) * 0.2
            
            # Score por acceso reciente
            days_since_access = (datetime.now() - chunk.last_accessed).days
            score += max(0, 1.0 - (days_since_access / 30.0)) * 0.3
            
            # Score por frecuencia de acceso
            score += min(1.0, chunk.access_count / 100.0) * 0.2
            
            # Score por similitud de contenido (simplificado)
            content_similarity = self._calculate_content_similarity(chunk.content, query.query_text)
            score += content_similarity * 0.3
            
            return score
        
        # Ordenar por score
        ranked_chunks = sorted(chunks, key=chunk_score, reverse=True)
        return ranked_chunks
    
    def _limit_by_tokens(self, chunks: List[MemoryChunk], max_tokens: int) -> List[MemoryChunk]:
        """Limita chunks por número de tokens."""
        selected_chunks = []
        current_tokens = 0
        
        for chunk in chunks:
            if current_tokens + chunk.tokens <= max_tokens:
                selected_chunks.append(chunk)
                current_tokens += chunk.tokens
            else:
                break
        
        return selected_chunks
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calcula similitud entre contenidos."""
        # Implementación simplificada - en producción usaría embeddings
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_compression_ratio(self, chunks: List[MemoryChunk]) -> float:
        """Calcula ratio de compresión promedio."""
        if not chunks:
            return 1.0
        
        total_original = sum(chunk.tokens * 4 for chunk in chunks)  # Aproximación
        total_compressed = sum(chunk.compressed_size for chunk in chunks)
        
        return total_compressed / total_original if total_original > 0 else 1.0
    
    def _cleanup_memory(self):
        """Limpia memoria para liberar espacio."""
        try:
            # Obtener chunks ordenados por prioridad y último acceso
            all_chunks = list(self.index.chunk_index.values())
            all_chunks.sort(key=lambda x: (x.priority.value, x.last_accessed))
            
            # Remover chunks de baja prioridad y antiguos
            chunks_to_remove = []
            tokens_to_free = self.current_tokens - int(self.max_tokens * 0.7)  # Liberar hasta 70%
            
            current_tokens_to_free = 0
            for chunk in all_chunks:
                if (chunk.priority.value >= MemoryPriority.LOW.value and 
                    current_tokens_to_free < tokens_to_free):
                    chunks_to_remove.append(chunk)
                    current_tokens_to_free += chunk.tokens
            
            # Remover chunks
            for chunk in chunks_to_remove:
                self._remove_chunk(chunk.chunk_id)
            
            logger.info(f"Limpieza de memoria: {len(chunks_to_remove)} chunks removidos, {current_tokens_to_free} tokens liberados")
            
        except Exception as e:
            logger.error(f"Error en limpieza de memoria: {e}")
    
    def _remove_chunk(self, chunk_id: str):
        """Remueve chunk de la memoria."""
        if chunk_id not in self.index.chunk_index:
            return
        
        chunk = self.index.chunk_index[chunk_id]
        
        # Remover del índice
        self.index.remove_chunk(chunk_id)
        
        # Actualizar contadores
        self.current_tokens -= chunk.tokens
        self.memory_stats['total_chunks_removed'] += 1
        
        # Remover archivo comprimido si existe
        compressed_file = os.path.join(self.memory_dir, f"{chunk_id}.compressed")
        if os.path.exists(compressed_file):
            os.remove(compressed_file)
    
    def _load_chunk(self, chunk_id: str) -> Optional[MemoryChunk]:
        """Carga chunk desde el índice."""
        if chunk_id not in self.index.chunk_index:
            return None
        
        chunk = self.index.chunk_index[chunk_id]
        
        # Si está comprimido, descomprimir
        if chunk.compression_method != CompressionMethod.NONE:
            compressed_file = os.path.join(self.memory_dir, f"{chunk_id}.compressed")
            if os.path.exists(compressed_file):
                with open(compressed_file, 'rb') as f:
                    compressed_data = f.read()
                chunk.content = self.compressor.decompress(compressed_data, chunk.compression_method)
        
        return chunk
    
    def _save_compressed_chunk(self, chunk_id: str, compressed_data: bytes):
        """Guarda chunk comprimido."""
        compressed_file = os.path.join(self.memory_dir, f"{chunk_id}.compressed")
        with open(compressed_file, 'wb') as f:
            f.write(compressed_data)
    
    def _is_expired(self, chunk: MemoryChunk) -> bool:
        """Verifica si chunk ha expirado."""
        if chunk.expires_at is None:
            return False
        return datetime.now() > chunk.expires_at
    
    def _generate_chunk_id(self) -> str:
        """Genera ID único para chunk."""
        self.chunk_counter += 1
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"chunk_{timestamp}_{self.chunk_counter:06d}"
    
    def _generate_cache_key(self, query: MemoryQuery) -> str:
        """Genera clave de cache para query."""
        key_data = {
            'query_text': query.query_text,
            'memory_types': [t.value for t in query.memory_types],
            'max_tokens': query.max_tokens,
            'similarity_threshold': query.similarity_threshold,
            'priority_filter': query.priority_filter.value if query.priority_filter else None,
            'tags_filter': query.tags_filter
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _update_cache(self, cache_key: str, result: MemoryResult):
        """Actualiza cache de consultas."""
        if len(self.query_cache) >= self.cache_max_size:
            # Remover entrada más antigua
            oldest_key = min(self.query_cache.keys())
            del self.query_cache[oldest_key]
        
        self.query_cache[cache_key] = result
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de memoria."""
        return {
            'memory_stats': self.memory_stats,
            'compression_stats': self.compressor.compression_stats,
            'current_tokens': self.current_tokens,
            'max_tokens': self.max_tokens,
            'utilization_percentage': (self.current_tokens / self.max_tokens) * 100,
            'total_chunks': len(self.index.chunk_index),
            'cache_size': len(self.query_cache)
        }
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de memoria."""
        summary = {
            'by_type': defaultdict(int),
            'by_priority': defaultdict(int),
            'by_tags': defaultdict(int),
            'total_tokens_by_type': defaultdict(int)
        }
        
        for chunk in self.index.chunk_index.values():
            summary['by_type'][chunk.memory_type.value] += 1
            summary['by_priority'][chunk.priority.value] += 1
            summary['total_tokens_by_type'][chunk.memory_type.value] += chunk.tokens
            
            for tag in chunk.tags:
                summary['by_tags'][tag] += 1
        
        return dict(summary)


if __name__ == "__main__":
    # Test del MemAgent
    logging.basicConfig(level=logging.INFO)
    
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
        print(f"Memoria almacenada: {chunk_id}")
    
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
    print(f"\nConsulta: {query.query_text}")
    print(f"Chunks encontrados: {len(result.chunks)}")
    print(f"Total tokens: {result.total_tokens}")
    print(f"Tiempo de búsqueda: {result.search_time_ms:.2f}ms")
    
    for chunk in result.chunks:
        print(f"- {chunk.chunk_id}: {chunk.content[:50]}... ({chunk.tokens} tokens)")
    
    # Mostrar estadísticas
    stats = memagent.get_memory_stats()
    print(f"\nEstadísticas: {stats}")
    
    # Mostrar resumen
    summary = memagent.get_memory_summary()
    print(f"Resumen: {summary}")
