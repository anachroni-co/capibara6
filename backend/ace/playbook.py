#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estructura de playbooks para el ACE Framework.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PlaybookPattern:
    """Representa un patrón en un playbook."""
    
    def __init__(self, 
                 query_pattern: str,
                 context_template: str,
                 helpful_count: int = 0,
                 harmful_count: int = 0,
                 pattern_id: Optional[str] = None):
        self.id = pattern_id or str(uuid.uuid4())
        self.query_pattern = query_pattern
        self.context_template = context_template
        self.helpful_count = helpful_count
        self.harmful_count = harmful_count
        self.last_updated = datetime.now().isoformat()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el patrón a diccionario."""
        return {
            'id': self.id,
            'query_pattern': self.query_pattern,
            'context_template': self.context_template,
            'helpful_count': self.helpful_count,
            'harmful_count': self.harmful_count,
            'last_updated': self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlaybookPattern':
        """Crea un patrón desde diccionario."""
        pattern = cls(
            query_pattern=data['query_pattern'],
            context_template=data['context_template'],
            helpful_count=data.get('helpful_count', 0),
            harmful_count=data.get('harmful_count', 0),
            pattern_id=data.get('id')
        )
        pattern.last_updated = data.get('last_updated', datetime.now().isoformat())
        return pattern
    
    def add_feedback(self, is_helpful: bool):
        """Agrega feedback al patrón."""
        if is_helpful:
            self.helpful_count += 1
        else:
            self.harmful_count += 1
        self.last_updated = datetime.now().isoformat()
        logger.debug(f"Feedback agregado al patrón {self.id}: helpful={is_helpful}")
    
    def get_success_rate(self) -> float:
        """Calcula la tasa de éxito del patrón."""
        total = self.helpful_count + self.harmful_count
        if total == 0:
            return 0.0
        return self.helpful_count / total
    
    def is_valuable(self, threshold: float = 0.5) -> bool:
        """Determina si el patrón es valioso basado en su tasa de éxito."""
        return self.get_success_rate() >= threshold


class Playbook:
    """Representa un playbook completo con patrones y metadata."""
    
    def __init__(self, 
                 domain: str = "general",
                 version: str = "1.0",
                 playbook_id: Optional[str] = None):
        self.id = playbook_id or str(uuid.uuid4())
        self.version = version
        self.domain = domain
        self.patterns: List[PlaybookPattern] = []
        self.successful_responses: List[Dict[str, Any]] = []
        self.failed_responses: List[Dict[str, Any]] = []
        self.metadata = {
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_interactions': 0,
            'success_rate': 0.0
        }
        
    def add_pattern(self, pattern: PlaybookPattern):
        """Agrega un patrón al playbook."""
        self.patterns.append(pattern)
        self.metadata['last_updated'] = datetime.now().isoformat()
        logger.info(f"Patrón agregado al playbook {self.id}: {pattern.id}")
    
    def find_matching_patterns(self, query: str, max_patterns: int = 5) -> List[PlaybookPattern]:
        """Encuentra patrones que coincidan con la query."""
        # Implementación simple: búsqueda por palabras clave
        # En una implementación real, usaríamos embeddings o regex más sofisticados
        query_lower = query.lower()
        matching_patterns = []
        
        for pattern in self.patterns:
            # Buscar coincidencias en el patrón de query
            if any(word in query_lower for word in pattern.query_pattern.lower().split()):
                matching_patterns.append(pattern)
        
        # Ordenar por tasa de éxito y devolver los mejores
        matching_patterns.sort(key=lambda p: p.get_success_rate(), reverse=True)
        return matching_patterns[:max_patterns]
    
    def add_successful_response(self, query: str, response: str, context_used: str):
        """Agrega una respuesta exitosa."""
        self.successful_responses.append({
            'query': query,
            'response': response,
            'context_used': context_used,
            'timestamp': datetime.now().isoformat()
        })
        self._update_metadata()
        logger.debug(f"Respuesta exitosa agregada al playbook {self.id}")
    
    def add_failed_response(self, query: str, response: str, error: str):
        """Agrega una respuesta fallida."""
        self.failed_responses.append({
            'query': query,
            'response': response,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self._update_metadata()
        logger.debug(f"Respuesta fallida agregada al playbook {self.id}")
    
    def _update_metadata(self):
        """Actualiza los metadatos del playbook."""
        total_interactions = len(self.successful_responses) + len(self.failed_responses)
        success_rate = 0.0
        
        if total_interactions > 0:
            success_rate = len(self.successful_responses) / total_interactions
        
        self.metadata.update({
            'last_updated': datetime.now().isoformat(),
            'total_interactions': total_interactions,
            'success_rate': success_rate
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del playbook."""
        pattern_stats = {
            'total_patterns': len(self.patterns),
            'valuable_patterns': sum(1 for p in self.patterns if p.is_valuable()),
            'avg_success_rate': sum(p.get_success_rate() for p in self.patterns) / len(self.patterns) if self.patterns else 0.0
        }
        
        return {
            'playbook_id': self.id,
            'domain': self.domain,
            'version': self.version,
            'patterns': pattern_stats,
            'interactions': {
                'total': self.metadata['total_interactions'],
                'successful': len(self.successful_responses),
                'failed': len(self.failed_responses),
                'success_rate': self.metadata['success_rate']
            },
            'last_updated': self.metadata['last_updated']
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el playbook a diccionario."""
        return {
            'id': self.id,
            'version': self.version,
            'domain': self.domain,
            'patterns': [pattern.to_dict() for pattern in self.patterns],
            'successful_responses': self.successful_responses,
            'failed_responses': self.failed_responses,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Playbook':
        """Crea un playbook desde diccionario."""
        playbook = cls(
            domain=data.get('domain', 'general'),
            version=data.get('version', '1.0'),
            playbook_id=data.get('id')
        )
        
        # Cargar patrones
        for pattern_data in data.get('patterns', []):
            pattern = PlaybookPattern.from_dict(pattern_data)
            playbook.patterns.append(pattern)
        
        # Cargar respuestas
        playbook.successful_responses = data.get('successful_responses', [])
        playbook.failed_responses = data.get('failed_responses', [])
        playbook.metadata = data.get('metadata', {})
        
        return playbook
    
    def save_to_file(self, filepath: str):
        """Guarda el playbook a un archivo JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"Playbook guardado en {filepath}")
        except Exception as e:
            logger.error(f"Error guardando playbook en {filepath}: {e}")
            raise
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Playbook':
        """Carga un playbook desde un archivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            playbook = cls.from_dict(data)
            logger.info(f"Playbook cargado desde {filepath}")
            return playbook
        except FileNotFoundError:
            logger.warning(f"Archivo de playbook no encontrado: {filepath}")
            # Crear playbook vacío
            return cls()
        except Exception as e:
            logger.error(f"Error cargando playbook desde {filepath}: {e}")
            raise


class PlaybookManager:
    """Gestiona múltiples playbooks."""
    
    def __init__(self, playbooks_dir: str = "backend/data/playbooks"):
        self.playbooks_dir = playbooks_dir
        self.playbooks: Dict[str, Playbook] = {}
        self._ensure_directory()
        self._load_all_playbooks()
    
    def _ensure_directory(self):
        """Asegura que el directorio de playbooks existe."""
        import os
        os.makedirs(self.playbooks_dir, exist_ok=True)
    
    def _load_all_playbooks(self):
        """Carga todos los playbooks del directorio."""
        import os
        import glob
        
        pattern = os.path.join(self.playbooks_dir, "*.json")
        for filepath in glob.glob(pattern):
            try:
                playbook = Playbook.load_from_file(filepath)
                self.playbooks[playbook.id] = playbook
                logger.info(f"Playbook cargado: {playbook.domain} ({playbook.id})")
            except Exception as e:
                logger.error(f"Error cargando playbook {filepath}: {e}")
    
    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        """Obtiene un playbook por ID."""
        return self.playbooks.get(playbook_id)
    
    def get_playbook_by_domain(self, domain: str) -> Optional[Playbook]:
        """Obtiene un playbook por dominio."""
        for playbook in self.playbooks.values():
            if playbook.domain == domain:
                return playbook
        return None
    
    def create_playbook(self, domain: str) -> Playbook:
        """Crea un nuevo playbook."""
        playbook = Playbook(domain=domain)
        self.playbooks[playbook.id] = playbook
        logger.info(f"Nuevo playbook creado: {domain} ({playbook.id})")
        return playbook
    
    def save_playbook(self, playbook: Playbook):
        """Guarda un playbook."""
        filepath = f"{self.playbooks_dir}/playbook_{playbook.id}.json"
        playbook.save_to_file(filepath)
        self.playbooks[playbook.id] = playbook
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de todos los playbooks."""
        stats = {
            'total_playbooks': len(self.playbooks),
            'domains': list(set(pb.domain for pb in self.playbooks.values())),
            'total_patterns': sum(len(pb.patterns) for pb in self.playbooks.values()),
            'total_interactions': sum(pb.metadata.get('total_interactions', 0) for pb in self.playbooks.values()),
            'playbooks': [pb.get_stats() for pb in self.playbooks.values()]
        }
        return stats


if __name__ == "__main__":
    # Test del sistema de playbooks
    logging.basicConfig(level=logging.INFO)
    
    # Crear manager
    manager = PlaybookManager()
    
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
    
    # Agregar respuestas
    playbook.add_successful_response(
        "How to create a Python function?",
        "Use the 'def' keyword followed by the function name...",
        "Python function context"
    )
    
    # Guardar
    manager.save_playbook(playbook)
    
    # Mostrar stats
    stats = manager.get_all_stats()
    print(f"Stats: {json.dumps(stats, indent=2)}")
