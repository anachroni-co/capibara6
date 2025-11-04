# ⚡ Comandos Directos para Ejecutar en la VM

## 🎯 Copia y Pega Estos Comandos (En la VM)

Ya que estás conectado a la VM, ejecuta esto:

---

## 📋 PASO 1: Verificar Qué Servicios Están Activos

```bash
# Ver sesiones de screen
screen -ls

# Ver puertos en uso
sudo netstat -tlnp | grep -E "5001|5002|5003|8080" || sudo ss -tlnp | grep -E "5001|5002|5003|8080"
```

---

## 📋 PASO 2: Verificar Servicios con curl

```bash
# Test cada servicio
echo "=== Gemma Model (8080) ==="
curl -m 2 http://localhost:8080/health 2>/dev/null || echo "INACTIVO"

echo ""
echo "=== Smart MCP (5003) ==="
curl -m 2 http://localhost:5003/health 2>/dev/null || echo "INACTIVO"

echo ""
echo "=== TTS Puerto 5001 ==="
curl -m 2 http://localhost:5001/health 2>/dev/null || echo "INACTIVO"

echo ""
echo "=== TTS Puerto 5002 ==="
curl -m 2 http://localhost:5002/health 2>/dev/null || echo "INACTIVO"
```

---

## 🚀 PASO 3: Iniciar Servicios Faltantes

### Si Smart MCP NO está activo:

```bash
cd ~/capibara6/backend

# Crear directorio si no existe
mkdir -p ~/capibara6/backend
cd ~/capibara6/backend

# Si no tienes smart_mcp_server.py, dímelo y te lo paso
# Si lo tienes:
screen -S smart-mcp
python3 smart_mcp_server.py
# Ctrl+A, D para salir
```

### Si TTS NO está activo:

```bash
cd ~/capibara6/backend

# Si no tienes coqui_tts_server.py, dímelo y te lo paso
# Por ahora, usa el servidor fallback simple:

# Crear servidor fallback rápido
cat > tts_fallback.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'service': 'tts-fallback', 'status': 'healthy'})

@app.route('/tts', methods=['POST'])
def tts():
    return jsonify({'fallback': True, 'provider': 'Web Speech API'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF

# Iniciar servidor fallback
screen -S tts-fallback
python3 tts_fallback.py
# Ctrl+A, D para salir
```

---

## ✅ PASO 4: Verificar de Nuevo

```bash
curl http://localhost:5003/health
curl http://localhost:5002/health
```

---

## 📊 Lista de Archivos Que Deberías Tener

```bash
# Ver qué archivos tienes
ls -la ~/capibara6/backend/

# Deberías tener:
# - smart_mcp_server.py
# - coqui_tts_server.py (o tts_fallback.py)
# - start_*.sh (scripts de inicio)
```

---

## 💡 Si No Tienes los Archivos

Dime qué archivo falta y te doy el comando para crearlo directamente en la VM.

O puedo:
1. Crear los archivos inline con `cat > archivo.py`
2. O darte el contenido completo para copiar/pegar

---

**Ejecuta primero el PASO 2 (verificación con curl) y dime qué servicios están activos/inactivos.** 🔍

