# 🚨 Solución Temporal para el Frontend

## Problema Actual
El backend Flask en bounty2 no está accesible en los puertos 5000/5001, pero Ollama sí funciona en el puerto 11434.

## Solución Temporal: Usar Ollama Directamente

Mientras se resuelve el problema del backend, puedes configurar el frontend para usar Ollama directamente.

### Opción 1: Modificar chat-app.js para usar Ollama directamente

Edita `web/chat-app.js` y cambia la configuración del modelo:

```javascript
const MODEL_CONFIG = {
    // Usar Ollama directamente en lugar del backend Flask
    serverUrl: window.location.hostname === 'localhost'
        ? 'http://34.12.166.76:11434/api/generate'  // Ollama directamente
        : 'https://www.capibara6.com/api/chat',
    // ...
};
```

**Nota**: Esto requiere modificar la función de envío de mensajes para usar el formato de API de Ollama.

### Opción 2: Crear un proxy local simple

Crea un archivo `web/proxy-ollama.js`:

```javascript
// Proxy simple para usar Ollama desde el frontend
async function sendToOllama(message, model = 'gpt-oss:20b') {
    const response = await fetch('http://34.12.166.76:11434/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: model,
            prompt: message,
            stream: false,
            options: {
                temperature: 0.7,
                top_p: 0.9,
            }
        })
    });
    
    const data = await response.json();
    return data.response;
}
```

### Opción 3: Iniciar el backend en tu máquina local

Si tienes Python y las dependencias instaladas localmente:

```bash
cd backend
python3 server.py
# O
python3 capibara6_integrated_server_ollama.py
```

Luego configura el frontend para usar `http://localhost:5000` o `http://localhost:5001`.

## Solución Definitiva: Arreglar el Backend en bounty2

### Paso 1: Conectarse a bounty2
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### Paso 2: Verificar si el backend está corriendo
```bash
ps aux | grep python | grep -E "(server|flask|capibara6)"
sudo ss -tulnp | grep -E "(5000|5001)"
```

### Paso 3: Si no está corriendo, iniciarlo
```bash
cd ~/capibara6/backend
# Activar entorno virtual si existe
source venv/bin/activate

# Iniciar el servidor
python3 server.py
# O
python3 capibara6_integrated_server_ollama.py
```

### Paso 4: Configurar para que se inicie automáticamente

Crear un servicio systemd o usar `screen`/`tmux`:

```bash
# Usando screen
screen -S capibara6-backend
cd ~/capibara6/backend
python3 server.py
# Presionar Ctrl+A luego D para detach

# O usando systemd (más robusto)
sudo nano /etc/systemd/system/capibara6-backend.service
```

Contenido del archivo systemd:
```ini
[Unit]
Description=Capibara6 Backend Server
After=network.target

[Service]
Type=simple
User=elect
WorkingDirectory=/home/elect/capibara6/backend
ExecStart=/usr/bin/python3 server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Luego:
```bash
sudo systemctl daemon-reload
sudo systemctl enable capibara6-backend
sudo systemctl start capibara6-backend
sudo systemctl status capibara6-backend
```

### Paso 5: Configurar firewall

Ejecuta el script:
```bash
bash fix_bounty2_firewall.sh
```

O manualmente:
```bash
gcloud compute firewall-rules create allow-bounty2-backend-5001 \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --target-tags bounty2 \
    --project=mamba-001
```

## Verificación

Después de configurar todo:

```bash
# Desde tu portátil local
curl http://34.12.166.76:5001/health
```

Deberías recibir una respuesta JSON con el estado del servidor.

