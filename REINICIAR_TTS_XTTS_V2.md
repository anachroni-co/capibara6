# 🔄 Reiniciar TTS con XTTS v2

## ✅ Cambios Aplicados

Se ha actualizado Coqui TTS de `css10/vits` → **XTTS v2** (multilingüe + máxima calidad)

---

## 📋 Pasos para Activar XTTS v2

### 1. Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### 2. Detener el TTS Actual

```bash
# Ver procesos de TTS
screen -ls

# Conectar al screen de TTS
screen -r coqui-tts

# Presionar Ctrl+C para detener el servidor
# Luego Ctrl+D para salir del screen
```

### 3. Iniciar XTTS v2

```bash
cd ~/capibara6/backend
screen -S coqui-xtts
./start_coqui_tts_py311.sh
```

**⏳ Primera vez:** Descargará ~2 GB (10-15 minutos)  
**🚀 Después:** ~30 segundos (modelo en caché)

### 4. Verificar que Funciona

```bash
# Salir del screen: Ctrl+A, D
# Probar el servicio:
curl http://localhost:5002/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "model": "xtts_v2",
  "service": "coqui-tts"
}
```

---

## 🎯 Resultado

- ✅ **Calidad de voz:** ⭐⭐⭐⭐⭐ (la mejor disponible)
- ✅ **Multilingüe:** Español, Inglés, Francés, Alemán, Italiano, Portugués, Polaco, Turco, Ruso, Holandés, Checo, Árabe, Chino, Japonés, Húngaro, Coreano
- ✅ **Características:** Clonación de voz disponible
- ✅ **Sample rate:** 24 kHz (vs 22 kHz anterior)

---

## 🔧 Estado de Servicios

| Servicio | Puerto | Estado |
|----------|--------|--------|
| Gemma 3-12B | 8080 | ✅ Activo |
| Smart MCP | 5010 | ✅ Activo |
| Coqui XTTS v2 | 5002 | 🔄 Reiniciar |

---

## ✨ Próximo Paso

Después de reiniciar el TTS, **recarga la página del chat** (Ctrl+Shift+R) y prueba el botón de audio 🔊.

¡La calidad de voz será notablemente superior! 🎙️✨

