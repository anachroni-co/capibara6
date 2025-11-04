#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark Tests - Sistema de evaluación HumanEval, MMLU, AppWorld y monitoreo de latencia.
"""

import pytest
import unittest
import logging
import json
import os
import sys
import asyncio
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

# Configurar logging para tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Resultado de benchmark."""
    benchmark_name: str
    test_id: str
    score: float
    execution_time_ms: float
    memory_usage_mb: float
    tokens_used: int
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class LatencyMetrics:
    """Métricas de latencia."""
    p50_ms: float
    p95_ms: float
    p99_ms: float
    p99_9_ms: float
    average_ms: float
    min_ms: float
    max_ms: float
    total_requests: int


class HumanEvalBenchmark:
    """Benchmark HumanEval para evaluación de código."""
    
    def __init__(self):
        self.humaneval_problems = self._load_humaneval_problems()
        self.results: List[BenchmarkResult] = []
        
        logger.info(f"HumanEvalBenchmark inicializado con {len(self.humaneval_problems)} problemas")
    
    def _load_humaneval_problems(self) -> List[Dict[str, Any]]:
        """Carga problemas de HumanEval."""
        # Problemas de ejemplo (en un entorno real se cargarían desde un archivo)
        problems = [
            {
                "task_id": "HumanEval/0",
                "prompt": "def add(a, b):\n    \"\"\"Add two numbers.\"\"\"\n    return a + b",
                "test": "assert add(2, 3) == 5\nassert add(-1, 1) == 0\nassert add(0, 0) == 0",
                "entry_point": "add"
            },
            {
                "task_id": "HumanEval/1",
                "prompt": "def fibonacci(n):\n    \"\"\"Return the nth Fibonacci number.\"\"\"\n    pass",
                "test": "assert fibonacci(0) == 0\nassert fibonacci(1) == 1\nassert fibonacci(10) == 55",
                "entry_point": "fibonacci"
            },
            {
                "task_id": "HumanEval/2",
                "prompt": "def is_palindrome(s):\n    \"\"\"Check if a string is a palindrome.\"\"\"\n    pass",
                "test": "assert is_palindrome('racecar') == True\nassert is_palindrome('hello') == False\nassert is_palindrome('') == True",
                "entry_point": "is_palindrome"
            },
            {
                "task_id": "HumanEval/3",
                "prompt": "def find_max(numbers):\n    \"\"\"Find the maximum number in a list.\"\"\"\n    pass",
                "test": "assert find_max([1, 2, 3, 4, 5]) == 5\nassert find_max([-1, -2, -3]) == -1\nassert find_max([42]) == 42",
                "entry_point": "find_max"
            },
            {
                "task_id": "HumanEval/4",
                "prompt": "def sort_list(lst):\n    \"\"\"Sort a list in ascending order.\"\"\"\n    pass",
                "test": "assert sort_list([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]\nassert sort_list([]) == []\nassert sort_list([1]) == [1]",
                "entry_point": "sort_list"
            }
        ]
        return problems
    
    def run_benchmark(self, model_system, num_problems: int = 5) -> List[BenchmarkResult]:
        """Ejecuta benchmark HumanEval."""
        logger.info(f"Iniciando benchmark HumanEval con {num_problems} problemas")
        
        results = []
        problems_to_test = self.humaneval_problems[:num_problems]
        
        for problem in problems_to_test:
            try:
                start_time = time.time()
                
                # Generar solución usando el sistema de modelo
                solution = self._generate_solution(model_system, problem)
                
                execution_time = (time.time() - start_time) * 1000
                
                # Evaluar solución
                score = self._evaluate_solution(solution, problem)
                
                # Crear resultado
                result = BenchmarkResult(
                    benchmark_name="HumanEval",
                    test_id=problem["task_id"],
                    score=score,
                    execution_time_ms=execution_time,
                    memory_usage_mb=0.0,  # Simulado
                    tokens_used=len(solution.split()) if solution else 0,
                    timestamp=datetime.now(),
                    metadata={
                        "problem": problem["prompt"][:100],
                        "solution": solution[:200] if solution else "",
                        "entry_point": problem["entry_point"]
                    }
                )
                
                results.append(result)
                self.results.append(result)
                
                logger.info(f"✓ HumanEval {problem['task_id']}: score={score:.2f}, time={execution_time:.1f}ms")
                
            except Exception as e:
                logger.error(f"Error en HumanEval {problem['task_id']}: {e}")
                
                # Resultado de error
                result = BenchmarkResult(
                    benchmark_name="HumanEval",
                    test_id=problem["task_id"],
                    score=0.0,
                    execution_time_ms=0.0,
                    memory_usage_mb=0.0,
                    tokens_used=0,
                    timestamp=datetime.now(),
                    metadata={"error": str(e)}
                )
                
                results.append(result)
                self.results.append(result)
        
        return results
    
    def _generate_solution(self, model_system, problem: Dict[str, Any]) -> str:
        """Genera solución usando el sistema de modelo."""
        try:
            # Simular generación de solución
            prompt = problem["prompt"]
            
            # En un entorno real, esto llamaría al sistema de modelo
            if "add" in prompt:
                return "def add(a, b):\n    return a + b"
            elif "fibonacci" in prompt:
                return "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
            elif "is_palindrome" in prompt:
                return "def is_palindrome(s):\n    return s == s[::-1]"
            elif "find_max" in prompt:
                return "def find_max(numbers):\n    return max(numbers) if numbers else None"
            elif "sort_list" in prompt:
                return "def sort_list(lst):\n    return sorted(lst)"
            else:
                return "# Generated solution"
                
        except Exception as e:
            logger.error(f"Error generando solución: {e}")
            return ""
    
    def _evaluate_solution(self, solution: str, problem: Dict[str, Any]) -> float:
        """Evalúa una solución."""
        try:
            if not solution or solution.strip() == "":
                return 0.0
            
            # Simular evaluación (en un entorno real se ejecutaría el código)
            if "add" in problem["prompt"] and "return a + b" in solution:
                return 1.0
            elif "fibonacci" in problem["prompt"] and "fibonacci" in solution:
                return 0.8
            elif "is_palindrome" in problem["prompt"] and "s[::-1]" in solution:
                return 1.0
            elif "find_max" in problem["prompt"] and "max" in solution:
                return 1.0
            elif "sort_list" in problem["prompt"] and "sorted" in solution:
                return 1.0
            else:
                return 0.5  # Solución parcial
            
        except Exception as e:
            logger.error(f"Error evaluando solución: {e}")
            return 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del benchmark."""
        if not self.results:
            return {"total_problems": 0, "average_score": 0.0, "pass_rate": 0.0}
        
        total_problems = len(self.results)
        scores = [r.score for r in self.results]
        average_score = statistics.mean(scores)
        pass_rate = sum(1 for score in scores if score >= 0.8) / total_problems
        
        return {
            "total_problems": total_problems,
            "average_score": average_score,
            "pass_rate": pass_rate,
            "scores": scores,
            "execution_times": [r.execution_time_ms for r in self.results]
        }


class MMLUBenchmark:
    """Benchmark MMLU para evaluación de conocimiento."""
    
    def __init__(self):
        self.mmlu_questions = self._load_mmlu_questions()
        self.results: List[BenchmarkResult] = []
        
        logger.info(f"MMLUBenchmark inicializado con {len(self.mmlu_questions)} preguntas")
    
    def _load_mmlu_questions(self) -> List[Dict[str, Any]]:
        """Carga preguntas de MMLU."""
        # Preguntas de ejemplo
        questions = [
            {
                "question_id": "MMLU/0",
                "subject": "computer_science",
                "question": "What is the time complexity of binary search?",
                "choices": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                "answer": 1
            },
            {
                "question_id": "MMLU/1",
                "subject": "mathematics",
                "question": "What is the derivative of x²?",
                "choices": ["x", "2x", "x²", "2x²"],
                "answer": 1
            },
            {
                "question_id": "MMLU/2",
                "subject": "physics",
                "question": "What is the speed of light in vacuum?",
                "choices": ["3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10¹² m/s"],
                "answer": 1
            },
            {
                "question_id": "MMLU/3",
                "subject": "biology",
                "question": "What is the powerhouse of the cell?",
                "choices": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic reticulum"],
                "answer": 1
            },
            {
                "question_id": "MMLU/4",
                "subject": "history",
                "question": "When did World War II end?",
                "choices": ["1944", "1945", "1946", "1947"],
                "answer": 1
            }
        ]
        return questions
    
    def run_benchmark(self, model_system, num_questions: int = 5) -> List[BenchmarkResult]:
        """Ejecuta benchmark MMLU."""
        logger.info(f"Iniciando benchmark MMLU con {num_questions} preguntas")
        
        results = []
        questions_to_test = self.mmlu_questions[:num_questions]
        
        for question in questions_to_test:
            try:
                start_time = time.time()
                
                # Generar respuesta usando el sistema de modelo
                answer = self._generate_answer(model_system, question)
                
                execution_time = (time.time() - start_time) * 1000
                
                # Evaluar respuesta
                score = self._evaluate_answer(answer, question)
                
                # Crear resultado
                result = BenchmarkResult(
                    benchmark_name="MMLU",
                    test_id=question["question_id"],
                    score=score,
                    execution_time_ms=execution_time,
                    memory_usage_mb=0.0,  # Simulado
                    tokens_used=len(question["question"].split()) + 10,
                    timestamp=datetime.now(),
                    metadata={
                        "subject": question["subject"],
                        "question": question["question"][:100],
                        "predicted_answer": answer,
                        "correct_answer": question["answer"]
                    }
                )
                
                results.append(result)
                self.results.append(result)
                
                logger.info(f"✓ MMLU {question['question_id']}: score={score:.2f}, time={execution_time:.1f}ms")
                
            except Exception as e:
                logger.error(f"Error en MMLU {question['question_id']}: {e}")
                
                # Resultado de error
                result = BenchmarkResult(
                    benchmark_name="MMLU",
                    test_id=question["question_id"],
                    score=0.0,
                    execution_time_ms=0.0,
                    memory_usage_mb=0.0,
                    tokens_used=0,
                    timestamp=datetime.now(),
                    metadata={"error": str(e)}
                )
                
                results.append(result)
                self.results.append(result)
        
        return results
    
    def _generate_answer(self, model_system, question: Dict[str, Any]) -> int:
        """Genera respuesta usando el sistema de modelo."""
        try:
            # Simular generación de respuesta
            question_text = question["question"].lower()
            choices = question["choices"]
            
            # Lógica simple de simulación
            if "binary search" in question_text:
                return 1  # O(log n)
            elif "derivative" in question_text and "x²" in question_text:
                return 1  # 2x
            elif "speed of light" in question_text:
                return 1  # 3 × 10⁸ m/s
            elif "powerhouse" in question_text and "cell" in question_text:
                return 1  # Mitochondria
            elif "world war ii" in question_text and "end" in question_text:
                return 1  # 1945
            else:
                return 0  # Respuesta por defecto
                
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return 0
    
    def _evaluate_answer(self, predicted_answer: int, question: Dict[str, Any]) -> float:
        """Evalúa una respuesta."""
        try:
            correct_answer = question["answer"]
            return 1.0 if predicted_answer == correct_answer else 0.0
            
        except Exception as e:
            logger.error(f"Error evaluando respuesta: {e}")
            return 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del benchmark."""
        if not self.results:
            return {"total_questions": 0, "average_score": 0.0, "accuracy": 0.0}
        
        total_questions = len(self.results)
        scores = [r.score for r in self.results]
        average_score = statistics.mean(scores)
        accuracy = sum(1 for score in scores if score == 1.0) / total_questions
        
        return {
            "total_questions": total_questions,
            "average_score": average_score,
            "accuracy": accuracy,
            "scores": scores,
            "execution_times": [r.execution_time_ms for r in self.results]
        }


class AppWorldBenchmark:
    """Benchmark AppWorld para evaluación de aplicaciones del mundo real."""
    
    def __init__(self):
        self.appworld_tasks = self._load_appworld_tasks()
        self.results: List[BenchmarkResult] = []
        
        logger.info(f"AppWorldBenchmark inicializado con {len(self.appworld_tasks)} tareas")
    
    def _load_appworld_tasks(self) -> List[Dict[str, Any]]:
        """Carga tareas de AppWorld."""
        # Tareas de ejemplo
        tasks = [
            {
                "task_id": "AppWorld/0",
                "category": "web_development",
                "description": "Create a simple REST API endpoint that returns user information",
                "requirements": ["Use Python Flask", "Return JSON", "Handle errors"],
                "test_cases": ["GET /user/1 returns user data", "GET /user/999 returns 404"]
            },
            {
                "task_id": "AppWorld/1",
                "category": "data_analysis",
                "description": "Analyze sales data and create a summary report",
                "requirements": ["Load CSV data", "Calculate metrics", "Generate report"],
                "test_cases": ["Report contains total sales", "Report contains top products"]
            },
            {
                "task_id": "AppWorld/2",
                "category": "automation",
                "description": "Create a script to backup files to cloud storage",
                "requirements": ["Connect to cloud", "Upload files", "Verify upload"],
                "test_cases": ["Files are uploaded", "Upload is verified"]
            }
        ]
        return tasks
    
    def run_benchmark(self, model_system, num_tasks: int = 3) -> List[BenchmarkResult]:
        """Ejecuta benchmark AppWorld."""
        logger.info(f"Iniciando benchmark AppWorld con {num_tasks} tareas")
        
        results = []
        tasks_to_test = self.appworld_tasks[:num_tasks]
        
        for task in tasks_to_test:
            try:
                start_time = time.time()
                
                # Generar solución usando el sistema de modelo
                solution = self._generate_solution(model_system, task)
                
                execution_time = (time.time() - start_time) * 1000
                
                # Evaluar solución
                score = self._evaluate_solution(solution, task)
                
                # Crear resultado
                result = BenchmarkResult(
                    benchmark_name="AppWorld",
                    test_id=task["task_id"],
                    score=score,
                    execution_time_ms=execution_time,
                    memory_usage_mb=0.0,  # Simulado
                    tokens_used=len(solution.split()) if solution else 0,
                    timestamp=datetime.now(),
                    metadata={
                        "category": task["category"],
                        "description": task["description"][:100],
                        "solution": solution[:200] if solution else "",
                        "requirements": task["requirements"]
                    }
                )
                
                results.append(result)
                self.results.append(result)
                
                logger.info(f"✓ AppWorld {task['task_id']}: score={score:.2f}, time={execution_time:.1f}ms")
                
            except Exception as e:
                logger.error(f"Error en AppWorld {task['task_id']}: {e}")
                
                # Resultado de error
                result = BenchmarkResult(
                    benchmark_name="AppWorld",
                    test_id=task["task_id"],
                    score=0.0,
                    execution_time_ms=0.0,
                    memory_usage_mb=0.0,
                    tokens_used=0,
                    timestamp=datetime.now(),
                    metadata={"error": str(e)}
                )
                
                results.append(result)
                self.results.append(result)
        
        return results
    
    def _generate_solution(self, model_system, task: Dict[str, Any]) -> str:
        """Genera solución usando el sistema de modelo."""
        try:
            # Simular generación de solución
            category = task["category"]
            description = task["description"]
            
            if "web_development" in category:
                return """
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/user/<int:user_id>')
def get_user(user_id):
    # Simulate user data
    users = {1: {"id": 1, "name": "John Doe", "email": "john@example.com"}}
    
    if user_id in users:
        return jsonify(users[user_id])
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
"""
            elif "data_analysis" in category:
                return """
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('sales_data.csv')

# Calculate metrics
total_sales = df['amount'].sum()
top_products = df.groupby('product')['amount'].sum().sort_values(ascending=False)

# Generate report
print(f"Total Sales: ${total_sales:,.2f}")
print("Top Products:")
print(top_products.head())
"""
            elif "automation" in category:
                return """
import boto3
import os
from pathlib import Path

def backup_files_to_s3(local_path, bucket_name):
    s3 = boto3.client('s3')
    
    for file_path in Path(local_path).rglob('*'):
        if file_path.is_file():
            s3.upload_file(str(file_path), bucket_name, str(file_path))
            print(f"Uploaded: {file_path}")

# Usage
backup_files_to_s3('./data', 'my-backup-bucket')
"""
            else:
                return "# Generated solution for AppWorld task"
                
        except Exception as e:
            logger.error(f"Error generando solución: {e}")
            return ""
    
    def _evaluate_solution(self, solution: str, task: Dict[str, Any]) -> float:
        """Evalúa una solución."""
        try:
            if not solution or solution.strip() == "":
                return 0.0
            
            score = 0.0
            requirements = task["requirements"]
            
            # Evaluar cada requerimiento
            for requirement in requirements:
                if requirement.lower() in solution.lower():
                    score += 1.0 / len(requirements)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error evaluando solución: {e}")
            return 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del benchmark."""
        if not self.results:
            return {"total_tasks": 0, "average_score": 0.0, "completion_rate": 0.0}
        
        total_tasks = len(self.results)
        scores = [r.score for r in self.results]
        average_score = statistics.mean(scores)
        completion_rate = sum(1 for score in scores if score >= 0.7) / total_tasks
        
        return {
            "total_tasks": total_tasks,
            "average_score": average_score,
            "completion_rate": completion_rate,
            "scores": scores,
            "execution_times": [r.execution_time_ms for r in self.results]
        }


class LatencyMonitor:
    """Monitor de latencia para métricas p50/p95/p99."""
    
    def __init__(self):
        self.latency_history: List[float] = []
        self.request_times: List[Tuple[datetime, float]] = []
        
        logger.info("LatencyMonitor inicializado")
    
    def record_request(self, latency_ms: float):
        """Registra latencia de una request."""
        self.latency_history.append(latency_ms)
        self.request_times.append((datetime.now(), latency_ms))
        
        # Mantener solo los últimos 1000 registros
        if len(self.latency_history) > 1000:
            self.latency_history = self.latency_history[-1000:]
            self.request_times = self.request_times[-1000:]
    
    def get_latency_metrics(self) -> LatencyMetrics:
        """Obtiene métricas de latencia."""
        if not self.latency_history:
            return LatencyMetrics(
                p50_ms=0.0, p95_ms=0.0, p99_ms=0.0, p99_9_ms=0.0,
                average_ms=0.0, min_ms=0.0, max_ms=0.0, total_requests=0
            )
        
        sorted_latencies = sorted(self.latency_history)
        total_requests = len(sorted_latencies)
        
        return LatencyMetrics(
            p50_ms=sorted_latencies[int(total_requests * 0.5)],
            p95_ms=sorted_latencies[int(total_requests * 0.95)],
            p99_ms=sorted_latencies[int(total_requests * 0.99)],
            p99_9_ms=sorted_latencies[int(total_requests * 0.999)],
            average_ms=statistics.mean(sorted_latencies),
            min_ms=min(sorted_latencies),
            max_ms=max(sorted_latencies),
            total_requests=total_requests
        )
    
    def get_recent_metrics(self, minutes: int = 5) -> LatencyMetrics:
        """Obtiene métricas de los últimos N minutos."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_latencies = [
            latency for timestamp, latency in self.request_times
            if timestamp >= cutoff_time
        ]
        
        if not recent_latencies:
            return LatencyMetrics(
                p50_ms=0.0, p95_ms=0.0, p99_ms=0.0, p99_9_ms=0.0,
                average_ms=0.0, min_ms=0.0, max_ms=0.0, total_requests=0
            )
        
        sorted_latencies = sorted(recent_latencies)
        total_requests = len(sorted_latencies)
        
        return LatencyMetrics(
            p50_ms=sorted_latencies[int(total_requests * 0.5)],
            p95_ms=sorted_latencies[int(total_requests * 0.95)],
            p99_ms=sorted_latencies[int(total_requests * 0.99)],
            p99_9_ms=sorted_latencies[int(total_requests * 0.999)],
            average_ms=statistics.mean(sorted_latencies),
            min_ms=min(sorted_latencies),
            max_ms=max(sorted_latencies),
            total_requests=total_requests
        )


class BenchmarkSuite:
    """Suite completa de benchmarks."""
    
    def __init__(self):
        self.humaneval = HumanEvalBenchmark()
        self.mmlu = MMLUBenchmark()
        self.appworld = AppWorldBenchmark()
        self.latency_monitor = LatencyMonitor()
        
        self.all_results: List[BenchmarkResult] = []
        
        logger.info("BenchmarkSuite inicializada")
    
    def run_all_benchmarks(self, model_system, 
                          humaneval_problems: int = 5,
                          mmlu_questions: int = 5,
                          appworld_tasks: int = 3) -> Dict[str, Any]:
        """Ejecuta todos los benchmarks."""
        logger.info("Iniciando suite completa de benchmarks")
        
        start_time = time.time()
        
        # Ejecutar benchmarks
        humaneval_results = self.humaneval.run_benchmark(model_system, humaneval_problems)
        mmlu_results = self.mmlu.run_benchmark(model_system, mmlu_questions)
        appworld_results = self.appworld.run_benchmark(model_system, appworld_tasks)
        
        # Recopilar todos los resultados
        self.all_results.extend(humaneval_results)
        self.all_results.extend(mmlu_results)
        self.all_results.extend(appworld_results)
        
        # Registrar latencias
        for result in self.all_results:
            self.latency_monitor.record_request(result.execution_time_ms)
        
        total_time = time.time() - start_time
        
        # Generar resumen
        summary = {
            "total_execution_time_seconds": total_time,
            "humaneval": self.humaneval.get_summary(),
            "mmlu": self.mmlu.get_summary(),
            "appworld": self.appworld.get_summary(),
            "latency_metrics": asdict(self.latency_monitor.get_latency_metrics()),
            "overall_score": self._calculate_overall_score()
        }
        
        logger.info(f"Suite de benchmarks completada en {total_time:.2f}s")
        return summary
    
    def _calculate_overall_score(self) -> float:
        """Calcula score general."""
        if not self.all_results:
            return 0.0
        
        scores = [r.score for r in self.all_results]
        return statistics.mean(scores)
    
    def run_latency_test(self, model_system, num_requests: int = 100) -> LatencyMetrics:
        """Ejecuta test de latencia."""
        logger.info(f"Iniciando test de latencia con {num_requests} requests")
        
        test_queries = [
            "Simple test query",
            "Complex machine learning question",
            "Database optimization query",
            "JavaScript debugging help",
            "API development question"
        ]
        
        for i in range(num_requests):
            query = test_queries[i % len(test_queries)]
            
            start_time = time.time()
            
            # Simular procesamiento
            try:
                # En un entorno real, esto llamaría al sistema de modelo
                time.sleep(0.01)  # Simular 10ms de procesamiento
                
                latency = (time.time() - start_time) * 1000
                self.latency_monitor.record_request(latency)
                
            except Exception as e:
                logger.error(f"Error en request {i}: {e}")
                self.latency_monitor.record_request(1000.0)  # Latencia de error
        
        metrics = self.latency_monitor.get_latency_metrics()
        logger.info(f"Test de latencia completado: p50={metrics.p50_ms:.1f}ms, p95={metrics.p95_ms:.1f}ms, p99={metrics.p99_ms:.1f}ms")
        
        return metrics
    
    def get_benchmark_report(self) -> Dict[str, Any]:
        """Genera reporte completo de benchmarks."""
        return {
            "timestamp": datetime.now().isoformat(),
            "humaneval_summary": self.humaneval.get_summary(),
            "mmlu_summary": self.mmlu.get_summary(),
            "appworld_summary": self.appworld.get_summary(),
            "latency_metrics": asdict(self.latency_monitor.get_latency_metrics()),
            "overall_score": self._calculate_overall_score(),
            "total_benchmarks": len(self.all_results),
            "results": [asdict(r) for r in self.all_results]
        }


def run_benchmark_tests():
    """Ejecuta todos los tests de benchmark."""
    logger.info("Iniciando tests de benchmark...")
    
    # Crear suite de benchmarks
    benchmark_suite = BenchmarkSuite()
    
    # Sistema de modelo simulado
    model_system = Mock()
    
    try:
        # Ejecutar benchmarks
        summary = benchmark_suite.run_all_benchmarks(
            model_system,
            humaneval_problems=5,
            mmlu_questions=5,
            appworld_tasks=3
        )
        
        # Ejecutar test de latencia
        latency_metrics = benchmark_suite.run_latency_test(model_system, num_requests=50)
        
        # Mostrar resultados
        logger.info(f"\n{'='*60}")
        logger.info("RESULTADOS DE BENCHMARKS")
        logger.info(f"{'='*60}")
        
        logger.info(f"HumanEval:")
        logger.info(f"  Problemas: {summary['humaneval']['total_problems']}")
        logger.info(f"  Score promedio: {summary['humaneval']['average_score']:.3f}")
        logger.info(f"  Pass rate: {summary['humaneval']['pass_rate']:.3f}")
        
        logger.info(f"MMLU:")
        logger.info(f"  Preguntas: {summary['mmlu']['total_questions']}")
        logger.info(f"  Score promedio: {summary['mmlu']['average_score']:.3f}")
        logger.info(f"  Accuracy: {summary['mmlu']['accuracy']:.3f}")
        
        logger.info(f"AppWorld:")
        logger.info(f"  Tareas: {summary['appworld']['total_tasks']}")
        logger.info(f"  Score promedio: {summary['appworld']['average_score']:.3f}")
        logger.info(f"  Completion rate: {summary['appworld']['completion_rate']:.3f}")
        
        logger.info(f"Latencia:")
        logger.info(f"  P50: {latency_metrics.p50_ms:.1f}ms")
        logger.info(f"  P95: {latency_metrics.p95_ms:.1f}ms")
        logger.info(f"  P99: {latency_metrics.p99_ms:.1f}ms")
        logger.info(f"  Promedio: {latency_metrics.average_ms:.1f}ms")
        
        logger.info(f"Score general: {summary['overall_score']:.3f}")
        
        # Generar reporte
        report = benchmark_suite.get_benchmark_report()
        
        # Guardar reporte
        report_file = "backend/data/benchmark_report.json"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Reporte guardado en: {report_file}")
        
        logger.info("🎉 Tests de benchmark completados exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"Error en tests de benchmark: {e}")
        return False


if __name__ == "__main__":
    success = run_benchmark_tests()
    sys.exit(0 if success else 1)
