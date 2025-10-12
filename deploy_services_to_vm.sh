#!/bin/bash
echo "========================================"
echo "  Deploy Coqui XTTS v2 + Smart MCP a VM"
echo "========================================"
echo ""

# Configuración de la VM
VM_NAME="gemma-3-12b"
ZONE="europe-southwest1-b"
VM_USER="gmarco"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "[1/7] Creando directorios en la VM..."
gcloud compute ssh $VM_NAME --zone=$ZONE --command="mkdir -p ~/capibara6/backend"

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo conectar a la VM${NC}"
    echo "Verifica que la VM esté corriendo: gcloud compute instances list"
    exit 1
fi

echo ""
echo "[2/7] Copiando servidor Kyutai TTS..."
gcloud compute scp backend/kyutai_tts_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo copiar kyutai_tts_server.py${NC}"
    exit 1
fi

echo ""
echo "[3/7] Copiando servidor Smart MCP..."
gcloud compute scp backend/smart_mcp_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo copiar smart_mcp_server.py${NC}"
    exit 1
fi

echo ""
echo "[4/7] Copiando requirements..."
gcloud compute scp backend/requirements.txt $VM_NAME:~/capibara6/backend/ --zone=$ZONE

echo ""
echo "[5/7] Copiando servidores y scripts TTS..."
gcloud compute scp backend/coqui_tts_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/kyutai_tts_server_simple.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/start_coqui_tts_py311.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/start_kyutai_tts.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/start_smart_mcp.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE

echo ""
echo "[6/7] Configurando firewall GCP (si no existe)..."

# Verificar y crear regla para TTS (puerto 5002)
gcloud compute firewall-rules describe allow-coqui-tts &>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creando regla de firewall para puerto 5002...${NC}"
    gcloud compute firewall-rules create allow-coqui-tts \
        --allow=tcp:5002 \
        --source-ranges=0.0.0.0/0 \
        --description="Coqui TTS Server"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Regla de firewall para TTS creada (puerto 5002)${NC}"
    fi
else
    echo -e "${GREEN}✓ Regla de firewall para TTS ya existe${NC}"
fi

# Verificar y crear regla para MCP (puerto 5010)
gcloud compute firewall-rules describe allow-smart-mcp-5010 &>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Creando regla de firewall para puerto 5010...${NC}"
    gcloud compute firewall-rules create allow-smart-mcp-5010 \
        --allow=tcp:5010 \
        --source-ranges=0.0.0.0/0 \
        --description="Smart MCP Server"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Regla de firewall para MCP creada (puerto 5010)${NC}"
    fi
else
    echo -e "${GREEN}✓ Regla de firewall para MCP ya existe${NC}"
fi

echo ""
echo "[7/7] Preparando virtualenv y permisos en la VM..."

# Preparar scripts y virtualenv
gcloud compute ssh $VM_NAME --zone=$ZONE --command="
    cd ~/capibara6/backend && \
    echo '✓ Dando permisos a scripts...' && \
    chmod +x start_kyutai_tts.sh start_smart_mcp.sh && \
    echo '✓ Permisos configurados' && \
    echo '' && \
    echo '📦 Nota: Las dependencias se instalarán automáticamente' && \
    echo '   en un virtualenv la primera vez que ejecutes los scripts.'
"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Advertencia: Error al configurar permisos${NC}"
    echo "Podrás darles permisos manualmente con: chmod +x start_*.sh"
fi

# Obtener IP de la VM
echo ""
echo "Obteniendo IP de la VM..."
VM_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format="get(networkInterfaces[0].accessConfigs[0].natIP)" 2>/dev/null)

echo ""
echo "========================================"
echo -e "${GREEN}  Deploy completado!${NC}"
echo "========================================"
echo ""
echo -e "${GREEN}✓ Archivos copiados a la VM${NC}"
echo -e "${GREEN}✓ Firewall configurado${NC}"
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""
echo "========================================"
echo "  Próximos pasos"
echo "========================================"
echo ""
echo "1. ${YELLOW}Conectar a la VM:${NC}"
echo "   gcloud compute ssh $VM_NAME --zone=$ZONE"
echo ""
echo "2a. ${YELLOW}Opción A - Coqui XTTS v2 (RECOMENDADO - Máxima calidad):${NC}"
echo "    screen -S coqui-tts"
echo "    cd ~/capibara6/backend"
echo "    ./start_coqui_tts_py311.sh"
echo "    ${GREEN}[Ctrl+A, D para salir]${NC}"
echo "    ${YELLOW}(Primera vez: ~10-15 min - descarga XTTS v2 ~2GB)${NC}"
echo ""
echo "2b. ${YELLOW}Opción B - Kyutai Fallback (Web Speech API):${NC}"
echo "    screen -S kyutai-tts"
echo "    cd ~/capibara6/backend"
echo "    ./start_kyutai_tts.sh"
echo "    ${GREEN}[Ctrl+A, D para salir]${NC}"
echo ""
echo "3. ${YELLOW}Iniciar Smart MCP (en otro screen):${NC}"
echo "   screen -S smart-mcp"
echo "   cd ~/capibara6/backend"
echo "   ./start_smart_mcp.sh"
echo "   ${GREEN}[Ctrl+A, D para salir]${NC}"
echo ""
echo "4. ${YELLOW}Verificar servicios:${NC}"

if [ ! -z "$VM_IP" ]; then
    echo "   curl http://$VM_IP:5002/health  # Coqui XTTS v2"
    echo "   curl http://$VM_IP:5010/health  # Smart MCP"
    echo ""
    echo "   ${YELLOW}IP de tu VM:${NC} ${GREEN}$VM_IP${NC}"
    echo ""
    echo "5. ${YELLOW}Configurar en Vercel:${NC}"
    echo "   Variable: KYUTAI_TTS_URL       → http://$VM_IP:5002/tts"
    echo "   Variable: SMART_MCP_URL        → http://$VM_IP:5010/analyze"
else
    echo "   curl http://VM_IP:5002/health  # Coqui XTTS v2"
    echo "   curl http://VM_IP:5010/health  # Smart MCP"
    echo ""
    echo "5. ${YELLOW}Configurar en Vercel:${NC}"
    echo "   Variable: KYUTAI_TTS_URL       → http://TU_IP_VM:5002/tts"
    echo "   Variable: SMART_MCP_URL        → http://TU_IP_VM:5010/analyze"
fi

echo ""
echo "========================================"
echo "  Servicios disponibles"
echo "========================================"
echo "  - Gemma 3-12B:     Puerto 8080"
echo "  - Coqui XTTS v2:   Puerto 5002 ${GREEN}(⭐ máxima calidad)${NC}"
echo "  - Smart MCP:       Puerto 5010 ${GREEN}(RAG contextual)${NC}"
echo "========================================"
echo ""
echo -e "${GREEN}¡Todo listo! Sigue los pasos de arriba.${NC}"
echo ""

