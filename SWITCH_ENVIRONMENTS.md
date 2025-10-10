# 🔄 Cambiar entre Desarrollo y Producción

## 📋 Instrucciones Rápidas

### Para Activar Desarrollo (localhost):
1. **backend/auth_server.py** - Línea 20-23:
   ```python
   # Configuración CORS - Desarrollo (localhost)
   CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])
   
   # Configuración CORS - Producción (comentado para activar más tarde)
   # CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000', 'https://capibara6.com', 'http://capibara6.com'])
   ```

2. **backend/auth_server.py** - Líneas de redirect:
   ```python
   # Desarrollo (localhost)
   frontend_url = f"http://localhost:8000/auth/success?token={jwt_token}"
   
   # Producción (comentado para activar más tarde)
   # frontend_url = f"https://capibara6.com/auth/success?token={jwt_token}"
   ```

3. **web/login.js** - Líneas 6-10:
   ```javascript
   // Desarrollo (localhost)
   const AUTH_SERVER_URL = 'http://localhost:5001';
   
   // Producción (comentado para activar más tarde)
   // const AUTH_SERVER_URL = 'https://api.capibara6.com';
   ```

### Para Activar Producción (capibara6.com):
1. **Comentar** las líneas de desarrollo
2. **Descomentar** las líneas de producción
3. **Actualizar** las apps OAuth con las URLs de producción

## 🚀 Comandos de Inicio

### Desarrollo:
```bash
# Windows
start_auth.bat

# Linux/Mac
./start_auth.sh
```

### Producción:
```bash
# Configurar variables de entorno de producción
# Desplegar en servidores correspondientes
```

## 📝 URLs por Entorno

| Entorno | Frontend | Auth Server | GitHub Callback | Google Callback |
|---------|----------|-------------|-----------------|-----------------|
| **Desarrollo** | http://localhost:8000 | http://localhost:5001 | http://localhost:5001/auth/callback/github | http://localhost:5001/auth/callback/google |
| **Producción** | https://capibara6.com | https://api.capibara6.com | https://api.capibara6.com/auth/callback/github | https://api.capibara6.com/auth/callback/google |

## ⚠️ Recordatorios

- **Desarrollo**: Usar localhost para testing
- **Producción**: Configurar HTTPS/SSL
- **OAuth Apps**: Actualizar URLs según el entorno
- **Variables de Entorno**: Configurar según el entorno
