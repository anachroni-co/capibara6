#!/bin/bash
# Script completo para iniciar todos los servicios en VM services
# Incluyendo el coordinador E2B que permite ejecución en models-europe pero con resultados al frontend local

echo " ============================================"
echo "    INICIAR SERVICIOS COMPLETOS - VM SERVICES"
echo " ============================================"
echo "Arquitectura:"
echo "- Frontend: Esta VM (services)"
echo "- Backend modelos: models-europe VM"
echo "- Ejecución E2B: models-europe VM (por velocidad)"
echo "- Coordinación E2B: Esta VM (services)"
echo " ============================================"

# Directorio
SERVICES_DIR="/home/elect/capibara6/vm_services"
COORDINATION_CONFIG="/home/elect/capibara6/vm_coordination_config.json"

# Verificar que exista el archivo de configuración
if [ ! -f "$COORDINATION_CONFIG" ]; then
    echo "❌ Archivo de configuración de coordinación no encontrado: $COORDINATION_CONFIG"
    exit 1
fi

# Iniciar el coordinador E2B
echo "🔌 Iniciando coordinador E2B para comunicación con models-europe..."
echo "   Ejecución de E2B ocurrirá en models-europe por velocidad"
echo "   Resultados se retornarán al frontend en esta VM (services)"

cd $SERVICES_DIR
nohup python3 e2b_coordinator.py > e2b_coordinator.log 2>&1 &

E2B_PID=$!
echo "   Coordinador E2B iniciado con PID: $E2B_PID"

# Esperar un momento para que el servidor inicie
sleep 8

# Verificar que esté corriendo
if curl -s http://localhost:5003/api/e2b/health > /dev/null; then
    echo "✅ Coordinador E2B activo y listo para coordinar ejecución desde models-europe"
    
    # Obtener información del estado
    HEALTH_INFO=$(curl -s http://localhost:5003/api/e2b/health)
    EXECUTION_VM=$(echo $HEALTH_INFO | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('execution_location', 'unknown'))")
    FRONTEND_VM=$(echo $HEALTH_INFO | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('frontend_location', 'unknown'))")
    
    echo "   - Ejecución E2B: $EXECUTION_VM"
    echo "   - Frontend: $FRONTEND_VM"
else
    echo "❌ Coordinador E2B no está respondiendo"
    echo "   Revisando logs..."
    tail -n 30 e2b_coordinator.log
    exit 1
fi

echo ""
echo " ============================================"
echo "         SERVICIOS INICIADOS - VM SERVICES"
echo " ============================================"
echo "✅ Coordinador E2B activo en puerto 5003"
echo "   - Ejecución: models-europe VM (máxima velocidad)"
echo "   - Coordinación/Visualización: services VM (frontend aquí)"
echo "   - Resultados: Retornados al frontend local"
echo ""
echo "📡 Endpoints disponibles:"
echo "   - Ejecución E2B: http://localhost:5003/api/e2b/execute"
echo "   - Visualización: http://localhost:5003/api/e2b/visualization/{filepath}"
echo "   - Health check: http://localhost:5003/api/e2b/health"
echo ""
echo "📋 Arquitectura operativa:"
echo "   1. Frontend envía petición E2B a este backend"
echo "   2. Este backend coordina con models-europe para ejecución"
echo "   3. models-europe ejecuta E2B (más rápido allí)"
echo "   4. Resultados se envían de vuelta al frontend en services"
echo ""
echo "💾 Logs: $SERVICES_DIR/e2b_coordinator.log"
echo "PID: $E2B_PID"
echo " ============================================"

# Crear archivo con el PID para poder detener el servicio después
echo $E2B_PID > e2b_coordinator.pid

echo ""
echo "🎉 VM services completamente configurada para coordinar E2B!"
echo "   La ejecución ocurre en models-europe por velocidad"
echo "   Los resultados se retornan al frontend en esta VM!"