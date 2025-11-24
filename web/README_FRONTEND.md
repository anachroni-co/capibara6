# 🌐 Frontend Capibara6 - Guía de Inicio

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

Desde la raíz del proyecto:
```bash
./start_frontend.sh
```

### Opción 2: Manual

```bash
cd web
python3 -m http.server 8000
```

### Opción 3: Con Python 2 (si no tienes Python 3)

```bash
cd web
python -m SimpleHTTPServer 8000
```

## 📍 Acceso

Una vez iniciado el servidor, abre en tu navegador:

- **Chat Principal**: http://localhost:8000/chat.html
- **Página Principal**: http://localhost:8000/index.html

## ⚙️ Configuración

El frontend está configurado para conectarse automáticamente a las VMs cuando se ejecuta en `localhost`:

- **Backend (Ollama)**: `http://34.12.166.76:5001` (VM bounty2)
- **MCP**: `http://34.175.136.104:5003` (VM gpt-oss-20b)
- **TTS**: `http://34.175.136.104:5002` (VM gpt-oss-20b)
- **N8n**: `http://34.175.136.104:5678` (VM gpt-oss-20b)

La configuración se encuentra en `web/config.js`.

## 🔍 Verificar Conexión

1. Abre la consola del navegador (F12)
2. Busca los mensajes de configuración:
   ```
   🔧 Configuración de desarrollo local activada
   🔗 Backend URL: http://34.12.166.76:5001
   📡 Servicios: {...}
   ```
3. Verifica que no haya errores de conexión

## 🐛 Troubleshooting

### Puerto 8000 ya en uso

Usa otro puerto:
```bash
python3 -m http.server 8001
```

Luego accede a: http://localhost:8001/chat.html

### Error CORS

Si ves errores CORS, verifica:
1. Que los servicios en las VMs tengan CORS habilitado
2. Que las IPs en `config.js` sean correctas
3. Que los servicios estén corriendo en las VMs

### No se conecta al backend

1. Verifica que el backend esté corriendo en bounty2:
   ```bash
   gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
   curl http://localhost:5001/api/health
   ```

2. Verifica que el firewall de Google Cloud permita conexiones desde tu IP

3. Revisa la consola del navegador para ver el error específico

## 📝 Notas

- El servidor se ejecuta en primer plano (bloquea la terminal)
- Para ejecutarlo en segundo plano, usa `&` al final del comando
- Para detenerlo, presiona `Ctrl+C`

---

**Última actualización**: Noviembre 2025

