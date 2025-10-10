# 🔐 Sistema de Autenticación Capibara6

## ✅ Implementación Completada

Se ha implementado un sistema completo de autenticación OAuth con GitHub y Google para acceder al chat de Capibara6.

### 🎯 Características Implementadas

- ✅ **Página de Login** con diseño moderno y responsive
- ✅ **Autenticación OAuth** con GitHub y Google
- ✅ **Servidor de Autenticación** en Python/Flask
- ✅ **Protección de Rutas** - El chat requiere autenticación
- ✅ **Información del Usuario** en la interfaz
- ✅ **Botón de Logout** funcional
- ✅ **Modo Invitado** para desarrollo
- ✅ **JWT Tokens** para sesiones seguras

### 📁 Archivos Creados

#### Frontend
- `web/login.html` - Página de inicio de sesión
- `web/login.css` - Estilos para la página de login
- `web/login.js` - Lógica de autenticación frontend
- `web/auth/success.html` - Página de éxito de autenticación

#### Backend
- `backend/auth_server.py` - Servidor de autenticación OAuth
- `backend/oauth_config.md` - Documentación de configuración
- `backend/requirements.txt` - Dependencias actualizadas

#### Scripts
- `start_auth.sh` - Script de inicio para Linux/Mac
- `start_auth.bat` - Script de inicio para Windows

### 🚀 Cómo Usar

#### 1. Configurar OAuth (Obligatorio)

**GitHub:**
1. Ir a: https://github.com/settings/applications/new
2. Application name: `Capibara6`
3. Homepage URL: `http://localhost:8000`
4. Authorization callback URL: `http://localhost:5001/auth/callback/github`

**Google:**
1. Ir a: https://console.developers.google.com/
2. Crear proyecto y habilitar Google+ API
3. Crear credenciales OAuth 2.0
4. Authorized redirect URIs: `http://localhost:5001/auth/callback/google`

#### 2. Configurar Variables de Entorno

```bash
# Windows
set GITHUB_CLIENT_ID=tu_github_client_id
set GITHUB_CLIENT_SECRET=tu_github_client_secret
set GOOGLE_CLIENT_ID=tu_google_client_id
set GOOGLE_CLIENT_SECRET=tu_google_client_secret
set JWT_SECRET=tu_jwt_secret_generado
set SECRET_KEY=tu_flask_secret_generado

# Linux/Mac
export GITHUB_CLIENT_ID="tu_github_client_id"
export GITHUB_CLIENT_SECRET="tu_github_client_secret"
export GOOGLE_CLIENT_ID="tu_google_client_id"
export GOOGLE_CLIENT_SECRET="tu_google_client_secret"
export JWT_SECRET="tu_jwt_secret_generado"
export SECRET_KEY="tu_flask_secret_generado"
```

#### 3. Iniciar el Sistema

**Windows:**
```cmd
start_auth.bat
```

**Linux/Mac:**
```bash
./start_auth.sh
```

**Manual:**
```bash
# Terminal 1 - Servidor de Autenticación
python backend/auth_server.py

# Terminal 2 - Frontend
cd web && python -m http.server 8000
```

### 🌐 URLs de Acceso

- **Login:** http://localhost:8000/login.html
- **Chat:** http://localhost:8000/chat.html (requiere autenticación)
- **Auth API:** http://localhost:5001

### 🔄 Flujo de Autenticación

1. Usuario accede a `/login.html`
2. Selecciona GitHub o Google
3. Redirige al proveedor OAuth
4. Usuario autoriza la aplicación
5. Callback a `/auth/callback/{provider}`
6. Servidor genera JWT token
7. Redirige a `/auth/success.html` con token
8. Frontend guarda token y redirige a `/chat.html`

### 🛡️ Seguridad

- **JWT Tokens** con expiración de 7 días
- **State Parameter** para prevenir CSRF
- **HTTPS Ready** (configurar en producción)
- **CORS** configurado para localhost
- **Secrets** generados automáticamente

### 🎨 Interfaz de Usuario

#### Página de Login
- Diseño moderno con gradientes
- Botones de GitHub y Google
- Información de características
- Modales de términos y privacidad
- Modo invitado para desarrollo

#### Chat con Autenticación
- Información del usuario en sidebar
- Avatar del usuario
- Botón de logout
- Protección automática de rutas

### 🔧 Desarrollo

#### Modo Invitado
Para desarrollo sin OAuth, se incluye un botón "Continuar como Invitado" que aparece automáticamente en localhost.

#### Variables de Entorno
Si no se configuran las variables OAuth, el sistema mostrará advertencias pero seguirá funcionando en modo invitado.

### 📋 Próximos Pasos

- [ ] Configurar HTTPS para producción
- [ ] Implementar refresh tokens
- [ ] Agregar más proveedores OAuth
- [ ] Sistema de roles y permisos
- [ ] Auditoría de sesiones

### 🆘 Solución de Problemas

**Error: "Invalid state parameter"**
- Verificar que las URLs de callback coincidan exactamente

**Error: "Authentication failed"**
- Verificar que las credenciales OAuth sean correctas
- Comprobar que las APIs estén habilitadas

**Error: "CORS"**
- Verificar que el frontend esté en localhost:8000
- Comprobar configuración CORS en auth_server.py

---

¡El sistema de autenticación está listo para usar! 🎉
