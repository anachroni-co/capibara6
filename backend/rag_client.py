#!/usr/bin/env python3
"""
Cliente para consultar el sistema RAG desde otras VMs (ej: bounty2)

Este cliente permite a los servidores con Ollama consultar el sistema RAG
en RAG3 para enriquecer respuestas con datos personales del usuario.
"""

import os
import logging
from typing import Dict, List, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class RAGClient:
    """Cliente HTTP para consultar el sistema RAG en VM RAG3"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Inicializar cliente RAG

        Args:
            base_url: URL base del servidor RAG (default: desde env o IP interna)
            timeout: Timeout para requests en segundos
            max_retries: Número máximo de reintentos
        """
        self.base_url = base_url or os.getenv(
            "RAG_API_URL",
            "http://10.154.0.2:8000"  # IP interna de RAG3 en GCloud
        )
        self.timeout = timeout

        # Configurar session con retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.info(f"RAGClient initialized with base_url: {self.base_url}")

    def search_semantic(
        self,
        query: str,
        collection_name: Optional[str] = None,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Búsqueda semántica en colecciones vectoriales

        Args:
            query: Texto de búsqueda
            collection_name: Colección específica o None para buscar en todas
            n_results: Número de resultados a retornar

        Returns:
            Dict con resultados de búsqueda
        """
        endpoint = f"{self.base_url}/api/search/semantic"
        payload = {
            "query": query,
            "collection_name": collection_name,
            "n_results": n_results
        }

        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return {
                "query": query,
                "total_results": 0,
                "results": [],
                "error": str(e)
            }

    def search_rag(
        self,
        query: str,
        n_results: int = 5,
        use_graph: bool = True
    ) -> Dict[str, Any]:
        """
        Búsqueda RAG completa (Vector + PostgreSQL + Grafo)

        Esta es la búsqueda más completa que combina:
        - Búsqueda vectorial semántica
        - Enriquecimiento con datos de PostgreSQL
        - Exploración de grafo de conocimiento en Nebula

        Args:
            query: Pregunta en lenguaje natural
            n_results: Resultados por colección
            use_graph: Si usar exploración de grafo

        Returns:
            Dict con contexto enriquecido del RAG
        """
        endpoint = f"{self.base_url}/api/search/rag"
        payload = {
            "query": query,
            "n_results": n_results,
            "use_graph": use_graph
        }

        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en búsqueda RAG: {e}")
            return {
                "query": query,
                "context": "",
                "sources": [],
                "error": str(e)
            }

    def search_all_collections(
        self,
        query: str,
        n_results: int = 3
    ) -> Dict[str, Any]:
        """
        Buscar en todas las colecciones simultáneamente

        Args:
            query: Texto de búsqueda
            n_results: Resultados por colección

        Returns:
            Dict con resultados por colección
        """
        endpoint = f"{self.base_url}/api/search/all"
        payload = {
            "query": query,
            "n_results": n_results
        }

        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en búsqueda multi-colección: {e}")
            return {
                "query": query,
                "total_results": 0,
                "collections": [],
                "results": {},
                "error": str(e)
            }

    def health_check(self) -> Dict[str, Any]:
        """
        Verificar estado del servicio RAG

        Returns:
            Dict con estado de servicios
        """
        endpoint = f"{self.base_url}/health"

        try:
            response = self.session.get(endpoint, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error en health check: {e}")
            return {
                "status": "unavailable",
                "error": str(e)
            }

    def get_context_for_llm(
        self,
        user_query: str,
        max_context_length: int = 2000,
        n_results: int = 3
    ) -> str:
        """
        Obtener contexto formateado para agregar al prompt de un LLM

        Esta función es útil para enriquecer las respuestas de Ollama
        con información personal del usuario.

        Args:
            user_query: Consulta del usuario
            max_context_length: Longitud máxima del contexto en caracteres
            n_results: Número de resultados a incluir

        Returns:
            String con contexto formateado para el LLM
        """
        rag_result = self.search_rag(
            query=user_query,
            n_results=n_results,
            use_graph=True
        )

        if "error" in rag_result:
            return ""

        # Construir contexto
        context_parts = []

        # Agregar contexto general si existe
        if rag_result.get("context"):
            context_parts.append("Información relevante del usuario:")
            context_parts.append(rag_result["context"])

        # Agregar fuentes si existen
        sources = rag_result.get("sources", [])
        if sources:
            context_parts.append("\nFuentes específicas:")
            for i, source in enumerate(sources[:n_results], 1):
                source_text = source.get("content", source.get("text", ""))
                if source_text:
                    context_parts.append(f"{i}. {source_text[:300]}...")

        full_context = "\n".join(context_parts)

        # Truncar si es necesario
        if len(full_context) > max_context_length:
            full_context = full_context[:max_context_length] + "..."

        return full_context


# Función helper para uso rápido
def get_rag_context(query: str, rag_url: Optional[str] = None) -> str:
    """
    Función helper para obtener rápidamente contexto RAG

    Uso:
        context = get_rag_context("¿Qué he hablado sobre IA?")
        full_prompt = f"{context}\n\nUsuario: {user_query}"
    """
    client = RAGClient(base_url=rag_url)
    return client.get_context_for_llm(query)


if __name__ == "__main__":
    # Demo de uso
    logging.basicConfig(level=logging.INFO)

    client = RAGClient()

    # Test health
    print("=== Health Check ===")
    health = client.health_check()
    print(health)

    # Test búsqueda
    print("\n=== Búsqueda RAG ===")
    result = client.search_rag("machine learning", n_results=2)
    print(f"Query: {result.get('query')}")
    print(f"Context length: {len(result.get('context', ''))}")
    print(f"Sources: {len(result.get('sources', []))}")

    # Test contexto para LLM
    print("\n=== Contexto para LLM ===")
    context = client.get_context_for_llm("IA y embeddings", max_context_length=500)
    print(context[:200] + "..." if len(context) > 200 else context)
