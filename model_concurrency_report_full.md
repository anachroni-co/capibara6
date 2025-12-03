# Pruebas de Concurrencia por Modelo

Este informe detalla las pruebas de concurrencia realizadas para cada modelo disponible en el servidor `multi_model_server`.

## Modelo: phi4_fast

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 6 | 6 | 0 | 0 | 1.62 | 32.2% | 32.2% |
| 2 | 12 | 12 | 0 | 0 | 1.74 | 32.2% | 32.2% |
| 4 | 17 | 17 | 0 | 0 | 3.60 | 32.2% | 32.2% |
| 8 | 21 | 21 | 0 | 0 | 9.02 | 32.2% | 32.2% |
| 12 | 25 | 25 | 0 | 0 | 13.61 | 32.2% | 32.2% |
| 16 | 29 | 29 | 0 | 0 | 17.90 | 32.2% | 32.2% |
| 20 | 33 | 33 | 0 | 0 | 21.77 | 32.2% | 32.2% |

### Conclusión para phi4_fast:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **20.4** solicitudes por prueba

## Modelo: mistral_balanced

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 5 | 5 | 0 | 0 | 2.52 | 47.1% | 47.1% |
| 2 | 10 | 10 | 0 | 0 | 2.78 | 47.1% | 47.1% |
| 4 | 12 | 12 | 0 | 0 | 7.06 | 47.1% | 47.2% |
| 8 | 16 | 16 | 0 | 0 | 14.58 | 47.2% | 47.2% |
| 12 | 20 | 20 | 0 | 0 | 21.07 | 47.2% | 47.2% |
| 16 | 24 | 24 | 0 | 0 | 27.07 | 47.2% | 47.1% |
| 20 | 25 | 25 | 0 | 0 | 31.08 | 47.1% | 47.1% |

### Conclusión para mistral_balanced:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **16.0** solicitudes por prueba

## Modelo: qwen_coder

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 7 | 7 | 0 | 0 | 0.94 | 53.6% | 53.7% |
| 2 | 14 | 14 | 0 | 0 | 1.03 | 53.7% | 53.7% |
| 4 | 26 | 26 | 0 | 0 | 1.17 | 53.7% | 53.7% |
| 8 | 31 | 31 | 0 | 0 | 4.44 | 53.7% | 53.7% |
| 12 | 35 | 35 | 0 | 0 | 7.59 | 53.7% | 53.7% |
| 16 | 39 | 39 | 0 | 0 | 10.33 | 53.7% | 53.6% |
| 20 | 43 | 43 | 0 | 0 | 13.15 | 53.6% | 53.6% |

### Conclusión para qwen_coder:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **27.9** solicitudes por prueba

## Modelo: gemma3_multimodal

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 9 | 0 | 9 | 0 | 0.00 | 53.6% | 53.6% |
| 2 | 18 | 0 | 18 | 0 | 0.00 | 53.6% | 53.6% |
| 4 | 36 | 0 | 36 | 0 | 0.00 | 53.6% | 53.7% |
| 8 | 72 | 0 | 72 | 0 | 0.00 | 53.7% | 53.7% |
| 12 | 108 | 0 | 108 | 0 | 0.00 | 53.7% | 53.7% |
| 16 | 144 | 0 | 144 | 0 | 0.00 | 53.7% | 53.7% |
| 20 | 180 | 0 | 180 | 0 | 0.00 | 53.7% | 53.7% |

### Conclusión para gemma3_multimodal:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **0.0** solicitudes por prueba

## Modelo: aya_expanse_multilingual

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 5 | 5 | 0 | 0 | 2.91 | 71.0% | 71.0% |
| 2 | 9 | 9 | 0 | 0 | 3.26 | 71.0% | 71.0% |
| 4 | 11 | 11 | 0 | 0 | 8.16 | 71.0% | 71.0% |
| 8 | 15 | 15 | 0 | 0 | 16.60 | 71.0% | 71.0% |
| 12 | 19 | 19 | 0 | 0 | 23.71 | 71.0% | 71.0% |
| 16 | 20 | 20 | 0 | 0 | 28.57 | 71.0% | 71.0% |
| 20 | 20 | 19 | 0 | 1 | 33.27 | 71.0% | 71.0% |

### Conclusión para aya_expanse_multilingual:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **14.0** solicitudes por prueba

## Resumen General

Las pruebas de concurrencia se realizaron con el objetivo de determinar:

- El número máximo de usuarios concurrentes que puede manejar cada modelo sin exceder el 90% de uso de RAM
- El rendimiento del modelo bajo carga concurrente
- El tiempo promedio de respuesta bajo diferentes niveles de concurrencia

### Metodología

- Duración de cada prueba: 25 segundos
- Intervalo entre solicitudes: 3 segundos
- Timeout de solicitud: 60 segundos
- Cada usuario envía solicitudes concurrentes al mismo modelo
- Se monitorea el uso de memoria durante todas las pruebas

### Configuración del Servidor

- Configuración ligera con lazy loading activado
- Optimizaciones ARM Axion aplicadas
- Uso de CPU (no GPU) para inferencia

