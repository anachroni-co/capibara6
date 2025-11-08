# 🔑 Guía de API Keys para Capibara6

Esta guía te ayudará a obtener todas las API keys necesarias para configurar Capibara6 correctamente.

## 📋 Índice

1. [Configuración Básica (Requerida)](#-configuración-básica-requerida)
2. [Servicios de IA](#-servicios-de-ia)
3. [Google Cloud Platform](#-google-cloud-platform)
4. [Bases de Datos Vectoriales](#-bases-de-datos-vectoriales)
5. [Herramientas de Desarrollo](#-herramientas-de-desarrollo)
6. [Servicios de Deployment](#-servicios-de-deployment)
7. [Monitoreo y Analytics](#-monitoreo-y-analytics)
8. [Servicios Externos](#-servicios-externos)

---

## 🔧 Configuración Básica (Requerida)

### 📧 SMTP (Email)

**Para Gmail:**
1. Ve a [myaccount.google.com](https://myaccount.google.com)
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Seguridad → Contraseñas de aplicación
4. Genera una nueva contraseña de aplicación
5. Usa esa contraseña en `SMTP_PASSWORD`

**Para otros proveedores:**
- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Tu dominio**: Consulta con tu proveedor de hosting

---

## 🤖 Servicios de IA

### OpenAI API
1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una cuenta o inicia sesión
3. Ve a API Keys → Create new secret key
4. Copia la clave que empieza con `sk-`

### Anthropic Claude API
1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta
3. Ve a API Keys → Create Key
4. Copia la clave que empieza con `sk-ant-`

### Google AI / Gemini API
1. Ve a [aistudio.google.com](https://aistudio.google.com)
2. Crea un proyecto en Google Cloud
3. Habilita la API de Gemini
4. Ve a Credentials → Create Credentials → API Key
5. Copia la clave que empieza con `AIzaSy`

### Hugging Face API
1. Ve a [huggingface.co](https://huggingface.co)
2. Crea una cuenta
3. Ve a Settings → Access Tokens
4. Crea un nuevo token
5. Copia la clave que empieza con `hf_`

---

## ☁️ Google Cloud Platform

### Configuración Básica
1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs necesarias:
   - Compute Engine API
   - TPU API
   - Cloud Storage API

### Service Account
1. Ve a IAM & Admin → Service Accounts
2. Crea una nueva service account
3. Asigna roles: Editor, TPU Admin
4. Crea y descarga la clave JSON
5. Coloca la ruta en `GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY`

### Google TPU
1. Ve a Compute Engine → TPU
2. Crea una instancia TPU
3. Anota el nombre y zona
4. Configura en las variables de entorno

---

## 🗄️ Bases de Datos Vectoriales

### Pinecone
1. Ve a [pinecone.io](https://pinecone.io)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Ve a API Keys → Copy API Key
5. Anota también el environment (ej: `us-west1-gcp`)

### Weaviate
1. Ve a [weaviate.io](https://weaviate.io)
2. Crea una cuenta
3. Crea un nuevo cluster
4. Copia la URL y API key del cluster

### Chroma (Local)
- No requiere API key, se ejecuta localmente
- Solo configura `CHROMA_PERSIST_DIRECTORY`

---

## 🔧 Herramientas de Desarrollo

### E2B (Code Execution)
1. Ve a [e2b.dev](https://e2b.dev)
2. Crea una cuenta
3. Ve a Dashboard → API Keys
4. Crea una nueva API key
5. Copia la clave que empieza con `e2b_`

### GitHub API
1. Ve a [github.com/settings/tokens](https://github.com/settings/tokens)
2. Generate new token → Classic
3. Selecciona scopes: `repo`, `user`, `admin:org`
4. Copia el token que empieza con `ghp_`

---

## 🚀 Servicios de Deployment

### Railway
1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta con GitHub
3. Ve a Account → Tokens
4. Crea un nuevo token
5. Copia el token que empieza con `railway_`

### Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Crea una cuenta con GitHub
3. Ve a Settings → Tokens
4. Crea un nuevo token
5. Copia el token

### Render
1. Ve a [render.com](https://render.com)
2. Crea una cuenta
3. Ve a Account → API Keys
4. Crea una nueva API key
5. Copia la clave que empieza con `rnd_`

---

## 📊 Monitoreo y Analytics

### Sentry (Error Tracking)
1. Ve a [sentry.io](https://sentry.io)
2. Crea un proyecto
3. Ve a Settings → Client Keys (DSN)
4. Copia el DSN

### DataDog (Monitoring)
1. Ve a [datadoghq.com](https://datadoghq.com)
2. Crea una cuenta
3. Ve a Organization Settings → API Keys
4. Crea una nueva API key

### New Relic (APM)
1. Ve a [newrelic.com](https://newrelic.com)
2. Crea una cuenta
3. Ve a Account Settings → API Keys
4. Crea una nueva license key

---

## 🌐 Servicios Externos

### Stripe (Pagos)
1. Ve a [stripe.com](https://stripe.com)
2. Crea una cuenta
3. Ve a Developers → API Keys
4. Copia las claves de test y producción

### SendGrid (Email Marketing)
1. Ve a [sendgrid.com](https://sendgrid.com)
2. Crea una cuenta
3. Ve a Settings → API Keys
4. Crea una nueva API key

### Twilio (SMS/WhatsApp)
1. Ve a [twilio.com](https://twilio.com)
2. Crea una cuenta
3. Ve a Console → Account Info
4. Copia Account SID y Auth Token

---

## 🔐 Configuración de Seguridad

### JWT Secret
```bash
# Genera un JWT secret seguro
openssl rand -base64 32
```

### Encryption Key
```bash
# Genera una clave de encriptación de 32 caracteres
openssl rand -hex 32
```

---

## 📝 Pasos de Configuración

1. **Copia el archivo de ejemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo .env:**
   ```bash
   nano .env
   ```

3. **Reemplaza todas las claves:**
   - Cambia `tu_*` por tus valores reales
   - Cambia `xxxxxxxx` por tus claves reales

4. **Verifica la configuración:**
   ```bash
   # Para el backend
   cd backend
   python test_email.py
   ```

5. **Nunca subas .env al repositorio:**
   - El archivo ya está en `.gitignore`
   - Usa variables de entorno en producción

---

## 🚨 Consideraciones de Seguridad

- **Rota las claves regularmente** (cada 3-6 meses)
- **Usa diferentes claves** para desarrollo, staging y producción
- **Monitorea el uso** de las API keys
- **Usa permisos mínimos** necesarios
- **Considera usar un gestor de secretos** para producción (AWS Secrets Manager, Azure Key Vault, etc.)

---

## 🆘 Solución de Problemas

### Error de autenticación SMTP
- Verifica que uses "Contraseña de aplicación" en Gmail
- Revisa que el puerto sea 587 (no 465)
- Asegúrate de que la verificación en 2 pasos esté activada

### Error de API de Google Cloud
- Verifica que la service account tenga los permisos correctos
- Asegúrate de que las APIs estén habilitadas
- Revisa que el archivo JSON esté en la ruta correcta

### Error de CORS en el frontend
- Verifica que la URL del backend sea correcta en `web/config.js`
- Asegúrate de que el backend tenga CORS habilitado

---

## 📞 Soporte

Si tienes problemas con alguna configuración:

1. **Revisa los logs** del backend
2. **Verifica las variables de entorno** están configuradas
3. **Consulta la documentación** del servicio específico
4. **Contacta al equipo** en [info@anachroni.co](mailto:info@anachroni.co)

---

**¡Listo!** 🎉 Con esta configuración tendrás Capibara6 funcionando con todas las integraciones necesarias.