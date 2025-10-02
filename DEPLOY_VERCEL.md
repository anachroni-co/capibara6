# 🌐 Desplegar Frontend en Vercel

## Guía Paso a Paso

### 1. Ir a Vercel
1. Abre [vercel.com](https://vercel.com)
2. Click en **"Sign Up"**
3. Selecciona **"Continue with GitHub"**
4. Autoriza a Vercel

### 2. Crear Nuevo Proyecto
1. Click en **"Add New..."** → **"Project"**
2. Click en **"Import Git Repository"**
3. Busca y selecciona tu repositorio **capibara6**
4. Click en **"Import"**

### 3. Configurar el Proyecto

En la pantalla de configuración:

**Configure Project:**
- **Project Name:** `capibara6` (o el que quieras)
- **Framework Preset:** `Other` (déjalo así)
- **Root Directory:** Click en **"Edit"** → Escribe: `web`
- **Build Command:** (déjalo vacío o escribe: `echo "No build needed"`)
- **Output Directory:** (déjalo vacío o: `./`)
- **Install Command:** (déjalo vacío)

**Environment Variables:**
No necesitas agregar ninguna (la URL del backend ya está en config.js)

### 4. Deploy
1. Click en **"Deploy"**
2. Espera 1-2 minutos
3. Vercel te mostrará:
   ```
   🎉 Congratulations!
   Your project has been deployed
   ```

### 5. Obtener URL
Vercel te dará una URL como:
```
https://capibara6.vercel.app
```

O si tienes dominio personalizado:
```
https://www.capibara6.com
```

## ✅ Verificar que Funciona

1. **Abre la URL de Vercel**
2. **Abre el chatbot** (botón de mensaje abajo a la derecha)
3. **Escribe tu email:** `electrohipy@gmail.com`
4. **Deberías ver:**
   - Mensaje: "✅ ¡Gracias! Hemos guardado tu email..."
   - Email de confirmación en tu correo

5. **Verifica en la consola del navegador (F12):**
   ```
   Enviando email al backend: electrohipy@gmail.com
   URL del backend: https://capibara6.com/api/save-conversation
   ✅ Email guardado y enviado correctamente
   ```

## 🐛 Si no funciona:

### El chatbot no aparece:
- Verifica que todos los archivos .js estén en `web/`
- Revisa la consola del navegador (F12) para errores

### Error de CORS:
- Verifica que el backend en Railway tenga CORS habilitado
- El código ya lo tiene, pero verifica los logs de Railway

### Emails no se envían:
- Verifica que la URL en `config.js` sea correcta
- Revisa los logs de Railway
- Abre https://capibara6.com en el navegador para verificar que el backend responde

## 💡 Tips

- Vercel despliega automáticamente en cada push a GitHub
- Puedes tener múltiples ambientes (producción, preview)
- Los deploys son instantáneos (~1 minuto)

## 🎨 Dominio Personalizado (Opcional)

Si tienes un dominio:
1. Vercel → Settings → Domains
2. Add Domain → Escribe tu dominio
3. Configura DNS según las instrucciones
4. ¡Listo!

---

**¿Problemas?** Revisa:
- Que Root Directory esté en `web`
- Que no haya errores en la consola del navegador
- Que el backend en Railway esté funcionando

