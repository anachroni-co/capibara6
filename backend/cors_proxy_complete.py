#!/usr/bin/env python3
"""
Proxy CORS Completo para Capibara6
Soporta todos los servicios: Backend, MCP, RAG, N8n
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000', '*'])

# URLs de los servicios en las VMs
SERVICES = {
    'backend': 'http://34.12.166.76:5001',      # bounty2 - Backend integrado
    'mcp': 'http://34.175.136.104:5010',        # gpt-oss-20b - Smart MCP
    'rag': 'http://34.105.131.8:8000',          # rag3 - RAG Service
    'n8n': 'http://34.175.136.104:5678',        # gpt-oss-20b - N8n
}

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint raíz - health check del proxy"""
    return jsonify({
        'status': 'ok',
        'service': 'capibara6-cors-proxy',
        'backend_target': SERVICES['backend'],
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'backend': SERVICES['backend'],
            'mcp': SERVICES['mcp'],
            'rag': SERVICES['rag'],
            'n8n': SERVICES['n8n']
        }
    })

# ============================================
# Backend Endpoints (bounty2:5001)
# ============================================

@app.route('/api/health', methods=['GET', 'OPTIONS'])
@app.route('/health', methods=['GET', 'OPTIONS'])
def proxy_health():
    """Proxy para health check del backend"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        response = requests.get(f"{SERVICES['backend']}/health", timeout=10)
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Backend no disponible: {str(e)}'}), 502

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def proxy_chat():
    """Proxy para chat"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        raw_data = request.get_data()
        headers = _get_clean_headers()
        
        response = requests.post(
            f"{SERVICES['backend']}/api/chat",
            headers=headers,
            data=raw_data,
            timeout=300  # 5 minutos para respuestas largas
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error de chat: {str(e)}'}), 502

@app.route('/api/ai/classify', methods=['POST', 'OPTIONS'])
def proxy_ai_classify():
    """Proxy para clasificación AI"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        raw_data = request.get_data()
        headers = _get_clean_headers()
        
        response = requests.post(
            f"{SERVICES['backend']}/api/ai/classify",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en AI classify: {str(e)}'}), 502

@app.route('/api/ai/generate', methods=['POST', 'OPTIONS'])
def proxy_ai_generate():
    """Proxy para generación AI"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        raw_data = request.get_data()
        headers = _get_clean_headers()
        
        response = requests.post(
            f"{SERVICES['backend']}/api/ai/generate",
            headers=headers,
            data=raw_data,
            timeout=300
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en AI generate: {str(e)}'}), 502

# ============================================
# MCP Endpoints (gpt-oss-20b:5010)
# ============================================

@app.route('/api/mcp/status', methods=['GET', 'OPTIONS'])
def proxy_mcp_status():
    """Proxy para MCP status"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        response = requests.get(f"{SERVICES['mcp']}/health", timeout=10)
        if response.ok:
            return jsonify({
                'status': 'healthy',
                'mcp_available': True,
                'service': 'smart-mcp',
                'timestamp': datetime.now().isoformat()
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

@app.route('/api/mcp/analyze', methods=['POST', 'OPTIONS'])
def proxy_mcp_analyze():
    """Proxy para MCP analyze"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        raw_data = request.get_data()
        headers = _get_clean_headers()
        
        response = requests.post(
            f"{SERVICES['mcp']}/api/mcp/analyze",
            headers=headers,
            data=raw_data,
            timeout=30
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'MCP no disponible: {str(e)}'}), 503

# ============================================
# RAG Endpoints (rag3:8000)
# ============================================

@app.route('/api/rag/health', methods=['GET', 'OPTIONS'])
def proxy_rag_health():
    """Proxy para RAG health"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        response = requests.get(f"{SERVICES['rag']}/health", timeout=10)
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'RAG no disponible: {str(e)}'}), 503

@app.route('/api/messages', methods=['GET', 'POST', 'OPTIONS'])
def proxy_rag_messages():
    """Proxy para RAG messages"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        raw_data = request.get_data() if request.method == 'POST' else None
        headers = _get_clean_headers()
        
        if request.method == 'GET':
            response = requests.get(
                f"{SERVICES['rag']}/api/messages",
                headers=headers,
                params=request.args,
                timeout=30
            )
        else:  # POST
            response = requests.post(
                f"{SERVICES['rag']}/api/messages",
                headers=headers,
                data=raw_data,
                timeout=30
            )
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en RAG messages: {str(e)}'}), 502

# ============================================
# N8n Endpoints (gpt-oss-20b:5678)
# ============================================

@app.route('/api/n8n/templates/recommended', methods=['GET', 'OPTIONS'])
def proxy_n8n_templates():
    """Proxy para N8n templates recomendados"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        # N8n puede no tener este endpoint específico, devolvemos un mock
        return jsonify({
            'templates': [],
            'message': 'N8n templates - usar interfaz web de N8n',
            'n8n_url': SERVICES['n8n']
        })
    except Exception as e:
        return jsonify({'error': f'Error en N8n: {str(e)}'}), 502

# ============================================
# Utilidades
# ============================================

def _cors_preflight_response():
    """Respuesta para preflight OPTIONS requests"""
    response = Response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

def _get_clean_headers():
    """Obtiene headers limpios de la request"""
    headers = {}
    for key, value in request.headers:
        if key.lower() not in ['host', 'origin', 'referer', 'content-length', 'connection']:
            headers[key] = value
    return headers

def _clean_headers(response_headers):
    """Limpia headers de la response"""
    headers = dict(response_headers)
    # Eliminar headers que pueden causar conflictos
    for header in ['Transfer-Encoding', 'Connection', 'Keep-Alive']:
        headers.pop(header, None)
    return headers

# ============================================
# Catch-all para otros endpoints
# ============================================

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_catchall(subpath):
    """Proxy general para cualquier otro endpoint"""
    if request.method == 'OPTIONS':
        return _cors_preflight_response()
    
    try:
        # Determinar a qué servicio dirigir basándose en el path
        if subpath.startswith('api/mcp'):
            target_url = f"{SERVICES['mcp']}/{subpath}"
        elif subpath.startswith('api/rag') or subpath.startswith('api/messages') or subpath.startswith('api/files'):
            target_url = f"{SERVICES['rag']}/{subpath}"
        elif subpath.startswith('api/n8n'):
            target_url = f"{SERVICES['n8n']}/{subpath}"
        else:
            # Por defecto, ir al backend
            target_url = f"{SERVICES['backend']}/{subpath}"
        
        method = request.method
        headers = _get_clean_headers()
        raw_data = request.get_data()
        
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
        
        return Response(
            response.content,
            status=response.status_code,
            headers=_clean_headers(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error en proxy: {str(e)}'}), 502

if __name__ == '__main__':
    print('=' * 60)
    print('🚀 Iniciando Proxy CORS Completo para Capibara6')
    print('=' * 60)
    print(f'🌐 Puerto local: 8001')
    print(f'🔗 Frontend: http://localhost:8000')
    print('')
    print('📡 Servicios configurados:')
    print(f'   • Backend (bounty2):    {SERVICES["backend"]}')
    print(f'   • MCP (gpt-oss-20b):    {SERVICES["mcp"]}')
    print(f'   • RAG (rag3):           {SERVICES["rag"]}')
    print(f'   • N8n (gpt-oss-20b):    {SERVICES["n8n"]}')
    print('')
    print('🔧 CORS habilitado para localhost:8000')
    print('=' * 60)
    
    app.run(host='0.0.0.0', port=8001, debug=False)


