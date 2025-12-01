#!/usr/bin/env python3
"""
Funcionalidad de Información Detallada - Integración RAG + Servicios
Implementa la funcionalidad para solicitar información detallada usando RAG y servicios
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

from integration_services.rag_multimodel_connector import RAGMultiModelConnector
from integration_services.integration_config import INTEGRATION_CONFIG, VM_CONFIG

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DetailedInfoRequester:
    """
    Clase para solicitar información detallada combinando:
    - Búsqueda RAG (Milvus + Nebula Graph)
    - Enriquecimiento de contexto MCP
    - Generación de respuesta con multimodelos vLLM
    - Opcional: TTS para salida de audio
    """
    
    def __init__(self):
        self.connector = RAGMultiModelConnector(
            vllm_url=INTEGRATION_CONFIG["vllm_endpoint"],
            rag_bridge_url=INTEGRATION_CONFIG["rag_bridge_endpoint"],
            mcp_url=INTEGRATION_CONFIG["mcp_endpoint"],
            tts_url=INTEGRATION_CONFIG["tts_endpoint"]
        )
        self.knowledge_sources = {}  # Almacenar fuentes de conocimiento
        self.query_history = []  # Historial de consultas para contexto conversacional
    
    async def initialize(self):
        """Inicializar el componente"""
        await self.connector.initialize()
        logger.info("✅ DetailedInfoRequester inicializado")
    
    async def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """
        Analizar la complejidad de la query para determinar qué componentes usar
        """
        analysis = {
            "complexity": "low",  # low, medium, high, expert
            "needs_rag": False,
            "needs_mcp": False,
            "needs_detailed_response": False,
            "domain": "general",
            "required_knowledge_depth": 1  # 1-5 scale
        }
        
        # Análisis de complejidad basado en palabras clave y longitud
        query_lower = query.lower()
        word_count = len(query.split())
        
        # Detectar tipo de consulta
        if any(kw in query_lower for kw in ["cómo funciona", "explica", "describe", "qué es"]):
            analysis["needs_detailed_response"] = True
            analysis["required_knowledge_depth"] = 3
            
        if any(kw in query_lower for kw in ["implementar", "código", "programación", "desarrollar"]):
            analysis["domain"] = "coding"
            analysis["complexity"] = "medium"
            analysis["required_knowledge_depth"] = 4
            analysis["needs_rag"] = True
            
        if any(kw in query_lower for kw in ["análisis", "complejo", "profundo", "razonamiento"]):
            analysis["complexity"] = "high"
            analysis["required_knowledge_depth"] = 5
            analysis["needs_rag"] = True
            analysis["needs_mcp"] = True
            
        if any(kw in query_lower for kw in ["multimodal", "imagen", "gráfica", "visual"]):
            analysis["domain"] = "multimodal"
            analysis["complexity"] = "medium"
            analysis["required_knowledge_depth"] = 4
            
        if word_count > 20:
            analysis["needs_detailed_response"] = True
            
        if word_count > 50:
            analysis["complexity"] = "high" if analysis["complexity"] == "low" else analysis["complexity"]
            analysis["needs_mcp"] = True
            
        return analysis
    
    async def fetch_detailed_context(self, query: str) -> Dict[str, Any]:
        """
        Obtener contexto detallado usando RAG (Milvus + Nebula Graph)
        """
        logger.info(f"🔍 Buscando contexto detallado para: '{query[:50]}...'")
        
        # Determinar si usar RAG basado en análisis de complejidad
        analysis = await self.analyze_query_complexity(query)
        
        if not analysis["needs_rag"]:
            logger.info("⏭️  RAG no requerido para esta consulta")
            return {"context": "", "sources": [], "quality_score": 0.0}
        
        # Buscar en RAG
        async with self.connector.rag_client as rag:
            rag_result = await rag.search_context(query, max_results=15)  # Más resultados para info detallada
        
        context = rag_result.get("context", "")
        results = rag_result.get("results", [])
        
        # Calcular calidad del contexto (score basado en cantidad y relevancia)
        quality_score = min(len(results) * 0.1, 1.0)  # Máximo 1.0
        if context:
            quality_score = min(quality_score + 0.3, 1.0)  # Bonus por tener contexto
        
        detailed_context = {
            "context": context,
            "sources": results,
            "quality_score": quality_score,
            "source_count": len(results),
            "is_detailed": len(results) > 5
        }
        
        logger.info(f"📚 Contexto obtenido: {len(results)} fuentes, calidad: {quality_score:.2f}")
        return detailed_context
    
    async def enhance_with_mcp(self, query: str, context: str) -> str:
        """
        Enriquecer contexto usando MCP (Model Context Protocol)
        """
        logger.info("🧠 Enriqueciendo contexto con MCP...")
        
        if not context:
            logger.info("⏭️  Sin contexto para enriquecer")
            return context
        
        async with self.connector.services_client as services:
            enhanced_context = await services.mcp_enhance_context(query, context)
        
        return enhanced_context
    
    async def generate_detailed_response(self, 
                                      query: str, 
                                      context: str = "", 
                                      use_mcp: bool = True) -> Dict[str, Any]:
        """
        Generar una respuesta detallada usando el multimodelo vLLM
        """
        logger.info(f"🤖 Generando respuesta detallada para: '{query[:50]}...'")
        
        # Analizar la query para seleccionar el mejor modelo
        analysis = await self.analyze_query_complexity(query)
        
        # Enrich context con MCP si está habilitado
        final_context = context
        if use_mcp and context:
            final_context = await self.enhance_with_mcp(query, context)
        
        # Usar el conector para generar la respuesta
        response_data = await self.connector.vllm_client.generate_with_context(
            model=self._select_appropriate_model(analysis),
            prompt=query,
            context=final_context,
            max_tokens=1000,  # Más tokens para respuestas detalladas
            temperature=0.6   # Menos aleatoriedad para respuestas consistentes
        )
        
        return {
            "response": response_data.get("response", ""),
            "model_used": response_data.get("model", "phi4_fast"),
            "context_used": bool(final_context),
            "analysis": analysis,
            "success": response_data.get("success", False)
        }
    
    def _select_appropriate_model(self, analysis: Dict[str, Any]) -> str:
        """
        Seleccionar modelo apropiado basado en el análisis de la query
        """
        # Basado en dominio y complejidad
        domain = analysis["domain"]
        complexity = analysis["complexity"]
        
        # Mapeo de dominios a modelos
        domain_to_model = {
            "coding": ["qwen_coder", "mistral_balanced"],
            "technical": ["mistral_balanced", "qwen_coder"],
            "multimodal": ["gemma3_multimodal", "gptoss_complex"],
            "expert": ["gptoss_complex", "gemma3_multimodal"]
        }
        
        # Buscar modelo apropiado
        if domain in domain_to_model:
            for model in domain_to_model[domain]:
                if model in self.connector.models_info:
                    return model
        
        # Si es alta complejidad, usar modelo experto
        if complexity in ["high", "expert"]:
            for model in ["gptoss_complex", "gemma3_multimodal"]:
                if model in self.connector.models_info:
                    return model
        
        # Por defecto, usar modelo según complejidad
        if complexity == "low":
            return "phi4_fast"
        else:
            return "mistral_balanced"  # Modelo balanceado para la mayoría de casos
    
    async def request_detailed_information(self, 
                                        query: str, 
                                        include_tts: bool = False,
                                        include_rag: bool = True,
                                        include_mcp: bool = True) -> Dict[str, Any]:
        """
        Método principal para solicitar información detallada usando todos los sistemas
        """
        logger.info(f"🎯 Solicitando información detallada: '{query[:50]}...'")
        
        start_time = datetime.now()
        
        # 1. Analizar la complejidad de la query
        analysis = await self.analyze_query_complexity(query)
        
        # 2. Obtener contexto detallado de RAG si es requerido
        rag_data = {"context": "", "sources": [], "quality_score": 0.0}
        if include_rag and analysis["needs_rag"]:
            rag_data = await self.fetch_detailed_context(query)
        
        # 3. Generar respuesta detallada
        response_data = await self.generate_detailed_response(
            query, 
            context=rag_data["context"], 
            use_mcp=include_mcp and analysis["needs_mcp"]
        )
        
        # 4. Opcionalmente, generar TTS
        tts_data = None
        if include_tts and response_data["success"] and response_data["response"]:
            logger.info("🎙️ Generando TTS para la respuesta...")
            async with self.connector.services_client as services:
                tts_data = await services.generate_tts(response_data["response"])
        
        # 5. Compilar resultado final
        result = {
            "query": query,
            "response": response_data["response"],
            "model_used": response_data["model_used"],
            "context_used": response_data["context_used"],
            "analysis": analysis,
            "rag_data": rag_data,
            "tts_available": tts_data is not None,
            "tts_data": tts_data,
            "success": response_data["success"],
            "processing_time": (datetime.now() - start_time).total_seconds(),
            "sources_count": len(rag_data["sources"]),
            "context_quality": rag_data["quality_score"]
        }
        
        # Agregar al historial de consultas
        self.query_history.append({
            "query": query,
            "response": response_data["response"][:200] + "..." if len(response_data["response"]) > 200 else response_data["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"✅ Información detallada generada: {len(result['response'])} caracteres, {result['processing_time']:.2f}s")
        return result
    
    async def multi_aspect_analysis(self, query: str) -> Dict[str, Any]:
        """
        Realizar un análisis multi-aspectos de la query usando diferentes modelos
        """
        logger.info(f"🔬 Análisis multi-aspectos: '{query[:50]}...'")
        
        # Obtener contexto base de RAG
        base_context = await self.fetch_detailed_context(query)
        
        # Análisis técnico
        technical_analysis = await self.connector.vllm_client.generate_with_context(
            model="mistral_balanced",
            prompt=f"Realiza un análisis técnico detallado de: {query}. Incluye aspectos como arquitectura, implementación, y consideraciones técnicas.",
            context=base_context["context"],
            max_tokens=800
        )
        
        # Análisis conceptual
        conceptual_analysis = await self.connector.vllm_client.generate_with_context(
            model="gptoss_complex",  
            prompt=f"Explica el concepto detrás de: {query}. Describe su fundamento teórico y principios clave.",
            context=base_context["context"],
            max_tokens=800
        )
        
        # Análisis práctico
        practical_analysis = await self.connector.vllm_client.generate_with_context(
            model="qwen_coder",
            prompt=f"Describe aplicaciones prácticas de: {query}. Incluye ejemplos concretos y casos de uso.",
            context=base_context["context"],
            max_tokens=800
        )
        
        return {
            "query": query,
            "technical_analysis": technical_analysis.get("response", ""),
            "conceptual_analysis": conceptual_analysis.get("response", ""),
            "practical_analysis": practical_analysis.get("response", ""),
            "context_used": bool(base_context["context"]),
            "sources_count": len(base_context["sources"])
        }
    
    async def comparative_answer(self, query: str) -> Dict[str, Any]:
        """
        Generar una respuesta comparativa usando múltiples modelos
        """
        logger.info(f"⚖️  Respuesta comparativa: '{query[:50]}...'")
        
        # Obtener contexto base
        base_context = await self.fetch_detailed_context(query)
        
        # Diferentes modelos para diferentes perspectivas
        models_and_prompts = [
            ("phi4_fast", f"Dame una respuesta rápida y concisa a: {query}"),
            ("mistral_balanced", f"Dame una explicación equilibrada y técnica de: {query}"),
            ("qwen_coder", f"Desde una perspectiva de programación/código, explica: {query}"),
            ("gptoss_complex", f"Dame un análisis profundo y complejo de: {query}")
        ]
        
        responses = {}
        for model, prompt in models_and_prompts:
            response = await self.connector.vllm_client.generate_with_context(
                model=model,
                prompt=prompt,
                context=base_context["context"],
                max_tokens=500
            )
            responses[model] = response.get("response", "")
        
        # Generar síntesis comparativa
        synthesis_prompt = f"""
        A continuación se presentan diferentes perspectivas sobre la consulta: "{query}"

        Perspectiva rápida (phi4_fast): {responses.get('phi4_fast', '')[:200]}...

        Perspectiva técnica (mistral_balanced): {responses.get('mistral_balanced', '')[:200]}...

        Perspectiva de código (qwen_coder): {responses.get('qwen_coder', '')[:200]}...

        Perspectiva compleja (gptoss_complex): {responses.get('gptoss_complex', '')[:200]}...

        Por favor, proporciona una síntesis comparativa que resuma las diferencias clave entre las perspectivas,
        destacando cuál es más apropiada para qué tipo de necesidad.
        """
        
        synthesis = await self.connector.vllm_client.generate_with_context(
            model="gptoss_complex",
            prompt=synthesis_prompt,
            max_tokens=800
        )
        
        return {
            "query": query,
            "individual_responses": responses,
            "comparative_synthesis": synthesis.get("response", ""),
            "context_used": bool(base_context["context"]),
            "best_model_for_query": self._select_appropriate_model(await self.analyze_query_complexity(query))
        }


# Función de demostración
async def demonstrate_detailed_info_functionality():
    """
    Demostrar la funcionalidad de información detallada
    """
    logger.info("🚀 Demostración de Funcionalidad de Información Detallada")
    
    requester = DetailedInfoRequester()
    await requester.initialize()
    
    # Ejemplos de consultas para información detallada
    detailed_queries = [
        "Explica cómo funciona el aprendizaje automático con redes neuronales",
        "¿Cuál es la diferencia entre RAG y un chatbot tradicional?",
        "Implementa un sistema de recomendación básico en Python",
        "¿Qué son las optimizaciones ARM-Axion y cómo mejoran el rendimiento?"
    ]
    
    for query in detailed_queries:
        print(f"\n--- Consulta detallada: {query} ---")
        
        # Solicitud de información detallada
        result = await requester.request_detailed_information(query, include_tts=False)
        
        print(f"🤖 Modelo usado: {result['model_used']}")
        print(f"📦 Contexto usado: {result['context_used']}")
        print(f"📊 Calidad del contexto: {result['context_quality']:.2f}")
        print(f"📚 Fuentes: {result['sources_count']}")
        print(f"⏱️  Tiempo: {result['processing_time']:.2f}s")
        print(f"💬 Respuesta (truncada): {result['response'][:200]}...")
        
        # Análisis multi-aspectos
        print("\n🔬 Análisis multi-aspectos:")
        multi_analysis = await requester.multi_aspect_analysis(query)
        print(f"  Fuentes: {multi_analysis['sources_count']}")
        print(f"  Contexto usado: {multi_analysis['context_used']}")
        
        # Respuesta comparativa
        print("\n⚖️  Respuesta comparativa:")
        comparative = await requester.comparative_answer(query[:50] + "...")
        print(f"  Modelo recomendado: {comparative['best_model_for_query']}")
        print(f"  Contexto usado: {comparative['context_used']}")
    
    logger.info("✅ Demostración completada")


if __name__ == "__main__":
    asyncio.run(demonstrate_detailed_info_functionality())