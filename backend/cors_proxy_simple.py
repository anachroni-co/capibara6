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

# URLs de los servicios en las VMs
BACKEND_URL = 'http://34.12.166.76:5001'      # bounty2 - Backend integrado
MCP_URL = 'http://34.175.136.104:5010'        # gpt-oss-20b - Smart MCP
RAG_URL = 'http://34.105.131.8:8000'          # rag3 - RAG Service
N8N_URL = 'http://34.175.136.104:5678'        # gpt-oss-20b - N8n

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
        headers['Host'] = '34.12.166.76:5001'
        
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
def proxy_health():
    """Proxy para health check"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con el backend remoto: {str(e)}'}), 502

# ============================================
# MCP Endpoints
# ============================================

@app.route('/api/mcp/status', methods=['GET'])
def proxy_mcp_status():
    """Proxy para MCP status"""
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=10)
        if response.ok:
            return jsonify({
                'status': 'healthy',
                'mcp_available': True,
                'service': 'smart-mcp',
                'timestamp': __import__('datetime').datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'mcp_available': False
            }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'unavailable',
            'mcp_available': False,
            'error': str(e)
        }), 503

@app.route('/api/mcp/analyze', methods=['POST'])
def proxy_mcp_analyze():
    """Proxy para MCP analyze"""
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        
        response = requests.post(
            f"{MCP_URL}/api/mcp/analyze",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'MCP no disponible: {str(e)}'}), 503

# ============================================
# N8n Endpoints
# ============================================

@app.route('/api/n8n/templates/recommended', methods=['GET'])
def proxy_n8n_templates():
    """Proxy para N8n templates recomendados"""
    try:
        # N8n puede no tener este endpoint específico, devolvemos un mock
        return jsonify({
            'templates': [],
            'message': 'N8n templates - usar interfaz web de N8n',
            'n8n_url': N8N_URL
        })
    except Exception as e:
        return jsonify({'error': f'Error en N8n: {str(e)}'}), 502

# ============================================
# AI Endpoints (Backend)
# ============================================

@app.route('/api/ai/generate', methods=['POST'])
def proxy_ai_generate():
    """Proxy para generación AI"""
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
                headers[key] = value
        headers['Host'] = '34.12.166.76:5001'
        
        response = requests.post(
            f"{BACKEND_URL}/api/ai/generate",
            headers=headers,
            data=raw_data,
            timeout=300
        )
        
        response_headers = dict(response.headers)
        if 'Transfer-Encoding' in response_headers:
            del response_headers['Transfer-Encoding']
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en AI generate: {str(e)}'}), 502

@app.route('/api/ai/classify', methods=['POST'])
def proxy_ai_classify():
    """Proxy para clasificación AI"""
    try:
        raw_data = request.get_data()
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
                headers[key] = value
        headers['Host'] = '34.12.166.76:5001'
        
        response = requests.post(
            f"{BACKEND_URL}/api/ai/classify",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        response_headers = dict(response.headers)
        if 'Transfer-Encoding' in response_headers:
            del response_headers['Transfer-Encoding']
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en AI classify: {str(e)}'}), 502

# ============================================
# Catch-all para otros endpoints
# ============================================

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_all(subpath):
    """Proxy general para todas las demás rutas"""
    try:
        # Determinar el método HTTP
        method = request.method
        
        # Obtener headers relevantes
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'origin', 'referer', 'content-length']:
                headers[key] = value
        
        # Obtener el cuerpo de la solicitud si existe
        raw_data = request.get_data()
        
        # Determinar la URL de destino según el subpath
        if subpath.startswith('api/mcp'):
            # MCP endpoints
            target_url = f"{MCP_URL}/{subpath.replace('api/mcp/', 'api/mcp/')}"
            if subpath == 'api/mcp/status':
                target_url = f"{MCP_URL}/health"
        elif subpath.startswith('api/rag') or subpath.startswith('api/messages') or subpath.startswith('api/files'):
            # RAG endpoints
            target_url = f"{RAG_URL}/{subpath}"
        elif subpath.startswith('api/n8n'):
            # N8n endpoints - devolver mock
            if subpath == 'api/n8n/templates/recommended':
                return jsonify({
                    'templates': [],
                    'message': 'N8n templates - usar interfaz web de N8n',
                    'n8n_url': N8N_URL
                })
            target_url = f"{N8N_URL}/{subpath}"
        else:
            # Backend endpoints (por defecto)
            if subpath.startswith('api/'):
                target_url = f"{BACKEND_URL}/{subpath}"
            else:
                target_url = f"{BACKEND_URL}/api/{subpath}"
            headers['Host'] = '34.12.166.76:5001'
        
        # Hacer la solicitud al servicio remoto
        if method == 'GET':
            response = requests.get(target_url, headers=headers, params=request.args, timeout=30)
        elif method == 'POST':
            response = requests.post(target_url, headers=headers, data=raw_data, timeout=30)
        elif method == 'PUT':
            response = requests.put(target_url, headers=headers, data=raw_data, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(target_url, headers=headers, timeout=30)
        else:
            return jsonify({'error': f'Método {method} no soportado'}), 405
        
        # Devolver la respuesta
        response_headers = dict(response.headers)
        if 'Transfer-Encoding' in response_headers:
            del response_headers['Transfer-Encoding']
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint para verificar que el proxy está corriendo"""
    return jsonify({
        'status': 'ok',
        'service': 'capibara6-cors-proxy',
        'backend_target': BACKEND_URL,
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'endpoints': {
            'backend': BACKEND_URL,
            'mcp': MCP_URL,
            'rag': RAG_URL,
            'n8n': N8N_URL
        }
    })

if __name__ == '__main__':
    print('=' * 60)
    print('🚀 Iniciando Proxy CORS para Capibara6')
    print('=' * 60)
    print(f'🌐 Puerto local: 8001')
    print('')
    print('📡 Servicios configurados:')
    print(f'   • Backend (bounty2):    {BACKEND_URL}')
    print(f'   • MCP (gpt-oss-20b):    {MCP_URL}')
    print(f'   • RAG (rag3):           {RAG_URL}')
    print(f'   • N8n (gpt-oss-20b):    {N8N_URL}')
    print('')
    print('🔧 CORS habilitado para localhost:8000')
    print('=' * 60)
    app.run(host='0.0.0.0', port=8001, debug=False)