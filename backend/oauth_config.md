# Configuración OAuth para Capibara6

## Variables de Entorno Requeridas

Crea un archivo `.env` en la carpeta `backend/` con las siguientes variables:

```bash
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# JWT Secret (generar uno seguro)
JWT_SECRET=your_jwt_secret_here

# Flask Secret Key
SECRET_KEY=your_flask_secret_key_here
```

## Configuración GitHub OAuth

1. **Ir a GitHub Settings:**
   - URL: https://github.com/settings/applications/new

2. **Configurar la aplicación:**
   - **Application name:** Capibara6
   - **Homepage URL:** http://localhost:8000 (desarrollo) / https://capibara6.com (producción)
   - **Authorization callback URL:** http://localhost:5001/auth/callback/github (desarrollo) / https://api.capibara6.com/auth/callback/github (producción)

3. **Copiar credenciales:**
   - Client ID
   - Client Secret

## Configuración Google OAuth

1. **Ir a Google Console:**
   - URL: https://console.developers.google.com/

2. **Crear/Seleccionar proyecto**

3. **Habilitar APIs:**
   - Google+ API
   - OAuth2 API

4. **Crear credenciales OAuth 2.0:**
   - **Authorized redirect URIs:** http://localhost:5001/auth/callback/google (desarrollo) / https://api.capibara6.com/auth/callback/google (producción)

5. **Copiar credenciales:**
   - Client ID
   - Client Secret

## Generar Secrets Seguros

```bash
# JWT Secret
openssl rand -hex 32

# Flask Secret
openssl rand -hex 32
```

## Comandos de Inicio

```bash
# 1. Instalar dependencias
pip install -r backend/requirements.txt

# 2. Configurar variables de entorno
export GITHUB_CLIENT_ID="tu_client_id"
export GITHUB_CLIENT_SECRET="tu_client_secret"
export GOOGLE_CLIENT_ID="tu_client_id"
export GOOGLE_CLIENT_SECRET="tu_client_secret"
export JWT_SECRET="tu_jwt_secret"
export SECRET_KEY="tu_flask_secret"

# 3. Iniciar servidor de autenticación
python backend/auth_server.py

# 4. En otra terminal, servir el frontend
cd web && python -m http.server 8000
```

## URLs de Acceso

### Desarrollo (localhost)
- **Frontend:** http://localhost:8000
- **Login:** http://localhost:8000/login.html
- **Chat:** http://localhost:8000/chat.html
- **Auth Server:** http://localhost:5001

### Producción (comentado para activar más tarde)
- **Frontend:** https://capibara6.com
- **Login:** https://capibara6.com/login.html
- **Chat:** https://capibara6.com/chat.html
- **Auth Server:** https://api.capibara6.com

## Flujo de Autenticación

1. Usuario accede a `/login.html`
2. Selecciona GitHub o Google
3. Redirige a proveedor OAuth
4. Usuario autoriza la aplicación
5. Callback a `/auth/callback/{provider}`
6. Servidor genera JWT
7. Redirige a `/auth/success.html` con token
8. Frontend guarda token y redirige a `/chat.html`
