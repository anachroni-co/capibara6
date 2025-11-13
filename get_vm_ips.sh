#!/bin/bash
# Script para obtener IPs de las VMs de Capibara6

echo "🔍 Obteniendo IPs de las VMs..."
echo ""

# Obtener IPs de bounty2
echo "📡 VM bounty2 (europe-west4-a):"
bounty2_public=$(gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)" 2>/dev/null)
bounty2_internal=$(gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].networkIP)" 2>/dev/null)
bounty2_network=$(gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].network)" 2>/dev/null)
echo "  IP Pública: ${bounty2_public:-N/A}"
echo "  IP Interna: ${bounty2_internal:-N/A}"
echo "  Red: ${bounty2_network:-N/A}"
echo ""

# Obtener IPs de rag3
echo "📡 VM rag3 (europe-west2-c):"
rag3_public=$(gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)" 2>/dev/null)
rag3_internal=$(gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].networkIP)" 2>/dev/null)
rag3_network=$(gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].network)" 2>/dev/null)
echo "  IP Pública: ${rag3_public:-N/A}"
echo "  IP Interna: ${rag3_internal:-N/A}"
echo "  Red: ${rag3_network:-N/A}"
echo ""

# Obtener IPs de gpt-oss-20b
echo "📡 VM gpt-oss-20b (europe-southwest1-b):"
gptoss_public=$(gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)" 2>/dev/null)
gptoss_internal=$(gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].networkIP)" 2>/dev/null)
gptoss_network=$(gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].network)" 2>/dev/null)
echo "  IP Pública: ${gptoss_public:-N/A}"
echo "  IP Interna: ${gptoss_internal:-N/A}"
echo "  Red: ${gptoss_network:-N/A}"
echo ""

echo "=========================================="
echo "  RESUMEN DE CONFIGURACIÓN"
echo "=========================================="
echo ""
echo "# Configuración para web/config.js (desarrollo local)"
echo "BACKEND_URL: http://${bounty2_public:-[IP_BOUNTY2]}:5001"
echo ""
echo "# Configuración para backend/.env (comunicación interna)"
echo "OLLAMA_BASE_URL=http://localhost:11434"
echo "RAG_URL=http://${rag3_internal:-[IP_INTERNA_RAG3]}:[PUERTO]"
echo "SERVICES_URL=http://${gptoss_internal:-[IP_INTERNA_GPT-OSS-20B]}:5000"
echo "MCP_URL=http://${gptoss_internal:-[IP_INTERNA_GPT-OSS-20B]}:5003"
echo ""
echo "# Verificar si las VMs están en la misma red:"
if [ "$bounty2_network" = "$rag3_network" ] && [ "$rag3_network" = "$gptoss_network" ]; then
    echo "✅ Todas las VMs están en la misma red: $bounty2_network"
else
    echo "⚠️  Las VMs están en redes diferentes:"
    echo "   - bounty2: $bounty2_network"
    echo "   - rag3: $rag3_network"
    echo "   - gpt-oss-20b: $gptoss_network"
    echo "   Considera configurar VPC Peering para alta velocidad"
fi

