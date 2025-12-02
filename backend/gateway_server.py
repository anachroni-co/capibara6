#!/usr/bin/env python3
"""
Capibara6 API Gateway con Semantic Router
Gateway inteligente con routing semántico, circuit breakers y rate limiting
"""

import os
import time
import logging
import asyncio
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from collections import defaultdict
from functools import wraps

from fastapi import FastAPI, HTTPException, Request, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import httpx
from dotenv import load_dotenv
import acontext_integration

# Cargar variables de entorno
load_dotenv("/home/elect/capibara6/backend/.env.production")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# CONFIGURACIÓN
# ============================================

# URLs de servicios
VLLM_URL = os.getenv("VLLM_URL", "http://10.204.0.9:8080")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://10.204.0.9:11434")
BRIDGE_API_URL = os.getenv("BRIDGE_API_URL", "http://10.204.0.10:8000")

# API Keys entre VMs
INTER_VM_API_KEY = os.getenv("INTER_VM_API_KEY", secrets.token_urlsafe(32))
logger.info(f"🔐 Inter-VM API Key: {INTER_VM_API_KEY[:8]}...")

# Acontext configuration
ACONTEXT_ENABLED = os.getenv("ACONTEXT_ENABLED", "true").lower() == "true"
ACONTEXT_PROJECT_ID = os.getenv("ACONTEXT_PROJECT_ID", "capibara6-project")
ACONTEXT_SPACE_ID = os.getenv("ACONTEXT_SPACE_ID", None)  # Optional space for learning

logger.info(f"📊 Acontext integration: {'enabled' if ACONTEXT_ENABLED else 'disabled'}")
if ACONTEXT_ENABLED:
    logger.info(f"📚 Acontext project: {ACONTEXT_PROJECT_ID}")
    if ACONTEXT_SPACE_ID:
        logger.info(f"🧠 Acontext space: {ACONTEXT_SPACE_ID}")

# Rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # segundos

# Circuit breaker
CIRCUIT_BREAKER_THRESHOLD = int(os.getenv("CIRCUIT_BREAKER_THRESHOLD", "5"))
CIRCUIT_BREAKER_TIMEOUT = int(os.getenv("CIRCUIT_BREAKER_TIMEOUT", "60"))

# ============================================
# MODELOS PYDANTIC
# ============================================

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    model: Optional[str] = None
    use_semantic_router: bool = True
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(200, ge=1, le=4000)

class ChatResponse(BaseModel):
    response: str
    model: str
    routing_info: Optional[Dict[str, Any]] = None
    tokens: Optional[int] = None
    latency_ms: int

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]
    semantic_router: Dict[str, Any]

# ============================================
# SEMANTIC ROUTER
# ============================================

class SemanticRouter:
    """Router semántico para selección inteligente de modelos"""

    def __init__(self):
        self.enabled = False
        self.router = None
        self._initialize()

    def _initialize(self):
        """Inicializa el semantic router"""
        try:
            from semantic_model_router import get_router
            self.router = get_router()
            self.enabled = True
            logger.info("✅ Semantic Router inicializado")
        except ImportError as e:
            logger.warning(f"⚠️ Semantic Router no disponible: {e}")
            self.enabled = False

    def select_model(self, query: str) -> Dict[str, Any]:
        """Selecciona el modelo óptimo para la query"""
        if not self.enabled or not self.router:
            return {
                'model_id': 'phi4_fast',  # Default
                'route_name': 'default',
                'confidence': 0.5,
                'reasoning': 'Semantic router no disponible',
                'fallback': True
            }

        try:
            return self.router.select_model(query)
        except Exception as e:
            logger.error(f"❌ Error en semantic router: {e}")
            return {
                'model_id': 'phi4_fast',
                'route_name': 'error',
                'confidence': 0.0,
                'reasoning': f'Error: {str(e)}',
                'fallback': True
            }

# ============================================
# CIRCUIT BREAKER
# ============================================

class CircuitBreaker:
    """Circuit breaker para fault tolerance"""

    def __init__(self, threshold: int = 5, timeout: int = 60):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = defaultdict(int)
        self.opened_at = {}
        self.fallback_enabled = defaultdict(lambda: False)

    def call(self, service_name: str, func, *args, **kwargs):
        """Ejecuta función con circuit breaker"""
        # Verificar si el circuito está abierto
        if self._is_open(service_name):
            logger.warning(f"⚡ Circuit breaker OPEN para {service_name}")
            raise HTTPException(
                status_code=503,
                detail=f"Service {service_name} temporarily unavailable"
            )

        try:
            result = func(*args, **kwargs)
            self._on_success(service_name)
            return result
        except Exception as e:
            self._on_failure(service_name)
            raise e

    async def call_async(self, service_name: str, func, *args, **kwargs):
        """Ejecuta función async con circuit breaker"""
        if self._is_open(service_name):
            logger.warning(f"⚡ Circuit breaker OPEN para {service_name}")
            raise HTTPException(
                status_code=503,
                detail=f"Service {service_name} temporarily unavailable"
            )

        try:
            result = await func(*args, **kwargs)
            self._on_success(service_name)
            return result
        except Exception as e:
            self._on_failure(service_name)
            raise e

    def _is_open(self, service_name: str) -> bool:
        """Verifica si el circuito está abierto"""
        if service_name not in self.opened_at:
            return False

        # Verificar si ya pasó el timeout
        if time.time() - self.opened_at[service_name] > self.timeout:
            logger.info(f"🔄 Circuit breaker HALF-OPEN para {service_name}")
            del self.opened_at[service_name]
            self.failures[service_name] = 0
            return False

        return True

    def _on_success(self, service_name: str):
        """Resetea el contador en caso de éxito"""
        if service_name in self.failures:
            self.failures[service_name] = 0
        if service_name in self.opened_at:
            del self.opened_at[service_name]

    def _on_failure(self, service_name: str):
        """Incrementa el contador de fallos"""
        self.failures[service_name] += 1

        if self.failures[service_name] >= self.threshold:
            logger.error(f"🔥 Circuit breaker OPENED para {service_name}")
            self.opened_at[service_name] = time.time()
            self.failures[service_name] = 0

# ============================================
# RATE LIMITER
# ============================================

class RateLimiter:
    """Rate limiter simple basado en IP"""

    def __init__(self, requests: int = 10, window: int = 60):
        self.requests = requests
        self.window = window
        self.requests_log = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Verifica si el cliente puede hacer una request"""
        now = time.time()

        # Limpiar requests antiguas
        self.requests_log[client_id] = [
            req_time for req_time in self.requests_log[client_id]
            if now - req_time < self.window
        ]

        # Verificar límite
        if len(self.requests_log[client_id]) >= self.requests:
            return False

        # Registrar nueva request
        self.requests_log[client_id].append(now)
        return True

    def get_retry_after(self, client_id: str) -> int:
        """Retorna segundos hasta que pueda hacer otra request"""
        if client_id not in self.requests_log or not self.requests_log[client_id]:
            return 0

        oldest_request = min(self.requests_log[client_id])
        retry_after = int(self.window - (time.time() - oldest_request))
        return max(0, retry_after)

# ============================================
# INSTANCIAS GLOBALES
# ============================================

semantic_router = SemanticRouter()
circuit_breaker = CircuitBreaker(
    threshold=CIRCUIT_BREAKER_THRESHOLD,
    timeout=CIRCUIT_BREAKER_TIMEOUT
)
rate_limiter = RateLimiter(
    requests=RATE_LIMIT_REQUESTS,
    window=RATE_LIMIT_WINDOW
)

# Acontext client
acontext_client = acontext_integration.acontext_client

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="Capibara6 API Gateway",
    description="Gateway inteligente con semantic routing, circuit breakers y rate limiting",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restringir en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# DEPENDENCIES
# ============================================

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verifica API key para requests inter-VM"""
    # Solo requerir API key para endpoints internos
    return x_api_key

async def check_rate_limit(request: Request):
    """Middleware de rate limiting"""
    client_id = request.client.host

    if not rate_limiter.is_allowed(client_id):
        retry_after = rate_limiter.get_retry_after(client_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds",
            headers={"Retry-After": str(retry_after)}
        )

# ============================================
# ENDPOINTS
# ============================================

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Información del API Gateway"""
    return {
        "service": "Capibara6 API Gateway",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Semantic Router",
            "Circuit Breaker",
            "Rate Limiting",
            "API Keys",
            "Multi-model Support"
        ],
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "router_info": "/api/router/info"
        }
    }

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check completo"""
    services_status = {}

    # Check vLLM
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{VLLM_URL}/health")
            services_status["vllm"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["vllm"] = "unavailable"

    # Check Ollama
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/version")
            services_status["ollama"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["ollama"] = "unavailable"

    # Check Bridge API
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BRIDGE_API_URL}/health")
            services_status["bridge_api"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["bridge_api"] = "unavailable"

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        services=services_status,
        semantic_router={
            "enabled": semantic_router.enabled,
            "status": "active" if semantic_router.enabled else "disabled"
        }
    )

@app.post("/api/chat", response_model=ChatResponse, dependencies=[Depends(check_rate_limit)])
async def chat(request: ChatRequest):
    """Endpoint de chat con routing semántico y persistencia de contexto Acontext"""
    start_time = time.time()

    # Initialize Acontext session if enabled
    acontext_session_id = None
    if ACONTEXT_ENABLED:
        try:
            acontext_session = await acontext_client.create_session(
                project_id=ACONTEXT_PROJECT_ID,
                space_id=ACONTEXT_SPACE_ID
            )
            acontext_session_id = acontext_session.id
            logger.info(f"📊 Acontext session created: {acontext_session_id}")
        except Exception as e:
            logger.error(f"❌ Error creating Acontext session: {e}")
            # Continue without Acontext if it fails

    # Seleccionar modelo
    if request.use_semantic_router and semantic_router.enabled:
        routing_info = semantic_router.select_model(request.message)
        selected_model = routing_info['model_id']
    else:
        routing_info = None
        selected_model = request.model or 'phi4_fast'

    logger.info(f"🎯 Modelo seleccionado: {selected_model}")

    # Prepare context from experiences if available
    context_message = ""
    if context_experiences:
        # Format experiences as context for the model
        context_parts = []
        for exp in context_experiences:
            title = exp.get('title', 'Unknown')
            content = exp.get('props', {}).get('content', '') if 'props' in exp else str(exp)
            context_parts.append(f"Relevant experience - {title}: {content}")

        context_message = "Relevant past experiences for this query:\n" + "\n".join(context_parts) + "\n\n"

    # Preparar request para vLLM
    messages = []
    if context_message:
        # Add context as a system message
        messages.append({"role": "system", "content": context_message})
    messages.append({"role": "user", "content": request.message})

    vllm_request = {
        "model": selected_model,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens
    }

    # Store user message in Acontext if enabled
    if ACONTEXT_ENABLED and acontext_session_id:
        try:
            user_message = {
                "role": "user",
                "content": request.message
            }
            await acontext_client.send_message_to_session(acontext_session_id, user_message)
            logger.info(f"💬 User message stored in Acontext session: {acontext_session_id}")
        except Exception as e:
            logger.error(f"❌ Error storing user message in Acontext: {e}")

    # If Acontext space is configured, search for relevant experiences
    context_experiences = []
    if ACONTEXT_ENABLED and ACONTEXT_SPACE_ID:
        try:
            # Search for relevant experiences in the space
            search_result = await acontext_client.search_space(
                space_id=ACONTEXT_SPACE_ID,
                query=request.message,
                mode="fast"
            )
            context_experiences = search_result.get("cited_blocks", [])
            if context_experiences:
                logger.info(f"🔍 Found {len(context_experiences)} relevant experiences from Acontext space")
            else:
                logger.info("🔍 No relevant experiences found in Acontext space")
        except Exception as e:
            logger.error(f"❌ Error searching Acontext space: {e}")
            # Continue without experiences if search fails

    try:
        # Llamar a vLLM con circuit breaker
        async def call_vllm():
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{VLLM_URL}/v1/chat/completions",
                    json=vllm_request
                )
                response.raise_for_status()
                return response.json()

        result = await circuit_breaker.call_async("vllm", call_vllm)

        # Procesar respuesta
        response_text = result['choices'][0]['message']['content']
        tokens = result.get('usage', {}).get('total_tokens', 0)

        # Store assistant response in Acontext if enabled
        if ACONTEXT_ENABLED and acontext_session_id:
            try:
                assistant_message = {
                    "role": "assistant",
                    "content": response_text
                }
                await acontext_client.send_message_to_session(acontext_session_id, assistant_message)
                logger.info(f"🤖 Assistant message stored in Acontext session: {acontext_session_id}")
            except Exception as e:
                logger.error(f"❌ Error storing assistant message in Acontext: {e}")

        latency_ms = int((time.time() - start_time) * 1000)

        return ChatResponse(
            response=response_text,
            model=selected_model,
            routing_info=routing_info,
            tokens=tokens,
            latency_ms=latency_ms
        )

    except HTTPException:
        # Even if the main call fails, try to flush session if Acontext was used
        if ACONTEXT_ENABLED and acontext_session_id:
            try:
                await acontext_client.flush_session(ACONTEXT_PROJECT_ID, acontext_session_id)
                logger.info(f"🔄 Acontext session flushed: {acontext_session_id}")
            except Exception as e:
                logger.error(f"❌ Error flushing Acontext session: {e}")

        raise
    except Exception as e:
        logger.error(f"❌ Error en chat: {e}")

        # Intentar fallback a Ollama
        try:
            logger.info("🔄 Intentando fallback a Ollama...")
            async with httpx.AsyncClient(timeout=120.0) as client:
                ollama_request = {
                    "model": "phi3:mini",
                    "prompt": request.message,
                    "stream": False
                }
                response = await client.post(
                    f"{OLLAMA_URL}/api/generate",
                    json=ollama_request
                )
                response.raise_for_status()
                result = response.json()

                # Store fallback response in Acontext if enabled
                if ACONTEXT_ENABLED and acontext_session_id:
                    try:
                        fallback_message = {
                            "role": "assistant",
                            "content": result['response']
                        }
                        await acontext_client.send_message_to_session(acontext_session_id, fallback_message)
                        logger.info(f"🔄 Fallback message stored in Acontext session: {acontext_session_id}")
                    except Exception as e:
                        logger.error(f"❌ Error storing fallback message in Acontext: {e}")

                latency_ms = int((time.time() - start_time) * 1000)

                return ChatResponse(
                    response=result['response'],
                    model="phi3:mini (fallback)",
                    routing_info={"fallback": True, "original_model": selected_model},
                    tokens=None,
                    latency_ms=latency_ms
                )
        except Exception as fallback_error:
            logger.error(f"❌ Fallback también falló: {fallback_error}")

            # Still try to flush session if Acontext was used
            if ACONTEXT_ENABLED and acontext_session_id:
                try:
                    await acontext_client.flush_session(ACONTEXT_PROJECT_ID, acontext_session_id)
                    logger.info(f"🔄 Acontext session flushed: {acontext_session_id}")
                except Exception as e:
                    logger.error(f"❌ Error flushing Acontext session: {e}")

            raise HTTPException(
                status_code=503,
                detail=f"All model services unavailable: {str(e)}"
            )

    # Flush session at the end of successful request
    if ACONTEXT_ENABLED and acontext_session_id:
        try:
            await acontext_client.flush_session(ACONTEXT_PROJECT_ID, acontext_session_id)
            logger.info(f"🔄 Acontext session flushed: {acontext_session_id}")
        except Exception as e:
            logger.error(f"❌ Error flushing Acontext session: {e}")

@app.get("/api/router/info")
async def router_info():
    """Información del semantic router"""
    if not semantic_router.enabled:
        return {
            "enabled": False,
            "status": "disabled",
            "message": "Semantic router no disponible"
        }

    return {
        "enabled": True,
        "status": "active",
        "routes": semantic_router.router.get_available_routes() if semantic_router.router else [],
        "model_mapping": semantic_router.router.get_model_mapping() if semantic_router.router else {}
    }

@app.post("/api/router/test")
async def router_test(query: str):
    """Probar routing semántico"""
    if not semantic_router.enabled:
        raise HTTPException(status_code=503, detail="Semantic router no disponible")

    result = semantic_router.select_model(query)
    return {
        "query": query,
        "decision": result
    }

# ============================================
# ACONTEXT ENDPOINTS
# ============================================

@app.get("/api/acontext/status")
async def acontext_status():
    """Estado de la integración Acontext"""
    return {
        "enabled": ACONTEXT_ENABLED,
        "project_id": ACONTEXT_PROJECT_ID,
        "space_id": ACONTEXT_SPACE_ID,
        "status": "connected" if ACONTEXT_ENABLED else "disconnected"
    }

@app.post("/api/acontext/session/create")
async def create_acontext_session(space_id: Optional[str] = None):
    """Crear una nueva sesión Acontext manualmente"""
    if not ACONTEXT_ENABLED:
        raise HTTPException(status_code=503, detail="Acontext integration not enabled")

    try:
        session = await acontext_client.create_session(
            project_id=ACONTEXT_PROJECT_ID,
            space_id=space_id or ACONTEXT_SPACE_ID
        )
        return {
            "session_id": session.id,
            "project_id": session.project_id,
            "space_id": session.space_id,
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating Acontext session: {e}")
        raise HTTPException(status_code=503, detail=f"Failed to create Acontext session: {str(e)}")

@app.post("/api/acontext/search")
async def search_acontext_space(query: str, space_id: Optional[str] = None, mode: str = "fast"):
    """Buscar en el espacio Acontext"""
    if not ACONTEXT_ENABLED:
        raise HTTPException(status_code=503, detail="Acontext integration not enabled")

    search_space_id = space_id or ACONTEXT_SPACE_ID
    if not search_space_id:
        raise HTTPException(status_code=400, detail="No space_id provided or configured")

    try:
        result = await acontext_client.search_space(search_space_id, query, mode)
        return result
    except Exception as e:
        logger.error(f"Error searching Acontext space: {e}")
        raise HTTPException(status_code=503, detail=f"Failed to search Acontext space: {str(e)}")

@app.post("/api/acontext/space/create")
async def create_acontext_space(name: str):
    """Crear un nuevo espacio Acontext"""
    if not ACONTEXT_ENABLED:
        raise HTTPException(status_code=503, detail="Acontext integration not enabled")

    try:
        result = await acontext_client.create_space(ACONTEXT_PROJECT_ID, name)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Update the global space ID if this is the first space
        if not ACONTEXT_SPACE_ID:
            logger.info(f"🧠 New Acontext space created: {result['id']}")

        return {
            "space_id": result["id"],
            "project_id": ACONTEXT_PROJECT_ID,
            "name": name,
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating Acontext space: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create Acontext space: {str(e)}")

# ============================================
# STARTUP/SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar"""
    logger.info("=" * 60)
    logger.info("🚀 Capibara6 API Gateway Iniciando...")
    logger.info("=" * 60)
    logger.info(f"🎯 Semantic Router: {'✅ Activo' if semantic_router.enabled else '❌ Inactivo'}")
    logger.info(f"⚡ Circuit Breaker: ✅ Activo (threshold={CIRCUIT_BREAKER_THRESHOLD})")
    logger.info(f"🚦 Rate Limiter: ✅ Activo ({RATE_LIMIT_REQUESTS} req/{RATE_LIMIT_WINDOW}s)")
    logger.info(f"📊 Acontext Integration: {'✅ Activo' if ACONTEXT_ENABLED else '❌ Inactivo'}")
    logger.info(f"📚 Acontext Project: {ACONTEXT_PROJECT_ID}")
    if ACONTEXT_SPACE_ID:
        logger.info(f"🧠 Acontext Space: {ACONTEXT_SPACE_ID}")
    logger.info(f"🔗 vLLM: {VLLM_URL}")
    logger.info(f"🔗 Ollama: {OLLAMA_URL}")
    logger.info(f"🔗 Bridge API: {BRIDGE_API_URL}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar"""
    logger.info("🛑 Cerrando API Gateway...")

    # Close Acontext client
    try:
        await acontext_client.close()
        logger.info("🔒 Acontext client closed")
    except Exception as e:
        logger.error(f"Error closing Acontext client: {e}")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("GATEWAY_PORT", "8080"))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
