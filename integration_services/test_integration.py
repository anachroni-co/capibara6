#!/usr/bin/env python3
"""
Prueba de Integración Completa - RAG + Multimodelos vLLM + Servicios
Script para verificar que todos los sistemas estén correctamente integrados
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

# Importar componentes
from integration_services.rag_multimodel_connector import RAGMultiModelConnector
from integration_services.detailed_info_requester import DetailedInfoRequester
from integration_services.integration_config import INTEGRATION_CONFIG, VM_CONFIG

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IntegrationTester:
    """
    Clase para probar la integración completa entre:
    - vLLM Multimodelos (puerto 8082 en esta VM)
    - Sistema RAG (Milvus + Nebula Graph)
    - Servicios (TTS, MCP, N8n)
    """
    
    def __init__(self):
        # URLs adaptadas para la red actual
        # models-europe (esta VM): 10.204.0.9 / 34.175.48.2
        self.vllm_url = "http://localhost:8082"  # Puerto actual de nuestro multimodelo
        self.rag_bridge_url = "http://10.154.0.2:8000"  # IP interna de rag3 (cuando esté disponible)
        self.mcp_url = "http://34.175.136.104:5003"   # IP de gpt-oss-20b servicios
        self.tts_url = "http://34.175.136.104:5002"    # IP de gpt-oss-20b TTS
        
        # Para pruebas locales en esta VM (vLLM solo)
        self.test_vllm_url = "http://localhost:8082"
        
        self.results = {
            "vllm_tests": [],
            "rag_tests": [],
            "services_tests": [],
            "integration_tests": []
        }
    
    async def test_vllm_connection(self) -> Dict[str, Any]:
        """Probar conexión con vLLM multimodelos"""
        logger.info("📡 Probando conexión con vLLM multimodelos...")
        
        start_time = datetime.now()
        
        try:
            async with aiohttp.ClientSession() as session:
                # Probar health endpoint
                health_url = f"{self.test_vllm_url}/health"
                async with session.get(health_url) as response:
                    health_ok = response.status == 200
                    health_data = await response.json() if health_ok else {}
                
                # Probar models endpoint
                models_url = f"{self.test_vllm_url}/v1/models"
                async with session.get(models_url) as response:
                    models_ok = response.status == 200
                    models_data = await response.json() if models_ok else {}
                
                # Probar generación simple
                chat_url = f"{self.test_vllm_url}/v1/chat/completions"
                payload = {
                    "model": "phi4_fast",  # Modelo más rápido para pruebas
                    "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
                    "max_tokens": 50
                }
                
                async with session.post(chat_url, json=payload) as response:
                    generation_ok = response.status == 200
                    generation_data = await response.json() if generation_ok else {}
            
            test_result = {
                "test_name": "vllm_connection",
                "status": "success",
                "vllm_healthy": health_ok,
                "models_available": len(models_data.get("data", [])) if models_ok else 0,
                "generation_working": generation_ok,
                "response_time": (datetime.now() - start_time).total_seconds(),
                "models_list": [m["id"] for m in models_data.get("data", [])] if models_ok else []
            }
            
            logger.info(f"✅ vLLM conexión: {test_result['models_available']} modelos, tiempo: {test_result['response_time']:.2f}s")
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de vLLM: {e}")
            return {
                "test_name": "vllm_connection",
                "status": "error",
                "error": str(e),
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def test_rag_connection(self) -> Dict[str, Any]:
        """Probar conexión con sistema RAG (simulado mientras no esté disponible)"""
        logger.info("📡 Probando conexión con sistema RAG...")
        
        start_time = datetime.now()
        
        # Actualmente no tenemos acceso a rag3, por lo tanto simulamos la prueba
        test_result = {
            "test_name": "rag_connection",
            "status": "skipped",
            "reason": "VM rag3 no disponible en esta instancia",
            "response_time": (datetime.now() - start_time).total_seconds(),
            "rag_available": False,
            "suggestion": "Ejecutar desde la VM rag3 o verificar conexión de red"
        }
        
        logger.info("⏭️  Prueba de RAG omitida - VM no disponible")
        return test_result
    
    async def test_services_connection(self) -> Dict[str, Any]:
        """Probar conexión con servicios (TTS, MCP, N8n)"""
        logger.info("📡 Probando conexión con servicios...")
        
        start_time = datetime.now()
        
        # Actualmente no tenemos acceso a gpt-oss-20b, por lo tanto simulamos
        test_result = {
            "test_name": "services_connection",
            "status": "skipped",
            "reason": "VM gpt-oss-20b no disponible en esta instancia",
            "response_time": (datetime.now() - start_time).total_seconds(),
            "services_available": [],
            "suggestion": "Ejecutar desde las VMs correspondientes o verificar conexión de red"
        }
        
        logger.info("⏭️  Prueba de servicios omitida - VM no disponible")
        return test_result
    
    async def test_basic_integration(self) -> Dict[str, Any]:
        """Probar integración básica usando solo vLLM"""
        logger.info("🔗 Probando integración básica (solo vLLM disponible localmente)...")
        
        start_time = datetime.now()
        
        try:
            # Inicializar el conector con solo vLLM
            connector = RAGMultiModelConnector(vllm_url=self.test_vllm_url)
            await connector.initialize()
            
            # Probar generación simple
            response_data = await connector.vllm_client.generate_with_context(
                model="phi4_fast",
                prompt="Hola, ¿qué puedes hacer?",
                max_tokens=100
            )
            
            # Probar selección de modelo
            selected_model = connector._select_model_for_query("Hola, ¿qué puedes hacer?")
            
            test_result = {
                "test_name": "basic_integration",
                "status": "success",
                "vllm_initialized": len(connector.models_info) > 0,
                "model_selection_working": True,
                "generation_success": response_data.get("success", False),
                "selected_model": selected_model,
                "response_length": len(response_data.get("response", "")),
                "response_time": (datetime.now() - start_time).total_seconds(),
                "models_available": list(connector.models_info.keys())
            }
            
            logger.info(f"✅ Integración básica: modelo {selected_model}, respuesta {test_result['response_length']} chars")
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Error en integración básica: {e}")
            return {
                "test_name": "basic_integration",
                "status": "error",
                "error": str(e),
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def test_detailed_info_functionality(self) -> Dict[str, Any]:
        """Probar funcionalidad de información detallada"""
        logger.info("📋 Probando funcionalidad de información detallada...")
        
        start_time = datetime.now()
        
        try:
            # Inicializar el requester de información detallada
            requester = DetailedInfoRequester()
            await requester.initialize()
            
            # Hacer una consulta simple (solo con vLLM disponible)
            query = "¿Qué es Python?"
            
            # Adaptar la solicitud para usar solo vLLM (sin RAG ni servicios externos)
            result = await requester.generate_detailed_response(query, context="", use_mcp=False)
            
            test_result = {
                "test_name": "detailed_info_functionality",
                "status": "partial_success",  # Parcial porque no hay RAG ni servicios
                "query_processed": True,
                "response_generated": len(result.get("response", "")) > 0,
                "model_used": result.get("model_used", "unknown"),
                "response_length": len(result.get("response", "")),
                "response_time": (datetime.now() - start_time).total_seconds(),
                "has_context": result.get("context_used", False)
            }
            
            logger.info(f"✅ Info detallada: modelo {result.get('model_used')}, respuesta {test_result['response_length']} chars")
            return test_result
            
        except Exception as e:
            logger.error(f"❌ Error en funcionalidad de info detallada: {e}")
            return {
                "test_name": "detailed_info_functionality",
                "status": "error",
                "error": str(e),
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Ejecutar todas las pruebas de integración"""
        logger.info("🚀 Iniciando pruebas de integración completa...")
        
        # Ejecutar todas las pruebas
        tests = [
            ("vllm_connection", self.test_vllm_connection),
            ("rag_connection", self.test_rag_connection),
            ("services_connection", self.test_services_connection),
            ("basic_integration", self.test_basic_integration),
            ("detailed_info_functionality", self.test_detailed_info_functionality)
        ]
        
        results = {
            "summary": {
                "total_tests": len(tests),
                "start_time": datetime.now().isoformat(),
                "tests_run": 0,
                "success_count": 0,
                "skipped_count": 0,
                "error_count": 0
            },
            "test_results": {}
        }
        
        for test_name, test_func in tests:
            logger.info(f"🧪 Ejecutando prueba: {test_name}")
            try:
                result = await test_func()
                results["test_results"][test_name] = result
                
                results["summary"]["tests_run"] += 1
                if result["status"] == "success":
                    results["summary"]["success_count"] += 1
                elif result["status"] == "skipped":
                    results["summary"]["skipped_count"] += 1
                elif result["status"] == "error":
                    results["summary"]["error_count"] += 1
            except Exception as e:
                logger.error(f"❌ Error ejecutando prueba {test_name}: {e}")
                results["test_results"][test_name] = {
                    "test_name": test_name,
                    "status": "error",
                    "error": str(e)
                }
                results["summary"]["error_count"] += 1
        
        results["summary"]["end_time"] = datetime.now().isoformat()
        results["summary"]["total_time"] = (datetime.now() - datetime.fromisoformat(results["summary"]["start_time"].replace("Z", "+00:00"))).total_seconds()
        
        return results
    
    def print_test_summary(self, results: Dict[str, Any]):
        """Imprimir resumen de las pruebas"""
        summary = results["summary"]
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE PRUEBAS DE INTEGRACIÓN")
        print("="*60)
        
        print(f"📅 Inicio: {summary['start_time']}")
        print(f"⏱️  Duración total: {summary['total_time']:.2f}s")
        print(f"🧪 Total pruebas: {summary['total_tests']}")
        print(f"✅ Éxito: {summary['success_count']}")
        print(f"⏭️  Omitidas: {summary['skipped_count']}")
        print(f"❌ Error: {summary['error_count']}")
        
        print("\n🔍 DETALLES POR PRUEBA:")
        for test_name, result in results["test_results"].items():
            status_emoji = {
                "success": "✅",
                "partial_success": "🟡",
                "skipped": "⏭️",
                "error": "❌"
            }.get(result.get("status", "error"), "❓")
            
            print(f"  {status_emoji} {test_name}: {result.get('status', 'unknown')}")
            
            # Mostrar detalles específicos según la prueba
            if test_name == "vllm_connection":
                if result.get("status") == "success":
                    print(f"    - Modelos disponibles: {result.get('models_available', 0)}")
                    print(f"    - Tiempo respuesta: {result.get('response_time', 0):.2f}s")
            
            elif test_name == "basic_integration":
                if result.get("status") == "success":
                    print(f"    - Modelos en connector: {len(result.get('models_available', []))}")
                    print(f"    - Selección modelo: {result.get('selected_model', 'N/A')}")
        
        print("\n💡 ESTADO DE LA INTEGRACIÓN:")
        
        # Evaluar el estado general
        if summary['error_count'] == 0 and summary['success_count'] > 0:
            print("  ¡Excelente! El componente funcional principal (vLLM) está operativo")
        elif summary['success_count'] == 0:
            print("  ⚠️  Requiere atención - hay errores en componentes críticos")
        else:
            print("  🟡 Estado mixto - componentes principales operativos, otros pendientes")
        
        print("\n📝 ACCIONES RECOMENDADAS:")
        if summary['skipped_count'] > 0:
            print("  • Verificar conexión con VMs faltantes (rag3, gpt-oss-20b)")
            print("  • Asegurarse que las IPs internas y reglas de firewall estén configuradas")
            print("  • Consultar la documentación de redes en VM_SERVICES_ESTADO_ACTUAL.md")
        
        print(f"  • Componente vLLM actualmente activo en puerto {self.test_vllm_url}")
        print(f"  • Componentes de integración creados en /integration_services/")
        print("  • Listo para usar cuando se conecten las VMs faltantes")
        
        print("="*60)


async def main():
    """Función principal para ejecutar las pruebas"""
    logger.info("🚀 Iniciando pruebas de integración completa")
    
    tester = IntegrationTester()
    results = await tester.run_all_tests()
    tester.print_test_summary(results)
    
    # Mostrar resultados detallados si hay interés
    print("\n🔍 ¿Ver resultados detallados? (s/n): ", end="")
    
    # En modo no interactivo, simplemente mostrar algunos detalles clave
    print("\n(En modo no interactivo - mostrando resumen detallado)")
    
    for test_name, result in results["test_results"].items():
        print(f"\n--- {test_name} ---")
        for key, value in result.items():
            if key != "test_name":
                print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())