# 🚀 Inicio Rápido - Backend capibara6

## ⚡ Instalación en 3 pasos

### 1️⃣ Configurar credenciales SMTP

```bash
cd backend
cp env.example .env
```

Edita `.env` con tus credenciales:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=info@anachroni.co
SMTP_PASSWORD=tu_contraseña_de_aplicacion
FROM_EMAIL=info@anachroni.co
```

**📧 Para Gmail:**
1. Ve a: https://myaccount.google.com/apppasswords
2. Genera una "Contraseña de aplicación"
3. Úsala en `SMTP_PASSWORD`

### 2️⃣ Iniciar servidor

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Manual:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### 3️⃣ Probar

El servidor estará en: **http://localhost:5000**

Prueba el endpoint:
```bash
curl http://localhost:5000/api/health
```

## 📧 ¿Cómo funciona?

### Cuando un usuario escribe su email en el chatbot:

1. **Frontend** → Detecta el email y envía al backend
2. **Backend** → Recibe los datos y:
   - ✅ Guarda en `user_data/conversations.json`
   - ✅ Crea archivo `.txt` individual
   - ✅ Envía email de confirmación al usuario
   - ✅ Envía notificación a `info@anachroni.co`

### Ejemplo de flujo:

```
Usuario escribe: "Hola, mi email es juan@example.com"
          ↓
Frontend detecta email automáticamente
          ↓
POST /api/save-conversation
{
  "email": "juan@example.com",
  "conversations": [...]
}
          ↓
Backend procesa y envía 2 emails:
  1. A juan@example.com → Email bonito de confirmación
  2. A info@anachroni.co → Notificación con datos del usuario
```

## 📁 Archivos generados

```
backend/
└── user_data/
    ├── conversations.json          # Todas las conversaciones
    ├── user_20251002_103045.txt   # Usuario individual
    └── user_20251002_110230.txt   # Otro usuario
```

## 🔧 Configuración avanzada

### Usar otro proveedor SMTP

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Servidor propio:**
```env
SMTP_SERVER=mail.tudominio.com
SMTP_PORT=587
```

## 🐛 Solución de problemas

### Error de autenticación
```
smtplib.SMTPAuthenticationError
```
**Solución:** Verifica que uses "Contraseña de aplicación" en Gmail

### Error de conexión
```
Connection refused
```
**Solución:** 
- Verifica que el servidor SMTP esté correcto
- Algunos ISPs bloquean el puerto 587

### CORS error en frontend
```
Access-Control-Allow-Origin
```
**Solución:** Ya está configurado CORS en el servidor

## 🌐 Desplegar en producción

### Opción 1: Servidor propio
```bash
# Usar gunicorn para producción
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Opción 2: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### Opción 3: Vercel/Railway/Render
El backend es compatible con estos servicios. Solo configura las variables de entorno.

## 📊 Monitoreo

Ver logs en tiempo real:
```bash
tail -f user_data/conversations.json
```

## ✅ Checklist

- [ ] Archivo `.env` configurado
- [ ] Contraseña de aplicación generada (Gmail)
- [ ] Servidor iniciado correctamente
- [ ] Endpoint `/api/health` responde
- [ ] Email de prueba enviado correctamente
- [ ] Frontend conectado al backend

## 🆘 Ayuda

¿Problemas? Verifica:
1. ✅ `.env` tiene las credenciales correctas
2. ✅ Puerto 5000 está libre
3. ✅ Frontend apunta a la URL correcta
4. ✅ Firewall permite conexión SMTP

---

**¡Listo!** 🎉 El backend está funcionando y enviando emails automáticamente.

