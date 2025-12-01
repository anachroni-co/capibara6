#!/usr/bin/env python3
"""
Componente de Integración - Conector RAG + Multimodelos vLLM + Servicios
Conecta los 3 sistemas para proporcionar respuestas detalladas con contexto enriquecido
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ModelDomain(Enum):
    """Dominios de los modelos para routing semántico"""
    GENERAL = "general"
    TECHNICAL = "technical" 
    CODING = "coding"
    MULTIMODAL = "multimodal_expert"
    EXPERT = "expert"


@dataclass
class ModelInfo:
    """Información del modelo"""
    name: str
    domain: ModelDomain
    description: str
    priority: int


class RAGClient:
    """Cliente para conectar con el sistema RAG (Milvus + Nebula Graph)"""
    
    def __init__(self, rag_bridge_url: str = "http://localhost:8001"):
        self.rag_bridge_url = rag_bridge_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_context(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Buscar contexto en el sistema RAG"""
        try:
            # Endpoint para búsqueda RAG (simulando el endpoint real del sistema)
            rag_url = f"{self.rag_bridge_url}/v1/search"
            
            payload = {
                "query": query,
                "max_results": max_results,
                "search_type": "hybrid"  # búsqueda híbrida (vector + gráfico)
            }
            
            async with self.session.post(rag_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"🔍 RAG search completed: {len(result.get('results', []))} results")
                    return result
                else:
                    logger.warning(f"⚠️ RAG search failed with status {response.status}")
                    return {"results": [], "context": "", "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            logger.error(f"❌ Error en búsqueda RAG: {e}")
            return {"results": [], "context": "", "error": str(e)}


class VLLMClient:
    """Cliente para conectar con el servidor de multimodelos vLLM"""
    
    def __init__(self, vllm_url: str = "http://localhost:8082"):
        self.vllm_url = vllm_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Obtener modelos disponibles en vLLM"""
        try:
            models_url = f"{self.vllm_url}/v1/models"
            
            async with self.session.get(models_url) as response:
                if response.status == 200:
                    data = await response.json()
                    models = []
                    for model_data in data.get("data", []):
                        model_info = {
                            "id": model_data["id"],
                            "description": model_data.get("description", ""),
                            "domain": model_data.get("domain", "general"),
                            "status": model_data.get("status", "available")
                        }
                        models.append(model_info)
                    
                    logger.info(f"🤖 vLLM models available: {len(models)}")
                    return models
                else:
                    logger.error(f"❌ Error getting models: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Error en vLLM client: {e}")
            return []
    
    async def generate_with_context(
        self, 
        model: str, 
        prompt: str, 
        context: str = "", 
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generar respuesta con contexto usando modelo específico"""
        try:
            chat_url = f"{self.vllm_url}/v1/chat/completions"
            
            # Construir prompt con contexto si está disponible
            full_prompt = prompt
            if context:
                full_prompt = f"Contexto previo:\n{context}\n\nPregunta actual: {prompt}"
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            async with self.session.post(chat_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "response": result["choices"][0]["message"]["content"],
                        "model": model,
                        "usage": result.get("usage", {}),
                        "success": True
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"❌ vLLM generation error {response.status}: {error_text}")
                    return {
                        "response": "",
                        "model": model,
                        "error": f"HTTP {response.status}: {error_text}",
                        "success": False
                    }
                    
        except Exception as e:
            logger.error(f"❌ Error en vLLM generation: {e}")
            return {
                "response": "",
                "model": model,
                "error": str(e),
                "success": False
            }


class ServicesClient:
    """Cliente para conectar con los servicios adicionales (TTS, MCP, N8n)"""
    
    def __init__(self, services_base_url: str = "http://localhost:5003"):
        self.services_base_url = services_base_url
        self.tts_url = "http://localhost:5002"
        self.mcp_url = "http://localhost:5003"
        self.n8n_url = "http://localhost:5678"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def mcp_enhance_context(self, query: str, current_context: str) -> str:
        """Usar MCP para enriquecer el contexto"""
        try:
            mcp_url = f"{self.mcp_url}/api/mcp/enhance"
            
            payload = {
                "query": query,
                "context": current_context,
                "approach": "selective-rag"
            }
            
            async with self.session.post(mcp_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    enhanced_context = result.get("enhanced_context", "")
                    logger.info("🧠 MCP context enhancement applied")
                    return enhanced_context
                else:
                    logger.warning(f"⚠️ MCP enhancement failed: {response.status}")
                    return current_context
                    
        except Exception as e:
            logger.error(f"❌ MCP enhancement error: {e}")
            return current_context
    
    async def generate_tts(self, text: str, voice: str = "default") -> Optional[str]:
        """Generar audio TTS usando servicio Kyutai TTS"""
        try:
            tts_url = f"{self.tts_url}/api/tts/speak"
            
            payload = {
                "text": text,
                "voice": voice,
                "language": "es"
            }
            
            async with self.session.post(tts_url, json=payload) as response:
                if response.status == 200:
                    logger.info("🎙️ TTS audio generated successfully")
                    # Devolver URL del audio generado o contenido binario
                    return await response.json()
                else:
                    logger.warning(f"⚠️ TTS generation failed: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ TTS generation error: {e}")
            return None


class RAGMultiModelConnector:
    """
    Componente principal de integración que conecta:
    - Sistema RAG (Milvus + Nebula)
    - Servidor de multimodelos vLLM
    - Servicios (TTS, MCP, N8n)
    """
    
    def __init__(self, 
                 vllm_url: str = "http://localhost:8082",
                 rag_bridge_url: str = "http://localhost:8001",
                 mcp_url: str = "http://localhost:5003",
                 tts_url: str = "http://localhost:5002"):
        
        self.vllm_url = vllm_url
        self.rag_bridge_url = rag_bridge_url
        self.mcp_url = mcp_url
        self.tts_url = tts_url
        
        # Clientes para cada sistema
        self.vllm_client = VLLMClient(vllm_url)
        self.rag_client = RAGClient(rag_bridge_url)
        self.services_client = ServicesClient(mcp_url)
        
        # Información de modelos
        self.models_info = {}
        
        logger.info("🔗 RAGMultiModelConnector inicializado")
    
    async def initialize(self):
        """Inicializar la conexión y obtener información de modelos"""
        logger.info("🚀 Inicializando RAGMultiModelConnector...")
        
        async with self.vllm_client as vllm:
            models = await vllm.get_available_models()
            
            for model_data in models:
                if model_data["status"] == "loaded":
                    domain = ModelDomain(model_data["domain"])
                    self.models_info[model_data["id"]] = ModelInfo(
                        name=model_data["id"],
                        domain=domain,
                        description=model_data["description"],
                        priority=self._get_model_priority(domain)
                    )
        
        logger.info(f"✅ {len(self.models_info)} modelos inicializados")
    
    def _get_model_priority(self, domain: ModelDomain) -> int:
        """Obtener prioridad del modelo según dominio"""
        priority_map = {
            ModelDomain.GENERAL: 5,
            ModelDomain.TECHNICAL: 4,
            ModelDomain.CODING: 3,
            ModelDomain.MULTIMODAL: 2,
            ModelDomain.EXPERT: 1
        }
        return priority_map.get(domain, 5)
    
    def _select_model_for_query(self, query: str) -> str:
        """Seleccionar modelo óptimo basado en la query"""
        query_lower = query.lower()
        
        # Análisis simple de dominio
        if any(keyword in query_lower for keyword in ["código", "programación", "python", "javascript", "función"]):
            model_domain = ModelDomain.CODING
        elif any(keyword in query_lower for keyword in ["análisis", "complejo", "profundo", "razonamiento"]):
            model_domain = ModelDomain.EXPERT
        elif any(keyword in query_lower for keyword in ["técnic", "método", "implementación"]):
            model_domain = ModelDomain.TECHNICAL
        elif any(keyword in query_lower for keyword in ["imagen", "multimodal", "visual"]):
            model_domain = ModelDomain.MULTIMODAL
        else:
            model_domain = ModelDomain.GENERAL
        
        # Buscar modelo con el dominio más cercano
        for model_name, model_info in self.models_info.items():
            if model_info.domain == model_domain and model_info.priority <= 3:  # Prioridad alta/medio
                return model_name
        
        # Fallback al modelo general
        for model_name, model_info in self.models_info.items():
            if model_info.domain == ModelDomain.GENERAL:
                return model_name
        
        # Si no hay modelo general, devolver el primero disponible
        return next(iter(self.models_info.keys()), "phi4_fast")
    
    async def get_enriched_response(self, query: str, use_rag: bool = True, use_mcp: bool = True) -> Dict[str, Any]:
        """Obtener respuesta enriquecida usando los 3 sistemas"""
        logger.info(f"🎯 Procesando query: '{query[:50]}...'")
        
        # 1. Buscar contexto RAG si está habilitado
        context_data = {"context": "", "rag_results": []}
        if use_rag:
            logger.info("🔍 Buscando contexto en RAG...")
            async with self.rag_client as rag:
                context_data = await rag.search_context(query)
        
        # 2. Enrich context con MCP si está habilitado
        final_context = context_data.get("context", "")
        if use_mcp and final_context:
            logger.info("🧠 Enriqueciendo contexto con MCP...")
            async with self.services_client as services:
                final_context = await services.mcp_enhance_context(query, final_context)
        
        # 3. Seleccionar modelo óptimo para la query
        selected_model = self._select_model_for_query(query)
        logger.info(f"🤖 Modelo seleccionado: {selected_model}")
        
        # 4. Generar respuesta usando el modelo seleccionado con contexto
        async with self.vllm_client as vllm:
            response_data = await vllm.generate_with_context(
                model=selected_model,
                prompt=query,
                context=final_context,
                max_tokens=500,
                temperature=0.7
            )
        
        # 5. Compilar respuesta final
        result = {
            "query": query,
            "response": response_data.get("response", ""),
            "model_used": response_data.get("model", selected_model),
            "context_used": bool(final_context),
            "context_source": "RAG + MCP" if (use_rag and use_mcp) else ("RAG" if use_rag else ("MCP" if use_mcp else "None")),
            "rag_data": context_data,
            "usage": response_data.get("usage", {}),
            "success": response_data.get("success", False)
        }
        
        logger.info(f"✅ Respuesta generada: {len(result['response'])} caracteres")
        return result
    
    async def get_response_with_tts(self, query: str) -> Dict[str, Any]:
        """Obtener respuesta con texto y audio (TTS)"""
        # Obtener la respuesta enriquecida
        response_data = await self.get_enriched_response(query)
        
        # Generar audio TTS si es posible
        tts_result = None
        if response_data["success"] and response_data["response"]:
            logger.info("🎙️ Generando audio TTS...")
            async with self.services_client as services:
                tts_result = await services.generate_tts(response_data["response"])
        
        response_data["tts_available"] = tts_result is not None
        response_data["tts_data"] = tts_result
        
        return response_data


async def main():
    """Función principal para demostrar la integración"""
    logger.info("🚀 Iniciando demostración de RAGMultiModelConnector")
    
    # Inicializar el conector
    connector = RAGMultiModelConnector(
        vllm_url="http://localhost:8082",  # Puerto actual de nuestro vLLM
        rag_bridge_url="http://10.154.0.2:8000",  # IP de rag3 cuando esté disponible
        mcp_url="http://34.175.136.104:5003",  # IP de gpt-oss-20b servicios
        tts_url="http://34.175.136.104:5002"   # IP de gpt-oss-20b TTS
    )
    
    await connector.initialize()
    
    # Ejemplos de consultas para demostrar la funcionalidad
    test_queries = [
        "¿Cómo funciona el modelo phi4_fast?",
        "Explica cómo implementar una red neuronal en Python",
        "¿Cuál es la diferencia entre un modelo multimodal y un modelo de texto?",
        "¿Qué es el razonamiento complejo en IA?"
    ]
    
    for query in test_queries:
        print(f"\n--- Consulta: {query} ---")
        try:
            result = await connector.get_enriched_response(query)
            print(f"🤖 Modelo usado: {result['model_used']}")
            print(f"📦 Contexto usado: {result['context_used']} ({result['context_source']})")
            print(f"💬 Respuesta: {result['response'][:200]}...")
            print(f"✅ Éxito: {result['success']}")
        except Exception as e:
            logger.error(f"❌ Error procesando query '{query}': {e}")
    
    logger.info("✅ Demostración completada")


if __name__ == "__main__":
    asyncio.run(main())