# Pruebas de Concurrencia por Modelo

Este informe detalla las pruebas de concurrencia realizadas para cada modelo disponible en el servidor `multi_model_server`.

## Modelo: phi4_fast

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 6 | 6 | 0 | 0 | 1.58 | 14.0% | 14.0% |
| 2 | 12 | 12 | 0 | 0 | 1.73 | 14.0% | 14.0% |
| 4 | 17 | 17 | 0 | 0 | 3.53 | 14.0% | 14.0% |
| 8 | 21 | 21 | 0 | 0 | 8.85 | 14.0% | 14.0% |
| 12 | 25 | 25 | 0 | 0 | 13.49 | 14.0% | 14.0% |
| 16 | 29 | 29 | 0 | 0 | 17.59 | 14.0% | 14.0% |
| 20 | 33 | 33 | 0 | 0 | 22.19 | 14.0% | 14.0% |

### Conclusión para phi4_fast:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **20.4** solicitudes por prueba

## Modelo: qwen_coder

| Usuarios | Solicitudes | Éxito | Errores | Timeouts | Tiempo Resp. (s) | Memoria Inicial | Memoria Final |
|----------|-------------|-------|---------|----------|-------------------|-----------------|---------------|
| 1 | 7 | 7 | 0 | 0 | 0.95 | 20.5% | 20.5% |
| 2 | 14 | 14 | 0 | 0 | 1.02 | 20.5% | 20.5% |
| 4 | 26 | 26 | 0 | 0 | 1.12 | 20.5% | 20.5% |
| 8 | 31 | 31 | 0 | 0 | 4.47 | 20.5% | 20.5% |
| 12 | 35 | 35 | 0 | 0 | 7.40 | 20.5% | 20.5% |
| 16 | 39 | 39 | 0 | 0 | 10.18 | 20.5% | 20.5% |
| 20 | 43 | 43 | 0 | 0 | 12.87 | 20.5% | 20.5% |

### Conclusión para qwen_coder:
- Número máximo seguro de usuarios concurrentes: **20**
- Tasa promedio de éxito: **27.9** solicitudes por prueba

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

