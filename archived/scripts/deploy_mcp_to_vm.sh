#!/bin/bash
# Script para deployar Smart MCP en la VM de GCP

set -e

echo "🚀 Deployando Smart MCP a la VM..."

# Variables
VM_USER="gmarco"
VM_HOST="34.175.104.187"
VM_NAME="gemma-3-12b"
ZONE="us-east1-b"

# Crear directorio en la VM
echo "📁 Creando directorios..."
gcloud compute ssh $VM_NAME --zone=$ZONE --command="mkdir -p ~/capibara6/backend"

# Copiar archivos del backend
echo "📤 Copiando archivos..."
gcloud compute scp backend/smart_mcp_server.py $VM_NAME:~/capibara6/backend/ --zone=$ZONE
gcloud compute scp backend/requirements.txt $VM_NAME:~/capibara6/backend/ --zone=$ZONE

# Crear archivo de configuración de systemd para Smart MCP
cat > /tmp/smart-mcp.service << 'EOF'
[Unit]
Description=Smart MCP Server for Capibara6
After=network.target

[Service]
Type=simple
User=gmarco
WorkingDirectory=/home/gmarco/capibara6/backend
Environment="PATH=/home/gmarco/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 smart_mcp_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copiar servicio a la VM
echo "⚙️ Configurando servicio systemd..."
gcloud compute scp /tmp/smart-mcp.service $VM_NAME:/tmp/ --zone=$ZONE

# Instalar dependencias y configurar servicio
gcloud compute ssh $VM_NAME --zone=$ZONE --command="
    cd ~/capibara6/backend && \
    python3 -m pip install --user -r requirements.txt && \
    sudo mv /tmp/smart-mcp.service /etc/systemd/system/ && \
    sudo systemctl daemon-reload && \
    sudo systemctl enable smart-mcp && \
    sudo systemctl start smart-mcp && \
    sudo systemctl status smart-mcp
"

echo "✅ Smart MCP deployado exitosamente!"
echo "🔗 Accesible en: http://$VM_HOST:5003"
echo ""
echo "Para ver logs: gcloud compute ssh $VM_NAME --zone=$ZONE --command='sudo journalctl -u smart-mcp -f'"

