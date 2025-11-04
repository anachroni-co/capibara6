# 🚀 Guía de Despliegue - capibara6

Esta guía te ayudará a desplegar el proyecto completo en producción.

## 📦 Arquitectura de Despliegue

```
Frontend (Vercel)           Backend (Railway)
     |                            |
     |-- HTML, CSS, JS            |-- Python Flask
     |-- Chatbot                  |-- Envío de emails
     |                            |-- Almacenamiento de datos
     |                            |
     +------- API Calls ----------+
```

---

## 🚂 Paso 1: Desplegar Backend en Railway

### 1.1 Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub (gratis)

### 1.2 Crear nuevo proyecto
1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Selecciona tu repositorio
4. Railway detectará Python automáticamente

### 1.3 Configurar variables de entorno
En Railway, ve a **Variables** y agrega:

```env
SMTP_SERVER=smtp.dondominio.com
SMTP_PORT=587
SMTP_USER=es2030@capibaragpt.com
SMTP_PASSWORD=Es2030$$
FROM_EMAIL=es2030@capibaragpt.com
```

### 1.4 Configurar directorio raíz
1. Ve a **Settings** → **General**
2. En **Root Directory** escribe: `backend`
3. Railway usará automáticamente el `Procfile`

### 1.5 Obtener la URL del backend
Una vez desplegado, Railway te dará una URL como:
```
https://capibara6-backend-production.up.railway.app
```

**⚠️ GUARDA ESTA URL - LA NECESITARÁS EN EL SIGUIENTE PASO**

---

## ☁️ Paso 2: Configurar Frontend para Producción

### 2.1 Actualizar la URL del backend

Edita el archivo `web/config.js` línea 7:

**ANTES:**
```javascript
: 'https://TU-PROYECTO.up.railway.app',
```

**DESPUÉS:**
```javascript
: 'https://capibara6-backend-production.up.railway.app',
```
(Reemplaza con tu URL real de Railway)

### 2.2 Verificar que funciona localmente
```bash
# Abre web/index.html en el navegador
# Prueba el chatbot con tu email
# Verifica en la consola que se conecta a Railway
```

---

## 🌐 Paso 3: Desplegar Frontend en Vercel

### 3.1 Preparar Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Regístrate con GitHub

### 3.2 Crear nuevo proyecto
1. Click en **"Add New"** → **"Project"**
2. Importa tu repositorio de GitHub
3. Configura:
   - **Framework Preset:** Other
   - **Root Directory:** `web`
   - **Build Command:** (déjalo vacío)
   - **Output Directory:** `./`

### 3.3 Variables de entorno (opcional)
No necesitas agregar variables de entorno porque la URL del backend ya está en `config.js`

### 3.4 Desplegar
1. Click en **"Deploy"**
2. Espera 1-2 minutos
3. Vercel te dará una URL como: `https://capibara6.vercel.app`

---

## ✅ Paso 4: Verificar que Todo Funciona

### 4.1 Verificar el backend
Abre en el navegador:
```
https://tu-backend.up.railway.app
```
Deberías ver: "capibara6 Backend - Servidor funcionando correctamente"

### 4.2 Verificar el frontend
Abre tu sitio de Vercel:
```
https://capibara6.vercel.app
```

### 4.3 Probar el chatbot
1. Abre el chatbot
2. Escribe tu email
3. Verifica:
   - ✅ Mensaje de confirmación aparece
   - ✅ Revisa tu email (deberías recibir confirmación)
   - ✅ En la consola del navegador (F12) no hay errores

### 4.4 Verificar logs de Railway
En Railway → Deployments → Logs, deberías ver:
```
POST /api/save-conversation HTTP/1.1" 200
```

---

## 🔧 Configuración Adicional

### Dominio personalizado en Vercel
1. Ve a tu proyecto en Vercel
2. Settings → Domains
3. Agrega tu dominio: `capibara6.tudominio.com`

### Variables de entorno en Railway
Si necesitas cambiar las credenciales de email:
1. Railway → Variables
2. Edita las variables
3. El servicio se reiniciará automáticamente

---

## 💰 Costos

### Railway (Backend)
- ✅ $5 USD gratis al mes
- ✅ Suficiente para ~500,000 requests
- ✅ Si superas, necesitarás agregar método de pago

### Vercel (Frontend)
- ✅ 100% gratis para proyectos personales
- ✅ 100 GB de bandwidth al mes
- ✅ Despliegues ilimitados

---

## 🐛 Troubleshooting

### El chatbot no envía emails
1. Verifica la consola del navegador (F12)
2. Revisa que la URL en `config.js` sea correcta
3. Verifica los logs de Railway

### Error de CORS
El backend ya tiene CORS habilitado. Si ves errores:
1. Verifica que la URL del backend sea correcta
2. Asegúrate de usar `https://` no `http://`

### Backend se duerme
Railway puede "dormir" servicios inactivos en el plan gratuito:
- Se reactiva automáticamente al recibir una request
- Primera carga puede tardar ~10 segundos

### Emails no llegan
1. Revisa la carpeta de SPAM
2. Verifica las credenciales SMTP en Railway
3. Revisa los logs de Railway para ver errores

---

## 📝 Checklist de Despliegue

- [ ] Backend desplegado en Railway
- [ ] Variables de entorno configuradas en Railway
- [ ] URL de Railway obtenida
- [ ] `web/config.js` actualizado con URL de Railway
- [ ] Frontend desplegado en Vercel
- [ ] Chatbot probado y funcionando
- [ ] Email de prueba recibido
- [ ] Sin errores en consola del navegador

---

## 🎉 ¡Listo!

Tu chatbot capibara6 ahora está en producción:
- ✅ Frontend rápido en Vercel
- ✅ Backend confiable en Railway
- ✅ Emails funcionando
- ✅ Datos guardados

**URL de tu sitio:** https://capibara6.vercel.app

**Mantenimiento:**
- Los datos en Railway son efímeros (se borran al reiniciar)
- Considera agregar una base de datos para producción real
- Monitorea el uso de créditos en Railway

---

¿Problemas? Revisa los logs:
- **Railway:** Dashboard → Deployments → Logs
- **Vercel:** Dashboard → Deployments → Function Logs
- **Navegador:** F12 → Console

