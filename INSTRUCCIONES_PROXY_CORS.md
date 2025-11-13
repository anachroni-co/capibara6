# 🚀 Instrucciones: Proxy CORS para Desarrollo Local

## 📍 ¿Dónde se ejecuta el proxy CORS?

**El proxy CORS se ejecuta en tu PORTÁTIL LOCAL** (no en ningún servidor remoto).

### Propósito del Proxy CORS

Cuando desarrollas localmente:
- **Frontend**: Corre en `http://localhost:8000` (tu portátil)
- **Backend**: Corre en `http://34.12.166.76:5001` (VM bounty2 en Google Cloud)

**Problema**: El navegador bloquea peticiones directas desde `localhost` a una IP externa por CORS.

**Solución**: El proxy CORS actúa como intermediario:
- El frontend se conecta al proxy local (`localhost:8001`)
- El proxy se conecta al backend remoto (`34.12.166.76:5001`)
- El navegador no ve problemas de CORS porque todo es `localhost`

## 🔧 Configuración Actual

### Frontend (`web/config.js`)
```javascript
BACKEND_URL: window.location.hostname === 'localhost'
    ? 'http://localhost:8001'  // ← Proxy CORS local
    : 'https://www.capibara6.com'
```

### Proxy CORS (`backend/cors_proxy_simple.py`)
```python
BACKEND_URL = 'http://34.12.166.76:5001'  # Backend remoto en bounty2
# Se ejecuta en: localhost:8001
```

## 🚀 Cómo Usar

### Paso 1: Iniciar el Proxy CORS en tu Portátil

```bash
cd backend
python3 cors_proxy_simple.py
```

Deberías ver:
```
🚀 Iniciando Proxy CORS local simplificado para Capibara6...
🎯 Backend remoto: http://34.12.166.76:5001
🌐 Puerto local: 8001
🔗 Endpoints: /api/chat, /api/health, y otros /api/*
 * Running on http://127.0.0.1:8001
```

**IMPORTANTE**: Deja este proceso corriendo mientras desarrollas.

### Paso 2: Iniciar el Frontend (en otra terminal)

```bash
cd web
python3 -m http.server 8000
```

### Paso 3: Abrir en el Navegador

```
http://localhost:8000/chat.html
```

El frontend ahora se conectará a `http://localhost:8001` (el proxy) que a su vez se conecta al backend remoto.

## 🔍 Verificación

### Verificar que el proxy esté corriendo

```bash
# Debe responder con información del proxy
curl http://localhost:8001/

# Debe hacer proxy al health check del backend
curl http://localhost:8001/health
```

### Verificar en el navegador

1. Abre `http://localhost:8000/chat.html`
2. Abre la consola del navegador (F12)
3. Verifica que las peticiones vayan a `http://localhost:8001` (no a `34.12.166.76:5001`)

## 🐛 Troubleshooting

### Error: "Connection refused" en localhost:8001

**Causa**: El proxy CORS no está corriendo.

**Solución**: Inicia el proxy:
```bash
cd backend
python3 cors_proxy_simple.py
```

### Error: CORS en el navegador

**Causa**: El frontend está intentando conectarse directamente al backend remoto.

**Solución**: Verifica que `web/config.js` use `http://localhost:8001` cuando esté en `localhost`.

### El proxy no conecta con el backend

**Verificar**:
```bash
# El backend debe ser accesible
curl http://34.12.166.76:5001/health

# El proxy debe poder conectarse
curl http://localhost:8001/health
```

## 📋 Flujo Completo

```
1. Frontend (localhost:8000)
   ↓ Petición HTTP
2. Proxy CORS (localhost:8001) ← CORRE EN TU PORTÁTIL
   ↓ Petición HTTP (sin CORS)
3. Backend (34.12.166.76:5001) ← CORRE EN BOUNTY2 (Google Cloud)
   ↓ Procesa
4. Respuesta vuelve por el mismo camino
```

## ✅ Checklist

- [ ] Proxy CORS corriendo en `localhost:8001` (en tu portátil)
- [ ] Frontend configurado para usar `localhost:8001` en desarrollo
- [ ] Backend accesible en `34.12.166.76:5001`
- [ ] Frontend abierto en `localhost:8000`
- [ ] Consola del navegador muestra peticiones a `localhost:8001`

## 🎯 Resumen

- **Proxy CORS**: Se ejecuta en tu PORTÁTIL LOCAL (puerto 8001)
- **Frontend**: Se ejecuta en tu PORTÁTIL LOCAL (puerto 8000)
- **Backend**: Se ejecuta en BOUNTY2 (Google Cloud, puerto 5001)
- **Flujo**: Frontend → Proxy Local → Backend Remoto

