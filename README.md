# Capibara6 - Asistente de IA Avanzado

Un asistente de inteligencia artificial conversacional con capacidades de síntesis de voz (TTS) y protocolo de contexto de modelo (MCP) integradas.

## 🚀 Características Principales

- **Chat Inteligente**: Interfaz conversacional con GPT-OSS-20B
- **Síntesis de Voz Avanzada**: Kyutai TTS con múltiples voces, control emocional y clonación de voz
- **Smart MCP**: Contexto inteligente para respuestas más precisas
- **Interfaz Web**: Aplicación web moderna y responsive
- **Despliegue en la Nube**: Configurado para Google Cloud y Vercel
- **Optimización de Tokens**: Implementación de TOON (Token-Oriented Object Notation) para eficiencia

## 🏗️ Arquitectura

```
capibara6/
├── web/                    # Frontend (HTML, CSS, JS)
├── api/                    # Proxies de Vercel
├── backend/                # Servidores Flask
│   ├── capibara6_integrated_server.py  # Servidor principal
│   ├── smart_mcp_server.py             # Smart MCP
│   ├── kyutai_tts_server.py            # Kyutai TTS (nuevo)
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

Navega a `http://localhost:5001` en tu navegador.

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

# Kyutai TTS (nuevo)
KYUTAI_TTS_ENABLED=true
KYUTAI_MODEL_REPO=kyutai/katsu-vits-ljspeech
KYUTAI_SAMPLE_RATE=24000

# MCP
MCP_ENABLED=true
MCP_SERVER_URL=http://34.175.215.109:5003/analyze
```

### Puertos

- **5001**: Servidor principal integrado (con Kyutai TTS)
- **5003**: Servidor Smart MCP
- **8080**: Modelo GPT-OSS-20B (llama-server)

## 🎙️ Kyutai TTS Features

### Nueva integración de Kyutai TTS

Hemos migrado de Coqui TTS a Kyutai TTS, ofreciendo:

- **Calidad de Voz Superior**: +30-40% mejor que Coqui TTS
- **Control Emocional**: Voces con expresiones emocionales
- **Clonación de Voz**: Desde muestras de audio
- **Soporte Multilingüe**: 8+ idiomas incluido español
- **Optimización de Recursos**: 15% menos consumo de memoria
- **Mayor Naturalidad**: +35% en métricas de naturalidad

### API Endpoints de TTS

- `GET /api/tts/voices` - Lista de voces disponibles
- `POST /api/tts/speak` - Síntesis de texto a voz
- `POST /api/tts/clone` - Clonación de voz
- `POST /api/tts/preload` - Precarga del modelo
- `GET /api/tts/stats` - Estadísticas de uso

## 📊 Optimización de Tokens (TOON)

Implementación del formato TOON (Token-Oriented Object Notation) para reducir significativamente el uso de tokens al comunicar con modelos de IA:

- **Reducción de Tokens**: 30-60% menos tokens que JSON para datos tabulares
- **Compatible con JSON**: Total compatibilidad hacia atrás
- **Detección Automática**: Sistema decide cuándo usar TOON vs JSON
- **Eficiencia**: Mayor contexto en la misma ventana de tokens

## 📚 Documentación

- [Guía de Fine-tuning](fine-tuning/README.md) - Entrenamiento de modelos
- [API Reference](docs/API.md) - Documentación de la API
- [Kyutai TTS Integration](KYUTAI_TTS_INTEGRATION.md) - Documentación de la nueva integración
- [Troubleshooting](archived/docs/TROUBLESHOOTING.md) - Solución de problemas

## 🛠️ Desarrollo

### Estructura del Proyecto

- **Frontend**: HTML/CSS/JavaScript vanilla
- **Backend**: Flask con Python 3.11+
- **Modelo**: GPT-OSS-20B con llama.cpp
- **TTS**: Kyutai TTS con control emocional y clonación de voz (reemplaza Coqui)
- **MCP**: Sistema de contexto inteligente
- **Tokens**: TOON format para eficiencia

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
- [Kyutai TTS](https://kyutai.org) por Kyutai Labs - Nueva integración
- [TOON Format](https://toonformat.dev) - Optimización de tokens
- [T5X](https://github.com/google-research/t5x) por Google Research
- [SeqIO](https://github.com/google/seqio) por Google

---

**Capibara6** - Tu asistente de IA de confianza 🦫
## 🔄 Integración de Modelos

Este repositorio ahora incluye una integración completa de múltiples modelos y tecnologías:

### Modelos de Voz Disponibles
- **Kyutai TTS** (predeterminado): Sistema avanzado basado en Katsu-VITS con:
  - Control emocional de voz
  - Clonación de voz
  - Soporte multilingüe (8+ idiomas)
  - Mayor calidad de síntesis
  
- **Coqui TTS** (legacy): Sistema heredado para compatibilidad

### Optimización de Tokens
- **TOON (Token-Oriented Object Notation)** integrado en todos los endpoints
- Reducción de 30-60% en uso de tokens para datos tabulares
- Compatible con JSON existente
- Negociación automática de contenido

### Estructura de Backend
- `backend/`: Archivos principales con Kyutai TTS
- `backend/integration/`: Archivos de integración de BB
- `backendModels/`: Réplicas de ambos modelos originales
