#!/bin/bash
# Script para iniciar servicios en la VM services

echo "🚀 Iniciando servicios en VM services..."
echo "   Arquitectura: E2B ejecución en models-europe, coordinación y frontend en services"

# Directorios
SERVICES_DIR="/home/elect/capibara6/vm_services"
BACKEND_DIR="/home/elect/capibara6/backend"

# Asegurarse de que estamos en el directorio correcto
cd $SERVICES_DIR

# Iniciar coordinador E2B que se comunicará con models-europe
echo "🔌 Iniciando coordinador E2B en puerto 5003..."
echo "   Este coordinador ejecutará tareas E2B en models-europe pero las resultados irán al frontend local"
nohup python3 e2b_coordinator.py > e2b_coordinator.log 2>&1 &

E2B_COORDINATOR_PID=$!
echo "   PID Coordinador E2B: $E2B_COORDINATOR_PID"

# Esperar a que el coordinador inicie
sleep 5

# Verificar que el coordinador E2B esté corriendo
if curl -s http://localhost:5003/api/e2b/health > /dev/null; then
    echo "✅ Coordinador E2B activo en puerto 5003"
else
    echo "❌ Coordinador E2B NO está activo"
    tail -n 20 e2b_coordinator.log
    exit 1
fi

echo ""
echo "🎉 Servicios en VM services iniciados correctamente"
echo ""
echo "🔌 Servicios disponibles:"
echo "   - Coordinador E2B: http://localhost:5003/api/e2b/execute"
echo "   - Health check: http://localhost:5003/api/e2b/health"
echo ""
echo "📋 Arquitectura:"
echo "   - Ejecución E2B: models-europe VM (mayor velocidad)"
echo "   - Coordinación/Visualización: services VM"
echo "   - Frontend: services VM"
echo ""
echo "💾 Logs:"
echo "   - Coordinador E2B: $SERVICES_DIR/e2b_coordinator.log"
echo ""
echo "PID del coordinador E2B: $E2B_COORDINATOR_PID"
echo ""
echo "✅ VM services lista para coordinar E2B desde models-europe al frontend local"