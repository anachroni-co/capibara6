<div align="center">

# 🦫 Capibara6

Enrutador multimodelo + frontend web para la plataforma Capibara6.

```
capibara6/
├── backend/             # Backend Flask activo (enrutador de modelos, MCP, utilidades)
├── web/                 # Frontend estático (chat y utilidades de UI)
├── api/                 # Endpoints serverless (Vercel) opcionales
├── docs/                # Documentación generada en Python
├── fine-tuning/         # Pipelines T5X/SeqIO para entrenamiento
├── k8s/                 # Manifiestos Kubernetes de despliegue
└── archived/            # Código legacy y documentación histórica
```

</div>

---

## ✨ ¿Qué incluye ahora el repositorio?

| Carpeta | Contenido |
| --- | --- |
| `backend/` | Código vivo del servidor Flask: `server.py` (router multimodelo), `ollama_client.py`, `task_classifier.py`, `mcp_connector.py`, scripts auxiliares y requisitos. |
| `web/` | Cliente web vanilla JS (chat, integraciones MCP/TTS, páginas de test). |
| `api/` | Handlers serverless (Vercel) para exponer chat/TTS/consenso cuando el backend no está disponible. |
| `docs/` | Scripts en Python que generan documentación (p. ej. API reference). |
| `fine-tuning/` | Configs y scripts para entrenamiento T5X/SeqIO en TPUs. |
| `k8s/` | Despliegues y servicios listos para Kubernetes. |
| `archived/legacy_backend/` | Servidores anteriores (Coqui TTS, consenso legacy, integrados monolíticos…). Mantener sólo como referencia. |

📌 **Nuevo**: Los servidores antiguos de TTS, consenso y el “integrated server” fueron movidos a `archived/legacy_backend/`. El backend soportado es `backend/server.py`, que enruta hacia Ollama/Anthropic/GPT-OSS mediante `ollama_client.py` y `task_classifier.py`.

---

## 🚀 Puesta en marcha rápida

### 1. Requisitos

- Python 3.11+
- Node 18+ (sólo si quieres usar los prototipos de `/api`)
- Ollama/servicios remotos para los modelos (phi3:mini, mistral, gpt-oss:20b)

### 2. Preparar entorno

```bash
cp backend/env.example backend/.env   # o usa .env.example en raíz según tu despliegue
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Lanzar backend

```bash
cd backend
python server.py
# logs indicarán si el puerto 5000 está libre; si no, escogerá uno alternativo
```

Endpoints principales:

- `POST /api/ai/generate` & `POST /api/ai/<tier>/generate`
- `POST /api/ai/classify`
- `POST /api/save-conversation`, `POST /api/save-lead`
- `GET /api/mcp/status` (si tienes MCP habilitado)

### 4. Frontend local

```bash
cd web
python -m http.server 8000
# abre http://localhost:8000
```

Ajusta `web/config.js` si el backend escucha en otro host/puerto.

### 5. (Opcional) Handlers serverless

`api/` contiene handlers vercel (Node). Puedes ejecutarlos con `vercel dev` o adaptarlos a tu despliegue serverless.

---

## 🧠 Configuración de modelos

- `backend/model_config.json`: define los tiers `fast_response`, `balanced`, `complex`.
- `backend/task_classifier.py`: heurística para elegir el tier.
- `backend/ollama_client.py`: llamadas a Ollama + fallback.
- Variables en `.env` relevantes:

```
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL_TIER=fast_response
STREAMING_ENABLED=true
FALLBACK_ENABLED=true
MODEL_CONFIG_PATH=backend/model_config.json
```

Para probar la conectividad de claves y servicios auxiliares: `python check_env.py`.

---

## 📁 Código legacy

Todo el código que ya no forma parte del flujo soportado está en `archived/legacy_backend/`. Allí encontrarás:

- `capibara6_integrated_server.py`: backend monolítico previo.
- `consensus_server.py`: servidor de consenso legacy.
- Servidores de TTS basados en Coqui (`coqui_tts_server*.py`).
- Prototipos de MCP “smart” y scripts de arranque antiguos.

Ajusta tus despliegues existentes para apuntar al nuevo backend si aún dependes de esos servicios.

---

## 📚 Documentación útil

- `CONFIGURACION.md`: guía paso a paso de variables y despliegue.
- `API_KEYS_GUIDE.md`: cómo conseguir cada API key.
- `ARCHITECTURE.md`: descripción global de arquitectura (si vas a profundizar).
- `fine-tuning/README.md`: instrucciones de entrenamiento.

---

## 🔧 Próximos pasos sugeridos

- Completar la migración de cualquier servicio que todavía use scripts legacy.
- Añadir cobertura de tests para el nuevo enrutador (`/api/ai/*`).
- Revisar `api/` y decidir si se moderniza o se integra con el backend principal.
- Automatizar despliegues (GitHub Actions / CI-CD) usando `ci-cd.yml`.

---

## 🤝 Contribuir

1. Crea un fork.
2. Instala las dependencias (`pip install -r backend/requirements.txt`).
3. Ataca un issue o abre una propuesta en discusiones.
4. Lanza un PR explicando cambios y cómo probarlos.

---

## 📬 Soporte

- Email: [info@anachroni.co](mailto:info@anachroni.co)
- Issues: abre un ticket en GitHub con logs y pasos.

---

¡Gracias por contribuir a que Capibara6 siga creciendo! 🦫

