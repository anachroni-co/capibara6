# 🚀 Comandos para Iniciar Servicios - Ejecutar Manualmente

## ⚠️ IMPORTANTE: Ejecuta estos comandos directamente en tu terminal

Los servicios necesitan iniciarse manualmente conectándote a cada VM.

---

## 1️⃣ Backend en bounty2 (Puerto 5001)

### Conectarse a bounty2:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### Una vez dentro de la VM, ejecuta:
```bash
cd ~/capibara6/backend

# Verificar si ya está corriendo
lsof -ti:5001 && echo "Ya está corriendo" || echo "Necesita iniciarse"

# Si no está corriendo, iniciarlo:
source venv/bin/activate

# Buscar el servidor correcto
ls -la *integrated*.py *server*.py

# Iniciar en screen (reemplaza SERVER_FILE con el archivo correcto)
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server_ollama.py
"

# Esperar unos segundos y verificar
sleep 3
curl http://localhost:5001/api/health

# Si funciona, salir de screen (Ctrl+A luego D)
# Para ver logs después: screen -r capibara6-backend
```

---

## 2️⃣ Smart MCP en gpt-oss-20b (Puerto 5010)

### Conectarse a gpt-oss-20b:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

### Una vez dentro de la VM, ejecuta:
```bash
cd ~/capibara6/backend

# Verificar si ya está corriendo
lsof -ti:5010 && echo "Ya está corriendo" || echo "Necesita iniciarse"

# Si no está corriendo, iniciarlo:
source venv/bin/activate

# Verificar que existe el archivo
ls -la smart_mcp_server.py

# Iniciar en screen
screen -dmS smart-mcp bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5010
    python3 smart_mcp_server.py
"

# Esperar unos segundos y verificar
sleep 3
curl http://localhost:5010/health

# Si funciona, salir de screen (Ctrl+A luego D)
# Para ver logs después: screen -r smart-mcp
```

---

## ✅ Verificación Final

### Desde tu PC local, ejecuta:

```bash
# Verificar Backend en bounty2
curl http://34.12.166.76:5001/api/health

# Verificar Smart MCP en gpt-oss-20b
curl http://34.175.136.104:5010/health
```

Si ambos responden correctamente, el frontend debería funcionar sin errores.

---

## 🔍 Troubleshooting

### Si el servicio no responde desde fuera:

1. **Verificar que escucha en 0.0.0.0**:
   ```bash
   sudo ss -tulnp | grep 5001
   # Debe mostrar 0.0.0.0:5001, no 127.0.0.1:5001
   ```

2. **Verificar firewall**:
   ```bash
   gcloud compute firewall-rules list --project=mamba-001 | grep -E "(5001|5010)"
   ```

3. **Ver logs del servicio**:
   ```bash
   screen -r capibara6-backend  # Para backend
   screen -r smart-mcp          # Para Smart MCP
   ```

### Si el puerto está en uso:

```bash
# Ver qué proceso usa el puerto
lsof -ti:5001

# Matar el proceso si es necesario
kill $(lsof -ti:5001)
```

---

## 📝 Notas Importantes

- Los servicios se ejecutan en `screen` para que sigan corriendo después de cerrar SSH
- Para ver los screens activos: `screen -ls`
- Para entrar a un screen: `screen -r [nombre]`
- Para salir de un screen sin cerrarlo: `Ctrl+A` luego `D`
- Para cerrar un screen: `screen -S [nombre] -X quit`

---

## 🎯 Resumen Rápido

1. Conectarte a bounty2 → Iniciar backend en puerto 5001
2. Conectarte a gpt-oss-20b → Iniciar Smart MCP en puerto 5010
3. Verificar desde local que ambos responden
4. Probar el frontend - debería funcionar sin errores

