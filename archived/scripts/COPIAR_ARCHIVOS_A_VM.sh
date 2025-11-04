#!/bin/bash
# Script para copiar todos los archivos actualizados a la VM
# Ejecutar desde tu PC

echo "============================================"
echo "  📦 Copiando Archivos a VM (Puerto 5002)"
echo "============================================"
echo ""

VM_NAME="gemma-3-12b"
ZONE="europe-southwest1-b"

# Copiar servidores actualizados (puerto 5002)
echo "📄 Copiando servidores..."
gcloud compute scp backend/coqui_tts_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/kyutai_tts_server_simple.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/smart_mcp_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE

echo ""
echo "📄 Copiando scripts de inicio..."
gcloud compute scp backend/start_coqui_tts_py311.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/start_smart_mcp.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/check_all_services.sh $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/requirements.txt $VM_NAME:~/capibara6/backend/ --zone=$ZONE

echo ""
echo "✅ Archivos copiados exitosamente"
echo ""
echo "============================================"
echo "  🔥 Crear Firewall para Puerto 5002"
echo "============================================"
echo ""

# Crear regla de firewall para puerto 5002
gcloud compute firewall-rules describe allow-coqui-tts &>/dev/null
if [ $? -ne 0 ]; then
    echo "Creando regla de firewall para puerto 5002..."
    gcloud compute firewall-rules create allow-coqui-tts \
        --allow=tcp:5002 \
        --source-ranges=0.0.0.0/0 \
        --description="Coqui TTS Server"
    echo "✅ Firewall configurado para puerto 5002"
else
    echo "✅ Regla de firewall ya existe"
fi

echo ""
echo "============================================"
echo "  📝 Próximos Pasos (EN LA VM)"
echo "============================================"
echo ""
echo "1. Verificar servicios:"
echo "   cd ~/capibara6/backend"
echo "   chmod +x check_all_services.sh"
echo "   ./check_all_services.sh"
echo ""
echo "2. Iniciar Smart MCP (si no está activo):"
echo "   screen -S smart-mcp"
echo "   ./start_smart_mcp.sh"
echo "   [Ctrl+A, D]"
echo ""
echo "3. Iniciar Coqui TTS (si no está activo):"
echo "   screen -S coqui-tts"
echo "   ./start_coqui_tts_py311.sh"
echo "   [Ctrl+A, D]"
echo ""
echo "============================================"
echo "  ✅ Listo!"
echo "============================================"

