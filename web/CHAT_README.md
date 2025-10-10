# 💬 Interfaz de Chat Capibara6

## Descripción

Interfaz de chat moderna tipo ChatGPT/Claude para interactuar con el modelo capibara6. Incluye una barra lateral plegable con historial de conversaciones y un área principal de chat con respuestas enriquecidas.

## Archivos

- **`chat.html`** - Página principal del chat
- **`chat.css`** - Estilos específicos de la interfaz de chat
- **`chat-app.js`** - Lógica de la aplicación (gestión de mensajes, chats, etc.)

## Características

### 🎨 Interfaz Moderna
- Diseño tipo ChatGPT/Claude
- Tema oscuro coherente con la landing page
- Animaciones suaves y transiciones fluidas
- Responsive para móviles y tablets

### 📁 Barra Lateral
- **Nueva Conversación**: Botón destacado para crear chats
- **Historial organizado**: "Hoy" y "Anteriores"
- **Acciones rápidas**: Eliminar conversaciones
- **Perfil de usuario**: Footer con información del usuario
- **Ocultable**: Toggle para maximizar el área de chat

### 💬 Área de Chat
- **Estado vacío**: Pantalla de bienvenida con sugerencias
- **Mensajes enriquecidos**: Soporte para markdown, código, etc.
- **Typing indicator**: Indicador visual mientras el modelo responde
- **Acciones de mensaje**: Copiar, me gusta, no me gusta
- **Auto-scroll**: Scroll automático a nuevos mensajes

### ⚙️ Funcionalidades
- **Persistencia local**: Los chats se guardan en `localStorage`
- **Soporte multiidioma**: Español e inglés
- **Adjuntar archivos**: Preparado para futura implementación
- **Configuración**: Modal con opciones de modelo, temperatura, etc.
- **Textarea inteligente**: Auto-resize y envío con Enter

## Tarjetas de Sugerencia

La página incluye 4 sugerencias predefinidas:
1. **Arquitectura Híbrida** - Sobre Transformer-Mamba
2. **Google TPU** - Ventajas de TPU v6e-64
3. **Programación** - Ayuda con código Python
4. **Optimización** - Mejora de rendimiento web

## Integración con Backend

Actualmente usa respuestas simuladas (`generateMockResponse`). Para conectar con un backend real:

```javascript
// En chat-app.js, reemplazar en simulateAssistantResponse()
const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        message: userMessage, 
        chatId: currentChatId 
    })
});
const data = await response.json();
appendMessage('assistant', data.message);
```

## Estructura de Datos

### Chat Object
```javascript
{
    id: string,
    title: string,
    messages: Message[],
    createdAt: ISO8601,
    updatedAt: ISO8601
}
```

### Message Object
```javascript
{
    role: 'user' | 'assistant',
    content: string,
    timestamp: ISO8601
}
```

## Responsive Design

- **Desktop**: Sidebar visible por defecto
- **Tablet/Mobile**: Sidebar oculta por defecto con botón toggle
- **Breakpoint**: 768px

## Personalización

### Colores
Los colores se heredan de `styles.css`:
- `--primary`: Color principal (#6366f1)
- `--secondary`: Color secundario (#ec4899)
- `--bg-primary`: Fondo principal (#1e293b)
- `--bg-secondary`: Fondo secundario (#334155)

### Variables CSS Específicas
Definidas en `chat.css` para personalización adicional.

## Acceso

La página es accesible desde:
- Botón "Comenzar Ahora" en el hero de `index.html`
- Botón "Comenzar Ahora" en la sección CTA de `index.html`
- Directamente en `/chat.html`

## Próximas Mejoras

- [ ] Conexión con backend real
- [ ] Soporte para adjuntar archivos (imágenes, PDFs)
- [ ] Exportar conversaciones
- [ ] Modo de búsqueda en historial
- [ ] Compartir conversaciones
- [ ] Voice input
- [ ] Renderizado de LaTeX para matemáticas
- [ ] Sintaxis highlighting mejorado para código
- [ ] Streaming de respuestas (token por token)

## Notas Técnicas

- Los chats se almacenan en `localStorage` con la clave `capibara6-chats`
- El idioma se sincroniza con `localStorage` (clave: `preferred-language`)
- Los iconos usan Lucide Icons (mismo que la landing page)
- Las traducciones están en `translations.js`

---

**Desarrollado por Anachroni s.coop**  
Parte del proyecto capibara6

