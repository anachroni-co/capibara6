# 🔄 Pasos Después de Reiniciar la VM

## 1️⃣ Obtener la Nueva IP

```bash
gcloud compute instances describe gemma-3-12b \
  --zone=europe-southwest1-b \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

O desde la consola de Google Cloud:
- https://console.cloud.google.com/compute/instances?project=mamba-001
- Ver la columna "IP externa"

## 2️⃣ Conectar por SSH (Desde el Navegador)

**URL directa:**
```
https://console.cloud.google.com/compute/instancesDetail/zones/europe-southwest1-b/instances/gemma-3-12b?project=mamba-001
```

1. Click en botón **SSH**
2. Esperar a que se abra la terminal

## 3️⃣ Verificar Qué Hay Instalado

Una vez conectado por SSH, ejecutar:

```bash
echo "=== Sistema ===" && \
uname -a && \
echo "=== Home directory ===" && \
ls -la ~/ && \
echo "=== Buscando llama.cpp ===" && \
find ~ -name "llama-server" -o -name "server" 2>/dev/null && \
echo "=== Buscando Ollama ===" && \
which ollama && \
echo "=== Procesos corriendo ===" && \
ps aux | grep -E 'llama|ollama' | grep -v grep && \
echo "=== Puerto 8080 ===" && \
sudo ss -tulnp | grep 8080
```

## 4️⃣ Iniciar el Servidor LLM

### Si tienes Llama.cpp:
```bash
# Navegar al directorio
cd ~/llama.cpp

# Iniciar servidor
./llama-server \
  --host 0.0.0.0 \
  --port 8080 \
  --model /path/to/gemma-3-12b.gguf \
  --ctx-size 4096
```

### Si tienes Ollama:
```bash
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

### Si tienes vLLM:
```bash
python -m vllm.entrypoints.api_server \
  --model google/gemma-3-12b \
  --host 0.0.0.0 \
  --port 8080
```

## 5️⃣ Verificar que Funciona

Desde la misma VM:
```bash
curl http://localhost:8080/health
```

## 6️⃣ Actualizar IP en el Chat

Si la IP cambió, actualizar en `web/chat-app.js`:

```javascript
const MODEL_CONFIG = {
    serverUrl: 'http://NUEVA_IP_AQUI:8080/completion',
    // ...
};
```

## 7️⃣ Probar desde el Chat

Abrir el chat y enviar un mensaje de prueba.

---

## ⚡ Inicio Rápido para Screen (Mantener Corriendo)

Si quieres que el servidor siga corriendo cuando cierres SSH:

```bash
# Instalar screen
sudo apt install screen -y

# Crear sesión
screen -S llama

# Iniciar servidor
./llama-server --host 0.0.0.0 --port 8080 --model model.gguf

# Desconectar: Ctrl + A, luego D
# Reconectar más tarde: screen -r llama
```

---

## 🔍 Troubleshooting

### Error: "Address already in use"
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

### Error: "llama-server not found"
```bash
# Buscar en todo el sistema
sudo find / -name "llama-server" 2>/dev/null
```

### Error: "Model not found"
```bash
# Buscar modelos .gguf
find ~ -name "*.gguf" 2>/dev/null
```

---

## 📝 Notas Importantes

- El servidor debe escuchar en `0.0.0.0` (no en `127.0.0.1`)
- El firewall ya está configurado para el puerto 8080
- Usa `screen` o `systemd` para mantener el servidor corriendo
- La IP puede cambiar en cada reinicio (considera reservar una IP estática)

---

**Una vez iniciado el servidor, comparte:**
1. La nueva IP
2. El output del comando de verificación
3. Si hay algún error al iniciar
