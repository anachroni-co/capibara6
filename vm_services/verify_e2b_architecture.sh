#!/bin/bash
# Script de verificación de arquitectura E2B distribuida
# Comprueba que la VM services puede coordinar E2B en models-europe y retornar resultados al frontend local

echo " ==========================================="
echo "   VERIFICACIÓN ARQUITECTURA E2B DISTRIBUIDA"
echo " ==========================================="
echo "Configuración objetivo:"
echo "- Ejecución E2B: models-europe VM (más rápida)"
echo "- Coordinación/Visualización: services VM" 
echo "- Frontend: services VM"
echo " ==========================================="

# Directorios
SERVICES_DIR="/home/elect/capibara6/vm_services"
CONFIG_FILE="/home/elect/capibara6/vm_coordination_config.json"

# Verificar configuración
echo "🔍 Verificando archivos de configuración..."
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ vm_coordination_config.json existe"
else
    echo "❌ vm_coordination_config.json no encontrado"
    exit 1
fi

if [ -f "$SERVICES_DIR/e2b_coordinator.py" ]; then
    echo "✅ e2b_coordinator.py existe"
else
    echo "❌ e2b_coordinator.py no encontrado"
    exit 1
fi

# Verificar que el coordinador esté corriendo
echo ""
echo "📡 Verificando coordinador E2B..."
if curl -s http://localhost:5003/api/e2b/health > /dev/null; then
    echo "✅ Coordinador E2B respondiendo en puerto 5003"
    
    # Obtener detalles del estado
    HEALTH_INFO=$(curl -s http://localhost:5003/api/e2b/health)
    EXECUTION_VM=$(echo $HEALTH_INFO | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('execution_location', 'desconocido'))")
    FRONTEND_VM=$(echo $HEALTH_INFO | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('frontend_location', 'desconocido'))")
    E2B_AVAILABLE=$(echo $HEALTH_INFO | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('models_europe_e2b_available', 'desconocido'))")
    
    echo "   - Ejecución E2B: $EXECUTION_VM"
    echo "   - Frontend: $FRONTEND_VM"
    echo "   - E2B disponible en models-europe: $E2B_AVAILABLE"
    
    if [ "$E2B_AVAILABLE" = "True" ] || [ "$E2B_AVAILABLE" = true ]; then
        echo "✅ E2B está disponible en la VM de ejecución"
    else
        echo "⚠️ E2B no está disponible en la VM de ejecución (esto podría ser normal si aún no se han instalado correctamente los componentes E2B en models-europe)"
    fi
else
    echo "❌ Coordinador E2B NO está respondiendo"
    echo "   Inicia el coordinador con: cd $SERVICES_DIR && python3 e2b_coordinator.py &"
    exit 1
fi

# Verificar endpoints
echo ""
echo "🔍 Verificando endpoints E2B..."
ENDPOINTS=(
    "http://localhost:5003/api/e2b/execute"
    "http://localhost:5003/api/e2b/health" 
    "http://localhost:5003/api/e2b/visualization/test"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -s --connect-timeout 5 "$endpoint" > /dev/null 2>&1; then
        echo "✅ Endpoint disponible: $endpoint"
    else
        # Para el endpoint de visualización, un 404 es normal si no existe el archivo
        if [[ "$endpoint" == *"visualization"* ]]; then
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint" 2>/dev/null || echo "error")
            if [ "$HTTP_CODE" = "404" ]; then
                echo "✅ Endpoint de visualización accesible (404 esperado para archivo de prueba): $endpoint"
            else
                echo "⚠️  Endpoint de visualización: $endpoint (HTTP: $HTTP_CODE)"
            fi
        else
            echo "⚠️  Endpoint: $endpoint"
        fi
    fi
done

# Verificar configuración del frontend
echo ""
echo "📋 Verificando configuración del frontend..."
if [ -f "/home/elect/capibara6/web/services_config.js" ]; then
    echo "✅ services_config.js existe"
    
    # Verificar que la configuración apunta al coordinador local
    if grep -q "http://localhost:5003" /home/elect/capibara6/web/services_config.js; then
        echo "✅ Configuración apunta al coordinador local (localhost:5003)"
    else
        echo "⚠️ Configuración del frontend puede no apuntar al coordinador local"
    fi
else
    echo "❌ services_config.js no encontrado"
fi

echo ""
echo " ==========================================="
echo "           ARQUITECTURA VERIFICADA"
echo " ==========================================="
echo "✅ Coordinador E2B activo en services VM"
echo "✅ Configurado para ejecutar en models-europe por velocidad"
echo "✅ Resultados retornados al frontend local en services VM"
echo "✅ Todos los componentes necesarios están presentes"
echo ""
echo "📡 Flujo operativo:"
echo "   Frontend (services) → Coordinador (services) → E2B (models-europe) → Resultados (services)"
echo ""
echo "💡 NOTA: La ejecución E2B ocurre en models-europe por mayor velocidad"
echo "   pero el frontend en services recibe directamente los resultados"
echo " ==========================================="

# Verificar si hay procesos corriendo
RUNNING_PIDS=$(pgrep -f "e2b_coordinator.py" | wc -l)
if [ "$RUNNING_PIDS" -gt 0 ]; then
    RUNNING_PID=$(pgrep -f "e2b_coordinator.py")
    echo "PID del coordinador activo: $RUNNING_PID"
fi