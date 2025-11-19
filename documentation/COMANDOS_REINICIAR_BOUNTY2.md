# 🔄 Comandos para Reiniciar Servicios en Bounty2

## 🎯 Script Principal (Recomendado)

### Opción 1: Script Completo de Verificación y Reinicio

**Ejecutar dentro de bounty2:**

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Ir al directorio del proyecto
cd ~/capibara6

# Ejecutar script de reinicio completo
bash scripts/check_and_restart_bounty2.sh
```

Este script:
- ✅ Verifica Ollama (puerto 11434)
- ✅ Verifica Backend Flask (puerto 5001)
- ✅ Reinicia ambos servicios si no están activos
- ✅ Asegura que escuchan en `0.0.0.0`
- ✅ Muestra estado final y comandos útiles

---

## 🚀 Opción 2: Reiniciar Solo Backend con CORS (Desde tu PC)

**Ejecutar desde tu PC local:**

```bash
./scripts/reiniciar_backend_con_cors.sh
```

Este script:
- ✅ Se conecta automáticamente a bounty2
- ✅ Detiene el servidor actual
- ✅ Actualiza código desde git
- ✅ Instala flask-cors si falta
- ✅ Reinicia el backend con CORS configurado
- ✅ Verifica que funciona

---

## 🔧 Opción 3: Script de Inicio de Servicios (Desde tu PC)

**Ejecutar desde tu PC local:**

```bash
./scripts/start_bounty2_services.sh
```

Este script:
- ✅ Verifica si los servicios ya están corriendo
- ✅ Inicia Ollama y Backend si no están activos
- ✅ Usa screen para mantener servicios corriendo

---

## 📋 Comandos Manuales (Si prefieres hacerlo paso a paso)

### 1. Conectarse a bounty2

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### 2. Detener servicios actuales

```bash
# Detener backend
screen -S capibara6-backend -X quit 2>/dev/null || kill $(lsof -ti:5001) 2>/dev/null

# Detener Ollama (si es necesario)
screen -S ollama -X quit 2>/dev/null || kill $(lsof -ti:11434) 2>/dev/null
```

### 3. Reiniciar Ollama

```bash
cd ~/capibara6
screen -dmS ollama bash -c "ollama serve; exec bash"
```

### 4. Reiniciar Backend con CORS

```bash
cd ~/capibara6/backend

# Activar entorno virtual
source venv/bin/activate

# Instalar flask-cors si falta
pip install flask-cors

# Reiniciar backend
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server.py
"
```

### 5. Verificar servicios

```bash
# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar Backend
curl http://localhost:5001/api/health

# Verificar CORS (preflight)
curl -X OPTIONS http://localhost:5001/api/health \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

---

## 📊 Verificar Estado de Servicios

### Script de verificación (desde tu PC):

```bash
./scripts/check_bounty2_status.sh
```

### O manualmente dentro de bounty2:

```bash
# Ver sesiones screen activas
screen -ls

# Ver puertos en uso
sudo ss -tulnp | grep -E "(11434|5001)"

# Ver procesos
ps aux | grep -E "(ollama|capibara6|flask)" | grep -v grep
```

---

## 🔍 Comandos Útiles para Debugging

```bash
# Ver logs del backend
screen -r capibara6-backend
# O si no está en screen:
tail -f /tmp/backend.log

# Ver logs de Ollama
screen -r ollama
# O:
tail -f /tmp/ollama.log

# Ver qué está escuchando en puerto 5001
sudo lsof -i :5001

# Ver qué está escuchando en puerto 11434
sudo lsof -i :11434

# Verificar desde fuera (desde tu PC)
curl http://34.12.166.76:5001/api/health
curl http://34.12.166.76:11434/api/tags
```

---

## ✅ Resumen Rápido

**Para reiniciar TODO en bounty2 (recomendado):**

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001" --command "cd ~/capibara6 && bash scripts/check_and_restart_bounty2.sh"
```

**Para reiniciar solo backend con CORS (desde tu PC):**

```bash
./scripts/reiniciar_backend_con_cors.sh
```

---

## 📝 Notas Importantes

1. **El script `check_and_restart_bounty2.sh` debe ejecutarse DENTRO de bounty2**
2. **Los scripts `reiniciar_backend_con_cors.sh` y `start_bounty2_services.sh` se ejecutan desde tu PC**
3. **Los servicios se ejecutan en `screen` para mantenerlos corriendo después de desconectarte**
4. **Verifica siempre que los servicios escuchen en `0.0.0.0` y no solo en `127.0.0.1`**

