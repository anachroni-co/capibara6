#!/usr/bin/env python3
"""
Demostración de Integración Real - Conexión entre VMs
Conectando el servicio de multimodelos vLLM en models-europe con otros sistemas
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetworkTopology:
    """
    Representación de la topología de red actual
    """
    def __init__(self):
        self.vms = {
            "models-europe": {
                "name": "models-europe",
                "internal_ip": "10.204.0.9",
                "external_ip": "34.175.48.2",
                "services": {
                    "vllm_multimodel": "http://localhost:8082",  # o http://10.204.0.9:8082
                    "description": "Servidor multimodelos vLLM ARM-Axion"
                }
            },
            "rag-europe": {
                "name": "rag-europe",
                "internal_ip": "10.204.0.10",
                "external_ip": "34.175.110.120",
                "services": {
                    # Sistema RAG principal - bases de datos
                    "milvus": "http://10.204.0.10:19530",    # Base de datos vectorial
                    "nebula_graph": "http://10.204.0.10:9669",  # Base de datos relacional/gráfica
                    "postgres": "http://10.204.0.10:5432",     # Base de datos relacional
                    "rag_bridge": "http://10.204.0.10:8000",   # Bridge RAG
                    "description": "Sistema RAG principal (bases de datos vectoriales y relacionales)"
                }
            },
            "services": {
                "name": "services",  # Anteriormente gpt-oss-20b
                "internal_ip": "10.204.0.5",
                "external_ip": "34.175.255.139",  # IP real de la VM services
                "services": {
                    "n8n": "http://10.204.0.5:5678",
                    "nebula_studio": "http://10.204.0.5:7001",
                    "smart_mcp": "http://10.204.0.5:5010",
                    "kyutai_tts": "http://10.204.0.5:5001",
                    "coqui_tts": "http://10.204.0.5:5002",
                    "description": "Servicios de automatización, TTS, MCP y monitoreo"
                }
            }
        }

class IntegrationDemonstrator:
    """
    Demostrador de la integración entre los sistemas
    """
    
    def __init__(self):
        self.topology = NetworkTopology()
        self.local_vllm_url = "http://localhost:8082"
    
    async def demonstrate_local_vllm_capabilities(self):
        """
        Demostrar las capacidades del sistema vLLM local
        """
        logger.info("🚀 Demostrando capacidades de vLLM multimodelos local")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Obtener modelos disponibles
                async with session.get(f"{self.local_vllm_url}/v1/models") as response:
                    models_data = await response.json()
                    available_models = models_data.get("data", [])
                
                print(f"\n🤖 Modelos disponibles en vLLM local ({self.local_vllm_url}):")
                for model in available_models:
                    print(f"  - {model['id']}: {model.get('description', 'Sin descripción')}")
                
                # Hacer una prueba de generación con cada modelo disponible
                test_query = "Explica en español qué es Python en una línea corta."
                
                print(f"\n💬 Prueba de generación para: '{test_query}'")
                
                for model in available_models[:3]:  # Probar con los primeros 3 modelos
                    model_id = model['id']
                    
                    payload = {
                        "model": model_id,
                        "messages": [{"role": "user", "content": test_query}],
                        "max_tokens": 100,
                        "temperature": 0.7
                    }
                    
                    try:
                        start_time = datetime.now()
                        async with session.post(f"{self.local_vllm_url}/v1/chat/completions", json=payload) as response:
                            if response.status == 200:
                                result = await response.json()
                                response_text = result["choices"][0]["message"]["content"]
                                elapsed_time = (datetime.now() - start_time).total_seconds()
                                
                                print(f"\n  Modelo: {model_id}")
                                print(f"  Respuesta: {response_text[:100]}...")
                                print(f"  Tiempo: {elapsed_time:.2f}s")
                            else:
                                print(f"  ❌ Error con modelo {model_id}: {response.status}")
                    except Exception as e:
                        print(f"  ❌ Excepción con modelo {model_id}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"❌ Error en demostración local: {e}")
    
    async def demonstrate_potential_rag_connection(self):
        """
        Demostrar cómo se conectaría con el sistema RAG en rag-europe
        """
        logger.info("🔗 Demostrando conexión potencial con sistema RAG")
        
        rag_europe_ip = self.topology.vms["rag-europe"]["internal_ip"]
        print(f"\n📡 IP interna de rag-europe: {rag_europe_ip}")
        print("   Esta VM está en la misma subred (10.204.0.0/24)")
        print("   Permitiendo comunicación interna de alta velocidad")
        
        # Mostrar cómo sería la conexión RAG
        rag_endpoints = {
            "bridge": f"http://{rag_europe_ip}:8000",
            "milvus": f"http://{rag_europe_ip}:19530", 
            "nebula_graph": f"http://{rag_europe_ip}:9669",
            "postgres": f"http://{rag_europe_ip}:5432"
        }
        
        print(f"\n🔌 Endpoints potenciales para sistema RAG en rag-europe:")
        for service, endpoint in rag_endpoints.items():
            print(f"   {service.upper()}: {endpoint}")
        
        print(f"\n💡 Estrategia de integración:")
        print(f"   1. models-europe (10.204.0.9) se comunica con")
        print(f"   2. rag-europe (10.204.0.10) para búsqueda de contexto usando:")
        print(f"      - Milvus para búsqueda vectorial")
        print(f"      - Nebula Graph para relaciones de conocimiento")
        print(f"      - PostgreSQL para metadatos")
        
        print(f"\n🔄 Flujo de información:")
        print(f"   Consulta -> models-europe -> rag-europe (Milvus/Nebula) -> contexto -> models-europe -> respuesta")
    
    async def demonstrate_potential_services_connection(self):
        """
        Demostrar cómo se conectaría con servicios distribuidos
        """
        logger.info("📡 Demostrando conexión potencial con servicios distribuidos")

        # Obtener IPs reales
        rag_europe_internal_ip = self.topology.vms["rag-europe"]["internal_ip"]
        services_internal_ip = self.topology.vms["services"]["internal_ip"]
        services_external_ip = self.topology.vms["services"]["external_ip"]

        print(f"\n🌐 Configuración real de servicios según firewall rules:")
        print(f"   rag-europe ({rag_europe_internal_ip}) tiene servicios:")
        print(f"   - Milvus (base de datos vectorial): http://{rag_europe_internal_ip}:19530")
        print(f"   - Nebula Graph (base de datos gráfica): http://{rag_europe_internal_ip}:9669")
        print(f"   - PostgreSQL (base de datos relacional): http://{rag_europe_internal_ip}:5432")
        print(f"   - Bridge RAG: http://{rag_europe_internal_ip}:8000")
        print(f"\n   services ({services_internal_ip}) tiene servicios:")
        print(f"   - N8n (automatización): http://{services_internal_ip}:5678")
        print(f"   - Smart MCP (contexto): http://{services_internal_ip}:5010")
        print(f"   - Nebula Graph Studio (visualización): http://{services_internal_ip}:7001")
        print(f"   - TTS (text-to-speech): http://{services_internal_ip}:5001/5002")

        print(f"\n🎯 Funcionalidades de servicios:")
        print(f"   - Bases de datos (en rag-europe): Milvus (vectorial), Nebula (gráfica), PostgreSQL (relacional)")
        print(f"   - MCP (en services): Enriquecimiento de contexto y protocolo de contexto")
        print(f"   - N8n (en services): Automatización de workflows")
        print(f"   - TTS (en services): Conversión texto-a-voz con Kyutai/Coqui TTS")
        print(f"   - Bridge RAG (en rag-europe): Interface para conexión con models-europe")
    
    async def demonstrate_complete_integration_flow(self):
        """
        Demostrar el flujo completo de integración
        """
        logger.info("🔄 DEMOSTRACIÓN COMPLETA: Flujo de integración entre sistemas")
        
        print(f"\n{'='*70}")
        print(f"🎯 FLUJO COMPLETO DE INTEGRACIÓN")
        print(f"{'='*70}")
        
        print(f"1. 📝 Usuario envía consulta")
        print(f"   └──> Ej: 'Explica cómo implementar un sistema RAG'")
        
        print(f"\n2. 🤖 models-europe (vLLM) - Selección de modelo óptimo")
        print(f"   └──> Basado en análisis de dominio y complejidad")
        print(f"   └──> Posible: gemma3_multimodal o gptoss_complex")
        
        print(f"\n3. 🔍 models-europe -> rag-europe - Búsqueda de contexto")
        print(f"   └──> Solicitud a rag-europe (10.204.0.10:8000)")
        print(f"   └──> Búsqueda vectorial en Milvus (10.204.0.10:19530)")
        print(f"   └──> Análisis relacional en Nebula (10.204.0.10:9669)")
        print(f"   └──> Combinación de fuentes de conocimiento")
        
        print(f"\n4. 🧠 rag-europe -> models-europe - Entrega de contexto enriquecido")
        print(f"   └──> Contexto con fuentes verificadas")
        print(f"   └──> Metadatos y relaciones de conocimiento")
        
        print(f"\n5. 🧩 models-europe -> services - Enriquecimiento MCP")
        print(f"   └──> Solicitud opcional a MCP (10.204.0.5:5010)")
        print(f"   └──> Mejora de contexto con protocolo de contexto")

        print(f"\n6. 🤖 models-europe (vLLM) - Generación de respuesta final")
        print(f"   └──> Uso de contexto enriquecido")
        print(f"   └──> Aplicación de optimizaciones ARM-Axion")
        print(f"   └──> Selección del modelo más apropiado")

        print(f"\n7. 🎯 Entrega de respuesta detallada al usuario")
        print(f"   └──> Opcional: conversión a audio vía TTS (10.204.0.5:5001/5002)")
        print(f"   └──> Opcional: automatización vía N8n (10.204.0.5:5678)")
        
        print(f"\n💡 VENTAJAS DE ESTA ARQUITECTURA:")
        print(f"   - Alta velocidad: comunicación interna entre VMs en 10.204.0.0/24")
        print(f"   - Seguridad: comunicación dentro de la VPC privada de Google Cloud")
        print(f"   - Especialización: cada VM optimizada para su función específica")
        print(f"   - Escalabilidad: servicios pueden escalarse independientemente")
        print(f"   - Resiliencia: fallo en un servicio no detiene completamente el sistema")
        print(f"   - ARM-Axion: optimizaciones específicas para rendimiento en ARM")
        
        print(f"{'='*70}")
    
    async def run_complete_demonstration(self):
        """
        Ejecutar la demostración completa
        """
        logger.info("🚀 INICIANDO DEMOSTRACIÓN COMPLETA DE INTEGRACIÓN")
        
        print(f"\n🌐 TOPOLOGÍA DE RED ACTUAL:")
        print(f"   models-europe: 10.204.0.9 (interna), 34.175.48.2 (externa)")
        print(f"   rag-europe:    10.204.0.10 (interna), 34.175.110.120 (externa)")
        print(f"   services:      10.204.0.5 (interna), 34.175.255.139 (externa) - Anteriormente gpt-oss-20b")
        print(f"\n   ✅ Todas las VMs están en la misma subred (10.204.0.0/24)!")
        print(f"   ✅ Comunicación interna de alta velocidad posible entre todas")
        
        # 1. Demostrar capacidades locales
        await self.demonstrate_local_vllm_capabilities()
        
        # 2. Demostrar conexión potencial RAG
        await self.demonstrate_potential_rag_connection()
        
        # 3. Demostrar conexión potencial servicios
        await self.demonstrate_potential_services_connection()
        
        # 4. Demostrar flujo completo
        await self.demonstrate_complete_integration_flow()
        
        logger.info("✅ DEMOSTRACIÓN COMPLETA FINALIZADA")


async def main():
    """
    Función principal para ejecutar la demostración
    """
    demonstrator = IntegrationDemonstrator()
    await demonstrator.run_complete_demonstration()

if __name__ == "__main__":
    asyncio.run(main())