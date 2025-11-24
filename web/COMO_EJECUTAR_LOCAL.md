# 🚀 Cómo Ejecutar el Chat Localmente

## 📍 Ubicación del Archivo

El archivo `chat.html` está ubicado en:
```
/mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC/web/chat.html
```

O en Windows:
```
C:\Users\elect\.cursor\worktrees\capibara6\NxnaC\web\chat.html
```

## 🌐 Dirección Local

Una vez ejecutado el servidor web, el chat estará disponible en:
```
http://localhost:8000/chat.html
```

O si el puerto 8000 está ocupado:
```
http://localhost:8080/chat.html
```

## 🖥️ Opción 1: Usar el Script Python (Recomendado)

El proyecto incluye un script para iniciar el servidor web local:

```bash
# Desde la raíz del proyecto
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC

# Ejecutar el servidor
python3 web/start_local_test_server.py
```

O desde Windows (WSL):
```bash
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC
python3 web/start_local_test_server.py
```

El servidor iniciará en `http://localhost:8000` y mostrará:
- ✅ URL del chat: `http://localhost:8000/chat.html`
- ✅ URL de la página principal: `http://localhost:8000/index.html`
- ✅ URL de pruebas: `http://localhost:8000/verify_real_vm_connection.html`

## 🖥️ Opción 2: Servidor HTTP Simple de Python

Si prefieres usar el servidor HTTP simple directamente:

```bash
# Navegar a la carpeta web
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC/web

# Python 3
python3 -m http.server 8000

# O Python 2 (si no tienes Python 3)
python -m SimpleHTTPServer 8000
```

Luego accede a: `http://localhost:8000/chat.html`

## 🖥️ Opción 3: Servidor HTTP de Node.js

Si tienes Node.js instalado:

```bash
# Instalar http-server globalmente (solo una vez)
npm install -g http-server

# Navegar a la carpeta web
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC/web

# Iniciar servidor
http-server -p 8000
```

## 🖥️ Opción 4: Usar Vercel CLI (Para Desarrollo)

Si tienes Vercel CLI instalado:

```bash
# Desde la raíz del proyecto
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC

# Iniciar servidor de desarrollo
npm run dev
```

Esto iniciará Vercel Dev en `http://localhost:3000`

## ⚠️ ¿Por qué necesitas un servidor web?

**SÍ, necesitas ejecutar un servidor web** porque:

1. **CORS (Cross-Origin Resource Sharing)**: Los navegadores bloquean las solicitudes AJAX/fetch desde archivos locales (`file://`) por seguridad.

2. **Módulos ES6**: Los scripts modernos usan `import/export` que requieren un servidor HTTP.

3. **Recursos relativos**: Los archivos CSS, JS e imágenes se cargan mejor con rutas relativas desde un servidor.

4. **Conexión con VMs**: El frontend necesita hacer solicitudes HTTP a las VMs de GCloud, lo cual requiere un servidor web.

## 🔧 Configuración de Conexión

El archivo `web/config.js` está configurado para:
- **Desarrollo local**: Conecta a las IPs de las VMs de GCloud
- **Producción**: Conecta a `https://www.capibara6.com`

Cuando ejecutes el servidor local, el frontend detectará automáticamente que estás en `localhost` y usará las IPs de las VMs configuradas.

## 📋 URLs Disponibles

Una vez que el servidor esté corriendo:

| Archivo | URL |
|---------|-----|
| Chat principal | `http://localhost:8000/chat.html` |
| Página principal | `http://localhost:8000/index.html` |
| Login | `http://localhost:8000/login.html` |
| Dashboard N8n | `http://localhost:8000/n8n-dashboard.html` |
| Demo RAG | `http://localhost:8000/rag-demo.html` |
| Pruebas de conexión | `http://localhost:8000/verify_real_vm_connection.html` |

## 🛑 Detener el Servidor

Presiona `CTRL+C` en la terminal donde está corriendo el servidor.

## ✅ Verificación Rápida

Para verificar que todo funciona:

1. Ejecuta el servidor:
   ```bash
   python3 web/start_local_test_server.py
   ```

2. Abre tu navegador y ve a:
   ```
   http://localhost:8000/chat.html
   ```

3. Abre la consola del navegador (F12) y verifica:
   - ✅ No hay errores de CORS
   - ✅ Los scripts se cargan correctamente
   - ✅ La conexión con las VMs se verifica automáticamente

## 🔍 Troubleshooting

### Puerto ocupado
Si el puerto 8000 está ocupado, el script intentará usar el 8080 automáticamente.

### Error de CORS
Si ves errores de CORS, asegúrate de estar usando el servidor web (no abriendo el archivo directamente con `file://`).

### Scripts no cargan
Verifica que todos los archivos `.js` estén en la carpeta `web/` y que las rutas en `chat.html` sean correctas.

---

**Nota**: El servidor web local solo sirve los archivos estáticos. El backend real está corriendo en las VMs de GCloud según la configuración en `config.js`.

