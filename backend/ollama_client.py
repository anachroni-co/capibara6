#!/usr/bin/env python3
# -*- coding: utf-8 -*-
<<<<<<< HEAD
"""
Cliente HTTP para interactuar con Ollama con selección de modelo y fallback.
"""
=======
"""Cliente HTTP para interactuar con Ollama con selección de modelo y fallback."""
>>>>>>> feature/rag-infra

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Iterable, Optional

import requests  # type: ignore[import-untyped]

from task_classifier import TaskClassifier

logger = logging.getLogger(__name__)


class OllamaClient:
    """Cliente para gestionar peticiones a Ollama con soporte de fallback."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.endpoint = config.get("api_settings", {}).get(
            "ollama_endpoint",
            os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434"),
        )
        self.models = config.get("models", {})

        fallback_cfg = config.get("fallback_strategy", {})
        self.fallback_enabled = fallback_cfg.get(
            "enabled", os.getenv("FALLBACK_ENABLED", "true").lower() == "true"
        )
        self.fallback_order = fallback_cfg.get(
            "order",
            ["fast_response", "balanced", "complex"],
        )

        self.default_tier = os.getenv(
            "DEFAULT_MODEL_TIER",
<<<<<<< HEAD
            config.get("api_settings", {}).get("default_model", "fast_response")
            if config
            else "fast_response",
        ) or "fast_response"
=======
            config.get("api_settings", {}).get("default_model", "fast_response"),
        )
>>>>>>> feature/rag-infra

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, prompt: str, model_tier: str, **options: Any) -> Dict[str, Any]:
        """Generar una respuesta usando el modelo asignado a `model_tier`."""

        model_cfg = self.models.get(model_tier)
        if not model_cfg:
            raise ValueError(f"Modelo no configurado para tier: {model_tier}")

        payload = self._build_payload(prompt, model_cfg, options)
        timeout = self._resolve_timeout(model_cfg, options)

        logger.debug("Solicitando a Ollama modelo %s", model_cfg["name"])
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()

        data = response.json()
        return {
            "success": True,
            "model": model_cfg["name"],
            "response": data.get("response", ""),
            "eval_duration": data.get("eval_duration"),
            "total_duration": data.get("total_duration"),
            "token_count": data.get("eval_count"),
        }

<<<<<<< HEAD
    def generate_with_fallback(
        self, prompt: str, model_tier: Optional[str] = None, **options: Any
    ) -> Dict[str, Any]:
=======
    def generate_with_fallback(self, prompt: str, model_tier: Optional[str] = None, **options: Any) -> Dict[str, Any]:
>>>>>>> feature/rag-infra
        """Generar respuesta con fallback según configuración."""

        selected_tier = model_tier or self.default_tier or "fast_response"
        tiers_to_try = self._resolve_tiers(prompt, selected_tier)
        last_error = None

        for tier in tiers_to_try:
            try:
                return self.generate(prompt, tier, **options)
            except Exception as exc:  # noqa: BLE001 - Propagamos último error
                logger.warning("Error con modelo %s: %s", tier, exc)
                last_error = exc
                continue

        return {
            "success": False,
            "model": None,
            "error": str(last_error) if last_error else "No se pudo generar respuesta",
        }

<<<<<<< HEAD
    def stream_with_model(
        self, prompt: str, model_tier: str, **options: Any
    ) -> Iterable[str]:
=======
    def stream_with_model(self, prompt: str, model_tier: str, **options: Any) -> Iterable[str]:
>>>>>>> feature/rag-infra
        """Generar texto en streaming usando un modelo específico."""

        model_cfg = self.models.get(model_tier)
        if not model_cfg:
            raise ValueError(f"Modelo no configurado para tier: {model_tier}")

        payload = self._build_payload(prompt, model_cfg, options, stream=True)
        timeout = self._resolve_timeout(model_cfg, options)

        with requests.post(
            f"{self.endpoint}/api/generate",
            json=payload,
            timeout=timeout,
            stream=True,
        ) as response:
            response.raise_for_status()

            buffer = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if not chunk:
                    continue
                buffer += chunk
                lines = buffer.split("\n")
                buffer = lines.pop()

                for line in lines:
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        logger.debug("No se pudo parsear línea de streaming: %s", line)
                        continue

                    if data.get("response"):
                        yield data["response"]

                    if data.get("done"):
                        return

            if buffer:
                try:
                    data = json.loads(buffer)
                    if data.get("response"):
                        yield data["response"]
                except json.JSONDecodeError:
<<<<<<< HEAD
                    logger.debug(
                        "No se pudo parsear buffer final de streaming: %s", buffer
                    )
=======
                    logger.debug("No se pudo parsear buffer final de streaming: %s", buffer)
>>>>>>> feature/rag-infra

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

<<<<<<< HEAD
    def _build_payload(
        self,
        prompt: str,
        model_cfg: Dict[str, Any],
        options: Dict[str, Any],
        stream: bool = False,
    ) -> Dict[str, Any]:
=======
    def _build_payload(self, prompt: str, model_cfg: Dict[str, Any], options: Dict[str, Any], stream: bool = False) -> Dict[str, Any]:
>>>>>>> feature/rag-infra
        max_tokens = options.get("max_tokens") or model_cfg.get("max_tokens", 512)

        payload: Dict[str, Any] = {
            "model": model_cfg["name"],
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": options.get("temperature", 0.7),
                "num_predict": min(max_tokens, 2048),
                "top_p": options.get("top_p", 0.9),
                "top_k": options.get("top_k", 40),
            },
        }

        context = options.get("context")
        if context:
            payload["context"] = context

        if options.get("stop"):
            payload["stop"] = options["stop"]

        return payload

    @staticmethod
    def _resolve_timeout(model_cfg: Dict[str, Any], options: Dict[str, Any]) -> float:
        timeout_ms = options.get("timeout") or model_cfg.get("timeout", 10000)
        return float(timeout_ms) / 1000.0

    def _resolve_tiers(self, prompt: str, preferred_tier: str) -> Iterable[str]:
        if preferred_tier == "auto":
            classification = TaskClassifier.classify(prompt)
            preferred_tier = classification.model_tier

        tiers = [preferred_tier]

        if self.fallback_enabled:
            tiers.extend([tier for tier in self.fallback_order if tier not in tiers])

        return tiers


