# 🔧 Configuración de Servicios - VM gpt-oss-20b

## 📋 Servicios a Configurar

En la VM **gpt-oss-20b** (34.175.136.104) deben correr:

1. **TTS (Text-to-Speech)** - Puerto 5002
2. **MCP (Model Context Protocol)** - Puerto 5003
3. **N8N (Automatización)** - Puerto 5678

---

## 🚀 Conectarse a la VM

```bash
./ssh-services.sh
# O directamente:
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

---

## 1️⃣ Configurar TTS (Text-to-Speech)

### Verificar si ya existe:

```bash
# Buscar archivos relacionados con TTS
find ~ -name "*tts*" -o -name "*kyutai*" 2>/dev/null

# Ver si hay un servidor corriendo
ps aux | grep -E "tts|kyutai"
netstat -tulpn | grep 5002
```

### Si no existe, crear servidor TTS:

```bash
# Crear directorio
mkdir -p ~/services/tts
cd ~/services/tts

# Crear servidor Flask simple
cat > tts_server.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/tts/speak', methods=['POST'])
def speak():
    """Endpoint para TTS"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice = data.get('voice', 'kyutai-default')
        language = data.get('language', 'es')

        # TODO: Integrar con Kyutai TTS real
        # Por ahora, devolver metadata

        return jsonify({
            'success': True,
            'text': text,
            'voice': voice,
            'language': language,
            'audio_url': None,  # Aquí iría la URL del audio generado
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tts/voices', methods=['GET'])
def voices():
    """Listar voces disponibles"""
    return jsonify({
        'voices': [
            {'id': 'kyutai-default', 'name': 'Kyutai Default', 'language': 'es'},
            {'id': 'kyutai-male', 'name': 'Kyutai Male', 'language': 'es'},
            {'id': 'kyutai-female', 'name': 'Kyutai Female', 'language': 'es'},
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'tts'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
EOF

chmod +x tts_server.py
```

### Instalar dependencias:

```bash
pip install flask flask-cors
```

### Crear servicio systemd:

```bash
sudo nano /etc/systemd/system/tts.service
```

Contenido:
```ini
[Unit]
Description=Capibara6 TTS Service
After=network.target

[Service]
Type=simple
User=elect
WorkingDirectory=/home/elect/services/tts
Environment="PORT=5002"
ExecStart=/usr/bin/python3 /home/elect/services/tts/tts_server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Habilitar y arrancar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tts
sudo systemctl start tts
sudo systemctl status tts

# Probar
curl http://localhost:5002/health
```

---

## 2️⃣ Configurar MCP (Model Context Protocol)

### Verificar si ya existe:

```bash
find ~ -name "*mcp*" 2>/dev/null
ps aux | grep mcp
netstat -tulpn | grep 5003
```

### Crear servidor MCP:

```bash
mkdir -p ~/services/mcp
cd ~/services/mcp

cat > mcp_server.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/mcp/analyze', methods=['POST'])
def analyze():
    """Analizar contexto y devolver información relevante"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        context = data.get('context', [])

        # TODO: Implementar análisis real de contexto

        return jsonify({
            'success': True,
            'prompt': prompt,
            'enhanced_prompt': prompt,  # Aquí iría el prompt mejorado
            'context_used': len(context),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mcp/status', methods=['GET'])
def status():
    """Estado del servicio MCP"""
    return jsonify({
        'status': 'ok',
        'service': 'mcp',
        'version': '1.0.0'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'mcp'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=False)
EOF

chmod +x mcp_server.py
```

### Crear servicio systemd:

```bash
sudo nano /etc/systemd/system/mcp.service
```

Contenido:
```ini
[Unit]
Description=Capibara6 MCP Service
After=network.target

[Service]
Type=simple
User=elect
WorkingDirectory=/home/elect/services/mcp
Environment="PORT=5003"
ExecStart=/usr/bin/python3 /home/elect/services/mcp/mcp_server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Habilitar y arrancar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp
sudo systemctl start mcp
sudo systemctl status mcp

# Probar
curl http://localhost:5003/health
```

---

## 3️⃣ Configurar N8N (Automatización)

### Instalar N8N:

```bash
# Instalar Node.js si no está instalado
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar N8N globalmente
sudo npm install -g n8n

# Verificar instalación
n8n --version
```

### Crear servicio systemd:

```bash
sudo nano /etc/systemd/system/n8n.service
```

Contenido:
```ini
[Unit]
Description=N8N Workflow Automation
After=network.target

[Service]
Type=simple
User=elect
Environment="N8N_HOST=0.0.0.0"
Environment="N8N_PORT=5678"
Environment="N8N_PROTOCOL=http"
Environment="WEBHOOK_URL=http://34.175.136.104:5678/"
ExecStart=/usr/bin/n8n start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Habilitar y arrancar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable n8n
sudo systemctl start n8n
sudo systemctl status n8n

# Probar (desde navegador)
# http://34.175.136.104:5678
```

---

## 🔥 Configurar Firewall

### Abrir puertos en Google Cloud:

Desde tu máquina local:

```bash
# Crear regla para todos los servicios
gcloud compute firewall-rules create allow-capibara6-services \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5002,tcp:5003,tcp:5678 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow TTS, MCP, N8N services"
```

### Firewall local (en la VM):

```bash
sudo ufw allow 5002/tcp  # TTS
sudo ufw allow 5003/tcp  # MCP
sudo ufw allow 5678/tcp  # N8N
sudo ufw reload
```

---

## ✅ Verificación Final

### En la VM gpt-oss-20b:

```bash
# Ver todos los servicios
sudo systemctl status tts
sudo systemctl status mcp
sudo systemctl status n8n

# Ver puertos abiertos
netstat -tulpn | grep -E "5002|5003|5678"

# Probar localmente
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5678
```

### Desde tu máquina local:

```bash
# TTS
curl http://34.175.136.104:5002/health

# MCP
curl http://34.175.136.104:5003/health

# N8N (en navegador)
http://34.175.136.104:5678
```

---

## 🔄 Gestión de Servicios

### Comandos útiles:

```bash
# Ver estado de todos los servicios
sudo systemctl status tts mcp n8n

# Reiniciar todos
sudo systemctl restart tts mcp n8n

# Ver logs
sudo journalctl -u tts -f
sudo journalctl -u mcp -f
sudo journalctl -u n8n -f

# Detener todos
sudo systemctl stop tts mcp n8n

# Iniciar todos
sudo systemctl start tts mcp n8n
```

---

## 📊 Script de Verificación

Crear script para verificar todos los servicios:

```bash
cat > ~/check-services.sh << 'EOF'
#!/bin/bash
echo "🔍 Verificando servicios..."
echo ""

echo "TTS (5002):"
curl -s http://localhost:5002/health && echo " ✓" || echo " ✗"

echo "MCP (5003):"
curl -s http://localhost:5003/health && echo " ✓" || echo " ✗"

echo "N8N (5678):"
curl -s http://localhost:5678 > /dev/null && echo " ✓" || echo " ✗"

echo ""
echo "Servicios systemd:"
sudo systemctl is-active tts mcp n8n
EOF

chmod +x ~/check-services.sh
```

Uso:
```bash
./check-services.sh
```

---

## 🚀 Inicio Automático

Todos los servicios están configurados para iniciar automáticamente al arrancar la VM.

Para deshabilitarlo:
```bash
sudo systemctl disable tts mcp n8n
```

Para rehabilitarlo:
```bash
sudo systemctl enable tts mcp n8n
```

---

**Última actualización**: 2025-11-10
**VM**: gpt-oss-20b (34.175.136.104)
