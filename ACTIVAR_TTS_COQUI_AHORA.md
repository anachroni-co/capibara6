# ⚡ Activar Coqui TTS AHORA - Guía Ultra Rápida

## 🎯 Objetivo

Activar Coqui TTS en la VM para que las 3 voces (Sofía, Ana, Carlos) suenen diferentes.

---

## 🚀 Comandos (5 minutos)

```bash
# 1. Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# 2. Ver si ya está corriendo
curl http://localhost:5002/health

# Si responde "healthy" → Ya está activo ✅
# Si da error → Continuar con paso 3

# 3. Ver screens de TTS
screen -ls | grep -i tts

# 4. Matar TTS antiguos (limpieza)
pkill -f coqui_tts

# 5. Iniciar Coqui TTS con clonación
screen -S coqui-xtts
cd ~/capibara6/backend
./start_coqui_tts_py311.sh

# Espera a ver: "✅ Modelo cargado exitosamente"
# Presiona: Ctrl+A, luego D (para salir)

# 6. Verificar
curl http://localhost:5002/health
```

**Debe responder:**
```json
{
  "status": "healthy",
  "model": "xtts_v2",
  "features": ["voice_cloning", "multilingual", "custom_voices"]
}
```

---

## 🎤 Resultado

Después de activar Coqui TTS:

1. Ve a: https://www.capibara6.com/chat.html
2. **Ctrl + Shift + R** (recarga forzada)
3. Abre el selector de voces (debería estar visible ahora)
4. El banner amarillo **NO debería aparecer**
5. Prueba las 3 voces con el botón ▶️:
   - **Sofía**: Voz femenina profesional
   - **Ana**: Voz femenina joven
   - **Carlos**: Voz masculina clara

**Cada una debería sonar DIFERENTE** 🎉

---

## 🐛 Si Aún Suenan Igual

### Verificar Consola del Navegador (F12)

Busca:
```javascript
⚠️ Coqui TTS no disponible, usando Web Speech API
```

Si ves esto:
1. Verifica que TTS esté corriendo en la VM:
   ```bash
   curl http://34.175.104.187:5002/health
   ```
2. Si no responde → El firewall puede estar bloqueando:
   ```bash
   gcloud compute firewall-rules list | grep 5002
   ```
3. Si no existe la regla:
   ```bash
   gcloud compute firewall-rules create allow-coqui-tts \
       --allow=tcp:5002 \
       --source-ranges=0.0.0.0/0 \
       --description="Coqui TTS Server"
   ```

---

## 📊 Diferencias Entre Voces

| Voz | Género | Características | Ideal Para |
|-----|--------|-----------------|-----------|
| **Sofía** | Femenina | Profesional, cálida | Tutoriales, explicaciones |
| **Ana** | Femenina | Joven, amigable | Conversación casual |
| **Carlos** | Masculina | Clara, firme | Narración, presentaciones |

---

## 🎭 Clonación de Voz

**Nota importante:** La clonación de voz ahora **SÍ está visible** en el panel.

Para clonar una voz:

1. **Grabar audio** de 5-10 segundos:
   - Hablar claramente en español
   - Sin ruido de fondo
   - Una sola persona

2. En el selector de voces, busca:
   ```
   🎭 Clonar Voz Personalizada
   [Área de arrastra audio o haz clic]
   ```

3. **Arrastra tu audio** o haz clic para seleccionar

4. Espera ~5-10 segundos

5. Tu voz aparecerá en "Voces Clonadas"

⚠️ **Solo funciona en desarrollo local** (localhost) por ahora.

---

## ✅ Checklist

- [ ] TTS corriendo en VM (puerto 5002)
- [ ] Health check responde OK
- [ ] Firewall abierto (puerto 5002)
- [ ] Panel de voces visible en el chat
- [ ] Banner amarillo NO aparece
- [ ] Las 3 voces suenan diferentes
- [ ] Sección de clonación visible

---

## 💡 Comando Todo-en-Uno

Copia y pega esto en la VM:

```bash
# Detener TTS anterior
pkill -f coqui_tts 2>/dev/null

# Iniciar nuevo TTS
cd ~/capibara6/backend && \
screen -dmS coqui-xtts bash -c './start_coqui_tts_py311.sh' && \
echo "✅ TTS iniciado en screen 'coqui-xtts'" && \
sleep 3 && \
curl -s http://localhost:5002/health | json_pp
```

---

## 🎯 Resumen

1. **VM:** Inicia `./start_coqui_tts_py311.sh` en screen
2. **Navegador:** Ctrl+Shift+R
3. **Prueba:** Botones ▶️ en cada voz
4. **¡Disfruta!** Voces diferentes y clonación disponible

**⏱️ Tiempo total:** 5 minutos  
**🎉 Resultado:** 3 voces únicas + clonación visible

