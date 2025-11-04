#!/bin/bash

echo "════════════════════════════════════════════"
echo "  🔄 Reiniciar TTS con XTTS v2"
echo "════════════════════════════════════════════"
echo ""

VM_NAME="gemma-3-12b"
ZONE="europe-southwest1-b"
VM_IP="34.175.104.187"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}[1/5] Copiando servidor actualizado a la VM...${NC}"
gcloud compute scp backend/coqui_tts_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al copiar archivo${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Archivo copiado${NC}"
echo ""

echo -e "${YELLOW}[2/5] Deteniendo servidor TTS antiguo...${NC}"
gcloud compute ssh $VM_NAME --zone=$ZONE --command="pkill -f coqui_tts"
sleep 2
echo -e "${GREEN}✓ Servidor detenido${NC}"
echo ""

echo -e "${YELLOW}[3/5] Iniciando XTTS v2 con las 3 voces...${NC}"
gcloud compute ssh $VM_NAME --zone=$ZONE --command="cd ~/capibara6/backend && screen -dmS coqui-xtts bash -c './start_coqui_tts_py311.sh'"
echo -e "${GREEN}✓ Servidor iniciado en background${NC}"
echo ""

echo -e "${YELLOW}[4/5] Esperando a que el servidor esté listo...${NC}"
echo "⏳ XTTS v2 tarda ~30-45 segundos en cargar..."
echo ""

for i in {1..15}; do
    sleep 3
    RESPONSE=$(gcloud compute ssh $VM_NAME --zone=$ZONE --command="curl -s http://localhost:5002/health 2>/dev/null")
    
    if echo "$RESPONSE" | grep -q "xtts_v2"; then
        echo -e "${GREEN}✅ XTTS v2 cargado correctamente!${NC}"
        echo ""
        echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
        break
    else
        echo "   Esperando... ($i/15)"
    fi
done

echo ""
echo -e "${YELLOW}[5/5] Verificando desde exterior...${NC}"
sleep 2

EXTERNAL_RESPONSE=$(curl -s http://$VM_IP:5002/health)

if echo "$EXTERNAL_RESPONSE" | grep -q "xtts_v2"; then
    echo -e "${GREEN}✅ TTS accesible desde exterior${NC}"
    echo ""
    echo "$EXTERNAL_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$EXTERNAL_RESPONSE"
    echo ""
    echo "════════════════════════════════════════════"
    echo -e "${GREEN}  ✅ ¡TODO PERFECTO!${NC}"
    echo "════════════════════════════════════════════"
    echo ""
    echo "🎤 Modelo: XTTS v2"
    echo "👥 Voces: Sofía, Ana, Carlos"
    echo "🎭 Clonación: Disponible"
    echo ""
    echo "📝 Próximos pasos:"
    echo "1. Ve a: https://www.capibara6.com/chat.html"
    echo "2. Ctrl + Shift + R"
    echo "3. Prueba las voces - ¡Ahora sí sonarán diferentes!"
    echo ""
else
    echo -e "${RED}❌ TTS no responde correctamente${NC}"
    echo ""
    echo "🔍 Ver logs:"
    echo "   gcloud compute ssh $VM_NAME --zone=$ZONE"
    echo "   screen -r coqui-xtts"
    echo ""
fi

echo ""

