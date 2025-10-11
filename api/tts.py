"""
Vercel Serverless Function (Python)
TTS con Kyutai Delayed Streams Modeling
Usa la biblioteca open-source Moshi para TTS de alta calidad
"""
from flask import Flask, request, jsonify
import base64
import os
import json
import tempfile
import torch

app = Flask(__name__)

# Configuración global
KYUTAI_CONFIG = {
    'model_repo': 'kyutai/tts-1b-en_es',  # Modelo multilingüe
    'sample_rate': 24000,
    'temperature': 0.7,
    'top_p': 0.9,
    'language': 'es',
}

# Cache del modelo (se carga una vez y se reutiliza)
_model_cache = None

def load_kyutai_model():
    """Carga el modelo Kyutai TTS (con cache)"""
    global _model_cache
    
    if _model_cache is not None:
        return _model_cache
    
    try:
        # Importar moshi
        from moshi import models
        
        # Cargar modelo desde Hugging Face
        print(f"📦 Cargando modelo Kyutai: {KYUTAI_CONFIG['model_repo']}")
        
        model = models.load_tts_model(
            hf_repo=KYUTAI_CONFIG['model_repo'],
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        
        _model_cache = model
        print(f"✅ Modelo Kyutai cargado en {model.device}")
        return model
        
    except ImportError:
        print("❌ Error: biblioteca 'moshi' no encontrada")
        raise Exception("Moshi library not installed")
    except Exception as e:
        print(f"❌ Error cargando modelo Kyutai: {str(e)}")
        raise

def synthesize_with_kyutai(text, language='es'):
    """Sintetiza texto con Kyutai TTS"""
    try:
        # Cargar modelo
        model = load_kyutai_model()
        
        # Preparar input
        # Kyutai soporta prompts de voz y texto para mejor control
        synthesis_input = {
            'text': text,
            'language': language,
            'temperature': KYUTAI_CONFIG['temperature'],
            'top_p': KYUTAI_CONFIG['top_p'],
        }
        
        # Sintetizar
        print(f"🎙️ Sintetizando: {len(text)} caracteres")
        audio_output = model.synthesize(**synthesis_input)
        
        # Convertir a WAV en memoria
        import io
        import soundfile as sf
        
        audio_buffer = io.BytesIO()
        sf.write(
            audio_buffer, 
            audio_output, 
            KYUTAI_CONFIG['sample_rate'],
            format='WAV'
        )
        audio_buffer.seek(0)
        
        return audio_buffer.read()
        
    except Exception as e:
        print(f"❌ Error en síntesis Kyutai: {str(e)}")
        raise

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
        language = data.get('language', 'es')
        
        if not text:
            return (json.dumps({'error': 'Text is required'}), 400, headers)
        
        # Limitar a 3000 caracteres para eficiencia
        if len(text) > 3000:
            text = text[:3000]
        
        print(f"📝 Request TTS: {len(text)} chars, lang={language}")
        
        # Sintetizar con Kyutai
        audio_data = synthesize_with_kyutai(text, language)
        
        # Convertir a base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        result = {
            'audioContent': audio_base64,
            'provider': 'Kyutai DSM TTS',
            'model': KYUTAI_CONFIG['model_repo'],
            'language': language,
            'characters': len(text),
            'sample_rate': KYUTAI_CONFIG['sample_rate'],
            'format': 'wav'
        }
        
        print(f"✅ TTS exitoso: {len(audio_data)} bytes")
        return (json.dumps(result), 200, headers)
        
    except Exception as e:
        print(f'❌ Error TTS: {str(e)}')
        import traceback
        traceback.print_exc()
        
        # Devolver fallback en caso de error
        result = {
            'error': str(e),
            'fallback': True,
            'provider': 'Kyutai DSM TTS (error)'
        }
        return (json.dumps(result), 500, headers)

