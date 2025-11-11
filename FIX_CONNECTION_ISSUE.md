# Solución al Problema de Conexión del Chat - Capibara6

## Descripción del Problema

El frontend del chat no se conectaba correctamente con los servicios backend. Se identificó que había discrepancias entre las URLs configuradas en los archivos del frontend y las URLs reales de los servicios backend.

## Análisis Realizado

Tras revisar la arquitectura de Capibara6, se identificaron las siguientes inconsistencias:

1. **Puertos incorrectos**: Los archivos de frontend estaban configurados para usar puerto 5000 en lugar del puerto 5001 correcto
2. **URLs desactualizadas**: Las configuraciones apuntaban a endpoints incorrectos
3. **Documentación inconsistente**: Diferentes archivos tenían diferentes configuraciones

## Arquitectura Correcta (según documentación oficial)

- **VM bounty2 (34.12.166.76)**: 
  - Ollama: puerto 11434
  - Backend Flask: puerto 5001 (archivo `server_gptoss.py`)
  
- **VM gpt-oss-20b (34.175.136.104)**:
  - TTS: puerto 5002
  - MCP: puerto 5003

## Cambios Realizados

### 1. Archivo `web/config.js`
- Cambiado puerto de backend de 5000 a 5001 tanto para desarrollo como producción
- Actualizado MODEL_CONFIG.serverUrl para apuntar al endpoint correcto `/api/chat`

### 2. Archivo `web/chat-app.js`
- Actualizado MODEL_CONFIG.serverUrl para usar la URL correcta del backend
- Modificada la configuración para que use la URL del archivo de configuración si está disponible

### 3. Archivo `web/script.js`
- Actualizados todos los puertos de 5000 a 5001 para el backend principal
- Asegurado que las URLs apuntan al puerto correcto (5001) del servicio Flask

### 4. Archivo `web/chatbot.js`
- Actualizadas las URLs de conexión para usar el puerto 5001 correcto

## Configuración Final Correcta

- **Desarrollo local**: `http://localhost:5001/api/chat`
- **Producción bounty2**: `http://34.12.166.76:5001/api/chat`
- **Endpoint para chat**: `/api/chat` en el servidor backend
- **Servidor backend**: `server_gptoss.py` corriendo en puerto 5001

## Validación

Para verificar que los cambios funcionan correctamente:

1. Asegúrese que el servidor backend está corriendo:
   ```bash
   cd backend
   python3 server_gptoss.py
   ```

2. Inicie el frontend:
   ```bash
   cd web
   python3 -m http.server 8000
   ```

3. Acceda a `http://localhost:8000/chat.html` y pruebe la funcionalidad del chat

## Comandos para Iniciar los Servicios

### En VM bounty2 (Modelos):
```bash
# Verificar Ollama
curl http://localhost:11434/api/tags

# Iniciar backend
cd ~/capibara6/backend
python3 server_gptoss.py
```

### En máquina local (Frontend):
```bash
# Iniciar frontend
cd web
python3 -m http.server 8000

# Abrir: http://localhost:8000/chat.html
```

## Solución de Problemas

Si aún hay problemas de conexión:

1. Verificar que el backend Flask esté corriendo en el puerto 5001
2. Validar que Ollama esté disponible en el puerto 11434
3. Confirmar que el modelo `gpt-oss:20b` esté disponible en Ollama
4. Revisar logs del backend para mensajes de error
5. Verificar CORS en el servidor backend

## Contacto

Para soporte adicional: marco@anachroni.co