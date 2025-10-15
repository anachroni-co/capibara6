#!/bin/bash

# Script para desplegar el servidor integrado Capibara6 en la VM
# VM: gpt-oss-20b en europe-southwest1-b

echo "🚀 Desplegando Servidor Integrado Capibara6 en VM..."

# Configuración de la VM
VM_NAME="gpt-oss-20b"
VM_ZONE="europe-southwest1-b"
VM_PROJECT="mamba-001"
VM_USER="gmarco"

# Archivos a copiar
FILES_TO_COPY=(
    "backend/capibara6_integrated_server.py"
    "backend/start_integrated_server.py"
)

echo "📁 Copiando archivos a la VM..."

# Copiar archivos
for file in "${FILES_TO_COPY[@]}"; do
    echo "  📄 Copiando $file..."
    gcloud compute scp "$file" "${VM_USER}@${VM_NAME}:/home/${VM_USER}/" --zone="$VM_ZONE" --project="$VM_PROJECT"
done

echo "🔧 Configurando servicios en la VM..."

# Comandos a ejecutar en la VM
gcloud compute ssh --zone "$VM_ZONE" --project "$VM_PROJECT" "$VM_NAME" --command="
    echo '📦 Instalando dependencias...'
    pip install flask-cors requests
    
    echo '🔧 Creando servicio systemd...'
    sudo tee /etc/systemd/system/capibara6-integrated.service > /dev/null <<EOF
[Unit]
Description=Capibara6 Integrated Server (GPT-OSS-20B + MCP + TTS)
After=network.target

[Service]
Type=simple
User=gmarco
WorkingDirectory=/home/gmarco
ExecStart=/home/gmarco/.local/bin/python /home/gmarco/capibara6_integrated_server.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/gmarco

[Install]
WantedBy=multi-user.target
EOF

    echo '🔄 Recargando systemd...'
    sudo systemctl daemon-reload
    
    echo '✅ Habilitando servicio...'
    sudo systemctl enable capibara6-integrated
    
    echo '🚀 Iniciando servicio...'
    sudo systemctl start capibara6-integrated
    
    echo '📊 Estado del servicio:'
    sudo systemctl status capibara6-integrated --no-pager
    
    echo '🌐 Verificando puerto 5000...'
    netstat -tlnp | grep :5000 || echo '⚠️ Puerto 5000 no está en uso'
"

echo "✅ Despliegue completado!"
echo ""
echo "🌐 URLs disponibles en la VM:"
echo "  • Chat: http://34.175.215.109:5000/api/chat"
echo "  • Health: http://34.175.215.109:5000/health"
echo "  • MCP: http://34.175.215.109:5000/api/mcp/analyze"
echo "  • TTS: http://34.175.215.109:5000/api/tts/speak"
echo ""
echo "📋 Comandos útiles:"
echo "  • Ver logs: gcloud compute ssh --zone $VM_ZONE --project $VM_PROJECT $VM_NAME --command='sudo journalctl -u capibara6-integrated -f'"
echo "  • Reiniciar: gcloud compute ssh --zone $VM_ZONE --project $VM_PROJECT $VM_NAME --command='sudo systemctl restart capibara6-integrated'"
echo "  • Estado: gcloud compute ssh --zone $VM_ZONE --project $VM_PROJECT $VM_NAME --command='sudo systemctl status capibara6-integrated'"
