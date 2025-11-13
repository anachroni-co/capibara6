# 🔗 Integración Completa Frontend-RAG

## 📋 Resumen

Configuración para conectar el frontend con el servicio RAG en rag3 para guardar y buscar datos del usuario (chats, mensajes, archivos).

## ✅ Cambios Realizados

### 1. Archivo `web/config.js`
- ✅ Agregada configuración para RAG3
- ✅ Agregados endpoints RAG en ENDPOINTS

### 2. Archivo `web/rag-integration.js` (NUEVO)
- ✅ Clase `RAGIntegration` para gestionar conexión con RAG
- ✅ Métodos para guardar mensajes, archivos
- ✅ Métodos para buscar en historial
- ✅ Gestión de usuario y sesión

## 🔧 Configuración Pendiente

### Paso 1: Obtener IP de rag3

```bash
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### Paso 2: Actualizar `web/rag-integration.js`

Reemplazar `[IP_RAG3]` con la IP real obtenida:

```javascript
this.ragBaseURL = window.location.hostname === 'localhost'
    ? 'http://[IP_RAG3_REAL]:8000'  // Reemplazar con IP real
    : 'https://www.capibara6.com/api/rag';
```

### Paso 3: Verificar Servicio RAG en rag3

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Verificar puerto del servicio
sudo ss -tulnp | grep -E "(8000|8001)"

# Verificar que responde
curl http://localhost:8000/health
# O
curl http://localhost:8001/health
```

### Paso 4: Integrar en el Frontend

Agregar el script en `chat.html` o `index.html`:

```html
<!-- Después de config.js -->
<script src="rag-api-client.js"></script>
<script src="rag-integration.js"></script>
```

### Paso 5: Usar en el Código del Chat

Modificar `chat-app.js` o `chat-page.js` para guardar en RAG:

```javascript
// Después de guardar en localStorage
if (window.ragIntegration) {
    await window.ragIntegration.saveMessage('user', messageContent);
    // Y cuando llegue la respuesta del asistente:
    await window.ragIntegration.saveMessage('assistant', aiResponse);
}
```

## 📝 Endpoints del Servicio RAG

### Base URL: `http://[IP_RAG3]:8000`

- `GET /health` - Health check
- `POST /api/search/semantic` - Búsqueda semántica
- `POST /api/search/rag` - Búsqueda RAG completa
- `GET /api/messages` - Listar mensajes
- `POST /api/messages` - Crear mensaje
- `GET /api/sessions/{session_id}` - Mensajes de sesión
- `GET /api/files` - Listar archivos
- `POST /api/files` - Subir archivo
- `GET /api/users` - Listar usuarios
- `POST /api/users` - Crear usuario

## 🔄 Flujo de Guardado

```
Usuario envía mensaje
    ↓
Frontend (chat-app.js)
    ↓
1. Guardar en localStorage (caché local) ✅
    ↓
2. Guardar en RAG (rag-integration.js) ⏳
    ↓
Servicio RAG (rag3:8000)
    ↓
PostgreSQL + ChromaDB + NebulaGraph
```

## 🧪 Pruebas

### Probar Conexión RAG

```javascript
// En consola del navegador
await window.ragIntegration.checkConnection();
```

### Probar Guardado

```javascript
// Guardar mensaje de prueba
await window.ragIntegration.saveMessage('user', 'Mensaje de prueba');
```

### Probar Búsqueda

```javascript
// Buscar en historial
const results = await window.ragIntegration.searchHistory('prueba');
console.log(results);
```

## ⚠️ Notas Importantes

1. **IP de rag3**: Debe obtenerse y configurarse antes de usar
2. **Firewall**: Asegurarse de que el puerto del servicio RAG esté abierto
3. **CORS**: El servicio RAG debe tener CORS configurado para `localhost:8000`
4. **Fallback**: El código tiene fallback a localStorage si RAG no está disponible

## 📚 Archivos Relacionados

- `web/rag-integration.js` - Integración RAG (NUEVO)
- `web/rag-api-client.js` - Cliente API RAG (existente)
- `backend/api_server.py` - Servicio RAG en rag3
- `backend/rag_client.py` - Cliente RAG para backend

## ✅ Checklist

- [x] Crear `rag-integration.js`
- [x] Actualizar `config.js` con endpoints RAG
- [ ] Obtener IP de rag3
- [ ] Actualizar `rag-integration.js` con IP real
- [ ] Verificar servicio RAG en rag3
- [ ] Integrar script en HTML
- [ ] Modificar código de chat para usar RAG
- [ ] Probar guardado y búsqueda
- [ ] Configurar CORS en servicio RAG si es necesario

