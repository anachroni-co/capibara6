# 🎨 Capibara6 Consensus - Nuevas Características de UI

## 📋 Resumen de Mejoras

Se ha adaptado completamente la UI del chat para reflejar todas las características del sistema **Capibara6 Consensus**, incluyendo selector de modelos, estado de servicios en tiempo real, y controles avanzados.

---

## ✨ Nuevas Características

### 1. **Panel de Control de Servicios** (Sidebar Derecho)

Un panel completo para gestionar todos los aspectos del sistema Capibara6 Consensus.

**Acceso**: Hacer clic en el botón "Control" en el header del chat.

**Características**:
- 📊 **Tarjeta de Modelo Actual**: Muestra el modelo activo con sus especificaciones
- 🔄 **Selector de Modelos**: Cambiar entre GPT-OSS 20B, Mistral, y Phi-3
- 📡 **Estado de Servicios**: Monitoreo en tiempo real de Ollama, TTS, MCP y N8N
- 🎛️ **Controles de Servicios**: Toggle para activar/desactivar TTS y MCP
- ⚙️ **Parámetros de Generación**: Sliders para temperatura, max_tokens y top_p
- 🏗️ **Info de Infraestructura**: IPs de VMs y región de Google Cloud

---

### 2. **Indicador de Modelo Activo en Header**

Muestra siempre visible el modelo que estás usando actualmente:
- 🦫 Icono del modelo
- Nombre del modelo (ej: "GPT-OSS 20B")
- Parámetros (ej: "20.9B params")

---

### 3. **Badges de Servicios Activos**

Badges visuales en el header que indican qué servicios están activos:
- 🛡️ **MCP**: Si Smart MCP está activado (contexto verificado)
- 🎙️ **TTS**: Si Text-to-Speech está activado
- Indicadores de color verde cuando el servicio está online

---

### 4. **Selector de Modelos**

Selecciona entre los modelos disponibles en Ollama:

| Modelo | Parámetros | Ventana de Contexto | Características |
|--------|-----------|---------------------|-----------------|
| **GPT-OSS 20B** | 20.9B | 4K tokens | Modelo principal, balanceado |
| **Mistral** | 7B | 32K tokens | Rápido y eficiente |
| **Phi-3** | 3.8B | 128K tokens | Compacto, ventana larga |

---

### 5. **Estado de Servicios en Tiempo Real**

El panel verifica automáticamente el estado de:
- **Ollama** (puerto 11434): Servidor de modelos
- **TTS** (puerto 5002): Text-to-Speech con Coqui
- **MCP** (puerto 5003): Model Context Protocol
- **N8N** (puerto 5678): Automatización de workflows

Estados posibles:
- 🟢 **Online**: Servicio activo y respondiendo
- 🔴 **Offline**: Servicio no disponible
- 🟡 **Verificando**: Comprobando estado

---

### 6. **Controles de Servicios**

Toggle switches para activar/desactivar servicios:

**TTS (Text-to-Speech)**:
- Cuando está activado, usa Coqui TTS desde el servidor
- Cuando está desactivado, usa Web Speech API del navegador

**MCP (Model Context Protocol)**:
- Cuando está activado, agrega contexto verificado a las consultas
- Cuando está desactivado, envía consultas directamente al modelo

---

### 7. **Parámetros de Generación Ajustables**

Controla cómo el modelo genera respuestas:

**Temperatura** (0.0 - 2.0):
- Valores bajos (0.1-0.3): Respuestas más conservadoras y predecibles
- Valores medios (0.7-0.9): Balanceadas
- Valores altos (1.2-2.0): Más creativas y variadas

**Máximo de Tokens** (100 - 2000):
- Define la longitud máxima de la respuesta
- 200-500: Respuestas cortas
- 500-1000: Respuestas medias
- 1000-2000: Respuestas largas

**Top P** (0.0 - 1.0):
- Controla la diversidad del vocabulario
- 0.5: Muy conservador
- 0.9: Balanceado (recomendado)
- 1.0: Máxima diversidad

---

### 8. **Branding "Capibara6 Consensus"**

Se ha actualizado todo el branding para reflejar el sistema de consenso:
- Título de página: "Capibara6 Consensus"
- Banner beta con información del modelo
- Badge de "Consensus System"
- Sugerencias actualizadas sobre el sistema

---

## 🎯 Cómo Usar las Nuevas Características

### Cambiar de Modelo:
1. Click en botón "Control" en el header
2. Sección "Modelo de IA"
3. Selecciona el modelo deseado
4. La tarjeta se actualiza automáticamente

### Ver Estado de Servicios:
1. Abre el panel de control
2. Sección "Estado de Servicios"
3. Verás indicadores en tiempo real
4. 🟢 = Online, 🔴 = Offline

### Activar/Desactivar TTS:
1. Panel de control → "TTS Activado"
2. Click en el toggle switch
3. Verde = Activado, Gris = Desactivado

### Activar/Desactivar MCP:
1. Panel de control → "MCP Activado"
2. Click en el toggle switch
3. Verde = Contexto verificado activado

### Ajustar Parámetros:
1. Panel de control → "Parámetros de Generación"
2. Mueve los sliders
3. Los cambios se aplican inmediatamente
4. Los valores se guardan en localStorage

---

## 🔧 Archivos Nuevos

### `/web/chat-consensus.css`
Estilos CSS para todos los nuevos componentes:
- Panel de servicios
- Selector de modelos
- Badges e indicadores
- Controles y sliders

### `/web/consensus-ui.js`
Lógica JavaScript para:
- Gestión del panel de servicios
- Verificación de estado de servicios
- Cambio de modelos
- Persistencia de configuración

---

## 📱 Responsive Design

Las nuevas características son completamente responsive:

**Desktop** (> 1024px):
- Panel lateral de 320px
- Todos los indicadores visibles

**Tablet** (768px - 1024px):
- Panel lateral adaptable
- Indicadores principales visibles

**Mobile** (< 768px):
- Panel de servicios a pantalla completa
- Algunos badges ocultos para ahorrar espacio
- Indicador de modelo oculto

---

## 🎨 Temas y Colores

Los nuevos componentes usan la paleta de colores existente:
- **Primario**: Púrpura (#8b5cf6)
- **Secundario**: Azul (#3b82f6)
- **Success**: Verde (#10b981)
- **Warning**: Naranja (#f59e0b)
- **Error**: Rojo (#ef4444)

---

## 🔄 Persistencia de Configuración

Todas las configuraciones se guardan en `localStorage`:
- Modelo seleccionado
- Estado de TTS (activado/desactivado)
- Estado de MCP (activado/desactivado)
- Valores de parámetros (temperatura, tokens, top_p)

Al recargar la página, se restaura la configuración anterior.

---

## 🚀 Mejoras Futuras Planificadas

- [ ] Gráficos de uso de recursos (CPU, RAM, GPU)
- [ ] Historial de cambios de modelo
- [ ] Exportar/Importar configuración
- [ ] Modo oscuro/claro
- [ ] Personalización de colores
- [ ] Estadísticas de uso de servicios
- [ ] Notificaciones cuando servicios se caen/activan

---

## 🐛 Troubleshooting

### Panel de servicios no se abre:
- Verifica que `consensus-ui.js` esté cargado
- Mira la consola del navegador por errores
- Recarga la página con Ctrl+F5

### Servicios aparecen como Offline:
- Verifica que los servicios estén corriendo en las VMs
- Comprueba conectividad: `curl http://34.12.166.76:11434/api/tags`
- Verifica firewall y puertos abiertos

### Modelo no cambia:
- El backend debe soportar cambios de modelo dinámicamente
- Por ahora, el cambio es visual (backend usa modelo configurado en .env)
- Implementación futura: pasar modelo en cada request

---

## 📝 Notas Técnicas

**Verificación de Servicios**:
- Timeout: 3 segundos por servicio
- Se ejecuta al cargar la página
- No se auto-refresca (planificado para futura versión)

**Integración con Backend**:
- TTS: `TTS_CONFIG.useCoquiTTS` controla el uso
- MCP: `SMART_MCP_CONFIG.enabled` controla el uso
- Modelo: Se guarda pero backend debe implementar cambio dinámico

---

**Última actualización**: 2025-11-11
**Versión**: 1.0
**Autor**: Claude (adaptación UI)
