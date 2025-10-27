#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging System - Sistema de logging centralizado para Capibara6.
"""

import logging
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import os
import sys

logger = logging.getLogger(__name__)

class LogLevel(Enum):
    """Niveles de log."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Categorías de log."""
    SYSTEM = "system"
    API = "api"
    ROUTING = "routing"
    ACE = "ace"
    E2B = "e2b"
    RAG = "rag"
    AGENTS = "agents"
    OPTIMIZATIONS = "optimizations"
    BUSINESS = "business"
    SECURITY = "security"
    PERFORMANCE = "performance"

@dataclass
class LogEntry:
    """Entrada de log estructurada."""
    timestamp: datetime
    level: LogLevel
    category: LogCategory
    message: str
    component: str
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    duration_ms: Optional[float] = None
    error_code: Optional[str] = None
    stack_trace: Optional[str] = None

class StructuredLogger:
    """Logger estructurado para Capibara6."""
    
    def __init__(self, name: str, category: LogCategory = LogCategory.SYSTEM):
        self.name = name
        self.category = category
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger."""
        if not self.logger.handlers:
            # Handler para consola
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Formatter estructurado
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        """Método interno de logging."""
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            category=self.category,
            message=message,
            component=self.name,
            **kwargs
        )
        
        # Log estructurado
        structured_message = self._format_structured_log(log_entry)
        
        # Log tradicional
        if level == LogLevel.DEBUG:
            self.logger.debug(structured_message)
        elif level == LogLevel.INFO:
            self.logger.info(structured_message)
        elif level == LogLevel.WARNING:
            self.logger.warning(structured_message)
        elif level == LogLevel.ERROR:
            self.logger.error(structured_message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(structured_message)
        
        # Enviar a sistema centralizado
        CentralizedLoggingSystem.get_instance().add_log_entry(log_entry)
    
    def _format_structured_log(self, log_entry: LogEntry) -> str:
        """Formatea el log de manera estructurada."""
        base_info = f"[{log_entry.category.value}] {log_entry.message}"
        
        if log_entry.user_id:
            base_info += f" | User: {log_entry.user_id}"
        
        if log_entry.request_id:
            base_info += f" | Request: {log_entry.request_id}"
        
        if log_entry.duration_ms:
            base_info += f" | Duration: {log_entry.duration_ms:.2f}ms"
        
        if log_entry.error_code:
            base_info += f" | Error: {log_entry.error_code}"
        
        if log_entry.metadata:
            base_info += f" | Metadata: {json.dumps(log_entry.metadata)}"
        
        return base_info
    
    def debug(self, message: str, **kwargs):
        """Log de debug."""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log de info."""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de warning."""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de error."""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log crítico."""
        self._log(LogLevel.CRITICAL, message, **kwargs)

class CentralizedLoggingSystem:
    """Sistema de logging centralizado."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.log_entries: List[LogEntry] = []
        self.max_entries = 10000
        self.log_buffer: List[LogEntry] = []
        self.buffer_size = 100
        self.flush_interval = 30  # segundos
        
        # Iniciar thread de flush
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()
        
        logger.info("CentralizedLoggingSystem inicializado")
    
    @classmethod
    def get_instance(cls):
        """Obtiene la instancia singleton."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def add_log_entry(self, log_entry: LogEntry):
        """Añade una entrada de log."""
        with self._lock:
            self.log_buffer.append(log_entry)
            
            # Flush si el buffer está lleno
            if len(self.log_buffer) >= self.buffer_size:
                self._flush_buffer()
    
    def _flush_buffer(self):
        """Flush del buffer de logs."""
        if not self.log_buffer:
            return
        
        # Añadir al almacenamiento principal
        self.log_entries.extend(self.log_buffer)
        
        # Mantener límite de entradas
        if len(self.log_entries) > self.max_entries:
            self.log_entries = self.log_entries[-self.max_entries:]
        
        # Limpiar buffer
        self.log_buffer.clear()
    
    def _flush_loop(self):
        """Loop de flush periódico."""
        while True:
            try:
                time.sleep(self.flush_interval)
                with self._lock:
                    self._flush_buffer()
            except Exception as e:
                logger.error(f"Error en flush loop: {e}")
    
    def get_logs(self, 
                 level: Optional[LogLevel] = None,
                 category: Optional[LogCategory] = None,
                 component: Optional[str] = None,
                 user_id: Optional[str] = None,
                 start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None,
                 limit: int = 1000) -> List[LogEntry]:
        """Obtiene logs con filtros."""
        with self._lock:
            logs = self.log_entries.copy()
        
        # Aplicar filtros
        if level:
            logs = [log for log in logs if log.level == level]
        
        if category:
            logs = [log for log in logs if log.category == category]
        
        if component:
            logs = [log for log in logs if log.component == component]
        
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        
        if start_time:
            logs = [log for log in logs if log.timestamp >= start_time]
        
        if end_time:
            logs = [log for log in logs if log.timestamp <= end_time]
        
        # Ordenar por timestamp (más recientes primero)
        logs.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Limitar resultados
        return logs[:limit]
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de logs."""
        with self._lock:
            logs = self.log_entries.copy()
        
        if not logs:
            return {
                "total_logs": 0,
                "level_distribution": {},
                "category_distribution": {},
                "component_distribution": {},
                "error_rate": 0.0,
                "time_range": None
            }
        
        # Distribución por nivel
        level_distribution = {}
        for log in logs:
            level = log.level.value
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        # Distribución por categoría
        category_distribution = {}
        for log in logs:
            category = log.category.value
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        # Distribución por componente
        component_distribution = {}
        for log in logs:
            component = log.component
            component_distribution[component] = component_distribution.get(component, 0) + 1
        
        # Tasa de errores
        error_logs = [log for log in logs if log.level in [LogLevel.ERROR, LogLevel.CRITICAL]]
        error_rate = len(error_logs) / len(logs) * 100 if logs else 0.0
        
        # Rango de tiempo
        timestamps = [log.timestamp for log in logs]
        time_range = {
            "start": min(timestamps).isoformat(),
            "end": max(timestamps).isoformat()
        }
        
        return {
            "total_logs": len(logs),
            "level_distribution": level_distribution,
            "category_distribution": category_distribution,
            "component_distribution": component_distribution,
            "error_rate": error_rate,
            "time_range": time_range
        }
    
    def export_logs(self, 
                   output_file: str,
                   format: str = "json",
                   **filters) -> bool:
        """Exporta logs a archivo."""
        try:
            logs = self.get_logs(**filters)
            
            if format == "json":
                with open(output_file, 'w') as f:
                    json.dump([asdict(log) for log in logs], f, indent=2, default=str)
            elif format == "csv":
                import csv
                with open(output_file, 'w', newline='') as f:
                    if logs:
                        writer = csv.DictWriter(f, fieldnames=asdict(logs[0]).keys())
                        writer.writeheader()
                        for log in logs:
                            writer.writerow(asdict(log))
            else:
                logger.error(f"Formato no soportado: {format}")
                return False
            
            logger.info(f"Logs exportados a {output_file}: {len(logs)} entradas")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando logs: {e}")
            return False
    
    def clear_logs(self):
        """Limpia todos los logs."""
        with self._lock:
            self.log_entries.clear()
            self.log_buffer.clear()
        
        logger.info("Logs limpiados")

class LoggingMiddleware:
    """Middleware de logging para FastAPI."""
    
    def __init__(self, app, logger_name: str = "api"):
        self.app = app
        self.logger = StructuredLogger(logger_name, LogCategory.API)
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extraer información de la request
            request_info = {
                "method": scope["method"],
                "path": scope["path"],
                "query_string": scope["query_string"].decode(),
                "headers": dict(scope["headers"])
            }
            
            start_time = time.time()
            
            # Log de inicio de request
            self.logger.info(
                f"Request iniciada: {request_info['method']} {request_info['path']}",
                metadata=request_info
            )
            
            # Procesar request
            await self.app(scope, receive, send)
            
            # Log de fin de request
            duration_ms = (time.time() - start_time) * 1000
            self.logger.info(
                f"Request completada: {request_info['method']} {request_info['path']}",
                duration_ms=duration_ms,
                metadata=request_info
            )
        else:
            await self.app(scope, receive, send)

# Funciones de utilidad
def get_logger(name: str, category: LogCategory = LogCategory.SYSTEM) -> StructuredLogger:
    """Obtiene un logger estructurado."""
    return StructuredLogger(name, category)

def get_centralized_logging() -> CentralizedLoggingSystem:
    """Obtiene el sistema de logging centralizado."""
    return CentralizedLoggingSystem.get_instance()

# Loggers específicos por componente
def get_system_logger() -> StructuredLogger:
    """Logger para el sistema."""
    return get_logger("system", LogCategory.SYSTEM)

def get_api_logger() -> StructuredLogger:
    """Logger para la API."""
    return get_logger("api", LogCategory.API)

def get_routing_logger() -> StructuredLogger:
    """Logger para routing."""
    return get_logger("routing", LogCategory.ROUTING)

def get_ace_logger() -> StructuredLogger:
    """Logger para ACE."""
    return get_logger("ace", LogCategory.ACE)

def get_e2b_logger() -> StructuredLogger:
    """Logger para E2B."""
    return get_logger("e2b", LogCategory.E2B)

def get_rag_logger() -> StructuredLogger:
    """Logger para RAG."""
    return get_logger("rag", LogCategory.RAG)

def get_agents_logger() -> StructuredLogger:
    """Logger para agentes."""
    return get_logger("agents", LogCategory.AGENTS)

def get_optimizations_logger() -> StructuredLogger:
    """Logger para optimizaciones."""
    return get_logger("optimizations", LogCategory.OPTIMIZATIONS)

def get_business_logger() -> StructuredLogger:
    """Logger para negocio."""
    return get_logger("business", LogCategory.BUSINESS)

def get_security_logger() -> StructuredLogger:
    """Logger para seguridad."""
    return get_logger("security", LogCategory.SECURITY)

def get_performance_logger() -> StructuredLogger:
    """Logger para rendimiento."""
    return get_logger("performance", LogCategory.PERFORMANCE)

if __name__ == "__main__":
    # Test del sistema de logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear loggers
    system_logger = get_system_logger()
    api_logger = get_api_logger()
    routing_logger = get_routing_logger()
    
    # Logs de prueba
    system_logger.info("Sistema iniciado correctamente")
    api_logger.info("API request procesada", user_id="user_123", request_id="req_456", duration_ms=150.5)
    routing_logger.warning("Routing con baja confianza", confidence=0.3, model_selected="capibara6-20b")
    
    # Obtener estadísticas
    centralized = get_centralized_logging()
    stats = centralized.get_log_statistics()
    
    print("Estadísticas de logging:")
    print(json.dumps(stats, indent=2, default=str))
    
    # Exportar logs
    centralized.export_logs("test_logs.json", format="json")
    
    print("Sistema de logging centralizado funcionando correctamente!")
