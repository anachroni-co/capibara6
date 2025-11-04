#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metrics Pipeline - Pipeline de agregación diaria, métricas derivadas y detección de anomalías.
"""

import logging
import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import os

from .timescaledb_manager import TimescaleDBManager

logger = logging.getLogger(__name__)


@dataclass
class AggregatedMetric:
    """Métrica agregada."""
    metric_name: str
    metric_type: str
    aggregation_type: str  # avg, sum, min, max, count, p50, p95, p99
    value: float
    timestamp: datetime
    time_bucket: str  # 1h, 1d, 1w
    tags: Dict[str, str]
    metadata: Dict[str, Any]


@dataclass
class AnomalyDetection:
    """Detección de anomalías."""
    metric_name: str
    metric_type: str
    anomaly_type: str  # spike, drop, trend_change, outlier
    severity: str  # low, medium, high, critical
    current_value: float
    expected_value: float
    deviation_percent: float
    confidence: float
    timestamp: datetime
    description: str
    recommendations: List[str]


@dataclass
class DerivedMetric:
    """Métrica derivada."""
    metric_name: str
    source_metrics: List[str]
    calculation: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    metadata: Dict[str, Any]


class MetricsAggregator:
    """Agregador de métricas diarias."""
    
    def __init__(self, timescaledb_manager: TimescaleDBManager):
        self.timescaledb_manager = timescaledb_manager
        self.aggregation_configs = self._initialize_aggregation_configs()
        
        self.aggregator_stats = {
            'total_aggregations': 0,
            'successful_aggregations': 0,
            'failed_aggregations': 0,
            'anomalies_detected': 0,
            'derived_metrics_calculated': 0
        }
        
        logger.info("MetricsAggregator inicializado")
    
    def _initialize_aggregation_configs(self) -> Dict[str, Dict[str, Any]]:
        """Inicializa configuraciones de agregación."""
        return {
            'routing_metrics': {
                'aggregations': ['avg', 'p95', 'p99', 'count'],
                'group_by': ['model_selected', 'domain_detected'],
                'time_buckets': ['1 hour', '1 day'],
                'metrics': ['routing_time_ms', 'complexity_score', 'confidence_score']
            },
            'memory_metrics': {
                'aggregations': ['avg', 'sum', 'max', 'count'],
                'group_by': ['agent_id', 'memory_type', 'memory_operation'],
                'time_buckets': ['1 hour', '1 day'],
                'metrics': ['operation_time_ms', 'memory_size_bytes', 'memory_tokens', 'compression_ratio']
            },
            'compute_metrics': {
                'aggregations': ['avg', 'p95', 'p99', 'max'],
                'group_by': ['model_id', 'operation_type'],
                'time_buckets': ['1 hour', '1 day'],
                'metrics': ['computation_time_ms', 'gpu_utilization_percent', 'throughput_tokens_per_sec', 'latency_p95_ms']
            },
            'execution_metrics': {
                'aggregations': ['avg', 'p95', 'p99', 'count'],
                'group_by': ['agent_id', 'language', 'success'],
                'time_buckets': ['1 hour', '1 day'],
                'metrics': ['execution_time_ms', 'memory_used_mb', 'cpu_used_percent']
            },
            'rag_metrics': {
                'aggregations': ['avg', 'p95', 'p99', 'count'],
                'group_by': ['rag_type', 'search_strategy'],
                'time_buckets': ['1 hour', '1 day'],
                'metrics': ['retrieval_time_ms', 'documents_retrieved', 'relevance_score', 'total_rag_time_ms']
            },
            'system_metrics': {
                'aggregations': ['avg', 'max', 'min'],
                'group_by': ['system_id'],
                'time_buckets': ['5 minutes', '1 hour', '1 day'],
                'metrics': ['cpu_usage_percent', 'memory_usage_percent', 'active_agents', 'error_rate']
            }
        }
    
    async def run_daily_aggregation(self, target_date: Optional[datetime] = None) -> bool:
        """Ejecuta agregación diaria de métricas."""
        if not target_date:
            target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        start_time = target_date
        end_time = target_date + timedelta(days=1)
        
        logger.info(f"Iniciando agregación diaria para {target_date.date()}")
        
        try:
            # Agregar métricas por tabla
            for table_name, config in self.aggregation_configs.items():
                await self._aggregate_table_metrics(table_name, config, start_time, end_time)
            
            # Calcular métricas derivadas
            await self._calculate_derived_metrics(start_time, end_time)
            
            # Detectar anomalías
            await self._detect_anomalies(start_time, end_time)
            
            self.aggregator_stats['successful_aggregations'] += 1
            logger.info(f"Agregación diaria completada para {target_date.date()}")
            return True
            
        except Exception as e:
            self.aggregator_stats['failed_aggregations'] += 1
            logger.error(f"Error en agregación diaria: {e}")
            return False
    
    async def _aggregate_table_metrics(self, 
                                     table_name: str, 
                                     config: Dict[str, Any], 
                                     start_time: datetime, 
                                     end_time: datetime):
        """Agrega métricas de una tabla específica."""
        try:
            for time_bucket in config['time_buckets']:
                for metric in config['metrics']:
                    for aggregation in config['aggregations']:
                        # Obtener datos agregados
                        aggregated_data = self._get_aggregated_data(
                            table_name, metric, aggregation, time_bucket, start_time, end_time
                        )
                        
                        # Procesar datos agregados
                        for data_point in aggregated_data:
                            await self._process_aggregated_data(
                                table_name, metric, aggregation, time_bucket, data_point
                            )
            
            logger.debug(f"Agregación completada para tabla {table_name}")
            
        except Exception as e:
            logger.error(f"Error agregando métricas de tabla {table_name}: {e}")
    
    def _get_aggregated_data(self, 
                           table_name: str, 
                           metric: str, 
                           aggregation: str, 
                           time_bucket: str, 
                           start_time: datetime, 
                           end_time: datetime) -> List[Dict[str, Any]]:
        """Obtiene datos agregados de TimescaleDB."""
        try:
            # Construir query de agregación
            if aggregation in ['p50', 'p95', 'p99']:
                # Percentiles
                percentile = aggregation[1:]  # Remover 'p'
                query = f"""
                    SELECT 
                        time_bucket(INTERVAL '{time_bucket}', time) as bucket,
                        percentile_cont(0.{percentile}) WITHIN GROUP (ORDER BY {metric}) as value,
                        COUNT(*) as count
                    FROM metrics.{table_name}
                    WHERE time >= %s AND time <= %s
                    AND {metric} IS NOT NULL
                    GROUP BY bucket
                    ORDER BY bucket
                """
            else:
                # Agregaciones estándar
                query = f"""
                    SELECT 
                        time_bucket(INTERVAL '{time_bucket}', time) as bucket,
                        {aggregation.upper()}({metric}) as value,
                        COUNT(*) as count
                    FROM metrics.{table_name}
                    WHERE time >= %s AND time <= %s
                    AND {metric} IS NOT NULL
                    GROUP BY bucket
                    ORDER BY bucket
                """
            
            # Ejecutar query
            with self.timescaledb_manager.connection.cursor() as cursor:
                cursor.execute(query, [start_time, end_time])
                results = cursor.fetchall()
                
                return [
                    {
                        'bucket': row[0],
                        'value': float(row[1]) if row[1] is not None else 0.0,
                        'count': row[2]
                    }
                    for row in results
                ]
                
        except Exception as e:
            logger.error(f"Error obteniendo datos agregados: {e}")
            return []
    
    async def _process_aggregated_data(self, 
                                     table_name: str, 
                                     metric: str, 
                                     aggregation: str, 
                                     time_bucket: str, 
                                     data_point: Dict[str, Any]):
        """Procesa datos agregados."""
        try:
            # Crear métrica agregada
            aggregated_metric = AggregatedMetric(
                metric_name=f"{table_name}.{metric}.{aggregation}",
                metric_type=table_name,
                aggregation_type=aggregation,
                value=data_point['value'],
                timestamp=data_point['bucket'],
                time_bucket=time_bucket,
                tags={
                    'table': table_name,
                    'metric': metric,
                    'aggregation': aggregation,
                    'time_bucket': time_bucket
                },
                metadata={
                    'count': data_point['count'],
                    'source_table': table_name
                }
            )
            
            # Almacenar métrica agregada (implementación simplificada)
            await self._store_aggregated_metric(aggregated_metric)
            
        except Exception as e:
            logger.error(f"Error procesando datos agregados: {e}")
    
    async def _store_aggregated_metric(self, metric: AggregatedMetric):
        """Almacena métrica agregada."""
        # En producción, se almacenaría en una tabla de métricas agregadas
        logger.debug(f"Métrica agregada almacenada: {metric.metric_name} = {metric.value}")
    
    async def _calculate_derived_metrics(self, start_time: datetime, end_time: datetime):
        """Calcula métricas derivadas."""
        try:
            # Configuración de métricas derivadas
            derived_configs = {
                'system_health_score': {
                    'source_metrics': ['system_metrics.cpu_usage_percent.avg', 'system_metrics.memory_usage_percent.avg', 'system_metrics.error_rate.avg'],
                    'calculation': '100 - (cpu_usage + memory_usage + error_rate * 100) / 3'
                },
                'agent_efficiency_score': {
                    'source_metrics': ['execution_metrics.success.avg', 'execution_metrics.execution_time_ms.p95'],
                    'calculation': 'success_rate * (1000 / max(execution_time_ms, 1))'
                },
                'routing_accuracy_score': {
                    'source_metrics': ['routing_metrics.confidence_score.avg', 'routing_metrics.complexity_score.avg'],
                    'calculation': 'confidence_score * (1 - abs(complexity_score - 0.7))'
                }
            }
            
            for metric_name, config in derived_configs.items():
                await self._calculate_single_derived_metric(metric_name, config, start_time, end_time)
            
            self.aggregator_stats['derived_metrics_calculated'] += len(derived_configs)
            
        except Exception as e:
            logger.error(f"Error calculando métricas derivadas: {e}")
    
    async def _calculate_single_derived_metric(self, 
                                             metric_name: str, 
                                             config: Dict[str, Any], 
                                             start_time: datetime, 
                                             end_time: datetime):
        """Calcula una métrica derivada específica."""
        try:
            # Obtener métricas fuente
            source_values = {}
            for source_metric in config['source_metrics']:
                # Simular obtención de valores (en producción vendría de TimescaleDB)
                source_values[source_metric] = np.random.uniform(0.1, 0.9)
            
            # Calcular métrica derivada
            calculation = config['calculation']
            for source_metric, value in source_values.items():
                calculation = calculation.replace(source_metric, str(value))
            
            # Evaluar cálculo (simplificado)
            try:
                derived_value = eval(calculation)
            except:
                derived_value = 0.0
            
            # Crear métrica derivada
            derived_metric = DerivedMetric(
                metric_name=metric_name,
                source_metrics=config['source_metrics'],
                calculation=config['calculation'],
                value=derived_value,
                timestamp=datetime.now(),
                tags={'type': 'derived'},
                metadata={'source_values': source_values}
            )
            
            # Almacenar métrica derivada
            await self._store_derived_metric(derived_metric)
            
        except Exception as e:
            logger.error(f"Error calculando métrica derivada {metric_name}: {e}")
    
    async def _store_derived_metric(self, metric: DerivedMetric):
        """Almacena métrica derivada."""
        # En producción, se almacenaría en una tabla de métricas derivadas
        logger.debug(f"Métrica derivada almacenada: {metric.metric_name} = {metric.value}")
    
    async def _detect_anomalies(self, start_time: datetime, end_time: datetime):
        """Detecta anomalías en las métricas."""
        try:
            # Configuración de detección de anomalías
            anomaly_configs = {
                'system_metrics.cpu_usage_percent.avg': {
                    'threshold': 80.0,
                    'anomaly_type': 'spike',
                    'severity': 'high'
                },
                'system_metrics.memory_usage_percent.avg': {
                    'threshold': 90.0,
                    'anomaly_type': 'spike',
                    'severity': 'critical'
                },
                'execution_metrics.execution_time_ms.p95': {
                    'threshold': 5000.0,
                    'anomaly_type': 'spike',
                    'severity': 'medium'
                },
                'routing_metrics.confidence_score.avg': {
                    'threshold': 0.5,
                    'anomaly_type': 'drop',
                    'severity': 'medium'
                }
            }
            
            for metric_name, config in anomaly_configs.items():
                await self._detect_single_metric_anomalies(metric_name, config, start_time, end_time)
            
        except Exception as e:
            logger.error(f"Error detectando anomalías: {e}")
    
    async def _detect_single_metric_anomalies(self, 
                                            metric_name: str, 
                                            config: Dict[str, Any], 
                                            start_time: datetime, 
                                            end_time: datetime):
        """Detecta anomalías en una métrica específica."""
        try:
            # Simular obtención de valores actuales e históricos
            current_value = np.random.uniform(0.1, 1.0) * 100
            historical_values = np.random.uniform(0.1, 1.0, 100) * 100
            
            # Detectar anomalías
            threshold = config['threshold']
            anomaly_type = config['anomaly_type']
            severity = config['severity']
            
            is_anomaly = False
            deviation_percent = 0.0
            expected_value = np.mean(historical_values)
            
            if anomaly_type == 'spike' and current_value > threshold:
                is_anomaly = True
                deviation_percent = ((current_value - expected_value) / expected_value) * 100
            elif anomaly_type == 'drop' and current_value < threshold:
                is_anomaly = True
                deviation_percent = ((expected_value - current_value) / expected_value) * 100
            
            if is_anomaly:
                # Crear detección de anomalía
                anomaly = AnomalyDetection(
                    metric_name=metric_name,
                    metric_type=metric_name.split('.')[0],
                    anomaly_type=anomaly_type,
                    severity=severity,
                    current_value=current_value,
                    expected_value=expected_value,
                    deviation_percent=deviation_percent,
                    confidence=0.85,  # Simulado
                    timestamp=datetime.now(),
                    description=f"{anomaly_type} detected in {metric_name}: {current_value:.2f} vs expected {expected_value:.2f}",
                    recommendations=self._generate_anomaly_recommendations(metric_name, anomaly_type, severity)
                )
                
                await self._store_anomaly_detection(anomaly)
                self.aggregator_stats['anomalies_detected'] += 1
                
        except Exception as e:
            logger.error(f"Error detectando anomalías en {metric_name}: {e}")
    
    def _generate_anomaly_recommendations(self, metric_name: str, anomaly_type: str, severity: str) -> List[str]:
        """Genera recomendaciones para anomalías."""
        recommendations = []
        
        if 'cpu_usage' in metric_name and anomaly_type == 'spike':
            recommendations.extend([
                "Consider scaling up compute resources",
                "Check for resource-intensive processes",
                "Monitor system load patterns"
            ])
        elif 'memory_usage' in metric_name and anomaly_type == 'spike':
            recommendations.extend([
                "Check for memory leaks",
                "Consider increasing memory allocation",
                "Monitor memory usage patterns"
            ])
        elif 'execution_time' in metric_name and anomaly_type == 'spike':
            recommendations.extend([
                "Check for performance bottlenecks",
                "Review code optimization opportunities",
                "Monitor execution patterns"
            ])
        elif 'confidence_score' in metric_name and anomaly_type == 'drop':
            recommendations.extend([
                "Review routing logic",
                "Check model performance",
                "Consider retraining models"
            ])
        
        return recommendations
    
    async def _store_anomaly_detection(self, anomaly: AnomalyDetection):
        """Almacena detección de anomalía."""
        # En producción, se almacenaría en una tabla de anomalías
        logger.warning(f"Anomalía detectada: {anomaly.description}")
    
    def get_aggregator_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del agregador."""
        return self.aggregator_stats.copy()
    
    async def generate_daily_report(self, target_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Genera reporte diario de métricas."""
        if not target_date:
            target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            start_time = target_date
            end_time = target_date + timedelta(days=1)
            
            report = {
                'date': target_date.date().isoformat(),
                'summary': {
                    'total_metrics_processed': 0,
                    'anomalies_detected': 0,
                    'derived_metrics_calculated': 0,
                    'system_health_score': 0.0,
                    'agent_efficiency_score': 0.0,
                    'routing_accuracy_score': 0.0
                },
                'top_metrics': {},
                'anomalies': [],
                'recommendations': []
            }
            
            # Simular datos del reporte
            report['summary']['total_metrics_processed'] = np.random.randint(1000, 10000)
            report['summary']['anomalies_detected'] = np.random.randint(0, 10)
            report['summary']['derived_metrics_calculated'] = 3
            report['summary']['system_health_score'] = np.random.uniform(70, 95)
            report['summary']['agent_efficiency_score'] = np.random.uniform(60, 90)
            report['summary']['routing_accuracy_score'] = np.random.uniform(75, 95)
            
            # Top métricas
            report['top_metrics'] = {
                'highest_cpu_usage': np.random.uniform(20, 80),
                'highest_memory_usage': np.random.uniform(30, 85),
                'longest_execution_time': np.random.uniform(1000, 5000),
                'most_active_agent': f"agent_{np.random.randint(1, 100)}"
            }
            
            # Anomalías
            if report['summary']['anomalies_detected'] > 0:
                report['anomalies'] = [
                    {
                        'metric': 'system_metrics.cpu_usage_percent.avg',
                        'severity': 'high',
                        'description': 'CPU usage spike detected',
                        'recommendation': 'Consider scaling up resources'
                    }
                ]
            
            # Recomendaciones
            report['recommendations'] = [
                "Monitor system resources closely",
                "Consider optimizing execution performance",
                "Review agent efficiency metrics"
            ]
            
            return report
            
        except Exception as e:
            logger.error(f"Error generando reporte diario: {e}")
            return {}


class MetricsPipeline:
    """Pipeline completo de procesamiento de métricas."""
    
    def __init__(self, timescaledb_manager: TimescaleDBManager):
        self.timescaledb_manager = timescaledb_manager
        self.aggregator = MetricsAggregator(timescaledb_manager)
        
        self.pipeline_stats = {
            'total_pipeline_runs': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'last_run_time': None,
            'next_scheduled_run': None
        }
        
        logger.info("MetricsPipeline inicializado")
    
    async def run_pipeline(self, target_date: Optional[datetime] = None) -> bool:
        """Ejecuta el pipeline completo de métricas."""
        logger.info("Iniciando pipeline de métricas")
        
        try:
            # Ejecutar agregación diaria
            aggregation_success = await self.aggregator.run_daily_aggregation(target_date)
            
            if aggregation_success:
                # Generar reporte diario
                report = await self.aggregator.generate_daily_report(target_date)
                
                # Almacenar reporte (implementación simplificada)
                await self._store_daily_report(report)
                
                self.pipeline_stats['successful_runs'] += 1
                logger.info("Pipeline de métricas completado exitosamente")
                return True
            else:
                self.pipeline_stats['failed_runs'] += 1
                return False
                
        except Exception as e:
            self.pipeline_stats['failed_runs'] += 1
            logger.error(f"Error en pipeline de métricas: {e}")
            return False
        finally:
            self.pipeline_stats['total_pipeline_runs'] += 1
            self.pipeline_stats['last_run_time'] = datetime.now()
    
    async def _store_daily_report(self, report: Dict[str, Any]):
        """Almacena reporte diario."""
        # En producción, se almacenaría en una tabla de reportes
        logger.info(f"Reporte diario almacenado para {report['date']}")
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del pipeline."""
        return {
            'pipeline_stats': self.pipeline_stats,
            'aggregator_stats': self.aggregator.get_aggregator_stats()
        }


if __name__ == "__main__":
    # Test del MetricsPipeline
    logging.basicConfig(level=logging.INFO)
    
    from .timescaledb_manager import TimescaleDBManager
    
    # Crear manager de TimescaleDB (simulado)
    timescaledb_manager = TimescaleDBManager()
    
    # Crear pipeline
    pipeline = MetricsPipeline(timescaledb_manager)
    
    # Ejecutar pipeline
    async def test_pipeline():
        success = await pipeline.run_pipeline()
        print(f"Pipeline ejecutado: {'exitoso' if success else 'fallido'}")
        
        # Mostrar estadísticas
        stats = pipeline.get_pipeline_stats()
        print(f"Estadísticas del pipeline: {stats}")
    
    # Ejecutar test
    asyncio.run(test_pipeline())
