# 🎙️ Voces Disponibles en Coqui TTS

## 🇪🇸 Voces en Español

### 1. tts_models/es/css10/vits (Actual)

**Características:**
- ✅ Español de España
- ✅ Voz femenina
- ✅ Calidad: ⭐⭐⭐⭐ (muy natural)
- ✅ Velocidad: Rápida (~1s por frase)
- ✅ Tamaño: ~100 MB

### 2. tts_models/es/mai/tacotron2-DDC

**Características:**
- Español
- Voz femenina
- Calidad: ⭐⭐⭐ (buena)
- Velocidad: Muy rápida (~0.5s)
- Tamaño: ~80 MB

**Cambiar a este modelo:**
```python
# En coqui_tts_server.py línea 17:
'model_name': 'tts_models/es/mai/tacotron2-DDC',
```

### 3. tts_models/multilingual/multi-dataset/xtts_v2 (⭐ MEJOR)

**Características:**
- ✅ **Multilingüe** (español, inglés, francés, alemán, italiano, portugués, polaco, turco, ruso, holandés, checo, árabe, chino, japonés, húngaro, coreano)
- ✅ **Clonación de voz** (puedes clonar cualquier voz con 6 segundos de audio)
- ✅ **Multi-hablante** (diferentes voces disponibles)
- ✅ Calidad: ⭐⭐⭐⭐⭐ (la mejor)
- ⚠️ Más lento (~3-5s por frase)
- ⚠️ Más pesado (~2 GB)

**Cambiar a XTTS v2:**
```python
# En coqui_tts_server.py línea 17:
'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
```

---

## 🌍 Voces en Otros Idiomas

### Inglés

```python
# Alta calidad
'tts_models/en/vctk/vits'  # Múltiples hablantes

# Jenny (muy natural)
'tts_models/en/ljspeech/tacotron2-DDC'

# XTTS v2 (mejor)
'tts_models/multilingual/multi-dataset/xtts_v2'
```

### Francés

```python
'tts_models/fr/css10/vits'
```

### Alemán

```python
'tts_models/de/thorsten/tacotron2-DDC'
```

---

## 🎯 Cómo Cambiar de Voz

### Paso 1: Editar el Archivo

**En la VM:**

```bash
cd ~/capibara6/backend

# Editar archivo
nano coqui_tts_server.py

# O crear uno nuevo con el modelo deseado
```

### Paso 2: Cambiar la Línea 17

```python
# ANTES:
COQUI_CONFIG = {
    'model_name': 'tts_models/es/css10/vits',  # ← Esta línea
    ...
}

# DESPUÉS (ejemplo con XTTS v2):
COQUI_CONFIG = {
    'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
    ...
}
```

### Paso 3: Reiniciar Servidor

```bash
# Detener servidor actual
# Ctrl+C (en la sesión de screen)

# Iniciar de nuevo
python3 coqui_tts_server.py

# La primera vez descargará el nuevo modelo
# Puede tardar 5-15 minutos dependiendo del tamaño
```

---

## 🎤 XTTS v2 - Clonación de Voz

Si usas XTTS v2, puedes **clonar cualquier voz**:

### Paso 1: Grabar Audio de Muestra

Necesitas 6-10 segundos de la voz que quieres clonar:
- Formato: WAV o MP3
- Calidad: Buena (sin ruido)
- Contenido: Cualquier frase clara

### Paso 2: Subir Audio a la VM

```bash
# Desde tu PC
gcloud compute scp mi_voz.wav gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
```

### Paso 3: Modificar `synthesize_audio()`

```python
# En coqui_tts_server.py
def synthesize_audio(text, language='es'):
    tts = load_coqui_model()
    
    # Generar con clonación de voz
    tts.tts_to_file(
        text=text,
        file_path=tmp_path,
        speaker_wav="~/capibara6/backend/mi_voz.wav",  # ← Tu audio
        language="es"
    )
```

**Resultado:** El TTS hablará con la voz del audio de muestra. 🎙️

---

## 🎨 Voces Recomendadas por Caso de Uso

| Caso de Uso | Modelo Recomendado | Por Qué |
|-------------|-------------------|---------|
| **Producción rápida** | `tts_models/es/css10/vits` | Balance perfecto calidad/velocidad |
| **Máxima calidad** | `tts_models/multilingual/multi-dataset/xtts_v2` | La mejor, multilingüe |
| **Velocidad extrema** | `tts_models/es/mai/tacotron2-DDC` | Muy rápido |
| **Clonar voz específica** | XTTS v2 + audio de muestra | Personalización total |
| **Múltiples idiomas** | XTTS v2 | Soporta 16+ idiomas |

---

## 📊 Comparativa de Modelos Español

| Modelo | Calidad | Velocidad | Tamaño | Mejor Para |
|--------|---------|-----------|--------|------------|
| **css10/vits** | ⭐⭐⭐⭐ | Rápido | 100 MB | **Producción** ✅ |
| mai/tacotron2 | ⭐⭐⭐ | Muy rápido | 80 MB | Prototipos |
| **xtts_v2** | ⭐⭐⭐⭐⭐ | Lento | 2 GB | **Máxima calidad** |

---

## 🚀 Para Cambiar de Voz Ahora

### Opción A: Usar XTTS v2 (Mejor Calidad)

**En la VM:**

```bash
cd ~/capibara6/backend

# Detener servidor
# Ctrl+C

# Crear nueva configuración
sed -i "s|tts_models/es/css10/vits|tts_models/multilingual/multi-dataset/xtts_v2|g" coqui_tts_server.py

# Reiniciar
python3 coqui_tts_server.py
# Tardará 10-15 minutos descargando modelo (solo primera vez)
```

### Opción B: Lista de Todos los Modelos

```bash
# Ver TODOS los modelos disponibles
python3 -c "from TTS.api import TTS; print(TTS().list_models())"

# O ver solo español
python3 -c "from TTS.api import TTS; [print(m) for m in TTS().list_models() if '/es/' in m]"
```

---

## 🎯 Mi Recomendación

**Para Capibara6:**

1. **Ahora:** Usa `tts_models/es/css10/vits` (rápido y bueno)
2. **Después:** Prueba `xtts_v2` (mejor calidad pero más lento)
3. **Futuro:** Clona tu propia voz con XTTS v2

---

**¿Quieres que te ayude a cambiar al modelo XTTS v2 para máxima calidad?** 🎙️✨
