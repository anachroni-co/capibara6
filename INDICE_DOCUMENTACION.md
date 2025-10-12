# 📚 Índice de Documentación - Capibara6

## 🚀 Inicio Rápido (Lee estos primero)

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| **`FINALIZAR_AHORA.md`** | ⭐ Guía de 3 pasos para activar todo | 15 min |
| **`RESUMEN_COMPLETO.md`** | 📊 Estado completo del sistema | 5 min lectura |
| **`ESTADO_FINAL_SISTEMA.md`** | 📋 Resumen ejecutivo | 3 min lectura |

---

## 🔧 Instalación y Deploy

### Backend (VM)
| Documento | Para qué sirve |
|-----------|----------------|
| `deploy_services_to_vm.sh` | Script principal de deploy a VM |
| `INSTALAR_PYTHON_311.md` | Instalar Python 3.11 para Coqui TTS |
| `REINICIAR_TTS_XTTS_V2.md` | Actualizar TTS a XTTS v2 (máxima calidad) |
| `CONECTAR_SSH_RAPIDO.md` | Comandos rápidos SSH a VM |
| `POST_REINICIO_VM.md` | Qué hacer después de reiniciar la VM |

### Frontend (Vercel)
| Documento | Para qué sirve |
|-----------|----------------|
| `DEPLOY_VERCEL.md` | Deploy del frontend a Vercel |
| `CONFIGURAR_VERCEL_ENV.md` | Variables de entorno en Vercel |
| `LIMPIAR_CACHE_INSTRUCCIONES.md` | Forzar actualización del cache |

---

## 🐛 Diagnóstico y Troubleshooting

| Documento | Problema que resuelve |
|-----------|----------------------|
| **`DIAGNOSTICO_MCP.md`** | ⭐ Smart MCP no se activa |
| `backend/verificar_servicios.sh` | Script para verificar todos los servicios |
| `TROUBLESHOOTING.md` | Problemas generales del sistema |
| `WEB_SPEECH_API_LIMITACIONES.md` | TTS con Web Speech API no funciona |
| `SOLUCION_TEXTBOX_DESAPARECE.md` | Textbox desaparece en móvil |

---

## 📖 Guías de Uso

### Smart MCP
| Documento | Contenido |
|-----------|-----------|
| `SMART_MCP_README.md` | Documentación completa de Smart MCP |
| `ACTIVAR_SMART_MCP_AHORA.md` | Pasos exactos para activar MCP |
| `MCP_README.md` | Versión anterior de MCP (referencia) |

### TTS (Text-to-Speech)
| Documento | Contenido |
|-----------|-----------|
| `VOCES_COQUI_TTS.md` | Todas las voces disponibles en Coqui |
| `COQUI_TTS_SETUP.md` | Setup inicial de Coqui TTS |
| `KYUTAI_TTS_README.md` | Kyutai TTS (alternativa, sin usar) |
| `TTS_OPTIONS.md` | Comparación de opciones TTS |

### Sistema de Plantillas
| Documento | Contenido |
|-----------|-----------|
| `SISTEMA_PLANTILLAS_README.md` | Documentación del sistema de plantillas |
| `COMO_PROBAR_PLANTILLAS.md` | Cómo probar las 7 plantillas |
| `RESUMEN_SISTEMA_PLANTILLAS.md` | Resumen del sistema |

### Rating y Entropía
| Documento | Contenido |
|-----------|-----------|
| `SISTEMA_EVALUACION_DETALLADO.md` | Sistema de rating completo |
| `AGREGAR_ENTROPIA.md` | Cálculo automático de entropía |
| `DEBUG_ENTROPIA.md` | Troubleshooting de entropía |

### Chatbot
| Documento | Contenido |
|-----------|-----------|
| `web/CHAT_README.md` | Documentación del chat |
| `web/CHAT_CONFIG.md` | Configuración del chatbot |
| `web/MARKDOWN_EXAMPLES.md` | Ejemplos de markdown soportado |

---

## 🏗️ Arquitectura y Desarrollo

| Documento | Contenido |
|-----------|-----------|
| `ARCHITECTURE.md` | Arquitectura del sistema |
| `API.md` | Documentación de APIs |
| `FUNCIONALIDADES_IMPLEMENTADAS.md` | Lista de features |
| `DOCS.md` | Documentación general |

---

## 📝 Documentos Técnicos

### Modelos
| Documento | Contenido |
|-----------|-----------|
| `CAMBIOS_CRITICOS_GEMMA.md` | Configuración de Gemma 3-12B |
| `INICIAR_SERVIDOR_GEMMA.md` | Cómo iniciar Gemma |
| `Gemini.md` | Integración con Gemini (referencia) |
| `Qwen.md` | Modelo Qwen (referencia) |

### Scripts de Inicio
| Documento | Contenido |
|-----------|-----------|
| `backend/start_coqui_tts_py311.sh` | Iniciar Coqui TTS con Python 3.11 |
| `backend/start_smart_mcp.sh` | Iniciar Smart MCP |
| `backend/start_kyutai_tts.sh` | Iniciar Kyutai TTS (fallback) |
| `startup.sh` | Script de inicio general |

---

## 🗂️ Organización por Tema

### 🎙️ Audio/TTS
```
VOCES_COQUI_TTS.md ← Voces disponibles
COQUI_TTS_SETUP.md ← Setup inicial
REINICIAR_TTS_XTTS_V2.md ← Actualizar a XTTS v2
KYUTAI_TTS_README.md ← Alternativa (referencia)
WEB_SPEECH_API_LIMITACIONES.md ← Limitaciones del fallback
```

### 🔍 Smart MCP / RAG
```
SMART_MCP_README.md ← Documentación completa
ACTIVAR_SMART_MCP_AHORA.md ← Activar MCP
DIAGNOSTICO_MCP.md ← Troubleshooting
ESTRATEGIA_MCP_SIMPLIFICADO.md ← Enfoque técnico
```

### 🚀 Deploy
```
deploy_services_to_vm.sh ← Deploy a VM
DEPLOY_VERCEL.md ← Deploy a Vercel
CONFIGURAR_VERCEL_ENV.md ← Variables de entorno
INSTALAR_PYTHON_311.md ← Setup Python
```

### 🧪 Testing
```
backend/verificar_servicios.sh ← Verificar servicios
DIAGNOSTICO_MCP.md ← Diagnóstico MCP
TROUBLESHOOTING.md ← Problemas generales
DEBUG_*.md ← Debugging específico
```

### 📱 Frontend
```
web/CHAT_README.md ← Chat
web/CHAT_CONFIG.md ← Configuración
SISTEMA_PLANTILLAS_README.md ← Plantillas
SISTEMA_EVALUACION_DETALLADO.md ← Rating
```

---

## 🎯 Flujo de Lectura Recomendado

### Para Usuarios Nuevos

1. `FINALIZAR_AHORA.md` ← Empezar aquí
2. `RESUMEN_COMPLETO.md` ← Entender el sistema
3. `deploy_services_to_vm.sh` ← Deploy
4. `DIAGNOSTICO_MCP.md` ← Si MCP no funciona
5. `VOCES_COQUI_TTS.md` ← Personalizar voz

### Para Desarrollo

1. `ARCHITECTURE.md` ← Arquitectura
2. `API.md` ← APIs disponibles
3. `web/CHAT_README.md` ← Frontend
4. `SMART_MCP_README.md` ← Backend MCP
5. `FUNCIONALIDADES_IMPLEMENTADAS.md` ← Features

### Para Troubleshooting

1. `DIAGNOSTICO_MCP.md` ← Si MCP no funciona
2. `backend/verificar_servicios.sh` ← Verificar servicios
3. `TROUBLESHOOTING.md` ← Problemas generales
4. `DEBUG_*.md` ← Debugging específico
5. `WEB_SPEECH_API_LIMITACIONES.md` ← Problemas de TTS

---

## 📊 Documentos por Prioridad

### ⭐⭐⭐ Críticos (Leer siempre)
- `FINALIZAR_AHORA.md`
- `RESUMEN_COMPLETO.md`
- `DIAGNOSTICO_MCP.md`

### ⭐⭐ Importantes (Leer para deploy)
- `deploy_services_to_vm.sh`
- `DEPLOY_VERCEL.md`
- `INSTALAR_PYTHON_311.md`
- `REINICIAR_TTS_XTTS_V2.md`

### ⭐ Útiles (Leer cuando necesites)
- `VOCES_COQUI_TTS.md`
- `SISTEMA_PLANTILLAS_README.md`
- `SMART_MCP_README.md`
- `TROUBLESHOOTING.md`

### 📚 Referencia (Consultar ocasionalmente)
- Todos los demás documentos

---

## 🗑️ Documentos Obsoletos (Ignorar)

Estos documentos son versiones antiguas o alternativas no usadas:

- `MCP_README.md` (reemplazado por `SMART_MCP_README.md`)
- `KYUTAI_TTS_PENDIENTE.md` (usamos Coqui TTS)
- `CONFIGURAR_KYUTAI.md` (no usamos Kyutai)
- `ERRORES_VERCEL_SOLUCIONADOS.md` (ya resueltos)
- `FIX_PYTHON_VENV.md` (ya integrado en scripts)
- Archivos `*.bat` (usamos `.sh` en la VM Linux)
- Archivos con nombres duplicados o versiones antiguas

---

## 💡 Tips de Navegación

1. **Buscar por tema:** Usa Ctrl+F en este documento
2. **Ver estructura:** Todos los `.md` están en el root, scripts en `backend/`
3. **README del proyecto:** `README.md` (español) o `README.en.md` (inglés)
4. **Documentación web:** Carpeta `web/` para frontend

---

## 🔄 Mantenimiento

Este índice debería actualizarse cuando:
- Se agreguen nuevas guías importantes
- Se deprecen documentos antiguos
- Cambien las prioridades del sistema

**Última actualización:** 12 Oct 2025  
**Versión:** v2.0  
**Total de documentos:** ~90+ archivos `.md`

