#!/bin/bash
# Despliegue rápido de mejoras a la VM

VM_USER="gmarco"
VM_IP="34.175.215.109"
VM_PATH="/home/elect"

echo "🚀 Despliegue Rápido a la VM"
echo "============================"

# Subir archivos esenciales
echo "📤 Subiendo archivos esenciales..."

scp backend/capibara6_integrated_server.py $VM_USER@$VM_IP:$VM_PATH/backend/
scp backend/gpt_oss_optimized_config.py $VM_USER@$VM_IP:$VM_PATH/backend/
scp web/chat-app.js $VM_USER@$VM_IP:$VM_PATH/web/
scp start_improved_server.sh $VM_USER@$VM_IP:$VM_PATH/

echo "✅ Archivos subidos"
echo ""
echo "🔧 Configurando en la VM..."
ssh $VM_USER@$VM_IP "cd $VM_PATH && chmod +x start_improved_server.sh"

echo "🎉 ¡Listo! Ahora ejecuta en la VM:"
echo "   ./start_improved_server.sh"
