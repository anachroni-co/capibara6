# 🔧 Crear Servicio Systemd para Gemma Server

## Para que el servidor se inicie automáticamente al arrancar la VM

### 1. Crear archivo de servicio

```bash
sudo nano /etc/systemd/system/gemma-server.service
```

### 2. Contenido del archivo:

```ini
[Unit]
Description=Gemma 3 12B LLM Server
After=network.target

[Service]
Type=simple
User=gmarco
WorkingDirectory=/home/gmarco/llama.cpp
ExecStart=/home/gmarco/llama.cpp/build/bin/llama-server --host 0.0.0.0 --port 8080 --model /mnt/data/models/gemma-3-12b.Q4_K_M.gguf --ctx-size 4096 --n-threads 16 --n-gpu-layers 0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Guardar y salir

- Presiona `Ctrl + X`
- Luego `Y`
- Luego `Enter`

### 4. Habilitar y arrancar el servicio

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar para inicio automático
sudo systemctl enable gemma-server

# Iniciar el servicio ahora
sudo systemctl start gemma-server

# Verificar estado
sudo systemctl status gemma-server
```

### 5. Comandos útiles

```bash
# Ver estado
sudo systemctl status gemma-server

# Ver logs
sudo journalctl -u gemma-server -f

# Reiniciar
sudo systemctl restart gemma-server

# Detener
sudo systemctl stop gemma-server

# Deshabilitar inicio automático
sudo systemctl disable gemma-server
```

## ✅ Ventajas

- ✅ Se inicia automáticamente al arrancar la VM
- ✅ Se reinicia automáticamente si falla
- ✅ Logs centralizados con journalctl
- ✅ No necesitas screen ni SSH para mantenerlo corriendo

## 🎯 Una vez configurado

Cada vez que reinicies la VM:
1. La VM arranca
2. El servidor llama.cpp se inicia automáticamente
3. En 30-60 segundos está listo para recibir peticiones

Solo necesitas actualizar la IP en el chat cuando cambie.
