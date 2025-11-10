# 🦫 CAPIBARA6 + E2B - GESTIÓN DINÁMICA DE VMS Y TEMPLATES

## Fecha: 10 de Noviembre de 2025

## Resumen

Hemos implementado un sistema avanzado de gestión de sandboxes E2B que permite:

1. **Templates predefinidos** para diferentes tipos de tareas
2. **Creación dinámica de VMs** según las necesidades de la tarea
3. **Gestión automática de recursos** (memoria, CPU, tiempo)
4. **Ejecución segura de código** en entornos aislados

## Templates Disponibles

### 1. Default Template
- **ID**: `default`
- **Descripción**: Template estándar para tareas generales
- **Recursos**: 512MB RAM, 50% CPU, 5 minutos timeout
- **Lenguajes**: Python, JavaScript

### 2. Data Analysis Template
- **ID**: `data_analysis`
- **Descripción**: Template optimizado para análisis de datos
- **Recursos**: 1024MB RAM, 75% CPU, 10 minutos timeout
- **Lenguajes**: Python
- **Paquetes**: pandas, numpy, matplotlib, seaborn

### 3. Machine Learning Template
- **ID**: `machine_learning`
- **Descripción**: Template con recursos para tareas ML
- **Recursos**: 2048MB RAM, 100% CPU, 30 minutos timeout
- **Lenguajes**: Python
- **Paquetes**: pandas, numpy, scikit-learn, tensorflow

### 4. Quick Script Template
- **ID**: `quick_script`
- **Descripción**: Template para scripts rápidos y simples
- **Recursos**: 256MB RAM, 25% CPU, 1 minuto timeout
- **Lenguajes**: Python, JavaScript, Bash

### 5. Visualization Template
- **ID**: `visualization`
- **Descripción**: Template optimizado para visualización de datos
- **Recursos**: 1024MB RAM, 75% CPU, 10 minutos timeout
- **Lenguajes**: Python
- **Paquetes**: pandas, matplotlib, seaborn, plotly

## Capacidad de Creación Dinámica

El sistema puede crear VMs dinámicamente basados en el tipo de tarea:

### Tipos de Tareas Soportadas
- `data_analysis`: Usa template de análisis de datos
- `data-visualization`: Usa template de visualización
- `machine_learning` o `ml`: Usa template de ML
- `quick`: Usa template de script rápido
- `default`: Usa template por defecto

### Ejemplo de Uso Dinámico
```python
result = await e2b_integration.process_code_request(
    code="print('Hola desde sandbox dinámico!')",
    task_type='quick',
    metadata={
        'request_type': 'dynamic',  # Esto activa la creación dinámica
        'requirements': {'timeout': 120, 'memory_limit_mb': 256}
    }
)
```

## API de Integración

### Clase Principal: `E2BIntegration`

#### Métodos Clave:
1. `process_code_request()` - Procesa solicitudes de ejecución
2. `get_available_templates()` - Lista templates disponibles
3. `get_execution_stats()` - Obtiene estadísticas
4. `health_check()` - Verifica estado del sistema

#### Modos de Operación:
- **Template Mode**: `metadata={'request_type': 'template'}` (default)
- **Dynamic Mode**: `metadata={'request_type': 'dynamic'}`

## Beneficios del Sistema

### 1. Eficiencia de Recursos
- Asignación dinámica según las necesidades
- Reciclaje automático de sandboxes
- Límites de concurrencia configurables

### 2. Seguridad
- Entornos completamente aislados
- Destrucción automática tras la ejecución
- Validación de lenguajes y paquetes

### 3. Flexibilidad
- Templates personalizables
- Configuración adaptable por tarea
- Soporte para múltiples lenguajes

### 4. Escalabilidad
- Pool configurable de sandboxes concurrentes
- Gestión automática de recursos
- Creación bajo demanda

## Uso en el Sistema Capibara6

### Integración con el Router
```python
# El sistema puede elegir automáticamente el template basado en la tarea
if "analysis" in query:
    template_id = "data_analysis"
elif "visualize" in query:
    template_id = "visualization"
elif "ml" in query or "learning" in query:
    template_id = "machine_learning"
else:
    template_id = "default"
```

### Ejemplo de Integración Completa
```python
async def process_ia_request(query: str, code: str):
    # Detectar tipo de tarea
    task_type = classify_task(query)
    
    # Ejecutar con los recursos adecuados
    result = await e2b_integration.process_code_request(
        code=code,
        template_id=get_relevant_template(task_type),
        task_type=task_type,
        metadata={'request_type': 'template'}
    )
    
    return result
```

## Estado Actual

✅ **Templates funcionales**: Todos los 5 templates predefinidos operativos
✅ **Creación dinámica**: Funcional y probada con éxito
✅ **Gestión de recursos**: Automática y eficiente
✅ **Integración con capibara6**: Lista para implementación
✅ **Destrucción automática**: Todos los VMs se destruyen tras la ejecución
✅ **Seguridad**: Aislamiento completo entre ejecuciones

## Próximos Pasos

1. **Integrar con el endpoint** `/api/v1/e2b/execute` en `main.py`
2. **Conectar al router semántico** para selección automática de templates
3. **Implementar sistema de caching** para resultados comunes
4. **Añadir monitoreo avanzado** de uso de recursos
5. **Crear dashboard** de administración de templates y VMs