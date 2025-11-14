# Solución al Problema de Conexión del Chat - Capibara6

## Descripción del Problema

El frontend del chat no se conectaba correctamente con los servicios backend. Se identificaron dos problemas principales:

1. **Discrepancias de URLs y puertos**: Los archivos de frontend estaban configurados para usar puertos incorrectos
2. **Problemas de CORS**: Intentar conectar desde localhost (frontend) a una IP remota (backend) causaba errores de Cross-Origin

## Análisis Realizado

Tras revisar la arquitectura de Capibara6, se identificaron las siguientes inconsistencias:

1. **Puertos incorrectos**: Los archivos de frontend estaban configurados para usar puerto 5000 en lugar del puerto 5001 correcto
2. **Problemas CORS**: El frontend en localhost no podía hacer peticiones a la IP remota del backend debido a políticas de seguridad del navegador
3. **Configuración de CORS insuficiente**: El backend no estaba configurado adecuadamente para permitir peticiones desde localhost

## Arquitectura Correcta (según documentación oficial)

- **VM bounty2 (34.12.166.76)**: 
  - Ollama: puerto 11434
  - Backend Flask: puerto 5001 (archivo `server_gptoss.py`)
  
- **VM gpt-oss-20b (34.175.136.104)**:
  - TTS: puerto 5002
  - MCP: puerto 5003

## Solución Implementada

### Solución 1: Configuración de CORS en backend
- Actualizado `backend/server_gptoss.py` para permitir peticiones desde localhost y otros orígenes
- Configurado puerto por defecto a 5001 en lugar de 5000

### Solución 2: Proxy CORS local (recomendado para desarrollo)
- Creado y actualizado `backend/cors_proxy_local.py` para evitar problemas CORS en desarrollo
- El proxy reenvía peticiones desde localhost:8001/api/* a la IP remota del backend (34.12.166.76:5001/api/*)
- Las rutas como `http://localhost:8001/api/health` se mapean a `http://34.12.166.76:5001/api/health`
- También maneja rutas directas como `http://localhost:8001/health` mapeándolas a `http://34.12.166.76:5001/api/health`

### Solución 3: Actualización de configuración del frontend
- Archivo `web/config.js`: Configurado para usar proxy local cuando en localhost
- Archivo `web/chat-app.js`: Actualizado para usar la URL correcta del proxy
- Archivo `web/script.js`: Configurado para usar proxy local en desarrollo
- Archivo `web/chatbot.js`: Actualizado para usar proxy local

## Configuración Final Correcta

- **Desarrollo local**: 
  - `http://localhost:8001/api/health` → `http://34.12.166.76:5001/api/health`
  - `http://localhost:8001/api/chat` → `http://34.12.166.76:5001/api/chat`
- **Producción bounty2**: `http://34.12.166.76:5001/api/chat`
- **Endpoint para chat**: `/api/chat` en el servidor backend
- **Servidor backend**: `server_gptoss.py` corriendo en puerto 5001

## Validación

### Opción 1: Con proxy CORS (recomendado para desarrollo)
1. Inicie el proxy CORS local:
   ```bash
   cd backend
   python3 cors_proxy_local.py
   ```

2. Inicie el frontend:
   ```bash
   cd web
   python3 -m http.server 8000
   ```

3. Acceda a `http://localhost:8000/chat.html` y pruebe la funcionalidad del chat

### Opción 2: Usando el script de inicio
1. Ejecute el script de inicio:
   ```bash
   ./start_capibara6.sh
   ```

2. Luego inicie el frontend:
   ```bash
   cd web
   python3 -m http.server 8000
   ```

3. Acceda a `http://localhost:8000/chat.html`

## Comandos para Iniciar los Servicios

### En VM bounty2 (Modelos):
```bash
# Verificar Ollama
curl http://localhost:11434/api/tags

# Iniciar backend con puerto correcto
cd ~/capibara6/backend
python3 server_gptoss.py
```

### En máquina local (Frontend con proxy):
```bash
# Iniciar proxy CORS local
cd backend
python3 cors_proxy_local.py

# En otra terminal, iniciar frontend
cd web
python3 -m http.server 8000

# Abrir: http://localhost:8000/chat.html
```

## Solución de Problemas

### Problemas comunes:
1. **Proxy CORS no responde**: Verifique que el puerto 8001 esté disponible
2. **Backend remoto no accesible**: Verifique que la IP remota esté activa y el puerto 5001 abierto
3. **Errores de conexión**: Revise los logs en `cors_proxy.log` o `backend.log`

### Verificación de servicios:
```bash
# Verificar proxy local
curl http://localhost:8001/

# Verificar backend remoto (si tiene acceso directo)
curl http://34.12.166.76:5001/api/health
```

## Contacto

Para soporte adicional: marco@anachroni.co