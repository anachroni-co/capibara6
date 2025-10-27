#!/usr/bin/env python3
"""
Script de Prueba para Mejoras GPT-OSS-20B
Prueba las mejoras implementadas en el servidor
"""

import requests
import json
import time
from gpt_oss_optimized_config import get_category_payload, get_quality_payload

# Configuración de prueba
TEST_SERVER_URL = "http://localhost:5001/api/chat"
TEST_QUESTIONS = [
    {
        "question": "¿Cómo te llamas?",
        "category": "general",
        "expected_keywords": ["Capibara6", "asistente", "IA"]
    },
    {
        "question": "¿Puedes ayudarme con código Python?",
        "category": "programming", 
        "expected_keywords": ["Python", "código", "programación"]
    },
    {
        "question": "Escribe un cuento corto",
        "category": "creative_writing",
        "expected_keywords": ["historia", "personaje", "narrativa"]
    },
    {
        "question": "¿Qué hora es?",
        "category": "quick_questions",
        "expected_keywords": ["hora", "tiempo", "fecha"]
    }
]

def test_server_connection():
    """Probar conexión con el servidor"""
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor conectado correctamente")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_question(question_data):
    """Probar una pregunta específica"""
    print(f"\n🔍 Probando: {question_data['question']}")
    
    try:
        payload = {
            "message": question_data["question"],
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        response = requests.post(
            TEST_SERVER_URL,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            
            print(f"📝 Respuesta ({len(response_text)} chars): {response_text[:100]}...")
            
            # Verificar longitud mínima
            if len(response_text) < 50:
                print("⚠️ Respuesta muy corta")
            else:
                print("✅ Respuesta de longitud adecuada")
            
            # Verificar palabras clave esperadas
            found_keywords = []
            for keyword in question_data['expected_keywords']:
                if keyword.lower() in response_text.lower():
                    found_keywords.append(keyword)
            
            if found_keywords:
                print(f"✅ Palabras clave encontradas: {found_keywords}")
            else:
                print(f"⚠️ No se encontraron palabras clave esperadas: {question_data['expected_keywords']}")
            
            # Verificar que no sea respuesta genérica
            generic_responses = [
                "i am a large language model",
                "soy un modelo de ia",
                "i am an ai assistant",
                "no puedo ayudarte"
            ]
            
            is_generic = any(generic in response_text.lower() for generic in generic_responses)
            if is_generic:
                print("❌ Respuesta genérica detectada")
            else:
                print("✅ Respuesta específica y útil")
            
            return {
                "success": True,
                "length": len(response_text),
                "keywords_found": found_keywords,
                "is_generic": is_generic,
                "response": response_text
            }
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return {"success": False, "error": str(e)}

def test_optimized_config():
    """Probar la configuración optimizada directamente"""
    print("\n🧪 Probando configuración optimizada...")
    
    test_prompt = "¿Cómo te llamas y qué puedes hacer?"
    
    # Probar diferentes categorías
    categories = ["general", "programming", "creative_writing", "quick_questions"]
    
    for category in categories:
        print(f"\n📋 Categoría: {category}")
        payload = get_category_payload(test_prompt, category)
        
        print(f"   - n_predict: {payload.get('n_predict', 'N/A')}")
        print(f"   - temperature: {payload.get('temperature', 'N/A')}")
        print(f"   - top_p: {payload.get('top_p', 'N/A')}")
        print(f"   - repeat_penalty: {payload.get('repeat_penalty', 'N/A')}")
        print(f"   - stop tokens: {len(payload.get('stop', []))}")

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas de mejoras GPT-OSS-20B")
    print("=" * 50)
    
    # Probar conexión
    if not test_server_connection():
        print("❌ No se puede conectar con el servidor. Asegúrate de que esté ejecutándose.")
        return
    
    # Probar configuración optimizada
    test_optimized_config()
    
    # Probar preguntas
    print("\n" + "=" * 50)
    print("🧪 Probando preguntas de ejemplo")
    print("=" * 50)
    
    results = []
    for question_data in TEST_QUESTIONS:
        result = test_question(question_data)
        results.append(result)
        time.sleep(1)  # Pausa entre pruebas
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 50)
    
    successful_tests = sum(1 for r in results if r.get("success", False))
    total_tests = len(results)
    
    print(f"✅ Pruebas exitosas: {successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! Las mejoras están funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    # Estadísticas de respuestas
    successful_results = [r for r in results if r.get("success", False)]
    if successful_results:
        avg_length = sum(r.get("length", 0) for r in successful_results) / len(successful_results)
        print(f"📏 Longitud promedio de respuestas: {avg_length:.1f} caracteres")
        
        generic_count = sum(1 for r in successful_results if r.get("is_generic", False))
        print(f"🎯 Respuestas específicas: {len(successful_results) - generic_count}/{len(successful_results)}")

if __name__ == "__main__":
    main()
