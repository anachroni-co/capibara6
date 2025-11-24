# 🚨 Solución Inmediata: Backend no está corriendo en bounty2

## Diagnóstico

✅ **Firewall configurado**: Las reglas de firewall están creadas  
✅ **Ollama funcionando**: Puerto 11434 accesible  
❌ **Backend Flask NO está corriendo**: Puertos 5000 y 5001 cerrados

## 🔧 Solución: Iniciar el Backend en bounty2

### Paso 1: Conectarse a bounty2

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### Paso 2: Verificar qué archivos de servidor existen

```bash
cd ~/capibara6/backend
ls -la *.py | grep -E "(server|integrated)"
```

Posibles archivos:
- `server.py`
- `capibara6_integrated_server_ollama.py`
- `server_gptoss.py`
- `capibara6_integrated_server.py`

### Paso 3: Iniciar el backend

**Opción A: Servidor integrado con Ollama (RECOMENDADO)**
```bash
cd ~/capibara6/backend
python3 capibara6_integrated_server_ollama.py
```

**Opción B: Servidor principal**
```bash
cd ~/capibara6/backend
python3 server.py
```

**Opción C: Servidor GPT-OSS**
```bash
cd ~/capibara6/backend
python3 server_gptoss.py
```

### Paso 4: Verificar que esté escuchando correctamente

El servidor debe mostrar algo como:
```
🌐 Servidor escuchando en puerto 5001
🔗 URL: http://0.0.0.0:5001
```

**IMPORTANTE**: Debe escuchar en `0.0.0.0` (no solo `localhost` o `127.0.0.1`) para ser accesible desde fuera.

### Paso 5: Probar desde tu portátil

En otra terminal (sin cerrar la conexión SSH):

```bash
curl http://34.12.166.76:5001/health
```

Deberías recibir una respuesta JSON con el estado del servidor.

## 🔄 Mantener el Backend Corriendo

### Opción 1: Usar screen (Simple)

```bash
# Dentro de bounty2
screen -S capibara6-backend
cd ~/capibara6/backend
python3 server.py
# Presionar Ctrl+A luego D para detach (dejar corriendo en segundo plano)
```

Para volver a ver el proceso:
```bash
screen -r capibara6-backend
```

### Opción 2: Usar systemd (Recomendado para producción)

Crear archivo de servicio:
```bash
sudo nano /etc/systemd/system/capibara6-backend.service
```

Contenido:
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
Environment="PORT=5001"

[Install]
WantedBy=multi-user.target
```

Activar y iniciar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable capibara6-backend
sudo systemctl start capibara6-backend
sudo systemctl status capibara6-backend
```

## ✅ Verificación Final

Después de iniciar el backend:

1. **Desde bounty2**:
```bash
curl http://localhost:5001/health
```

2. **Desde tu portátil**:
```bash
curl http://34.12.166.76:5001/health
```

3. **Desde el frontend**:
   - Abre `web/chat.html` en tu navegador
   - Abre la consola (F12)
   - Verifica que la URL sea `http://34.12.166.76:5001`
   - Intenta enviar un mensaje

## 🐛 Troubleshooting

### El servidor no inicia

**Error de dependencias**:
```bash
pip3 install -r requirements.txt
```

**Error de puerto en uso**:
```bash
# Ver qué está usando el puerto
sudo lsof -i :5001
# Matar el proceso si es necesario
kill -9 <PID>
```

### El servidor inicia pero no es accesible desde fuera

**Verificar que escuche en 0.0.0.0**:
```bash
sudo ss -tulnp | grep 5001
# Debe mostrar: 0.0.0.0:5001 (no 127.0.0.1:5001)
```

**Verificar firewall**:
```bash
gcloud compute firewall-rules list --project=mamba-001 --filter="targetTags:bounty2"
```

## 📋 Checklist

- [ ] Conectado a bounty2
- [ ] Backend iniciado
- [ ] Servidor escuchando en `0.0.0.0:5001`
- [ ] Health check funciona desde bounty2: `curl http://localhost:5001/health`
- [ ] Health check funciona desde local: `curl http://34.12.166.76:5001/health`
- [ ] Frontend puede conectarse y enviar mensajes

## 🎯 Una vez funcionando

El frontend debería poder:
- Conectarse al backend en `http://34.12.166.76:5001`
- Enviar mensajes a `/api/chat`
- Recibir respuestas del modelo a través de Ollama

