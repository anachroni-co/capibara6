<<<<<<< HEAD
# capibara6_integrated_server.py
# Servidor integrado principal para el proyecto Capibara6

from flask import Flask, request, jsonify, Response
import requests
import json
import os
from models_config import MODEL_CONFIGS, DEFAULT_MODEL, TIMEOUT
from toon_utils.format_manager import FormatManager
import logging

import sys
import os
# Asegurar que el path incluya el directorio backend
sys.path.insert(0, os.path.dirname(__file__))

# Importar la integración de e2b
try:
    from capibara6_e2b_integration import init_e2b_integration
    from utils import analyze_context, understand_query, determine_action, calculate_relevance
    E2B_AVAILABLE = True
    print("Integración e2b disponible")
except ImportError as e:
    E2B_AVAILABLE = False
    print(f"Integración e2b no disponible: {e}")
    # Definir funciones de respaldo en caso de error
    def analyze_context(context):
        if isinstance(context, str):
            return {
                'length': len(context),
                'word_count': len(context.split()),
                'has_personal_info': 'nombre' in context.lower() or 'usuario' in context.lower(),
                'context_type': 'text'
            }
        return {'type': type(context).__name__}

    def understand_query(query):
        query_lower = query.lower() if isinstance(query, str) else ''
        intent_analysis = {
            'is_question': '?' in query or any(word in query_lower for word in ['qué', 'cuál', 'cómo', 'por qué', 'when', 'what', 'how', 'why']),
            'is_command': any(word in query_lower for word in ['haz', 'crea', 'genera', 'hablemos', 'do', 'create', 'generate', 'let\'s']),
            'complexity': 'high' if len(query) > 100 else 'medium' if len(query) > 50 else 'low'
        }
        return intent_analysis

    def determine_action(context, query):
        return {
            'next_step': 'process_query',
            'requires_context_extension': len(str(context)) < 100,
            'model_preference': 'context_aware'
        }

    def calculate_relevance(context, query):
        if not context or not query:
            return 0.0
        context_words = set(str(context).lower().split())
        query_words = set(str(query).lower().split())
        if not context_words or not query_words:
            return 0.0
        common_words = context_words.intersection(query_words)
        relevance_score = len(common_words) / len(query_words) if query_words else 0.0
        return min(relevance_score, 1.0)

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar la integración de e2b si está disponible
e2b_integration = None
if E2B_AVAILABLE:
    try:
        e2b_integration = init_e2b_integration()
        logger.info("Integración e2b inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la integración e2b: {e}")
        E2B_AVAILABLE = False

# Proxy para GPT-OSS-20B
@app.route('/api/chat', methods=['POST'])
def proxy_gpt_oss_20b():
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        
        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()
        
        model_config = MODEL_CONFIGS.get('gpt_oss_20b')
        
        if not model_config:
            error_response = {'error': 'Modelo GPT-OSS-20B no configurado'}
            
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManager.encode(error_response, 'toon')
                return Response(content, mimetype='text/plain', status=404)
            else:
                return jsonify(error_response), 404
        
        # Reenviar la solicitud al servidor remoto
        response = requests.post(
            model_config['endpoint'],
            json=input_data,
            timeout=TIMEOUT/1000  # Convertir de ms a segundos
        )
        
        # Determinar el formato de la respuesta del modelo
        if response.headers.get('Content-Type', '').startswith('application/json'):
            model_response = response.json()
        else:
            model_response = response.text  # Si no es JSON, manejar como texto
        
        # Determinar formato de salida para el cliente
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(model_response, 'toon')
            return Response(
                content,
                status=response.status_code,
                mimetype='text/plain'
            )
        else:
            # Devolver directamente la respuesta del modelo
            return Response(
                response.content,
                status=response.status_code,
                content_type='application/json'
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al conectar con GPT-OSS-20B: {e}")
        error_response = {'error': 'Error al conectar con el modelo GPT-OSS-20B'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        error_response = {'error': 'Error interno del servidor'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

# Smart MCP integrado
@app.route('/api/mcp/analyze', methods=['POST'])
def smart_mcp_analyze():
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        
        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()
        
        # Análisis inteligente del contexto (misma lógica que en smart_mcp_server)
        context = input_data.get('context', '')
        query = input_data.get('query', '')
        
        analysis_result = {
            'status': 'completed',
            'context_analysis': _analyze_context(context),
            'query_understanding': _understand_query(query),
            'recommended_action': _determine_action(context, query),
            'context_relevance': _calculate_relevance(context, query),
            'token_optimization_used': True,  # Indicar soporte de TOON
            'source': 'integrated_server'
        }
        
        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(analysis_result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(analysis_result)
            
    except Exception as e:
        logger.error(f"Error en MCP integrado: {e}")
        error_response = {'error': 'Error en el análisis MCP integrado'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

# Las funciones analíticas ahora están en utils.py para evitar importaciones circulares
# Mantenemos estas funciones para mantener compatibilidad con código existente
def _analyze_context(context):
    return analyze_context(context)

def _understand_query(query):
    return understand_query(query)

def _determine_action(context, query):
    return determine_action(context, query)

def _calculate_relevance(context, query):
    return calculate_relevance(context, query)

# TTS básico integrado
@app.route('/api/tts/speak', methods=['POST'])
def basic_tts():
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        
        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()
        
        text = input_data.get('text', '')
        
        # Simulación de respuesta TTS
        result = {
            'status': 'success',
            'message': f'Texto procesado para TTS: {text[:50]}...',
            'token_optimization_used': True
        }
        
        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error en TTS: {e}")
        error_response = {'error': 'Error en el servicio TTS'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

# Endpoint para tareas que requieren entornos aislados con e2b
@app.route('/api/e2b/process', methods=['POST'])
def e2b_process():
    """Procesa tareas que requieren entornos aislados usando e2b"""
    if not E2B_AVAILABLE:
        error_response = {'error': 'Integración e2b no disponible'}
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()

        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()

        prompt = input_data.get('prompt', '')
        context = input_data.get('context', '')
        
        if not prompt:
            error_response = {'error': 'Prompt es requerido'}
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManager.encode(error_response, 'toon')
                return Response(content, mimetype='text/plain', status=400)
            else:
                return jsonify(error_response), 400

        # Usar la integración de e2b para procesar la tarea
        import asyncio
        from threading import Thread

        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    e2b_integration.handle_complex_task_with_e2b(prompt, context)
                )
                return result
            finally:
                loop.close()

        # Ejecutar la operación asíncrona en un hilo separado
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_async)
            result = future.result()

        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)

    except Exception as e:
        logger.error(f"Error en e2b_process: {e}")
        error_response = {'error': f'Error en el procesamiento e2b: {str(e)}'}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

# Endpoint para obtener archivos de visualización desde e2b
@app.route('/api/e2b/visualization/<path:filepath>', methods=['GET'])
def get_visualization_file(filepath):
    """Obtiene un archivo de visualización generado en e2b"""
    if not E2B_AVAILABLE:
        return jsonify({'error': 'Integración e2b no disponible'}), 500
    
    try:
        # Este endpoint sería para servir archivos directamente
        # Por ahora, simulamos el comportamiento
        # En una implementación completa, se recuperaría el archivo del sandbox
        return jsonify({'error': 'Funcionalidad de recuperación de archivos en desarrollo'}), 503
    except Exception as e:
        logger.error(f"Error obteniendo archivo de visualización: {e}")
        return jsonify({'error': f'Error obteniendo archivo: {str(e)}'}), 500

# Endpoint para estimar recursos necesarios para una tarea
@app.route('/api/e2b/estimate', methods=['POST'])
def e2b_estimate():
    """Estima los recursos necesarios para una tarea usando e2b"""
    if not E2B_AVAILABLE:
        error_response = {'error': 'Integración e2b no disponible'}
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()

        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()

        prompt = input_data.get('prompt', '')
        
        if not prompt:
            error_response = {'error': 'Prompt es requerido'}
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManager.encode(error_response, 'toon')
                return Response(content, mimetype='text/plain', status=400)
            else:
                return jsonify(error_response), 400

        # Usar la integración de e2b para estimar recursos
        resources = e2b_integration.estimate_task_resources(prompt)

        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(resources, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(resources)

    except Exception as e:
        logger.error(f"Error en e2b_estimate: {e}")
        error_response = {'error': f'Error en la estimación de recursos e2b: {str(e)}'}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

# Endpoint para generar texto con clasificación CTM (funcionalidad de Ollama local)
@app.route('/api/ai/generate', methods=['POST'])
def ai_generate_ctm():
    """Genera texto usando CTM para clasificar la tarea y Ollama local para la generación"""
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        
        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()

        prompt = input_data.get('prompt', '')
        modelPreference = input_data.get('modelPreference', 'auto')
        
        # Importar dinámicamente el sistema CTM desde la implementación de Node.js
        # Para hacerlo funcional, necesitamos implementar la lógica CTM en Python también
        model_recommendation = classify_task_ctm(prompt) if modelPreference == 'auto' else modelPreference
        
        # Generar respuesta usando Ollama local
        response = generate_with_ollama(prompt, model_recommendation)
        
        if response and response.get('success'):
            result = {
                'success': True,
                'response': response.get('response', ''),
                'model_used': response.get('model', model_recommendation),
                'processing_time': response.get('total_duration', 0),
                'token_count': response.get('token_count', 0)
            }
        else:
            result = {
                'success': False,
                'error': response.get('error', 'Error al generar la respuesta'),
                'model_used': model_recommendation
            }

        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)

    except Exception as e:
        logger.error(f"Error en ai_generate_ctm: {e}")
        error_response = {'error': f'Error al generar respuesta: {str(e)}', 'success': False}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManager.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500

def classify_task_ctm(prompt):
    """Implementación de clasificación CTM en Python (equivalente al sistema de Node.js)"""
    import re
    
    prompt_lower = prompt.lower()
    
    # Clasificación basada en características cognitivas (similar al sistema CTM de Node.js)
    complexity_indicators = {
        'complex': ['análisis', 'razonamiento', 'comparación', 'evaluar', 'estrategia', 'planificación', 
                   'investigación', 'profundo', 'detalle', 'complejo', 'técnico', 'evaluación', 
                   'interpretación', 'síntesis', 'problema', 'dilema', 'paradigma', 'metodología', 
                   'hipótesis', 'teoría', 'implicaciones', 'consecuencias', 'factores', 'dimensiones'],
        'balanced': ['explicar', 'qué es', 'cómo funciona', 'describir', 'resumen', 'breve', 
                    'ejemplo', 'definir', 'funciona', 'significado', 'característica', 'proceso'],
        'simple': ['qué', 'quién', 'cuál', 'cuándo', 'dónde', 'chiste', 'broma', 'saludo', 
                  'ayuda', 'cuánto', 'dime', 'haz', 'crea']
    }

    # Contar indicadores de cada tipo
    complex_score = sum(2 for indicator in complexity_indicators['complex'] if indicator in prompt_lower)
    balanced_score = sum(1 for indicator in complexity_indicators['balanced'] if indicator in prompt_lower)
    simple_score = sum(1 for indicator in complexity_indicators['simple'] if indicator in prompt_lower)
    
    # Considerar la longitud del prompt
    if len(prompt) > 100:
        balanced_score += 1
    if len(prompt) > 200:
        complex_score += 1
    
    # Considerar la complejidad sintáctica (número de frases)
    sentence_count = len(re.split(r'[.!?]+', prompt)) - 1  # Restar 1 porque hay un elemento extra al final
    if sentence_count > 3:
        complex_score += 1
    
    # Determinar el modelo más apropiado
    max_score = max(complex_score, balanced_score, simple_score)
    if max_score == complex_score:
        return 'complex'
    elif max_score == balanced_score:
        return 'balanced'
    else:
        return 'fast_response'

def generate_with_ollama(prompt, model_tier):
    """Genera texto usando Ollama local"""
    import requests
    import time
    
    # Mapear el tier al modelo real
    model_mapping = {
        'fast_response': 'phi3:mini',
        'balanced': 'mistral', 
        'complex': 'gpt-oss:20b'
    }
    
    model_name = model_mapping.get(model_tier, 'phi3:mini')
    
    # Configurar el endpoint de Ollama
    ollama_endpoint = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
            "top_k": 40
        }
    }
    
    try:
        start_time = time.time()
        response = requests.post(ollama_endpoint, json=payload, timeout=240)  # Ajustar timeout
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'response': data.get('response', ''),
                'model': model_name,
                'total_duration': int((end_time - start_time) * 1000),  # Convertir a ms
                'token_count': data.get('eval_count', 0)
            }
        else:
            return {
                'success': False,
                'error': f'Error de Ollama: {response.status_code}'
            }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Timeout al comunicarse con Ollama'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error al comunicarse con Ollama: {str(e)}'
        }

# Health check funcional
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'capibara6_integrated_server',
        'models': list(MODEL_CONFIGS.keys()),
        'e2b_available': E2B_AVAILABLE,
        'toon_support': True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
=======
#!/usr/bin/env python3
"""
Servidor Integrado Capibara6
Combina:
- Proxy CORS para GPT-OSS-20B
- Smart MCP Server
- Coqui TTS Server
Puerto: 5000
"""

from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import requests
import json
import os
import sys
import tempfile
import base64
import io
from datetime import datetime
import re
from pathlib import Path
from gpt_oss_optimized_config import get_category_payload, get_context_aware_payload

# Importar TOON Format Manager
try:
    from toon_utils.format_manager import FormatManager
    TOON_AVAILABLE = True
    print("✅ TOON Format Manager disponible")
except ImportError as e:
    print(f"⚠️ TOON Format Manager no disponible: {e}")
    TOON_AVAILABLE = False

# Importar Semantic Router
try:
    from semantic_model_router import get_router
    SEMANTIC_ROUTER_ENABLED = True
    print("✅ Semantic Router disponible")
except ImportError as e:
    print(f"⚠️ Semantic Router no disponible: {e}")
    print("   Instalar con: pip install semantic-router")
    SEMANTIC_ROUTER_ENABLED = False

# Importar configuración de modelos
try:
    from models_config import get_model_config, MODELS_CONFIG
    MODELS_CONFIG_AVAILABLE = True
except ImportError:
    print("⚠️ models_config.py no disponible, usando configuración por defecto")
    MODELS_CONFIG_AVAILABLE = False

app = Flask(__name__)
CORS(app, origins='*')  # Permitir conexiones desde cualquier origen

# ============================================
# CONFIGURACIÓN GPT-OSS-20B (Local en la VM)
# ============================================
GPTOSS_API_URL = 'http://34.175.215.109:8080/completion'  # VM en la nube
GPTOSS_HEALTH_URL = 'http://34.175.215.109:8080/health'

# ============================================
# CONFIGURACIÓN MCP (Smart Context)
# ============================================
KNOWLEDGE_BASE = {
    "identity": {
        "name": "Capibara6",
        "creator": "Anachroni s.coop",
        "status": "Producción",
        "type": "Modelo de lenguaje GPT-OSS-20B",
        "hardware": "Google Cloud VM en europe-southwest1-b",
        "website": "https://capibara6.com",
        "email": "info@anachroni.co"
    },
    "current_info": {
        "date": "15 de octubre de 2025",
        "day": "martes"
    }
}

CONTEXT_TRIGGERS = {
    "identity": {
        "patterns": [
            r'\b(quién|quien|que|qué)\s+(eres|soy|es)\b',
            r'\b(cómo|como)\s+(te\s+llamas|se\s+llama)\b',
            r'\b(tu|tú)\s+(nombre|identidad)\b',
            r'\bcapibara\b',
            r'\bcreo|creador|desarrollador\b',
            r'\bquién\s+te\s+(creó|creo|hizo|desarrollo)\b',
            r'\b(tu|tú)\s+nombre\b'
        ],
        "context": lambda: f"""[INFORMACIÓN VERIFICADA]
Tu nombre es: {KNOWLEDGE_BASE['identity']['name']}
Estado: {KNOWLEDGE_BASE['identity']['status']}
Creado por: {KNOWLEDGE_BASE['identity']['creator']}
Tipo: {KNOWLEDGE_BASE['identity']['type']}
Contacto: {KNOWLEDGE_BASE['identity']['email']}
Web: {KNOWLEDGE_BASE['identity']['website']}
"""
    },
    "date": {
        "patterns": [
            r'\b(fecha|día|día de hoy|hoy)\b',
            r'\bqu\w*\s+día\b',
            r'\bque\s+fecha\b'
        ],
        "context": lambda: f"""[INFORMACIÓN ACTUAL]
Fecha: {KNOWLEDGE_BASE['current_info']['date']}
Día: {KNOWLEDGE_BASE['current_info']['day']}
"""
    }
}

# ============================================
# CONFIGURACIÓN TTS
# ============================================
COQUI_CONFIG = {
    'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
    'sample_rate': 24000,
    'max_chars': 3000,
    'speed': 1.0,
    'language': 'es',
}

VOICES_DIR = Path(__file__).parent / 'voices_reference'
VOICES_DIR.mkdir(exist_ok=True)

PREDEFINED_VOICES = {
    'sofia': {
        'name': 'Sofía',
        'gender': 'female',
        'description': 'Voz femenina cálida y profesional',
        'language': 'es',
        'speaker_embedding': 'Claribel Dervla',
    },
    'ana': {
        'name': 'Ana',
        'gender': 'female', 
        'description': 'Voz femenina joven y amigable',
        'language': 'es',
        'speaker_embedding': 'Daisy Studious',
    },
    'carlos': {
        'name': 'Carlos',
        'gender': 'male',
        'description': 'Voz masculina profesional',
        'language': 'es',
        'speaker_embedding': 'Josh',
    }
}

# ============================================
# FUNCIONES MCP
# ============================================
def analyze_message_for_context(message):
    """Analiza el mensaje para determinar si necesita contexto adicional"""
    message_lower = message.lower()
    
    for category, trigger_info in CONTEXT_TRIGGERS.items():
        for pattern in trigger_info['patterns']:
            if re.search(pattern, message_lower):
                return trigger_info['context']()
    
    return None

def enhance_message_with_context(message):
    """Mejora el mensaje con contexto relevante si es necesario"""
    context = analyze_message_for_context(message)
    
    if context:
        enhanced_message = f"{context}\n\nPregunta del usuario: {message}"
        return enhanced_message
    
    return message

# ============================================
# ENDPOINTS GPT-OSS-20B
# ============================================
@app.route('/health', methods=['GET'])
def health():
    """Health check del servidor integrado"""
    try:
        # Verificar conexión con la VM
        response = requests.get(GPTOSS_HEALTH_URL, timeout=5)
        vm_status = response.json() if response.ok else {'error': 'VM no disponible'}
        
        return jsonify({
            'status': 'ok',
            'server': 'Capibara6 Integrated Server',
            'components': {
                'gpt_oss_proxy': '✅ Activo',
                'smart_mcp': '✅ Activo', 
                'coqui_tts': '✅ Activo'
            },
            'vm_status': vm_status,
            'timestamp': datetime.now().isoformat()
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'server': 'Capibara6 Integrated Server',
            'vm_status': {'error': f'No se puede conectar con la VM: {str(e)}'},
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_proxy():
    """Proxy para las peticiones de chat con Smart MCP, Semantic Router y soporte TOON"""

    # Manejar preflight OPTIONS
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        # Detectar formato de entrada (JSON o TOON)
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        accept_format = request.headers.get('Accept', 'application/json').lower()

        # Determinar formato de salida preferido
        output_format = 'json'
        if TOON_AVAILABLE and ('toon' in accept_format or 'text/plain' in accept_format):
            output_format = 'toon'

        # Decodificar datos de entrada
        if TOON_AVAILABLE and ('toon' in content_type or 'text/plain' in content_type):
            # Entrada en TOON
            toon_content = request.get_data(as_text=True)
            data = FormatManager.decode(toon_content, 'toon')
        else:
            # Entrada en JSON
            data = request.get_json()

        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        message = data.get('message', '')
        use_semantic_router = data.get('use_semantic_router', True)  # Por defecto activado

        print(f"📨 Mensaje recibido: {message[:50]}...")

        # 🧠 SMART MCP: Analizar y mejorar el mensaje con contexto
        enhanced_message = enhance_message_with_context(message)

        if enhanced_message != message:
            print(f"🧠 Contexto MCP añadido: {enhanced_message[:100]}...")

        # 🎯 SEMANTIC ROUTER: Seleccionar modelo óptimo
        routing_info = None
        selected_model_id = None
        model_url = GPTOSS_API_URL  # URL por defecto

        if SEMANTIC_ROUTER_ENABLED and use_semantic_router:
            try:
                router = get_router()
                routing_decision = router.select_model(message)
                selected_model_id = routing_decision['model_id']
                routing_info = routing_decision

                print(f"🎯 Semantic Router:")
                print(f"   Consulta: {message[:50]}...")
                print(f"   Ruta: {routing_decision['route_name']}")
                print(f"   Modelo: {selected_model_id}")
                print(f"   Confianza: {routing_decision['confidence']:.1%}")
                print(f"   Razón: {routing_decision['reasoning']}")

                # Obtener configuración del modelo seleccionado
                if MODELS_CONFIG_AVAILABLE:
                    model_config = get_model_config(selected_model_id)
                    if model_config:
                        model_url = model_config['server_url']
                        print(f"   URL: {model_url}")
                    else:
                        print(f"⚠️ Modelo {selected_model_id} no configurado, usando por defecto")
                        model_url = GPTOSS_API_URL
                        selected_model_id = "gpt-oss-20b"

            except Exception as e:
                print(f"⚠️ Error en Semantic Router: {e}")
                print("   Usando modelo por defecto")
                selected_model_id = "gpt-oss-20b"
                model_url = GPTOSS_API_URL
        else:
            # Sin semantic router, usar lógica antigua
            category = "general"
            if any(word in message.lower() for word in ["código", "programar", "python", "javascript", "html", "css"]):
                category = "programming"
            elif any(word in message.lower() for word in ["escribir", "historia", "cuento", "poema", "creativo"]):
                category = "creative_writing"
            elif len(message.split()) < 10:
                category = "quick_questions"

            selected_model_id = "gpt-oss-20b"
            model_url = GPTOSS_API_URL

        # 🚀 Crear payload optimizado
        context = enhanced_message if enhanced_message != message else None

        # Usar configuración del modelo si está disponible
        if MODELS_CONFIG_AVAILABLE and selected_model_id:
            model_config = get_model_config(selected_model_id)
            if model_config and 'parameters' in model_config:
                payload = {
                    'prompt': enhanced_message,
                    **model_config['parameters']
                }
            else:
                # Fallback a configuración antigua
                payload = get_category_payload(message, "general", context)
        else:
            # Fallback a configuración antigua
            category = "general"
            payload = get_category_payload(message, category, context)

        # Añadir parámetros personalizados del cliente
        if 'max_tokens' in data:
            payload['n_predict'] = data['max_tokens']
        if 'temperature' in data:
            payload['temperature'] = data['temperature']

        # Reenviar petición al modelo
        print(f"📡 Enviando request a: {model_url}")
        response = requests.post(
            model_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )

        if response.ok:
            response_data = response.json()
            # Convertir respuesta al formato esperado
            result = {
                "response": response_data.get('content', 'Sin respuesta'),
                "model": selected_model_id or "gpt-oss-20b",
                "tokens": response_data.get('tokens_predicted', 0),
            }

            # Agregar información de routing si está disponible
            if routing_info:
                result["routing_info"] = routing_info

            print(f"✅ Respuesta exitosa ({result['model']}): {result.get('response', '')[:50]}...")

            # Retornar en el formato solicitado
            if output_format == 'toon' and TOON_AVAILABLE:
                content, fmt = FormatManager.encode(result, preferred_format='toon')
                return Response(content, mimetype='application/toon')
            else:
                return jsonify(result)
        else:
            print(f"❌ Error del modelo: {response.status_code}")
            return jsonify({
                'error': f'Error del modelo: {response.status_code}',
                'details': response.text
            }), response.status_code

    except requests.exceptions.Timeout:
        print("⏰ Timeout en la petición")
        return jsonify({'error': 'Timeout: El modelo tardó demasiado en responder'}), 504
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502
    except Exception as e:
        print(f"❌ Error interno del servidor: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/models', methods=['GET'])
def models():
    """Información de modelos disponibles"""
    return jsonify({
        'models': [{
            'id': 'gpt-oss-20b',
            'name': 'GPT-OSS-20B',
            'description': 'Modelo de 20B parámetros ejecutándose en Google Cloud VM',
            'features': ['Smart MCP Context', 'Multilingual', 'High Performance']
        }]
    })

# ============================================
# ENDPOINTS MCP
# ============================================
@app.route('/api/mcp/analyze', methods=['POST'])
def mcp_analyze():
    """Analizar mensaje para contexto MCP"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        context = analyze_message_for_context(message)
        
        return jsonify({
            'needs_context': context is not None,
            'context': context,
            'enhanced_message': enhance_message_with_context(message)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/context', methods=['GET'])
def mcp_context():
    """Obtener información de contexto disponible"""
    return jsonify({
        'knowledge_base': KNOWLEDGE_BASE,
        'triggers': list(CONTEXT_TRIGGERS.keys()),
        'status': 'active'
    })

# ============================================
# ENDPOINTS TTS
# ============================================
@app.route('/api/tts/voices', methods=['GET'])
def tts_voices():
    """Obtener voces disponibles"""
    return jsonify({
        'voices': PREDEFINED_VOICES,
        'config': COQUI_CONFIG,
        'status': 'active'
    })

@app.route('/api/tts/speak', methods=['POST'])
def tts_speak():
    """Generar audio TTS (simulado - requiere instalación de Coqui)"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'sofia')
        
        if not text:
            return jsonify({'error': 'No se proporcionó texto'}), 400
        
        if voice not in PREDEFINED_VOICES:
            return jsonify({'error': 'Voz no encontrada'}), 400
        
        # Generar audio WAV simple (tono de prueba)
        import numpy as np
        from scipy.io.wavfile import write
        import io
        
        # Crear un tono simple como audio de prueba
        sample_rate = 24000
        duration = min(len(text) / 15, 10)  # Duración basada en longitud del texto (máx 10 seg)
        frequency = 440  # Tono de 440 Hz
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        amplitude = 0.3  # Volumen moderado
        audio_data = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Convertir a 16-bit
        audio_data_16bit = (audio_data * 32767).astype(np.int16)
        
        # Crear archivo WAV en memoria
        wav_buffer = io.BytesIO()
        write(wav_buffer, sample_rate, audio_data_16bit)
        wav_buffer.seek(0)
        
        return send_file(
            io.BytesIO(wav_buffer.read()),
            mimetype='audio/wav',
            as_attachment=False,
            download_name='speech.wav'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tts/clone', methods=['POST'])
def tts_clone():
    """Clonar voz desde audio (simulado)"""
    try:
        data = request.get_json()
        audio_data = data.get('audio_data', '')
        voice_name = data.get('voice_name', 'cloned_voice')

        if not audio_data:
            return jsonify({'error': 'No se proporcionó audio'}), 400

        # Simular clonación de voz
        return jsonify({
            'status': 'success',
            'message': 'Voz clonada correctamente',
            'voice_name': voice_name,
            'note': 'Clonación de voz requiere instalación de Coqui XTTS v2'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ENDPOINTS SEMANTIC ROUTER
# ============================================

@app.route('/api/router/info', methods=['GET'])
def router_info():
    """Información sobre el Semantic Router"""
    if not SEMANTIC_ROUTER_ENABLED:
        return jsonify({
            'enabled': False,
            'error': 'Semantic Router no disponible',
            'install_command': 'pip install semantic-router'
        }), 503

    try:
        router = get_router()
        return jsonify({
            'enabled': True,
            'routes': router.get_available_routes(),
            'model_mapping': router.get_model_mapping(),
            'encoder': 'FastEmbed (local)',
            'status': 'active',
            'models_configured': len(router.get_model_mapping())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/router/test', methods=['POST'])
def router_test():
    """Prueba el router sin hacer consulta al modelo real"""
    if not SEMANTIC_ROUTER_ENABLED:
        return jsonify({
            'enabled': False,
            'error': 'Semantic Router no disponible'
        }), 503

    try:
        data = request.get_json()
        query = data.get('query', '')

        if not query:
            return jsonify({'error': 'Query requerido'}), 400

        router = get_router()
        test_result = router.test_query(query)

        return jsonify(test_result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/router/routes', methods=['GET'])
def router_routes():
    """Obtiene todas las rutas disponibles con detalles"""
    if not SEMANTIC_ROUTER_ENABLED:
        return jsonify({
            'enabled': False,
            'error': 'Semantic Router no disponible'
        }), 503

    try:
        router = get_router()
        routes_info = []

        for route_name in router.get_available_routes():
            route_details = router.get_route_info(route_name)
            if route_details:
                routes_info.append(route_details)

        return jsonify({
            'routes': routes_info,
            'total': len(routes_info)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/router/models', methods=['GET'])
def router_models():
    """Lista todos los modelos disponibles con su configuración"""
    if not MODELS_CONFIG_AVAILABLE:
        return jsonify({
            'error': 'Configuración de modelos no disponible'
        }), 503

    try:
        models_info = []
        for model_id, config in MODELS_CONFIG.items():
            models_info.append({
                'id': model_id,
                'name': config.get('name', model_id),
                'base_model': config.get('base_model', 'unknown'),
                'hardware': config.get('hardware', 'unknown'),
                'status': config.get('status', 'unknown'),
                'server_url': config.get('server_url', 'unknown')
            })

        return jsonify({
            'models': models_info,
            'total': len(models_info)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ENDPOINTS TOON
# ============================================

@app.route('/api/toon/info', methods=['GET'])
def toon_info():
    """Información sobre el soporte TOON"""
    if not TOON_AVAILABLE:
        return jsonify({
            'enabled': False,
            'error': 'TOON Format Manager no disponible',
            'install_command': 'Módulo integrado en backend/toon_utils'
        }), 503

    return jsonify({
        'enabled': True,
        'version': '1.0.0',
        'formats_supported': ['json', 'toon'],
        'min_array_size': 5,
        'min_savings_percent': 20,
        'content_types': {
            'toon': 'application/toon',
            'json': 'application/json'
        },
        'status': 'active'
    })

@app.route('/api/toon/analyze', methods=['POST'])
def toon_analyze():
    """Analiza datos y retorna estadísticas de eficiencia TOON vs JSON"""
    if not TOON_AVAILABLE:
        return jsonify({
            'enabled': False,
            'error': 'TOON Format Manager no disponible'
        }), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        # Analizar eficiencia
        stats = FormatManager.analyze_data(data)

        return jsonify({
            'analysis': stats,
            'recommendation': {
                'use_toon': stats['toon_recommended'],
                'reason': f"TOON ahorra {stats['savings_percent']:.1f}% de espacio" if stats['toon_recommended']
                         else "JSON es más eficiente para estos datos"
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/toon/convert', methods=['POST'])
def toon_convert():
    """Convierte entre formatos JSON y TOON"""
    if not TOON_AVAILABLE:
        return jsonify({
            'enabled': False,
            'error': 'TOON Format Manager no disponible'
        }), 503

    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        target_format = request.args.get('target', 'toon')  # 'json' o 'toon'

        # Obtener datos
        if 'toon' in content_type or 'text/plain' in content_type:
            source_format = 'toon'
            content = request.get_data(as_text=True)
            data = FormatManager.decode(content, source_format)
        else:
            source_format = 'json'
            data = request.get_json()

        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        # Convertir
        result_content, result_format = FormatManager.encode(data, preferred_format=target_format)

        # Retornar en formato solicitado
        if target_format == 'toon':
            return Response(result_content, mimetype='application/toon')
        else:
            return Response(result_content, mimetype='application/json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/toon/example', methods=['GET'])
def toon_example():
    """Retorna ejemplo de uso de TOON"""
    example_data = {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin", "active": True},
            {"id": 2, "name": "Bob", "role": "user", "active": True},
            {"id": 3, "name": "Charlie", "role": "user", "active": False}
        ]
    }

    if TOON_AVAILABLE:
        # Generar versiones JSON y TOON
        import json
        json_version = json.dumps(example_data, indent=2)
        toon_version, _ = FormatManager.encode(example_data, 'toon')

        stats = FormatManager.analyze_data(example_data)

        return jsonify({
            'example_data': example_data,
            'json_format': json_version,
            'toon_format': toon_version,
            'stats': stats,
            'usage': {
                'description': 'Enviar datos en TOON usando Content-Type: application/toon',
                'curl_example_json_to_toon': 'curl -X POST http://localhost:5001/api/toon/convert?target=toon -H "Content-Type: application/json" -d \'{"users":[...]}\'',
                'curl_example_toon_to_json': 'curl -X POST http://localhost:5001/api/toon/convert?target=json -H "Content-Type: application/toon" -d \'users[3]{id,name,role,active}: 1,Alice,admin,true ...\''
            }
        })
    else:
        return jsonify({
            'error': 'TOON not available',
            'example_data': example_data
        })

if __name__ == '__main__':
    print('=' * 60)
    print('🚀 Iniciando Servidor Integrado Capibara6...')
    print('=' * 60)
    print(f'📡 VM GPT-OSS-20B: {GPTOSS_API_URL}')
    print('🧠 Smart MCP: Activo')
    print('🎵 Coqui TTS: Activo')
    print(f'🎯 Semantic Router: {"✅ Activo" if SEMANTIC_ROUTER_ENABLED else "⚠️ No disponible"}')
    print(f'🤖 Models Config: {"✅ Activo" if MODELS_CONFIG_AVAILABLE else "⚠️ No disponible"}')
    print(f'📊 TOON Format: {"✅ Activo" if TOON_AVAILABLE else "⚠️ No disponible"}')
    print('🌐 Puerto: 5001')
    print('🔧 CORS habilitado para *')

    # Verificar conexión con la VM al inicio
    try:
        response = requests.get(GPTOSS_HEALTH_URL, timeout=5)
        if response.ok:
            print('✅ Conexión con VM GPT-OSS-20B: OK')
        else:
            print('⚠️ Advertencia: VM no responde correctamente')
    except requests.exceptions.RequestException as e:
        print(f'⚠️ Advertencia: No se puede conectar con la VM: {e}')

    # Mostrar información de Semantic Router
    if SEMANTIC_ROUTER_ENABLED:
        try:
            router = get_router()
            routes = router.get_available_routes()
            models = router.get_model_mapping()
            print(f'\n📋 Semantic Router configurado:')
            print(f'   • Rutas: {len(routes)} ({", ".join(routes[:5])}...)')
            print(f'   • Modelos: {len(models)}')
        except Exception as e:
            print(f'⚠️ Error inicializando router: {e}')

    print('\n📝 Endpoints disponibles:')
    print('   • POST /api/chat - Chat con selección automática de modelo (soporta TOON)')
    print('   • GET  /api/router/info - Info del Semantic Router')
    print('   • POST /api/router/test - Probar routing sin llamar modelo')
    print('   • GET  /api/router/routes - Ver todas las rutas')
    print('   • GET  /api/router/models - Ver todos los modelos')
    print('   • GET  /api/toon/info - Info del formato TOON')
    print('   • POST /api/toon/analyze - Analizar eficiencia TOON vs JSON')
    print('   • POST /api/toon/convert - Convertir entre JSON y TOON')
    print('   • GET  /api/toon/example - Ver ejemplo de uso TOON')
    print('   • GET  /health - Health check')

    print('=' * 60)
    print('🦫 Servidor Integrado iniciado correctamente')
    print('=' * 60)
    app.run(host='0.0.0.0', port=5001, debug=False)
>>>>>>> 6569617 (new files)
