"""
Servidor TTS con Coqui TTS para Capibara6
Alta calidad en español con VITS
Puerto: 5001
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import sys
import os

app = Flask(__name__)
CORS(app, origins='*')

# Configuración del modelo
COQUI_CONFIG = {
    'model_name': 'tts_models/es/css10/vits',  # Modelo español de alta calidad
    'sample_rate': 22050,
    'max_chars': 3000,
    'speed': 1.0,
}

# Cache del modelo
_tts_model = None
_model_loading = False

def load_coqui_model():
    """Carga el modelo Coqui TTS"""
    global _tts_model, _model_loading
    
    if _tts_model is not None:
        return _tts_model
    
    if _model_loading:
        raise Exception("Modelo ya está cargándose")
    
    _model_loading = True
    
    try:
        print(f"📦 Cargando modelo Coqui TTS: {COQUI_CONFIG['model_name']}")
        
        from TTS.api import TTS
        
        # Cargar modelo
        tts = TTS(model_name=COQUI_CONFIG['model_name'], progress_bar=True)
        
        _tts_model = tts
        _model_loading = False
        
        print(f"✅ Modelo Coqui TTS cargado exitosamente")
        print(f"📊 Sample rate: {COQUI_CONFIG['sample_rate']} Hz")
        print(f"🎤 Modelo: {COQUI_CONFIG['model_name']}")
        
        return tts
        
    except ImportError:
        _model_loading = False
        print("❌ Error: Coqui TTS no encontrado")
        print("💡 Instalar con: pip install TTS")
        raise Exception("Coqui TTS not installed. Run: pip install TTS")
    except Exception as e:
        _model_loading = False
        print(f"❌ Error cargando modelo: {str(e)}")
        raise

def synthesize_audio(text, language='es'):
    """Sintetiza texto a audio con Coqui TTS"""
    try:
        # Limitar caracteres
        if len(text) > COQUI_CONFIG['max_chars']:
            print(f"⚠️ Texto truncado de {len(text)} a {COQUI_CONFIG['max_chars']} caracteres")
            text = text[:COQUI_CONFIG['max_chars']]
        
        print(f"🎙️ Sintetizando: {len(text)} caracteres")
        
        # Cargar modelo
        tts = load_coqui_model()
        
        # Sintetizar a archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # Generar audio
        tts.tts_to_file(
            text=text,
            file_path=tmp_path,
            speed=COQUI_CONFIG['speed']
        )
        
        # Leer audio generado
        with open(tmp_path, 'rb') as f:
            audio_data = f.read()
        
        # Limpiar archivo temporal
        os.remove(tmp_path)
        
        print(f"✅ Audio generado: {len(audio_data)} bytes")
        return audio_data
        
    except Exception as e:
        print(f"❌ Error en síntesis: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        model_loaded = _tts_model is not None
        
        return jsonify({
            'service': 'coqui-tts',
            'status': 'healthy',
            'model': COQUI_CONFIG['model_name'],
            'model_loaded': model_loaded,
            'sample_rate': COQUI_CONFIG['sample_rate'],
            'max_chars': COQUI_CONFIG['max_chars'],
            'provider': 'Coqui TTS (VITS)'
        })
    except Exception as e:
        return jsonify({
            'service': 'coqui-tts',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/tts', methods=['POST'])
def tts():
    """Endpoint principal de TTS"""
    try:
        # Obtener datos del request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '')
        language = data.get('language', 'es')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        print(f"📝 Request TTS: {len(text)} chars, lang={language}")
        
        # Sintetizar
        audio_data = synthesize_audio(text, language)
        
        # Convertir a base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        result = {
            'audioContent': audio_base64,
            'provider': 'Coqui TTS',
            'model': COQUI_CONFIG['model_name'],
            'language': language,
            'characters': len(text),
            'sample_rate': COQUI_CONFIG['sample_rate'],
            'format': 'wav'
        }
        
        print(f"✅ TTS exitoso")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error TTS: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Devolver fallback para que frontend use Web Speech API
        return jsonify({
            'error': str(e),
            'fallback': True,
            'provider': 'Coqui TTS (error)'
        }), 500

@app.route('/preload', methods=['POST'])
def preload():
    """Pre-cargar modelo (útil para warmup)"""
    try:
        tts = load_coqui_model()
        return jsonify({
            'status': 'success',
            'message': 'Modelo Coqui TTS cargado exitosamente',
            'model': COQUI_CONFIG['model_name']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎙️  COQUI TTS SERVER - Capibara6")
    print("=" * 60)
    print(f"📦 Modelo: {COQUI_CONFIG['model_name']}")
    print(f"🔊 Sample rate: {COQUI_CONFIG['sample_rate']} Hz")
    print(f"📝 Max caracteres: {COQUI_CONFIG['max_chars']}")
    print(f"🌐 Idioma: Español")
    print("=" * 60)
    
    # Pre-cargar modelo al iniciar (recomendado)
    print("\n🚀 Pre-cargando modelo Coqui TTS...")
    try:
        load_coqui_model()
        print("✅ Modelo pre-cargado exitosamente\n")
    except Exception as e:
        print(f"⚠️ No se pudo pre-cargar el modelo: {str(e)}")
        print("💡 Se cargará en el primer request\n")
    
    print("🌐 Iniciando servidor Flask en puerto 5001...")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )

