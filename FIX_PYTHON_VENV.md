# 🔧 Solución: Error "externally-managed-environment"

## ❌ Error que estás viendo

```
error: externally-managed-environment
× This environment is externally managed
```

## ✅ Solución: Usar Virtualenv

Python 3.13+ en Debian/Ubuntu protege el sistema contra instalar paquetes globalmente. Debes usar un **virtualenv**.

---

## 🚀 Solución Rápida (Ya estás en la VM)

### Si ya copiaste los archivos:

```bash
# 1. Asegúrate de estar en el directorio correcto
cd ~/capibara6/backend

# 2. Re-copiar el script actualizado desde tu PC
# (En tu PC, ejecuta:)
# gcloud compute scp backend/start_kyutai_tts.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
# gcloud compute scp backend/start_smart_mcp.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

# 3. Dar permisos
chmod +x start_kyutai_tts.sh start_smart_mcp.sh

# 4. Instalar python3-venv si no está
sudo apt update
sudo apt install -y python3-venv python3-full

# 5. Iniciar Kyutai TTS (ahora usará virtualenv automáticamente)
screen -S kyutai-tts
./start_kyutai_tts.sh
# Ctrl+A, D para salir
```

---

## 📦 Lo que hace el script actualizado

```bash
backend/start_kyutai_tts.sh
```

Este script ahora:

1. ✅ **Crea un virtualenv** en `~/capibara6/backend/venv/`
2. ✅ **Instala dependencias** dentro del virtualenv (no global)
3. ✅ **Ejecuta el servidor** usando Python del virtualenv

---

## 🔄 Proceso Completo desde Cero

### Desde tu PC:

```bash
# 1. Pull los últimos cambios del repo
cd capibara6
git pull

# 2. Ejecutar script de deploy actualizado
./deploy_services_to_vm.sh   # Linux/Mac
# o
deploy_services_to_vm.bat     # Windows
```

### En la VM:

```bash
# 1. Conectar
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# 2. Instalar python3-venv (si no está)
sudo apt update
sudo apt install -y python3-venv python3-full

# 3. Iniciar Kyutai TTS
cd ~/capibara6/backend
screen -S kyutai-tts
./start_kyutai_tts.sh
# La primera vez tardará ~5 minutos instalando dependencias
# Ctrl+A, D para salir

# 4. Iniciar Smart MCP (en otro screen)
screen -S smart-mcp
./start_smart_mcp.sh
# Ctrl+A, D para salir

# 5. Verificar
curl http://localhost:5001/health  # TTS
curl http://localhost:5003/health  # MCP
```

---

## 🎯 Verificar que Funciona

### Dentro del virtualenv:

```bash
cd ~/capibara6/backend
source venv/bin/activate
python -c "import flask; print('✅ Flask OK')"
python -c "import moshi; print('✅ Moshi OK')"
python -c "import torch; print('✅ Torch OK')"
deactivate
```

### Servidor corriendo:

```bash
# Ver procesos
ps aux | grep kyutai

# Ver logs
screen -r kyutai-tts  # Ver logs en tiempo real
```

---

## 📋 Estructura de Virtualenv

Después de ejecutar el script:

```
~/capibara6/backend/
├── venv/                      ← Virtualenv (nuevo)
│   ├── bin/python
│   ├── lib/python3.13/
│   └── ...
├── kyutai_tts_server.py
├── smart_mcp_server.py
├── start_kyutai_tts.sh       ← Script actualizado
└── start_smart_mcp.sh         ← Script actualizado
```

---

## 🐛 Troubleshooting

### Error: "python3-venv not found"

```bash
sudo apt update
sudo apt install -y python3-venv python3-full
```

### Error: "Permission denied: ./start_kyutai_tts.sh"

```bash
chmod +x start_kyutai_tts.sh start_smart_mcp.sh
```

### Reinstalar virtualenv desde cero

```bash
cd ~/capibara6/backend
rm -rf venv
./start_kyutai_tts.sh  # Creará nuevo virtualenv
```

### Ver qué instaló pip

```bash
cd ~/capibara6/backend
source venv/bin/activate
pip list
deactivate
```

---

## 💡 Por qué Virtualenv?

| Sin Virtualenv (❌) | Con Virtualenv (✅) |
|---------------------|---------------------|
| Instala global | Instala local |
| Conflictos con sistema | Aislado del sistema |
| Requiere sudo | No requiere sudo |
| Puede romper Python del OS | Seguro |
| Error PEP 668 | Sin errores |

---

## 🎉 Resultado Final

Una vez que funcione, verás:

```bash
=========================================
  Iniciando Kyutai TTS Server
=========================================
📦 Creando virtualenv...
✅ Virtualenv creado
📦 Verificando dependencias...
⚙️  Instalando Flask...
⚙️  Instalando Moshi y dependencias...
✅ Dependencias listas
🚀 Iniciando servidor en puerto 5001...

============================================================
🎙️  KYUTAI TTS SERVER - Capibara6
============================================================
📦 Modelo: kyutai/tts-1b-en_es
🔊 Sample rate: 24000 Hz
🔧 Device: CUDA
============================================================
✅ Modelo pre-cargado exitosamente
🌐 Iniciando servidor Flask en puerto 5001...
```

---

**¡Ahora tus servicios correrán en un virtualenv seguro!** 🎉

