#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TimescaleDB Manager - Gestión de métricas en TimescaleDB con compresión automática.
"""

import logging
import psycopg2
import psycopg2.extras
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import os

logger = logging.getLogger(__name__)


class TimescaleDBManager:
    """Gestiona la conexión y operaciones con TimescaleDB."""
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5432,
                 database: str = "capibara6_metrics",
                 username: str = "postgres",
                 password: str = "password",
                 ssl_mode: str = "prefer"):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.ssl_mode = ssl_mode
        
        self.connection = None
        self.is_connected = False
        
        # Configuración de compresión
        self.compression_policies = {
            'routing_metrics': 30,  # Comprimir después de 30 días
            'memory_metrics': 30,
            'compute_metrics': 30,
            'execution_metrics': 30,
            'agent_evolution_metrics': 30,
            'rag_metrics': 30,
            'system_metrics': 7  # Comprimir más rápido
        }
        
        # Estadísticas
        self.stats = {
            'total_connections': 0,
            'total_queries': 0,
            'total_inserts': 0,
            'total_compressions': 0,
            'connection_errors': 0,
            'query_errors': 0
        }
        
        logger.info(f"TimescaleDBManager inicializado: {host}:{port}/{database}")
    
    def connect(self) -> bool:
        """Conecta a TimescaleDB."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
                sslmode=self.ssl_mode
            )
            
            self.connection.autocommit = False
            self.is_connected = True
            self.stats['total_connections'] += 1
            
            # Verificar extensión TimescaleDB
            self._check_timescaledb_extension()
            
            # Inicializar esquemas
            self._initialize_schemas()
            
            logger.info("Conexión a TimescaleDB establecida exitosamente")
            return True
            
        except Exception as e:
            self.stats['connection_errors'] += 1
            logger.error(f"Error conectando a TimescaleDB: {e}")
            return False
    
    def disconnect(self):
        """Desconecta de TimescaleDB."""
        if self.connection:
            try:
                self.connection.close()
                self.is_connected = False
                logger.info("Desconectado de TimescaleDB")
            except Exception as e:
                logger.error(f"Error desconectando de TimescaleDB: {e}")
    
    def _check_timescaledb_extension(self):
        """Verifica que la extensión TimescaleDB esté instalada."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM pg_extension WHERE extname = 'timescaledb'")
                if not cursor.fetchone():
                    logger.warning("Extensión TimescaleDB no encontrada. Instalando...")
                    cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
                    self.connection.commit()
                    logger.info("Extensión TimescaleDB instalada")
        except Exception as e:
            logger.error(f"Error verificando extensión TimescaleDB: {e}")
    
    def _initialize_schemas(self):
        """Inicializa los esquemas de métricas."""
        try:
            with self.connection.cursor() as cursor:
                # Crear esquema de métricas
                cursor.execute("CREATE SCHEMA IF NOT EXISTS metrics")
                
                # Tabla de métricas de routing
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.routing_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        query_id TEXT,
                        query_text TEXT,
                        complexity_score REAL,
                        confidence_score REAL,
                        model_selected TEXT,
                        routing_time_ms INTEGER,
                        embedding_time_ms INTEGER,
                        threshold_comparison_time_ms INTEGER,
                        total_routing_time_ms INTEGER,
                        tokens_estimated INTEGER,
                        context_length INTEGER,
                        user_intent TEXT,
                        domain_detected TEXT,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas de memoria
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.memory_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        agent_id TEXT,
                        memory_type TEXT,
                        memory_operation TEXT,
                        memory_size_bytes BIGINT,
                        memory_tokens INTEGER,
                        operation_time_ms INTEGER,
                        cache_hit BOOLEAN,
                        compression_ratio REAL,
                        importance_score REAL,
                        access_count INTEGER,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas de cómputo
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.compute_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        model_id TEXT,
                        operation_type TEXT,
                        batch_size INTEGER,
                        sequence_length INTEGER,
                        tokens_processed BIGINT,
                        computation_time_ms INTEGER,
                        gpu_utilization_percent REAL,
                        gpu_memory_used_mb REAL,
                        cpu_utilization_percent REAL,
                        cpu_memory_used_mb REAL,
                        throughput_tokens_per_sec REAL,
                        latency_p50_ms REAL,
                        latency_p95_ms REAL,
                        latency_p99_ms REAL,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas de ejecución
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.execution_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        execution_id TEXT,
                        agent_id TEXT,
                        language TEXT,
                        code_length INTEGER,
                        execution_time_ms INTEGER,
                        memory_used_mb REAL,
                        cpu_used_percent REAL,
                        success BOOLEAN,
                        error_type TEXT,
                        corrections_applied INTEGER,
                        sandbox_id TEXT,
                        timeout_occurred BOOLEAN,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas de evolución de agentes
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.agent_evolution_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        agent_id TEXT,
                        domain TEXT,
                        evolution_event TEXT,
                        interactions_count INTEGER,
                        success_rate REAL,
                        graduation_score REAL,
                        memory_utilization REAL,
                        domain_expertise REAL,
                        collaboration_count INTEGER,
                        playbook_contributions INTEGER,
                        learning_rate REAL,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas de RAG
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.rag_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        query_id TEXT,
                        rag_type TEXT,
                        query_text TEXT,
                        retrieval_time_ms INTEGER,
                        documents_retrieved INTEGER,
                        documents_relevant INTEGER,
                        relevance_score REAL,
                        context_length INTEGER,
                        context_tokens INTEGER,
                        search_strategy TEXT,
                        vector_search_time_ms INTEGER,
                        reranking_time_ms INTEGER,
                        total_rag_time_ms INTEGER,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Tabla de métricas del sistema
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metrics.system_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        system_id TEXT,
                        cpu_usage_percent REAL,
                        memory_usage_percent REAL,
                        disk_usage_percent REAL,
                        network_io_bytes BIGINT,
                        active_connections INTEGER,
                        active_agents INTEGER,
                        total_requests BIGINT,
                        error_rate REAL,
                        response_time_avg_ms REAL,
                        throughput_requests_per_sec REAL,
                        tags JSONB,
                        metadata JSONB
                    )
                """)
                
                # Convertir tablas a hypertables
                self._create_hypertables()
                
                # Configurar políticas de compresión
                self._setup_compression_policies()
                
                self.connection.commit()
                logger.info("Esquemas de métricas inicializados")
                
        except Exception as e:
            logger.error(f"Error inicializando esquemas: {e}")
            if self.connection:
                self.connection.rollback()
    
    def _create_hypertables(self):
        """Convierte tablas a hypertables de TimescaleDB."""
        try:
            with self.connection.cursor() as cursor:
                tables = [
                    'routing_metrics', 'memory_metrics', 'compute_metrics',
                    'execution_metrics', 'agent_evolution_metrics', 'rag_metrics', 'system_metrics'
                ]
                
                for table in tables:
                    # Verificar si ya es hypertable
                    cursor.execute("""
                        SELECT * FROM timescaledb_information.hypertables 
                        WHERE hypertable_name = %s AND hypertable_schema = 'metrics'
                    """, (table,))
                    
                    if not cursor.fetchone():
                        cursor.execute(f"SELECT create_hypertable('metrics.{table}', 'time')")
                        logger.info(f"Hypertable creada: metrics.{table}")
                    else:
                        logger.debug(f"Hypertable ya existe: metrics.{table}")
                        
        except Exception as e:
            logger.error(f"Error creando hypertables: {e}")
    
    def _setup_compression_policies(self):
        """Configura políticas de compresión automática."""
        try:
            with self.connection.cursor() as cursor:
                for table, days in self.compression_policies.items():
                    # Verificar si ya existe política de compresión
                    cursor.execute("""
                        SELECT * FROM timescaledb_information.jobs 
                        WHERE hypertable_name = %s AND hypertable_schema = 'metrics'
                        AND proc_name = 'policy_compression'
                    """, (table,))
                    
                    if not cursor.fetchone():
                        # Habilitar compresión
                        cursor.execute(f"ALTER TABLE metrics.{table} SET (timescaledb.compress, timescaledb.compress_segmentby = 'time')")
                        
                        # Agregar política de compresión
                        cursor.execute(f"""
                            SELECT add_compression_policy('metrics.{table}', INTERVAL '{days} days')
                        """)
                        
                        logger.info(f"Política de compresión configurada para metrics.{table}: {days} días")
                    else:
                        logger.debug(f"Política de compresión ya existe para metrics.{table}")
                        
        except Exception as e:
            logger.error(f"Error configurando políticas de compresión: {e}")
    
    def insert_routing_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de routing."""
        return self._insert_metrics('routing_metrics', metrics_data)
    
    def insert_memory_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de memoria."""
        return self._insert_metrics('memory_metrics', metrics_data)
    
    def insert_compute_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de cómputo."""
        return self._insert_metrics('compute_metrics', metrics_data)
    
    def insert_execution_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de ejecución."""
        return self._insert_metrics('execution_metrics', metrics_data)
    
    def insert_agent_evolution_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de evolución de agentes."""
        return self._insert_metrics('agent_evolution_metrics', metrics_data)
    
    def insert_rag_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas de RAG."""
        return self._insert_metrics('rag_metrics', metrics_data)
    
    def insert_system_metrics(self, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas del sistema."""
        return self._insert_metrics('system_metrics', metrics_data)
    
    def _insert_metrics(self, table_name: str, metrics_data: List[Dict[str, Any]]) -> bool:
        """Inserta métricas en una tabla específica."""
        if not self.is_connected or not metrics_data:
            return False
        
        try:
            with self.connection.cursor() as cursor:
                # Preparar datos para inserción
                insert_data = []
                for metric in metrics_data:
                    # Asegurar que 'time' esté presente
                    if 'time' not in metric:
                        metric['time'] = datetime.now()
                    
                    # Convertir datetime a string si es necesario
                    if isinstance(metric['time'], datetime):
                        metric['time'] = metric['time'].isoformat()
                    
                    insert_data.append(metric)
                
                # Construir query de inserción
                columns = list(insert_data[0].keys())
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                
                query = f"""
                    INSERT INTO metrics.{table_name} ({columns_str})
                    VALUES ({placeholders})
                """
                
                # Ejecutar inserción
                cursor.executemany(query, [tuple(metric[col] for col in columns) for metric in insert_data])
                self.connection.commit()
                
                self.stats['total_inserts'] += len(insert_data)
                self.stats['total_queries'] += 1
                
                logger.debug(f"Insertadas {len(insert_data)} métricas en metrics.{table_name}")
                return True
                
        except Exception as e:
            self.stats['query_errors'] += 1
            logger.error(f"Error insertando métricas en {table_name}: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def query_metrics(self, 
                     table_name: str,
                     start_time: datetime,
                     end_time: datetime,
                     filters: Dict[str, Any] = None,
                     limit: int = 1000) -> List[Dict[str, Any]]:
        """Consulta métricas de una tabla específica."""
        if not self.is_connected:
            return []
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Construir query
                query = f"SELECT * FROM metrics.{table_name} WHERE time >= %s AND time <= %s"
                params = [start_time, end_time]
                
                # Agregar filtros
                if filters:
                    for key, value in filters.items():
                        if isinstance(value, str):
                            query += f" AND {key} = %s"
                            params.append(value)
                        elif isinstance(value, (int, float)):
                            query += f" AND {key} = %s"
                            params.append(value)
                        elif isinstance(value, list):
                            placeholders = ', '.join(['%s'] * len(value))
                            query += f" AND {key} IN ({placeholders})"
                            params.extend(value)
                
                query += f" ORDER BY time DESC LIMIT {limit}"
                
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                self.stats['total_queries'] += 1
                
                # Convertir a lista de diccionarios
                return [dict(row) for row in results]
                
        except Exception as e:
            self.stats['query_errors'] += 1
            logger.error(f"Error consultando métricas de {table_name}: {e}")
            return []
    
    def get_aggregated_metrics(self,
                             table_name: str,
                             start_time: datetime,
                             end_time: datetime,
                             group_by: str = "1 hour",
                             aggregation: str = "avg") -> List[Dict[str, Any]]:
        """Obtiene métricas agregadas."""
        if not self.is_connected:
            return []
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Construir query de agregación
                query = f"""
                    SELECT 
                        time_bucket(INTERVAL '{group_by}', time) as bucket,
                        {aggregation}(*.*) as aggregated_data
                    FROM metrics.{table_name}
                    WHERE time >= %s AND time <= %s
                    GROUP BY bucket
                    ORDER BY bucket DESC
                """
                
                cursor.execute(query, [start_time, end_time])
                results = cursor.fetchall()
                
                self.stats['total_queries'] += 1
                
                return [dict(row) for row in results]
                
        except Exception as e:
            self.stats['query_errors'] += 1
            logger.error(f"Error obteniendo métricas agregadas de {table_name}: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la base de datos."""
        if not self.is_connected:
            return {}
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                stats = {}
                
                # Estadísticas de tablas
                tables = ['routing_metrics', 'memory_metrics', 'compute_metrics', 
                         'execution_metrics', 'agent_evolution_metrics', 'rag_metrics', 'system_metrics']
                
                for table in tables:
                    cursor.execute(f"""
                        SELECT 
                            COUNT(*) as total_rows,
                            MIN(time) as earliest_time,
                            MAX(time) as latest_time
                        FROM metrics.{table}
                    """)
                    
                    result = cursor.fetchone()
                    if result:
                        stats[table] = dict(result)
                
                # Estadísticas de compresión
                cursor.execute("""
                    SELECT 
                        hypertable_name,
                        compressed_bytes,
                        uncompressed_bytes,
                        compression_ratio
                    FROM timescaledb_information.compression_stats
                    WHERE hypertable_schema = 'metrics'
                """)
                
                compression_stats = cursor.fetchall()
                stats['compression'] = [dict(row) for row in compression_stats]
                
                # Estadísticas de jobs
                cursor.execute("""
                    SELECT 
                        hypertable_name,
                        job_id,
                        last_run_started_at,
                        last_successful_finish,
                        next_start
                    FROM timescaledb_information.jobs
                    WHERE hypertable_schema = 'metrics'
                """)
                
                job_stats = cursor.fetchall()
                stats['jobs'] = [dict(row) for row in job_stats]
                
                return stats
                
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de la base de datos: {e}")
            return {}
    
    def get_manager_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del manager."""
        return self.stats.copy()
    
    def cleanup_old_data(self, days_to_keep: int = 90) -> bool:
        """Limpia datos antiguos."""
        if not self.is_connected:
            return False
        
        try:
            with self.connection.cursor() as cursor:
                cutoff_date = datetime.now() - timedelta(days=days_to_keep)
                
                tables = ['routing_metrics', 'memory_metrics', 'compute_metrics',
                         'execution_metrics', 'agent_evolution_metrics', 'rag_metrics', 'system_metrics']
                
                total_deleted = 0
                for table in tables:
                    cursor.execute(f"DELETE FROM metrics.{table} WHERE time < %s", (cutoff_date,))
                    deleted = cursor.rowcount
                    total_deleted += deleted
                    logger.info(f"Eliminados {deleted} registros antiguos de metrics.{table}")
                
                self.connection.commit()
                logger.info(f"Limpieza completada: {total_deleted} registros eliminados")
                return True
                
        except Exception as e:
            logger.error(f"Error en limpieza de datos: {e}")
            if self.connection:
                self.connection.rollback()
            return False


if __name__ == "__main__":
    # Test del TimescaleDBManager
    logging.basicConfig(level=logging.INFO)
    
    # Configuración de prueba (ajustar según tu setup)
    manager = TimescaleDBManager(
        host="localhost",
        port=5432,
        database="capibara6_metrics",
        username="postgres",
        password="password"
    )
    
    # Conectar
    if manager.connect():
        print("Conectado a TimescaleDB exitosamente")
        
        # Test de inserción de métricas
        test_metrics = [
            {
                'time': datetime.now(),
                'query_id': 'test_001',
                'complexity_score': 0.8,
                'confidence_score': 0.9,
                'model_selected': '120B',
                'routing_time_ms': 50,
                'tags': {'test': 'true'},
                'metadata': {'source': 'test'}
            }
        ]
        
        success = manager.insert_routing_metrics(test_metrics)
        print(f"Inserción de métricas: {'exitosa' if success else 'fallida'}")
        
        # Test de consulta
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        
        results = manager.query_metrics('routing_metrics', start_time, end_time)
        print(f"Consulta de métricas: {len(results)} resultados")
        
        # Mostrar estadísticas
        db_stats = manager.get_database_stats()
        print(f"Estadísticas de BD: {db_stats}")
        
        manager_stats = manager.get_manager_stats()
        print(f"Estadísticas del manager: {manager_stats}")
        
        # Desconectar
        manager.disconnect()
    else:
        print("Error conectando a TimescaleDB")
