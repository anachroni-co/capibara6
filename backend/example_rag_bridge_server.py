#!/usr/bin/env python3
"""
Ejemplo de servidor Flask con integración Ollama-RAG

Este es un ejemplo completo de cómo integrar el bridge RAG-Ollama
en un servidor Flask existente.
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import logging
import os
import sys

# Añadir path si es necesario
sys.path.insert(0, os.path.dirname(__file__))

from ollama_rag_integration import create_integrated_client
from rag_client import RAGClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app Flask
app = Flask(__name__)
CORS(app)

# Cargar configuración de Ollama
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "model_config.json"
)

with open(CONFIG_PATH) as f:
    ollama_config = json.load(f)

# Crear cliente integrado Ollama-RAG
RAG_URL = os.getenv("RAG_API_URL", "http://10.154.0.2:8000")
integrated_client = create_integrated_client(
    ollama_config=ollama_config,
    rag_url=RAG_URL
)

logger.info(f"Servidor iniciado con RAG URL: {RAG_URL}")


# ============================================================
# ENDPOINTS
# ============================================================

@app.route("/")
def index():
    """Información del servidor"""
    return jsonify({
        "name": "Capibara6 Server with RAG Bridge",
        "version": "2.0.0",
        "features": {
            "ollama": True,
            "rag_integration": True,
            "streaming": True
        },
        "endpoints": {
            "chat": "/api/chat",
            "stream": "/api/chat/stream",
            "rag_status": "/api/rag/status",
            "health": "/api/health"
        }
    })


@app.route("/api/health")
def health():
    """Health check del servidor y dependencias"""
    try:
        # Verificar RAG
        rag_client = RAGClient(base_url=RAG_URL)
        rag_health = rag_client.health_check()

        # Verificar Ollama
        ollama_endpoint = ollama_config.get("api_settings", {}).get("ollama_endpoint")
        import requests
        ollama_response = requests.get(f"{ollama_endpoint}/api/tags", timeout=5)
        ollama_ok = ollama_response.status_code == 200

        return jsonify({
            "status": "healthy",
            "services": {
                "ollama": "ok" if ollama_ok else "error",
                "rag": rag_health.get("status", "error"),
                "rag_services": rag_health.get("services", {})
            },
            "rag_url": RAG_URL
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint principal de chat con integración RAG

    Request body:
    {
        "message": "¿Qué he comentado sobre IA?",
        "model_tier": "balanced",  // opcional: fast_response, balanced, complex, auto
        "use_rag": true,           // opcional: default true
        "stream": false            // opcional: default false
    }
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Missing 'message' field"
            }), 400

        user_message = data["message"]
        model_tier = data.get("model_tier", "auto")
        use_rag = data.get("use_rag", True)
        stream = data.get("stream", False)

        logger.info(f"Chat request: '{user_message[:50]}...' (model: {model_tier}, rag: {use_rag})")

        # Generar respuesta
        response = integrated_client.generate_with_rag(
            prompt=user_message,
            model_tier=model_tier,
            use_rag=use_rag
        )

        if not response.get("success"):
            return jsonify({
                "error": response.get("error", "Generation failed")
            }), 500

        # Preparar respuesta
        result = {
            "response": response["response"],
            "model": response["model"],
            "rag_used": response["rag_used"],
            "metadata": {
                "model_tier": model_tier,
                "use_rag": use_rag
            }
        }

        if response.get("rag_metadata"):
            result["rag_metadata"] = response["rag_metadata"]

        logger.info(f"Response generated (model: {response['model']}, rag: {response['rag_used']})")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    """
    Endpoint de chat con streaming

    Request body:
    {
        "message": "Explícame machine learning",
        "model_tier": "balanced",
        "use_rag": true
    }
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data["message"]
        model_tier = data.get("model_tier", "balanced")
        use_rag = data.get("use_rag", True)

        logger.info(f"Stream request: '{user_message[:50]}...' (model: {model_tier})")

        def generate():
            """Generator para streaming"""
            try:
                for chunk in integrated_client.stream_with_rag(
                    prompt=user_message,
                    model_tier=model_tier,
                    use_rag=use_rag
                ):
                    # Enviar chunk como SSE (Server-Sent Events)
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"

                # Enviar señal de fin
                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                logger.error(f"Error in streaming: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        logger.error(f"Error in stream endpoint: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/rag/status")
def rag_status():
    """Verificar estado de la conexión RAG"""
    try:
        rag_client = RAGClient(base_url=RAG_URL)
        health = rag_client.health_check()

        return jsonify({
            "connected": health.get("status") == "healthy",
            "rag_url": RAG_URL,
            "details": health
        })
    except Exception as e:
        logger.error(f"RAG status check failed: {e}")
        return jsonify({
            "connected": False,
            "rag_url": RAG_URL,
            "error": str(e)
        }), 503


@app.route("/api/rag/search", methods=["POST"])
def rag_search():
    """
    Búsqueda directa en el sistema RAG

    Request body:
    {
        "query": "machine learning",
        "n_results": 5,
        "use_graph": true
    }
    """
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' field"}), 400

        query = data["query"]
        n_results = data.get("n_results", 5)
        use_graph = data.get("use_graph", True)

        rag_client = RAGClient(base_url=RAG_URL)
        result = rag_client.search_rag(
            query=query,
            n_results=n_results,
            use_graph=use_graph
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in RAG search: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/models")
def list_models():
    """Listar modelos de Ollama disponibles"""
    try:
        import requests
        ollama_endpoint = ollama_config.get("api_settings", {}).get("ollama_endpoint")
        response = requests.get(f"{ollama_endpoint}/api/tags", timeout=5)
        response.raise_for_status()

        models_data = response.json()
        models = models_data.get("models", [])

        return jsonify({
            "models": [
                {
                    "name": m["name"],
                    "size": m.get("size", 0),
                    "modified_at": m.get("modified_at")
                }
                for m in models
            ],
            "total": len(models)
        })

    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return jsonify({
            "error": str(e),
            "models": []
        }), 500


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    logger.info(f"Starting server on port {port}")
    logger.info(f"RAG integration URL: {RAG_URL}")
    logger.info(f"Ollama endpoint: {ollama_config.get('api_settings', {}).get('ollama_endpoint')}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
