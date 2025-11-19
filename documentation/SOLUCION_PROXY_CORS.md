# 🔧 Solución: Proxy CORS Local

## ✅ Estado Actual

El proxy CORS está corriendo en el puerto **8001** y está configurado para hacer proxy al backend en bounty2 (`http://34.12.166.76:5001`).

## 🔍 Cambios Realizados

### 1. Proxy CORS Actualizado (`backend/cors_proxy_simple.py`)

- ✅ Soporta tanto `/health` como `/api/health`
- ✅ Maneja correctamente el endpoint `/health` del servidor integrado
- ✅ Proxy general para todas las rutas `/api/*`

### 2. Configuración del Frontend

El frontend está configurado para usar el proxy cuando está en `localhost`:
- **Desarrollo local**: `http://localhost:8001` (proxy CORS)
- **Producción**: `http://34.12.166.76:5001` (directo)

## 🧪 Pruebas

### Probar el Proxy

```bash
# Health check del proxy
curl http://localhost:8001/

# Health check del backend a través del proxy
curl http://localhost:8001/health
curl http://localhost:8001/api/health

# Chat a través del proxy
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'
```

### Desde el Frontend

1. Asegúrate de que el proxy esté corriendo:
```bash
cd backend
python3 cors_proxy_simple.py
```

2. Abre el frontend en el navegador:
```bash
cd web
python3 -m http.server 8000
```

3. Abre `http://localhost:8000/chat.html` en tu navegador

4. Verifica en la consola del navegador (F12) que las peticiones vayan a `http://localhost:8001`

## 🔧 Endpoints del Proxy

El proxy expone los siguientes endpoints:

- `GET /` - Health check del proxy
- `GET /health` - Proxy a `/health` del backend
- `GET /api/health` - Proxy a `/api/health` del backend (fallback)
- `POST /api/chat` - Proxy a `/api/chat` del backend
- `GET|POST|PUT|DELETE /<path>` - Proxy general para otras rutas

## 🐛 Troubleshooting

### El proxy no responde

**Verificar que esté corriendo**:
```bash
ps aux | grep cors_proxy_simple
lsof -i :8001
```

**Reiniciar el proxy**:
```bash
cd backend
python3 cors_proxy_simple.py
```

### Error de conexión con el backend

**Verificar que el backend esté accesible**:
```bash
curl http://34.12.166.76:5001/health
```

**Verificar la URL en el proxy**:
Edita `backend/cors_proxy_simple.py` y verifica que `BACKEND_URL` sea correcto:
```python
BACKEND_URL = 'http://34.12.166.76:5001'
```

### CORS sigue apareciendo en el navegador

**Verificar que el frontend use el proxy**:
- En `localhost`: debe usar `http://localhost:8001`
- Verifica en la consola del navegador las URLs de las peticiones

**Verificar CORS en el proxy**:
El proxy tiene `CORS(app)` configurado, debería permitir todas las peticiones.

## 📋 Checklist

- [ ] Proxy corriendo en puerto 8001
- [ ] Backend accesible en `http://34.12.166.76:5001`
- [ ] Proxy responde a `/health`
- [ ] Frontend configurado para usar `http://localhost:8001` en desarrollo
- [ ] Frontend puede conectarse y enviar mensajes

## 🚀 Uso en Desarrollo

### Iniciar el Proxy

```bash
cd backend
source venv/bin/activate  # Si usas venv
python3 cors_proxy_simple.py
```

### Iniciar el Frontend

En otra terminal:
```bash
cd web
python3 -m http.server 8000
```

### Probar

1. Abre `http://localhost:8000/chat.html`
2. Verifica en la consola que las peticiones vayan a `localhost:8001`
3. Intenta enviar un mensaje

## 📝 Notas

- El proxy es solo para desarrollo local
- En producción (Vercel), el frontend se conecta directamente al backend
- El proxy maneja automáticamente los problemas de CORS
- Todos los endpoints del backend están disponibles a través del proxy

