# 🔧 Guía de Configuración de Capibara6

Esta guía te ayudará a configurar Capibara6 con todas las API keys necesarias para los servicios de terceros.

## 🚀 Configuración Rápida

### 1. Copiar archivo de configuración
```bash
cp .env.example .env
```

### 2. Editar configuración
```bash
nano .env
```

### 3. Verificar configuración
```bash
python check_env.py
```

## 📋 Servicios Incluidos

### 🔧 Configuración Básica (Requerida)
- **SMTP**: Para envío de emails del chatbot
- **Email**: Configuración de correo electrónico

### 🤖 Servicios de IA
- **OpenAI**: GPT-4, GPT-3.5, Embeddings
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Haiku
- **Google AI**: Gemini Pro, Gemini Ultra
- **Hugging Face**: Modelos open source, Transformers

### ☁️ Google Cloud Platform
- **Google Cloud**: Para TPU v5e/v6e-64 y ARM Axion
- **TPU Configuration**: Configuración específica para TPUs
- **Service Account**: Autenticación con Google Cloud

### 🗄️ Bases de Datos Vectoriales
- **Pinecone**: Base de datos vectorial para embeddings
- **Weaviate**: Base de datos vectorial open source
- **Chroma**: Base de datos vectorial local

### 🔧 Herramientas de Desarrollo
- **E2B**: Entorno de ejecución de código
- **GitHub**: API de GitHub para integraciones

### 🚀 Servicios de Deployment
- **Railway**: Para deployment del backend
- **Vercel**: Para deployment del frontend
- **Render**: Alternativa de deployment

### 📊 Monitoreo y Analytics
- **Sentry**: Tracking de errores
- **DataDog**: Monitoreo de aplicaciones
- **New Relic**: APM (Application Performance Monitoring)

### 🌐 Servicios Externos
- **Stripe**: Procesamiento de pagos
- **SendGrid**: Email marketing
- **Twilio**: SMS y WhatsApp

## 🔑 Cómo Obtener las API Keys

### 📧 SMTP (Gmail)
1. Ve a [myaccount.google.com](https://myaccount.google.com)
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Seguridad → Contraseñas de aplicación
4. Genera una nueva contraseña de aplicación
5. Usa esa contraseña en `SMTP_PASSWORD`

### 🤖 OpenAI
1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una cuenta o inicia sesión
3. Ve a API Keys → Create new secret key
4. Copia la clave que empieza con `sk-`

### 🧠 Anthropic Claude
1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta
3. Ve a API Keys → Create Key
4. Copia la clave que empieza con `sk-ant-`

### 🔍 Google AI
1. Ve a [aistudio.google.com](https://aistudio.google.com)
2. Crea un proyecto en Google Cloud
3. Habilita la API de Gemini
4. Ve a Credentials → Create Credentials → API Key
5. Copia la clave que empieza con `AIzaSy`

### 🤗 Hugging Face
1. Ve a [huggingface.co](https://huggingface.co)
2. Crea una cuenta
3. Ve a Settings → Access Tokens
4. Crea un nuevo token
5. Copia la clave que empieza con `hf_`

### 🌲 Pinecone
1. Ve a [pinecone.io](https://pinecone.io)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Ve a API Keys → Copy API Key
5. Anota también el environment

### ☁️ Google Cloud Platform
1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Crea un nuevo proyecto
3. Habilita las APIs necesarias
4. Crea una Service Account
5. Descarga la clave JSON

## 🧪 Verificación de Configuración

### Script de Verificación
```bash
python check_env.py
```

Este script verifica:
- ✅ Variables de entorno configuradas
- 🔍 Conectividad con APIs
- 📧 Configuración SMTP
- 🤖 Servicios de IA
- ☁️ Servicios de cloud

### Verificación Manual
```bash
# Verificar variables de entorno
echo $SMTP_SERVER
echo $OPENAI_API_KEY

# Probar backend
cd backend
python test_email.py
```

## 🔐 Seguridad

### Mejores Prácticas
- 🔒 Nunca subas el archivo `.env` al repositorio
- 🔄 Rota las claves regularmente (cada 3-6 meses)
- 👥 Usa diferentes claves para desarrollo, staging y producción
- 📊 Monitorea el uso de las API keys
- 🛡️ Usa permisos mínimos necesarios

### Permisos del Archivo
```bash
chmod 600 .env
```

## 🚨 Solución de Problemas

### Error de SMTP
```
❌ Error SMTP: (535, '5.7.8 Username and Password not accepted')
```
**Solución**: Usa "Contraseña de aplicación" en Gmail, no tu contraseña normal.

### Error de API
```
❌ Error OpenAI API: 401
```
**Solución**: Verifica que la API key sea correcta y tenga créditos.

### Error de CORS
```
❌ CORS error en frontend
```
**Solución**: Verifica que la URL del backend sea correcta en `web/config.js`.

## 📚 Documentación Adicional

- [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md) - Guía detallada de cada API
- [README.md](README.md) - Documentación principal del proyecto
- [backend/README.md](backend/README.md) - Documentación del backend

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los logs** del backend
2. **Verifica las variables de entorno**
3. **Consulta la documentación** del servicio específico
4. **Contacta al equipo**: [info@anachroni.co](mailto:info@anachroni.co)

---

**¡Listo!** 🎉 Con esta configuración tendrás Capibara6 funcionando con todas las integraciones necesarias.