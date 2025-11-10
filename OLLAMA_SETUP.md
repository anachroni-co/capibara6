# 🦫 Capibara6 - Guía de Configuración de Ollama

## 📦 ¿Qué es Ollama?

Ollama es un servidor de modelos de IA que permite ejecutar modelos de lenguaje localmente de forma sencilla. Capibara6 usa Ollama para servir el modelo GPT-OSS-20B.

**Sitio oficial**: https://ollama.ai

---

## 🚀 Instalación de Ollama

### En la VM de modelos (bounty2):

```bash
# Conectarse a la VM
./ssh-bounty2.sh

# Instalar Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar instalación
ollama --version
```

### Instalación local (para desarrollo):

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Descargar desde: https://ollama.ai/download

---

## 📥 Cargar el modelo GPT-OSS-20B

### Opción 1: Si el modelo ya está descargado

```bash
# Listar modelos disponibles
ollama list

# Si gpt-oss-20b aparece en la lista, ya está listo
```

### Opción 2: Descargar/importar el modelo

```bash
# Si tienes un Modelfile
ollama create gpt-oss-20b -f /path/to/Modelfile

# Si tienes archivos GGUF
ollama create gpt-oss-20b -f - <<EOF
FROM /path/to/model.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF
```

### Opción 3: Usar un modelo compatible de Ollama

Si no tienes GPT-OSS-20B específicamente, puedes usar otro modelo:

```bash
# Modelos recomendados:
ollama pull llama2:13b
ollama pull mixtral:8x7b
ollama pull codellama:13b

# Luego actualiza .env:
# OLLAMA_MODEL=llama2:13b
```

---

## ▶️ Iniciar Ollama como servicio

### Linux (systemd):

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/ollama.service
```

Contenido:
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=elect
Environment="OLLAMA_HOST=0.0.0.0:11434"
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Habilitar y arrancar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### Manualmente (para pruebas):

```bash
# Iniciar servidor (expuesto en todas las interfaces)
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# O solo localhost
ollama serve
```

---

## 🔍 Verificación

### Verificar que Ollama está corriendo:

```bash
# Localmente
curl http://localhost:11434/api/tags

# Desde otra máquina
curl http://34.12.166.76:11434/api/tags
```

Deberías ver una lista de modelos en JSON.

### Probar generación de texto:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss-20b",
  "prompt": "Hola, ¿cómo estás?",
  "stream": false
}'
```

---

## 🔥 Firewall

### Abrir puerto 11434 en Google Cloud:

```bash
gcloud compute firewall-rules create allow-ollama \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:11434 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow Ollama API"
```

### Firewall local (ufw):

```bash
sudo ufw allow 11434/tcp
sudo ufw reload
```

---

## ⚙️ Configuración de Capibara6

### En la VM bounty2:

```bash
cd ~/capibara6/backend
nano .env
```

Configuración:
```env
PORT=5001
OLLAMA_URL=http://localhost:11434  # O http://127.0.0.1:11434
OLLAMA_MODEL=gpt-oss-20b
OLLAMA_TIMEOUT=120
USE_DEMO_MODE=false
```

### Desde desarrollo local (conectándose a VM):

```bash
cd ~/capibara6/backend
nano .env
```

Configuración:
```env
PORT=5001
OLLAMA_URL=http://34.12.166.76:11434
OLLAMA_MODEL=gpt-oss-20b
OLLAMA_TIMEOUT=120
USE_DEMO_MODE=false
```

---

## 🐛 Troubleshooting

### "Connection refused" al acceder a Ollama

**Causa**: Ollama está escuchando solo en localhost

**Solución**:
```bash
# Detener Ollama
sudo systemctl stop ollama

# Editar servicio para exponer en todas las interfaces
sudo nano /etc/systemd/system/ollama.service
# Agregar: Environment="OLLAMA_HOST=0.0.0.0:11434"

# Reiniciar
sudo systemctl daemon-reload
sudo systemctl start ollama

# Verificar
netstat -tulpn | grep 11434
# Debe mostrar: 0.0.0.0:11434 en lugar de 127.0.0.1:11434
```

### Modelo no encontrado

**Error**: `model 'gpt-oss-20b' not found`

**Solución**:
```bash
# Listar modelos disponibles
ollama list

# Usar un modelo que exista
# Por ejemplo: llama2, mixtral, etc.

# Actualizar .env con el modelo correcto
OLLAMA_MODEL=llama2
```

### Respuestas muy lentas

**Posibles causas**:
- Modelo muy grande para la VM
- Poca RAM/GPU

**Soluciones**:
```bash
# Usar un modelo más pequeño
ollama pull llama2:7b

# Aumentar timeout en .env
OLLAMA_TIMEOUT=300

# Verificar recursos
free -h
nvidia-smi  # Si tienes GPU
```

### Puerto bloqueado

```bash
# Verificar que el puerto esté abierto
sudo netstat -tulpn | grep 11434

# Si no aparece nada, Ollama no está corriendo
sudo systemctl status ollama

# Verificar firewall
sudo ufw status | grep 11434
```

---

## 📊 Comandos útiles

```bash
# Listar modelos
ollama list

# Eliminar modelo
ollama rm modelo-name

# Ver logs
sudo journalctl -u ollama -f

# Detener servicio
sudo systemctl stop ollama

# Reiniciar servicio
sudo systemctl restart ollama

# Ver uso de recursos
ps aux | grep ollama
```

---

## 🔗 Recursos

- **Documentación oficial**: https://github.com/jmorganca/ollama
- **API Reference**: https://github.com/jmorganca/ollama/blob/main/docs/api.md
- **Modelos disponibles**: https://ollama.ai/library
- **Discord**: https://discord.gg/ollama

---

**Última actualización**: 2025-11-10
**Para Capibara6 v2.0**
