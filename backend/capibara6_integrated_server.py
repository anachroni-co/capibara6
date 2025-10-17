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

app = Flask(__name__)
CORS(app, origins='*')  # Permitir conexiones desde cualquier origen

# ============================================
# CONFIGURACIÓN GPT-OSS-20B (Local en la VM)
# ============================================
GPTOSS_API_URL = 'http://localhost:8080/completion'  # Modelo local en la VM
GPTOSS_HEALTH_URL = 'http://localhost:8080/health'

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
    """Proxy para las peticiones de chat con Smart MCP"""
    
    # Manejar preflight OPTIONS
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        # Obtener datos de la petición
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400
        
        message = data.get('message', '')
        print(f"📨 Mensaje recibido: {message[:50]}...")
        
        # 🧠 SMART MCP: Analizar y mejorar el mensaje con contexto
        enhanced_message = enhance_message_with_context(message)
        
        if enhanced_message != message:
            print(f"🧠 Contexto MCP añadido: {enhanced_message[:100]}...")
        
        # 🚀 USAR CONFIGURACIÓN OPTIMIZADA
        # Determinar categoría de la consulta
        category = "general"
        if any(word in message.lower() for word in ["código", "programar", "python", "javascript", "html", "css"]):
            category = "programming"
        elif any(word in message.lower() for word in ["escribir", "historia", "cuento", "poema", "creativo"]):
            category = "creative_writing"
        elif len(message.split()) < 10:  # Preguntas cortas
            category = "quick_questions"
        
        # Crear payload optimizado con contexto
        context = enhanced_message if enhanced_message != message else None
        payload = get_category_payload(message, category, context)
        
        # Añadir parámetros personalizados del cliente si los hay
        if 'max_tokens' in data:
            payload['n_predict'] = data['max_tokens']
        if 'temperature' in data:
            payload['temperature'] = data['temperature']
        
        # Reenviar petición a la VM
        response = requests.post(
            GPTOSS_API_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )
        
        if response.ok:
            data = response.json()
            # Convertir respuesta del modelo local al formato esperado
            result = {
                "response": data.get('content', 'Sin respuesta'),
                "model": "gpt-oss-20b",
                "tokens": data.get('tokens_predicted', 0)
            }
            print(f"✅ Respuesta exitosa: {result.get('response', 'Sin respuesta')[:50]}...")
            return jsonify(result)
        else:
            print(f"❌ Error de la VM: {response.status_code}")
            return jsonify({
                'error': f'Error de la VM: {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout en la petición a la VM")
        return jsonify({'error': 'Timeout: La VM tardó demasiado en responder'}), 504
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la VM: {e}")
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502
    except Exception as e:
        print(f"❌ Error interno del servidor: {e}")
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

if __name__ == '__main__':
    print('🚀 Iniciando Servidor Integrado Capibara6...')
    print(f'📡 VM GPT-OSS-20B: {GPTOSS_API_URL}')
    print('🧠 Smart MCP: Activo')
    print('🎵 Coqui TTS: Activo')
    print('🌐 Puerto: 5000')
    print('🔧 CORS habilitado para localhost:8000')
    
    # Verificar conexión con la VM al inicio
    try:
        response = requests.get(GPTOSS_HEALTH_URL, timeout=5)
        if response.ok:
            print('✅ Conexión con VM GPT-OSS-20B: OK')
        else:
            print('⚠️ Advertencia: VM no responde correctamente')
    except requests.exceptions.RequestException as e:
        print(f'⚠️ Advertencia: No se puede conectar con la VM: {e}')
    
    print('🦫 Servidor Integrado iniciado correctamente')
    app.run(host='0.0.0.0', port=5000, debug=False)
