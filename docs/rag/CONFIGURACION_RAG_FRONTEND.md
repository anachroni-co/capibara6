# 🔗 Configuración de Conexión Frontend-RAG

## 📋 Objetivo

Conectar el frontend con el servicio RAG en rag3 para guardar:
- ✅ Chats del usuario
- ✅ Mensajes de conversación
- ✅ Archivos subidos
- ✅ Datos personales del usuario

## 🏗️ Arquitectura

```
Frontend (localhost:8000)
    ↓
Backend en bounty2 (34.12.166.76:5001)
    ↓ (guarda en RAG)
Servicio RAG en rag3 (IP pendiente)
    ↓
Base de datos PostgreSQL + ChromaDB + NebulaGraph
```

## 🔧 Configuración Necesaria

### 1. Obtener IP de rag3

```bash
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### 2. Verificar que el servicio RAG esté corriendo en rag3

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Verificar puerto del servicio RAG (probablemente 8000 u 8001)
sudo ss -tulnp | grep -E "(8000|8001)"

# Verificar que el servicio responda
curl http://localhost:8000/health
# O
curl http://localhost:8001/health
```

### 3. Configurar el Backend para Guardar en RAG

El backend en bounty2 debe:
- Recibir peticiones del frontend
- Guardar en archivo local (backup)
- Guardar en RAG (rag3) para persistencia y búsqueda

### 4. Configurar el Frontend

El frontend debe:
- Usar `rag-api-client.js` para conectarse al servicio RAG
- Guardar mensajes en RAG además de localStorage
- Permitir búsqueda en historial usando RAG

## 📝 Endpoints del Servicio RAG

Según `backend/api_server.py`, el servicio RAG tiene:

### Búsqueda
- `POST /api/search/semantic` - Búsqueda semántica
- `POST /api/search/rag` - Búsqueda RAG completa
- `POST /api/search/all` - Búsqueda en todas las colecciones

### Usuarios
- `GET /api/users` - Listar usuarios
- `GET /api/users/{username}` - Obtener usuario
- `POST /api/users` - Crear usuario

### Mensajes
- `GET /api/messages` - Listar mensajes
- `POST /api/messages` - Crear mensaje
- `GET /api/sessions/{session_id}` - Mensajes de sesión

### Archivos
- `GET /api/files` - Listar archivos
- `POST /api/files` - Subir archivo

## 🔄 Flujo de Guardado

### Actual (solo localStorage):
```
Usuario envía mensaje → Frontend guarda en localStorage
```

### Nuevo (con RAG):
```
Usuario envía mensaje 
    → Frontend guarda en localStorage (caché local)
    → Frontend envía a Backend (bounty2:5001)
    → Backend guarda en archivo local (backup)
    → Backend envía a RAG (rag3) para persistencia y búsqueda
```

## ✅ Próximos Pasos

1. Obtener IP de rag3
2. Verificar servicio RAG en rag3
3. Configurar backend para guardar en RAG
4. Actualizar frontend para usar RAG API
5. Probar guardado y búsqueda

