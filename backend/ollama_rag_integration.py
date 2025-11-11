#!/usr/bin/env python3
"""
Integración entre Ollama y sistema RAG

Este módulo permite que las respuestas de Ollama sean enriquecidas
con información del sistema RAG cuando se detecte que la consulta
requiere datos personales del usuario.
"""

import logging
import re
from typing import Dict, Any, Optional, Tuple
from ollama_client import OllamaClient
from rag_client import RAGClient

logger = logging.getLogger(__name__)


class OllamaRAGIntegration:
    """Integración entre Ollama y RAG para respuestas enriquecidas"""

    # Patrones que indican necesidad de consultar RAG
    RAG_TRIGGERS = [
        r"\b(mi|mis|yo|he|tengo|recuerdo)\b",  # Referencias personales
        r"\b(dije|hablé|comenté|mencioné)\b",  # Referencias a conversaciones
        r"\b(guardé|guardado|archivé)\b",  # Referencias a archivos
        r"\b(conversación|chat|mensaje)\b",  # Conversaciones
        r"\b(archivo|documento|pdf|imagen)\b",  # Archivos
        r"\b(contacto|persona|amigo)\b",  # Relaciones
        r"qué (tengo|hay|dijiste|dije)",  # Preguntas sobre datos
        r"(muéstrame|busca|encuentra) (mi|mis)",  # Búsquedas personales
    ]

    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        rag_client: Optional[RAGClient] = None,
        rag_threshold: float = 0.3,  # Score mínimo para usar RAG
        context_max_length: int = 1500,
    ):
        """
        Inicializar integración Ollama-RAG

        Args:
            ollama_client: Cliente Ollama configurado
            rag_client: Cliente RAG configurado
            rag_threshold: Umbral para decidir si usar RAG
            context_max_length: Longitud máxima del contexto RAG
        """
        self.ollama_client = ollama_client
        self.rag_client = rag_client or RAGClient()
        self.rag_threshold = rag_threshold
        self.context_max_length = context_max_length

        logger.info("OllamaRAGIntegration initialized")

    def should_use_rag(self, query: str) -> Tuple[bool, float]:
        """
        Determinar si una consulta requiere información del RAG

        Args:
            query: Consulta del usuario

        Returns:
            Tuple (should_use, confidence_score)
        """
        query_lower = query.lower()
        matches = 0

        for pattern in self.RAG_TRIGGERS:
            if re.search(pattern, query_lower, re.IGNORECASE):
                matches += 1

        # Score basado en número de coincidencias
        score = min(matches * 0.2, 1.0)

        should_use = score >= self.rag_threshold

        logger.debug(f"RAG decision for '{query[:50]}...': {should_use} (score: {score:.2f})")

        return should_use, score

    def enrich_prompt_with_rag(
        self,
        user_prompt: str,
        n_results: int = 3
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Enriquecer prompt con contexto del RAG

        Args:
            user_prompt: Prompt original del usuario
            n_results: Número de resultados RAG a incluir

        Returns:
            Tuple (enriched_prompt, rag_data)
        """
        should_use, confidence = self.should_use_rag(user_prompt)

        if not should_use:
            logger.info("RAG not needed for this query")
            return user_prompt, None

        # Obtener contexto del RAG
        rag_context = self.rag_client.get_context_for_llm(
            user_query=user_prompt,
            max_context_length=self.context_max_length,
            n_results=n_results
        )

        if not rag_context:
            logger.warning("RAG query returned empty context")
            return user_prompt, None

        # Construir prompt enriquecido
        enriched_prompt = f"""Contexto de información personal del usuario:
{rag_context}

---

Basándote en el contexto anterior, responde a la siguiente pregunta:
{user_prompt}

Si el contexto contiene información relevante, úsala en tu respuesta.
Si no hay información relevante en el contexto, responde normalmente."""

        rag_data = {
            "used_rag": True,
            "confidence": confidence,
            "context_length": len(rag_context)
        }

        logger.info(f"Prompt enriched with RAG context ({len(rag_context)} chars)")

        return enriched_prompt, rag_data

    def generate_with_rag(
        self,
        prompt: str,
        model_tier: Optional[str] = None,
        use_rag: bool = True,
        **ollama_options: Any
    ) -> Dict[str, Any]:
        """
        Generar respuesta con Ollama, usando RAG si es necesario

        Args:
            prompt: Prompt del usuario
            model_tier: Tier del modelo Ollama (fast_response, balanced, complex)
            use_rag: Si permitir el uso de RAG
            **ollama_options: Opciones adicionales para Ollama

        Returns:
            Dict con respuesta y metadatos
        """
        if not self.ollama_client:
            raise ValueError("OllamaClient no configurado")

        rag_data = None

        # Enriquecer con RAG si está habilitado
        if use_rag:
            enriched_prompt, rag_data = self.enrich_prompt_with_rag(prompt)
        else:
            enriched_prompt = prompt

        # Generar respuesta con Ollama
        ollama_response = self.ollama_client.generate_with_fallback(
            prompt=enriched_prompt,
            model_tier=model_tier,
            **ollama_options
        )

        # Combinar respuesta con metadata RAG
        response = {
            "response": ollama_response.get("response", ""),
            "success": ollama_response.get("success", False),
            "model": ollama_response.get("model"),
            "rag_used": rag_data is not None,
        }

        if rag_data:
            response["rag_metadata"] = rag_data

        if "error" in ollama_response:
            response["error"] = ollama_response["error"]

        return response

    def stream_with_rag(
        self,
        prompt: str,
        model_tier: str,
        use_rag: bool = True,
        **ollama_options: Any
    ):
        """
        Generar respuesta en streaming con Ollama y RAG

        Args:
            prompt: Prompt del usuario
            model_tier: Tier del modelo
            use_rag: Si usar RAG
            **ollama_options: Opciones adicionales

        Yields:
            Chunks de texto
        """
        if not self.ollama_client:
            raise ValueError("OllamaClient no configurado")

        # Enriquecer con RAG si está habilitado
        if use_rag:
            enriched_prompt, rag_data = self.enrich_prompt_with_rag(prompt)
            # Yield metadata inicial si se usó RAG
            if rag_data:
                yield f"[RAG: {rag_data['confidence']:.2f} confidence]\n\n"
        else:
            enriched_prompt = prompt

        # Stream desde Ollama
        for chunk in self.ollama_client.stream_with_model(
            prompt=enriched_prompt,
            model_tier=model_tier,
            **ollama_options
        ):
            yield chunk


def create_integrated_client(
    ollama_config: Dict[str, Any],
    rag_url: Optional[str] = None
) -> OllamaRAGIntegration:
    """
    Factory para crear cliente integrado Ollama-RAG

    Args:
        ollama_config: Configuración de Ollama (model_config.json)
        rag_url: URL del servidor RAG (opcional)

    Returns:
        Cliente integrado configurado
    """
    ollama_client = OllamaClient(ollama_config)
    rag_client = RAGClient(base_url=rag_url)

    return OllamaRAGIntegration(
        ollama_client=ollama_client,
        rag_client=rag_client
    )


if __name__ == "__main__":
    # Demo de uso
    import json
    logging.basicConfig(level=logging.INFO)

    # Cargar configuración de Ollama
    with open("/home/elect/capibara6/model_config.json") as f:
        ollama_config = json.load(f)

    # Crear cliente integrado
    integrated_client = create_integrated_client(ollama_config)

    # Test: consulta que NO debería usar RAG
    print("=== Test 1: Pregunta general ===")
    response1 = integrated_client.generate_with_rag(
        prompt="¿Qué es machine learning?",
        model_tier="fast_response"
    )
    print(f"RAG usado: {response1['rag_used']}")
    print(f"Respuesta: {response1['response'][:100]}...")

    # Test: consulta que SÍ debería usar RAG
    print("\n=== Test 2: Pregunta personal ===")
    response2 = integrated_client.generate_with_rag(
        prompt="¿Qué he comentado sobre machine learning?",
        model_tier="balanced"
    )
    print(f"RAG usado: {response2['rag_used']}")
    if response2.get('rag_metadata'):
        print(f"RAG confidence: {response2['rag_metadata']['confidence']:.2f}")
    print(f"Respuesta: {response2['response'][:100]}...")
