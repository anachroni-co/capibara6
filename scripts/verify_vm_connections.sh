#!/bin/bash
# Script de verificación de conexiones entre VMs de Capibara6

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Verificación de Conexiones - Capibara6 VMs${NC}"
echo "=========================================="
echo ""

# Configuración de VMs
BOUNTY2_IP="34.12.166.76"
BOUNTY2_ZONE="europe-west4-a"
BOUNTY2_NAME="bounty2"

RAG3_ZONE="europe-west2-c"
RAG3_NAME="rag3"

GPT_OSS_20B_IP="34.175.136.104"
GPT_OSS_20B_ZONE="europe-southwest1-b"
GPT_OSS_20B_NAME="gpt-oss-20b"

PROJECT="mamba-001"

# Función para obtener IP pública
get_public_ip() {
    local vm_name=$1
    local zone=$2
    gcloud compute instances describe "$vm_name" \
        --zone="$zone" \
        --project="$PROJECT" \
        --format="value(networkInterfaces[0].accessConfigs[0].natIP)" 2>/dev/null || echo "N/A"
}

# Función para obtener IP interna
get_internal_ip() {
    local vm_name=$1
    local zone=$2
    gcloud compute instances describe "$vm_name" \
        --zone="$zone" \
        --project="$PROJECT" \
        --format="value(networkInterfaces[0].networkIP)" 2>/dev/null || echo "N/A"
}

# Función para verificar conectividad
check_connection() {
    local url=$1
    local service_name=$2
    
    if curl -s --connect-timeout 5 "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $service_name: Conectado"
        return 0
    else
        echo -e "${RED}❌${NC} $service_name: No conectado"
        return 1
    fi
}

# Función para verificar servicio en VM
check_vm_service() {
    local vm_name=$1
    local zone=$2
    local command=$3
    local service_name=$4
    
    echo -e "${YELLOW}🔍${NC} Verificando $service_name en $vm_name..."
    if gcloud compute ssh --zone "$zone" "$vm_name" --project "$PROJECT" --command "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $service_name: Activo"
        return 0
    else
        echo -e "${RED}❌${NC} $service_name: No disponible"
        return 1
    fi
}

echo -e "${BLUE}📡 Obteniendo IPs de las VMs...${NC}"
echo ""

# Obtener IPs
BOUNTY2_PUBLIC=$(get_public_ip "$BOUNTY2_NAME" "$BOUNTY2_ZONE")
BOUNTY2_INTERNAL=$(get_internal_ip "$BOUNTY2_NAME" "$BOUNTY2_ZONE")

RAG3_PUBLIC=$(get_public_ip "$RAG3_NAME" "$RAG3_ZONE")
RAG3_INTERNAL=$(get_internal_ip "$RAG3_NAME" "$RAG3_ZONE")

GPT_OSS_20B_PUBLIC=$(get_public_ip "$GPT_OSS_20B_NAME" "$GPT_OSS_20B_ZONE")
GPT_OSS_20B_INTERNAL=$(get_internal_ip "$GPT_OSS_20B_NAME" "$GPT_OSS_20B_ZONE")

echo -e "${GREEN}VM: bounty2${NC}"
echo "  IP Pública: $BOUNTY2_PUBLIC"
echo "  IP Interna: $BOUNTY2_INTERNAL"
echo ""

echo -e "${GREEN}VM: rag3${NC}"
echo "  IP Pública: $RAG3_PUBLIC"
echo "  IP Interna: $RAG3_INTERNAL"
echo ""

echo -e "${GREEN}VM: gpt-oss-20b${NC}"
echo "  IP Pública: $GPT_OSS_20B_PUBLIC"
echo "  IP Interna: $GPT_OSS_20B_INTERNAL"
echo ""

echo "=========================================="
echo -e "${BLUE}🔌 Verificando servicios en gpt-oss-20b (34.175.136.104)...${NC}"
echo ""

# Verificar servicios en gpt-oss-20b
check_connection "http://$GPT_OSS_20B_IP:5000/api/health" "Servidor Principal (5000)"
check_connection "http://$GPT_OSS_20B_IP:5003/api/mcp/status" "MCP Server (5003)"
check_connection "http://$GPT_OSS_20B_IP:5010/api/mcp/analyze" "MCP Server Alternativo (5010)"
check_connection "http://$GPT_OSS_20B_IP:8080/health" "Llama Server (8080)"

echo ""
echo "=========================================="
echo -e "${BLUE}🔌 Verificando servicios en bounty2 (34.12.166.76)...${NC}"
echo ""

# Verificar servicios en bounty2
check_connection "http://$BOUNTY2_IP:11434/api/tags" "Ollama (11434)"
check_connection "http://$BOUNTY2_IP:5001/api/health" "Backend Capibara6 (5001)"

echo ""
echo "=========================================="
echo -e "${BLUE}🖥️  Verificando servicios activos en VMs...${NC}"
echo ""

# Verificar servicios activos en cada VM
check_vm_service "$GPT_OSS_20B_NAME" "$GPT_OSS_20B_ZONE" \
    "sudo ss -tulnp | grep -E '(5000|5003|5010|8080)' | head -5" \
    "Servicios en gpt-oss-20b"

check_vm_service "$BOUNTY2_NAME" "$BOUNTY2_ZONE" \
    "sudo ss -tulnp | grep -E '(11434|5001)' | head -5" \
    "Servicios en bounty2"

check_vm_service "$RAG3_NAME" "$RAG3_ZONE" \
    "sudo ss -tulnp | head -10" \
    "Servicios en rag3"

echo ""
echo "=========================================="
echo -e "${BLUE}📊 Resumen de Configuración${NC}"
echo ""

echo "Para desarrollo local, configura:"
echo ""
echo "Frontend (web/config.js):"
echo "  BACKEND_URL: 'http://$GPT_OSS_20B_IP:5000'"
echo ""
echo "Backend (backend/.env):"
echo "  OLLAMA_BASE_URL=http://$BOUNTY2_IP:11434"
echo "  GPT_OSS_URL=http://$GPT_OSS_20B_IP:8080"
echo "  RAG_SERVER_URL=http://$RAG3_INTERNAL/api/rag  # Usar IP interna"
echo ""

echo -e "${GREEN}✅ Verificación completada${NC}"

