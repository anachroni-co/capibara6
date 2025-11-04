# Capibara6 - Asistente de IA Avanzado

Un asistente de inteligencia artificial conversacional con capacidades de síntesis de voz (TTS) y protocolo de contexto de modelo (MCP) integradas.

## 🚀 Características Principales

- **Chat Inteligente**: Interfaz conversacional con GPT-OSS-20B
- **Síntesis de Voz**: TTS con múltiples voces y clonación
- **Smart MCP**: Contexto inteligente para respuestas más precisas
- **Interfaz Web**: Aplicación web moderna y responsive
- **Despliegue en la Nube**: Configurado para Google Cloud y Vercel

## 🏗️ Arquitectura

```
capibara6/
├── web/                    # Frontend (HTML, CSS, JS)
├── api/                    # Proxies de Vercel
├── backend/                # Servidores Flask
│   ├── capibara6_integrated_server.py  # Servidor principal
│   ├── smart_mcp_server.py             # Smart MCP
│   ├── coqui_tts_server.py             # TTS
│   └── requirements.txt
├── fine-tuning/            # Fine-tuning GPT-OSS-20B
│   ├── configs/            # Configuraciones T5X
│   ├── scripts/            # Scripts de entrenamiento
│   ├── datasets/           # Configuración SeqIO
│   └── t5x/                # Código T5X
├── archived/               # Archivos obsoletos
└── docs/                   # Documentación
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/capibara6.git
cd capibara6
```

### 2. Configurar el backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar con tus valores
nano .env
```

### 4. Ejecutar servidor local

```bash
python capibara6_integrated_server.py
```

### 5. Abrir la aplicación

Navega a `http://localhost:8000` en tu navegador.

## 🌐 Despliegue en Producción

### Google Cloud VM (Backend)

El backend se ejecuta en una VM de Google Cloud con el modelo GPT-OSS-20B:

```bash
# Conectar a la VM
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Ejecutar servidor
python3 capibara6_integrated_server.py
```

### Vercel (Frontend)

El frontend se despliega automáticamente en Vercel:

1. Conecta tu repositorio a Vercel
2. Configura las variables de entorno
3. Despliega automáticamente

## 🔧 Configuración

### Variables de Entorno

```bash
# Backend
GPTOSS_API_URL=http://34.175.215.109:8080/completion
GPTOSS_HEALTH_URL=http://34.175.215.109:8080/health

# TTS
COQUI_TTS_ENABLED=true
TTS_MODEL_NAME=tts_models/multilingual/multi-dataset/xtts_v2

# MCP
MCP_ENABLED=true
MCP_SERVER_URL=http://34.175.215.109:5003/analyze
```

### Puertos

- **5001**: Servidor principal integrado
- **5002**: Servidor TTS
- **5003**: Servidor Smart MCP
- **8080**: Modelo GPT-OSS-20B (llama-server)

## 📚 Documentación

- [Guía de Fine-tuning](fine-tuning/README.md) - Entrenamiento de modelos
- [API Reference](docs/API.md) - Documentación de la API
- [Troubleshooting](archived/docs/TROUBLESHOOTING.md) - Solución de problemas

## 🛠️ Desarrollo

### Estructura del Proyecto

- **Frontend**: HTML/CSS/JavaScript vanilla
- **Backend**: Flask con Python 3.11+
- **Modelo**: GPT-OSS-20B con llama.cpp
- **TTS**: Coqui TTS con clonación de voz
- **MCP**: Sistema de contexto inteligente

### Scripts Útiles

```bash
# Validar setup
python fine-tuning/scripts/validate_setup.py

# Monitorear entrenamiento
python fine-tuning/scripts/monitor_training.py

# Lanzar fine-tuning
./fine-tuning/scripts/launch_training.sh
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

Si tienes problemas:

1. Revisa la [documentación](docs/)
2. Consulta [Troubleshooting](archived/docs/TROUBLESHOOTING.md)
3. Abre un [issue](https://github.com/tu-usuario/capibara6/issues)

## 🙏 Agradecimientos

- [GPT-OSS-20B](https://huggingface.co/microsoft/DialoGPT-medium) por Microsoft
- [Coqui TTS](https://github.com/coqui-ai/TTS) por Coqui AI
- [T5X](https://github.com/google-research/t5x) por Google Research
- [SeqIO](https://github.com/google/seqio) por Google

---

**Capibara6** - Tu asistente de IA de confianza 🦫
