# 🔥 Configuración de Firewall - VM rag3

## ✅ Puertos Abiertos según Firewall

| Puerto | Servicio | Regla de Firewall | Estado |
|--------|----------|-------------------|--------|
| **5000** | Capibara6 Integrated Server | `allow-capibara6-port5000`, `allow-capibara6-main` | ✅ ABIERTO |
| **5001** | Kyutai TTS Server | `allow-kyutai-tts` | ✅ ABIERTO |
| **8080** | llama.cpp Server / CapibaraGPT-v2 GUI | `allow-llama-server-8080`, `allow-capibara-gui` | ✅ ABIERTO |
| **11434** | Ollama API | `allow-ollama` | ✅ ABIERTO |
| **443** | HTTPS | `default-allow-https`, `allow-capibara6-https` | ✅ ABIERTO |
| **22** | SSH | `allow-ssh` | ✅ ABIERTO |
| **7001** | Nebula Graph Studio | `allow-nebula-studio` | ✅ ABIERTO |

## ❌ Puertos NO Abiertos (según firewall)

- **8000** - RAG API (NO hay regla, necesita añadirse o usar otro puerto)

## 🔍 Observaciones

La VM rag3 tiene servicios similares a gpt-oss-20b:
- ✅ Ollama en puerto 11434
- ✅ Capibara6 Integrated Server en puerto 5000
- ✅ llama.cpp Server en puerto 8080
- ✅ Kyutai TTS en puerto 5001
- ✅ Nebula Graph Studio en puerto 7001

**Nota**: No hay puerto 8000 abierto para RAG API. Posibles opciones:
1. Añadir regla de firewall para puerto 8000
2. Usar el puerto 5000 (Capibara6 Integrated Server) que ya está abierto
3. Verificar si RAG está corriendo en otro puerto

## 📝 Cambios Necesarios

1. Actualizar configuración de RAG para usar puerto disponible (5000 o verificar)
2. Obtener IP externa de rag3
3. Verificar qué servicio RAG está realmente corriendo

