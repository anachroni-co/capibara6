#!/usr/bin/env python3
"""
Proxy CORS local simplificado y robusto para evitar problemas de Cross-Origin 
al conectar con el servidor backend remoto de Capibara6
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# URL del backend remoto (bounty2:5000 según firewall)
BACKEND_URL = 'http://34.12.166.76:5000'

@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    """Proxy específico para el endpoint de chat - versión robusta"""
    try:
        # Obtener el cuerpo de la solicitud como bytes
        raw_data = request.get_data()
        
        # Obtener todos los headers relevantes, manteniendo cuidadosamente solo los necesarios
        headers = {}
        for key, value in request.headers:
            # Mantener headers importantes para el procesamiento
            if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
                headers[key] = value
        
        # Asegurarse de que Host esté configurado correctamente
        headers['Host'] = '34.12.166.76:5000'
        
        # Añadir header de conexión si no está presente
        if 'Connection' not in headers:
            headers['Connection'] = 'close'
        
        # Hacer la solicitud al backend remoto
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            headers=headers,
            data=raw_data
        )
        
        # Devolver la respuesta del backend remoto
        response_headers = dict(response.headers)
        # Asegurarse de que no hay headers conflictivos
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

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def proxy_health():
    """Proxy para health check - soporta tanto /health como /api/health"""
    try:
        # Intentar primero /health (endpoint real del servidor integrado)
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                return Response(
                    response.content,
                    status=response.status_code,
                    headers=dict(response.headers)
                )
        except:
            pass
        
        # Fallback a /api/health si /health no funciona
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con el backend remoto: {str(e)}'}), 502

@app.route('/api/mcp/analyze', methods=['POST'])
def proxy_mcp_analyze():
    """Proxy específico para el endpoint MCP analyze"""
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
                headers[key] = value
        headers['Host'] = '34.12.166.76:5000'
        
        response = requests.post(
            f"{BACKEND_URL}/api/mcp/analyze",
            headers=headers,
            data=raw_data,
            timeout=10
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error conectando con MCP: {str(e)}'}), 502

@app.route('/api/mcp/status', methods=['GET'])
def proxy_mcp_status():
    """Proxy para el health check de MCP - usa /health del servidor integrado"""
    try:
        # El servidor integrado no tiene /api/mcp/status específico, usar /health
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Formatear respuesta como si fuera MCP status
            mcp_status = {
                'status': 'ok',
                'mcp_available': True,
                'service': 'capibara6_integrated_server',
                'mcp_endpoint': '/api/mcp/analyze',
                'models': data.get('models', [])
            }
            return jsonify(mcp_status), 200
        return jsonify({'status': 'error', 'mcp_available': False}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'mcp_available': False, 'error': str(e)}), 502

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_all(subpath):
    """Proxy general para todas las demás rutas"""
    try:
        # NO hacer proxy de archivos estáticos HTML/CSS/JS
        if subpath.endswith(('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot')):
            return jsonify({'error': 'Este proxy solo maneja endpoints de API. Los archivos estáticos deben servirse desde el servidor web del frontend.'}), 404
        
        # Determinar el método HTTP
        method = request.method
        
        # Obtener headers relevantes
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        
        # Asegurarse de que Host esté configurado correctamente
        headers['Host'] = '34.12.166.76:5000'
        
        # Obtener el cuerpo de la solicitud si existe
        raw_data = request.get_data()
        
        # Determinar la URL de destino según el subpath
        if subpath == 'health':
            # El servidor integrado usa /health directamente
            target_url = f"{BACKEND_URL}/health"
        elif subpath.startswith('api/'):
            target_url = f"{BACKEND_URL}/{subpath}"
        else:
            target_url = f"{BACKEND_URL}/api/{subpath}"
        
        # Hacer la solicitud al backend remoto
        if method == 'GET':
            response = requests.get(target_url, headers=headers, params=request.args)
        elif method == 'POST':
            response = requests.post(target_url, headers=headers, data=raw_data)
        elif method == 'PUT':
            response = requests.put(target_url, headers=headers, data=raw_data)
        elif method == 'DELETE':
            response = requests.delete(target_url, headers=headers)
        else:
            return jsonify({'error': f'Método {method} no soportado'}), 405
        
        # Devolver la respuesta del backend remoto
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
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
    print('🔗 Endpoints: /api/chat, /api/health, y otros /api/*')
    app.run(host='0.0.0.0', port=8001, debug=False)