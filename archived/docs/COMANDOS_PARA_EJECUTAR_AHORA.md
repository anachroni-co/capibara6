# ⚡ Ejecuta Esto AHORA en la VM

## 🎯 Estás en la VM - Ejecuta Estos Comandos

### 1. Verificar Estado de Todos los Servicios

```bash
cd ~/capibara6/backend
chmod +x check_all_services.sh
./check_all_services.sh
```

Esto te mostrará:
- ✅ Qué servicios están activos
- ❌ Qué servicios están inactivos
- 🖥️ Sesiones de screen corriendo
- 🔌 Puertos en uso

---

### 2. Si Necesitas Re-copiar el Script

**Desde tu PC (otra terminal):**

```bash
gcloud compute scp backend/check_all_services.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
```

**En la VM:**

```bash
cd ~/capibara6/backend
chmod +x check_all_services.sh
./check_all_services.sh
```

---

## 🚀 Iniciar Servicios Faltantes

### Si Smart MCP NO está corriendo:

```bash
cd ~/capibara6/backend
screen -S smart-mcp
./start_smart_mcp.sh
# Ctrl+A, D para salir
```

### Si Coqui TTS NO está corriendo:

```bash
cd ~/capibara6/backend
screen -S coqui-tts
./start_coqui_tts_py311.sh
# Ctrl+A, D para salir
```

---

## 📋 Comandos Directos (sin script)

Si prefieres verificar manualmente:

```bash
# Ver sesiones de screen
screen -ls

# Verificar servicios uno por uno
curl http://localhost:8080/health  # Gemma
curl http://localhost:5003/health  # Smart MCP
curl http://localhost:5002/health  # Coqui TTS

# Ver puertos en uso
sudo lsof -i -P -n | grep LISTEN | grep -E "5001|5002|5003|8080"
```

---

## ✅ Resultado Esperado

Deberías ver:

```
🔍 Gemma Model     (puerto 8080): ✅ ACTIVO
🔍 Smart MCP       (puerto 5003): ✅ ACTIVO
🔍 Coqui TTS       (puerto 5002): ✅ ACTIVO
```

---

## 🔧 Si Smart MCP no está activo:

```bash
# Iniciar Smart MCP
cd ~/capibara6/backend
screen -S smart-mcp
python3 smart_mcp_server.py
# Ctrl+A, D

# Verificar
curl http://localhost:5003/health
```

---

**Ejecuta `./check_all_services.sh` primero y dime qué muestra.** 🔍

