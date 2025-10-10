# Configuración del Chat - Capibara6

> 🟡 **MODO BETA**: El sistema Capibara6 Consensus está actualmente en fase beta.

## Conexión con el Servidor

El chat está configurado para conectarse con un servidor de inferencia que ejecuta Capibara6.

### URL del Servidor
```
http://34.175.89.158:8080/completion
```

### Parámetros Configurados

```javascript
{
  "prompt": "<bos><start_of_turn>system\nResponde en el mismo idioma de la pregunta. Si piden código, usa bloques markdown: \`\`\`lenguaje<end_of_turn>\n<start_of_turn>user\n{mensaje}<end_of_turn>\n<start_of_turn>model\n",
  "n_predict": 100,           // Respuestas cortas y enfocadas
  "temperature": 0.6,         // Balanceado
  "top_p": 0.85,             // Ligeramente reducido
  "repeat_penalty": 1.3,     // Evita repeticiones sin ser excesivo
  "stream": true,            // Streaming activado
  "stop": ["<end_of_turn>", "<|im_end|>", "\n```", "html<!DOCTYPE", "html<", "php<", "js<", "{-", "<audio", "<video"]
}
```

### System Prompt

El chat incluye automáticamente un **system prompt** mejorado que evita respuestas antropomórficas incorrectas:

```
Tu nombre es Capibara6. Responde de forma breve y precisa.
```

**Filosofía MINIMALISTA para Gemma 3:**
- ✅ Ultra corto (10 palabras) - imposible de citar
- ✅ Solo lo esencial: nombre + comportamiento
- ✅ Lenguaje directo sin listas ni formatos
- ✅ El modelo no tiene nada que copiar o repetir

**Por qué tan simple:**
Los prompts largos con Gemma 3 tienden a ser citados por el modelo en lugar de seguirlos. 
Un prompt minimalista evita este problema completamente.

**Parámetros OPTIMIZADOS y BALANCEADOS:**
- `n_predict: 100` - Respuestas cortas y al punto
- `temperature: 0.6` - Balanceado (ni muy creativo ni muy rígido)
- `top_p: 0.85` - Ligeramente reducido
- `repeat_penalty: 1.3` - Evita repeticiones sin bloquear
- **Streaming**: Activado para respuestas en tiempo real
- **Stops especiales**: Para evitar código duplicado y tokens extraños
  - `"\n```"` - Detiene después de bloques de código
  - `"html<!DOCTYPE"`, `"html<"`, `"php<"` - Evita tokens malformados
  - `"<audio"`, `"<video"` - Evita metadata multimedia
  - `"<|im_end|>"` - Token de fin estándar

**Estadísticas mostradas (6 valores informativos):**
- ⏱️ **Tiempo**: Duración de generación
- 💬 **Tokens Gen**: Tokens generados por el modelo
- ➡️ **Tokens In**: Tokens del prompt (entrada)
- 📚 **Total**: Tokens totales procesados
- ⚡ **Velocidad**: Tokens/segundo
- 🖥️ **Modelo**: capibara6

Este prompt puede modificarse en `chat-app.js` línea 8.

### Ejemplos de Respuestas Correctas

❌ **INCORRECTO:**
```
Usuario: ¿Cuál es la capital de Italia?
Capibara6: La capital de Italia es Roma. Puedes encontrar más detalles 
en Wikipedia (https://it.wikipedia.org/wiki/Roma). ¿Hay algo más en lo 
que pueda ayudarte? Puedes buscar información sobre otros países...
```

✅ **CORRECTO:**
```
Usuario: ¿Cuál es la capital de Italia?
Capibara6: La capital de Italia es Roma.
```

❌ **INCORRECTO:**
```
Usuario: ¿Qué haces en tu tiempo libre?
Capibara6: En mi tiempo libre disfruto de aprender sobre IA...
```

✅ **CORRECTO:**
```
Usuario: ¿Qué haces en tu tiempo libre?
Capibara6: Soy un modelo de IA, no tengo tiempo libre.
```

### Modificar Configuración

Para cambiar la URL o los parámetros, edita el archivo `chat-app.js`:

```javascript
// Configuración del modelo (líneas 5-18)
const MODEL_CONFIG = {
    serverUrl: 'http://34.175.89.158:8080/completion',
    systemPrompt: `Tu nombre es Capibara6. Responde de forma breve y precisa.`,
    defaultParams: {
        n_predict: 512,
        temperature: 0.6,
        top_p: 0.9,
        repeat_penalty: 1.1,
        presence_penalty: 0.2,
        frequency_penalty: 0.2,
        stop: ["<end_of_turn>", "\n\n\n"]
    }
};
```

### Ejemplo de Request

**Mensaje simple:**
```bash
curl http://34.175.89.158:8080/completion -d '{
  "prompt": "<bos><start_of_turn>user\nDescribe qué es la inteligencia artificial.<end_of_turn>\n<start_of_turn>model\n",
  "n_predict": 128,
  "temperature": 0.6,
  "top_p": 0.9,
  "repeat_penalty": 1.1,
  "presence_penalty": 0.2,
  "frequency_penalty": 0.2
}'
```

**Conversación con historial y system prompt:**
```bash
curl http://34.175.89.158:8080/completion -d '{
  "prompt": "<bos><start_of_turn>system\nEres Capibara6, un asistente de IA creado por Anachroni s.coop. Eres útil, conciso y preciso. Responde solo lo necesario, en el idioma del usuario. Evita repetir la pregunta y limita tus respuestas a 3 párrafos como máximo. Cuando te pregunten quién eres, di que te llamas Capibara6 y fuiste creado por Anachroni s.coop.<end_of_turn>\n<start_of_turn>user\n¿Cuál es la capital de España?<end_of_turn>\n<start_of_turn>model\nMadrid.<end_of_turn>\n<start_of_turn>user\n¿Y de Italia?<end_of_turn>\n<start_of_turn>model\n",
  "n_predict": 64
}'
```

El chat **automáticamente**:
- Agrega el system prompt al inicio
- Construye el historial completo de la conversación
- Mantiene el contexto en cada request

### Formato de Respuesta

El servidor retorna un JSON con la siguiente estructura:

```json
{
  "content": "respuesta del modelo...",
  "tokens_predicted": 88,
  "stop": true,
  "model": "gpt-3.5-turbo",
  ...
}
```

## Características Implementadas

✅ Conexión directa con Capibara6  
✅ Manejo de errores con mensajes amigables  
✅ Indicador de escritura mientras genera  
✅ Soporte para archivos adjuntos (hasta 10MB)  
✅ Historial de conversaciones  
✅ Interfaz estilo ChatGPT  

## CORS

**Importante:** El servidor debe tener CORS habilitado para permitir peticiones desde el navegador.

Si encuentras errores de CORS, necesitarás configurar el servidor o usar un proxy.

## Solución de Problemas

### Error de CORS
Si ves errores de CORS en la consola del navegador, el servidor necesita agregar estos headers:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### Servidor no responde
Verifica que el servidor esté activo:

```bash
curl http://34.175.89.158:8080/completion -d '{"prompt":"test","n_predict":10}'
```

### Timeout
Si las respuestas tardan mucho, reduce `n_predict` a un valor menor (ej: 256).

## Desarrollo Local

Para probar localmente con un servidor diferente:

1. Modifica `MODEL_CONFIG.serverUrl` en `chat-app.js`
2. Asegúrate de que el servidor esté corriendo
3. Abre `chat.html` en tu navegador

## Producción

Para producción, considera:

- Usar HTTPS en lugar de HTTP
- Implementar autenticación
- Agregar rate limiting
- Configurar un proxy inverso (nginx/Apache)

