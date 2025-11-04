# ⚡ Solución Rápida - Errores en VM

## 🎯 Estás Aquí Ahora (en la VM)

Veo que tienes dos problemas:

1. ❌ **Python 3.13** incompatible con Coqui TTS
2. ❌ **Puerto 5001** ya en uso

---

## ✅ Solución Inmediata (3 minutos)

### Paso 1: Liberar Puerto 5001

```bash
# Matar proceso actual
lsof -ti:5001 | xargs kill -9

# Verificar
lsof -i:5001
# Debería estar vacío
```

### Paso 2: Usar Servidor Fallback Simple

Ya que Python 3.13 no soporta Coqui TTS, usa el servidor fallback:

```bash
cd ~/capibara6/backend
screen -S tts-fallback
python3 kyutai_tts_server_simple.py
# Ctrl+A, D para salir
```

Este servidor devuelve `fallback: true` y el frontend usa **Web Speech API** (que funciona bien ahora con v7.0).

### Paso 3: Verificar

```bash
curl http://localhost:5001/health

# Respuesta:
{
  "service": "tts-fallback-server",
  "status": "healthy",
  "mode": "fallback"
}
```

---

## 🚀 Solución Completa (15 minutos) - Para Alta Calidad

### Opción A: Instalar Python 3.11

```bash
# 1. Agregar repositorio
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# 2. Instalar Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# 3. Verificar
python3.11 --version

# 4. Re-copiar scripts desde tu PC
# (En tu PC ejecutar:)
# gcloud compute scp backend/start_coqui_tts_py311.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
# gcloud compute scp backend/kill_port_5001.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

# 5. Liberar puerto
chmod +x kill_port_5001.sh
./kill_port_5001.sh

# 6. Iniciar Coqui con Python 3.11
chmod +x start_coqui_tts_py311.sh
screen -S coqui-tts
./start_coqui_tts_py311.sh
# Tardará 5-10 min la primera vez
# Ctrl+A, D
```

---

## 📊 Comparación

| Solución | Tiempo | Calidad TTS | Dificultad |
|----------|--------|-------------|------------|
| **Fallback Simple** | 1 min | ⭐⭐⭐ (Web Speech) | ✅ Fácil |
| **Python 3.11 + Coqui** | 15 min | ⭐⭐⭐⭐⭐ (VITS) | ⚠️ Media |

---

## 💡 Recomendación

**Para ahora (1 minuto):**
```bash
# Usar servidor fallback
lsof -ti:5001 | xargs kill -9
screen -S tts-fallback
python3 kyutai_tts_server_simple.py
# Ctrl+A, D
```

**Para después (mejor calidad):**
- Instalar Python 3.11
- Usar Coqui TTS

---

## 🔍 Verificar Servicios Corriendo

```bash
# Ver sesiones de screen
screen -ls

# Debería mostrar:
# 5001.coqui-tts  o  5001.tts-fallback
# 5003.smart-mcp

# Reconectar a una sesión
screen -r coqui-tts
# o
screen -r tts-fallback
```

---

## 📚 Documentación Completa

- **`INSTALAR_PYTHON_311.md`** - Instalar Python 3.11
- `COQUI_TTS_SETUP.md` - Setup de Coqui
- `WEB_SPEECH_API_LIMITACIONES.md` - Info de fallback

---

**Solución rápida:** Usar servidor fallback ahora  
**Solución completa:** Instalar Python 3.11 después

**¡Cualquiera de las dos funciona!** 🚀

