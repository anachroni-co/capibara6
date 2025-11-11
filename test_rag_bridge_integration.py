#!/usr/bin/env python3
"""
Script de prueba completa para el Bridge RAG-Ollama

Este script prueba la integración completa entre:
- Ollama en bounty2 (10.164.0.9:5001)
- Sistema RAG en RAG3 (10.154.0.2:8000)
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Colores para output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Configuración
BOUNTY2_URL = "http://10.164.0.9:5001"
RAG3_URL = "http://10.154.0.2:8000"

def print_header(text: str):
    """Imprimir encabezado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}\n")

def print_success(text: str):
    """Imprimir éxito"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Imprimir error"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    """Imprimir info"""
    print(f"{Colors.BLUE}→ {text}{Colors.END}")

def test_connectivity():
    """Test 1: Verificar conectividad básica"""
    print_header("Test 1: Conectividad Básica")

    # Test bounty2
    print_info("Probando conexión a bounty2...")
    try:
        response = requests.get(f"{BOUNTY2_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"bounty2 respondió: {data.get('status')}")
            print(f"  - Ollama: {data.get('ollama_status')}")
            print(f"  - Modelo: {data.get('ollama_model')}")
        else:
            print_error(f"bounty2 respondió con código {response.status_code}")
            return False
    except Exception as e:
        print_error(f"No se pudo conectar a bounty2: {e}")
        return False

    # Test RAG3
    print_info("\nProbando conexión a RAG3...")
    try:
        response = requests.get(f"{RAG3_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"RAG3 respondió: {data.get('status')}")
            services = data.get('services', {})
            for service, status in services.items():
                print(f"  - {service}: {status}")
        else:
            print_error(f"RAG3 respondió con código {response.status_code}")
            return False
    except Exception as e:
        print_error(f"No se pudo conectar a RAG3: {e}")
        return False

    return True

def test_ollama_models():
    """Test 2: Listar modelos disponibles en Ollama"""
    print_header("Test 2: Modelos Ollama Disponibles")

    try:
        response = requests.get(f"{BOUNTY2_URL}/api/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print_success(f"Se encontraron {len(models)} modelos:")
            for model in models:
                size_gb = model.get('size', 0) / (1024**3)
                print(f"  - {model['name']}: {size_gb:.2f} GB ({model['details']['parameter_size']})")
            return True
        else:
            print_error(f"Error al listar modelos: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_ollama_chat(message: str, description: str) -> Dict[str, Any]:
    """Test chat con Ollama"""
    print_info(f"Probando: {description}")
    print(f"  Pregunta: \"{message}\"")

    try:
        start_time = time.time()
        response = requests.post(
            f"{BOUNTY2_URL}/api/chat",
            json={"message": message},
            timeout=30
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            model = data.get('model', 'unknown')

            print_success(f"Respuesta recibida en {elapsed:.2f}s (modelo: {model})")
            print(f"  Respuesta ({len(response_text)} chars): {response_text[:150]}...")

            return {
                "success": True,
                "response": response_text,
                "model": model,
                "elapsed": elapsed
            }
        else:
            print_error(f"Error {response.status_code}")
            return {"success": False, "error": response.text}

    except Exception as e:
        print_error(f"Error: {e}")
        return {"success": False, "error": str(e)}

def test_rag_search(query: str) -> Dict[str, Any]:
    """Test búsqueda en sistema RAG"""
    print_info(f"Buscando en RAG: \"{query}\"")

    try:
        start_time = time.time()
        response = requests.post(
            f"{RAG3_URL}/api/search/rag",
            json={
                "query": query,
                "n_results": 3,
                "use_graph": True
            },
            timeout=30
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            context = data.get('context', '')
            sources = data.get('sources', [])

            print_success(f"RAG respondió en {elapsed:.2f}s")
            print(f"  Contexto: {len(context)} chars")
            print(f"  Fuentes: {len(sources)}")

            if context:
                print(f"  Muestra: {context[:200]}...")

            return {
                "success": True,
                "context": context,
                "sources": sources,
                "elapsed": elapsed
            }
        else:
            print_error(f"Error {response.status_code}")
            return {"success": False, "error": response.text}

    except Exception as e:
        print_error(f"Error: {e}")
        return {"success": False, "error": str(e)}

def test_rag_enriched_query():
    """Test 4: Consulta enriquecida con RAG (simulada)"""
    print_header("Test 4: Simulación de Consulta Enriquecida con RAG")

    # 1. Primero buscar contexto en RAG
    print_info("Paso 1: Buscar contexto en sistema RAG...")
    query = "machine learning"
    rag_result = test_rag_search(query)

    if not rag_result.get("success"):
        print_error("No se pudo obtener contexto del RAG")
        return False

    context = rag_result.get("context", "")

    # 2. Construir prompt enriquecido
    print_info("\nPaso 2: Construir prompt enriquecido...")
    enriched_prompt = f"""Contexto de información del usuario:
{context[:500] if context else '[Sin contexto disponible]'}

---

Basándote en el contexto anterior (si hay información relevante), responde:
¿Qué es machine learning y cómo se relaciona con IA?"""

    print(f"  Prompt enriquecido: {len(enriched_prompt)} chars")

    # 3. Enviar a Ollama
    print_info("\nPaso 3: Enviar a Ollama con contexto...")
    chat_result = test_ollama_chat(
        enriched_prompt,
        "Chat con contexto RAG"
    )

    if chat_result.get("success"):
        print_success("\n✓ Prueba de integración RAG-Ollama completada!")
        return True
    else:
        print_error("\n✗ Prueba de integración RAG-Ollama falló")
        return False

def test_performance_comparison():
    """Test 5: Comparación de performance"""
    print_header("Test 5: Comparación de Performance")

    tests = [
        ("Pregunta simple", "¿Qué es Python?"),
        ("Pregunta técnica", "Explica qué son los embeddings"),
        ("Generación de código", "Dame código Python para leer un CSV")
    ]

    results = []
    for description, question in tests:
        result = test_ollama_chat(question, description)
        if result.get("success"):
            results.append({
                "description": description,
                "elapsed": result.get("elapsed", 0),
                "response_length": len(result.get("response", ""))
            })
        time.sleep(0.5)  # Pequeña pausa entre requests

    # Mostrar resumen
    print(f"\n{Colors.BOLD}Resumen de Performance:{Colors.END}")
    for r in results:
        print(f"  - {r['description']}: {r['elapsed']:.2f}s ({r['response_length']} chars)")

    if results:
        avg_time = sum(r['elapsed'] for r in results) / len(results)
        print(f"\n  Tiempo promedio: {avg_time:.2f}s")

    return True

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     TEST SUITE: Bridge RAG-Ollama (RAG3 ↔ bounty2)      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(Colors.END)

    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"bounty2: {BOUNTY2_URL}")
    print(f"RAG3: {RAG3_URL}")

    results = {}

    # Test 1: Conectividad
    results['connectivity'] = test_connectivity()

    if not results['connectivity']:
        print_error("\nPruebas canceladas: Sin conectividad básica")
        return

    # Test 2: Modelos
    results['models'] = test_ollama_models()

    # Test 3: Chat básico
    print_header("Test 3: Chat Básico con Ollama")
    results['basic_chat'] = test_ollama_chat(
        "Hola, ¿cómo estás?",
        "Saludo simple"
    ).get("success", False)

    time.sleep(1)

    results['complex_chat'] = test_ollama_chat(
        "Dame un ejemplo de código Python para un chatbot simple",
        "Generación de código"
    ).get("success", False)

    # Test 4: Integración RAG
    results['rag_integration'] = test_rag_enriched_query()

    # Test 5: Performance
    results['performance'] = test_performance_comparison()

    # Resumen final
    print_header("Resumen de Pruebas")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    for test_name, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"  {test_name.ljust(20)}: {status}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} pruebas pasadas{Colors.END}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡Todos los tests pasaron! 🎉{Colors.END}")
    elif passed > total / 2:
        print(f"\n{Colors.YELLOW}Mayoría de tests pasaron, pero hay algunos problemas{Colors.END}")
    else:
        print(f"\n{Colors.RED}Múltiples tests fallaron. Revisar configuración.{Colors.END}")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrumpidos por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}Error fatal: {e}{Colors.END}")
