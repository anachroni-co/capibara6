# 🎨 Diseños Pendientes de Integración - Capibara6

## 📋 Resumen

Se han identificado varios servicios y diseños desarrollados que **NO están integrados** en el chat principal (`chat.html`). Estos servicios tienen interfaces completas y funcionales que deberían estar disponibles desde el chat.

## 🔍 Servicios con Diseños Completos No Integrados

### 1. ✅ **TTS (Text-to-Speech)** - Parcialmente Integrado

**Estado**: ⚠️ Archivo existe pero NO está cargado en `chat.html`

**Archivos**:
- `tts-integration.js` - Integración completa de TTS con Coqui/Kyutai
- Funcionalidad: Síntesis de voz, control de velocidad, pitch, volumen

**Lo que falta**:
- ❌ No se carga el script en `chat.html`
- ❌ No hay UI para controlar TTS (botones de play/pause, velocidad, etc.)
- ❌ No hay indicador visual cuando está hablando

**Diseño sugerido**: Botones de control TTS en la barra de herramientas del chat

---

### 2. ❌ **MCP (Model Context Protocol)** - No Integrado

**Estado**: ⚠️ Archivos existen pero NO están integrados

**Archivos**:
- `mcp-integration.js` - Integración básica de MCP
- `smart-mcp-integration.js` - Integración avanzada con análisis de contexto
- `mcp-cors-proxy.js` - Proxy CORS para MCP

**Lo que falta**:
- ❌ No se cargan los scripts en `chat.html`
- ❌ No hay UI para ver el contexto MCP activo
- ❌ No hay indicadores de cuando MCP está analizando
- ❌ No hay configuración de MCP en settings

**Diseño sugerido**: 
- Panel lateral con contexto MCP activo
- Indicador de estado MCP en el header
- Configuración en modal de settings

---

### 3. ❌ **N8n Dashboard** - Completamente Separado

**Estado**: ✅ Diseño completo pero página separada

**Archivos**:
- `n8n-dashboard.html` - Dashboard completo y moderno
- `n8n-manager.js` - Gestor completo de workflows
- `n8n-widget.js` - Widget para mostrar workflows

**Lo que falta**:
- ❌ Es una página separada, no integrada en el chat
- ❌ No hay acceso rápido desde el chat principal
- ❌ No hay widget pequeño en el sidebar

**Diseño sugerido**:
- Botón en sidebar para abrir dashboard n8n
- Widget pequeño mostrando workflows activos
- Integración en el modal de settings

---

### 4. ❌ **RAG System** - Demo Separado

**Estado**: ✅ Demo completo pero página separada

**Archivos**:
- `rag-demo.html` - Demo completo con UI moderna
- `rag-api-client.js` - Cliente completo para RAG API

**Lo que falta**:
- ❌ Es una página separada, no integrada
- ❌ No hay acceso desde el chat principal
- ❌ No hay indicador de cuando RAG está siendo usado
- ❌ No hay visualización de fuentes RAG en las respuestas

**Diseño sugerido**:
- Panel lateral con búsqueda RAG
- Indicador de fuentes RAG en mensajes
- Botón para buscar en RAG desde el chat
- Integración en el modal de settings

---

### 5. ⚠️ **Model Visualization** - Archivo Existe

**Estado**: ⚠️ Archivo existe pero no se usa

**Archivos**:
- `model-visualization.js` - Visualización de modelos activos

**Lo que falta**:
- ❌ No se carga en `chat.html`
- ❌ No hay UI para visualizar modelos disponibles
- ❌ No hay selector de modelo en el chat

**Diseño sugerido**: Selector de modelo en el header o settings

---

### 6. ⚠️ **Entropy Monitor** - Archivo Existe

**Estado**: ⚠️ Archivo existe pero no se usa

**Archivos**:
- `entropy-monitor.js` - Monitor de entropía
- `entropy-auto-inject.js` - Inyección automática de entropía

**Lo que falta**:
- ❌ No se carga en `chat.html`
- ❌ No hay visualización de entropía en tiempo real
- ❌ No hay gráficos de entropía

**Diseño sugerido**: Panel de estadísticas con gráfico de entropía

---

## 📊 Comparación: Lo que hay vs Lo que se usa

| Servicio | Archivo Existe | Cargado en chat.html | UI Integrada | Estado |
|----------|----------------|---------------------|--------------|--------|
| TTS | ✅ | ❌ | ❌ | Pendiente |
| MCP | ✅ | ❌ | ❌ | Pendiente |
| Smart MCP | ✅ | ❌ | ❌ | Pendiente |
| N8n | ✅ | ❌ | ❌ (separado) | Pendiente |
| RAG | ✅ | ❌ | ❌ (separado) | Pendiente |
| Model Viz | ✅ | ❌ | ❌ | Pendiente |
| Entropy | ✅ | ❌ | ❌ | Pendiente |

## 🎯 Plan de Integración Sugerido

### Fase 1: Integración Básica (Prioridad Alta)

1. **TTS Integration**
   - Cargar `tts-integration.js` en `chat.html`
   - Añadir botones de control TTS en la barra de herramientas
   - Indicador visual cuando está hablando

2. **MCP Integration**
   - Cargar `smart-mcp-integration.js` en `chat.html`
   - Añadir indicador de estado MCP en header
   - Panel lateral con contexto MCP activo

### Fase 2: Integración Avanzada (Prioridad Media)

3. **RAG Integration**
   - Integrar búsqueda RAG en el chat
   - Mostrar fuentes RAG en respuestas
   - Panel lateral con búsqueda RAG

4. **N8n Widget**
   - Widget pequeño en sidebar
   - Acceso rápido al dashboard
   - Indicador de workflows activos

### Fase 3: Mejoras Visuales (Prioridad Baja)

5. **Model Visualization**
   - Selector de modelo en settings
   - Visualización de modelos disponibles

6. **Entropy Monitor**
   - Panel de estadísticas
   - Gráfico de entropía en tiempo real

## 🔧 Cambios Necesarios en `chat.html`

### Scripts a Añadir:

```html
<!-- Después de config.js -->
<script src="tts-integration.js"></script>
<script src="smart-mcp-integration.js"></script>
<script src="rag-api-client.js"></script>
<script src="n8n-manager.js"></script>
<script src="model-visualization.js"></script>
<script src="entropy-monitor.js"></script>
```

### Elementos UI a Añadir:

1. **Barra de herramientas TTS**:
   - Botón play/pause
   - Control de velocidad
   - Selector de voz

2. **Indicador MCP**:
   - Badge en header mostrando estado MCP
   - Panel lateral con contexto

3. **Acceso RAG**:
   - Botón de búsqueda RAG
   - Panel lateral con resultados

4. **Widget N8n**:
   - Botón en sidebar
   - Indicador de workflows activos

## 📝 Archivos de Referencia

- `n8n-dashboard.html` - Ejemplo de diseño moderno para dashboard
- `rag-demo.html` - Ejemplo de diseño para búsqueda RAG
- `test-integrated.html` - Ejemplo de integración múltiple

## ✅ Próximos Pasos

1. Revisar cada archivo de integración
2. Crear componentes UI para cada servicio
3. Integrar scripts en `chat.html`
4. Añadir elementos UI necesarios
5. Probar funcionalidad completa

---

**Última actualización**: Noviembre 2025

