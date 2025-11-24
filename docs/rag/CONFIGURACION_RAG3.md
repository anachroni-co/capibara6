# Configuración de RAG3

## 📋 Información de la VM

- **Nombre**: rag3
- **IP Pública**: `34.105.131.8`
- **Zona**: europe-west2-c
- **Proyecto**: mamba-001
- **Puerto del servicio RAG**: 8000

## 🔌 Servicios Configurados

### RAG Server
- **URL Base**: `http://34.105.131.8:8000`
- **API REST**: `http://34.105.131.8:8000/api`
- **Health Check**: `http://34.105.131.8:8000/health`

### Endpoints Disponibles

1. **Health Check**
   - URL: `http://34.105.131.8:8000/health`
   - Método: GET
   - Descripción: Verifica estado del servicio

2. **Guardar Mensajes**
   - URL: `http://34.105.131.8:8000/api/messages`
   - Método: POST
   - Body:
     ```json
     {
       "session_id": "string",
       "content": "string",
       "message_role": "user|assistant",
       "metadata": {
         "user_id": "string",
         "timestamp": "ISO8601"
       }
     }
     ```

3. **Guardar Archivos**
   - URL: `http://34.105.131.8:8000/api/files`
   - Método: POST
   - Content-Type: multipart/form-data
   - Form Fields:
     - `file`: Archivo a subir
     - `user_id`: ID del usuario
     - `session_id`: ID de la sesión
     - `metadata`: JSON con metadata adicional

4. **Búsqueda Semántica**
   - URL: `http://34.105.131.8:8000/api/search/semantic`
   - Método: POST
   - Body:
     ```json
     {
       "query": "string",
       "collection": "string",
       "n_results": 5
     }
     ```

5. **Búsqueda en RAG**
   - URL: `http://34.105.131.8:8000/api/search/rag`
   - Método: POST
   - Body:
     ```json
     {
       "query": "string",
       "n_results": 5
     }
     ```

## 🔧 Configuración en el Frontend

### 1. Configuración en `config.js`

```javascript
VMS: {
    RAG3: {
        ip: '34.105.131.8',
        services: {
            rag: 'http://34.105.131.8:8000',
            api: 'http://34.105.131.8:8000/api'
        }
    }
}
```

### 2. Integración RAG (`rag-integration.js`)

La clase `RAGIntegration` se configura automáticamente usando `CHATBOT_CONFIG.VMS.RAG3.services.rag`.

**Métodos disponibles:**

- `saveMessage(role, content, metadata)`: Guarda un mensaje en RAG
- `saveFile(file, metadata)`: Guarda un archivo en RAG
- `searchHistory(query, nResults)`: Busca en el historial
- `getSessionHistory()`: Obtiene historial de la sesión actual
- `checkConnection()`: Verifica conexión con RAG

**Uso:**

```javascript
// La instancia global está disponible automáticamente
window.ragIntegration.saveMessage('user', 'Hola mundo', {});
```

## 🧪 Verificación de Conexión

### Desde Terminal (Local)

```bash
# Test básico
curl http://34.105.131.8:8000/health

# Test de guardado de mensaje
curl -X POST http://34.105.131.8:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_session",
    "content": "Test message",
    "message_role": "user",
    "metadata": {
      "user_id": "test_user",
      "timestamp": "2025-11-13T17:00:00Z"
    }
  }'
```

### Script Automatizado

```bash
# Ejecutar script de prueba
./scripts/test_rag3_connection.sh
```

### Desde el Frontend (Console)

```javascript
// Test de conexión
await window.ragIntegration.checkConnection();

// Test de guardado
await window.ragIntegration.saveMessage('user', 'Test message');
```

## 🔐 Configuración de Firewall

Asegúrate de que el firewall de GCloud permita conexiones al puerto 8000:

```bash
# Ver reglas de firewall
gcloud compute firewall-rules list --project=mamba-001

# Crear regla si es necesaria
gcloud compute firewall-rules create allow-rag-8000 \
  --project=mamba-001 \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=rag3
```

## 📝 Acceso SSH

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

## 🔍 Verificación en la VM

Una vez conectado por SSH a rag3:

```bash
# Ver servicios corriendo en puerto 8000
sudo netstat -tulpn | grep :8000

# Ver procesos del servicio RAG
ps aux | grep rag

# Ver logs del servicio
journalctl -u rag-service -f
```

## 🚀 Iniciar Servicio RAG (si no está corriendo)

```bash
# Conectarse a la VM
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Navegar al directorio del servicio
cd /path/to/rag/service

# Iniciar con screen (para mantenerlo corriendo)
screen -S rag-service
python3 app.py --port 8000
# Ctrl+A, D para desconectar sin cerrar

# O con systemd (si está configurado)
sudo systemctl start rag-service
sudo systemctl enable rag-service
```

## 📊 Monitoreo

### Estado del Servicio

```bash
# Verificar que el servicio esté respondiendo
curl -s http://34.105.131.8:8000/health | jq

# Ver estadísticas
curl -s http://34.105.131.8:8000/api/stats | jq
```

### Logs

```bash
# Ver logs en tiempo real
tail -f /var/log/rag-service.log

# O con journalctl
journalctl -u rag-service -f
```

## ⚠️ Troubleshooting

### Problema: No responde en el puerto 8000

**Solución:**

1. Verificar que el servicio esté corriendo:
   ```bash
   ps aux | grep rag
   ```

2. Verificar que el puerto esté abierto:
   ```bash
   sudo netstat -tulpn | grep :8000
   ```

3. Verificar logs:
   ```bash
   journalctl -u rag-service -n 50
   ```

### Problema: Error de conexión desde el frontend

**Solución:**

1. Verificar configuración CORS en el servicio RAG
2. Verificar que la IP sea accesible desde tu red
3. Verificar firewall de GCloud

### Problema: Error 404 en endpoints

**Solución:**

1. Verificar que la versión del servicio RAG esté actualizada
2. Revisar documentación de la API
3. Verificar que el endpoint exista: `curl http://34.105.131.8:8000/api`

## 🔗 Integración con Frontend

La integración con el frontend se realiza automáticamente a través de:

1. **config.js**: Configuración centralizada de URLs
2. **rag-integration.js**: Clase que gestiona la comunicación
3. **chat-page.js**: Uso de RAG para guardar mensajes
4. **chat-app.js**: Uso de RAG para búsqueda y contexto

El frontend guarda automáticamente:
- Mensajes de usuario y asistente
- Archivos subidos
- Metadata de sesión
- Datos de usuario

## ✅ Checklist de Configuración

- [x] IP de RAG3 obtenida: `34.105.131.8`
- [x] Configuración actualizada en `config.js`
- [x] Integración RAG configurada en `rag-integration.js`
- [x] Script de prueba creado
- [ ] Verificar que el servicio RAG esté corriendo en rag3
- [ ] Verificar firewall de GCloud
- [ ] Test de conexión desde frontend
- [ ] Test de guardado de mensajes
- [ ] Test de guardado de archivos

## 📚 Próximos Pasos

1. Conectarse a la VM rag3 y verificar que el servicio esté corriendo
2. Ejecutar el script de prueba: `./scripts/test_rag3_connection.sh`
3. Probar desde el frontend en `http://localhost:8000`
4. Verificar que los mensajes se guarden correctamente
5. Configurar backups de la base de datos RAG

