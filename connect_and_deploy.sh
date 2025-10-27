#!/bin/bash
# Conectar a la VM y ejecutar comandos de despliegue

VM_USER="gmarco"
VM_IP="34.175.215.109"
VM_PATH="/home/elect"

echo "🚀 Conectando a la VM y desplegando mejoras"
echo "==========================================="

# Subir archivos primero
echo "📤 Subiendo archivos mejorados..."
scp backend/capibara6_integrated_server.py $VM_USER@$VM_IP:$VM_PATH/backend/
scp backend/gpt_oss_optimized_config.py $VM_USER@$VM_IP:$VM_PATH/backend/
scp web/chat-app.js $VM_USER@$VM_IP:$VM_PATH/web/
scp start_improved_server.sh $VM_USER@$VM_IP:$VM_PATH/
scp test_quick.sh $VM_USER@$VM_IP:$VM_PATH/

echo "✅ Archivos subidos exitosamente"
echo ""
echo "🔗 Conectando a la VM..."
echo "💡 Una vez conectado, ejecuta estos comandos:"
echo ""
echo "   cd $VM_PATH"
echo "   chmod +x start_improved_server.sh test_quick.sh"
echo "   ./start_improved_server.sh"
echo ""
echo "   (En otra terminal)"
echo "   ./test_quick.sh"
echo ""

# Conectar a la VM
ssh $VM_USER@$VM_IP
