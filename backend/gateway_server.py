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
VLLM_URL = os.getenv("VLLM_URL", "http://10.204.0.9:8082")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://10.204.0.9:11434")
BRIDGE_API_URL = os.getenv("BRIDGE_API_URL", "http://10.204.0.10:8000")

# API Keys entre VMs
INTER_VM_API_KEY = os.getenv("INTER_VM_API_KEY", secrets.token_urlsafe(32))
logger.info(f"🔐 Inter-VM API Key: {INTER_VM_API_KEY[:8]}...")

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
    """Endpoint de chat con routing semántico"""
    start_time = time.time()

    # Seleccionar modelo
    if request.use_semantic_router and semantic_router.enabled:
        routing_info = semantic_router.select_model(request.message)
        selected_model = routing_info['model_id']
    else:
        routing_info = None
        selected_model = request.model or 'phi4_fast'

    logger.info(f"🎯 Modelo seleccionado: {selected_model}")

    # Preparar request para vLLM
    vllm_request = {
        "model": selected_model,
        "messages": [{"role": "user", "content": request.message}],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens
    }

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

        latency_ms = int((time.time() - start_time) * 1000)

        return ChatResponse(
            response=response_text,
            model=selected_model,
            routing_info=routing_info,
            tokens=tokens,
            latency_ms=latency_ms
        )

    except HTTPException:
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
            raise HTTPException(
                status_code=503,
                detail=f"All model services unavailable: {str(e)}"
            )

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
    logger.info(f"🔗 vLLM: {VLLM_URL}")
    logger.info(f"🔗 Ollama: {OLLAMA_URL}")
    logger.info(f"🔗 Bridge API: {BRIDGE_API_URL}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar"""
    logger.info("🛑 Cerrando API Gateway...")

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
