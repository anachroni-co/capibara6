"""
Vercel Serverless Function (Python)
TTS con Google Cloud Chirp 3 HD
"""
from google.cloud import texttospeech
from flask import Flask, request, jsonify
import base64
import os
import json

app = Flask(__name__)

def handler(request):
    """Handler principal para Vercel"""
    # CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    if request.method != 'POST':
        return (json.dumps({'error': 'Method not allowed'}), 405, headers)
    
    try:
        # Obtener texto del request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return (json.dumps({'error': 'Text is required'}), 400, headers)
        
        # Limitar a 5000 caracteres para evitar costos excesivos
        if len(text) > 5000:
            text = text[:5000]
        
        # Configurar credenciales desde variable de entorno
        credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if credentials_json:
            # Cargar credenciales desde JSON string
            import tempfile
            credentials_info = json.loads(credentials_json)
            
            # Crear archivo temporal para las credenciales
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(credentials_info, temp_file)
                temp_path = temp_file.name
            
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_path
        
        # Inicializar cliente de Text-to-Speech
        client = texttospeech.TextToSpeechClient()
        
        # Configurar input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Configurar voz Chirp 3 HD en español
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-ES",
            name="es-ES-Chirp-3-HD",  # Chirp 3 de alta definición
        )
        
        # Configurar audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0,
            effects_profile_id=['headphone-class-device']
        )
        
        # Sintetizar
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Convertir a base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        
        result = {
            'audioContent': audio_base64,
            'provider': 'Google Chirp 3 HD',
            'voice': 'es-ES-Chirp-3-HD',
            'characters': len(text)
        }
        
        return (json.dumps(result), 200, headers)
        
    except Exception as e:
        print(f'Error TTS: {str(e)}')
        # Devolver fallback en caso de error
        result = {
            'error': str(e),
            'fallback': True
        }
        return (json.dumps(result), 200, headers)

