#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de capibara6 - Servidor Flask para conectar con vLLM
"""

from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import requests
import json
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Configuración de vLLM
VLLM_URL = os.getenv('VLLM_URL', 'http://34.12.166.76:8000/v1')  # vLLM endpoint
VLLM_MODEL = os.getenv('VLLM_MODEL', 'gpt-oss-20b')
VLLM_TIMEOUT = int(os.getenv('VLLM_TIMEOUT', '120'))

# Backwards compatibility: si existe OLLAMA_URL, usarlo como VLLM_URL para migración
if os.getenv('OLLAMA_URL'):
    VLLM_URL = os.getenv('OLLAMA_URL').replace('/api/generate', '/v1/chat/completions').replace(':11434', ':8000/v1')
if os.getenv('GPT_OSS_URL'):
    # Si hay una URL específica de GPT-OSS, adaptarla a vLLM
    original_url = os.getenv('GPT_OSS_URL')
    if ':8080' in original_url:
        VLLM_URL = original_url.replace(':8080', ':8000/v1')
    else:
        VLLM_URL = original_url + '/v1/chat/completions'

# Archivo para guardar datos
DATA_FILE = 'user_data/conversations.json'
UPLOAD_FOLDER = 'user_data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'csv', 'xlsx', 'xls', 'pptx', 'ppt', 'zip', 'rar'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def ensure_data_dir():
    """Crear directorio de datos si no existe"""
    os.makedirs('user_data', exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_conversation(user_message, ai_response, user_email=None):
    """Guardar conversación en archivo JSON"""
    ensure_data_dir()
    
    # Leer datos existentes
    existing_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
    
    # Agregar nueva conversación
    conversation = {
        'timestamp': datetime.now().isoformat(),
        'user_message': user_message,
        'ai_response': ai_response,
        'user_email': user_email,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent')
    }
    
    existing_data.append(conversation)
    
    # Guardar
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

def call_vllm(prompt, max_tokens=500, temperature=0.7):
    """Llamar al modelo a través de vLLM"""

    # Modo demo: si la variable de entorno USE_DEMO_MODE está activa
    use_demo = os.getenv('USE_DEMO_MODE', 'false').lower() == 'true'

    if use_demo:
        print("⚠️ MODO DEMO: Generando respuesta simulada")
        return """¡Hola! Soy Capibara6 en modo demo.

El backend está funcionando correctamente, pero vLLM no está accesible en este momento.

Para activar el modelo real:
1. Verifica que vLLM esté corriendo en la VM
2. Asegúrate de que el puerto 8000 esté abierto para vLLM endpoints
3. Configura el archivo .env con la URL correcta de vLLM
4. Desactiva el modo demo quitando USE_DEMO_MODE=true del .env

Esta es una respuesta simulada para probar la funcionalidad del chat. Todas las demás características (subida de archivos, guardado de conversaciones, UI) están funcionando correctamente."""

    try:
        # Preparar el payload para vLLM OpenAI-compatible API
        payload = {
            "model": VLLM_MODEL,
            "messages": [
                {"role": "system", "content": "Eres Capibara6, un asistente de IA útil y preciso."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stream": False
        }

        # Llamar a vLLM API (OpenAI-compatible endpoint)
        response = requests.post(
            f"{VLLM_URL}/chat/completions",
            json=payload,
            timeout=VLLM_TIMEOUT,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer EMPTY'  # vLLM típicamente no requiere auth
            }
        )

        if response.status_code == 200:
            data = response.json()
            # vLLM devuelve la respuesta en el campo choices[0].message.content
            response_text = data.get('choices', [{}])[0].get('message', {}).get('content', '')

            return response_text.strip()
        else:
            print(f"Error en vLLM: {response.status_code} - {response.text}")
            return f"Error: No se pudo conectar con vLLM ({response.status_code}). Verifica que esté corriendo en {VLLM_URL}"

    except requests.exceptions.Timeout:
        return f"Error: Tiempo de espera agotado. vLLM ({VLLM_URL}) está tardando demasiado en responder."
    except requests.exceptions.ConnectionError:
        return f"Error: No se pudo conectar con vLLM en {VLLM_URL}. Verifica que esté corriendo y que el puerto correspondiente esté abierto."
    except Exception as e:
        print(f"Error llamando a vLLM: {e}")
        return f"Error: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal para chat con GPT-OSS-20B con soporte para archivos"""
    try:
        # Verificar si es multipart/form-data (con archivos) o JSON
        files_info = []

        if request.content_type and 'multipart/form-data' in request.content_type:
            # Procesar archivos si hay
            if 'files' in request.files:
                files = request.files.getlist('files')
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_filename = f"{timestamp}_{filename}"
                        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                        file.save(filepath)

                        files_info.append({
                            'name': filename,
                            'size': os.path.getsize(filepath),
                            'path': filepath
                        })

            # Obtener datos del formulario
            user_message = request.form.get('message', '').strip()
            user_email = request.form.get('email', '')
            max_tokens = int(request.form.get('max_tokens', 500))
            temperature = float(request.form.get('temperature', 0.7))
        else:
            # Procesar JSON tradicional
            data = request.get_json()
            user_message = data.get('message', '').strip()
            user_email = data.get('email', '')
            max_tokens = data.get('max_tokens', 500)
            temperature = data.get('temperature', 0.7)

        if not user_message:
            return jsonify({'error': 'Mensaje requerido'}), 400

        # Si hay archivos, agregar información al mensaje
        if files_info:
            files_summary = "\n\n[El usuario ha adjuntado los siguientes archivos: " + ", ".join([f['name'] for f in files_info]) + "]"
            user_message_with_files = user_message + files_summary
        else:
            user_message_with_files = user_message
        
        # Crear prompt mejorado y optimizado
        system_prompt = """Eres Capibara6, un asistente de IA especializado en tecnología, programación e inteligencia artificial desarrollado por Anachroni s.coop.

INSTRUCCIONES CRÍTICAS:
- Responde SIEMPRE en español
- Sé específico y detallado en tus respuestas (mínimo 50 palabras)
- Evita respuestas genéricas como "soy un modelo de IA"
- Proporciona información útil y práctica
- Mantén un tono profesional pero amigable
- Si no sabes algo, admítelo honestamente
- Incluye ejemplos cuando sea apropiado

Tu personalidad es profesional pero cercana, y siempre intentas ayudar de la mejor manera posible."""
        
        full_prompt = f"{system_prompt}\n\nUsuario: {user_message_with_files}\n\nCapibara6:"

        # Llamar al modelo a través de vLLM
        ai_response = call_vllm(full_prompt, max_tokens, temperature)

        # Guardar conversación
        save_conversation(user_message, ai_response, user_email)

        response_data = {
            'response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'model': 'gpt-oss-20b'
        }

        # Agregar información de archivos si los hay
        if files_info:
            response_data['files'] = files_info

        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Endpoint para chat con streaming (respuesta en tiempo real)"""
    try:
        data = request.get_json()
        
        user_message = data.get('message', '').strip()
        user_email = data.get('email', '')
        max_tokens = data.get('max_tokens', 500)
        temperature = data.get('temperature', 0.7)
        
        if not user_message:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        # Crear prompt mejorado y optimizado
        system_prompt = """Eres Capibara6, un asistente de IA especializado en tecnología, programación e inteligencia artificial desarrollado por Anachroni s.coop.

INSTRUCCIONES CRÍTICAS:
- Responde SIEMPRE en español
- Sé específico y detallado en tus respuestas (mínimo 50 palabras)
- Evita respuestas genéricas como "soy un modelo de IA"
- Proporciona información útil y práctica
- Mantén un tono profesional pero amigable
- Si no sabes algo, admítelo honestamente
- Incluye ejemplos cuando sea apropiado

Tu personalidad es profesional pero cercana, y siempre intentas ayudar de la mejor manera posible."""
        
        full_prompt = f"{system_prompt}\n\nUsuario: {user_message}\n\nCapibara6:"
        
        def generate():
            try:
                payload = {
                    "model": VLLM_MODEL,
                    "messages": [
                        {"role": "system", "content": "Eres Capibara6, un asistente de IA útil y preciso."},
                        {"role": "user", "content": full_prompt}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "stream": True
                }
                
                response = requests.post(
                    f"{VLLM_URL}/chat/completions",
                    json=payload,
                    timeout=VLLM_TIMEOUT,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer EMPTY'
                    },
                    stream=True
                )
                
                if response.status_code == 200:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8').strip()
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]  # Remove 'data: ' prefix
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data = json.loads(data_str)
                                    if data.get('choices') and data['choices'][0].get('delta', {}).get('content'):
                                        content = data['choices'][0]['delta']['content']
                                        full_response += content
                                        yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
                                except json.JSONDecodeError:
                                    continue

                    # Guardar conversación completa
                    save_conversation(user_message, full_response, user_email)

                    # Enviar señal de finalización
                    yield f"data: {json.dumps({'content': '', 'done': True, 'full_response': full_response})}\n\n"
                else:
                    error_msg = f"Error: No se pudo conectar con el modelo vLLM ({response.status_code})"
                    yield f"data: {json.dumps({'error': error_msg, 'done': True})}\n\n"
                    
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'error': error_msg, 'done': True})}\n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/plain')
    
    except Exception as e:
        print(f"Error en chat stream: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    try:
        # Verificar conexión con vLLM
        response = requests.get(f"{VLLM_URL}/models", timeout=5)
        vllm_status = "ok" if response.status_code == 200 else "error"
    except:
        vllm_status = "error"

    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'vllm_status': vllm_status,
        'vllm_url': VLLM_URL,
        'vllm_model': VLLM_MODEL
    })

@app.route('/api/models', methods=['GET'])
def models():
    """Endpoint para obtener información de los modelos disponibles en vLLM"""
    try:
        # Intentar obtener modelos desde vLLM
        response = requests.get(f"{VLLM_URL}/models", timeout=5)
        if response.status_code == 200:
            vllm_models = response.json().get('data', [])
            return jsonify({
                'models': vllm_models,
                'current_model': VLLM_MODEL,
                'source': 'vllm'
            })
    except Exception as e:
        print(f"Error obteniendo modelos de vLLM: {e}")

    # Fallback: devolver modelo configurado
    return jsonify({
        'models': [{
            'name': VLLM_MODEL,
            'description': f'Modelo configurado en vLLM: {VLLM_MODEL}',
            'source': 'config'
        }],
        'current_model': VLLM_MODEL
    })

@app.route('/api/save-conversation', methods=['POST'])
def save_conversation_endpoint():
    """Endpoint para guardar conversación manualmente"""
    try:
        data = request.get_json()
        
        user_message = data.get('message', '')
        ai_response = data.get('response', '')
        user_email = data.get('email', '')
        
        if not user_message or not ai_response:
            return jsonify({'error': 'Mensaje y respuesta requeridos'}), 400
        
        save_conversation(user_message, ai_response, user_email)
        
        return jsonify({'success': True, 'message': 'Conversación guardada'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return '''
    <html>
        <head>
            <title>capibara6 Backend - GPT-OSS-20B</title>
            <style>
                body { font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 40px; }
                h1 { color: #00ffff; }
                .status { color: #00ff00; }
                .endpoint { color: #ffff00; margin: 10px 0; }
                .model { color: #ff8800; }
            </style>
        </head>
        <body>
            <h1>🦫 capibara6 Backend</h1>
            <p class="status">Servidor funcionando correctamente</p>
            <p class="model">Modelo: ''' + VLLM_MODEL + ''' (via vLLM)</p>
            <p>URL de vLLM: ''' + VLLM_URL + '''</p>
            <p>Endpoints disponibles:</p>
            <ul>
                <li class="endpoint">POST /api/chat - Chat con modelo via vLLM</li>
                <li class="endpoint">POST /api/chat/stream - Chat con streaming</li>
                <li class="endpoint">GET /api/health - Health check</li>
                <li class="endpoint">GET /api/models - Listar modelos disponibles en vLLM</li>
                <li class="endpoint">POST /api/save-conversation - Guardar conversación</li>
            </ul>
        </body>
    </html>
    '''

if __name__ == '__main__':
    ensure_data_dir()
    print('🦫 capibara6 Backend iniciado')
    print(f'🤖 Modelo: {VLLM_MODEL}')
    print(f'🌐 URL de vLLM: {VLLM_URL}')

    # Puerto 5001 para desarrollo local (el frontend espera este puerto)
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
