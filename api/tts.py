"""
Vercel Serverless Function (Python)
Proxy ligero a Kyutai TTS en VM
NO intenta cargar el modelo aquí (muy grande para Vercel)
SOLO usa librería estándar de Python
"""
import json
import os
import urllib.request
import urllib.error

# URL del servidor Kyutai TTS en la VM
# Configurar esta variable de entorno en Vercel
KYUTAI_TTS_URL = os.environ.get('KYUTAI_TTS_URL', 'http://34.175.89.158:5001/tts')

def handler(request):
    """Handler principal para Vercel - Proxy a VM"""
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
        # Obtener datos del request
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'es')
        
        if not text:
            return (json.dumps({'error': 'Text is required'}), 400, headers)
        
        # Limitar caracteres
        if len(text) > 3000:
            text = text[:3000]
        
        print(f"📝 Proxy TTS: {len(text)} chars -> {KYUTAI_TTS_URL}")
        
        # Reenviar request a la VM
        req_data = json.dumps({'text': text, 'language': language}).encode('utf-8')
        req = urllib.request.Request(
            KYUTAI_TTS_URL,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"✅ TTS exitoso desde VM")
                return (json.dumps(result), 200, headers)
        except urllib.error.URLError as e:
            print(f"❌ Error conectando a VM: {str(e)}")
            # Devolver fallback para que el frontend use Web Speech API
            result = {
                'error': f'TTS server unavailable: {str(e)}',
                'fallback': True,
                'provider': 'Kyutai TTS (VM offline)'
            }
            return (json.dumps(result), 200, headers)  # 200 para activar fallback gracefully
        
    except Exception as e:
        print(f'❌ Error en proxy: {str(e)}')
        
        # Devolver fallback
        result = {
            'error': str(e),
            'fallback': True,
            'provider': 'Kyutai TTS (proxy error)'
        }
        return (json.dumps(result), 200, headers)

