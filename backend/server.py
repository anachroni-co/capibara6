#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de capibara6 - Servidor Flask para gestión de emails
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

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
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})on as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

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
            </style>
        </head>
        <body>
            <h1>capibara6 Backend</h1>
            <p class="status">Servidor funcionando correctamente</p>
            <p>Endpoints disponibles:</p>
            <ul>
                <li>POST /api/save-conversation - Guardar conversacion y enviar email</li>
                <li>GET /api/health - Health check</li>
            </ul>
        </body>
    </html>
    '''

if __name__ == '__main__':
    ensure_data_dir()
    print('capibara6 Backend iniciado')
    print(f'Email configurado: {FROM_EMAIL}')
    
    # Puerto para Railway (usa variable de entorno PORT)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

