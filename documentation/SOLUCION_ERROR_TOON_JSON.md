# 🔧 Solución Error: JSON.parse unexpected character (Formato TOON)

## ❌ Problema

Error al enviar mensajes desde el frontend:

```
Error enviando mensaje: SyntaxError: JSON.parse: unexpected character at line 1 column 1 of the JSON data
chat-page.js:455:21
```

## 🔍 Causa Raíz

El backend tiene integrado un sistema de formato **TOON** que puede devolver respuestas en formato `text/plain` en lugar de `application/json` cuando:

1. El frontend no especifica explícitamente `Accept: application/json`
2. El backend detecta que el cliente acepta `text/plain` o `application/toon`
3. El backend decide usar formato TOON para optimizar el tamaño de la respuesta

El frontend estaba intentando parsear todas las respuestas como JSON sin verificar el `Content-Type`, causando el error cuando recibía formato TOON.

## ✅ Solución Aplicada

### 1. Agregado header `Accept: application/json` en todas las peticiones

**En `sendToBackend()`:**
```javascript
headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json', // Asegurar que siempre pedimos JSON
}
```

**En `checkConnection()`:**
```javascript
headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json', // Asegurar que siempre pedimos JSON
}
```

### 2. Manejo robusto de respuestas verificando Content-Type

Antes de parsear la respuesta, ahora verificamos el `Content-Type`:

```javascript
const contentType = response.headers.get('Content-Type') || '';

let data;
if (contentType.includes('application/json')) {
    // Respuesta es JSON
    data = await response.json();
} else if (contentType.includes('text/plain') || contentType.includes('application/toon')) {
    // Respuesta es formato toon - manejar error informativo
    const textResponse = await response.text();
    try {
        data = JSON.parse(textResponse);
    } catch (e) {
        throw new Error('El servidor devolvió formato TOON. Por favor, asegúrate de que el servidor esté configurado para devolver JSON.');
    }
} else {
    // Intentar parsear como JSON por defecto con manejo de errores
    try {
        data = await response.json();
    } catch (e) {
        const textResponse = await response.text();
        throw new Error(`Error parseando respuesta del servidor: ${textResponse.substring(0, 100)}`);
    }
}
```

## 📝 Cambios Realizados

### Archivo: `web/chat-page.js`

1. ✅ Agregado `Accept: application/json` en `sendToBackend()`
2. ✅ Agregado `Accept: application/json` en `checkConnection()`
3. ✅ Agregado manejo robusto de Content-Type antes de parsear
4. ✅ Agregado manejo de errores informativo para formato TOON

## 🔄 Cómo Funciona el Sistema TOON

El sistema TOON es un formato optimizado para reducir el tamaño de las respuestas JSON cuando hay muchos datos repetitivos (arrays grandes, objetos similares).

**Ejemplo TOON:**
```
users[2]{id,name,email}:
  1,Alice,alice@example.com
  2,Bob,bob@example.com
```

**Equivalente JSON:**
```json
{
  "users": [
    {"id": "1", "name": "Alice", "email": "alice@example.com"},
    {"id": "2", "name": "Bob", "email": "bob@example.com"}
  ]
}
```

El backend decide usar TOON cuando:
- El cliente acepta `application/toon` o `text/plain` en el header `Accept`
- Los datos son grandes y repetitivos (arrays con muchos elementos similares)
- El formato TOON sería más eficiente que JSON

## ✅ Verificación

Después de estos cambios:

1. ✅ El frontend siempre solicita JSON explícitamente
2. ✅ El backend respetará el header `Accept` y devolverá JSON
3. ✅ Si por alguna razón se recibe formato TOON, se maneja correctamente
4. ✅ Los errores son más informativos y ayudan a debuggear

## 🧪 Pruebas

Para verificar que funciona:

1. Abre la consola del navegador
2. Envía un mensaje desde el chat
3. Verifica que no aparezca el error de JSON.parse
4. Verifica en Network tab que las peticiones tienen `Accept: application/json`
5. Verifica que las respuestas tienen `Content-Type: application/json`

## 📚 Archivos Relacionados

- `web/chat-page.js` - Frontend (modificado)
- `backend/capibara6_integrated_server.py` - Backend (usa TOON condicionalmente)
- `backend/toon_utils/format_manager_ultra_optimized.py` - Sistema TOON

## ⚠️ Notas Importantes

1. **El sistema TOON sigue disponible** para optimizar respuestas grandes cuando sea necesario
2. **El frontend ahora siempre solicita JSON** para evitar problemas de parsing
3. **Si necesitas usar TOON en el futuro**, puedes agregar soporte explícito en el frontend usando `FormatManager` de JavaScript

