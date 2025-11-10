#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test E2B Integration - Prueba del sistema E2B con los modelos de IA
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Añadir el directorio backend al path para importar módulos
sys.path.insert(0, '/home/elect/capibara6/backend')

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Verificar que la API key de E2B está configurada
E2B_API_KEY = os.getenv('E2B_API_KEY')
if not E2B_API_KEY or E2B_API_KEY.startswith('e2b_') and len(E2B_API_KEY) > 10:
    logger.info(f"E2B API Key está configurada: {E2B_API_KEY[:15]}...")
else:
    logger.warning("E2B API Key no está configurada correctamente")

async def test_basic_e2b_functionality():
    """Prueba básica de funcionalidad E2B"""
    logger.info("=== Iniciando prueba de funcionalidad E2B ===")
    
    try:
        # Intentar importar E2BIntegration
        from execution.e2b_integration import E2BIntegration
        logger.info("✅ E2BIntegration importado correctamente")
        
        # Crear una instancia
        integration = E2BIntegration()
        logger.info("✅ E2BIntegration inicializado correctamente")
        
        # Mostrar estadísticas iniciales
        stats = integration.get_integration_stats()
        logger.info(f"📊 Estadísticas iniciales: {stats}")
        
        return integration
        
    except ImportError as e:
        logger.error(f"❌ Error importando E2BIntegration: {e}")
        # Buscar en otra ubicación
        try:
            sys.path.insert(0, '/home/elect/capibara6/archived/backend_modules')
            from execution.e2b_integration import E2BIntegration
            logger.info("✅ E2BIntegration importado desde archived")
            
            integration = E2BIntegration()
            logger.info("✅ E2BIntegration inicializado correctamente")
            
            return integration
        except ImportError as e2:
            logger.error(f"❌ Error importando E2BIntegration desde archived: {e}")
            return None
    except Exception as e:
        logger.error(f"❌ Error inicializando E2BIntegration: {e}")
        return None

async def test_code_execution(integration):
    """Prueba de ejecución de código con E2B"""
    logger.info("\n=== Prueba de ejecución de código ===")
    
    if not integration:
        logger.error("❌ No hay integración E2B disponible para pruebas")
        return False
    
    # Código de prueba
    test_code = """
import sys
print("Hola desde el sandbox E2B!")
print(f"Python version: {sys.version}")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
    
    try:
        # Ejecutar código de prueba
        result = await integration.execute_code_directly(
            code=test_code,
            language="python",
            context="Prueba de conexión E2B",
            user_intent="Test execution"
        )
        
        logger.info(f"Resultado de ejecución: {result}")
        
        if result.get('success'):
            logger.info("✅ Ejecución de código exitosa")
            return True
        else:
            logger.warning(f"⚠️  Ejecución fallida: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error ejecutando código: {e}")
        return False

async def test_code_analysis(integration):
    """Prueba de análisis de código"""
    logger.info("\n=== Prueba de análisis de código ===")
    
    if not integration:
        logger.error("❌ No hay integración E2B disponible para análisis")
        return False
    
    # Texto con código para analizar
    text_with_code = """
    Aquí tienes una función en Python:
    
    ```python
    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)
    
    print(fibonacci(10))
    ```
    
    También puedes usar JavaScript:
    
    ```javascript
    function greet(name) {
        return `Hello, ${name}!`;
    }
    ```
    """
    
    try:
        analysis = integration.get_code_analysis(text_with_code)
        logger.info(f"Análisis de código: {analysis}")
        
        if analysis['total_blocks'] > 0:
            logger.info("✅ Análisis de código exitoso")
            return True
        else:
            logger.warning("⚠️  No se detectaron bloques de código")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error analizando código: {e}")
        return False

async def test_with_main_integration():
    """Prueba integrada con el sistema principal"""
    logger.info("\n=== Prueba con integración principal ===")
    
    try:
        from main import initialize_components, app
        
        # Iniciar la aplicación
        app.state = type('State', (), {})()  # Crear objeto de estado
        
        await initialize_components()
        
        # Verificar que E2B esté disponible
        if hasattr(app.state, 'e2b_integration') and app.state.e2b_integration:
            logger.info("✅ E2B integration disponible en sistema principal")
            return app.state.e2b_integration
        else:
            logger.warning("⚠️  E2B integration no disponible en sistema principal")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error con integración principal: {e}")
        return None

async def main():
    """Función principal para probar E2B"""
    logger.info("🧪 Iniciando pruebas del sistema E2B...")
    
    # Configurar la API key en el entorno
    os.environ['E2B_API_KEY'] = "e2b_4bebb1dfce65d4db486ed23cd352d88e72f105df"
    
    # 1. Probar funcionalidad básica
    integration = await test_basic_e2b_functionality()
    
    # 2. Probar análisis de código
    analysis_success = await test_code_analysis(integration)
    
    # 3. Probar ejecución de código (si la integración está disponible)
    execution_success = False
    if integration:
        execution_success = await test_code_execution(integration)
    
    # 4. Probar integración con sistema principal
    main_integration = await test_with_main_integration()
    
    # Resultados
    logger.info("\n" + "="*50)
    logger.info("📋 RESULTADOS DE PRUEBAS E2B")
    logger.info("="*50)
    logger.info(f"✅ Funcionalidad Básica: {'OK' if integration else 'FALLÓ'}")
    logger.info(f"✅ Análisis de Código: {'OK' if analysis_success else 'FALLÓ'}")
    logger.info(f"✅ Ejecución de Código: {'OK' if execution_success else 'FALLÓ'}")
    logger.info(f"✅ Integración Principal: {'OK' if main_integration else 'FALLÓ'}")
    logger.info("="*50)
    
    # Información adicional
    if integration:
        insights = integration.get_insights()
        logger.info(f"💡 Insights del sistema: {insights}")

if __name__ == "__main__":
    asyncio.run(main())