# 📊 Estado del Proyecto Capibara6

> **Última actualización:** 2025-11-09
> **Versión actual:** 3.0.0
> **Estado:** En desarrollo activo - Implementando sistema de gemelo digital

---

## 🎯 Resumen Ejecutivo

**Capibara6** es una plataforma de IA conversacional multilingüe con arquitectura híbrida Transformer-Mamba (70%/30%), optimizada para Google TPU v5e/v6e-64 y Google ARM Axion. El sistema ofrece la mayor ventana de contexto del mercado (10M+ tokens) con compliance total para empresas y administraciones públicas europeas.

---

## 📈 Métricas Actuales

| Métrica | Valor |
|---------|-------|
| **Versión** | 3.0.0 |
| **Líneas de código backend** | ~7,896 |
| **Líneas de código frontend** | ~15,989 |
| **Líneas de código archivado** | ~50,000+ |
| **Modelos soportados** | 3 tiers (fast, balanced, complex) |
| **Contexto máximo** | 10M+ tokens |
| **Lenguajes de programación** | Python, JavaScript |
| **Frameworks** | Flask (backend), Vanilla JS (frontend) |

---

## 🏗️ Arquitectura Actual

### **Stack Tecnológico**

#### Backend
- **Framework:** Flask 3.0.0 + Flask-CORS 4.0.0
- **Python:** 3.11+
- **API:** RESTful + Server-Sent Events (SSE) para streaming
- **Modelos:** Ollama (phi3:mini, mistral, gpt-oss:20b)

#### Frontend
- **HTML5/CSS3** con diseño responsivo
- **JavaScript ES6+** vanilla (sin frameworks)
- **Fuentes:** Inter, JetBrains Mono
- **Iconos:** Lucide
- **Markdown:** Marked.js
- **Syntax Highlighting:** Highlight.js

#### Infraestructura
- **Deployment:** Vercel (frontend) + Google Cloud VM (backend)
- **Contenedores:** Docker + Docker Compose
- **Orquestación:** Kubernetes (manifiestos disponibles)
- **Bases de datos:** PostgreSQL + TimescaleDB + Redis
- **Monitoreo:** Prometheus + Grafana + Jaeger

---

## 🎨 Estado del Frontend

### **Archivos Principales**

| Archivo | Líneas | Estado | Descripción |
|---------|--------|--------|-------------|
| `web/index.html` | 829 | ✅ Operativo | Landing page con información del proyecto |
| `web/chat.html` | 612 | ⚠️ Conflicto | Página de chat (2 versiones en conflicto) |
| `web/styles.css` | 1,831 | ✅ Operativo | Estilos globales |
| `web/chat.css` | 2,689 | ✅ Operativo | Estilos del chat v1 (minimalista) |
| `web/chat-styles.css` | 1,013 | ✅ Operativo | Estilos del chat v2 (gradientes vibrantes) |
| `web/chat-app.js` | 65KB | ✅ Operativo | Lógica principal del chat |
| `web/translations.js` | 38KB | ✅ Operativo | Sistema multiidioma (ES/EN) |

### **Características Implementadas**

#### ✅ Funcionales
- ✅ Chat en tiempo real con streaming
- ✅ Sistema multiidioma (Español/Inglés)
- ✅ Renderizado de Markdown
- ✅ Syntax highlighting para código
- ✅ Sistema de rating para respuestas
- ✅ Historial de conversaciones
- ✅ Smart MCP integration
- ✅ TTS con Kyutai (v3.0.0)
- ✅ Sistema de entropía
- ✅ Perfiles y plantillas de agentes
- ✅ Animación neural en hero

#### ⚠️ En Conflicto
- ⚠️ Diseño del chat (2 versiones: minimalista vs. vibrante)

#### ❌ No Implementadas
- ❌ Visualización de modelos activos
- ❌ Panel de E2B sandboxes
- ❌ Sistema de gemelo digital
- ❌ Importador de redes sociales
- ❌ Autenticación de usuarios

---

## 🔧 Estado del Backend

### **Archivos Principales**

| Archivo | Líneas | Estado | Descripción |
|---------|--------|--------|-------------|
| `backend/server.py` | 7,896+ | ✅ Operativo | Router principal con 3 tiers de modelos |
| `backend/task_classifier.py` | - | ✅ Operativo | Clasificador de tareas (fast/balanced/complex) |
| `backend/ollama_client.py` | - | ✅ Operativo | Cliente para Ollama con fallback |
| `backend/mcp_connector.py` | - | ✅ Operativo | Conector MCP con contexto 10M+ tokens |
| `backend/requirements.txt` | 53 | ✅ Sin conflictos | Dependencias Python |

### **Endpoints Activos**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/ai/generate` | POST | Generación con clasificación automática |
| `/api/ai/<tier>/generate` | POST | Generación en tier específico (fast/balanced/complex) |
| `/api/ai/classify` | POST | Clasificar tarea para seleccionar tier |
| `/api/save-conversation` | POST | Guardar conversación del usuario |
| `/api/save-lead` | POST | Guardar lead del usuario |
| `/api/mcp/status` | GET | Estado del sistema MCP |
| `/api/tts/*` | POST/GET | Endpoints de TTS (Kyutai) |

### **Modelos Configurados**

```json
{
  "fast_response": {
    "model": "phi3:mini",
    "max_tokens": 512,
    "timeout": 5
  },
  "balanced": {
    "model": "mistral",
    "max_tokens": 1024,
    "timeout": 10
  },
  "complex": {
    "model": "gpt-oss:20b",
    "max_tokens": 2048,
    "timeout": 120
  }
}
```

**Endpoint Ollama:** `http://10.164.0.9:11434`

---

## 📦 Módulos Archivados

El directorio `archived/` contiene **~50,000 líneas** de código de módulos enterprise avanzados:

### **Backend Modules (`archived/backend_modules/`)**

| Módulo | Estado | Descripción |
|--------|--------|-------------|
| **ACE Framework** | 🟡 Archivado | Sistema de consciencia artificial |
| **Agents** | 🟡 Archivado | Sistema de agentes especializados |
| **Execution (E2B)** | 🟡 Archivado | ✅ **Listo para reactivar** - Sandboxes de código |
| **Monitoring** | 🟡 Archivado | Monitoreo Prometheus/Grafana |
| **RAG** | 🟡 Archivado | Retrieval Augmented Generation |
| **Vector Stores** | 🟡 Archivado | FAISS, ChromaDB, embeddings |
| **CAG (Context-Aware Generation)** | 🟡 Archivado | Generación con contexto avanzado |

### **E2B Integration (Execution)**

**Estado:** ✅ **Sistema completo disponible** - Listo para integrar en frontend

**Componentes:**
- `e2b_integration.py` - Integración completa con ACE
- `e2b_manager.py` - Gestor de sandboxes concurrentes
- `execution_loop.py` - Loop de ejecución multi-round
- `code_detector.py` - Detector de código en respuestas
- `feedback_loop.py` - Feedback loop con ACE
- `error_mapping.py` - Mapeo de errores

**Capacidades:**
- ✅ Ejecución de código en sandboxes aislados
- ✅ Soporte multi-lenguaje (Python, JS, SQL, Bash, etc.)
- ✅ Límites de recursos (CPU, memoria, timeout)
- ✅ Corrección automática de errores
- ✅ Pool de sandboxes reutilizables
- ✅ Logs de ejecución para fine-tuning
- ✅ Detección automática de código en respuestas

---

## 🚀 Funcionalidades Clave

### **1. Sistema de Routing Multi-Tier**
- Clasificación automática de queries (fast/balanced/complex)
- Fallback automático entre modelos
- Optimización de costos y latencia

### **2. MCP (Model Context Protocol)**
- Contexto extendido de 10M+ tokens
- Arquitectura híbrida Transformer-Mamba (70%/30%)
- Soporte Google TPU v5e/v6e-64
- Modo compliance para sector público EU

### **3. TTS (Kyutai)**
- Síntesis de voz de alta calidad
- Control emocional de voz
- Clonación de voz avanzada
- 8+ idiomas soportados
- 15% menos consumo de recursos vs Coqui

### **4. Sistema Multiidioma**
- Español e Inglés
- Traducción dinámica de UI
- 180+ strings traducidos

---

## 🔄 Cambios Recientes

### **v3.0.0 (2025-11-07)**
- ✅ Integración completa de Kyutai TTS (reemplaza Coqui)
- ✅ Implementación de TOON (Token-Oriented Object Notation)
- ✅ Actualización de endpoints API para Kyutai
- ✅ Mejora de latencia del 20%

### **v2.1.0 (2025-10-15)**
- ✅ Smart MCP Server para análisis de contexto
- ✅ Sistema de consenso multi-modelo
- ✅ Fallback Web Speech API

### **Hoy (2025-11-09)**
- ✅ Resolución de conflictos de merge en `requirements.txt` y `config.js`
- 🔄 En progreso: Resolución de conflicto en `chat.html`

---

## 🎯 En Desarrollo Activo

### **Fase Actual: Sistema de Gemelo Digital**

#### Objetivos:
1. ✅ Resolver conflicto en `chat.html` (usar versión 2 - gradientes vibrantes)
2. 🔄 Implementar visualización de modelos activos
3. 🔄 Integrar panel de E2B sandboxes
4. 🔄 Crear importador de perfiles de redes sociales
5. 🔄 Desarrollar sistema de gemelo digital con fine-tuning personalizado
6. 🔄 Panel avanzado con métricas de personalidad

---

## 📊 Desglose de Código

### **Por Directorio**

```
capibara6/
├── backend/          ~8,000 líneas (activo)
├── web/              ~16,000 líneas (activo)
├── api/              ~500 líneas (serverless)
├── archived/         ~50,000 líneas (enterprise modules)
├── fine-tuning/      ~5,000 líneas (T5X, SeqIO)
├── k8s/              ~1,000 líneas (manifiestos)
└── docs/             ~2,000 líneas (documentación)
```

### **Por Lenguaje**

| Lenguaje | Líneas | Porcentaje |
|----------|--------|------------|
| Python | ~55,000 | 65% |
| JavaScript | ~18,000 | 22% |
| HTML/CSS | ~8,000 | 10% |
| YAML/JSON | ~2,500 | 3% |

---

## 🐛 Problemas Conocidos

### **Críticos**
- ⚠️ Conflicto de merge en `chat.html` (2 versiones)

### **Menores**
- 🟡 Chatbot de `index.html` comentado temporalmente
- 🟡 Código legacy en `archived/` necesita evaluación para reactivación
- 🟡 Mix de español/inglés en código y comentarios

---

## 🔐 Seguridad y Compliance

- ✅ GDPR compliance
- ✅ CCPA compliance
- ✅ AI Act (EU) compliance
- ✅ Certificación para sector público
- ✅ Auditorías de seguridad y ética integradas

---

## 📞 Información de Contacto

**Organización:** Anachroni s.coop
**País:** España
**Website:** https://www.anachroni.co
**Email:** info@anachroni.co
**LinkedIn:** https://www.linkedin.com/company/anachroni/
**Licencia:** MIT / Apache 2.0

---

## 🔗 Enlaces Importantes

- **Producción:** https://www.capibara6.com
- **GitHub:** https://github.com/anachroni-co/capibara6
- **Documentación:** En desarrollo
- **Changelog:** `/CHANGELOG.md`

---

## 📝 Notas de Desarrollo

### **Próximos Pasos Inmediatos**
1. Resolver conflicto `chat.html` → Versión 2 (gradientes)
2. Implementar visualización de modelos en tiempo real
3. Integrar panel E2B desde `archived/backend_modules/execution/`
4. Desarrollar importador de redes sociales (Twitter, LinkedIn, Instagram, GitHub)
5. Crear sistema de análisis NLP para gemelo digital
6. Implementar fine-tuning personalizado con datos del usuario

### **Decisiones Técnicas Pendientes**
- [ ] Definir estrategia de almacenamiento de perfiles de gemelo digital
- [ ] Seleccionar APIs/scrapers para redes sociales
- [ ] Decidir modelo base para fine-tuning de gemelo digital
- [ ] Definir métricas de similitud de personalidad

---

**Estado:** 🟢 Sistema operativo y estable. En desarrollo activo de nuevas funcionalidades.
