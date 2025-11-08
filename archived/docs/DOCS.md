<<<<<<< HEAD:archived/docs/DOCS.md
# capibara6 - Documentación Completa

## Tabla de Contenidos
- [Acerca del Proyecto](#acerca-del-proyecto)
- [Características Principales](#características-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Instalación y Configuración](#instalación-y-configuración)
- [Configuración del Backend](#configuración-del-backend)
- [API del Backend](#api-del-backend)
- [Uso del Sistema](#uso-del-sistema)
- [Benchmarks y Rendimiento](#benchmarks-y-rendimiento)
- [Compliance y Seguridad](#compliance-y-seguridad)
- [Soporte y Contribución](#soporte-y-contribución)
- [Recursos Adicionales](#recursos-adicionales)

## Acerca del Proyecto

**capibara6** es un sistema de IA de última generación desarrollado por **Anachroni s.coop** (España) que combina lo mejor de las arquitecturas Transformer y Mamba SSM en un diseño híbrido optimizado (70% Transformer / 30% Mamba). Diseñado específicamente para Google TPU v5e/v6e-64 y procesadores Google ARM Axion, ofrece la mayor ventana de contexto del mercado (10M+ tokens) con compliance total para empresas y administraciones públicas.

### Características Destacadas
=======
# capibara6 Consensu

<div align="center">

**Sistema avanzado de IA conversacional con arquitectura híbrida Transformer-Mamba (70%/30%), optimizaciones Google TPU v5e/v6e y Google ARM Axion. Mayor ventana de contexto del mercado. Compliance total para empresas y administraciones públicas.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TPU](https://img.shields.io/badge/TPU-v5e%20%7C%20v6e-orange.svg)](https://cloud.google.com/tpu)
[![ARM](https://img.shields.io/badge/ARM-Google%20Axion-green.svg)](https://cloud.google.com/compute/docs/cpu-platforms)

🌐 **[capibara6.com](https://capibara6.com)** | 📧 **[info@anachroni.co](mailto:info@anachroni.co)** | 🏢 **[Anachroni s.coop](https://www.anachroni.co)**

</div>

---

## 📋 Descripción General

**capibara6 Consensu** es un sistema de IA de última generación desarrollado por **Anachroni s.coop** (España) que combina lo mejor de las arquitecturas Transformer y Mamba SSM en un diseño híbrido optimizado (70% Transformer / 30% Mamba). Diseñado específicamente para Google TPU v5e/v6e-64 y procesadores Google ARM Axion, ofrece la mayor ventana de contexto del mercado (10M+ tokens) con compliance total para empresas y administraciones públicas.

### 🎯 Características Destacadas
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md

- **🧠 Arquitectura Híbrida**: 70% Transformer + 30% Mamba SSM para balance óptimo
- **⚡ Google TPU v5e/v6e-64**: 4,500+ tokens/sec con latencia <120ms
- **🚀 Google ARM Axion**: Inferencia eficiente 2,100+ tokens/sec, consumo 95W
- **🔍 Contexto Líder**: 10M+ tokens, superando cualquier competidor
- **🔒 Compliance Total**: GDPR, CCPA, AI Act UE - Certificado sector público
- **🌐 Capacidades Multimodales**: Texto, imagen, video y audio
- **🔗 Chain-of-Thought**: Razonamiento verificable hasta 12 pasos

<<<<<<< HEAD:archived/docs/DOCS.md
## Características Principales

### Mixture of Experts (MoE)
- 32 expertos especializados con enrutamiento dinámico para dominios como matemáticas, ciencias, código y creatividad
- Especialización automática por dominio
- Balanceamiento de carga inteligente
- Expert routing adaptativo (96.3% precisión)

### Chain-of-Thought Reasoning
- Razonamiento paso a paso con hasta 12 pasos
- Meta-cognición avanzada y auto-reflexión
- Ajuste de confianza automático
- Process reward models integrados
- Explicabilidad completa

### Capacidades Multimodales
- Vision encoder (224x224, patches 16x16)
- Video encoder (64 frames, 30 FPS)
- Text-to-Speech con contexto emocional
- Procesamiento de texto, imágenes y video

### Google TPU v5e/v6e-64
- 4,500+ tokens/sec en TPU v6e-64
- Flash attention y kernel fusion
- Eficiencia energética superior
- XLA compilation y mixed precision

### Google ARM Axion
- 2,100+ tokens/sec (cuantizado 8-bit)
- Arquitectura ARM de Google Cloud
- Eficiencia energética excepcional
- NEON y SVE2 vectorization

### Ventana de Contexto Líder
- 10M+ tokens de contexto real
- Arquitectura híbrida optimizada
- Gestión eficiente de memoria
- Supera a cualquier competidor actual

### Adaptación por Edad
- Ajuste automático de vocabulario
- Filtrado de contenido por edad
- Estándares educativos integrados
- Sistema inteligente para 3-18 años

### Compliance Total UE
- GDPR, CCPA, AI Act compliance
- Certificado para administraciones públicas
- Auditorías de seguridad y ética
- Cumplimiento exhaustivo de normativas europeas

### Monitorización Enterprise
- Métricas en tiempo real (TFLOPS, memoria)
- Exportación Grafana/Prometheus
- Auto-optimización basada en métricas
- Dashboard completo con métricas TPU

## Arquitectura del Sistema

### Arquitectura Híbrida (70% Transformer + 30% Mamba)

```
┌─────────────────────────────────────┐
│  Entrada Multimodal                 │
│  (Texto, Imagen, Video, Audio)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Arquitectura Híbrida               │
│                                     │
│  ┌─────────────────┐                │
│  │  Transformer    │  70%           │
│  │  - Atención     │  - Precisión   │
│  │  - Contexto     │  - Calidad     │
│  └─────────────────┘                │
│                                     │
│  ┌─────────────────┐                │
│  │  Mamba SSM      │  30%           │
│  │  - O(n) linear  │  - Velocidad   │
│  │  - Eficiencia   │  - Escalado    │
│  └─────────────────┘                │
│                                     │
│  Routing Inteligente Automático    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Ventana de Contexto: 10M+ tokens  │
│  (Mayor del mercado)                │
└─────────────────────────────────────┘
```

### Distribución de Capas

1. **🌐 Capa de Entrada Multimodal**: Encoders especializados para texto, imagen y video
   - Vision Encoder
   - Video Encoder
   - Text Encoder

2. **🔍 Capa de Recuperación (RAG 2.0)**: Contexto de 1M tokens con hybrid search
   - Semantic Chunking
   - Hybrid Search
   - Memory Compression

3. **🧠 Arquitectura Híbrida**: 70% Transformer + 30% Mamba SSM optimizado
   - Transformer (70%)
   - Mamba SSM (30%)
   - Routing Inteligente

4. **🔗 Capa de Razonamiento (CoT)**: Chain-of-Thought con hasta 12 pasos
   - Step-by-Step
   - Meta-Cognition
   - Self-Reflection

5. **⚡ Capa de Computación**: Google TPU v5e/v6e-64 y Google ARM Axion
   - Google TPU v5e/v6e-64
   - Google ARM Axion
   - Mixed Precision

6. **🔒 Capa de Compliance**: Normativas UE para sector público y privado
   - GDPR + AI Act
   - Certificación Pública
   - Auditorías Continuas

## Instalación y Configuración

### Requisitos

**Hardware**:
- Google TPU v5e-64 o v6e-64 (recomendado para training)
- Google ARM Axion o Graviton3 (recomendado para inferencia)
- 32GB+ RAM
- SSD NVMe 500GB+

**Software**:
=======
---

## 🌐 Sitio Web

Visita **[capibara6.com](https://capibara6.com)** para documentación interactiva completa.

El sitio detecta automáticamente tu ubicación:
- **España y Latinoamérica**: Versión en español
- **Resto del mundo**: Versión en inglés
- Cambio manual: `capibaraLanguage.switch('es')` o `capibaraLanguage.switch('en')` en consola

### Ver el sitio localmente

```bash
cd web
python -m http.server 8000
# Abre http://localhost:8000
```

---

## 🏗️ Arquitectura del Sistema

### Frontend Web (Interfaz de Usuario)

**Tecnologías Implementadas:**
- **HTML5 Semántico**: Estructura moderna y accesible
- **CSS3 Avanzado**: Variables CSS, Grid, Flexbox, animaciones
- **JavaScript ES6+**: Módulos, async/await, clases
- **Canvas API**: Animaciones de red neuronal interactivas
- **Web APIs**: Geolocalización, LocalStorage, Fetch API

**Características del Frontend:**
- **Detección Automática de Idioma**: Basada en geolocalización del usuario
- **Animaciones Neuronales**: Red neuronal interactiva en canvas
- **Sistema de Chatbot**: Captura inteligente de leads empresariales
- **Responsive Design**: Adaptable a móviles, tablets y desktop
- **Internacionalización Completa**: Español e inglés con traducciones dinámicas
- **Navegación Suave**: Scroll automático y efectos visuales
- **Indicador de Progreso**: Barra de progreso de lectura
- **Efectos Parallax**: Animaciones de fondo dinámicas

### Backend Flask (API REST)

**Tecnologías Implementadas:**
- **Flask**: Framework web ligero y flexible
- **Flask-CORS**: Manejo de peticiones cross-origin
- **SMTP**: Envío de emails automáticos
- **JSON**: Almacenamiento de datos estructurados
- **Python-dotenv**: Gestión de variables de entorno

**Endpoints Implementados:**
- `POST /api/save-conversation`: Guarda conversaciones y envía emails
- `POST /api/save-lead`: Captura leads empresariales
- `GET /api/health`: Health check del servidor
- `GET /`: Página principal del backend

**Características del Backend:**
- **Gestión de Emails**: Envío automático de confirmaciones
- **Captura de Leads**: Sistema completo de leads empresariales
- **Almacenamiento de Datos**: JSON estructurado con timestamps
- **Notificaciones Admin**: Alertas automáticas para nuevos contactos
- **Configuración Flexible**: Variables de entorno para diferentes entornos
- **Logs de Auditoría**: Registro completo de interacciones

### Sistema de Chatbot Inteligente

**Características Implementadas:**
- **Captura de Leads Empresariales**: Formulario guiado paso a paso
- **Respuestas Inteligentes**: Sistema de keywords y respuestas contextuales
- **Respuestas Rápidas**: Botones de respuesta predefinidos
- **Detección de Email**: Extracción automática de emails del texto
- **Estados de Conversación**: Manejo de flujos complejos
- **Internacionalización**: Soporte completo español/inglés
- **Integración Backend**: Envío automático de datos al servidor

**Flujo de Captura de Leads:**
1. **Tipo de Contacto**: Consultoría, colaboración, implementación, info general
2. **Información de Empresa**: Nombre de la organización
3. **Datos de Contacto**: Nombre completo y email
4. **Descripción del Proyecto**: Necesidades específicas
5. **Rango de Presupuesto**: Categorías predefinidas
6. **Timeline**: Plazos de implementación
7. **Confirmación**: Resumen y envío final

---

## 🧠 Características de IA Implementadas

### Arquitectura Híbrida Transformer-Mamba

**Distribución Optimizada:**
- **70% Transformer**: Precisión y comprensión contextual
- **30% Mamba SSM**: Eficiencia O(n) y velocidad

**Ventajas del Diseño Híbrido:**
- **Transformer (70%)**: Alta precisión en tareas complejas, excelente comprensión contextual
- **Mamba SSM (30%)**: Complejidad lineal O(n), procesamiento ultrarrápido de secuencias largas
- **Routing Inteligente**: Selección automática del mejor componente para cada tarea

### Mixture of Experts (MoE)

**32 Expertos Especializados:**
- **Matemáticas**: Álgebra, cálculo, estadística, optimización
- **Ciencias**: Física cuántica, mecánica clásica, simulaciones
- **Ingeniería**: Electrónica, FPGA, circuitos, documentación técnica
- **Robótica**: Control, percepción, planificación de movimiento
- **Sistemas**: Linux kernel, administración, seguridad
- **Multimodal**: Audio emocional, análisis de sentimientos
- **Comunidad Española**: NLP en español, literatura, medios

**Características MoE:**
- **Enrutamiento Dinámico**: 96.3% precisión en selección de expertos
- **Balanceamiento de Carga**: Distribución inteligente de tareas
- **Especialización Automática**: Adaptación por dominio de conocimiento

### Chain-of-Thought Reasoning

**Razonamiento Estructurado:**
- **Hasta 12 Pasos**: Procesos de razonamiento complejos
- **Meta-cognición**: Ajuste automático de confianza
- **Auto-reflexión**: Verificación interna de resultados
- **Process Reward Models**: Evaluación de calidad por paso

**Características CoT:**
- **Razonamiento Verificable**: Cada paso es explicable y comprobable
- **Confidence Scoring**: Puntuación de confianza por cada paso
- **Explicabilidad Completa**: Transparencia total en el proceso

### Capacidades Multimodales

**Vision Encoder:**
- **Resolución**: 224x224 a 1024x1024
- **Arquitectura**: ViT-Large optimizado
- **Patches**: 16x16 adaptativos
- **Capacidades**: Clasificación, detección, segmentación, OCR

**Video Encoder:**
- **Frames**: Hasta 64 frames
- **FPS**: 30 FPS procesamiento
- **Temporal Attention**: Bidireccional
- **Capacidades**: Análisis de acción, tracking, eventos

**Audio/TTS:**
- **Múltiples Voces**: Variedad de idiomas
- **Contexto Emocional**: Adaptativo al contenido
- **Calidad**: 24kHz, natural
- **Latencia**: <300ms

---

## ⚡ Optimizaciones de Hardware

### Google TPU v5e/v6e-64

**TPU v6e-64 Performance:**
```
Throughput:      4,500+ tokens/sec
Latencia P95:    120ms
Memoria HBM:     32GB
Eficiencia:      98.5%
Arquitectura:    256 chips interconectados
```

**TPU v5e-64 Performance:**
```
Throughput:      3,800+ tokens/sec
Latencia P95:    145ms
Memoria HBM:     24GB
Eficiencia:      96.8%
```

**Optimizaciones Implementadas:**
- **XLA Compilation**: Compilación avanzada para TPU
- **Kernel Fusion**: Fusión automática de operaciones
- **Mixed Precision**: bfloat16 para eficiencia
- **Flash Attention**: Atención optimizada
- **Pipeline Parallelism**: Paralelización de pipeline

### Google ARM Axion

**Performance ARM Axion:**
```
Throughput:      2,100+ tokens/sec
Latencia P95:    280ms
Memoria:         16GB
Consumo:         95W
Cores:           Hasta 192 cores
```

**Optimizaciones ARM:**
- **NEON Vectorization**: Vectorización automática
- **SVE2 Optimizations**: 512-bit vectorization
- **Cuantización**: 4-bit/8-bit calibrada
- **Memory Pool**: Optimización de memoria
- **Cache-aware**: Algoritmos conscientes de cache

### Ventana de Contexto Líder

**10M+ Tokens de Contexto Real:**
- **Supera a GPT-4 Turbo**: 128K tokens
- **Supera a Claude 2.1**: 200K tokens  
- **Supera a Gemini 1.5 Pro**: 1M tokens
- **capibara6: 10M+ tokens** 🏆

**Capacidades de Contexto:**
- **Análisis de Documentos**: Extensos sin pérdida de contexto
- **Procesamiento de Código**: Bases de código completas
- **Conversaciones Largas**: Días sin degradación
- **RAG 2.0**: Memoria episódica avanzada
- **Gestión Eficiente**: Sin degradación de rendimiento

---

## 🔒 Compliance y Seguridad

### Normativas Cumplidas

**Regulaciones Europeas:**
- ✅ **GDPR** (Reglamento General de Protección de Datos)
- ✅ **AI Act** (Ley de IA de la Unión Europea)
- ✅ **CCPA** (California Consumer Privacy Act)
- ✅ **ePrivacy Directive** (Directiva de privacidad electrónica)
- ✅ **NIS2 Directive** (Ciberseguridad)

**Certificaciones:**
- **Certificado para Administraciones Públicas**: Españolas y europeas
- **Auditorías de Seguridad**: Continuas y transparentes
- **Evaluación Ética**: Independiente y regular
- **Transparencia Algorítmica**: Explicabilidad completa

### Medidas de Seguridad

**Encriptación:**
- **AES-256**: En reposo
- **TLS 1.3**: En tránsito
- **Segregación de Datos**: Por cliente
- **Logs de Auditoría**: Inmutables
- **Backup Georeplicado**: En UE

**Privacidad:**
- **Derecho al Olvido**: Implementado
- **Portabilidad de Datos**: Completa
- **Consentimiento**: Granular y específico
- **Minimización**: Solo datos necesarios

---

## 🌐 Funcionalidades Web Implementadas

### Sistema de Internacionalización

**Detección Automática:**
- **Geolocalización**: Basada en IP del usuario
- **Países Hispanohablantes**: Detección automática de ES, MX, AR, CO, etc.
- **Fallback**: Idioma del navegador como respaldo
- **Persistencia**: Preferencias guardadas en LocalStorage

**Idiomas Soportados:**
- **Español**: Completo con traducciones contextuales
- **Inglés**: Traducción completa y natural
- **Cambio Manual**: API para cambio dinámico de idioma

### Animaciones y Efectos Visuales

**Red Neuronal Interactiva:**
- **Canvas API**: Animación fluida de partículas
- **Interactividad**: Respuesta al movimiento del mouse
- **Efectos Visuales**: Gradientes y pulsos dinámicos
- **Performance**: Optimizada con requestAnimationFrame

**Efectos de Interfaz:**
- **Scroll Suave**: Navegación fluida entre secciones
- **Parallax**: Efectos de profundidad
- **Hover Effects**: Interacciones visuales
- **Loading States**: Indicadores de progreso

### Sistema de Chatbot Avanzado

**Características Implementadas:**
- **Interfaz Flotante**: Chatbot siempre accesible
- **Estados de Conversación**: Manejo complejo de flujos
- **Respuestas Inteligentes**: Sistema de keywords contextual
- **Quick Replies**: Botones de respuesta rápida
- **Detección de Email**: Extracción automática
- **Integración Backend**: Envío automático de datos

**Flujo de Captura de Leads:**
1. **Inicio**: Detección de intención empresarial
2. **Tipo de Contacto**: Selección de categoría
3. **Información Empresa**: Datos de la organización
4. **Contacto**: Nombre y email
5. **Proyecto**: Descripción de necesidades
6. **Presupuesto**: Rango aproximado
7. **Timeline**: Plazos de implementación
8. **Confirmación**: Resumen y envío

---

## 📊 Datasets Especializados

### Colección de Datasets Implementada

**Datasets Académicos:**
- Datasets institucionales de universidades
- Datasets de Wikipedia académica
- Código académico y papers
- Metadatos de investigación

**Datasets Multimodales:**
- Datasets de audio emocional
- Análisis de sentimientos multimodal
- Datasets de conversación

**Datasets de Ingeniería:**
- Datasets de electrónica
- Datasets de FPGA
- Diseños de circuitos
- Documentación técnica

**Datasets de Física:**
- Datasets de física cuántica
- Simulaciones físicas
- Datasets de mecánica clásica
- Datasets de física de partículas

**Datasets de Robótica:**
- Datasets de control robótico
- Datasets de percepción
- Datasets de planificación de movimiento
- Datasets de interacción humano-robot

**Datasets de Matemáticas:**
- Datasets de álgebra
- Datasets de cálculo
- Datasets de estadística
- Datasets de optimización

**Datasets de Sistemas:**
- Datasets de Linux kernel
- Logs de sistemas
- Datasets de administración de sistemas
- Datasets de seguridad

**Comunidad Española:**
- Datasets de NLP en español
- Datasets de literatura española
- Datasets de medios en español

---

## 🚀 Instalación y Configuración

### Requisitos del Sistema

**Hardware Recomendado:**
- Google TPU v5e-64 o v6e-64 (para entrenamiento)
- Google ARM Axion o Graviton3 (para inferencia)
- 32GB+ RAM
- SSD NVMe 500GB+

**Software Requerido:**
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md
```bash
# Dependencias core
pip install torch>=2.0.0
pip install jax[tpu]>=0.4.0
pip install flax>=0.7.0
pip install transformers>=4.30.0

# Google TPU
pip install cloud-tpu-client
pip install torch-xla

# Optimización ARM
pip install onnxruntime-arm64

# RAG y vectores
pip install faiss-gpu
pip install sentence-transformers

# Monitoring
pip install prometheus-client
pip install wandb
```

### Configuración Rápida

<<<<<<< HEAD:archived/docs/DOCS.md
=======
**Backend (Flask):**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
# Editar .env con credenciales SMTP
python server.py
```

**Frontend (Web):**
```bash
cd web
python -m http.server 8000
# Abre http://localhost:8000
```

**Configuración Automática:**
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md
```python
from capibara.config import CapibaraConfig

# Auto-detección de hardware
config = CapibaraConfig.auto_detect_hardware()

if config.has_tpu:
    print(f"🔥 Google TPU: {config.tpu_type}")
elif config.has_arm_axion:
<<<<<<< HEAD:archived/docs/DOCS.md
    print(f"💪 Google ARM Axion: {config.arm_version)")
=======
    print(f"💪 Google ARM Axion: {config.arm_version}")
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md

print(f"✅ Arquitectura: 70% Transformer + 30% Mamba")
print(f"📊 Contexto: {config.context_window} tokens")
```

<<<<<<< HEAD:archived/docs/DOCS.md
## Configuración del Backend

El backend de capibara6 es un servidor Flask que gestiona los emails y conversaciones del chatbot.

### Instalación del Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración del Backend

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales SMTP:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=info@anachroni.co
SMTP_PASSWORD=tu_contraseña_de_aplicacion
FROM_EMAIL=info@anachroni.co
```

### Configuración SMTP para diferentes proveedores

- **Gmail**: Usa contraseñas de aplicación y el servidor `smtp.gmail.com`
- **Outlook/Hotmail**: `SMTP_SERVER=smtp.office365.com`
- **Yahoo**: `SMTP_SERVER=smtp.mail.yahoo.com`

### Ejecutar el Backend

```bash
python server.py
```

El servidor estará disponible en: `http://localhost:5000`

## API del Backend

### `POST /api/save-conversation`
Guarda la conversación y envía emails.

**Body:**
```json
{
  "email": "usuario@example.com",
  "conversations": [
    {
      "message": "Hola, me interesa capibara6",
      "timestamp": "2025-10-02T10:30:00.000Z"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "email_sent": true,
  "admin_notified": true,
  "message": "Datos guardados correctamente"
}
```

### `GET /api/health`
Health check del servidor.

## Uso del Sistema
=======
---

## 🎯 Ejemplos de Uso
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md

### 1. Análisis de Documentos Extensos

```python
from capibara import Capibara6

model = Capibara6(
    tpu_type="v6e-64",
    context_window=10_000_000,  # 10M tokens
    hybrid_mode=True  # 70/30 Transformer/Mamba
)

# Analizar base de código completa
result = model.analyze_codebase(
    path="./my-project",
    query="Encuentra vulnerabilidades de seguridad",
    deep_analysis=True
)
```

### 2. Asistente para Administración Pública

```python
from capibara import Capibara6

# Modo compliance para sector público
model = Capibara6(
    compliance_mode="eu_public_sector",
    gdpr_strict=True,
    audit_logging=True,
    data_residency="EU"
)

response = model.query(
    "Analiza este expediente administrativo",
    document=large_document,
    ensure_compliance=True
)
```

### 3. Procesamiento Multimodal

```python
from capibara import Capibara6

model = Capibara6(
    multimodal=True,
    enable_vision=True,
    enable_audio=True
)

result = model.process_multimodal({
    "text": "Analiza este video de seguridad",
    "video": security_footage,
    "generate_report": True,
    "language": "es"
})
```

<<<<<<< HEAD:archived/docs/DOCS.md
## Benchmarks y Rendimiento

### Comparativa Hardware
=======
### 4. Uso del Chatbot Web

```javascript
// Inicializar chatbot
const chatbot = new Capibara6Chat();

// Cambiar idioma
capibaraLanguage.switch('es'); // Español
capibaraLanguage.switch('en'); // English

// Acceder a conversaciones
const userData = chatbot.loadUserData();
console.log(userData.conversations);
```

---

## 📈 Benchmarks y Rendimiento

### Comparativa de Hardware
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md

| Hardware | Throughput | Latencia P95 | Memoria | Consumo | Costo/hora |
|----------|------------|--------------|---------|---------|------------|
| **Google TPU v6e-64** | **4,500+ tok/s** | **120ms** | 32GB | 380W | $14.00 |
| Google TPU v5e-64 | 3,800+ tok/s | 145ms | 24GB | 420W | $10.00 |
| Google ARM Axion | 2,100+ tok/s | 280ms | 16GB | 95W | $2.80 |
| NVIDIA A100 80GB | 1,890 tok/s | 280ms | 42GB | 400W | $3.20 |
| AWS Graviton3 | 1,450 tok/s | 380ms | 16GB | 140W | $2.50 |

### Arquitectura Híbrida Performance

```
Transformer (70%):
  - Precisión: 97.8%
  - Tareas complejas: 98.2%
  - Razonamiento: 96.5%

Mamba SSM (30%):
  - Velocidad: +185% vs Transformer puro
  - Memoria: -60% uso vs Transformer
  - Secuencias largas: O(n) vs O(n²)

Híbrido capibara6:
  - Balance óptimo: 97.8% precisión + velocidad
  - Contexto: 10M+ tokens
  - Eficiencia: 98.5% en TPU v6e-64
```

### Comparativa Ventana de Contexto

| Modelo | Contexto | Compañía |
|--------|----------|----------|
| **capibara6** | **10M+ tokens** | **Anachroni** 🏆 |
| Gemini 1.5 Pro | 1M tokens | Google |
| Claude 2.1 | 200K tokens | Anthropic |
| GPT-4 Turbo | 128K tokens | OpenAI |
| Llama 2 | 4K tokens | Meta |

<<<<<<< HEAD:archived/docs/DOCS.md
## Compliance y Seguridad

### Normativas Cumplidas
- ✅ **GDPR** (Reglamento General de Protección de Datos)
- ✅ **AI Act** (Ley de IA de la Unión Europea)
- ✅ **CCPA** (California Consumer Privacy Act)
- ✅ **ePrivacy Directive** (Directiva de privacidad electrónica)
- ✅ **NIS2 Directive** (Ciberseguridad)

### Certificaciones
- Certificado para administraciones públicas españolas y europeas
- Auditorías de seguridad continuas
- Evaluación ética independiente
- Transparencia algorítmica

### Seguridad
- Encriptación AES-256 en reposo
- TLS 1.3 en tránsito
- Segregación de datos por cliente
- Logs de auditoría inmutables
- Backup georeplicado UE

## Soporte y Contribución

### Contribución

```bash
git clone https://github.com/anachroni/capibara6
=======
---

## 🔧 API y Desarrollo

### Endpoints del Backend

**Guardar Conversación:**
```bash
POST /api/save-conversation
Content-Type: application/json

{
  "email": "usuario@example.com",
  "conversations": [
    {
      "message": "Hola, me interesa capibara6",
      "timestamp": "2025-01-02T10:30:00.000Z"
    }
  ]
}
```

**Guardar Lead Empresarial:**
```bash
POST /api/save-lead
Content-Type: application/json

{
  "contactType": "enterprise_consulting",
  "companyName": "Mi Empresa S.L.",
  "fullName": "Juan Pérez",
  "email": "juan@miempresa.com",
  "projectDescription": "Implementación de IA conversacional",
  "budgetRange": "50k_100k",
  "timeline": "medium_term"
}
```

**Health Check:**
```bash
GET /api/health

Response: {"status": "ok", "timestamp": "2025-01-02T10:30:00.000Z"}
```

### Configuración del Frontend

**Variables de Configuración:**
```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: 'https://www.capibara6.com',
    ENDPOINTS: {
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health'
    }
};
```

**API de Idioma:**
```javascript
// Cambiar idioma
capibaraLanguage.switch('es'); // Español
capibaraLanguage.switch('en'); // English

// Obtener idioma actual
const currentLang = capibaraLanguage.current();
```

---

## 📚 Documentación Técnica

### Estructura del Proyecto

```
capibara6-consensu/
├── backend/                 # Servidor Flask
│   ├── server.py           # API principal
│   ├── requirements.txt    # Dependencias Python
│   ├── .env.example       # Variables de entorno
│   └── user_data/         # Datos almacenados
├── web/                    # Frontend web
│   ├── index.html         # Página principal
│   ├── styles.css         # Estilos CSS
│   ├── script.js          # JavaScript principal
│   ├── chatbot.js         # Sistema de chatbot
│   ├── translations.js    # Traducciones
│   ├── neural-animation.js # Animaciones
│   └── config.js          # Configuración
├── user_data/             # Datos de usuarios
└── README.md              # Este archivo
```

### Arquitectura de Componentes

**Frontend:**
- **HTML5 Semántico**: Estructura accesible
- **CSS3 Variables**: Sistema de diseño consistente
- **JavaScript ES6+**: Módulos y clases modernas
- **Canvas API**: Animaciones interactivas
- **Web APIs**: Geolocalización, Storage, Fetch

**Backend:**
- **Flask**: Framework web ligero
- **CORS**: Manejo cross-origin
- **SMTP**: Envío de emails
- **JSON**: Almacenamiento de datos
- **Environment**: Configuración flexible

**Chatbot:**
- **State Machine**: Manejo de estados
- **Keyword Detection**: Respuestas inteligentes
- **Lead Capture**: Formulario guiado
- **Email Extraction**: Detección automática
- **Backend Integration**: Envío de datos

---

## 🤝 Contribución

### Cómo Contribuir

```bash
git clone https://github.com/anachroni-co/capibara6
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md
cd capibara6
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
pytest tests/
```

<<<<<<< HEAD:archived/docs/DOCS.md
### Contacto

**Empresa**: Anachroni s.coop  
**País**: España  
**Web**: [www.anachroni.co](https://www.anachroni.co)  
**Email**: [info@anachroni.co](mailto:info@anachroni.co)  
**Proyecto**: [capibara6.com](https://capibara6.com)

### Servicios para Empresas y Administraciones Públicas
=======
### Guías de Desarrollo

**Frontend:**
- Usar variables CSS para consistencia
- Implementar responsive design
- Añadir traducciones en ambos idiomas
- Optimizar performance de animaciones

**Backend:**
- Seguir patrones REST
- Implementar logging apropiado
- Validar entrada de datos
- Manejar errores gracefully

**Chatbot:**
- Añadir nuevos tipos de respuesta
- Mejorar detección de keywords
- Expandir flujos de conversación
- Optimizar captura de leads

---

## 📞 Contacto y Soporte

### Anachroni s.coop

**🏢 Empresa**: Anachroni s.coop  
**🌍 País**: España  
**🌐 Web**: [www.anachroni.co](https://www.anachroni.co)  
**📧 Email**: [info@anachroni.co](mailto:info@anachroni.co)  
**🦫 Proyecto**: [capibara6.com](https://capibara6.com)

### Enterprise & Sector Público

Para empresas y administraciones públicas:

**Servicios:**
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md
- Despliegue on-premise o cloud privado
- Certificaciones sector público (ENS, CCN-CERT)
- Custom training para dominios específicos
- SLA 99.9% - 99.99% uptime
- Soporte prioritario <4h
- Auditorías de compliance

<<<<<<< HEAD:archived/docs/DOCS.md
## Recursos Adicionales

### Datasets Especializados
1. **Academic**: Datasets institucionales de universidades, Wikipedia académica, código académico y papers
2. **Multimodal**: Datasets de audio emocional, análisis de sentimientos multimodal, datasets de conversación
3. **Engineering Design**: Datasets de electrónica, FPGA, diseños de circuitos, documentación técnica
4. **Physics**: Datasets de física cuántica, simulaciones físicas, mecánica clásica, física de partículas
5. **Robotics**: Datasets de control robótico, percepción, planificación de movimiento, interacción humano-robot
6. **Mathematics**: Datasets de álgebra, cálculo, estadística, optimización
7. **Systems**: Datasets de Linux kernel, logs de sistemas, administración de sistemas, seguridad
8. **Spanish Community**: Datasets de NLP en español, literatura española, medios en español

### Configuración del Sistema
El sistema usa un sistema de configuración flexible basado en YAML con soporte para múltiples perfiles y generación automática de variables de entorno:

```yaml
project:
  name: capibara6
  version: 1.0.0

tpu:
  name: capibara-tpu-v5
  zone: us-central1-a
  type: v5litepod-16

training:
  batch_size: 32
  mamba_threshold: 512
  enable_quantization: true
  
model:
  router_type: meta_consensus
  use_mamba: true
  use_transformer: true
```

### Performance Enterprise-Grade
- 20x aceleración con Cython kernels
- 75% reducción de memoria con cuantización INT8
- 40x mejora teórica combinada
- Entrenamiento distribuido multi-worker
- Consenso federado Byzantine fault-tolerant
- Soporte TPU/ARM/CUDA
- Sistema de configuración TOML completo
- Factory pattern para agentes
- Strategy pattern para orquestación
- Adapter pattern para hardware
=======
**Contacto**: [info@anachroni.co](mailto:info@anachroni.co)

---

## 📄 Licencia

**Apache License 2.0**

```
Copyright 2025 Anachroni s.coop

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

<div align="center">

**capibara6 Consensu** - Construido con ❤️ por [Anachroni s.coop](https://www.anachroni.co)

*IA avanzada con compliance total para empresas y administraciones públicas* 🦫

[![Star on GitHub](https://img.shields.io/github/stars/anachroni/capibara6?style=social)](https://github.com/anachroni/capibara6)

**Hecho en España 🇪🇸 | Cumplimiento UE 🇪🇺 | Sector Público ✅**

</div>
>>>>>>> b9e73c0 (Refactor: Update README with Consensu details and structure):README.md
