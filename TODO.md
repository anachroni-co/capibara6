# ✅ TODO - Capibara6 Digital Twin Implementation

> **Proyecto:** Sistema de Gemelo Digital con Visualización de Modelos y E2B
> **Inicio:** 2025-11-09
> **Última actualización:** 2025-11-09
> **Estado global:** 🔄 En progreso (2/40 completadas - 5%)

---

## 📊 Progreso General

```
[███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 10% Completado

✅ Completadas: 4/40
🔄 En progreso: 0/40
⏳ Pendientes: 36/40
```

---

## 🎯 FASE 1: Preparación y Resolución de Conflictos

**Objetivo:** Resolver conflictos de merge y preparar base del proyecto
**Estado:** ✅ Completado (4/4 completadas)

### Tareas:

- [x] **1.1** Analizar estado actual del proyecto
  - **Estado:** ✅ Completado
  - **Fecha:** 2025-11-09
  - **Resultado:** PROJECT_STATUS.md creado

- [x] **1.2** Crear documentación de TODOs
  - **Estado:** ✅ Completado
  - **Fecha:** 2025-11-09
  - **Archivo:** TODO.md (este archivo)

- [x] **1.3** Resolver conflicto en `web/chat.html`
  - **Estado:** ✅ Completado
  - **Fecha:** 2025-11-09
  - **Decisión:** Usar versión 2 (diseño con gradientes vibrantes)
  - **Resultado:** Archivo reducido de 611 a 227 líneas, sin marcadores de conflicto
  - **Archivos afectados:**
    - `web/chat.html` ✅
    - `web/chat-styles.css` (usado)
  - **Commit:** 3399ff9

- [x] **1.4** Limpiar código de plantillas del chat
  - **Estado:** ✅ Completado (implícito)
  - **Fecha:** 2025-11-09
  - **Nota:** La versión 2 de chat.html NO incluye sistema de plantillas
  - **Resultado:** Sistema de plantillas eliminado al elegir versión 2

---

## 🎨 FASE 2: Visualización de Modelos

**Objetivo:** Implementar panel de visualización de modelos activos y respuestas
**Estado:** ⏳ Pendiente (0/8 completadas)

### Tareas:

- [ ] **2.1** Diseñar componente de modelo activo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Crear badge/chip que muestre modelo usado (phi3, mistral, gpt-oss-20b)
  - **Ubicación:** Chat header
  - **Tiempo estimado:** 20 min

- [ ] **2.2** Implementar indicador de modelo por mensaje
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Badge pequeño en cada mensaje mostrando qué modelo lo generó
  - **Tiempo estimado:** 15 min

- [ ] **2.3** Crear panel de métricas de modelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Panel lateral con métricas en tiempo real
  - **Métricas:**
    - Velocidad de respuesta (tokens/s)
    - Tokens generados
    - Tiempo de respuesta
    - Tier usado (fast/balanced/complex)
  - **Tiempo estimado:** 30 min

- [ ] **2.4** Implementar selector manual de modelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Dropdown para seleccionar modelo manualmente
  - **Tiempo estimado:** 20 min

- [ ] **2.5** Añadir visualización de clasificación de tarea
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Mostrar por qué se eligió determinado tier
  - **Tiempo estimado:** 25 min

- [ ] **2.6** Implementar indicador de consenso multi-modelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Si se usan múltiples modelos, mostrar consenso
  - **Tiempo estimado:** 30 min

- [ ] **2.7** Crear gráfico de uso de modelos
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Gráfico de barras/donut con % de uso de cada modelo
  - **Tiempo estimado:** 35 min

- [ ] **2.8** Integrar sistema de métricas con backend
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Conectar frontend con endpoints de métricas
  - **Endpoint nuevo:** `/api/metrics/models`
  - **Tiempo estimado:** 20 min

**Tiempo total estimado Fase 2:** ~3 horas

---

## 🖥️ FASE 3: Panel de E2B Sandboxes

**Objetivo:** Integrar visualización de sandboxes E2B para ejecución de código
**Estado:** ⏳ Pendiente (0/10 completadas)

### Tareas:

- [ ] **3.1** Reactivar módulo E2B desde archived
  - **Estado:** ⏳ Pendiente
  - **Acción:** Copiar módulos de `archived/backend_modules/execution/` a `backend/`
  - **Archivos:**
    - `e2b_integration.py`
    - `e2b_manager.py`
    - `execution_loop.py`
    - `code_detector.py`
    - `feedback_loop.py`
    - `error_mapping.py`
  - **Tiempo estimado:** 15 min

- [ ] **3.2** Crear endpoints API para E2B
  - **Estado:** ⏳ Pendiente
  - **Endpoints a crear:**
    - `POST /api/e2b/execute` - Ejecutar código
    - `GET /api/e2b/status` - Estado de sandboxes
    - `GET /api/e2b/logs` - Logs de ejecución
    - `GET /api/e2b/sandboxes` - Lista de sandboxes activos
  - **Tiempo estimado:** 45 min

- [ ] **3.3** Diseñar componente de terminal integrado
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Terminal estilo VSCode para mostrar output
  - **Librería:** Usar xterm.js o similar
  - **Tiempo estimado:** 40 min

- [ ] **3.4** Implementar panel de estado de sandbox
  - **Estado:** ⏳ Pendiente
  - **Información a mostrar:**
    - Estado: activo/inactivo
    - Lenguaje de programación
    - Uso de CPU (%)
    - Uso de memoria (MB)
    - Tiempo de ejecución
  - **Tiempo estimado:** 30 min

- [ ] **3.5** Crear visualización de logs de ejecución
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Historial de códigos ejecutados con resultados
  - **Tiempo estimado:** 25 min

- [ ] **3.6** Implementar editor de código embebido
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Editor Monaco (VSCode) para probar código
  - **Lenguajes:** Python, JavaScript, SQL, Bash
  - **Tiempo estimado:** 50 min

- [ ] **3.7** Añadir botón "Ejecutar código" en mensajes
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Detectar bloques de código y añadir botón de ejecución
  - **Tiempo estimado:** 20 min

- [ ] **3.8** Implementar sistema de corrección automática
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Mostrar sugerencias cuando el código falla
  - **Tiempo estimado:** 35 min

- [ ] **3.9** Crear panel de recursos del sandbox
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Gráficos en tiempo real de CPU, memoria, tiempo
  - **Tiempo estimado:** 40 min

- [ ] **3.10** Integrar detección automática de código
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Usar code_detector.py para detectar código en respuestas
  - **Tiempo estimado:** 25 min

**Tiempo total estimado Fase 3:** ~5.5 horas

---

## 👤 FASE 4: Importador de Redes Sociales

**Objetivo:** Crear sistema para importar perfiles de redes sociales
**Estado:** ⏳ Pendiente (0/9 completadas)

### Tareas:

- [ ] **4.1** Diseñar UI del importador
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Modal/página para importar perfiles
  - **Redes a soportar:** Twitter/X, LinkedIn, Instagram, GitHub
  - **Tiempo estimado:** 30 min

- [ ] **4.2** Implementar importador de Twitter/X
  - **Estado:** ⏳ Pendiente
  - **Método:** API oficial o scraper
  - **Datos a extraer:**
    - Tweets (texto, fecha, likes, RTs)
    - Respuestas
    - Bio
    - Interacciones
  - **Tiempo estimado:** 90 min

- [ ] **4.3** Implementar importador de LinkedIn
  - **Estado:** ⏳ Pendiente
  - **Método:** LinkedIn API
  - **Datos a extraer:**
    - Posts
    - Artículos
    - Comentarios
    - Perfil profesional
  - **Tiempo estimado:** 90 min

- [ ] **4.4** Implementar importador de Instagram
  - **Estado:** ⏳ Pendiente
  - **Método:** Instagram Graph API o scraper
  - **Datos a extraer:**
    - Captions de posts
    - Comentarios
    - Bio
  - **Tiempo estimado:** 90 min

- [ ] **4.5** Implementar importador de GitHub
  - **Estado:** ⏳ Pendiente
  - **Método:** GitHub API v3/v4
  - **Datos a extraer:**
    - Repositorios
    - Commits messages
    - Issues
    - Pull requests
    - README files
  - **Tiempo estimado:** 60 min

- [ ] **4.6** Crear backend para procesamiento de datos
  - **Estado:** ⏳ Pendiente
  - **Endpoints:**
    - `POST /api/digital-twin/import/twitter`
    - `POST /api/digital-twin/import/linkedin`
    - `POST /api/digital-twin/import/instagram`
    - `POST /api/digital-twin/import/github`
  - **Tiempo estimado:** 45 min

- [ ] **4.7** Implementar sistema de almacenamiento
  - **Estado:** ⏳ Pendiente
  - **Base de datos:** PostgreSQL
  - **Tablas a crear:**
    - `digital_twins` - Perfiles de usuarios
    - `social_data` - Datos importados
    - `training_data` - Datos procesados para fine-tuning
  - **Tiempo estimado:** 40 min

- [ ] **4.8** Crear validación y limpieza de datos
  - **Estado:** ⏳ Pendiente
  - **Acciones:**
    - Eliminar duplicados
    - Filtrar spam
    - Normalizar texto
    - Detectar idioma
  - **Tiempo estimado:** 50 min

- [ ] **4.9** Implementar progreso de importación
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Barra de progreso en tiempo real
  - **Tecnología:** WebSockets o SSE
  - **Tiempo estimado:** 30 min

**Tiempo total estimado Fase 4:** ~8.5 horas

---

## 🧠 FASE 5: Sistema de Gemelo Digital

**Objetivo:** Crear sistema de análisis NLP y generación de gemelo digital
**Estado:** ⏳ Pendiente (0/12 completadas)

### Tareas:

- [ ] **5.1** Implementar analizador de patrones de escritura
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Extraer estilo de escritura del usuario
  - **Métricas:**
    - Longitud promedio de frases
    - Vocabulario característico
    - Uso de puntuación
    - Complejidad léxica
  - **Tiempo estimado:** 60 min

- [ ] **5.2** Implementar análisis de temas frecuentes
  - **Estado:** ⏳ Pendiente
  - **Técnicas:** LDA, TF-IDF, clustering
  - **Tiempo estimado:** 50 min

- [ ] **5.3** Implementar análisis de sentimientos
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Detectar tono general (positivo, negativo, neutro)
  - **Librería:** VADER o transformers
  - **Tiempo estimado:** 40 min

- [ ] **5.4** Implementar detección de personalidad
  - **Estado:** ⏳ Pendiente
  - **Modelo:** Big Five (OCEAN)
  - **Rasgos:**
    - Openness (Apertura)
    - Conscientiousness (Responsabilidad)
    - Extraversion (Extroversión)
    - Agreeableness (Amabilidad)
    - Neuroticism (Neuroticismo)
  - **Tiempo estimado:** 70 min

- [ ] **5.5** Crear sistema de extracción de vocabulario único
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Palabras y frases características del usuario
  - **Tiempo estimado:** 35 min

- [ ] **5.6** Implementar generador de perfil de gemelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Compilar todos los análisis en un perfil único
  - **Formato:** JSON estructurado
  - **Tiempo estimado:** 40 min

- [ ] **5.7** Crear sistema de fine-tuning personalizado
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Adaptar modelo base con datos del usuario
  - **Técnica:** LoRA o full fine-tuning
  - **Modelo base:** mistral o gemma
  - **Tiempo estimado:** 120 min

- [ ] **5.8** Implementar sistema de almacenamiento de gemelos
  - **Estado:** ⏳ Pendiente
  - **Almacenamiento:**
    - Perfil en PostgreSQL
    - Modelo fine-tuned en disco
    - Embeddings en vector DB
  - **Tiempo estimado:** 45 min

- [ ] **5.9** Crear endpoints API para gemelo digital
  - **Estado:** ⏳ Pendiente
  - **Endpoints:**
    - `POST /api/digital-twin/create` - Crear gemelo
    - `GET /api/digital-twin/:id` - Obtener gemelo
    - `POST /api/digital-twin/:id/chat` - Chatear con gemelo
    - `GET /api/digital-twin/:id/personality` - Obtener análisis de personalidad
    - `DELETE /api/digital-twin/:id` - Eliminar gemelo
  - **Tiempo estimado:** 50 min

- [ ] **5.10** Implementar modo "hablar como yo"
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Generar respuestas con el estilo del usuario
  - **Tiempo estimado:** 60 min

- [ ] **5.11** Crear sistema de validación de similitud
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Medir qué tan parecidas son las respuestas del gemelo vs usuario real
  - **Métricas:**
    - Similitud coseno de embeddings
    - BLEU score
    - Coherencia de estilo
  - **Tiempo estimado:** 50 min

- [ ] **5.12** Implementar actualización incremental del gemelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Mejorar gemelo con nuevas interacciones
  - **Tiempo estimado:** 40 min

**Tiempo total estimado Fase 5:** ~10.5 horas

---

## 📊 FASE 6: Panel Avanzado con Métricas

**Objetivo:** Crear interfaz visual para gestión y análisis del gemelo digital
**Estado:** ⏳ Pendiente (0/11 completadas)

### Tareas:

- [ ] **6.1** Diseñar dashboard principal
  - **Estado:** ⏳ Pendiente
  - **Secciones:**
    - Resumen del gemelo
    - Métricas de personalidad
    - Gráficos de análisis
    - Historial de uso
  - **Tiempo estimado:** 45 min

- [ ] **6.2** Crear tarjeta de perfil de gemelo
  - **Estado:** ⏳ Pendiente
  - **Información:**
    - Avatar/foto
    - Nombre
    - Fecha de creación
    - Redes sociales importadas
    - Cantidad de datos procesados
  - **Tiempo estimado:** 30 min

- [ ] **6.3** Implementar gráfico de personalidad (Big Five)
  - **Estado:** ⏳ Pendiente
  - **Tipo:** Radar chart
  - **Tiempo estimado:** 35 min

- [ ] **6.4** Crear visualización de temas frecuentes
  - **Estado:** ⏳ Pendiente
  - **Tipo:** Word cloud + lista categorizada
  - **Tiempo estimado:** 40 min

- [ ] **6.5** Implementar gráfico de análisis de sentimientos
  - **Estado:** ⏳ Pendiente
  - **Tipo:** Pie chart o donut
  - **Categorías:** Positivo, Neutro, Negativo
  - **Tiempo estimado:** 25 min

- [ ] **6.6** Crear panel de vocabulario característico
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Top 50 palabras/frases únicas del usuario
  - **Tiempo estimado:** 20 min

- [ ] **6.7** Implementar métricas de similitud en tiempo real
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Mostrar score de similitud con cada respuesta
  - **Visualización:** Progress bar o gauge
  - **Tiempo estimado:** 30 min

- [ ] **6.8** Crear comparador de respuestas
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Vista lado a lado: respuesta original vs gemelo
  - **Tiempo estimado:** 40 min

- [ ] **6.9** Implementar panel de configuración avanzada
  - **Estado:** ⏳ Pendiente
  - **Opciones:**
    - Ajustar temperatura del gemelo
    - Activar/desactivar rasgos de personalidad
    - Re-entrenar con nuevos datos
  - **Tiempo estimado:** 35 min

- [ ] **6.10** Crear sistema de exportación de perfil
  - **Estado:** ⏳ Pendiente
  - **Formatos:** JSON, PDF (informe)
  - **Tiempo estimado:** 30 min

- [ ] **6.11** Implementar historial de evolución del gemelo
  - **Estado:** ⏳ Pendiente
  - **Descripción:** Timeline mostrando cambios en personalidad a lo largo del tiempo
  - **Tiempo estimado:** 45 min

**Tiempo total estimado Fase 6:** ~6 horas

---

## 🧪 FASE 7: Testing y Optimización

**Objetivo:** Probar y optimizar todo el sistema
**Estado:** ⏳ Pendiente (0/8 completadas)

### Tareas:

- [ ] **7.1** Crear tests unitarios para importadores
  - **Estado:** ⏳ Pendiente
  - **Framework:** pytest
  - **Tiempo estimado:** 60 min

- [ ] **7.2** Crear tests para analizadores NLP
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 50 min

- [ ] **7.3** Crear tests para sistema de fine-tuning
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 60 min

- [ ] **7.4** Pruebas de carga de E2B sandboxes
  - **Estado:** ⏳ Pendiente
  - **Herramienta:** Locust o Artillery
  - **Tiempo estimado:** 40 min

- [ ] **7.5** Optimización de queries a base de datos
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 30 min

- [ ] **7.6** Implementar caché para gemelos digitales
  - **Estado:** ⏳ Pendiente
  - **Tecnología:** Redis
  - **Tiempo estimado:** 35 min

- [ ] **7.7** Optimizar carga de visualizaciones
  - **Estado:** ⏳ Pendiente
  - **Técnicas:** Lazy loading, code splitting
  - **Tiempo estimado:** 40 min

- [ ] **7.8** Pruebas de usuario (UAT)
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 90 min

**Tiempo total estimado Fase 7:** ~6.5 horas

---

## 📚 FASE 8: Documentación

**Objetivo:** Documentar todo el sistema nuevo
**Estado:** ⏳ Pendiente (0/6 completadas)

### Tareas:

- [ ] **8.1** Documentar API de gemelo digital
  - **Estado:** ⏳ Pendiente
  - **Formato:** OpenAPI/Swagger
  - **Tiempo estimado:** 60 min

- [ ] **8.2** Crear guía de usuario del gemelo digital
  - **Estado:** ⏳ Pendiente
  - **Formato:** Markdown con screenshots
  - **Tiempo estimado:** 90 min

- [ ] **8.3** Documentar sistema de importadores
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 40 min

- [ ] **8.4** Crear tutorial de E2B sandboxes
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 45 min

- [ ] **8.5** Actualizar README principal
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 30 min

- [ ] **8.6** Crear video demo (opcional)
  - **Estado:** ⏳ Pendiente
  - **Tiempo estimado:** 120 min (opcional)

**Tiempo total estimado Fase 8:** ~6 horas

---

## 📅 Cronograma Estimado

| Fase | Tareas | Tiempo Estimado | Estado |
|------|--------|-----------------|--------|
| **Fase 1** | Preparación | 25 min | 🔄 En progreso (50%) |
| **Fase 2** | Visualización Modelos | ~3 horas | ⏳ Pendiente |
| **Fase 3** | Panel E2B | ~5.5 horas | ⏳ Pendiente |
| **Fase 4** | Importador Redes Sociales | ~8.5 horas | ⏳ Pendiente |
| **Fase 5** | Sistema Gemelo Digital | ~10.5 horas | ⏳ Pendiente |
| **Fase 6** | Panel Avanzado | ~6 horas | ⏳ Pendiente |
| **Fase 7** | Testing y Optimización | ~6.5 horas | ⏳ Pendiente |
| **Fase 8** | Documentación | ~6 horas | ⏳ Pendiente |
| **TOTAL** | **40+ tareas** | **~46 horas** | **5% completado** |

---

## 🎯 Prioridades

### Alta Prioridad (Hacer primero)
1. ✅ Resolver conflicto chat.html
2. ✅ Limpiar plantillas
3. 🔄 Visualización de modelos básica
4. 🔄 Panel E2B básico

### Media Prioridad (Hacer después)
5. Importador de redes sociales
6. Sistema de gemelo digital core
7. Panel de métricas

### Baja Prioridad (Hacer al final)
8. Optimizaciones avanzadas
9. Documentación completa
10. Video demo

---

## 📝 Notas de Implementación

### Decisiones Técnicas

#### Frontend
- **Framework:** Vanilla JS (sin React/Vue para mantener simplicidad)
- **Gráficos:** Chart.js o D3.js
- **Terminal:** xterm.js
- **Editor:** Monaco Editor
- **Word Cloud:** wordcloud2.js

#### Backend
- **API:** Flask con RESTful endpoints
- **NLP:** spaCy + transformers (HuggingFace)
- **Fine-tuning:** LoRA con PEFT
- **Vector DB:** FAISS o ChromaDB (ya disponible en archived)
- **Caché:** Redis

#### Base de Datos
```sql
-- Nuevas tablas necesarias
CREATE TABLE digital_twins (
    id UUID PRIMARY KEY,
    user_id UUID,
    name VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    personality_profile JSONB,
    model_path VARCHAR(500),
    status VARCHAR(50)
);

CREATE TABLE social_data (
    id UUID PRIMARY KEY,
    twin_id UUID REFERENCES digital_twins(id),
    platform VARCHAR(50),
    data_type VARCHAR(50),
    content TEXT,
    metadata JSONB,
    imported_at TIMESTAMP
);

CREATE TABLE training_data (
    id UUID PRIMARY KEY,
    twin_id UUID REFERENCES digital_twins(id),
    input_text TEXT,
    target_text TEXT,
    quality_score FLOAT,
    created_at TIMESTAMP
);
```

---

## 🚨 Riesgos y Mitigaciones

### Riesgos Identificados

1. **Límites de APIs de redes sociales**
   - **Mitigación:** Implementar rate limiting y caché

2. **Tiempo de fine-tuning largo**
   - **Mitigación:** Usar LoRA para reducir tiempo, o usar modelo pre-entrenado con prompting

3. **Privacidad de datos del usuario**
   - **Mitigación:** Encriptación, consentimiento explícito, GDPR compliance

4. **Costos de almacenamiento de modelos**
   - **Mitigación:** Comprimir modelos, usar cuantización

---

## 📞 Contacto y Soporte

**Desarrollador:** Claude Code
**Proyecto:** Capibara6 Digital Twin
**Organización:** Anachroni s.coop

---

## 🔄 Historial de Cambios

| Fecha | Cambio | Responsable |
|-------|--------|-------------|
| 2025-11-09 | Creación inicial del TODO.md | Claude |
| 2025-11-09 | Completado PROJECT_STATUS.md | Claude |
| 2025-11-09 | ✅ Fase 1 completada - Conflictos resueltos | Claude |
| 2025-11-09 | Actualizado progreso: 10% completado (4/40 tareas) | Claude |

---

**Próxima actualización:** Durante Fase 2 (Visualización de Modelos)
