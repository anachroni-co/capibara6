#!/usr/bin/env python3
"""
Script para iniciar un servidor local para probar la conexión con la VM real de Capibara6
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def start_local_server():
    """Inicia un servidor local para probar la conexión con la VM real"""
    
    # Directorio web donde están los archivos
    web_dir = Path(__file__).parent / "web"
    
    if not web_dir.exists():
        print(f"❌ Directorio web no encontrado: {web_dir}")
        print("Vamos a usar el directorio actual")
        web_dir = Path.cwd()
    
    print(f"📁 Usando directorio: {web_dir}")
    print(f"🌐 IP real de la VM: 34.175.136.104")
    print(f"🔌 Puertos confirmados: 5000 (escuchando), 8000 (escuchando)")
    print()
    
    # Cambiar al directorio web
    os.chdir(web_dir)
    
    port = 8000
    print(f"🚀 Iniciando servidor local en: http://localhost:{port}")
    print(f"🔧 Para acceder a las pruebas: http://localhost:{port}/verify_real_vm_connection.html")
    print(f"💬 Para chat: http://localhost:{port}/chat.html")
    print(f"🏠 Para página principal: http://localhost:{port}/index.html")
    print()
    print("Presiona CTRL+C para detener el servidor")
    
    try:
        # Manejar correctamente la solicitud del favicon
        class Handler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', '*')
                super().end_headers()
            
            def do_OPTIONS(self):
                self.send_response(200)
                self.end_headers()
            
            def log_message(self, format, *args):
                # Solo mostrar solicitudes importantes
                if not (self.path.endswith('/favicon.ico') or 'GET / HTTP' in format):
                    super().log_message(format, *args)

        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ El puerto {port} ya está en uso")
            print(".intentando con puerto 8080...")
            try:
                with socketserver.TCPServer(("", 8080), Handler) as httpd:
                    print(f"🚀 Servidor iniciado en: http://localhost:8080")
                    print(f"🔧 Accede a las pruebas en: http://localhost:8080/verify_real_vm_connection.html")
                    print("Presiona CTRL+C para detener")
                    httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Servidor detenido por el usuario")
                sys.exit(0)
        else:
            print(f"❌ Error al iniciar el servidor: {e}")
            sys.exit(1)

if __name__ == "__main__":
    print("🧪 Script de Prueba - Conexión Frontend a VM Real de Capibara6")
    print("="*60)
    print()
    print("✅ Servicios confirmados en VM real (34.175.136.104):")
    print("   • Puerto 5000: Servidor Capibara6 Principal (escuchando)")
    print("   • Puerto 8000: Servicio Adicional (escuchando)")
    print("   • Puerto 5010: Posible servicio MCP (según firewall)")
    print("   • Puerto 5003: Posible servicio MCP (según firewall)")
    print()
    print("📋 Archivos actualizados con la IP real:")
    print("   • config.js")
    print("   • chat-page.js")
    print("   • mcp-integration.js")
    print("   • smart-mcp-integration.js")
    print("   • consensus-integration.js")
    print("   • chatbot.js")
    print("   • script.js")
    print("   • y otros archivos relacionados")
    print()
    
    start_local_server()