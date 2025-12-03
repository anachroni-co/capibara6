# Guía Completa para Agentes - Sistema ARM-Axion Capibara6

## Descripción General

Este documento proporciona la guía completa para agentes que trabajan con el sistema ARM-Axion Capibara6 en la VM `models-europe`. El sistema está optimizado para el procesador ARM Axion de Google Cloud con vLLM y 5 modelos especializados.

## ⚠️ Arquitectura Distribuida - Crítica para Agentes

### VM models-europe (esta VM - 34.175.48.2)
**SOLO servicios de IA/modelos**:
- ✅ Puerto 8082: `multi_model_server.py` (servidor de modelos con router semántico)
- ✅ 5 modelos de IA especializados con optimizaciones ARM-Axion
- ✅ Lazy loading para eficiencia de memoria
- ❌ NO iniciar: MCP, TTS, servidores backend (corren en VM `services`)

### VM services (34.175.255.139)
- ✅ Puerto 5000: Servidor API principal
- ✅ Puerto 5002: Servidor TTS (Text-to-Speech)
- ✅ Puerto 5003: Servidor MCP (Model Context Protocol)
- ✅ Puerto 5010: Servidor MCP alternativo
- ✅ Puerto 5678: Servidor n8n
- ❌ NO iniciar: Servidor de modelos vLLM (corre en models-europe)

## 🚀 Optimizaciones ARM-Axion Implementadas

### 1. Kernels NEON Optimizados
- **MatMul FP32 con tiles 8x8**: Multiplicación de matrices hasta 40% más rápida
- **Softmax vectorizado**: Aproximación polinomial de exp, 8-10x más rápido
- **RMSNorm**: 5x más rápido con operaciones vectorizadas
- **RoPE (Rotary Position Embeddings)**: Procesamiento vectorizado de pares
- **SwiGLU fusionado**: Activaciones procesadas en un solo kernel
- **GeLU fusionado**: Aproximación optimizada con vectorización

### 2. KV Cache en FP8
- **Reducción de memoria**: KV Cache en 8-bit en lugar de 16-bit
- **Mayor eficiencia**: Uso reducido de ancho de banda de memoria
- **Mejor rendimiento**: Mayor cantidad de tokens en caché al mismo tiempo
- **Aplicado a**: Todos los modelos (`phi4_fast`, `mistral_balanced`, `qwen_coder`, `gemma3_multimodal`, `aya_expanse_multilingual`)

### 3. Captured Graphs
- **Menor overhead**: Gráficos computacionales pre-compilados
- **Mayor velocidad**: No hay JIT compilation en solicitudes repetidas
- **Optimizado**: Longitud de contexto de 8192 tokens para captura

### 4. Scheduler Optimizado
- **Low latency focus**: Configuración para priorizar latencia sobre throughput
- **Num scheduler steps**: Reducido a 2 para menor latencia
- **Chunked prefill**: Activado para mejorar TTFT (Time To First Token)

### 5. Lazy Loading Inteligente
- **Carga bajo demanda**: Modelos se cargan solo cuando se necesitan
- **Pool de warmup**: 2 modelos precargados para respuesta rápida
- **Auto-unloading**: Modelos descargan después de 5 minutos de inactividad

## 📋 Estado Actual del Servidor

**Fecha**: 2025-12-02

- **VM**: models-europe (ARM Axion C4A-standard-32)
- **vCPUs**: 32 cores ARM Axion
- **RAM**: 125 GB
- **Servidor activo**: Puerto 8082
- **Modelos disponibles**: 5 modelos especializados
- **Modelos cargados actualmente**: 
  - `gemma3_multimodal`
  - `aya_expanse_multilingual`

## 🤖 Modelos Disponibles

1. **phi4_fast**
   - Dominio: General
   - Descripción: Modelo rápido para respuestas simples y directas
   - Optimizaciones: Quantization AWQ, NEON, float16
   - Latencia típica: ~0.15-0.25s (después del warmup)

2. **mistral_balanced** 
   - Dominio: Technical
   - Descripción: Modelo equilibrado para tareas técnicas intermedias
   - Optimizaciones: Quantization AWQ, NEON, float16
   - Latencia típica: ~0.3-0.4s (después del warmup)

3. **qwen_coder**
   - Dominio: Coding
   - Descripción: Modelo especializado en código y programación
   - Optimizaciones: Quantization AWQ, NEON, float16
   - Latencia típica: ~0.2-0.3s (después del warmup)

4. **gemma3_multimodal**
   - Dominio: Multimodal Expert
   - Descripción: Modelo multimodal para texto + imágenes, análisis complejo
   - Optimizaciones: Flash Attention, ACL GEMM, NEON, bfloat16
   - Latencia típica: ~4.5-5.0s (después del warmup)

5. **aya_expanse_multilingual**
   - Dominio: Multilingual Expert
   - Descripción: Modelo experto multilingüe de Cohere, 23 idiomas
   - Optimizaciones: Flash Attention, ACL GEMM, NEON, bfloat16
   - Latencia típica: ~4.0s (después del warmup)

## 🔧 Endpoints API Disponibles

### Servidor Estándar (Puerto 8082) - Respuesta Completa
- Health Check: `GET http://localhost:8082/health`
- Listar Modelos: `GET http://localhost:8082/v1/models`
- Chat Completions (OpenAI): `POST http://localhost:8082/v1/chat/completions`
- Completions (OpenAI): `POST http://localhost:8082/v1/completions`
- Estadísticas: `GET http://localhost:8082/stats`

### Servidor con Streaming (Puerto 8083) - Streaming Verdadero
- Health Check: `GET http://localhost:8083/health`
- Listar Modelos: `GET http://localhost:8083/v1/models`
- Chat Completions (OpenAI con streaming): `POST http://localhost:8083/v1/chat/completions`
- Completions (OpenAI con streaming): `POST http://localhost:8083/v1/completions`
- Estadísticas: `GET http://localhost:8083/stats`

### Servidor con Consenso Paralelo (Puerto 8084) - Múltiples Expertos
- Health Check: `GET http://localhost:8084/health`
- Listar Modelos: `GET http://localhost:8084/v1/models`
- Chat Completions (OpenAI con consenso): `POST http://localhost:8084/v1/chat/completions`
- Completions (OpenAI con consenso): `POST http://localhost:8084/v1/completions`
- Estadísticas: `GET http://localhost:8084/stats`

### Ejemplo de solicitud con streaming
```
POST http://localhost:8083/v1/chat/completions
Content-Type: application/json

{
  "model": "aya_expanse_multilingual",
  "messages": [
    {"role": "user", "content": "¿Cómo funciona la atención Flash en ARM Axion?"}
  ],
  "max_tokens": 100,
  "temperature": 0.7,
  "stream": true
}
```

### Ejemplo de solicitud con consenso (sin especificar modelo)
```
POST http://localhost:8084/v1/chat/completions
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Explica cómo se implementan las optimizaciones ARM-Axion"}
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
```

### Notas sobre las diferentes configuraciones
- **Puerto 8082**: Servidor estándar, respuesta completa al finalizar generación
- **Puerto 8083**: Streaming verdadero (token por token), baja latencia TTFT
- **Puerto 8084**: Consenso paralelo, múltiples expertos en paralelo con síntesis de respuestas
- Todos los servidores usan las mismas optimizaciones ARM-Axion (NEON, ACL, FP8 KV Cache, etc.)

## 📊 Rendimiento Post-Optimización

### Mejoras Logradas
- **Latencia promedio reducida**: 82.3% (de 22.62s a 4.01s)
- **Estabilidad mejorada**: 96.4% (desviación estándar reducida de 31.32s a 1.14s)
- **Velocidad aumentada**: 44.0% (de 7.63 a 10.98 tokens/segundo)
- **Bloqueos eliminados**: El servidor ya no se bloquea durante pruebas de latencia

## 🛠️ Archivos Principales del Sistema

### Servidores
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/multi_model_server.py` - Servidor estándar (respuesta completa)
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/multi_model_server_streaming.py` - Servidor con streaming verdadero (token por token)
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/multi_model_server_consensus.py` - Servidor con sistema de consenso paralelo (múltiples expertos)

### Configuración del Servidor
`/home/elect/capibara6/arm-axion-optimizations/vllm_integration/config.json`

### Scripts de Inicio y Verificación
- `/home/elect/capibara6/start_all_models_server.sh` - Iniciar servidor estándar (puerto 8082)
- `/home/elect/capibara6/start_streaming_server.sh` - Iniciar servidor con streaming (puerto 8083)
- `/home/elect/capibara6/start_consensus_server.sh` - Iniciar servidor con consenso (puerto 8084)
- `/home/elect/capibara6/test_latency_safe.py` - Prueba de latencia segura
- `/home/elect/capibara6/latency_comparison_test.py` - Comparación de rendimiento

## 🧪 Scripts de Prueba Optimizados

### 1. Prueba de Latencia Segura (`test_latency_safe.py`)
- Prueba un solo modelo a la vez
- Añade pausas entre pruebas para evitar saturación
- Maneja errores robustamente
- Monitorea tokens por segundo y latencia

### 2. Prueba de Comparación de Optimización (`latency_comparison_test.py`)
- Verifica resultados antes y después de las optimizaciones
- Calcula métricas de rendimiento
- Genera informes detallados

### 3. Script de Mejoras (`arm-axion-improvements.py`)
- Aplica optimizaciones de FP8 KV Cache
- Configura Captured Graphs
- Ajusta scheduler para minimizar latencia
- Optimiza parámetros por modelo

## 🚀 Iniciar el Servicio

1. **Iniciar el servidor**:
```bash
cd /home/elect/capibara6/arm-axion-optimizations/vllm_integration
python3 multi_model_server.py --host 0.0.0.0 --port 8082 --config config.json
```

2. **Verificar que está activo**:
```bash
curl http://localhost:8082/health
```

3. **Verificar modelos disponibles**:
```bash
curl http://localhost:8082/v1/models
```

## 🔧 Solución de Problemas

### Servidor no responde
1. Verificar que el puerto 8082 esté escuchando:
```bash
ss -tlnp | grep 8082
```

2. Verificar procesos:
```bash
ps aux | grep multi_model_server
```

3. Revisar logs:
```bash
tail -50 /tmp/multi_model_server.log
```

### Modelo tarda mucho en responder
- Normal en primera solicitud (lazy loading)
- Las siguientes solicitudes serán mucho más rápidas
- Algunos modelos grandes pueden tener tiempos de carga iniciales más largos

### Errores 500 en pruebas
- Puede indicar modelos aún no completamente cargados
- Verificar logs del servidor
- Probar modelos ya cargados (`curl http://localhost:8082/stats`)

## 📁 Archivos Importantes en el Servidor

### Directorio Principal
- `README.md` - Documentación actualizada del sistema
- `PRODUCTION_ARCHITECTURE.md` - Arquitectura distribuida
- `AYA_EXPANSE_MODEL_CONFIRMATION.md` - Documentación específica de Aya Expanse

### Directorio de Optimización ARM-Axion
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/`
  - `multi_model_server.py` - Servidor principal con optimizaciones
  - `config.json` - Configuración de los 5 expertos
  - `README.md` - Documentación técnica del servidor

### Scripts de Verificación
- `test_latency_safe.py` - Prueba segura de latencia
- `latency_comparison_test.py` - Comparación de optimización
- `compare_optimization_results.py` - Comparación antes/después

## ⚠️ No Iniciar Otros Servicios en Esta VM

No iniciar en esta VM (`models-europe`):
- `mcp_server.py` (corre en services:5003)
- `kyutai_tts_server.py` (corre en services:5002)
- `capibara6_integrated_server.py` (corre en services:5000)

---

**Última actualización**: 2025-12-02
**Versión**: ARM-Axion Optimized v2.0
**Estado**: ✅ Producción - Operativo