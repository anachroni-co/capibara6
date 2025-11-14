# 📊 Guía de Implementación de TOON para Capibara6

**TOON** (Token-Oriented Object Notation) - Formato compacto de serialización para optimizar el uso de tokens con LLMs.

---

## 📋 Resumen del Proyecto

El proyecto **Capibara6** es una plataforma de IA distribuida que integra múltiples modelos de lenguaje (GPT-OSS-20B, Phi-3 Mini, Mixtral 8x7B) con un sistema de:
- 🎯 **Semantic Router** - Selección automática de modelos
- 🧠 **Smart MCP** - Contexto inteligente
- 📊 **TOON** - Optimización de tokens
- 🎵 **TTS** - Síntesis de voz

---

## 🎯 ¿Qué es TOON?

**TOON** es un formato de serialización compacto y legible por humanos diseñado para reducir significativamente el uso de tokens cuando se pasan datos estructurados a Modelos de Lenguaje Grande (LLMs).

### 💡 Beneficios de TOON

- ⚡ **Reducción de 30-60% de tokens** en comparación con JSON para datos tabulares
- 💰 **Mayor eficiencia** en costos y uso de contexto
- 🔄 **Compatible** con estructuras de datos complejas
- 📖 **Legible** y estructurado

---

## 🤔 ¿Cuándo usar TOON?

TOON es especialmente beneficioso en estos escenarios:

1. **Datos tabulares uniformes** - Arrays de objetos con la misma estructura
2. **Grandes volúmenes de datos** - Arrays con más de 5 elementos
3. **Comunicación frecuente** - Interacciones repetidas con LLMs
4. **Optimización de contexto** - Donde el espacio de tokens es crítico

### Ejemplo Comparativo

**JSON** (169 caracteres):
```json
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" }
  ]
}
```

**TOON** (92 caracteres - **45% de ahorro**):
```
users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user
```

---

## 🚀 Implementación en Capibara6

### 1. Servidor Integrado

El servidor principal ahora soporta TOON para todas sus funcionalidades.

- **Endpoint**: `/api/chat`
- **Soporte**: Entrada/salida en TOON o JSON
- **Negociación de contenido**: Selecciona automáticamente el formato óptimo

#### Ejemplo de uso:

```bash
# Enviar request en JSON, recibir en TOON
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept: application/toon" \
  -d '{"message": "hola"}'
```

### 2. Endpoints TOON

#### GET `/api/toon/info`
Información sobre el soporte TOON

```bash
curl http://localhost:5001/api/toon/info
```

Respuesta:
```json
{
  "enabled": true,
  "version": "1.0.0",
  "formats_supported": ["json", "toon"],
  "min_array_size": 5,
  "min_savings_percent": 20
}
```

#### POST `/api/toon/analyze`
Analiza datos y retorna estadísticas de eficiencia

```bash
curl -X POST http://localhost:5001/api/toon/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {"id": 1, "amount": 100, "status": "completed"},
      {"id": 2, "amount": 200, "status": "pending"}
    ]
  }'
```

Respuesta:
```json
{
  "analysis": {
    "json_size": 150,
    "toon_size": 85,
    "savings_percent": 43.3,
    "toon_recommended": true
  },
  "recommendation": {
    "use_toon": true,
    "reason": "TOON ahorra 43.3% de espacio"
  }
}
```

#### POST `/api/toon/convert`
Convierte entre formatos JSON y TOON

```bash
# JSON a TOON
curl -X POST "http://localhost:5001/api/toon/convert?target=toon" \
  -H "Content-Type: application/json" \
  -d '{"users": [{"id": 1, "name": "Alice"}]}'

# TOON a JSON
curl -X POST "http://localhost:5001/api/toon/convert?target=json" \
  -H "Content-Type: application/toon" \
  --data 'users[1]{id,name}:
  1,Alice'
```

#### GET `/api/toon/example`
Retorna ejemplo completo de uso de TOON

```bash
curl http://localhost:5001/api/toon/example
```

---

## 🔧 Implementación Técnica

### Headers HTTP para TOON

Para usar TOON en lugar de JSON:

```http
Content-Type: application/toon
Accept: application/toon
```

O como alternativa:

```http
Content-Type: text/plain
Accept: text/plain
```

### Detección Automática

El sistema puede detectar automáticamente cuándo usar TOON:

```python
from toon_utils.format_manager import FormatManager

# Codificar automáticamente en el mejor formato
content, format_type = FormatManager.encode(data, preferred_format='auto')

# format_type será 'toon' si es más eficiente, 'json' si no
```

### Conversión entre formatos

```python
from toon_utils.format_manager import FormatManager

# Codificar datos
content, format_type = FormatManager.encode(datos, preferred_format='auto')

# Decodificar datos
decoded_data = FormatManager.decode(content, format_type='auto')
```

---

## 📖 Sintaxis TOON

### Arrays de Objetos

```
key[count]{field1,field2,...}:
  value1,value2,...
  value1,value2,...
```

**Ejemplo**:
```
users[3]{id,name,email}:
  1,Alice,alice@example.com
  2,Bob,bob@example.com
  3,Charlie,charlie@example.com
```

### Objeto Único

```
key{field1,field2,...}:
  value1,value2,...
```

**Ejemplo**:
```
config{debug,timeout,retries}:
  true,30,3
```

### Valores Simples

```
key: value
```

**Ejemplo**:
```
version: 1.0.0
enabled: true
count: 42
```

### Tipos de Datos

- **null/None**: `null`
- **Boolean**: `true` / `false`
- **Números**: `42`, `3.14`
- **Strings**: `hello` o `"with, comma"`
  - Usar comillas si contiene comas o espacios

---

## 🧪 Testing

### Test Suite Completo

```bash
cd backend
python test_toon.py
```

Output esperado:
```
✅ TODOS LOS TESTS PASARON

Tests incluidos:
✅ Encoding Python -> TOON
✅ Decoding TOON -> Python
✅ Format Manager
✅ Roundtrip conversions
✅ Edge cases
✅ Efficiency benchmark
```

### Test de Eficiencia

El script de test muestra el ahorro real:

```
Items      JSON            TOON            Ahorro          Recomendado
----------------------------------------------------------------------
5          342             198              42.1%          TOON ✅
10         672             378              43.8%          TOON ✅
20         1332            738              44.6%          TOON ✅
50         3282            1818             44.6%          TOON ✅
100        6552            3618             44.8%          TOON ✅
```

---

## 💻 Uso Programático

### Encoding (Python → TOON)

```python
from toon_utils import ToonEncoder

data = {
    "users": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"}
    ]
}

# Codificar a TOON
toon_string = ToonEncoder.encode(data)
print(toon_string)
# Output:
# users[2]{id,name,role}:
#   1,Alice,admin
#   2,Bob,user

# Verificar ahorro
stats = ToonEncoder.estimate_token_savings(data)
print(f"Ahorro: {stats['savings_percent']}%")
```

### Decoding (TOON → Python)

```python
from toon_utils import ToonParser

toon_string = """
users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user
"""

# Parsear TOON
data = ToonParser.parse(toon_string)
print(data)
# Output:
# {
#   "users": [
#     {"id": 1, "name": "Alice", "role": "admin"},
#     {"id": 2, "name": "Bob", "role": "user"}
#   ]
# }
```

### Format Manager (Auto)

```python
from toon_utils.format_manager import FormatManager

# Análisis automático
stats = FormatManager.analyze_data(data)

if stats['toon_recommended']:
    print(f"Usar TOON - Ahorro: {stats['savings_percent']}%")
    content, fmt = FormatManager.encode(data, 'toon')
else:
    print("Usar JSON")
    content, fmt = FormatManager.encode(data, 'json')
```

---

## 🌐 Uso con APIs

### Cliente Python

```python
import requests

# Enviar en JSON, recibir en TOON
response = requests.post(
    'http://localhost:5001/api/chat',
    json={"message": "hola"},
    headers={"Accept": "application/toon"}
)

# Si la respuesta es TOON
if 'toon' in response.headers.get('Content-Type', ''):
    from toon_utils.format_manager import FormatManager
    data = FormatManager.decode(response.text, 'toon')
else:
    data = response.json()
```

### Cliente JavaScript/TypeScript

```javascript
// Enviar JSON, recibir TOON
const response = await fetch('http://localhost:5001/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/toon'
  },
  body: JSON.stringify({ message: 'hola' })
});

const contentType = response.headers.get('Content-Type');

if (contentType?.includes('toon')) {
  const toonText = await response.text();
  // Parsear TOON (necesitarías un parser JS)
  console.log('Respuesta en TOON:', toonText);
} else {
  const jsonData = await response.json();
  console.log('Respuesta en JSON:', jsonData);
}
```

---

## 📊 Casos de Uso en Capibara6

### 1. Sistema de Consenso

Combinar respuestas de múltiples LLMs de forma eficiente:

```python
# Respuestas de múltiples modelos
responses = {
    "model_responses": [
        {"model": "gpt-oss-20b", "text": "...", "confidence": 0.9},
        {"model": "phi", "text": "...", "confidence": 0.7},
        {"model": "mixtral", "text": "...", "confidence": 0.85}
    ]
}

# Enviar a LLM para análisis
content, fmt = FormatManager.encode(responses, 'auto')
# Ahorro de ~50% vs JSON
```

### 2. Historial de Conversación

```python
# Historial de mensajes
history = {
    "messages": [
        {"role": "user", "content": "...", "timestamp": 1234567890},
        {"role": "assistant", "content": "...", "timestamp": 1234567891},
        # ... 50 mensajes más
    ]
}

# TOON reduce el contexto significativamente
```

### 3. Datos de Usuario

```python
# Información estructurada para personalización
user_data = {
    "preferences": [
        {"key": "language", "value": "es"},
        {"key": "theme", "value": "dark"},
        {"key": "notifications", "value": "enabled"}
    ]
}
```

### 4. Resultados Analíticos

```python
# Datos tabulares que se envían a LLMs para interpretación
analytics = {
    "daily_metrics": [
        {"date": "2025-01-01", "users": 1000, "requests": 5000},
        {"date": "2025-01-02", "users": 1100, "requests": 5500},
        # ... más datos
    ]
}
```

---

## ✅ Buenas Prácticas

### 1. Compatibilidad

Mantener soporte para JSON existente:

```python
@app.route('/api/endpoint', methods=['POST'])
def api_endpoint():
    # Determinar formato de entrada
    content_type = request.headers.get('Content-Type', 'application/json').lower()

    if 'application/toon' in content_type:
        input_data = FormatManager.decode(request.get_data(as_text=True), 'toon')
    else:
        input_data = request.get_json()

    # Procesar...
    result = process_data(input_data)

    # Determinar formato de salida
    accept = request.headers.get('Accept', 'application/json').lower()

    if 'toon' in accept:
        content, fmt = FormatManager.encode(result, 'toon')
        return Response(content, mimetype='application/toon')
    else:
        return jsonify(result)
```

### 2. Negociación de Contenido

Usar headers HTTP para determinar formato automáticamente.

### 3. Detección Automática

Implementar lógica para determinar cuándo usar TOON:

```python
if FormatManager.should_use_toon(data):
    content, fmt = FormatManager.encode(data, 'toon')
else:
    content, fmt = FormatManager.encode(data, 'json')
```

### 4. Pruebas de Eficiencia

Verificar que TOON realmente reduce tokens en tu caso de uso:

```python
stats = FormatManager.analyze_data(data)
print(f"Ahorro estimado: {stats['savings_percent']}%")
print(f"Recomendado: {stats['toon_recommended']}")
```

### 5. Documentación

Documentar claramente los endpoints que soportan TOON.

---

## 🐛 Troubleshooting

### Error: "TOON Format Manager no disponible"

**Causa**: Módulo toon_utils no importado correctamente

**Solución**:
```bash
# Verificar que exista el módulo
ls -la backend/toon_utils/

# Debería contener:
# __init__.py
# parser.py
# encoder.py
# format_manager.py
```

### Datos no coinciden después de roundtrip

**Causa**: Tipos de datos no soportados o formato incorrecto

**Solución**:
```python
# Ejecutar test
python test_toon.py

# Verificar que tu caso de uso esté cubierto
```

### TOON no ahorra espacio

**Causa**: Datos no son adecuados para TOON

**Solución**:
```python
# Analizar datos
stats = FormatManager.analyze_data(data)

if not stats['toon_recommended']:
    print(stats['savings_percent'])  # Ver diferencia
    # Usar JSON en su lugar
```

---

## 📚 Referencias

- **Módulo TOON**: `backend/toon_utils/`
- **Tests**: `backend/test_toon.py`
- **Servidor Integrado**: `backend/capibara6_integrated_server.py`
- **Deployment**: `DEPLOYMENT_GUIDE.md`

---

## 🆘 Soporte

Si tienes problemas con TOON:

1. Ejecuta tests: `python test_toon.py`
2. Verifica análisis: `curl http://localhost:5001/api/toon/analyze`
3. Consulta ejemplos: `curl http://localhost:5001/api/toon/example`
4. Revisa logs del servidor

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0.0
