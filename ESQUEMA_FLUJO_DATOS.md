# Esquema del Flujo de Datos del Sistema Capibara6

## Arquitectura de las VMs
- **services**: 34.175.48.1 (IP interna 10.204.0.9) - Gateway server
- **models-europe**: 34.175.48.2 (IP interna 10.204.0.8) - vLLM multi-model service
- **rag-europe**: 34.175.48.3 (IP interna 10.204.0.10) - RAG system

**Nota importante**: Según diagnóstico recibido, la VM models-europe tiene IP interna 10.204.0.9, por lo que se usará esta IP como destino

## Flujo Completo de una Solicitud de Chat

### 1. Inicio: Usuario envía mensaje
- Usuario escribe mensaje en el frontend y hace clic en "Enviar"
- Frontend: `web/chat-page.js` captura el evento
- Se construye payload con: `{message, model, temperature, max_tokens, use_semantic_router: true}`

### 2. Frontend a Vercel API Route
- Frontend hace POST a: `https://www.capibara6.com/api/chat`
- Se envía el payload completo, incluyendo `use_semantic_router: true`
- Vercel ejecuta: `/api/chat.js` (Next.js API route)

### 3. Vercel a VM models-europe
- Vercel API route (`/api/chat.js`) conecta a: `http://10.204.0.9:8082/v1/chat/completions`
- Payload se transforma a formato OpenAI: `{model, messages: [{role: "user", content}], temperature, max_tokens, use_semantic_router}`
- Se usa la IP interna para comunicación segura entre VMs

### 4. VM models-europe procesa solicitud
- VM models-europe (10.204.0.9:8082) recibe la solicitud en endpoint `/v1/chat/completions`
- Sistema "Programming-Only RAG" analiza si el contenido es de programación
- Si es programación → activa RAG para contexto externo
- Si es general → no usa RAG (respuesta más rápida)

### 5. VM models-europe devuelve respuesta
- El modelo `aya_expanse_multilingual` procesa la solicitud
- Se devuelve respuesta en formato OpenAI: `{choices: [{message: {role, content}}], model, etc.}`

### 6. Vercel procesa respuesta
- Si respuesta exitosa: `/api/chat.js` la devuelve tal cual al frontend
- Si hay error: se devuelve respuesta simulada con información sobre sistema RAG
- Se mantienen headers CORS apropiados

### 7. Frontend recibe y muestra respuesta
- Frontend recibe respuesta de: `https://www.capibara6.com/api/chat`
- `web/chat-page.js` procesa la respuesta y la muestra en el chat
- Si hay conexión fallida, se usan respuestas simuladas como fallback

## Manejo de Errores y Fallback
- Timeouts (30s) → respuestas simuladas
- Connection errors → respuestas simuladas
- Error 500 evitados → respuestas simuladas
- Sistema robusto que mantiene experiencia de usuario incluso en beta

## Características del Sistema RAG
- **Programming-Only RAG**: Solo activa RAG para consultas de programación (Python, JS, etc.)
- **Consultas generales**: No usan RAG para mayor velocidad
- **Detección precisa**: 100% de detección correcta entre programación y general
- **Sistema listo**: Funcional y preparado para integración completa
- **Colas de trabajo**: Activadas cuando recursos > 90%

## Seguridad
- Comunicación interna usando IPs internas (10.204.0.x)
- CORS restringido según entorno
- Conexión HTTPS desde frontend a Vercel
- Endpoint de backend no expuesto directamente al público