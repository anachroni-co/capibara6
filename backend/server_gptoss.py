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

# Configuración de la VM GPT-OSS-20B
GPT_OSS_URL = os.getenv('GPT_OSS_URL', 'http://34.175.215.109:8080')
GPT_OSS_TIMEOUT = int(os.getenv('GPT_OSS_TIMEOUT', '60'))

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

def call_gpt_oss(prompt, max_tokens=500, temperature=0.7):
    """Llamar al modelo GPT-OSS-20B (con modo demo si no está disponible)"""

    # Modo demo: si la variable de entorno USE_DEMO_MODE está activa
    use_demo = os.getenv('USE_DEMO_MODE', 'false').lower() == 'true'

    if use_demo:
        print("⚠️ MODO DEMO: Generando respuesta simulada")
        return """¡Hola! Soy Capibara6 en modo demo.

El backend está funcionando correctamente, pero el modelo GPT-OSS-20B no está accesible en este momento.

Para activar el modelo real:
1. Verifica que las VMs de Google Cloud estén encendidas
2. Asegúrate de que los puertos estén abiertos en el firewall
3. Configura el archivo .env con las IPs correctas
4. Desactiva el modo demo quitando USE_DEMO_MODE=true del .env

Esta es una respuesta simulada para probar la funcionalidad del chat. Todas las demás características (subida de archivos, guardado de conversaciones, UI) están funcionando correctamente."""

    try:
        payload = {
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "stream": False,
            "stop": ["Usuario:", "Capibara6:", "\n\n", "<|endoftext|>", "</s>", "<|end|>"]
        }

        response = requests.post(
            f"{GPT_OSS_URL}/completion",
            json=payload,
            timeout=GPT_OSS_TIMEOUT,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('content', '').strip()
        else:
            print(f"Error en GPT-OSS: {response.status_code} - {response.text}")
            return f"Error: No se pudo conectar con el modelo ({response.status_code}). Activa el modo demo con USE_DEMO_MODE=true en el .env para probar la interfaz."

    except requests.exceptions.Timeout:
        return "Error: Tiempo de espera agotado. El modelo está procesando una petición muy larga. Activa el modo demo con USE_DEMO_MODE=true en el .env para probar la interfaz."
    except requests.exceptions.ConnectionError:
        return "Error: No se pudo conectar con el modelo GPT-OSS-20B. Verifica que esté funcionando o activa el modo demo con USE_DEMO_MODE=true en el .env."
    except Exception as e:
        print(f"Error llamando a GPT-OSS: {e}")
        return f"Error: {str(e)}. Activa el modo demo con USE_DEMO_MODE=true en el .env para probar la interfaz."

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

        # Llamar al modelo
        ai_response = call_gpt_oss(full_prompt, max_tokens, temperature)

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
        # Verificar conexión con GPT-OSS
        response = requests.get(f"{GPT_OSS_URL}/health", timeout=5)
        gpt_oss_status = "ok" if response.status_code == 200 else "error"
    except:
        gpt_oss_status = "error"
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'gpt_oss_status': gpt_oss_status,
        'gpt_oss_url': GPT_OSS_URL
    })

@app.route('/api/models', methods=['GET'])
def models():
    """Endpoint para obtener información del modelo"""
    return jsonify({
        'models': [{
            'id': 'gpt-oss-20b',
            'name': 'GPT-OSS-20B',
            'description': 'Modelo de lenguaje de código abierto de 20B parámetros',
            'max_tokens': 4096,
            'temperature_range': [0.1, 2.0]
        }]
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
            <p class="model">Modelo: GPT-OSS-20B</p>
            <p>URL del modelo: ''' + GPT_OSS_URL + '''</p>
            <p>Endpoints disponibles:</p>
            <ul>
                <li class="endpoint">POST /api/chat - Chat con GPT-OSS-20B</li>
                <li class="endpoint">POST /api/chat/stream - Chat con streaming</li>
                <li class="endpoint">GET /api/health - Health check</li>
                <li class="endpoint">GET /api/models - Información del modelo</li>
                <li class="endpoint">POST /api/save-conversation - Guardar conversación</li>
            </ul>
        </body>
    </html>
    '''

if __name__ == '__main__':
    ensure_data_dir()
    print('🦫 capibara6 Backend iniciado')
    print(f'🤖 Modelo: GPT-OSS-20B')
    print(f'🌐 URL del modelo: {GPT_OSS_URL}')
    
    # Puerto 5001 para desarrollo local (el frontend espera este puerto)
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
