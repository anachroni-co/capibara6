#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aggressive Caching - Sistema de caché agresivo para optimización de rendimiento.
"""

import logging
import json
import os
import time
import hashlib
import pickle
import threading
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

logger = logging.getLogger(__name__)


class CacheLevel(Enum):
    """Niveles de caché."""
    L1 = "l1"  # Memoria RAM (más rápido)
    L2 = "l2"  # SSD (rápido)
    L3 = "l3"  # HDD (lento)
    DISTRIBUTED = "distributed"  # Red distribuida


class CacheStrategy(Enum):
    """Estrategias de caché."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    ADAPTIVE = "adaptive"  # Adaptativo
    PREDICTIVE = "predictive"  # Predictivo


class CacheType(Enum):
    """Tipos de caché."""
    QUERY_RESULT = "query_result"
    EMBEDDING = "embedding"
    MODEL_OUTPUT = "model_output"
    COMPUTATION = "computation"
    METADATA = "metadata"


@dataclass
class CacheEntry:
    """Entrada de caché."""
    key: str
    value: Any
    cache_type: CacheType
    cache_level: CacheLevel
    size_bytes: int
    created_at: datetime
    last_accessed: datetime
    access_count: int
    ttl_seconds: Optional[int]
    expires_at: Optional[datetime]
    metadata: Dict[str, Any]


@dataclass
class CacheStats:
    """Estadísticas de caché."""
    total_entries: int
    total_size_bytes: int
    hit_count: int
    miss_count: int
    hit_rate: float
    eviction_count: int
    average_access_time_ms: float
    cache_efficiency: float


class L1Cache:
    """Caché L1 (Memoria RAM)."""
    
    def __init__(self, max_size_mb: int = 1024):
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size_bytes = 0
        
        # Almacenamiento en memoria
        self.entries: Dict[str, CacheEntry] = {}
        self.access_order: deque = deque()
        
        # Estadísticas
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_accesses': 0
        }
        
        # Lock para thread safety
        self.lock = threading.RLock()
        
        logger.info(f"L1Cache inicializado: max_size={max_size_mb}MB")
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del caché."""
        with self.lock:
            self.stats['total_accesses'] += 1
            
            if key in self.entries:
                entry = self.entries[key]
                
                # Verificar expiración
                if entry.expires_at and datetime.now() > entry.expires_at:
                    self._remove_entry(key)
                    self.stats['misses'] += 1
                    return None
                
                # Actualizar acceso
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                
                # Actualizar orden de acceso
                if key in self.access_order:
                    self.access_order.remove(key)
                self.access_order.append(key)
                
                self.stats['hits'] += 1
                return entry.value
            else:
                self.stats['misses'] += 1
                return None
    
    def set(self, key: str, value: Any, cache_type: CacheType, 
            ttl_seconds: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Establece valor en el caché."""
        with self.lock:
            try:
                # Calcular tamaño
                size_bytes = self._calculate_size(value)
                
                # Verificar si cabe
                if size_bytes > self.max_size_bytes:
                    logger.warning(f"Valor demasiado grande para L1 cache: {size_bytes} bytes")
                    return False
                
                # Crear entrada
                expires_at = None
                if ttl_seconds:
                    expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
                
                entry = CacheEntry(
                    key=key,
                    value=value,
                    cache_type=cache_type,
                    cache_level=CacheLevel.L1,
                    size_bytes=size_bytes,
                    created_at=datetime.now(),
                    last_accessed=datetime.now(),
                    access_count=1,
                    ttl_seconds=ttl_seconds,
                    expires_at=expires_at,
                    metadata=metadata or {}
                )
                
                # Remover entrada existente si existe
                if key in self.entries:
                    self._remove_entry(key)
                
                # Verificar espacio disponible
                while self.current_size_bytes + size_bytes > self.max_size_bytes:
                    if not self._evict_entry():
                        logger.warning("No se puede hacer espacio en L1 cache")
                        return False
                
                # Agregar entrada
                self.entries[key] = entry
                self.current_size_bytes += size_bytes
                self.access_order.append(key)
                
                logger.debug(f"Entrada agregada a L1 cache: {key} ({size_bytes} bytes)")
                return True
                
            except Exception as e:
                logger.error(f"Error estableciendo valor en L1 cache: {e}")
                return False
    
    def _remove_entry(self, key: str):
        """Remueve entrada del caché."""
        if key in self.entries:
            entry = self.entries[key]
            self.current_size_bytes -= entry.size_bytes
            del self.entries[key]
            
            if key in self.access_order:
                self.access_order.remove(key)
    
    def _evict_entry(self) -> bool:
        """Expulsa entrada del caché (LRU)."""
        if not self.access_order:
            return False
        
        # Remover entrada menos recientemente usada
        oldest_key = self.access_order.popleft()
        if oldest_key in self.entries:
            self._remove_entry(oldest_key)
            self.stats['evictions'] += 1
            logger.debug(f"Entrada expulsada de L1 cache: {oldest_key}")
            return True
        
        return False
    
    def _calculate_size(self, value: Any) -> int:
        """Calcula tamaño aproximado del valor."""
        try:
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (int, float)):
                return 8
            elif isinstance(value, np.ndarray):
                return value.nbytes
            else:
                # Serializar para estimar tamaño
                serialized = pickle.dumps(value)
                return len(serialized)
        except:
            return 1024  # Tamaño por defecto
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché."""
        with self.lock:
            hit_rate = self.stats['hits'] / max(1, self.stats['total_accesses'])
            
            return {
                'level': 'L1',
                'max_size_mb': self.max_size_mb,
                'current_size_mb': self.current_size_bytes / (1024 * 1024),
                'utilization_percentage': (self.current_size_bytes / self.max_size_bytes) * 100,
                'total_entries': len(self.entries),
                'hit_rate': hit_rate,
                'stats': self.stats.copy()
            }


class L2Cache:
    """Caché L2 (SSD)."""
    
    def __init__(self, cache_dir: str = "backend/data/cache/l2", max_size_mb: int = 10240):
        self.cache_dir = cache_dir
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size_bytes = 0
        
        # Asegurar directorio
        os.makedirs(cache_dir, exist_ok=True)
        
        # Índice de entradas
        self.entries: Dict[str, CacheEntry] = {}
        self.access_order: deque = deque()
        
        # Estadísticas
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_accesses': 0,
            'disk_reads': 0,
            'disk_writes': 0
        }
        
        # Lock para thread safety
        self.lock = threading.RLock()
        
        # Cargar entradas existentes
        self._load_existing_entries()
        
        logger.info(f"L2Cache inicializado: cache_dir={cache_dir}, max_size={max_size_mb}MB")
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene valor del caché."""
        with self.lock:
            self.stats['total_accesses'] += 1
            
            if key in self.entries:
                entry = self.entries[key]
                
                # Verificar expiración
                if entry.expires_at and datetime.now() > entry.expires_at:
                    self._remove_entry(key)
                    self.stats['misses'] += 1
                    return None
                
                # Cargar valor desde disco
                value = self._load_from_disk(key)
                if value is None:
                    self._remove_entry(key)
                    self.stats['misses'] += 1
                    return None
                
                # Actualizar acceso
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                
                # Actualizar orden de acceso
                if key in self.access_order:
                    self.access_order.remove(key)
                self.access_order.append(key)
                
                self.stats['hits'] += 1
                self.stats['disk_reads'] += 1
                return value
            else:
                self.stats['misses'] += 1
                return None
    
    def set(self, key: str, value: Any, cache_type: CacheType, 
            ttl_seconds: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Establece valor en el caché."""
        with self.lock:
            try:
                # Calcular tamaño
                size_bytes = self._calculate_size(value)
                
                # Verificar si cabe
                if size_bytes > self.max_size_bytes:
                    logger.warning(f"Valor demasiado grande para L2 cache: {size_bytes} bytes")
                    return False
                
                # Crear entrada
                expires_at = None
                if ttl_seconds:
                    expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
                
                entry = CacheEntry(
                    key=key,
                    value=None,  # No almacenar valor en memoria
                    cache_type=cache_type,
                    cache_level=CacheLevel.L2,
                    size_bytes=size_bytes,
                    created_at=datetime.now(),
                    last_accessed=datetime.now(),
                    access_count=1,
                    ttl_seconds=ttl_seconds,
                    expires_at=expires_at,
                    metadata=metadata or {}
                )
                
                # Remover entrada existente si existe
                if key in self.entries:
                    self._remove_entry(key)
                
                # Verificar espacio disponible
                while self.current_size_bytes + size_bytes > self.max_size_bytes:
                    if not self._evict_entry():
                        logger.warning("No se puede hacer espacio en L2 cache")
                        return False
                
                # Guardar en disco
                if self._save_to_disk(key, value):
                    # Agregar entrada
                    self.entries[key] = entry
                    self.current_size_bytes += size_bytes
                    self.access_order.append(key)
                    self.stats['disk_writes'] += 1
                    
                    logger.debug(f"Entrada agregada a L2 cache: {key} ({size_bytes} bytes)")
                    return True
                else:
                    return False
                
            except Exception as e:
                logger.error(f"Error estableciendo valor en L2 cache: {e}")
                return False
    
    def _save_to_disk(self, key: str, value: Any) -> bool:
        """Guarda valor en disco."""
        try:
            file_path = os.path.join(self.cache_dir, f"{key}.cache")
            
            with open(file_path, 'wb') as f:
                pickle.dump(value, f)
            
            return True
            
        except Exception as e:
            logger.error(f"Error guardando en disco: {e}")
            return False
    
    def _load_from_disk(self, key: str) -> Optional[Any]:
        """Carga valor desde disco."""
        try:
            file_path = os.path.join(self.cache_dir, f"{key}.cache")
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'rb') as f:
                value = pickle.load(f)
            
            return value
            
        except Exception as e:
            logger.error(f"Error cargando desde disco: {e}")
            return None
    
    def _remove_entry(self, key: str):
        """Remueve entrada del caché."""
        if key in self.entries:
            entry = self.entries[key]
            self.current_size_bytes -= entry.size_bytes
            del self.entries[key]
            
            if key in self.access_order:
                self.access_order.remove(key)
            
            # Remover archivo del disco
            file_path = os.path.join(self.cache_dir, f"{key}.cache")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removiendo archivo de cache: {e}")
    
    def _evict_entry(self) -> bool:
        """Expulsa entrada del caché (LRU)."""
        if not self.access_order:
            return False
        
        # Remover entrada menos recientemente usada
        oldest_key = self.access_order.popleft()
        if oldest_key in self.entries:
            self._remove_entry(oldest_key)
            self.stats['evictions'] += 1
            logger.debug(f"Entrada expulsada de L2 cache: {oldest_key}")
            return True
        
        return False
    
    def _calculate_size(self, value: Any) -> int:
        """Calcula tamaño aproximado del valor."""
        try:
            serialized = pickle.dumps(value)
            return len(serialized)
        except:
            return 1024  # Tamaño por defecto
    
    def _load_existing_entries(self):
        """Carga entradas existentes del disco."""
        try:
            index_file = os.path.join(self.cache_dir, "index.json")
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                
                for key, entry_data in index_data.items():
                    entry = CacheEntry(
                        key=key,
                        value=None,
                        cache_type=CacheType(entry_data['cache_type']),
                        cache_level=CacheLevel.L2,
                        size_bytes=entry_data['size_bytes'],
                        created_at=datetime.fromisoformat(entry_data['created_at']),
                        last_accessed=datetime.fromisoformat(entry_data['last_accessed']),
                        access_count=entry_data['access_count'],
                        ttl_seconds=entry_data.get('ttl_seconds'),
                        expires_at=datetime.fromisoformat(entry_data['expires_at']) if entry_data.get('expires_at') else None,
                        metadata=entry_data.get('metadata', {})
                    )
                    
                    self.entries[key] = entry
                    self.current_size_bytes += entry.size_bytes
                    self.access_order.append(key)
                
                logger.info(f"Cargadas {len(self.entries)} entradas existentes de L2 cache")
                
        except Exception as e:
            logger.error(f"Error cargando entradas existentes: {e}")
    
    def _save_index(self):
        """Guarda índice de entradas."""
        try:
            index_file = os.path.join(self.cache_dir, "index.json")
            index_data = {}
            
            for key, entry in self.entries.items():
                index_data[key] = {
                    'cache_type': entry.cache_type.value,
                    'size_bytes': entry.size_bytes,
                    'created_at': entry.created_at.isoformat(),
                    'last_accessed': entry.last_accessed.isoformat(),
                    'access_count': entry.access_count,
                    'ttl_seconds': entry.ttl_seconds,
                    'expires_at': entry.expires_at.isoformat() if entry.expires_at else None,
                    'metadata': entry.metadata
                }
            
            with open(index_file, 'w') as f:
                json.dump(index_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error guardando índice: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché."""
        with self.lock:
            hit_rate = self.stats['hits'] / max(1, self.stats['total_accesses'])
            
            return {
                'level': 'L2',
                'max_size_mb': self.max_size_mb,
                'current_size_mb': self.current_size_bytes / (1024 * 1024),
                'utilization_percentage': (self.current_size_bytes / self.max_size_bytes) * 100,
                'total_entries': len(self.entries),
                'hit_rate': hit_rate,
                'stats': self.stats.copy()
            }


class AggressiveCache:
    """Sistema de caché agresivo multi-nivel."""
    
    def __init__(self, 
                 l1_size_mb: int = 1024,
                 l2_size_mb: int = 10240,
                 l2_cache_dir: str = "backend/data/cache/l2",
                 strategy: CacheStrategy = CacheStrategy.ADAPTIVE):
        self.strategy = strategy
        
        # Cachés por nivel
        self.l1_cache = L1Cache(max_size_mb=l1_size_mb)
        self.l2_cache = L2Cache(cache_dir=l2_cache_dir, max_size_mb=l2_size_mb)
        
        # Configuración
        self.default_ttl = {
            CacheType.QUERY_RESULT: 3600,      # 1 hora
            CacheType.EMBEDDING: 86400,        # 24 horas
            CacheType.MODEL_OUTPUT: 1800,      # 30 minutos
            CacheType.COMPUTATION: 7200,       # 2 horas
            CacheType.METADATA: 3600           # 1 hora
        }
        
        # Estadísticas globales
        self.global_stats = {
            'total_requests': 0,
            'l1_hits': 0,
            'l2_hits': 0,
            'misses': 0,
            'total_access_time_ms': 0.0
        }
        
        # Thread de limpieza
        self.cleanup_thread = None
        self.is_cleanup_running = False
        
        # Iniciar limpieza automática
        self._start_cleanup_thread()
        
        logger.info(f"AggressiveCache inicializado: L1={l1_size_mb}MB, L2={l2_size_mb}MB, strategy={strategy.value}")
    
    def _start_cleanup_thread(self):
        """Inicia thread de limpieza automática."""
        if self.is_cleanup_running:
            return
        
        self.is_cleanup_running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        
        logger.info("Thread de limpieza automática iniciado")
    
    def _cleanup_loop(self):
        """Loop de limpieza automática."""
        while self.is_cleanup_running:
            try:
                # Limpiar entradas expiradas
                self._cleanup_expired_entries()
                
                # Optimizar cachés
                self._optimize_caches()
                
                # Esperar 5 minutos
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Error en loop de limpieza: {e}")
                time.sleep(60)  # Esperar 1 minuto en caso de error
    
    def _cleanup_expired_entries(self):
        """Limpia entradas expiradas."""
        current_time = datetime.now()
        
        # Limpiar L1
        with self.l1_cache.lock:
            expired_keys = []
            for key, entry in self.l1_cache.entries.items():
                if entry.expires_at and current_time > entry.expires_at:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self.l1_cache._remove_entry(key)
        
        # Limpiar L2
        with self.l2_cache.lock:
            expired_keys = []
            for key, entry in self.l2_cache.entries.items():
                if entry.expires_at and current_time > entry.expires_at:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self.l2_cache._remove_entry(key)
        
        if expired_keys:
            logger.info(f"Limpiadas {len(expired_keys)} entradas expiradas")
    
    def _optimize_caches(self):
        """Optimiza cachés."""
        # Optimizar L1 basado en estrategia
        if self.strategy == CacheStrategy.ADAPTIVE:
            self._optimize_l1_adaptive()
        
        # Guardar índice de L2
        self.l2_cache._save_index()
    
    def _optimize_l1_adaptive(self):
        """Optimiza L1 cache de forma adaptativa."""
        l1_stats = self.l1_cache.get_stats()
        
        # Si la utilización es muy alta, ser más agresivo con la expulsión
        if l1_stats['utilization_percentage'] > 90:
            # Expulsar entradas menos usadas
            with self.l1_cache.lock:
                entries_by_access = sorted(
                    self.l1_cache.entries.items(),
                    key=lambda x: x[1].access_count
                )
                
                # Expulsar 10% de las entradas menos usadas
                num_to_evict = max(1, len(entries_by_access) // 10)
                for i in range(num_to_evict):
                    key = entries_by_access[i][0]
                    self.l1_cache._remove_entry(key)
    
    def get(self, key: str, cache_type: CacheType = CacheType.QUERY_RESULT) -> Optional[Any]:
        """Obtiene valor del caché."""
        start_time = time.time()
        self.global_stats['total_requests'] += 1
        
        # Intentar L1 primero
        value = self.l1_cache.get(key)
        if value is not None:
            self.global_stats['l1_hits'] += 1
            access_time = (time.time() - start_time) * 1000
            self.global_stats['total_access_time_ms'] += access_time
            return value
        
        # Intentar L2
        value = self.l2_cache.get(key)
        if value is not None:
            self.global_stats['l2_hits'] += 1
            
            # Promover a L1 si es pequeño
            if self._should_promote_to_l1(value, cache_type):
                self.l1_cache.set(key, value, cache_type, 
                                ttl_seconds=self.default_ttl.get(cache_type))
            
            access_time = (time.time() - start_time) * 1000
            self.global_stats['total_access_time_ms'] += access_time
            return value
        
        # Miss
        self.global_stats['misses'] += 1
        access_time = (time.time() - start_time) * 1000
        self.global_stats['total_access_time_ms'] += access_time
        return None
    
    def set(self, key: str, value: Any, cache_type: CacheType = CacheType.QUERY_RESULT,
            ttl_seconds: Optional[int] = None, promote_to_l1: bool = True) -> bool:
        """Establece valor en el caché."""
        # Usar TTL por defecto si no se especifica
        if ttl_seconds is None:
            ttl_seconds = self.default_ttl.get(cache_type, 3600)
        
        # Determinar nivel de caché
        if promote_to_l1 and self._should_promote_to_l1(value, cache_type):
            # Intentar L1 primero
            success = self.l1_cache.set(key, value, cache_type, ttl_seconds)
            if success:
                return True
        
        # Usar L2
        return self.l2_cache.set(key, value, cache_type, ttl_seconds)
    
    def _should_promote_to_l1(self, value: Any, cache_type: CacheType) -> bool:
        """Determina si un valor debe promoverse a L1."""
        # Calcular tamaño
        size_bytes = self.l1_cache._calculate_size(value)
        
        # Promover si es pequeño y frecuentemente accedido
        if size_bytes < 1024 * 1024:  # < 1MB
            return True
        
        # Promover embeddings y metadata
        if cache_type in [CacheType.EMBEDDING, CacheType.METADATA]:
            return size_bytes < 10 * 1024 * 1024  # < 10MB
        
        return False
    
    def invalidate(self, key: str) -> bool:
        """Invalida entrada del caché."""
        l1_removed = False
        l2_removed = False
        
        # Remover de L1
        with self.l1_cache.lock:
            if key in self.l1_cache.entries:
                self.l1_cache._remove_entry(key)
                l1_removed = True
        
        # Remover de L2
        with self.l2_cache.lock:
            if key in self.l2_cache.entries:
                self.l2_cache._remove_entry(key)
                l2_removed = True
        
        return l1_removed or l2_removed
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalida entradas que coincidan con un patrón."""
        removed_count = 0
        
        # Remover de L1
        with self.l1_cache.lock:
            keys_to_remove = [key for key in self.l1_cache.entries.keys() if pattern in key]
            for key in keys_to_remove:
                self.l1_cache._remove_entry(key)
                removed_count += 1
        
        # Remover de L2
        with self.l2_cache.lock:
            keys_to_remove = [key for key in self.l2_cache.entries.keys() if pattern in key]
            for key in keys_to_remove:
                self.l2_cache._remove_entry(key)
                removed_count += 1
        
        logger.info(f"Invalidadas {removed_count} entradas con patrón '{pattern}'")
        return removed_count
    
    def clear(self):
        """Limpia todos los cachés."""
        # Limpiar L1
        with self.l1_cache.lock:
            self.l1_cache.entries.clear()
            self.l1_cache.access_order.clear()
            self.l1_cache.current_size_bytes = 0
        
        # Limpiar L2
        with self.l2_cache.lock:
            self.l2_cache.entries.clear()
            self.l2_cache.access_order.clear()
            self.l2_cache.current_size_bytes = 0
        
        logger.info("Todos los cachés limpiados")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de todos los cachés."""
        l1_stats = self.l1_cache.get_stats()
        l2_stats = self.l2_cache.get_stats()
        
        # Calcular estadísticas globales
        total_requests = self.global_stats['total_requests']
        total_hits = self.global_stats['l1_hits'] + self.global_stats['l2_hits']
        overall_hit_rate = total_hits / max(1, total_requests)
        average_access_time = self.global_stats['total_access_time_ms'] / max(1, total_requests)
        
        return {
            'overall': {
                'total_requests': total_requests,
                'total_hits': total_hits,
                'total_misses': self.global_stats['misses'],
                'overall_hit_rate': overall_hit_rate,
                'average_access_time_ms': average_access_time,
                'l1_hit_rate': l1_stats['hit_rate'],
                'l2_hit_rate': l2_stats['hit_rate']
            },
            'l1_cache': l1_stats,
            'l2_cache': l2_stats,
            'strategy': self.strategy.value
        }
    
    def generate_cache_key(self, *args, **kwargs) -> str:
        """Genera clave de caché única."""
        # Combinar argumentos
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        
        # Crear hash
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def shutdown(self):
        """Cierra el sistema de caché."""
        self.is_cleanup_running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
        
        # Guardar índice de L2
        self.l2_cache._save_index()
        
        logger.info("Sistema de caché cerrado")


if __name__ == "__main__":
    # Test del AggressiveCache
    logging.basicConfig(level=logging.INFO)
    
    cache = AggressiveCache(
        l1_size_mb=100,  # 100MB para test
        l2_size_mb=500,  # 500MB para test
        strategy=CacheStrategy.ADAPTIVE
    )
    
    # Test de operaciones básicas
    test_data = {
        "query_1": "How to optimize Python code?",
        "query_2": "What is machine learning?",
        "embedding_1": np.random.randn(768),
        "computation_1": {"result": 42, "metadata": {"time": 1.5}},
        "metadata_1": {"version": "1.0", "timestamp": datetime.now().isoformat()}
    }
    
    # Establecer valores
    for key, value in test_data.items():
        cache_type = CacheType.QUERY_RESULT
        if "embedding" in key:
            cache_type = CacheType.EMBEDDING
        elif "computation" in key:
            cache_type = CacheType.COMPUTATION
        elif "metadata" in key:
            cache_type = CacheType.METADATA
        
        success = cache.set(key, value, cache_type)
        print(f"Set {key}: {'Success' if success else 'Failed'}")
    
    # Obtener valores
    for key in test_data.keys():
        value = cache.get(key)
        print(f"Get {key}: {'Found' if value is not None else 'Not found'}")
    
    # Test de generación de clave
    cache_key = cache.generate_cache_key("test_function", arg1="value1", arg2=42)
    print(f"Generated cache key: {cache_key}")
    
    # Mostrar estadísticas
    stats = cache.get_cache_stats()
    print(f"\nCache Statistics:")
    print(f"  Overall Hit Rate: {stats['overall']['overall_hit_rate']:.2%}")
    print(f"  L1 Hit Rate: {stats['overall']['l1_hit_rate']:.2%}")
    print(f"  L2 Hit Rate: {stats['overall']['l2_hit_rate']:.2%}")
    print(f"  Average Access Time: {stats['overall']['average_access_time_ms']:.2f}ms")
    print(f"  L1 Utilization: {stats['l1_cache']['utilization_percentage']:.1f}%")
    print(f"  L2 Utilization: {stats['l2_cache']['utilization_percentage']:.1f}%")
    
    # Cerrar caché
    cache.shutdown()
