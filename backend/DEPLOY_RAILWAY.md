# 🚂 Desplegar Backend en Railway

## 📋 Pasos para desplegar

### 1. Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub (es gratis)
3. Conecta tu cuenta de GitHub

### 2. Crear nuevo proyecto
1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Selecciona tu repositorio `capibara6`
4. Railway detectará automáticamente que es Python

### 3. Configurar el proyecto
1. Railway te preguntará qué desplegar
2. Click en **"Add variables"** o **"Variables"**
3. Agrega estas variables de entorno:

```
SMTP_SERVER=smtp.dondominio.com
SMTP_PORT=587
SMTP_USER=es2030@capibaragpt.com
SMTP_PASSWORD=Es2030$$
FROM_EMAIL=es2030@capibaragpt.com
```

### 4. Configurar el directorio raíz
1. En **Settings** → **Build**
2. En **Root Directory** escribe: `backend`
3. Railway automáticamente ejecutará `python server.py`

### 5. Desplegar
1. Railway desplegará automáticamente
2. Espera 2-3 minutos
3. Verás un dominio como: `https://tu-proyecto.up.railway.app`

### 6. Verificar que funciona
Abre en el navegador:
```
https://tu-proyecto.up.railway.app
```

Deberías ver: "capibara6 Backend - Servidor funcionando correctamente"

## 🔗 Conectar con el Frontend

Una vez desplegado, copia la URL de Railway (ej: `https://capibara6-backend.up.railway.app`)

Actualiza `web/chatbot.js` línea ~405:

```javascript
const backendUrl = 'https://capibara6-backend.up.railway.app/api/save-conversation';
```

## 💰 Costos

Railway tiene plan gratuito:
- ✅ $5 USD de crédito gratis al mes
- ✅ Suficiente para el chatbot
- ✅ No necesitas tarjeta de crédito inicialmente

## ⚠️ Importante

- Los datos se guardarán en Railway (efímeros)
- Para producción, considera agregar una base de datos
- Railway reiniciará el servidor si no detecta actividad

## 🐛 Troubleshooting

**Error: "Application failed to respond"**
- Verifica que las variables de entorno estén configuradas
- Revisa los logs en Railway

**Error: "Module not found"**
- Railway debe instalar automáticamente desde `requirements.txt`

**Emails no se envían:**
- Verifica las credenciales SMTP en las variables de entorno
- Revisa los logs de Railway

## 📝 Notas

- Railway usa el archivo `Procfile` para saber cómo iniciar la app
- El puerto se asigna automáticamente (variable `PORT`)
- Los logs están disponibles en tiempo real en el dashboard

