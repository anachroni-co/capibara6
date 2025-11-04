# 🚀 Guía para Iniciar Servidor Gemma-3-12B

## 📋 Información del Servidor

- **Nombre:** gemma-3-12b
- **IP Externa:** 34.175.89.158
- **Puerto:** 8080
- **Zona:** europe-southwest1-b
- **Firewall:** ✅ Configurado (allow-llama-server-8080)

## 🔌 Paso 1: Conectar por SSH

### Desde Google Cloud Console:
1. Ir a: https://console.cloud.google.com/compute/instances
2. Encontrar instancia: `gemma-3-12b`
3. Click en botón **SSH**

### Desde Terminal/WSL:
```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

## 🔍 Paso 2: Verificar Qué Tienes Instalado

Una vez conectado, ejecuta:

```bash
# Ver directorio home
ls -la ~/

# Buscar llama.cpp
which llama-server
find / -name "llama-server" 2>/dev/null

# Buscar ollama
which ollama

# Buscar vLLM
which vllm
pip list | grep vllm

# Ver modelos
ls -la /models/ 2>/dev/null
ls -la ~/models/ 2>/dev/null
```

## 🚀 Paso 3: Iniciar el Servidor

### Si tienes **Llama.cpp:**
```bash
# Navegar al directorio
cd ~/llama.cpp

# Iniciar servidor
./llama-server \
  --host 0.0.0.0 \
  --port 8080 \
  --model /path/to/gemma-3-12b.gguf \
  --ctx-size 4096 \
  --n-gpu-layers 99
```

### Si tienes **Ollama:**
```bash
# Iniciar servidor
OLLAMA_HOST=0.0.0.0:8080 ollama serve &

# Cargar modelo
ollama run gemma:12b
```

### Si tienes **vLLM:**
```bash
# Iniciar servidor
python -m vllm.entrypoints.api_server \
  --model google/gemma-3-12b \
  --host 0.0.0.0 \
  --port 8080
```

### Si tienes **HuggingFace Text Generation Inference:**
```bash
# Iniciar servidor
text-generation-launcher \
  --model-id google/gemma-3-12b \
  --hostname 0.0.0.0 \
  --port 8080
```

## 🧪 Paso 4: Verificar que Funciona

### Desde el mismo servidor:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/v1/models
```

### Desde tu PC:
```bash
curl http://34.175.89.158:8080/health
```

## 🔧 Si el Servidor No Está Instalado

### Instalar Llama.cpp (ARM64):
```bash
# Instalar dependencias
sudo apt update
sudo apt install -y build-essential cmake git

# Clonar repositorio
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Compilar
cmake -B build
cmake --build build --config Release

# Iniciar servidor
./build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8080 \
  --model /path/to/model.gguf
```

### Instalar Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

## 📝 Mantener el Servidor Corriendo

### Usar screen (recomendado):
```bash
# Instalar screen
sudo apt install screen

# Crear sesión
screen -S gemma-server

# Iniciar servidor
./llama-server --host 0.0.0.0 --port 8080 --model model.gguf

# Desconectar (Ctrl + A, luego D)
# Reconectar: screen -r gemma-server
```

### Usar systemd (persistente):
```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/gemma-server.service
```

Contenido:
```ini
[Unit]
Description=Gemma 3 12B LLM Server
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/llama.cpp
ExecStart=/home/YOUR_USER/llama.cpp/llama-server --host 0.0.0.0 --port 8080 --model /path/to/model.gguf
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gemma-server
sudo systemctl start gemma-server
sudo systemctl status gemma-server
```

## 🆘 Problemas Comunes

### Error: "Address already in use"
```bash
# Ver qué usa el puerto 8080
sudo netstat -tulnp | grep 8080

# Matar proceso
sudo kill -9 <PID>
```

### Error: "Permission denied"
```bash
# Usar puerto > 1024 o ejecutar con sudo
sudo ./llama-server --host 0.0.0.0 --port 8080
```

### Error: "Cannot find model"
```bash
# Verificar ruta del modelo
ls -la /path/to/model.gguf

# Descargar modelo si es necesario
huggingface-cli download google/gemma-3-12b
```

## ✅ Verificación Final

Una vez iniciado el servidor, deberías poder:

1. **Desde el servidor:**
   ```bash
   curl http://localhost:8080/health
   ```

2. **Desde tu PC:**
   ```bash
   curl http://34.175.89.158:8080/health
   ```

3. **Desde el navegador:**
   ```
   http://34.175.89.158:8080
   ```

4. **Desde el chat de Capibara6:**
   - El chat debería conectar automáticamente
   - Probar enviando un mensaje

## 📞 Comandos Útiles

```bash
# Ver logs del servidor
tail -f /var/log/gemma-server.log

# Ver uso de recursos
htop

# Ver procesos
ps aux | grep llama

# Reiniciar servidor
sudo systemctl restart gemma-server
```

---

**Siguiente paso:** Conéctate por SSH y ejecuta los comandos de verificación para ver qué tienes instalado. 🔧
