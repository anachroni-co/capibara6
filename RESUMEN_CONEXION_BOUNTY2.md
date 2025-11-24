# 🔗 Resumen: Conexión Frontend ↔ Backend bounty2

## ✅ Estado Actual

### Lo que funciona:
- **Ollama**: Puerto 11434 ✅ ACCESIBLE
  - IP: `34.12.166.76:11434`
  - Modelos disponibles: `mistral:latest`, `phi3:mini`, `gpt-oss:20b`

### Lo que NO funciona:
- **Backend Flask**: Puertos 5000 y 5001 ❌ NO ACCESIBLES
  - Puerto 5000: Connection refused
  - Puerto 5001: Connection refused
  - IP esperada: `34.12.166.76:5001`

## 🔧 Acciones Realizadas

1. ✅ **Configuración del frontend actualizada**
   - `web/config.js` ahora usa `http://34.12.166.76:5001` por defecto en desarrollo local
   - Compatible con configuración de VMs si está disponible

2. ✅ **Scripts de diagnóstico creados**
   - `setup_bounty2_backend.sh` - Configuración completa
   - `test_bounty2_complete.sh` - Diagnóstico completo
   - `fix_bounty2_firewall.sh` - Configuración de firewall

3. ⏳ **Firewall configurado** (ejecutado, verificar resultado)
   - Regla para puerto 5001 creada
   - Tag `bounty2` añadido a la VM

## 🚨 Problema Principal

**El backend Flask NO está corriendo en bounty2** o **no está escuchando en los puertos esperados**.

## 📋 Próximos Pasos CRÍTICOS

### Paso 1: Verificar estado del backend en bounty2

Conéctate a la VM y verifica:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

Dentro de la VM:

```bash
# Ver procesos Python corriendo
ps aux | grep python | grep -E "(server|flask|capibara6)"

# Ver puertos abiertos
sudo ss -tulnp | grep -E "(5000|5001|8000|8080)"

# Verificar si hay algún servidor escuchando
sudo netstat -tulnp | grep LISTEN
```

### Paso 2: Iniciar el backend si no está corriendo

Si no hay procesos corriendo, inicia el backend:

```bash
cd ~/capibara6/backend

# Opción 1: Servidor integrado con Ollama
python3 capibara6_integrated_server_ollama.py

# Opción 2: Servidor principal
python3 server.py

# Opción 3: Servidor GPT-OSS
python3 server_gptoss.py
```

**Importante**: El servidor debe escuchar en `0.0.0.0` (no solo `localhost`) para ser accesible desde fuera.

### Paso 3: Verificar firewall

Después de iniciar el backend, verifica que el firewall permita el tráfico:

```bash
# Desde tu portátil local
curl http://34.12.166.76:5001/health

# Si funciona, deberías ver una respuesta JSON
```

### Paso 4: Configurar inicio automático (Opcional pero recomendado)

Para que el backend se inicie automáticamente al reiniciar la VM:

```bash
# Usando screen (simple)
screen -S capibara6-backend
cd ~/capibara6/backend
python3 server.py
# Presionar Ctrl+A luego D para detach

# O usando systemd (más robusto)
sudo nano /etc/systemd/system/capibara6-backend.service
```

Contenido del servicio systemd:
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

Luego:
```bash
sudo systemctl daemon-reload
sudo systemctl enable capibara6-backend
sudo systemctl start capibara6-backend
sudo systemctl status capibara6-backend
```

## 🧪 Pruebas de Conexión

### Desde tu portátil local:

```bash
# Probar health check
curl http://34.12.166.76:5001/health

# Probar endpoint de chat (si está disponible)
curl -X POST http://34.12.166.76:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'

# Probar Ollama directamente
curl http://34.12.166.76:11434/api/tags
```

### Desde el frontend:

1. Abre `web/chat.html` en tu navegador (servido desde `localhost`)
2. Abre la consola del navegador (F12)
3. Verifica que la URL del backend sea `http://34.12.166.76:5001`
4. Intenta enviar un mensaje y verifica los errores en la consola

## 📝 Configuración del Frontend

El frontend está configurado para usar:
- **Desarrollo local**: `http://34.12.166.76:5001` (bounty2)
- **Producción**: `https://www.capibara6.com` (Vercel)

Si necesitas cambiar el puerto, edita `web/config.js`:
```javascript
const BOUNTY2_IP = '34.12.166.76';
// Cambiar el puerto aquí si es necesario
BACKEND_URL: `http://${BOUNTY2_IP}:5001`  // Cambiar 5001 por el puerto correcto
```

## 🐛 Troubleshooting

### Error: "Connection refused"
- El backend no está corriendo
- El puerto está cerrado por firewall
- El backend está escuchando solo en localhost

**Solución**: Verificar que el backend esté corriendo y escuchando en `0.0.0.0`

### Error: "Timeout"
- El firewall está bloqueando el tráfico
- El backend no está respondiendo

**Solución**: Verificar reglas de firewall y que el backend esté funcionando

### Error: CORS en el navegador
- El backend no tiene CORS configurado correctamente

**Solución**: Verificar que el backend tenga `CORS(app)` o `CORS(app, origins=['*'])`

## ✅ Checklist Final

- [ ] Backend corriendo en bounty2
- [ ] Backend escuchando en `0.0.0.0:5001` (o puerto correcto)
- [ ] Firewall configurado para permitir puerto 5001
- [ ] Tag `bounty2` en la VM
- [ ] Health check responde desde local: `curl http://34.12.166.76:5001/health`
- [ ] Frontend configurado con IP correcta
- [ ] Frontend puede conectarse y enviar mensajes

## 📞 Comandos Útiles

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Ver logs del backend (si está corriendo)
tail -f ~/capibara6/backend/logs/*.log

# Verificar firewall
gcloud compute firewall-rules list --project=mamba-001 --filter="targetTags:bounty2"

# Probar conexión
curl http://34.12.166.76:5001/health
```

