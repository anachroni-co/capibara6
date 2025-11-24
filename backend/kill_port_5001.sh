#!/bin/bash
# Script para liberar un puerto específico
# Uso: ./kill_port_5001.sh [--port PORT] [PORT]

PORT=5001  # Puerto por defecto

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        -p)
            PORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Uso: $0 [--port PORT] [PORT]"
            echo ""
            echo "Opciones:"
            echo "  --port PORT, -p PORT    Especifica el puerto a liberar"
            echo "  PORT                    Especifica el puerto directamente"
            echo "  --help, -h              Muestra esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  $0                      # Mata proceso en puerto 5001 (por defecto)"
            echo "  $0 --port 8001          # Mata proceso en puerto 8001"
            echo "  $0 -p 3000              # Mata proceso en puerto 3000"
            echo "  $0 8080                 # Mata proceso en puerto 8080"
            exit 0
            ;;
        [0-9]*)
            # Si es un número, asumir que es el puerto
            PORT="$1"
            shift
            ;;
        *)
            echo "❌ Argumento desconocido: $1"
            echo "Usa --help para ver las opciones disponibles"
            exit 1
            ;;
    esac
done

# Validar que el puerto sea un número válido
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "❌ Puerto inválido: $PORT"
    echo "El puerto debe ser un número entre 1 y 65535"
    exit 1
fi

echo "🔍 Buscando procesos en puerto $PORT..."

PORT_PID=$(lsof -ti:$PORT 2>/dev/null)

if [ -z "$PORT_PID" ]; then
    echo "✅ Puerto $PORT ya está libre"
    exit 0
fi

echo "⚠️  Proceso encontrado: PID $PORT_PID"
echo "📋 Información del proceso:"
ps -p $PORT_PID -o pid,cmd 2>/dev/null || echo "   PID: $PORT_PID (información no disponible)"

echo ""
read -p "¿Deseas terminar este proceso? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operación cancelada"
    exit 0
fi

echo "🛑 Terminando proceso..."
kill -9 $PORT_PID 2>/dev/null

sleep 1

# Verificar que se mató
if lsof -ti:$PORT &>/dev/null; then
    echo "❌ El proceso aún está corriendo"
    exit 1
else
    echo "✅ Puerto $PORT liberado exitosamente"
fi

