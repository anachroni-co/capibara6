# 🌐 Compartir el Chat Públicamente

## 🚀 Opción 1: Ngrok (Rápido - Para Demostración)

### Ventajas:
- ✅ Configuración en 2 minutos
- ✅ No requiere cambios en el código
- ✅ Funciona desde localhost

### Desventajas:
- ❌ URL cambia cada vez que reinicias
- ❌ Sesión gratuita limitada a 8 horas

### Pasos:

1. **Descargar Ngrok:**
   - https://ngrok.com/download
   - Crear cuenta gratis

2. **Instalar y configurar:**
   ```cmd
   # Autenticarse
   ngrok config add-authtoken TU_TOKEN_AQUI
   
   # Crear túnel
   ngrok http 5500
   ```

3. **Compartir la URL:**
   ```
   Ngrok te dará algo como:
   https://abc123-xyz.ngrok.io
   
   Comparte esa URL con quien quieras
   ```

---

## 🎯 Opción 2: Vercel (Recomendado - Gratis Permanente)

### Ventajas:
- ✅ URL permanente y personalizable
- ✅ HTTPS automático
- ✅ Deploy en segundos
- ✅ 100% gratis para proyectos open source

### Pasos:

1. **Instalar Vercel CLI:**
   ```cmd
   npm install -g vercel
   ```

2. **Desplegar:**
   ```cmd
   cd web
   vercel
   ```

3. **Configuración:**
   - Proyecto: capibara6
   - Framework: None (estático)
   - Output directory: ./

4. **URL Final:**
   ```
   https://capibara6.vercel.app
   o
   https://capibara6-tu-usuario.vercel.app
   ```

5. **Actualizar en cada cambio:**
   ```cmd
   vercel --prod
   ```

---

## 📦 Opción 3: Netlify (Alternativa a Vercel)

### Pasos:

1. **Instalar Netlify CLI:**
   ```cmd
   npm install -g netlify-cli
   ```

2. **Desplegar:**
   ```cmd
   cd web
   netlify deploy --prod
   ```

3. **URL Final:**
   ```
   https://capibara6.netlify.app
   ```

---

## 🐙 Opción 4: GitHub Pages

### Pasos:

1. **Crear repositorio en GitHub**

2. **Subir código:**
   ```cmd
   git init
   git add web/*
   git commit -m "Deploy Capibara6"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/capibara6.git
   git push -u origin main
   ```

3. **Habilitar GitHub Pages:**
   - Ir a Settings → Pages
   - Source: Deploy from branch
   - Branch: main / web
   - Save

4. **URL Final:**
   ```
   https://TU_USUARIO.github.io/capibara6/
   ```

---

## 🔧 Configuración CORS (Importante)

Si usas Vercel/Netlify/GitHub Pages, el frontend estará en un dominio diferente al servidor. Necesitas actualizar CORS:

### En `backend/auth_server.py`:
```python
CORS(app, origins=[
    'http://localhost:8000',
    'http://localhost:5500',
    'https://capibara6.vercel.app',  # Tu dominio de Vercel
    'https://capibara6.netlify.app',  # Tu dominio de Netlify
    'https://TU_USUARIO.github.io'    # Tu dominio de GitHub Pages
])
```

---

## 🎨 Opción 5: Cloudflare Tunnel (Avanzado)

### Ventajas:
- ✅ No expone tu IP
- ✅ HTTPS automático
- ✅ Subdominio personalizable

### Pasos:

1. **Instalar cloudflared:**
   ```cmd
   # Windows
   winget install Cloudflare.cloudflared
   ```

2. **Crear túnel:**
   ```cmd
   cloudflared tunnel --url http://localhost:5500
   ```

3. **URL compartible:**
   ```
   https://random-name.trycloudflare.com
   ```

---

## 🌟 Recomendación Final

Para **demostración rápida (hoy mismo):**
→ **Usa Ngrok** (2 minutos de setup)

Para **uso permanente (producción):**
→ **Usa Vercel** (gratis, rápido, profesional)

Para **dominio personalizado (capibara6.com):**
→ **Usa Vercel + Dominio** (conectar tu dominio en settings)

---

## 📋 Checklist Pre-Deploy

Antes de compartir públicamente:

- [ ] Desactivar autenticación o configurar OAuth
- [ ] Verificar que el servidor Gemma esté corriendo
- [ ] Probar que el chat funciona en localhost
- [ ] Actualizar URLs si usas dominio diferente
- [ ] Configurar CORS en el backend
- [ ] Probar desde un navegador en modo incógnito

---

## 🔒 Seguridad

Si vas a compartir públicamente:

1. **Rate Limiting:** Limita peticiones por IP
2. **Autenticación:** Habilita OAuth si quieres control de acceso
3. **Monitoreo:** Revisa logs del servidor Gemma
4. **Costos:** Verifica que no excedas límites gratuitos de la VM

---

## 🆘 Troubleshooting

**Error: CORS**
- Agregar el dominio público a la configuración CORS

**Error: Mixed Content (HTTP/HTTPS)**
- Usar HTTPS en el frontend también

**Error: Can't connect to server**
- Verificar que el servidor Gemma esté accesible públicamente
- Firewall en puerto 8080 debe estar abierto

---

## 🎯 Comando Rápido (Ngrok)

```cmd
# Todo en uno
ngrok http 5500 --domain=tu-subdominio-estatico.ngrok.app
```

Con ngrok de pago puedes tener subdominio fijo.

---

**Siguiente paso:** Elige la opción que prefieras y te ayudo a configurarla paso a paso.
