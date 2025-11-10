#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced E2B Integration Module for Capibara6
Módulo avanzado de integración con E2B para ejecución segura de código generado por IA
con gestión dinámica de recursos y templates
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json

# Importar desde el módulo archivado como base
import sys
sys.path.insert(0, '/home/elect/capibara6/archived/backend_modules')
from execution.e2b_manager import E2BManager as BaseE2BManager

# Importar E2B SDK
from e2b_code_interpreter import AsyncSandbox

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class E2BTemplate:
    """Representa una plantilla de sandbox E2B con configuración predefinida"""
    
    def __init__(self, template_id: str, config: Dict[str, Any]):
        self.template_id = template_id
        self.config = config  # timeout, memory, cpu, etc.
        self.name = config.get('name', template_id)
        self.description = config.get('description', 'Template without description')
        self.supported_languages = config.get('supported_languages', ['python'])
        self.created_at = datetime.now()
    
    def get_sandbox_config(self) -> Dict[str, Any]:
        """Obtiene la configuración para crear un sandbox basado en esta plantilla"""
        return {
            'timeout': self.config.get('timeout', 300),
            'memory_limit_mb': self.config.get('memory_limit_mb', 512),
            'cpu_limit_percent': self.config.get('cpu_limit_percent', 50),
            'template_name': self.config.get('template_name', 'code-interpreter-v1')
        }


class AdvancedE2BManager(BaseE2BManager):
    """Gestor avanzado de E2B con soporte para templates y gestión dinámica de VMs"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # Usar la API key de entorno si no se proporciona
        api_key = api_key or os.getenv("E2B_API_KEY")
        if not api_key:
            raise ValueError("E2B_API_KEY no encontrada en variables de entorno")
        
        # Configurar templates predefinidos
        self.templates = self._initialize_templates()
        
        # Inicializar con configuración extendida
        super().__init__(
            api_key=api_key,
            **kwargs
        )
        
        self.api_key = api_key
        logger.info("AdvancedE2BManager inicializado con soporte para templates")
    
    def _initialize_templates(self) -> Dict[str, E2BTemplate]:
        """Inicializa templates predefinidos para diferentes tipos de tareas"""
        templates = {
            'default': E2BTemplate('default', {
                'name': 'Default Template',
                'description': 'Template estándar para tareas generales',
                'timeout': 300,  # 5 minutos
                'memory_limit_mb': 512,
                'cpu_limit_percent': 50,
                'supported_languages': ['python', 'javascript'],
                'template_name': 'code-interpreter-v1'
            }),
            'data_analysis': E2BTemplate('data_analysis', {
                'name': 'Data Analysis Template',
                'description': 'Template optimizado para análisis de datos',
                'timeout': 600,  # 10 minutos
                'memory_limit_mb': 1024,  # 1GB
                'cpu_limit_percent': 75,
                'supported_languages': ['python'],
                'template_name': 'code-interpreter-v1',
                'packages': ['pandas', 'numpy', 'matplotlib', 'seaborn']
            }),
            'machine_learning': E2BTemplate('machine_learning', {
                'name': 'Machine Learning Template',
                'description': 'Template con recursos para tareas ML',
                'timeout': 1800,  # 30 minutos
                'memory_limit_mb': 2048,  # 2GB
                'cpu_limit_percent': 100,
                'supported_languages': ['python'],
                'template_name': 'code-interpreter-v1',
                'packages': ['pandas', 'numpy', 'scikit-learn', 'matplotlib', 'seaborn', 'tensorflow']
            }),
            'quick_script': E2BTemplate('quick_script', {
                'name': 'Quick Script Template',
                'description': 'Template para scripts rápidos y simples',
                'timeout': 60,   # 1 minuto
                'memory_limit_mb': 256,
                'cpu_limit_percent': 25,
                'supported_languages': ['python', 'javascript', 'bash'],
                'template_name': 'code-interpreter-v1'
            }),
            'visualization': E2BTemplate('visualization', {
                'name': 'Visualization Template',
                'description': 'Template optimizado para visualización de datos',
                'timeout': 600,  # 10 minutos
                'memory_limit_mb': 1024,
                'cpu_limit_percent': 75,
                'supported_languages': ['python'],
                'template_name': 'code-interpreter-v1',
                'packages': ['pandas', 'matplotlib', 'seaborn', 'plotly']
            })
        }
        
        logger.info(f"Templates inicializados: {list(templates.keys())}")
        return templates
    
    def get_template(self, template_id: str) -> Optional[E2BTemplate]:
        """Obtiene un template por ID"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[str]:
        """Lista todos los templates disponibles"""
        return list(self.templates.keys())
    
    async def execute_with_template(self, 
                                  code: str, 
                                  template_id: str = 'default',
                                  custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ejecuta código usando un template específico
        
        Args:
            code: Código a ejecutar
            template_id: ID del template a usar
            custom_config: Configuración personalizada que sobreescribe el template
            
        Returns:
            Dict: Resultados de la ejecución
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' no encontrado")
        
        # Combinar configuración del template con configuración personalizada
        config = template.get_sandbox_config()
        if custom_config:
            config.update(custom_config)
        
        # Detectar lenguaje del código si no está especificado
        language = self._detect_language(code)
        
        logger.info(f"Usando template '{template_id}' para ejecutar código en {language}")
        
        # Ejecutar código con la configuración del template
        result = await self.execute_code(
            code=code,
            language=language,
            timeout=config['timeout'],
            memory_limit_mb=config['memory_limit_mb'],
            cpu_limit_percent=config['cpu_limit_percent']
        )
        
        result['template_used'] = template_id
        result['template_config'] = config
        
        return result
    
    def _detect_language(self, code: str) -> str:
        """Detecta el lenguaje de programación del código"""
        code_lower = code.lower().strip()
        
        if code_lower.startswith('import pandas') or code_lower.startswith('import numpy'):
            return 'python'
        elif 'console.log' in code_lower or 'function' in code_lower:
            return 'javascript'
        elif code_lower.startswith('select') or code_lower.startswith('insert') or code_lower.startswith('update'):
            return 'sql'
        elif code_lower.startswith('#!') or 'echo' in code_lower:
            return 'bash'
        
        # Por defecto, asumir Python
        return 'python'
    
    async def create_dynamic_sandbox(self, 
                                   task_type: str,
                                   requirements: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Crea un sandbox dinámicamente basado en el tipo de tarea
        
        Args:
            task_type: Tipo de tarea ('data_analysis', 'ml', 'quick', etc.)
            requirements: Requisitos específicos para el sandbox
            
        Returns:
            Dict: Información del sandbox creado
        """
        # Mapear tipos de tarea a templates
        task_to_template = {
            'data_analysis': 'data_analysis',
            'data-visualization': 'visualization',
            'machine_learning': 'machine_learning',
            'ml': 'machine_learning',
            'quick': 'quick_script',
            'default': 'default'
        }
        
        template_id = task_to_template.get(task_type, 'default')
        template = self.get_template(template_id)
        
        if not template:
            template = self.get_template('default')
            template_id = 'default'
        
        # Aplicar requisitos personalizados
        config = template.get_sandbox_config()
        if requirements:
            config.update(requirements)
        
        # Crear sandbox con configuración dinámica
        sandbox_key = f"{task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(self)}"
        
        # Crear sandbox real usando la API de E2B directamente
        try:
            e2b_sandbox = await AsyncSandbox.create(
                api_key=self.api_key,
                template=config['template_name'],
                timeout=config['timeout']
            )
            
            sandbox_info = {
                'sandbox_id': e2b_sandbox.sandbox_id,
                'task_type': task_type,
                'template_used': template_id,
                'configuration': config,
                'created_at': datetime.now().isoformat(),
                'sandbox_instance': e2b_sandbox
            }
            
            logger.info(f"Sandbox dinámico creado: {sandbox_info['sandbox_id']} para {task_type}")
            return sandbox_info
            
        except Exception as e:
            logger.error(f"Error creando sandbox dinámico: {e}")
            return {
                'error': str(e),
                'task_type': task_type,
                'template_used': template_id,
                'configuration': config
            }
    
    async def execute_with_dynamic_sandbox(self, 
                                         code: str, 
                                         task_type: str = 'default',
                                         requirements: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Ejecuta código en un sandbox creado dinámicamente según el tipo de tarea
        """
        start_time = datetime.now()
        
        # Crear sandbox dinámico
        sandbox_info = await self.create_dynamic_sandbox(task_type, requirements)
        
        if 'error' in sandbox_info:
            return {
                'success': False,
                'error': sandbox_info['error'],
                'execution_time': (datetime.now() - start_time).total_seconds()
            }
        
        # Ejecutar código en el sandbox
        try:
            execution_result = await sandbox_info['sandbox_instance'].run_code(code)
            
            # Preparar resultado
            result = {
                'success': not execution_result.error,
                'sandbox_id': sandbox_info['sandbox_id'],
                'task_type': task_type,
                'template_used': sandbox_info['template_used'],
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'logs': {
                    'stdout': [line.rstrip() for line in execution_result.logs.stdout] if execution_result.logs.stdout else [],
                    'stderr': [line.rstrip() for line in execution_result.logs.stderr] if execution_result.logs.stderr else []
                },
                'result': [str(r) for r in execution_result.results] if execution_result.results else [],
                'error': str(execution_result.error) if execution_result.error else None,
                'timestamp': datetime.now().isoformat()
            }
            
            # Actualizar estadísticas
            self._update_execution_stats(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error ejecutando código en sandbox dinámico: {e}")
            return {
                'success': False,
                'error': str(e),
                'sandbox_id': sandbox_info['sandbox_id'],
                'task_type': task_type,
                'execution_time': (datetime.now() - start_time).total_seconds()
            }
        finally:
            # Siempre destruir el sandbox después de la ejecución
            try:
                await sandbox_info['sandbox_instance'].kill()
                logger.info(f"Sandbox destruido: {sandbox_info['sandbox_id']}")
            except Exception as e:
                logger.error(f"Error destruyendo sandbox: {e}")


class E2BIntegration:
    """Integración completa de E2B para el sistema capibara6 con templates y gestión dinámica"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializa la integración E2B avanzada"""
        self.e2b_manager = AdvancedE2BManager(api_key)
        logger.info("E2BIntegration avanzada inicializado")
    
    async def process_code_request(self, 
                                 code: str, 
                                 template_id: str = 'default',
                                 task_type: str = 'default',
                                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una solicitud de ejecución de código con posibilidad de usar templates o creación dinámica
        """
        metadata = metadata or {}
        request_type = metadata.get('request_type', 'template')  # 'template' o 'dynamic'
        
        if request_type == 'dynamic':
            # Usar creación dinámica de sandbox
            return await self.e2b_manager.execute_with_dynamic_sandbox(
                code=code,
                task_type=task_type,
                requirements=metadata.get('requirements')
            )
        else:
            # Usar template predefinido
            return await self.e2b_manager.execute_with_template(
                code=code,
                template_id=template_id,
                custom_config=metadata.get('custom_config')
            )
    
    async def get_available_templates(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de templates disponibles"""
        templates_info = []
        for template_id in self.e2b_manager.list_templates():
            template = self.e2b_manager.get_template(template_id)
            if template:
                templates_info.append({
                    'id': template.template_id,
                    'name': template.name,
                    'description': template.description,
                    'supported_languages': template.supported_languages,
                    'config': template.get_sandbox_config()
                })
        return templates_info
    
    async def get_execution_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de ejecución"""
        return self.e2b_manager.get_stats()
    
    async def health_check(self) -> Dict[str, Any]:
        """Realiza un health check del sistema E2B"""
        try:
            # Probar conexión con un comando simple
            result = await self.e2b_manager.execute_with_template(
                code="print('E2B connection OK')", 
                template_id='quick_script'
            )
            
            return {
                'status': 'healthy' if result['success'] else 'unhealthy',
                'api_key_valid': bool(self.e2b_manager.api_key),
                'test_execution': result,
                'timestamp': datetime.now().isoformat(),
                'templates_available': await self.get_available_templates()
            }
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def cleanup(self):
        """Limpia recursos"""
        await self.e2b_manager.cleanup()


# Función de ejemplo para probar la integración avanzada
async def advanced_example_usage():
    """Ejemplo de uso del sistema E2B avanzado con templates y creación dinámica"""
    
    # Inicializar la integración
    e2b_integration = E2BIntegration()
    
    # 1. Listar templates disponibles
    print("1. Templates disponibles:")
    templates = await e2b_integration.get_available_templates()
    for template in templates:
        print(f"   - {template['name']}: {template['description']}")
    
    # 2. Ejecutar con template estándar
    print("\n2. Ejecutando con template 'data_analysis'...")
    result1 = await e2b_integration.process_code_request(
        code="""
import pandas as pd
import numpy as np

# Crear datos de ejemplo
data = {'value': np.random.randn(100)}
df = pd.DataFrame(data)

print(f"Dataset shape: {df.shape}")
print(f"Mean: {df['value'].mean():.2f}")
print(f"Std: {df['value'].std():.2f}")
""",
        template_id='data_analysis',
        metadata={'request_type': 'template'}
    )
    
    print(f"Resultado: {result1['success']}")
    
    # 3. Ejecutar con creación dinámica de sandbox
    print("\n3. Ejecutando con sandbox dinámico...")
    result2 = await e2b_integration.process_code_request(
        code="print('Hola desde sandbox dinámico!')",
        task_type='quick',
        metadata={
            'request_type': 'dynamic',
            'requirements': {'timeout': 120, 'memory_limit_mb': 256}
        }
    )
    
    print(f"Resultado sandbox dinámico: {result2['success']}")
    
    # 4. Ejecutar análisis de datos complejo
    print("\n4. Ejecutando análisis complejo...")
    result3 = await e2b_integration.process_code_request(
        code="""
import numpy as np
import matplotlib.pyplot as plt

# Generar datos
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10)

print(f'Seno amortiguado generado: {len(x)} puntos')
print(f'Valor máximo: {y.max():.3f}')
print(f'Valor mínimo: {y.min():.3f}')

# Crear gráfico
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Seno Amortiguado')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.savefig('/home/user/amortiguado.png')
print('Gráfico guardado como amortiguado.png')
""",
        template_id='visualization',
        metadata={'request_type': 'template'}
    )
    
    print(f"Resultado análisis complejo: {result3['success']}")
    
    # Mostrar estadísticas
    print("\n5. Estadísticas de ejecución:")
    stats = await e2b_integration.get_execution_stats()
    print(f"   Total ejecuciones: {stats['execution_stats']['total_executions']}")
    print(f"   Éxito: {stats['execution_stats']['successful_executions']}")
    print(f"   Tasa de éxito: {stats['success_rate']:.2%}")
    
    # Health check
    print("\n6. Health check:")
    health = await e2b_integration.health_check()
    print(f"   Estado: {health['status']}")
    
    # Limpieza
    await e2b_integration.cleanup()
    print("\n7. Recursos limpiados")


if __name__ == "__main__":
    print("🧪 Iniciando ejemplo de integración E2B avanzada...")
    asyncio.run(advanced_example_usage())
    print("✅ Ejemplo avanzado completado")