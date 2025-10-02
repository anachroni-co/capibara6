#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar configuración SMTP
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar variables de entorno
load_dotenv()

def test_smtp_connection():
    """Probar conexión SMTP"""
    print("🔍 Verificando configuración SMTP...\n")
    
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    FROM_EMAIL = os.getenv('FROM_EMAIL')
    
    print(f"📧 Servidor: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"👤 Usuario: {SMTP_USER}")
    print(f"📨 From: {FROM_EMAIL}")
    print()
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("❌ ERROR: SMTP_USER o SMTP_PASSWORD no configurados")
        print("💡 Configura el archivo .env con tus credenciales")
        return False
    
    try:
        print("🔌 Conectando al servidor SMTP...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        
        print("🔒 Iniciando TLS...")
        server.starttls()
        
        print("🔑 Autenticando...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        
        print("✅ ¡Conexión exitosa!\n")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ ERROR: Autenticación fallida")
        print("💡 Verifica que SMTP_USER y SMTP_PASSWORD sean correctos")
        print("💡 Si usas Gmail, genera una 'Contraseña de aplicación':")
        print("   https://myaccount.google.com/apppasswords")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ ERROR SMTP: {e}")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def send_test_email():
    """Enviar email de prueba"""
    print("📧 ¿Quieres enviar un email de prueba? (s/n): ", end="")
    response = input().strip().lower()
    
    if response != 's':
        print("👋 Test cancelado")
        return
    
    print("\n📝 Ingresa el email de destino: ", end="")
    to_email = input().strip()
    
    if not to_email or '@' not in to_email:
        print("❌ Email inválido")
        return
    
    try:
        SMTP_SERVER = os.getenv('SMTP_SERVER')
        SMTP_PORT = int(os.getenv('SMTP_PORT'))
        SMTP_USER = os.getenv('SMTP_USER')
        SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
        FROM_EMAIL = os.getenv('FROM_EMAIL')
        
        print(f"\n📤 Enviando email de prueba a {to_email}...")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🦫 Email de prueba - capibara6'
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        text = """
¡Hola!

Este es un email de prueba del backend de capibara6.

Si recibes este mensaje, significa que la configuración SMTP está funcionando correctamente ✅

Saludos,
Backend capibara6
        """
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
        h1 { color: #667eea; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦫 capibara6</h1>
        <h2>Email de Prueba</h2>
        <p>¡Hola!</p>
        <p>Este es un email de prueba del backend de capibara6.</p>
        <div class="success">
            <strong>✅ ¡Configuración exitosa!</strong><br>
            Si recibes este mensaje, tu configuración SMTP está funcionando correctamente.
        </div>
        <p>Saludos,<br><strong>Backend capibara6</strong></p>
    </div>
</body>
</html>
        """
        
        part1 = MIMEText(text, 'plain', 'utf-8')
        part2 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        print("✅ Email enviado exitosamente!")
        print(f"📬 Revisa la bandeja de entrada de {to_email}")
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("🦫 CAPIBARA6 - TEST DE CONFIGURACIÓN SMTP")
    print("=" * 60)
    print()
    
    if test_smtp_connection():
        print()
        send_test_email()
    
    print()
    print("=" * 60)
    print("✅ Test completado")
    print("=" * 60)

