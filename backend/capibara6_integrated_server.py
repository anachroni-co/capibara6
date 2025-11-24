# capibara6_integrated_server.py
# Servidor integrado principal para el proyecto Capibara6

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from models_config import MODEL_CONFIGS, DEFAULT_MODEL, TIMEOUT
from toon_utils.format_manager_ultra_optimized import FormatManagerUltraOptimized
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

# Configurar CORS - solo para peticiones directas (no desde proxy)
# El proxy maneja CORS, así que el backend no debe añadir headers duplicados
# NOTA: flask_cors añade headers automáticamente, pero el proxy los elimina antes de enviar al frontend
CORS(app, 
     origins=[
         "http://localhost:8000",
         "http://127.0.0.1:8000",
         "http://localhost:3000",
         "http://127.0.0.1:3000",
         "http://localhost:8080",
         "http://127.0.0.1:8080",
         "http://localhost:8001",  # Proxy CORS local
         "http://127.0.0.1:8001",   # Proxy CORS local
         "https://www.capibara6.com",
         "https://capibara6.com",
         "http://34.12.166.76:5001",
         "http://34.12.166.76:8000",
         "http://34.175.136.104:8000"
     ],
     supports_credentials=True,
     allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'Origin', 'X-Requested-With'],
     expose_headers=['Content-Type', 'Content-Length'],
     max_age=3600)

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
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()
        
        model_config = MODEL_CONFIGS.get('gpt_oss_20b')
        
        if not model_config:
            error_response = {'error': 'Modelo GPT-OSS-20B no configurado'}
            
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(model_response, 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        error_response = {'error': 'Error interno del servidor'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(analysis_result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(analysis_result)
            
    except Exception as e:
        logger.error(f"Error en MCP integrado: {e}")
        error_response = {'error': 'Error en el análisis MCP integrado'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error en TTS: {e}")
        error_response = {'error': 'Error en el servicio TTS'}
        
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()

        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()

        prompt = input_data.get('prompt', '')
        context = input_data.get('context', '')
        
        if not prompt:
            error_response = {'error': 'Prompt es requerido'}
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)

    except Exception as e:
        logger.error(f"Error en e2b_process: {e}")
        error_response = {'error': f'Error en el procesamiento e2b: {str(e)}'}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
            return Response(content, mimetype='text/plain', status=500)
        else:
            return jsonify(error_response), 500
    
    try:
        # Determinar formato de entrada
        content_type = request.headers.get('Content-Type', 'application/json').lower()
        preferred_output_format = request.headers.get('Accept', 'application/json').lower()

        if 'application/toon' in content_type or 'text/plain' in content_type:
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
        else:
            input_data = request.get_json()

        prompt = input_data.get('prompt', '')
        
        if not prompt:
            error_response = {'error': 'Prompt es requerido'}
            if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
                content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
                return Response(content, mimetype='text/plain', status=400)
            else:
                return jsonify(error_response), 400

        # Usar la integración de e2b para estimar recursos
        resources = e2b_integration.estimate_task_resources(prompt)

        # Determinar formato de salida
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(resources, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(resources)

    except Exception as e:
        logger.error(f"Error en e2b_estimate: {e}")
        error_response = {'error': f'Error en la estimación de recursos e2b: {str(e)}'}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
            input_data = FormatManagerUltraOptimized.decode(request.get_data(as_text=True), 'toon')
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
            content, format_type = FormatManagerUltraOptimized.encode(result, 'toon')
            return Response(content, mimetype='text/plain')
        else:
            return jsonify(result)

    except Exception as e:
        logger.error(f"Error en ai_generate_ctm: {e}")
        error_response = {'error': f'Error al generar respuesta: {str(e)}', 'success': False}

        preferred_output_format = request.headers.get('Accept', 'application/json').lower()
        if 'toon' in preferred_output_format or 'text/plain' in preferred_output_format:
            content, format_type = FormatManagerUltraOptimized.encode(error_response, 'toon')
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
