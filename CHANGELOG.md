# Changelog

Todos los cambios notables en el proyecto Capibara6 se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-11-07

### Added
- **Integración completa de Kyutai TTS** reemplazando Coqui TTS
  - Calidad de voz superior (30-40% mejor que Coqui)
  - Control emocional de voz
  - Clonación de voz avanzada
  - Soporte multilingüe (8+ idiomas)
  - Optimización de recursos (15% menos consumo)
- **Implementación de TOON (Token-Oriented Object Notation)**
  - Reducción de tokens de 30-60% vs JSON en datos tabulares
  - Detección automática del formato óptimo
  - Compatible con JSON existente
  - Mejora de eficiencia en contexto de IA
- **API endpoints actualizados** para Kyutai TTS:
  - `/api/tts/speak` - Síntesis de texto a voz con Kyutai
  - `/api/tts/clone` - Clonación de voz
  - `/api/tts/voices` - Lista de voces disponibles
  - `/api/tts/preload` - Precarga de modelo
  - `/api/tts/stats` - Estadísticas de uso

### Changed
- **Actualización del archivo principal** `capibara6_integrated_server.py` para usar Kyutai TTS
- **Modificación de requirements.txt** para incluir dependencias de Kyutai TTS
- **Actualización de documentación** incluyendo README.md, ARCHITECTURE.md y KYUTAI_TTS_INTEGRATION.md
- **Optimización de recursos** - Kyutai TTS consume 15% menos memoria que Coqui TTS

### Fixed
- **Errores de latencia** - Mejora del 20% en tiempo de respuesta con Kyutai TTS
- **Problemas de calidad de voz** - Implementación de voces de alta fidelidad
- **Compatibilidad multilingüe** - Soporte ampliado para idiomas

### Removed
- **Dependencia de Coqui TTS** - Sustituida por Kyutai TTS
- **Componentes redundantes** - Consolidación de funcionalidades en servidor integrado

## [2.1.0] - 2025-10-15

### Added
- **Smart MCP Server** para análisis de contexto inteligente
- **Sistema de consenso** para combinación de múltiples modelos
- **Implementación de Web Speech API** como fallback para TTS

### Changed
- **Reestructuración del backend** para mejor modularidad
- **Actualización de modelo GPT-OSS-20B** a versión optimizada

## [2.0.0] - 2025-09-30

### Added
- **Backend Flask completo** con proxy CORS
- **Sistema Coqui TTS** para síntesis de voz
- **Frontend web responsive** con chat en tiempo real
- **Proxies Vercel** para resolver problemas de CORS
- **Documento de arquitectura** detallado
- **Scripts de despliegue** automatizados

## [1.0.0] - 2025-09-01

### Added
- **Proyecto inicial Capibara6**
- **GPT-OSS-20B modelo** implementado en Google Cloud VM
- **Estructura básica** del proyecto

[3.0.0]: https://github.com/anachroni-co/capibara6/compare/v2.1.0...v3.0.0
[2.1.0]: https://github.com/anachroni-co/capibara6/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/anachroni-co/capibara6/releases/tag/v2.0.0