#!/bin/bash

# Script para verificar conexiones y servicios en las VMs de Capibara6

echo "🔍 Verificando conexiones y servicios en las VMs..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para obtener IPs
get_vm_info() {
    local vm_name=$1
    local zone=$2
    
    echo "📡 Obteniendo información de $vm_name ($zone)..."
    gcloud compute instances describe "$vm_name" --zone="$zone" --project=mamba-001 --format="json" > "/tmp/${vm_name}_info.json" 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Información obtenida${NC}"
        # Extraer IPs
        nat_ip=$(grep -o '"natIP": "[^"]*"' "/tmp/${vm_name}_info.json" | head -1 | cut -d'"' -f4)
        network_ip=$(grep -o '"networkIP": "[^"]*"' "/tmp/${vm_name}_info.json" | head -1 | cut -d'"' -f4)
        
        echo "  IP Pública: ${nat_ip:-N/A}"
        echo "  IP Interna: ${network_ip:-N/A}"
        echo ""
    else
        echo -e "${RED}❌ Error obteniendo información${NC}"
        echo ""
    fi
}

# Verificar servicios en cada VM
check_vm_services() {
    local vm_name=$1
    local zone=$2
    local description=$3
    
    echo "🔧 Verificando servicios en $vm_name ($description)..."
    echo "Conectando a $vm_name..."
    
    # Comando para verificar servicios
    gcloud compute ssh --zone="$zone" "$vm_name" --project=mamba-001 --command="
        echo '=== PUERTOS ESCUCHANDO ==='
        sudo ss -tulnp | grep LISTEN || netstat -tulnp | grep LISTEN || echo 'No se pudo obtener información de puertos'
        echo ''
        echo '=== PROCESOS PYTHON ==='
        ps aux | grep python | grep -v grep | head -5
        echo ''
        echo '=== PROCESOS NODE ==='
        ps aux | grep node | grep -v grep | head -5
        echo ''
        echo '=== PROCESOS OLLAMA ==='
        ps aux | grep ollama | grep -v grep | head -5
        echo ''
        echo '=== VERIFICAR SERVICIOS COMUNES ==='
        curl -s http://localhost:5000/health 2>/dev/null && echo '✅ Puerto 5000 activo' || echo '❌ Puerto 5000 no responde'
        curl -s http://localhost:5001/health 2>/dev/null && echo '✅ Puerto 5001 activo' || echo '❌ Puerto 5001 no responde'
        curl -s http://localhost:5003/health 2>/dev/null && echo '✅ Puerto 5003 activo' || echo '❌ Puerto 5003 no responde'
        curl -s http://localhost:8080/health 2>/dev/null && echo '✅ Puerto 8080 activo' || echo '❌ Puerto 8080 no responde'
        curl -s http://localhost:11434/api/tags 2>/dev/null && echo '✅ Ollama (11434) activo' || echo '❌ Ollama no responde'
    " 2>&1 | head -50
    
    echo ""
    echo "---"
    echo ""
}

# Obtener información de las VMs
echo "=========================================="
echo "  VERIFICACIÓN DE VMs - CAPIBARA6"
echo "=========================================="
echo ""

# VM 1: bounty2 (Ollama con modelos)
get_vm_info "bounty2" "europe-west4-a"
check_vm_services "bounty2" "europe-west4-a" "Ollama con modelos (gpt-oss-20B, mixtral, phi-mini3)"

# VM 2: rag3 (Base de datos)
get_vm_info "rag3" "europe-west2-c"
check_vm_services "rag3" "europe-west2-c" "Sistema de base de datos"

# VM 3: gpt-oss-20b (Servicios TTS, MCP, N8n, Bridge)
get_vm_info "gpt-oss-20b" "europe-southwest1-b"
check_vm_services "gpt-oss-20b" "europe-southwest1-b" "Servicios TTS, MCP, N8n, Bridge"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN COMPLETA"
echo "=========================================="
echo ""
echo "📋 Archivos temporales guardados en /tmp/"
echo "   - bounty2_info.json"
echo "   - rag3_info.json"
echo "   - gpt-oss-20b_info.json"

