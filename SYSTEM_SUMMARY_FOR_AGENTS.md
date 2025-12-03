# Resumen de Archivos Principales - VM models-europe (ARM-Axion)

## Archivos Importantes que Deben Mantenerse

### Documentación Principal
- `README.md` - Documentación actualizada del sistema completo
- `AGENT_GUIDE_ARM_AXION.md` - Guía para agentes sobre optimizaciones ARM-Axion
- `PRODUCTION_ARCHITECTURE.md` - Arquitectura distribuida del sistema

### Componentes del Servidor de Modelos
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/multi_model_server.py` - Servidor estándar (respuesta completa)
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/multi_model_server_streaming.py` - Servidor con streaming verdadero (token por token)
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/config.json` - Archivo de configuración actualizado (symlink)
- `/home/elect/capibara6/arm-axion-optimizations/vllm_integration/README.md` - Documentación técnica del servidor

### Scripts de Inicio y Pruebas
- `/home/elect/capibara6/start_all_models_server.sh` - Iniciar servidor estándar (puerto 8082)
- `/home/elect/capibara6/start_streaming_server.sh` - Iniciar servidor con streaming (puerto 8083)
- `/home/elect/capibara6/start_consensus_server.sh` - Iniciar servidor con consenso (puerto 8084)
- `/home/elect/capibara6/test_latency_safe.py` - Prueba de latencia segura
- `/home/elect/capibara6/latency_comparison_test.py` - Comparación de rendimiento ARM-Axion
- `/home/elect/capibara6/compare_optimization_results.py` - Comparación antes/después de optimizaciones
- `/home/elect/capibara6/arm-axion-improvements.py` - Aplicación de optimizaciones adicionales

### Optimizaciones Específicas ARM-Axion
- `/home/elect/capibara6/arm-axion-optimizations/kernels/neon_kernels.py` - Kernels NEON optimizados
- `/home/elect/capibara6/arm-axion-optimizations/kernels/neon_matmul.cpp` - Multiplicación de matrices optimizada
- `/home/elect/capibara6/arm-axion-optimizations/kernels/acl_gemm.cpp` - GEMM con ARM Compute Library
- `/home/elect/capibara6/arm-axion-optimizations/kernels/README_ACL.md` - Documentación ACL
- `/home/elect/capibara6/arm-axion-optimizations/kernels/README_OPTIMIZATIONS.md` - Documentación optimizaciones

## Archivos Movidos a Deprecated

### Documentación Obsoleta
- `QUICK_START.md` → `docs/deprecated/OLD_QUICK_START.md`
- `README_MODELS_SETUP.md` → `docs/deprecated/`

### Scripts Antiguos
- Muchos scripts de prueba no optimizados
- Scripts de instalación antiguos
- Documentación duplicada

## 🚀 Comandos para Levantar Servicios

### Iniciar Servidor Multi-Modelo Estándar
```bash
cd /home/elect/capibara6/arm-axion-optimizations/vllm_integration
python3 multi_model_server.py --host 0.0.0.0 --port 8082 --config config.json
```

### Iniciar Servidor Multi-Modelo con Streaming Verdadero
```bash
cd /home/elect/capibara6/arm-axion-optimizations/vllm_integration
python3 multi_model_server_streaming.py --host 0.0.0.0 --port 8083 --config config.json
```

### Scripts de Inicio
- `/home/elect/capibara6/start_all_models_server.sh` - Iniciar servidor estándar (puerto 8082)
- `/home/elect/capibara6/start_streaming_server.sh` - Iniciar servidor con streaming (puerto 8083)

### Verificar Estado del Servidor
```bash
curl http://localhost:8082/health
curl http://localhost:8082/v1/models
curl http://localhost:8082/stats
```

### Prueba de Rendimiento
```bash
python3 /home/elect/capibara6/test_latency_safe.py
```

## ⚠️ Nota Importante para Agentes

Este servidor (`models-europe`) **SOLO** debe ejecutar:
- Servidor de modelos multi-experto
- Kernels de optimización ARM-Axion
- Pruebas de rendimiento no saturantes

**NO debe ejecutar**:
- Servicios MCP, TTS, backend (corren en VM `services`)
- Scripts de pruebas intensivas que sobrecarguen el sistema

---

**Última actualización**: 2025-12-02
**Responsable**: Agentes del sistema ARM-Axion Capibara6