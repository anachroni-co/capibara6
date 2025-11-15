#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de capibara6 - Servidor Flask para conectar con GPT-OSS-20B
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

# Configuración de Ollama
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://34.12.166.76:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gpt-oss-20b')
OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '120'))

# Backwards compatibility: si existe GPT_OSS_URL, usarlo como OLLAMA_URL
if os.getenv('GPT_OSS_URL'):
    OLLAMA_URL = os.getenv('GPT_OSS_URL')
    # Si la URL tiene :8080, cambiar a :11434 (puerto por defecto de Ollama)
    if ':8080' in OLLAMA_URL:
        OLLAMA_URL = OLLAMA_URL.replace(':8080', ':11434')

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

def call_ollama(prompt, max_tokens=500, temperature=0.7):
    """Llamar al modelo a través de Ollama"""

    # Modo demo: si la variable de entorno USE_DEMO_MODE está activa
    use_demo = os.getenv('USE_DEMO_MODE', 'false').lower() == 'true'

    if use_demo:
        print("⚠️ MODO DEMO: Generando respuesta simulada")
        return """¡Hola! Soy Capibara6 en modo demo.

El backend está funcionando correctamente, pero Ollama no está accesible en este momento.

Para activar el modelo real:
1. Verifica que Ollama esté corriendo en la VM
2. Asegúrate de que el puerto 11434 esté abierto
3. Configura el archivo .env con la URL correcta de Ollama
4. Desactiva el modo demo quitando USE_DEMO_MODE=true del .env

Esta es una respuesta simulada para probar la funcionalidad del chat. Todas las demás características (subida de archivos, guardado de conversaciones, UI) están funcionando correctamente."""

    try:
        # Preparar el payload para Ollama API
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "stop": ["Usuario:", "Capibara6:", "\n\n"]
            }
        }

        # Llamar a Ollama API
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=OLLAMA_TIMEOUT,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            data = response.json()
            # Ollama devuelve la respuesta en el campo 'response', pero para GPT-OSS-20B puede estar en 'thinking' o combinado
            response_text = data.get('response', '')
            
            # Si el campo 'response' está vacío, intentar extraer de 'thinking'
            if not response_text and 'thinking' in data:
                thinking = data.get('thinking', '')
                if thinking:
                    # Estrategia de extracción para GPT-OSS-20B
                    # Buscar patrones comunes en el contenido de thinking
                    import re
                    
                    # Patrón 1: Después de "So respond in Spanish:" o similar
                    patterns = [
                        r'So respond in [^:]*: (.+?)(?:\. |, |\n|$)',
                        r'So (.+?)(?:\. |, |\n|$)',
                        r'The assistant should respond appropriately.*?: (.+?)(?:\. |, |\n|$)',
                        r'should respond in Spanish: (.+?)(?:\. |, |\n|$)',
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, thinking)
                        if match:
                            response_text = match.group(1).strip()
                            break
                    
                    # Si aún no hay respuesta, usar el contenido todo del thinking
                    if not response_text:
                        response_text = thinking[:200]  # Limitar longitud para evitar basura
                        
            return response_text.strip()
        else:
            print(f"Error en Ollama: {response.status_code} - {response.text}")
            return f"Error: No se pudo conectar con Ollama ({response.status_code}). Verifica que esté corriendo en {OLLAMA_URL}"

    except requests.exceptions.Timeout:
        return f"Error: Tiempo de espera agotado. Ollama ({OLLAMA_URL}) está tardando demasiado en responder."
    except requests.exceptions.ConnectionError:
        return f"Error: No se pudo conectar con Ollama en {OLLAMA_URL}. Verifica que esté corriendo y que el puerto 11434 esté abierto."
    except Exception as e:
        print(f"Error llamando a Ollama: {e}")
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

        # Llamar al modelo a través de Ollama
        ai_response = call_ollama(full_prompt, max_tokens, temperature)

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
                    "prompt": full_prompt,
                    "n_predict": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,  # Añadido para mejor diversidad
                    "repeat_penalty": 1.1,  # Reducido para evitar repeticiones excesivas
                    "stream": True,
                    "stop": ["Usuario:", "Capibara6:", "\n\n", "<|endoftext|>", "</s>", "<|end|>"]
                }
                
                response = requests.post(
                    f"{GPT_OSS_URL}/completion",
                    json=payload,
                    timeout=GPT_OSS_TIMEOUT,
                    headers={'Content-Type': 'application/json'},
                    stream=True
                )
                
                if response.status_code == 200:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                content = data.get('content', '')
                                if content:
                                    full_response += content
                                    yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
                            except json.JSONDecodeError:
                                continue
                    
                    # Guardar conversación completa
                    save_conversation(user_message, full_response, user_email)
                    
                    # Enviar señal de finalización
                    yield f"data: {json.dumps({'content': '', 'done': True, 'full_response': full_response})}\n\n"
                else:
                    error_msg = f"Error: No se pudo conectar con el modelo ({response.status_code})"
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
        # Verificar conexión con Ollama
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_status = "ok" if response.status_code == 200 else "error"
    except:
        ollama_status = "error"

    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'ollama_status': ollama_status,
        'ollama_url': OLLAMA_URL,
        'ollama_model': OLLAMA_MODEL
    })

@app.route('/api/models', methods=['GET'])
def models():
    """Endpoint para obtener información de los modelos disponibles en Ollama"""
    try:
        # Intentar obtener modelos desde Ollama
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            ollama_models = response.json().get('models', [])
            return jsonify({
                'models': ollama_models,
                'current_model': OLLAMA_MODEL,
                'source': 'ollama'
            })
    except Exception as e:
        print(f"Error obteniendo modelos de Ollama: {e}")

    # Fallback: devolver modelo configurado
    return jsonify({
        'models': [{
            'name': OLLAMA_MODEL,
            'description': f'Modelo configurado en Ollama: {OLLAMA_MODEL}',
            'source': 'config'
        }],
        'current_model': OLLAMA_MODEL
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
            <p class="model">Modelo: ''' + OLLAMA_MODEL + ''' (via Ollama)</p>
            <p>URL de Ollama: ''' + OLLAMA_URL + '''</p>
            <p>Endpoints disponibles:</p>
            <ul>
                <li class="endpoint">POST /api/chat - Chat con modelo via Ollama</li>
                <li class="endpoint">POST /api/chat/stream - Chat con streaming</li>
                <li class="endpoint">GET /api/health - Health check</li>
                <li class="endpoint">GET /api/models - Listar modelos disponibles en Ollama</li>
                <li class="endpoint">POST /api/save-conversation - Guardar conversación</li>
            </ul>
        </body>
    </html>
    '''

if __name__ == '__main__':
    ensure_data_dir()
    print('🦫 capibara6 Backend iniciado')
    print(f'🤖 Modelo: {OLLAMA_MODEL}')
    print(f'🌐 URL de Ollama: {OLLAMA_URL}')
    
    # Puerto 5001 para desarrollo local (el frontend espera este puerto)
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
