# 🚀 Scripts de Deploy - Guía Rápida

## Dos versiones disponibles

| Script | Plataforma | Características |
|--------|------------|-----------------|
| `deploy_services_to_vm.bat` | Windows | Básico, compatible CMD |
| `deploy_services_to_vm.sh` | Linux/Mac | Con colores, muestra IP automáticamente |

---

## 🪟 Windows

```cmd
deploy_services_to_vm.bat
```

---

## 🐧 Linux / Mac

```bash
# Dar permisos de ejecución (solo la primera vez)
chmod +x deploy_services_to_vm.sh

# Ejecutar
./deploy_services_to_vm.sh
```

### Ventajas de la versión .sh:

- ✅ **Colores en output** (mejor visualización)
- ✅ **Muestra la IP de tu VM automáticamente**
- ✅ **Manejo de errores mejorado**
- ✅ **Progress indicators**

---

## 📋 Lo que hacen ambos scripts

1. ✅ Crean directorios en la VM
2. ✅ Copian `kyutai_tts_server.py`
3. ✅ Copian `smart_mcp_server.py`
4. ✅ Copian `requirements.txt`
5. ✅ Copian `start_kyutai_tts.sh`
6. ✅ Configuran firewall (puertos 5001 y 5003)
7. ✅ Instalan dependencias Python

---

## 🎯 Después de ejecutar el script

Ambos scripts te mostrarán los siguientes pasos:

### 1. Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### 2. Iniciar Kyutai TTS

```bash
screen -S kyutai-tts
cd ~/capibara6/backend
./start_kyutai_tts.sh
# Ctrl+A, luego D para salir
```

### 3. Iniciar Smart MCP

```bash
screen -S smart-mcp
cd ~/capibara6/backend
python3 smart_mcp_server.py
# Ctrl+A, luego D para salir
```

### 4. Verificar servicios

```bash
# Desde dentro de la VM
curl http://localhost:5001/health  # TTS
curl http://localhost:5003/health  # MCP

# O desde tu PC (reemplaza VM_IP)
curl http://VM_IP:5001/health
curl http://VM_IP:5003/health
```

---

## 🔧 Variables de Configuración

Ambos scripts usan esta configuración:

```bash
VM_NAME="gemma-3-12b"
ZONE="europe-southwest1-b"
```

Si tu VM tiene otro nombre o está en otra zona, edita estas variables al inicio del script.

---

## 🐛 Troubleshooting

### Error: "No se pudo conectar a la VM"

**Causa:** La VM no está corriendo o no tienes permisos.

**Solución:**
```bash
# Ver VMs corriendo
gcloud compute instances list

# Iniciar VM si está detenida
gcloud compute instances start gemma-3-12b --zone=europe-southwest1-b
```

### Error: "Permission denied" (solo Linux/Mac)

**Causa:** El script no tiene permisos de ejecución.

**Solución:**
```bash
chmod +x deploy_services_to_vm.sh
```

### Error al instalar dependencias

**Causa:** Memoria insuficiente o dependencias pesadas (torch, moshi).

**Solución:**
```bash
# Conectar a la VM e instalar manualmente
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Instalar en partes
pip install --user flask flask-cors
pip install --user torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install --user moshi soundfile numpy
```

---

## 📊 Servicios Finales

Una vez completado, tendrás estos servicios corriendo:

| Servicio | Puerto | Comando para verificar |
|----------|--------|------------------------|
| Gemma Model | 8080 | `curl localhost:8080/health` |
| Kyutai TTS | 5001 | `curl localhost:5001/health` |
| Smart MCP | 5003 | `curl localhost:5003/health` |

---

## ✅ Siguientes pasos

Después de deployar con estos scripts:

1. ✅ Configurar `KYUTAI_TTS_URL` en Vercel
2. ✅ Re-deploy en Vercel
3. ✅ Probar el botón "Escuchar" en el chat

Ver `DEPLOY_AHORA.md` para instrucciones completas.

---

**¡Elige el script según tu sistema operativo y ejecuta!** 🚀

