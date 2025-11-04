#!/bin/bash

echo "════════════════════════════════════════════"
echo "  🚀 Activar Coqui TTS en la VM"
echo "════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

VM_NAME="gemma-3-12b"
ZONE="europe-southwest1-b"
VM_IP="34.175.104.187"

echo -e "${YELLOW}[1/4] Copiando script a la VM...${NC}"
gcloud compute scp EJECUTAR_EN_VM.sh $VM_NAME:~/ --zone=$ZONE

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al copiar script${NC}"
    echo "Verifica que estés autenticado: gcloud auth login"
    exit 1
fi

echo -e "${GREEN}✓ Script copiado${NC}"
echo ""

echo -e "${YELLOW}[2/4] Ejecutando script en la VM...${NC}"
echo "⏳ Esto puede tardar 1-2 minutos..."
echo ""

gcloud compute ssh $VM_NAME --zone=$ZONE --command="chmod +x ~/EJECUTAR_EN_VM.sh && ~/EJECUTAR_EN_VM.sh"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al ejecutar script en la VM${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[3/4] Esperando a que el servidor esté listo...${NC}"
sleep 5

echo ""
echo -e "${YELLOW}[4/4] Verificando desde exterior...${NC}"

for i in {1..5}; do
    if curl -s http://$VM_IP:5002/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ TTS accesible desde exterior${NC}"
        echo ""
        curl -s http://$VM_IP:5002/health | python3 -m json.tool 2>/dev/null || curl -s http://$VM_IP:5002/health
        break
    else
        echo "   Intento $i/5..."
        sleep 3
    fi
done

echo ""
echo "════════════════════════════════════════════"
echo -e "${GREEN}  ✅ Proceso Completado${NC}"
echo "════════════════════════════════════════════"
echo ""
echo "🎤 Próximos pasos:"
echo ""
echo "1. Ve a: https://www.capibara6.com/chat.html"
echo ""
echo "2. Presiona: Ctrl + Shift + R (recarga forzada)"
echo ""
echo "3. Abre el selector de voces (debería estar visible)"
echo ""
echo "4. Prueba las 3 voces con el botón ▶️:"
echo "   👩 Sofía - Voz femenina profesional"
echo "   👧 Ana - Voz femenina joven"
echo "   👨 Carlos - Voz masculina clara"
echo ""
echo "5. 🎭 Arrastra un audio a la sección de clonación"
echo ""
echo -e "${GREEN}🎉 ¡Cada voz debería sonar diferente ahora!${NC}"
echo ""
echo "📊 URLs de verificación:"
echo "   Local: http://localhost:5002/health"
echo "   Externa: http://$VM_IP:5002/health"
echo ""
echo "🔍 Para ver logs del TTS:"
echo "   gcloud compute ssh $VM_NAME --zone=$ZONE"
echo "   screen -r coqui-xtts"
echo "   (Salir: Ctrl+A, D)"
echo ""

