#!/bin/bash

echo "════════════════════════════════════════════"
echo "  🚀 Activar Coqui TTS - Script Automático"
echo "════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Paso 1: Limpiar TTS anteriores
echo -e "${YELLOW}📦 Paso 1: Limpiando procesos TTS anteriores...${NC}"
pkill -f coqui_tts 2>/dev/null
pkill -f kyutai_tts 2>/dev/null
sleep 2
echo -e "${GREEN}✓ Limpieza completada${NC}"
echo ""

# Paso 2: Verificar archivos necesarios
echo -e "${YELLOW}📦 Paso 2: Verificando archivos...${NC}"

if [ ! -d ~/capibara6/backend ]; then
    echo -e "${RED}❌ Error: Directorio ~/capibara6/backend no existe${NC}"
    echo "Ejecuta: git clone [tu-repo] ~/capibara6"
    exit 1
fi

cd ~/capibara6/backend

if [ ! -f ./start_coqui_tts_py311.sh ]; then
    echo -e "${YELLOW}⚠️  Script no encontrado. Descargando última versión...${NC}"
    git pull origin main
fi

if [ ! -f ./coqui_tts_server.py ]; then
    echo -e "${RED}❌ Error: coqui_tts_server.py no encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Archivos verificados${NC}"
echo ""

# Paso 3: Dar permisos
echo -e "${YELLOW}📦 Paso 3: Configurando permisos...${NC}"
chmod +x ./start_coqui_tts_py311.sh
echo -e "${GREEN}✓ Permisos configurados${NC}"
echo ""

# Paso 4: Iniciar TTS en screen
echo -e "${YELLOW}📦 Paso 4: Iniciando Coqui TTS...${NC}"
screen -dmS coqui-xtts bash -c 'cd ~/capibara6/backend && ./start_coqui_tts_py311.sh'
echo -e "${GREEN}✓ TTS iniciado en screen 'coqui-xtts'${NC}"
echo ""

# Paso 5: Esperar y verificar
echo -e "${YELLOW}📦 Paso 5: Esperando inicio del servidor...${NC}"
echo "⏳ Esto puede tardar 30-60 segundos..."
echo ""

for i in {1..12}; do
    sleep 5
    if curl -s http://localhost:5002/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ¡Servidor TTS activo!${NC}"
        break
    fi
    echo "   Intento $i/12..."
done

echo ""

# Paso 6: Verificación final
echo "════════════════════════════════════════════"
echo "  📊 Estado Final"
echo "════════════════════════════════════════════"
echo ""

if curl -s http://localhost:5002/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Coqui TTS: ACTIVO${NC}"
    echo ""
    echo "📋 Detalles:"
    curl -s http://localhost:5002/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:5002/health
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════"
    echo "  ✅ ¡TODO LISTO!"
    echo "════════════════════════════════════════════${NC}"
    echo ""
    echo "🎤 Próximos pasos:"
    echo "1. Ve a: https://www.capibara6.com/chat.html"
    echo "2. Presiona: Ctrl + Shift + R"
    echo "3. Abre el selector de voces"
    echo "4. Prueba las 3 voces con el botón ▶️"
    echo ""
    echo "🎉 ¡Cada voz debería sonar diferente ahora!"
else
    echo -e "${RED}❌ Coqui TTS: NO RESPONDE${NC}"
    echo ""
    echo "🔍 Diagnóstico:"
    echo "   Ver logs: screen -r coqui-xtts"
    echo "   Salir: Ctrl+A, D"
    echo ""
    echo "💡 Posibles causas:"
    echo "   1. Python 3.11 no instalado"
    echo "   2. Dependencias faltantes"
    echo "   3. Puerto 5002 en uso"
    echo ""
    echo "📝 Ver guía: ACTIVAR_TTS_COQUI_AHORA.md"
fi

echo ""

