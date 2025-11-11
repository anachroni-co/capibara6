#!/bin/bash
# Script de configuración del Bridge Ollama-RAG en bounty2

set -e

echo "================================================"
echo "  Configuración Bridge Ollama-RAG (bounty2)"
echo "================================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variables
RAG_API_URL="${RAG_API_URL:-http://10.154.0.2:8000}"
OLLAMA_ENDPOINT="${OLLAMA_ENDPOINT:-http://localhost:11434}"

echo "Configuración:"
echo "  RAG API: $RAG_API_URL"
echo "  Ollama:  $OLLAMA_ENDPOINT"
echo ""

# 1. Verificar conectividad con RAG3
echo -e "${YELLOW}[1/5]${NC} Verificando conectividad con RAG3..."
if ping -c 2 10.154.0.2 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Conectividad con RAG3: OK"
else
    echo -e "${RED}✗${NC} No se puede conectar a RAG3"
    exit 1
fi

# 2. Verificar API de RAG
echo -e "${YELLOW}[2/5]${NC} Verificando API de RAG..."
if curl -s -m 5 "$RAG_API_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} API de RAG: OK"
else
    echo -e "${RED}✗${NC} API de RAG no responde"
    exit 1
fi

# 3. Verificar Ollama
echo -e "${YELLOW}[3/5]${NC} Verificando Ollama..."
if curl -s -m 5 "$OLLAMA_ENDPOINT/api/tags" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama: OK"

    # Mostrar modelos disponibles
    echo "   Modelos disponibles:"
    curl -s "$OLLAMA_ENDPOINT/api/tags" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for model in data.get('models', []):
    print(f\"   - {model['name']}\")
" 2>/dev/null || echo "   (no se pudieron listar modelos)"
else
    echo -e "${RED}✗${NC} Ollama no responde"
    exit 1
fi

# 4. Instalar dependencias Python
echo -e "${YELLOW}[4/5]${NC} Verificando dependencias Python..."
MISSING_DEPS=0

for package in requests urllib3; do
    if ! python3 -c "import $package" 2>/dev/null; then
        echo "   Instalando $package..."
        pip3 install "$package" --quiet
        MISSING_DEPS=1
    fi
done

if [ $MISSING_DEPS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Dependencias Python: OK"
else
    echo -e "${GREEN}✓${NC} Dependencias instaladas"
fi

# 5. Crear archivo de configuración
echo -e "${YELLOW}[5/5]${NC} Creando archivo de configuración..."

cat > .env.rag_bridge <<EOF
# Configuración del Bridge Ollama-RAG
# Generado: $(date)

# URL del servidor RAG en RAG3 (red privada GCloud)
RAG_API_URL=$RAG_API_URL

# Endpoint de Ollama (local en bounty2)
OLLAMA_ENDPOINT=$OLLAMA_ENDPOINT

# Modelo por defecto
DEFAULT_MODEL_TIER=balanced

# Configuración de RAG
RAG_THRESHOLD=0.3
RAG_CONTEXT_MAX_LENGTH=1500
RAG_TIMEOUT=30
EOF

echo -e "${GREEN}✓${NC} Configuración guardada en .env.rag_bridge"

# Test final
echo ""
echo -e "${YELLOW}Ejecutando test de integración...${NC}"

python3 - <<'PYEOF'
import sys
sys.path.insert(0, '/home/elect/capibara6/backend')

try:
    from rag_client import RAGClient

    # Test básico
    client = RAGClient(base_url="http://10.154.0.2:8000")
    health = client.health_check()

    if health.get("status") == "healthy":
        print("✓ Test de integración: OK")
        print(f"  Servicios RAG: {list(health.get('services', {}).keys())}")
        sys.exit(0)
    else:
        print("✗ Test de integración: FAILED")
        print(f"  Error: {health.get('error', 'Unknown')}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Test de integración: ERROR")
    print(f"  {str(e)}")
    sys.exit(1)
PYEOF

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "================================================"
    echo -e "${GREEN}  ✓ Configuración completada exitosamente!${NC}"
    echo "================================================"
    echo ""
    echo "Próximos pasos:"
    echo ""
    echo "1. Cargar configuración en tu servidor:"
    echo "   source .env.rag_bridge"
    echo ""
    echo "2. Usar en tu código Python:"
    echo "   from ollama_rag_integration import create_integrated_client"
    echo "   client = create_integrated_client(ollama_config)"
    echo ""
    echo "3. Consultar documentación:"
    echo "   cat OLLAMA_RAG_BRIDGE.md"
    echo ""
else
    echo "================================================"
    echo -e "${RED}  ✗ Configuración falló${NC}"
    echo "================================================"
    echo ""
    echo "Verifica:"
    echo "1. Que RAG3 esté ejecutando el API en puerto 8000"
    echo "2. Que no haya reglas de firewall bloqueando la comunicación"
    echo "3. Los logs en /var/log/ para más detalles"
    echo ""
    exit 1
fi
