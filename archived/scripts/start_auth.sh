#!/bin/bash

# ============================================
# SCRIPT DE INICIO - CAPIBARA6 CON AUTH
# ============================================

echo "🚀 Iniciando Capibara6 con Autenticación..."
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r backend/requirements.txt

# Verificar variables de entorno
echo ""
echo "🔍 Verificando configuración OAuth..."

if [ -z "$GITHUB_CLIENT_ID" ]; then
    echo "⚠️  GITHUB_CLIENT_ID no configurado"
    echo "   Configura: export GITHUB_CLIENT_ID='tu_client_id'"
fi

if [ -z "$GITHUB_CLIENT_SECRET" ]; then
    echo "⚠️  GITHUB_CLIENT_SECRET no configurado"
    echo "   Configura: export GITHUB_CLIENT_SECRET='tu_client_secret'"
fi

if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo "⚠️  GOOGLE_CLIENT_ID no configurado"
    echo "   Configura: export GOOGLE_CLIENT_ID='tu_client_id'"
fi

if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "⚠️  GOOGLE_CLIENT_SECRET no configurado"
    echo "   Configura: export GOOGLE_CLIENT_SECRET='tu_client_secret'"
fi

if [ -z "$JWT_SECRET" ]; then
    echo "⚠️  JWT_SECRET no configurado"
    echo "   Genera uno: openssl rand -hex 32"
fi

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  SECRET_KEY no configurado"
    echo "   Genera uno: openssl rand -hex 32"
fi

echo ""
echo "🌐 URLs de acceso:"
echo "   Frontend: http://localhost:8000"
echo "   Login:    http://localhost:8000/login.html"
echo "   Chat:     http://localhost:8000/chat.html"
echo "   Auth API: http://localhost:5001"
echo ""

# Iniciar servidor de autenticación en background
echo "🔐 Iniciando servidor de autenticación..."
python backend/auth_server.py &
AUTH_PID=$!

# Esperar un momento para que el servidor de auth inicie
sleep 3

# Iniciar servidor del frontend
echo "🎨 Iniciando servidor del frontend..."
cd web && python3 -m http.server 8000 &
FRONTEND_PID=$!

echo ""
echo "✅ Capibara6 iniciado correctamente!"
echo "   - Servidor de Auth (PID: $AUTH_PID)"
echo "   - Servidor Frontend (PID: $FRONTEND_PID)"
echo ""
echo "📋 Para detener los servidores:"
echo "   kill $AUTH_PID $FRONTEND_PID"
echo ""
echo "🔗 Accede a: http://localhost:8000/login.html"

# Mantener el script corriendo
wait
