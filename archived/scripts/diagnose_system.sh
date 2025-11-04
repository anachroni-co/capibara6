#!/bin/bash
# Script de diagnóstico del sistema GPT-OSS-20B

echo "🔍 Diagnóstico del Sistema GPT-OSS-20B"
echo "====================================="

# Verificar directorio actual
echo "📁 Directorio actual: $(pwd)"
echo "👤 Usuario: $(whoami)"
echo "🖥️ Sistema: $(uname -a)"

# Verificar espacio en disco
echo ""
echo "💾 Espacio en disco:"
df -h /home

# Verificar memoria
echo ""
echo "🧠 Memoria disponible:"
free -h

# Verificar procesos relacionados
echo ""
echo "🔄 Procesos relacionados:"
ps aux | grep -E "(llama|gpt|capibara)" | grep -v grep || echo "No hay procesos relacionados ejecutándose"

# Verificar puertos
echo ""
echo "🌐 Puertos en uso:"
netstat -tlnp | grep -E ":(8080|5001|5000)" || echo "Puertos 8080, 5001, 5000 no están en uso"

# Verificar archivos del proyecto
echo ""
echo "📁 Archivos del proyecto:"
if [ -d "/home/elect" ]; then
    echo "✅ Directorio /home/elect existe"
    ls -la /home/elect/ | head -10
else
    echo "❌ Directorio /home/elect no existe"
fi

# Verificar modelos
echo ""
echo "🤖 Modelos disponibles:"
if [ -d "/home/elect/models" ]; then
    echo "✅ Directorio de modelos existe"
    ls -la /home/elect/models/ | head -5
    echo "Tamaño total: $(du -sh /home/elect/models 2>/dev/null || echo 'No disponible')"
else
    echo "❌ Directorio de modelos no existe"
fi

# Verificar Google Cloud
echo ""
echo "☁️ Google Cloud Storage:"
if command -v gcloud &> /dev/null; then
    echo "✅ gcloud CLI instalado"
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        echo "✅ Autenticado en Google Cloud"
        echo "Cuenta: $(gcloud auth list --filter=status:ACTIVE --format='value(account)')"
    else
        echo "❌ No autenticado en Google Cloud"
    fi
else
    echo "❌ gcloud CLI no instalado"
fi

# Verificar Python
echo ""
echo "🐍 Python:"
if command -v python3 &> /dev/null; then
    echo "✅ Python3 instalado: $(python3 --version)"
else
    echo "❌ Python3 no instalado"
fi

if command -v pip3 &> /dev/null; then
    echo "✅ pip3 instalado: $(pip3 --version)"
else
    echo "❌ pip3 no instalado"
fi

# Verificar dependencias
echo ""
echo "📦 Dependencias Python:"
if [ -f "/home/elect/backend/requirements.txt" ]; then
    echo "✅ requirements.txt encontrado"
    echo "Dependencias requeridas:"
    cat /home/elect/backend/requirements.txt | head -5
else
    echo "❌ requirements.txt no encontrado"
fi

# Verificar scripts
echo ""
echo "📜 Scripts disponibles:"
ls -la /home/elect/*.sh 2>/dev/null || echo "No hay scripts en /home/elect"

# Verificar conectividad
echo ""
echo "🌐 Conectividad:"
if curl -s --connect-timeout 5 http://localhost:8080/health > /dev/null; then
    echo "✅ Modelo respondiendo en puerto 8080"
else
    echo "❌ Modelo no responde en puerto 8080"
fi

if curl -s --connect-timeout 5 http://localhost:5001/health > /dev/null; then
    echo "✅ Servidor respondiendo en puerto 5001"
else
    echo "❌ Servidor no responde en puerto 5001"
fi

echo ""
echo "🎯 Resumen del diagnóstico:"
echo "=========================="

# Contar problemas
PROBLEMS=0

if [ ! -d "/home/elect" ]; then
    echo "❌ Directorio del proyecto no existe"
    ((PROBLEMS++))
fi

if [ ! -d "/home/elect/models" ]; then
    echo "❌ Directorio de modelos no existe"
    ((PROBLEMS++))
fi

if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI no instalado"
    ((PROBLEMS++))
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no instalado"
    ((PROBLEMS++))
fi

if [ $PROBLEMS -eq 0 ]; then
    echo "✅ Sistema listo para configurar"
    echo "🚀 Ejecutar: ./setup_complete_system.sh"
else
    echo "⚠️ Se encontraron $PROBLEMS problemas"
    echo "🔧 Revisar y corregir antes de continuar"
fi
