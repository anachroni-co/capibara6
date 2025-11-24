# 🔥 Configuración de Firewall - VM bounty2

## ✅ Puertos Abiertos según Firewall

| Puerto | Servicio | Regla de Firewall | Estado |
|--------|----------|-------------------|--------|
| **5000** | Capibara6 Integrated Server | `allow-capibara6-port5000` | ✅ ABIERTO |
| **5002** | Coqui TTS Server | `allow-coqui-tts` | ✅ ABIERTO |
| **8080** | Gemma Model Server / CapibaraGPT-v2 GUI | `allow-gemma-model`, `allow-capibara-gui` | ✅ ABIERTO |
| **7001** | Nebula Graph Studio | `allow-nebula-studio` | ✅ ABIERTO |
| **80** | HTTP | `allow-http-llama` | ✅ ABIERTO |
| **22** | SSH | `allow-ssh` | ✅ ABIERTO |
| **8470** | TPU interno | `allow-internal-tpu` (solo 10.0.0.0/8) | 🔒 INTERNO |
| **9230** | TPU healthcheck | Rangos específicos de Google | 🔒 GOOGLE |
| **12355** | TPU coordination | Solo 10.128.0.0/20 | 🔒 INTERNO |

## ❌ Puertos NO Abiertos Externamente

- **5001** - Backend Flask (NO hay regla, usar 5000 en su lugar)
- **11434** - Ollama API (NO está abierto externamente, solo acceso interno)

## 🔍 Observaciones Importantes

1. **Backend**: El puerto **5000** está abierto, no el 5001. El backend debería estar en 5000.
2. **Ollama**: El puerto **11434** NO está abierto externamente. Solo accesible desde:
   - Red interna (10.0.0.0/8)
   - Otras VMs en la misma VPC
3. **TTS**: Puerto **5002** (Coqui TTS) está abierto, no 5001.

## 📝 Cambios Necesarios

1. Actualizar backend URL de puerto 5001 → 5000
2. Ollama solo accesible internamente (no desde frontend directamente)
3. TTS en bounty2 usa puerto 5002 (Coqui), no 5001

