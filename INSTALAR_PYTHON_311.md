# 🐍 Solución: Python 3.13 → Python 3.11 para Coqui TTS

## ❌ Problema

Coqui TTS requiere **Python <3.12**, pero tu VM tiene **Python 3.13**.

```
ERROR: Could not find a version that satisfies the requirement TTS
ERROR: No matching distribution found for TTS
```

**Causa:** Todas las versiones de Coqui TTS tienen `Requires-Python <3.12`

---

## ✅ Solución: Instalar Python 3.11

### Opción A: Deadsnakes PPA (Recomendado)

```bash
# En la VM

# 1. Agregar repositorio deadsnakes
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# 2. Instalar Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# 3. Verificar instalación
python3.11 --version
# Debería mostrar: Python 3.11.x
```

---

## 🔧 Actualizar Scripts para Usar Python 3.11

### Opción 1: Usar Python 3.11 solo para TTS

Edita `start_coqui_tts.sh`:

```bash
# ANTES:
python3 -m venv venv

# DESPUÉS:
python3.11 -m venv venv
```

### Opción 2: Script Automático

He creado un script mejorado que lo hace automáticamente:

```bash
chmod +x backend/start_coqui_tts_py311.sh
./start_coqui_tts_py311.sh
```

---

## 🚀 Procedimiento Completo

### Desde tu PC - Re-copiar archivos actualizados:

```bash
gcloud compute scp backend/fix_coqui_python.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

gcloud compute scp backend/start_coqui_tts_py311.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
```

### En la VM:

```bash
# 1. Matar proceso en puerto 5001
lsof -ti:5001 | xargs kill -9

# 2. Instalar Python 3.11
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# 3. Verificar
python3.11 --version

# 4. Iniciar Coqui TTS con Python 3.11
cd ~/capibara6/backend
chmod +x start_coqui_tts_py311.sh
screen -S coqui-tts
./start_coqui_tts_py311.sh
# Ctrl+A, D
```

---

## 🐛 Troubleshooting

### Error: "add-apt-repository: command not found"

```bash
sudo apt install -y software-properties-common
```

### Error: "PPA not found"

```bash
# Agregar manualmente
echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/deadsnakes.list

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776

sudo apt update
sudo apt install -y python3.11 python3.11-venv
```

### Puerto 5001 aún en uso:

```bash
# Ver qué proceso está usando el puerto
sudo lsof -i:5001

# Matar proceso específico
kill -9 PROCESS_ID

# O matar todo en 5001
lsof -ti:5001 | xargs kill -9
```

---

## 📋 Alternativa: Usar Python 3.11 desde Pyenv

Si no puedes usar deadsnakes:

```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Agregar a ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Recargar
source ~/.bashrc

# Instalar Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9

# Verificar
python --version  # Debería mostrar 3.11.9
```

---

## 🎯 Resultado Esperado

Una vez instalado Python 3.11:

```bash
$ ./start_coqui_tts_py311.sh

=========================================
  Iniciando Coqui TTS Server (Python 3.11)
=========================================
🐍 Usando Python: 3.11.9
📦 Creando virtualenv con Python 3.11...
✅ Virtualenv creado
📦 Verificando dependencias...
⚙️  Instalando Coqui TTS (puede tardar 5-10 minutos)...
📥 Descargando modelos y dependencias...
✅ Coqui TTS instalado exitosamente
📦 Cargando modelo Coqui TTS: tts_models/es/css10/vits
✅ Modelo Coqui TTS cargado exitosamente
🌐 Iniciando servidor Flask en puerto 5001...
 * Running on http://0.0.0.0:5001
```

---

## 📊 Versiones de Python y Compatibilidad

| Python | Coqui TTS | Estado |
|--------|-----------|--------|
| 3.8 | ✅ | Compatible |
| 3.9 | ✅ | Compatible |
| 3.10 | ✅ | Compatible |
| 3.11 | ✅ | **Recomendado** |
| 3.12 | ❌ | No compatible |
| 3.13 | ❌ | No compatible |

---

**Sigue esta guía para instalar Python 3.11 y poder usar Coqui TTS.** 🐍✨

