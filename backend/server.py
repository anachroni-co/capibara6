#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de capibara6 - Servidor Flask para gestión de emails y endpoints MCP.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS  # type: ignore[import-untyped]
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional
import os
import json
import socket
from dotenv import load_dotenv

# Importar conector MCP
try:
    from mcp_connector import Capibara6MCPConnector
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  MCP Connector no disponible - instala dependencias opcionales para MCP.")

# Importar gestor de plantillas n8n
try:
    from n8n_templates import (
        get_templates_catalog,
        get_recommended_templates,
        get_template_details,
        search_templates,
        download_template_json,
        import_template
    )
    N8N_TEMPLATES_AVAILABLE = True
except ImportError:
    N8N_TEMPLATES_AVAILABLE = False
    print("⚠️  N8N Templates Manager no disponible")

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Inicializar conector MCP si está disponible
mcp_connector = None
if MCP_AVAILABLE:
    try:
        mcp_connector = Capibara6MCPConnector()
        print("✅ Conector MCP inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando MCP: {e}")
        MCP_AVAILABLE = False

# Configuración SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', 'info@anachroni.co')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'info@anachroni.co')

# Archivo para guardar datos
DATA_FILE = 'user_data/conversations.json'

def ensure_data_dir():
    """Crear directorio de datos si no existe"""
    os.makedirs('user_data', exist_ok=True)

def save_to_file(data):
    """Guardar datos en archivo JSON"""
    ensure_data_dir()
    
    # Leer datos existentes
    existing_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
    
    # Agregar nuevos datos
    existing_data.append({
        'timestamp': datetime.now().isoformat(),
        'email': data.get('email'),
        'conversations': data.get('conversations', []),
        'user_agent': request.headers.get('User-Agent'),
        'ip': request.remote_addr
    })
    
    # Guardar
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    # También guardar en txt
    txt_file = f'user_data/user_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('=== CAPIBARA6 - DATOS DE USUARIO ===\n\n')
        f.write(f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'Email: {data.get("email")}\n')
        f.write(f'IP: {request.remote_addr}\n\n')
        f.write('--- CONVERSACIONES ---\n\n')
        for conv in data.get('conversations', []):
            f.write(f'[{conv.get("timestamp")}]\n')
            f.write(f'{conv.get("message")}\n\n')

def send_email(to_email, conversations):
    """Enviar email de confirmación al usuario"""
    try:
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '¡Gracias por tu interés en capibara6! 🦫'
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        # Contenido del email
        text_content = f"""
¡Hola!

Gracias por tu interés en capibara6, nuestro sistema de IA conversacional avanzado.

Hemos recibido tu mensaje y nos pondremos en contacto contigo muy pronto.

Mientras tanto, puedes:
- Visitar nuestro repositorio: https://github.com/anachroni-co/capibara6
- Explorar la documentación en nuestra web
- Seguirnos en nuestras redes sociales

Un saludo,
Equipo Anachroni
https://www.anachroni.co

---
Este es un email automático. Si necesitas ayuda inmediata, responde a este correo.
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
        .links {{ margin: 20px 0; }}
        .links a {{ color: #667eea; text-decoration: none; margin: 0 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦫 capibara6</h1>
            <p>Sistema de IA Conversacional Avanzado</p>
        </div>
        <div class="content">
            <h2>¡Hola!</h2>
            <p>Gracias por tu interés en <strong>capibara6</strong>, nuestro sistema de IA conversacional de última generación.</p>
            <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo muy pronto para darte más información.</p>
            
            <h3>Mientras tanto, puedes:</h3>
            <ul>
                <li>🔗 <a href="https://github.com/anachroni-co/capibara6">Explorar nuestro repositorio en GitHub</a></li>
                <li>📚 Revisar nuestra documentación técnica</li>
                <li>🚀 Probar nuestras demos interactivas</li>
            </ul>
            
            <div style="text-align: center;">
                <a href="https://github.com/anachroni-co/capibara6" class="button">Ver en GitHub</a>
            </div>
            
            <div class="footer">
                <p><strong>Equipo Anachroni</strong><br>
                <a href="https://www.anachroni.co">www.anachroni.co</a></p>
                <p style="font-size: 12px; color: #999;">
                    Este es un email automático. Si necesitas ayuda inmediata, responde a este correo.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        # Adjuntar contenido
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        # Enviar email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f'Error enviando email: {e}')
        return False

def save_lead_to_file(lead_data):
    """Guardar lead en archivo JSON"""
    ensure_data_dir()
    
    leads_file = 'user_data/leads.json'
    
    # Leer leads existentes
    existing_leads = []
    if os.path.exists(leads_file):
        try:
            with open(leads_file, 'r', encoding='utf-8') as f:
                existing_leads = json.load(f)
        except:
            existing_leads = []
    
    # Agregar nuevo lead
    existing_leads.append(lead_data)
    
    # Guardar
    with open(leads_file, 'w', encoding='utf-8') as f:
        json.dump(existing_leads, f, indent=2, ensure_ascii=False)
    
    # También guardar en txt individual
    txt_file = f'user_data/lead_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('=== CAPIBARA6 - LEAD EMPRESARIAL ===\n\n')
        f.write(f'Fecha: {lead_data["timestamp"]}\n')
        f.write(f'Empresa: {lead_data["company_name"]}\n')
        f.write(f'Contacto: {lead_data["full_name"]}\n')
        f.write(f'Email: {lead_data["email"]}\n')
        f.write(f'Tipo: {lead_data["contact_type"]}\n')
        f.write(f'Presupuesto: {lead_data["budget_range"]}\n')
        f.write(f'Timeline: {lead_data["timeline"]}\n')
        f.write(f'Proyecto: {lead_data["project_description"]}\n')
        f.write(f'Idioma: {lead_data["language"]}\n')
        f.write(f'IP: {lead_data["ip"]}\n')

def send_lead_confirmation_email(lead_data):
    """Enviar email de confirmación al lead"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '¡Gracias por tu interés en capibara6! - Anachroni'
        msg['From'] = FROM_EMAIL
        msg['To'] = lead_data['email']
        
        # Contenido del email
        text_content = f"""
¡Hola {lead_data['full_name']}!

Gracias por tu interés en capibara6 y nuestros servicios empresariales.

Hemos recibido tu consulta sobre {lead_data['contact_type']} y nos pondremos en contacto contigo muy pronto.

Resumen de tu consulta:
- Empresa: {lead_data['company_name']}
- Tipo de contacto: {lead_data['contact_type']}
- Proyecto: {lead_data['project_description']}

Nuestro equipo revisará tu solicitud y te contactará en las próximas 24 horas.

Mientras tanto, puedes:
- Visitar nuestro repositorio: https://github.com/anachroni-co/capibara6
- Explorar la documentación en nuestra web
- Seguirnos en nuestras redes sociales

Un saludo,
Equipo Anachroni
https://www.anachroni.co

---
Este es un email automático. Si necesitas ayuda inmediata, responde a este correo.
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
        .summary {{ background: #e8f4fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .summary h3 {{ margin-top: 0; color: #1e40af; }}
        .summary p {{ margin: 5px 0; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦫 capibara6</h1>
            <p>Servicios Empresariales de IA</p>
        </div>
        <div class="content">
            <h2>¡Hola {lead_data['full_name']}!</h2>
            <p>Gracias por tu interés en <strong>capibara6</strong> y nuestros servicios empresariales.</p>
            <p>Hemos recibido tu consulta y nuestro equipo se pondrá en contacto contigo en las próximas 24 horas.</p>
            
            <div class="summary">
                <h3>📋 Resumen de tu consulta</h3>
                <p><strong>Empresa:</strong> {lead_data['company_name']}</p>
                <p><strong>Tipo de contacto:</strong> {lead_data['contact_type']}</p>
                <p><strong>Proyecto:</strong> {lead_data['project_description']}</p>
                <p><strong>Presupuesto:</strong> {lead_data['budget_range']}</p>
                <p><strong>Timeline:</strong> {lead_data['timeline']}</p>
            </div>
            
            <h3>Mientras tanto, puedes:</h3>
            <ul>
                <li>🔗 <a href="https://github.com/anachroni-co/capibara6">Explorar nuestro repositorio en GitHub</a></li>
                <li>📚 Revisar nuestra documentación técnica</li>
                <li>🚀 Probar nuestras demos interactivas</li>
            </ul>
            
            <div style="text-align: center;">
                <a href="https://github.com/anachroni-co/capibara6" class="button">Ver en GitHub</a>
            </div>
            
            <div class="footer">
                <p><strong>Equipo Anachroni</strong><br>
                <a href="https://www.anachroni.co">www.anachroni.co</a></p>
                <p style="font-size: 12px; color: #999;">
                    Este es un email automático. Si necesitas ayuda inmediata, responde a este correo.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        # Adjuntar contenido
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        # Enviar email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f'Error enviando email de confirmación: {e}')
        return False

def send_lead_notification_to_admin(lead_data):
    """Enviar notificación al admin con datos del lead"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🔥 NUEVO LEAD: {lead_data["company_name"]} - {lead_data["contact_type"]}'
        msg['From'] = FROM_EMAIL
        msg['To'] = FROM_EMAIL
        
        # Preparar contenido
        text_content = f"""
NUEVO LEAD EMPRESARIAL - CAPIBARA6

Empresa: {lead_data['company_name']}
Contacto: {lead_data['full_name']}
Email: {lead_data['email']}
Tipo: {lead_data['contact_type']}
Presupuesto: {lead_data['budget_range']}
Timeline: {lead_data['timeline']}

Proyecto:
{lead_data['project_description']}

---
Fecha: {lead_data['timestamp']}
Idioma: {lead_data['language']}
IP: {lead_data['ip']}
User Agent: {lead_data['user_agent']}
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: monospace; background: #1a1a1a; color: #00ff00; padding: 20px; }}
        .container {{ background: #0a0a0a; padding: 20px; border: 2px solid #00ff00; border-radius: 5px; }}
        .lead-header {{ color: #00ffff; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
        .lead-info {{ background: #151515; padding: 15px; margin: 10px 0; border-left: 3px solid #667eea; }}
        .lead-info h3 {{ color: #00ffff; margin-top: 0; }}
        .lead-info p {{ margin: 5px 0; }}
        .project-desc {{ background: #1a1a1a; padding: 15px; border: 1px solid #333; margin: 10px 0; }}
        .urgent {{ color: #ff6b6b; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="lead-header">🔥 NUEVO LEAD EMPRESARIAL - CAPIBARA6</div>
        
        <div class="lead-info">
            <h3>📊 Información del Lead</h3>
            <p><strong>Empresa:</strong> {lead_data['company_name']}</p>
            <p><strong>Contacto:</strong> {lead_data['full_name']}</p>
            <p><strong>Email:</strong> <a href="mailto:{lead_data['email']}" style="color: #00ffff;">{lead_data['email']}</a></p>
            <p><strong>Tipo:</strong> {lead_data['contact_type']}</p>
            <p><strong>Presupuesto:</strong> {lead_data['budget_range']}</p>
            <p><strong>Timeline:</strong> {lead_data['timeline']}</p>
        </div>
        
        <div class="project-desc">
            <h3>📝 Descripción del Proyecto</h3>
            <p>{lead_data['project_description']}</p>
        </div>
        
        <div class="lead-info">
            <h3>🔍 Metadatos</h3>
            <p><strong>Fecha:</strong> {lead_data['timestamp']}</p>
            <p><strong>Idioma:</strong> {lead_data['language']}</p>
            <p><strong>IP:</strong> {lead_data['ip']}</p>
            <p><strong>User Agent:</strong> {lead_data['user_agent']}</p>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <a href="mailto:{lead_data['email']}" style="background: #00ff00; color: #000; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                📧 CONTACTAR LEAD
            </a>
        </div>
    </div>
</body>
</html>
        """
        
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f'Error enviando notificación de lead al admin: {e}')
        return False

def send_notification_to_admin(user_email, conversations):
    """Enviar notificación al admin con los datos del usuario"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Nuevo contacto desde capibara6: {user_email}'
        msg['From'] = FROM_EMAIL
        msg['To'] = FROM_EMAIL
        
        # Preparar conversaciones
        conv_text = '\n'.join([f"[{c.get('timestamp')}] {c.get('message')}" for c in conversations])
        
        text_content = f"""
NUEVO CONTACTO DESDE CAPIBARA6

Email: {user_email}
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

CONVERSACIONES:
{conv_text}

---
IP: {request.remote_addr}
User Agent: {request.headers.get('User-Agent')}
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: monospace; background: #1a1a1a; color: #00ff00; padding: 20px; }}
        .container {{ background: #0a0a0a; padding: 20px; border: 2px solid #00ff00; border-radius: 5px; }}
        .email {{ color: #00ffff; font-size: 18px; font-weight: bold; }}
        .conversation {{ background: #151515; padding: 15px; margin: 10px 0; border-left: 3px solid #667eea; }}
        .timestamp {{ color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🦫 NUEVO CONTACTO DESDE CAPIBARA6</h2>
        <p><strong>Email:</strong> <span class="email">{user_email}</span></p>
        <p><strong>Fecha:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <h3>CONVERSACIONES:</h3>
        {''.join([f'<div class="conversation"><div class="timestamp">{c.get("timestamp")}</div><div>{c.get("message")}</div></div>' for c in conversations])}
        
        <hr>
        <p style="color: #666; font-size: 12px;">
            IP: {request.remote_addr}<br>
            User Agent: {request.headers.get('User-Agent')}
        </p>
    </div>
</body>
</html>
        """
        
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f'Error enviando notificación al admin: {e}')
        return False

@app.route('/api/save-conversation', methods=['POST'])
def save_conversation():
    """Endpoint para guardar conversación y enviar email"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        conversations = data.get('conversations', [])
        
        if not email:
            return jsonify({'success': False, 'error': 'Email requerido'}), 400
        
        # Guardar en archivo
        save_to_file(data)
        
        # Enviar email al usuario
        email_sent = send_email(email, conversations)
        
        # Enviar notificación al admin
        admin_notified = send_notification_to_admin(email, conversations)
        
        return jsonify({
            'success': True,
            'email_sent': email_sent,
            'admin_notified': admin_notified,
            'message': 'Conversación guardada correctamente'
        })
    except Exception as e:
        print(f'Error guardando conversación: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/save-lead', methods=['POST'])
def save_lead():
    """Endpoint para guardar leads empresariales"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['contactType', 'companyName', 'fullName', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'}), 400
        
        # Preparar datos del lead
        lead_data = {
            'timestamp': datetime.now().isoformat(),
            'contact_type': data.get('contactType'),
            'company_name': data.get('companyName'),
            'full_name': data.get('fullName'),
            'email': data.get('email'),
            'project_description': data.get('projectDescription', ''),
            'budget_range': data.get('budgetRange', ''),
            'timeline': data.get('timeline', ''),
            'source': data.get('source', 'chatbot'),
            'language': data.get('language', 'es'),
            'user_agent': request.headers.get('User-Agent'),
            'ip': request.remote_addr
        }
        
        # Guardar en archivo de leads
        save_lead_to_file(lead_data)
        
        # Enviar email de confirmación al lead
        email_sent = send_lead_confirmation_email(lead_data)
        
        # Enviar notificación al admin
        admin_notified = send_lead_notification_to_admin(lead_data)
        
        return jsonify({
            'success': True,
            'email_sent': email_sent,
            'admin_notified': admin_notified,
            'message': 'Lead guardado correctamente'
        })
    
    except Exception as e:
        print(f'Error guardando lead: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# ENDPOINTS MCP (Model Context Protocol)
# ============================================================================

@app.route('/api/mcp/status', methods=['GET'])
def mcp_status():
    """Estado del conector MCP"""
    if not MCP_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'MCP Connector no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    return jsonify({
        'status': 'running',
        'connector': 'capibara6-mcp-connector',
        'version': '1.0.0',
        'capabilities': mcp_connector.capabilities if mcp_connector else {},
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/mcp/initialize', methods=['POST'])
def mcp_initialize():
    """Inicializar conexión MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": request.get_json() or {}
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/tools/list', methods=['GET', 'POST'])
def mcp_tools_list():
    """Listar herramientas MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        request_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": request.get_json() or {}
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": 2,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/tools/call', methods=['POST'])
def mcp_tools_call():
    """Ejecutar herramienta MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos requeridos"}), 400
        
        request_data = {
            "jsonrpc": "2.0",
            "id": data.get("id", 3),
            "method": "tools/call",
            "params": data
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request.get_json().get("id", 3) if request.get_json() else 3,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/resources/list', methods=['GET', 'POST'])
def mcp_resources_list():
    """Listar recursos MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        request_data = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/list",
            "params": request.get_json() or {}
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": 4,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/resources/read', methods=['POST'])
def mcp_resources_read():
    """Leer recurso MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos requeridos"}), 400
        
        request_data = {
            "jsonrpc": "2.0",
            "id": data.get("id", 5),
            "method": "resources/read",
            "params": data
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request.get_json().get("id", 5) if request.get_json() else 5,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/prompts/list', methods=['GET', 'POST'])
def mcp_prompts_list():
    """Listar prompts MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        request_data = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "prompts/list",
            "params": request.get_json() or {}
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": 6,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/prompts/get', methods=['POST'])
def mcp_prompts_get():
    """Obtener prompt MCP"""
    if not MCP_AVAILABLE:
        return jsonify({'error': 'MCP Connector no disponible'}), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos requeridos"}), 400
        
        request_data = {
            "jsonrpc": "2.0",
            "id": data.get("id", 7),
            "method": "prompts/get",
            "params": data
        }
        
        response = loop.run_until_complete(mcp_connector.handle_request(request_data))
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request.get_json().get("id", 7) if request.get_json() else 7,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/api/mcp/test', methods=['POST'])
def mcp_test():
    """Probar funcionalidad MCP"""
    if not MCP_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'MCP Connector no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        data = request.get_json() or {}
        test_type = data.get("test_type", "full")
        
        results = {}
        
        if test_type in ["full", "tools"]:
            # Test de herramientas
            tools_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            tools_response = loop.run_until_complete(mcp_connector.handle_request(tools_request))
            results["tools"] = tools_response
        
        if test_type in ["full", "resources"]:
            # Test de recursos
            resources_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "resources/list",
                "params": {}
            }
            resources_response = loop.run_until_complete(mcp_connector.handle_request(resources_request))
            results["resources"] = resources_response
        
        if test_type in ["full", "prompts"]:
            # Test de prompts
            prompts_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "prompts/list",
                "params": {}
            }
            prompts_response = loop.run_until_complete(mcp_connector.handle_request(prompts_request))
            results["prompts"] = prompts_response
        
        return jsonify({
            "status": "success",
            "test_type": test_type,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/mcp', methods=['GET'])
def mcp_documentation():
    """Página de documentación del conector MCP"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>capibara6 MCP Connector</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px;
                background: #f5f5f5;
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 40px; 
                border-radius: 10px; 
                text-align: center; 
                margin-bottom: 30px;
            }
            .header h1 { margin: 0; font-size: 36px; }
            .header p { margin: 10px 0 0 0; font-size: 18px; opacity: 0.9; }
            .section { 
                background: white; 
                padding: 30px; 
                border-radius: 10px; 
                margin-bottom: 20px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .section h2 { color: #667eea; margin-top: 0; }
            .endpoint { 
                background: #f8f9fa; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 10px 0; 
                border-left: 4px solid #667eea;
            }
            .method { 
                font-weight: bold; 
                color: #28a745; 
                font-family: monospace; 
            }
            .url { 
                font-family: monospace; 
                background: #e9ecef; 
                padding: 2px 6px; 
                border-radius: 3px;
            }
            .code { 
                background: #2d3748; 
                color: #e2e8f0; 
                padding: 20px; 
                border-radius: 5px; 
                overflow-x: auto; 
                font-family: 'Courier New', monospace;
            }
            .feature { 
                display: inline-block; 
                background: #667eea; 
                color: white; 
                padding: 5px 15px; 
                border-radius: 20px; 
                margin: 5px; 
                font-size: 14px;
            }
            .status { 
                display: inline-block; 
                background: #28a745; 
                color: white; 
                padding: 5px 15px; 
                border-radius: 20px; 
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🦫 capibara6 MCP Connector</h1>
            <p>Conector Model Context Protocol para IA híbrida Transformer-Mamba</p>
            <div class="status">🟢 Servidor Activo</div>
        </div>
        
        <div class="section">
            <h2>📋 Descripción General</h2>
            <p>El conector MCP de capibara6 permite integrar el sistema de IA híbrido con aplicaciones que soporten el Model Context Protocol. Proporciona acceso a herramientas, recursos y prompts del modelo a través de una API estandarizada.</p>
            
            <h3>Características Principales:</h3>
            <div class="feature">Arquitectura Híbrida 70/30</div>
            <div class="feature">Google TPU v5e/v6e</div>
            <div class="feature">Google ARM Axion</div>
            <div class="feature">10M+ Tokens Contexto</div>
            <div class="feature">Compliance UE Total</div>
            <div class="feature">Multimodal</div>
            <div class="feature">Chain-of-Thought</div>
        </div>
        
        <div class="section">
            <h2>🔧 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/api/mcp/status</div>
                <p>Verificar estado del servidor MCP</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/mcp/initialize</div>
                <p>Inicializar conexión MCP</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET/POST</div>
                <div class="url">/api/mcp/tools/list</div>
                <p>Listar herramientas disponibles</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/mcp/tools/call</div>
                <p>Ejecutar herramienta específica</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET/POST</div>
                <div class="url">/api/mcp/resources/list</div>
                <p>Listar recursos disponibles</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/mcp/resources/read</div>
                <p>Leer recurso específico</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET/POST</div>
                <div class="url">/api/mcp/prompts/list</div>
                <p>Listar prompts disponibles</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/mcp/prompts/get</div>
                <p>Obtener prompt específico</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/api/mcp/test</div>
                <p>Probar funcionalidad MCP</p>
            </div>
        </div>
        
        <div class="section">
            <h2>🛠️ Herramientas Disponibles</h2>
            <ul>
                <li><strong>analyze_document</strong> - Análisis de documentos extensos (10M+ tokens)</li>
                <li><strong>codebase_analysis</strong> - Análisis completo de bases de código</li>
                <li><strong>multimodal_processing</strong> - Procesamiento de texto, imagen, video y audio</li>
                <li><strong>compliance_check</strong> - Verificación GDPR, AI Act UE, CCPA</li>
                <li><strong>reasoning_chain</strong> - Chain-of-Thought reasoning hasta 12 pasos</li>
                <li><strong>performance_optimization</strong> - Optimización para TPU y ARM</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📚 Ejemplo de Uso</h2>
            <div class="code">
# Ejemplo de llamada a herramienta
curl -X POST http://localhost:5000/api/mcp/tools/call \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "analyze_document",
    "arguments": {
      "document": "Contenido del documento...",
      "analysis_type": "compliance",
      "language": "es"
    }
  }'
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 Recursos Adicionales</h2>
            <ul>
                <li><a href="https://modelcontextprotocol.io">Documentación oficial MCP</a></li>
                <li><a href="https://capibara6.com">Sitio web capibara6</a></li>
                <li><a href="https://github.com/anachroni-co/capibara6">Repositorio GitHub</a></li>
                <li><a href="https://www.anachroni.co">Anachroni s.coop</a></li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📞 Soporte</h2>
            <p>Para soporte técnico o consultas sobre el conector MCP de capibara6:</p>
            <p>📧 Email: <a href="mailto:info@anachroni.co">info@anachroni.co</a></p>
            <p>🌐 Web: <a href="https://www.anachroni.co">www.anachroni.co</a></p>
        </div>
    </body>
    </html>
    '''


@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return '''
    <html>
        <head>
            <title>capibara6 Backend</title>
            <style>
                body { font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 40px; }
                h1 { color: #00ffff; }
                .status { color: #00ff00; }
                .mcp { color: #ff6b6b; }
                a { color: #00ffff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🦫 capibara6 Backend</h1>
            <p class="status">Servidor funcionando correctamente</p>
            
            <h2>📡 Endpoints Disponibles:</h2>
            <ul>
                <li>POST /api/save-conversation - Guardar conversación y enviar email</li>
                <li>POST /api/save-lead - Guardar leads empresariales</li>
                <li>GET /api/health - Health check</li>
            </ul>
            
            <h2 class="mcp">🔌 MCP Connector:</h2>
            <ul>
                <li><a href="/mcp">📚 Documentación MCP</a></li>
                <li>GET /api/mcp/status - Estado del conector MCP</li>
                <li>POST /api/mcp/initialize - Inicializar MCP</li>
                <li>GET /api/mcp/tools/list - Listar herramientas</li>
                <li>POST /api/mcp/tools/call - Ejecutar herramienta</li>
                <li>GET /api/mcp/resources/list - Listar recursos</li>
                <li>POST /api/mcp/resources/read - Leer recurso</li>
                <li>GET /api/mcp/prompts/list - Listar prompts</li>
                <li>POST /api/mcp/prompts/get - Obtener prompt</li>
                <li>POST /api/mcp/test - Probar funcionalidad</li>
            </ul>
            
            <h2>🚀 Características:</h2>
            <ul>
                <li>Arquitectura Híbrida 70% Transformer / 30% Mamba</li>
                <li>Google TPU v5e/v6e-64 optimizado</li>
                <li>Google ARM Axion support</li>
                <li>10M+ tokens de contexto</li>
                <li>Compliance total UE (GDPR, AI Act, CCPA)</li>
                <li>Procesamiento multimodal</li>
                <li>Chain-of-Thought reasoning</li>
            </ul>
        </body>
    </html>
    '''


# ===========================================
# 🔄 N8N TEMPLATES ENDPOINTS
# ===========================================

@app.route('/api/n8n/templates', methods=['GET'])
def n8n_templates_catalog():
    """Obtiene el catálogo completo de plantillas n8n"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        catalog = get_templates_catalog()
        return jsonify({
            'status': 'success',
            'catalog': catalog,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/n8n/templates/recommended', methods=['GET'])
def n8n_templates_recommended():
    """Obtiene plantillas recomendadas para Capibara6"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        templates = get_recommended_templates()
        return jsonify({
            'status': 'success',
            'count': len(templates),
            'templates': templates,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/n8n/templates/<template_id>', methods=['GET'])
def n8n_template_details(template_id: str):
    """Obtiene detalles de una plantilla específica"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        template = get_template_details(template_id)
        if not template:
            return jsonify({
                'status': 'not_found',
                'error': f'Plantilla {template_id} no encontrada',
                'timestamp': datetime.now().isoformat()
            }), 404

        return jsonify({
            'status': 'success',
            'template': template,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/n8n/templates/search', methods=['GET', 'POST'])
def n8n_templates_search():
    """Busca plantillas por palabra clave"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        if request.method == 'GET':
            query = request.args.get('q', '')
        else:
            data = request.get_json() or {}
            query = data.get('query', '')

        if not query:
            return jsonify({
                'status': 'error',
                'error': 'Query parameter required',
                'timestamp': datetime.now().isoformat()
            }), 400

        results = search_templates(query)
        return jsonify({
            'status': 'success',
            'query': query,
            'count': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/n8n/templates/<template_id>/download', methods=['GET'])
def n8n_template_download(template_id: str):
    """Descarga el JSON de una plantilla"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        workflow = download_template_json(template_id)
        if not workflow:
            return jsonify({
                'status': 'not_found',
                'error': f'Plantilla {template_id} no encontrada o error al descargar',
                'timestamp': datetime.now().isoformat()
            }), 404

        return jsonify({
            'status': 'success',
            'template_id': template_id,
            'workflow': workflow,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/n8n/templates/<template_id>/import', methods=['POST'])
def n8n_template_import(template_id: str):
    """Importa una plantilla directamente a n8n"""
    if not N8N_TEMPLATES_AVAILABLE:
        return jsonify({
            'status': 'unavailable',
            'error': 'N8N Templates Manager no disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    try:
        data = request.get_json() or {}
        n8n_url = data.get('n8n_url') or os.getenv('N8N_URL', 'http://n8n:5678')
        api_key = data.get('api_key') or os.getenv('N8N_API_KEY')

        result = import_template(
            template_id=template_id,
            n8n_url=n8n_url,
            api_key=api_key
        )

        status_code = 200 if result.get('success') else 500
        return jsonify({
            **result,
            'timestamp': datetime.now().isoformat()
        }), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


def _is_port_available(port: int) -> bool:
    """Verificar si un puerto está disponible para escuchar."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('0.0.0.0', port))
        except OSError:
            return False
    return True


def choose_port(preferred: int, extra_candidates: Optional[List[int]] = None) -> int:
    """Seleccionar un puerto disponible a partir de candidatos predefinidos."""
    candidates = [preferred]
    if extra_candidates:
        candidates.extend(extra_candidates)
    # Asegurar candidatos únicos y positivos
    seen = set()
    filtered = []
    for p in candidates:
        if p and p > 0 and p not in seen:
            filtered.append(p)
            seen.add(p)

    for port in filtered:
        if _is_port_available(port):
            return port

    # Fallback a un puerto aleatorio asignado por el SO
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 0))
        return sock.getsockname()[1]


if __name__ == '__main__':
    ensure_data_dir()
    print('🦫 capibara6 Backend iniciado')
    print(f'📧 Email configurado: {FROM_EMAIL}')

    if MCP_AVAILABLE:
        print('✅ Conector MCP disponible')
        print('🔌 Endpoints MCP: /api/mcp/*')
        print('📚 Documentación MCP: /mcp')
    else:
        print('⚠️  Conector MCP no disponible')

    preferred_port = int(os.getenv('PORT', 5000))
    fallback_env = os.getenv('PORT_FALLBACKS', '')
    fallback_ports = []
    if fallback_env:
        try:
            fallback_ports = [int(p.strip()) for p in fallback_env.split(',') if p.strip()]
        except ValueError:
            print('⚠️  PORT_FALLBACKS contiene valores no numéricos, usando valores por defecto.')
            fallback_ports = []

    # Añadir algunos candidatos comunes adicionales
    fallback_ports.extend([5001, 5002, 8000, 8080])

    selected_port = choose_port(preferred_port, fallback_ports)

    if selected_port != preferred_port:
        print(f'⚠️  Puerto {preferred_port} en uso. Cambiando a {selected_port}.')

    print(f'🌐 Servidor escuchando en puerto {selected_port}')
    print(f'🔗 URL: http://localhost:{selected_port}')

    # ============================================
    # 🔀 ENDPOINTS DE PROXY CORS - Para evitar problemas de CORS en el frontend
    # ============================================


@app.route('/api/proxy', methods=['POST'])
def proxy_endpoint():
    """Endpoint genérico de proxy para evitar problemas CORS"""
    try:
        import requests
        
        data = request.get_json()
        target_url = data.get('target_url')
        method = data.get('method', 'GET').upper()
        headers = data.get('headers', {})
        body = data.get('body', {})
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        # Hacer la solicitud al destino real
        if method == 'GET':
            response = requests.get(target_url, headers=headers)
        elif method == 'POST':
            response = requests.post(target_url, json=body, headers=headers)
        elif method == 'PUT':
            response = requests.put(target_url, json=body, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(target_url, headers=headers)
        else:
            return jsonify({'error': f'Method {method} not supported'}), 400
        
        # Devolver la respuesta
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


    app.run(host='0.0.0.0', port=selected_port, debug=False)


# ============================================
# 🔀 ENDPOINTS DE PROXY CORS - Para evitar problemas de CORS en el frontend
# ============================================

@app.route('/api/mcp-proxy', methods=['POST'])
def mcp_proxy_endpoint():
    """Endpoint específico para proxy MCP que soluciona problemas de CORS"""
    try:
        import requests
        
        data = request.get_json()
        target = data.get('target', '')
        method = data.get('method', 'GET')
        body = data.get('body', {})
        
        # Hacer la llamada interna al MCP
        if method.upper() == 'GET':
            response = requests.get(target)
        elif method.upper() == 'POST':
            response = requests.post(target, json=body)
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mcp/tools/call-proxy', methods=['POST'])
def mcp_tools_call_proxy():
    """Proxy específico para llamadas a herramientas MCP"""
    try:
        import requests
        
        data = request.get_json()
        
        # Llamar directamente al endpoint MCP interno
        mcp_call_url = "http://localhost:5000/api/mcp/tools/call"
        response = requests.post(mcp_call_url, json=data, headers={'Content-Type': 'application/json'})
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

