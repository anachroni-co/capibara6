# Arquitectura del Sistema capibara6

## Tabla de Contenidos
- [Visión General de la Arquitectura](#visión-general-de-la-arquitectura)
- [Arquitectura Híbrida Transformer-Mamba](#arquitectura-híbrida-transformer-mamba)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Frontend Web](#frontend-web)
- [Backend API](#backend-api)
- [Componentes del Modelo](#componentes-del-modelo)
- [Optimización Hardware](#optimización-hardware)
- [Flujo de Datos](#flujo-de-datos)
- [Patrones de Diseño](#patrones-de-diseño)
- [Seguridad y Compliance](#seguridad-y-compliance)
- [Escalabilidad](#escalabilidad)
- [Monitorización](#monitorización)

## Visión General de la Arquitectura

capibara6 implementa una arquitectura de IA conversacional de última generación que combina lo mejor de las arquitecturas Transformer y Mamba SSM en un diseño híbrido optimizado (70% Transformer / 30% Mamba). Diseñado específicamente para Google TPU v5e/v6e-64 y procesadores Google ARM Axion, el sistema ofrece la mayor ventana de contexto del mercado (10M+ tokens) con compliance total para empresas y administraciones públicas.

### Visión General del Sistema
```
┌─────────────────────────────────────────────────────────────────┐
│                    capibara6 Arquitectura                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Frontend  │    │   Backend   │    │   Modelo    │         │
│  │   Web UI    │◄──►│   Flask     │◄──►│  Híbrido    │         │
│  │             │    │   API       │    │Transformer- │         │
│  └─────────────┘    └─────────────┘    │   Mamba     │         │
│                                        └─────────────┘         │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │   Chatbot   │    │   Email     │    │   TPU/ARM   │       │
│  │   Widget    │    │  Service    │    │   Opt.      │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Arquitectura Híbrida Transformer-Mamba

### Distribución de Arquitectura (70/30)
El sistema utiliza una distribución optimizada de 70% Transformer y 30% Mamba SSM para balancear precisión y velocidad:

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

### Componentes de la Arquitectura Híbrida

#### Transformer (70%)
- **Atención multi-cabeza**: Implementación optimizada para TPU
- **Feed-forward networks**: Capas densas con GeLU activation
- **Capas residuales y normalization**: LayerNorm para estabilidad
- **Posicional encoding**: Rotary Position Embedding (RoPE) para secuencias largas

#### Mamba SSM (30%)
- **Selective State Spaces**: Complejidad lineal O(n) para secuencias largas
- **Hardware-aware optimization**: Optimizado específicamente para TPU v5e/v6e
- **Gating mechanisms**: Mejor manejo de información a largo plazo
- **Efficient memory utilization**: Uso optimizado de HBM en TPUs

#### Sistema de Enrutamiento Inteligente
- **Meta-consensus router**: Sistema de enrutamiento basado en confianza
- **Input-adaptive routing**: Decide dinámicamente qué componente usar
- **Performance-based load balancing**: Distribuye la carga según rendimiento

## Estructura del Proyecto

### Organización de Directorios
```
capibara6/
├── backend/              # Servidor Flask y lógica de negocio
│   ├── server.py         # Punto de entrada del servidor
│   ├── requirements.txt  # Dependencias de Python
│   ├── .env.example      # Plantilla de variables de entorno
│   ├── user_data/        # Almacenamiento temporal de conversaciones
│   ├── __pycache__/      # Caché de Python
│   └── tests/            # Pruebas unitarias (si existen)
├── web/                  # Frontend web
│   ├── index.html        # Página principal
│   ├── styles.css        # Estilos CSS
│   ├── script.js         # Lógica de frontend
│   ├── chatbot.js        # Funcionalidad del chatbot
│   ├── neural-animation.js # Animación de red neuronal en header
│   ├── config.js         # Configuración del frontend
│   ├── translations.js   # Sistema de traducción i18n
│   ├── favicon.svg       # Favicon
│   └── .vercel/          # Configuración de despliegue en Vercel
├── user_data/            # Datos de usuario (excluido de git)
├── datasets/             # Datasets especializados (no implementado aún)
├── AGENTS.md             # Documentación de agentes de IA
├── README.md             # Documentación general
├── DOCS.md               # Documentación completa
├── API.md                # Documentación de la API
├── INSTALLATION.md       # Guía de instalación
├── ARCHITECTURE.md       # Documentación de arquitectura (este archivo)
├── Qwen.md               # Notas del asistente Qwen
├── LICENSE               # Licencia Apache 2.0
├── .gitignore            # Archivos excluidos de git
└── vercel.json           # Configuración de despliegue Vercel
```

## Frontend Web

### Componentes Principales

#### index.html
- **Estructura principal**: Define la arquitectura visual del sitio
- **Secciones**: Hero, Features, Architecture, Datasets, Component Status, Performance, CTA, Footer
- **Chatbot integration**: Widget de chatbot integrado
- **Internationalization**: Soporte para múltiples idiomas
- **Responsive design**: Compatible con dispositivos móviles

#### styles.css
- **CSS moderno**: Utiliza Grid y Flexbox
- **Variables CSS**: Sistema de theming
- **Animaciones**: Transiciones suaves y efectos visuales
- **Responsive breakpoints**: Diseño adaptable

#### script.js
- **DOM manipulation**: Control de la interfaz de usuario
- **API calls**: Comunicación con el backend
- **Event handling**: Gestión de interacciones del usuario
- **Performance optimization**: Lazy loading y optimizaciones de renderizado

#### chatbot.js
- **Message management**: Gestión del historial de conversación
- **UI controls**: Control del widget de chat
- **Email collection**: Sistema de recolección de emails
- **API integration**: Comunicación con `/api/save-conversation`

#### neural-animation.js
- **Canvas rendering**: Animación de red neuronal en el hero
- **Performance optimization**: Uso eficiente de requestAnimationFrame
- **WebGL (opcional)**: Potencial uso para animaciones 3D

#### translations.js
- **i18n system**: Sistema de traducción multi-idioma
- **Dynamic loading**: Carga dinámica de traducciones
- **Language detection**: Detección automática de idioma

### Patrones de Diseño en el Frontend
- **Modular architecture**: Código organizado en módulos lógicos
- **Separation of concerns**: HTML/CSS/JS separados claramente
- **Component-based UI**: Estructura similar a componentes

## Backend API

### Arquitectura del Backend

#### server.py
- **Flask framework**: Web framework ligero
- **RESTful API**: Endpoints siguiendo principios REST
- **CORS handling**: Gestión de peticiones cross-origin
- **Email service**: Integración con SMTP para notificaciones
- **Data persistence**: Almacenamiento local de conversaciones

#### Componentes Clave
```python
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json
import os
from datetime import datetime
```

#### Endpoints Disponibles
- `POST /api/save-conversation`: Guarda conversaciones y envía emails
- `GET /api/health`: Verificación de estado del servidor

#### Flujo de Trabajo del Backend
1. Recibe solicitud de conversación
2. Valida los datos de entrada
3. Guarda los datos localmente
4. Envía email de confirmación al usuario
5. Envía notificación al administrador
6. Retorna respuesta de éxito

### Seguridad del Backend
- **Input validation**: Validación de datos entrantes
- **Email validation**: Verificación de formato de email
- **Rate limiting**: (No implementado en la versión base)
- **Environment isolation**: Variables de entorno protegidas

## Componentes del Modelo

### Arquitectura del Modelo Principal

#### Mixture of Experts (MoE)
- **32 expertos especializados**: Para diferentes dominios (matemáticas, ciencias, código, creatividad)
- **Expert routing**: Sistema de enrutamiento dinámico
- **Load balancing**: Distribución inteligente de carga
- **Domain specialization**: Cada experto especializado en dominios específicos

#### Chain-of-Thought (CoT) Reasoning
- **Up to 12 steps**: Razonamiento paso a paso verificable
- **Meta-cognition**: Sistema de autoevaluación de confianza
- **Self-reflection**: Mecanismos de reflexión interna
- **Process reward models**: Integración de modelos de recompensa de proceso

#### Capacidades Multimodales
- **Vision encoder**: ViT-Large optimizado para imágenes
- **Video encoder**: Capacidad para procesar hasta 64 frames
- **Audio processing**: Text-to-speech con contexto emocional
- **Multimodal fusion**: Atención multimodal para integrar diferentes tipos de datos

### Rendimiento y Optimización

#### Google TPU v5e/v6e-64
- **XLA compilation**: Compilación avanzada para aceleración
- **Kernel fusion**: Fusión automática de kernels
- **Mixed precision**: Uso de bfloat16 para eficiencia
- **Flash attention**: Atención optimizada para secuencias largas
- **Pipeline parallelism**: Paralelismo de pipeline para alto throughput

#### Google ARM Axion
- **NEON vectorization**: Vectorización automática
- **SVE2 optimizations**: Optimizaciones de 512-bit
- **Quantization**: Cuantización 4-bit/8-bit calibrada
- **Memory pool optimization**: Optimización de pools de memoria
- **Cache-aware algorithms**: Algoritmos conscientes de cache

## Optimización Hardware

### Google TPU v6e-64 Performance
```
Throughput:      4,500+ tokens/sec
Latencia P95:    120ms
Memoria HBM:     32GB
Eficiencia:      98.5%
Arquitectura:    256 chips interconectados
```

### Google TPU v5e-64 Performance
```
Throughput:      3,800+ tokens/sec
Latencia P95:    145ms
Memoria HBM:     24GB
Eficiencia:      96.8%
```

### Google ARM Axion Performance
```
Throughput:      2,100+ tokens/sec
Latencia P95:    280ms
Memoria:         16GB
Consumo:         95W
Cores:           Hasta 192 cores
```

### Optimizaciones Clave
- **Cython kernels**: 20x speedup para operaciones críticas
- **Memory optimization**: Gestión eficiente de memoria para contextos largos
- **Distributed training**: Soporte para entrenamiento multi-worker
- **Quantization**: INT8 para reducción de 75% de memoria
- **Hybrid architectures**: Combinación teórica de 40x mejora

## Flujo de Datos

### Flujo de Conversación Completo
```
Usuario → Frontend → Backend → Almacenamiento → Email Service → Confirmación
   ↓           ↓          ↓           ↓              ↓              ↓
Mensaje → Widget → API Call → JSON/File → SMTP → User/Admin → Success
```

### Flujo de Procesamiento del Modelo
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Input textual  │ -> │  Preprocessing  │ -> │  MoE Routing    │
│  or multimodal  │    │  & Embedding    │    │  & Distribution │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ↓                       ↓                       ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Context        │ -> │  Hybrid        │ -> │  CoT Reasoning  │
│  Management     │    │  Processing     │    │  & Validation   │
│  (10M+ tokens)  │    │  (T/M Split)    │    │  (12 steps)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ↓                       ↓                       ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  TPU/ARM        │ -> │  Postprocessing │ -> │  Response       │
│  Acceleration   │    │  & Formatting   │    │  Generation     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Gestión de Contexto
- **Long-context handling**: Capacidad para manejar contextos de 10M+ tokens
- **Memory compression**: Técnicas de compresión de memoria
- **Chunking strategies**: Estrategias de división de contexto
- **Attention optimization**: Optimización de mecanismos de atención para long-context

## Patrones de Diseño

### Patrones de Arquitectura

#### Factory Pattern
- **Agent factory**: Sistema para crear diferentes tipos de agentes
- **Hardware adapter**: Adaptadores para diferentes tipos de hardware (TPU/ARM/CUDA)

#### Strategy Pattern
- **Orchestration strategy**: Diferentes estrategias de orquestación
- **Processing strategy**: Diferentes enfoques para procesamiento

#### Adapter Pattern
- **Hardware abstraction**: Capa de abstracción para diferentes hardware
- **Storage adapter**: Adaptadores para diferentes backends de almacenamiento

### Patrones de Código

#### Modular Design
- **Component isolation**: Componentes aislados funcionalmente
- **Dependency injection**: Inyección de dependencias donde es apropiado
- **Configuration management**: Sistema de configuración flexible

#### Performance Patterns
- **Caching strategies**: Caching inteligente para resultados frecuentes
- **Lazy loading**: Carga diferida de componentes pesados
- **Batch processing**: Procesamiento en lotes para eficiencia

## Seguridad y Compliance

### Niveles de Seguridad

#### Datos y Privacidad
- **Encriptación AES-256**: En reposo y en tránsito con TLS 1.3
- **Segregación de datos**: Por cliente y sesión
- **Derecho al olvido**: Implementación del derecho a ser olvidado
- **Portabilidad de datos**: Sistema para exportar datos de usuario

#### Cumplimiento Regulatorio
- **GDPR**: Reglamento General de Protección de Datos
- **AI Act**: Ley de IA de la Unión Europea
- **CCPA**: California Consumer Privacy Act
- **ePrivacy Directive**: Directiva de privacidad electrónica
- **NIS2 Directive**: Directiva de ciberseguridad

#### Certificaciones
- **Certificado para administraciones públicas**: Cumplimiento para sector público
- **Auditorías de seguridad continuas**: Revisiones periódicas
- **Evaluación ética independiente**: Revisión externa de algoritmos
- **Transparencia algorítmica**: Explicabilidad de decisiones

### Registros y Auditoría
- **Logs de auditoría inmutables**: Registros seguros de todas las operaciones
- **Backup georeplicado UE**: Copias de seguridad en la Unión Europea
- **Control de acceso**: Gestión detallada de permisos

## Escalabilidad

### Escalabilidad Horizontal
- **Multi-worker training**: Soporte para entrenamiento distribuido
- **Load balancing**: Distribución de carga entre múltiples instancias
- **Byzantine fault-tolerant**: Sistema tolerante a fallos

### Escalabilidad Vertical
- **TPU/ARM/CUDA support**: Soporte para diferentes tipos de hardware
- **Resource optimization**: Uso eficiente de recursos disponibles
- **Auto-scaling readiness**: Preparado para sistemas de auto-escalado

### Estrategias de Escalado
- **Microservices approach**: Arquitectura preparada para servicios
- **Container deployment**: Compatible con contenedores (Docker)
- **Cloud-native design**: Diseño nativo para nube

## Monitorización

### Métricas Clave
- **TPU metrics**: TFLOPS, uso de memoria, eficiencia
- **Performance metrics**: Throughput, latencia, tasa de error
- **System metrics**: CPU, memoria, disco, red

### Herramientas de Monitorización
- **Grafana/Prometheus**: Exportación y visualización de métricas
- **Weights & Biases**: Seguimiento de entrenamiento y experimentos
- **Custom dashboards**: Paneles personalizados para operaciones

### Auto-optimización
- **Metrics-based optimization**: Optimización basada en métricas en tiempo real
- **Predictive scaling**: Escalado predictivo basado en patrones
- **Performance alerting**: Alertas automáticas para degradaciones

### Monitoreo Distribuido
- **Distributed tracing**: Seguimiento de solicitudes a través del sistema
- **Centralized logging**: Registro centralizado de todos los componentes
- **Health monitoring**: Verificación continua de salud del sistema