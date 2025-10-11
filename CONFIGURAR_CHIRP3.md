# 🔊 Configurar Google Chirp 3 TTS

Este documento explica cómo configurar la API de **Google Cloud Text-to-Speech** con **Chirp 3** para síntesis de voz natural.

---

## 📋 Prerequisitos

1. ✅ Cuenta de Google Cloud Platform (GCP)
2. ✅ Proyecto de GCP creado
3. ✅ Tarjeta de crédito (tiene free tier de $300)

---

## 🔧 Paso 1: Habilitar la API

### **1.1 Ir a la consola de Google Cloud:**
```
https://console.cloud.google.com/
```

### **1.2 Habilitar Text-to-Speech API:**
```
https://console.cloud.google.com/apis/library/texttospeech.googleapis.com
```

Clic en **"Habilitar"**

---

## 🔑 Paso 2: Crear Cuenta de Servicio

### **2.1 Ir a Credenciales:**
```
https://console.cloud.google.com/apis/credentials
```

### **2.2 Crear cuenta de servicio:**
- Clic en **"Crear credenciales"**
- Seleccionar **"Cuenta de servicio"**
- Nombre: `capibara6-tts`
- Rol: **"Cloud Text-to-Speech User"**
- Clic en **"Crear"**

### **2.3 Crear clave JSON:**
- En la lista de cuentas de servicio, clic en `capibara6-tts`
- Pestaña **"Claves"**
- **"Agregar clave"** → **"Crear clave nueva"**
- Tipo: **JSON**
- Clic en **"Crear"**

Se descargará un archivo JSON como:
```
capibara6-tts-abc123.json
```

**⚠️ IMPORTANTE: Guarda este archivo de forma segura, no lo compartas públicamente.**

---

## ⚙️ Paso 3: Configurar en Vercel

### **3.1 Ir al dashboard de Vercel:**
```
https://vercel.com/dashboard
```

### **3.2 Seleccionar tu proyecto** (capibara6)

### **3.3 Ir a Settings → Environment Variables**

### **3.4 Agregar credenciales de Google Cloud:**

#### **Opción A: Usar el archivo JSON completo (Recomendado)**

1. Abre el archivo JSON descargado con un editor de texto
2. Copia **TODO** el contenido JSON
3. En Vercel, agregar variable:
   - **Key:** `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value:** Pega todo el JSON (será algo como `{"type":"service_account","project_id":...}`)
   - **Environments:** Marcar todas (Production, Preview, Development)

#### **Opción B: Usar variables individuales**

Extraer del JSON y agregar cada una:
- `GOOGLE_CLOUD_PROJECT` = `project_id` del JSON
- `GOOGLE_CLOUD_PRIVATE_KEY` = `private_key` del JSON
- `GOOGLE_CLOUD_CLIENT_EMAIL` = `client_email` del JSON

### **3.5 Guardar** y hacer **Redeploy**

### **3.6 Verificar en los logs**

En el deploy verás:
```
✓ Building...
✓ Installing dependencies
✓ google-cloud-texttospeech installed
```

---

## 🧪 Paso 4: Probar

### **Desde tu navegador:**
```
https://www.capibara6.com/chat.html
```

1. Haz una pregunta al modelo
2. Espera la respuesta
3. Clic en el botón **"Escuchar" 🔊**
4. Debería reproducir con voz **Chirp 3 HD**

---

## 📊 Costos

### **Free Tier:**
- ✅ **Primeros $300**: Gratis durante 90 días
- ✅ **Después:** 4 millones de caracteres gratis al mes

### **Precios después del free tier:**
- Standard voices: $4 USD / 1 millón de caracteres
- WaveNet voices: $16 USD / 1 millón de caracteres
- **Chirp 3 HD**: ~$16 USD / 1 millón de caracteres

**Ejemplo:**
- 1,000 respuestas de 200 palabras ≈ 200,000 caracteres
- Costo: ~$3.20 USD/mes

---

## 🎯 Voces Disponibles en Español

| Voz | Idioma | Género | Calidad |
|-----|--------|--------|---------|
| `es-ES-Chirp-3-HD` | Español España | Femenino | ⭐⭐⭐⭐⭐ |
| `es-ES-Neural2-A` | Español España | Femenino | ⭐⭐⭐⭐ |
| `es-MX-Neural2-C` | Español México | Masculino | ⭐⭐⭐⭐ |

---

## 🔀 Fallback Automático

Si Chirp 3 no está disponible:
- ✅ El sistema usa **Web Speech API** del navegador (gratis)
- ✅ Calidad reducida pero funcional
- ✅ Sin costos adicionales

---

## 🛡️ Seguridad

### **Protección de la API Key:**
- ✅ La API key está en **variables de entorno** de Vercel
- ✅ **NUNCA** en el código frontend
- ✅ El proxy `/api/tts` maneja la autenticación
- ✅ CORS configurado solo para tu dominio

### **Restricciones recomendadas:**
- Referente HTTP solo desde `capibara6.com`
- Solo acceso a Text-to-Speech API
- Cuota máxima diaria configurada

---

## 🧪 Testing

### **Probar API directamente:**
```bash
curl -X POST https://www.capibara6.com/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola, soy Capibara6 con voz Chirp 3"}'
```

Deberías recibir:
```json
{
  "audioContent": "base64encodedaudio...",
  "provider": "Google Chirp 3 HD"
}
```

---

## 📝 Variables de Entorno Requeridas

En Vercel Settings → Environment Variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | `{"type":"service_account",...}` | Contenido completo del archivo JSON de credenciales |

**Formato del JSON:**
```json
{
  "type": "service_account",
  "project_id": "tu-proyecto",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "capibara6-tts@...iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

---

## 🚨 Troubleshooting

### **Error: API key no configurada**
- Verificar que la variable esté en Vercel
- Hacer redeploy después de agregar la variable

### **Error: Cuota excedida**
- Verificar uso en Google Cloud Console
- Aumentar cuota o esperar al siguiente mes

### **Error: Voz no disponible**
- Verificar que Chirp 3 esté habilitado en tu región
- Usar voz alternativa (Neural2)

---

## ✅ Resumen

1. Habilitar Text-to-Speech API en Google Cloud
2. Crear API key
3. Restringir API key a tu dominio
4. Agregar `GOOGLE_CLOUD_API_KEY` en Vercel
5. Redeploy
6. Probar botón "Escuchar" en el chat

**¡Chirp 3 HD te dará la mejor calidad de voz en español!** 🎯

