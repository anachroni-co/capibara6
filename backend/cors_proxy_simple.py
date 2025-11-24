#!/usr/bin/env python3
"""
Proxy CORS local simplificado y robusto para evitar problemas de Cross-Origin 
al conectar con el servidor backend remoto de Capibara6
"""

from flask import Flask, request, jsonify, Response, make_response
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
# CORS muy permisivo para desarrollo local - solo en el proxy
# IMPORTANTE: No usar origins='*' con supports_credentials=True
CORS(app, 
     origins=['http://localhost:8000', 'http://127.0.0.1:8000', '*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
     supports_credentials=False)  # No usar credentials para evitar problemas

# URL del backend remoto (bounty2:5001)
BACKEND_URL = 'http://34.12.166.76:5001'

# Middleware para eliminar headers CORS duplicados
@app.after_request
def remove_duplicate_cors_headers(response):
    """Elimina headers CORS duplicados antes de enviar la respuesta"""
    # Obtener todos los valores del header Access-Control-Allow-Origin
    cors_origin_values = response.headers.getlist('Access-Control-Allow-Origin')
    if len(cors_origin_values) > 1:
        # Si hay múltiples valores, mantener solo el primero
        response.headers.pop('Access-Control-Allow-Origin', None)
        response.headers['Access-Control-Allow-Origin'] = cors_origin_values[0] if cors_origin_values else '*'
    
    # Hacer lo mismo para otros headers CORS
    for header_name in ['Access-Control-Allow-Methods', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Credentials']:
        values = response.headers.getlist(header_name)
        if len(values) > 1:
            response.headers.pop(header_name, None)
            if values:
                response.headers[header_name] = values[0]
    
    return response

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def proxy_chat():
    """Proxy específico para el endpoint de chat"""
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    try:
        raw_data = request.get_data()
        
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
                headers[key] = value
        
        headers['Host'] = '34.12.166.76:5001'
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        # Remover headers CORS del backend para evitar duplicación
        response_headers = dict(response.headers)
        cors_headers_to_remove = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers',
            'access-control-allow-credentials'
        ]
        for header in cors_headers_to_remove:
            response_headers.pop(header, None)
        
        if 'Transfer-Encoding' in response_headers:
            del response_headers['Transfer-Encoding']
            
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de conexión con el backend remoto: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

def _proxy_health_internal():
    """Función interna para hacer health check al backend"""
    # Intentar primero /api/health, luego /health
    response = None
    error_msg = None
    
    # Intentar /api/health primero
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            # Éxito, usar esta respuesta
            return response
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
    
    # Si /api/health falló, intentar /health
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        return None

@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def proxy_health():
    """Proxy para health check - soporta tanto /api/health como /health"""
    if request.method == 'OPTIONS':
        # Flask-CORS manejará esto automáticamente
        response = make_response()
        return response
    
    try:
        backend_response = _proxy_health_internal()
        
        if backend_response is None:
            error_response = make_response(jsonify({
                'error': 'Error al conectar con el backend remoto',
                'tried_endpoints': ['/api/health', '/health']
            }), 502)
            return error_response
        
        # Crear respuesta sin headers CORS del backend
        # Flask-CORS añadirá los headers automáticamente
        flask_response = make_response(
            backend_response.content,
            backend_response.status_code
        )
        
        # Copiar headers del backend EXCEPTO CORS
        for key, value in backend_response.headers.items():
            key_lower = key.lower()
            if key_lower not in [
                'access-control-allow-origin',
                'access-control-allow-methods',
                'access-control-allow-headers',
                'access-control-allow-credentials',
                'content-encoding',
                'transfer-encoding'
            ]:
                flask_response.headers[key] = value
        
        # Flask-CORS añadirá automáticamente los headers CORS correctos
        return flask_response
        
    except Exception as e:
        error_response = make_response(jsonify({'error': f'Error interno: {str(e)}'}), 500)
        return error_response

@app.route('/api/ai/generate', methods=['POST', 'OPTIONS'])
def proxy_ai_generate():
    """Proxy para AI generate endpoint"""
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        headers['Host'] = '34.12.166.76:5001'
        
        response = requests.post(
            f"{BACKEND_URL}/api/ai/generate",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        # Remover headers CORS del backend
        response_headers = dict(response.headers)
        cors_headers_to_remove = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers',
            'access-control-allow-credentials'
        ]
        for header in cors_headers_to_remove:
            response_headers.pop(header, None)
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con el backend remoto: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/ai/classify', methods=['POST', 'OPTIONS'])
def proxy_ai_classify():
    """Proxy para AI classify endpoint"""
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        headers['Host'] = '34.12.166.76:5001'
        
        response = requests.post(
            f"{BACKEND_URL}/api/ai/classify",
            headers=headers,
            data=raw_data,
            timeout=10
        )
        
        # Remover headers CORS del backend
        response_headers = dict(response.headers)
        cors_headers_to_remove = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers',
            'access-control-allow-credentials'
        ]
        for header in cors_headers_to_remove:
            response_headers.pop(header, None)
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con el backend remoto: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_all(subpath):
    """Proxy general para todas las demás rutas con soporte OPTIONS"""
    # Evitar que capture rutas ya manejadas específicamente
    if subpath in ['health', 'api/health']:
        # Estas rutas ya están manejadas por proxy_health
        return jsonify({'error': 'Ruta no encontrada'}), 404
    
    if request.method == 'OPTIONS':
        response = make_response()
        return response
    
    try:
        method = request.method
        
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        
        headers['Host'] = '34.12.166.76:5001'
        raw_data = request.get_data()
        
        # Construir URL de destino
        if subpath.startswith('api/'):
            target_url = f"{BACKEND_URL}/{subpath}"
        else:
            target_url = f"{BACKEND_URL}/api/{subpath}"
        
        if method == 'GET':
            response = requests.get(target_url, headers=headers, params=request.args, timeout=10)
        elif method == 'POST':
            response = requests.post(target_url, headers=headers, data=raw_data, timeout=30)
        elif method == 'PUT':
            response = requests.put(target_url, headers=headers, data=raw_data, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(target_url, headers=headers, timeout=10)
        else:
            return jsonify({'error': f'Método {method} no soportado'}), 405
        
        # Remover headers CORS del backend para evitar duplicación
        response_headers = dict(response.headers)
        cors_headers_to_remove = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers',
            'access-control-allow-credentials'
        ]
        for header in cors_headers_to_remove:
            response_headers.pop(header, None)
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de conexión con el backend remoto: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint para verificar que el proxy está corriendo"""
    return jsonify({
        'status': 'ok',
        'service': 'capibara6-cors-proxy-simplified',
        'backend_target': BACKEND_URL,
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })

if __name__ == '__main__':
    print('🚀 Iniciando Proxy CORS local simplificado para Capibara6...')
    print(f'🎯 Backend remoto: {BACKEND_URL}')
    print('🌐 Puerto local: 8001')
    print('🔗 Endpoints: /api/chat, /api/health, /api/ai/generate, /api/ai/classify, y otros /api/*')
    print('⚠️  IMPORTANTE: El proxy elimina headers CORS del backend para evitar duplicación')
    app.run(host='0.0.0.0', port=8001, debug=False)
