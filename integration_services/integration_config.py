#!/usr/bin/env python3
"""
Configuración de Integración - RAG + Multimodelos vLLM + Servicios
Contiene las configuraciones de conexión para los 3 sistemas
"""

# Configuración de las VMs del sistema
VM_CONFIG = {
    # models-europe VM: Nuestro servidor actual con vLLM multimodelos
    "models-europe": {
        "name": "models-europe",
        "external_ip": "34.175.48.2",      # IP externa
        "internal_ip": "10.204.0.9",       # IP interna
        "services": {
            "vllm_multimodel": {
                "url": "http://localhost:8082",  # Puerto actual de nuestro multimodelo vLLM
                "description": "Servidor vLLM con 5 modelos ARM-Axion optimizados",
                "models": ["phi4_fast", "mistral_balanced", "qwen_coder", "gemma3_multimodal", "gptoss_complex"]
            }
        }
    },
    
    # rag3 VM: Sistema RAG con Milvus y Nebula Graph
    "rag3": {
        "name": "rag3",
        "external_ip": "",  # Por definir - se debe verificar
        "internal_ip": "10.154.0.2",        # IP interna probable basada en el proxy-cors.js
        "services": {
            "rag_bridge": {
                "url": "http://10.154.0.2:8000",  # URL del bridge de RAG
                "description": "Bridge API para el sistema RAG (Milvus + Nebula)"
            },
            "milvus": {
                "url": "http://10.154.0.2:19530",  # Puerto de Milvus
                "description": "Vector database Milvus para búsqueda semántica"
            },
            "nebula_graph": {
                "url": "http://10.154.0.2:9669",  # Puerto de Nebula Graph
                "description": "Knowledge graph Nebula para relaciones"
            }
        }
    },
    
    # gpt-oss-20b VM: Servicios TTS, MCP y N8n
    "gpt-oss-20b": {
        "name": "gpt-oss-20b",
        "external_ip": "34.175.136.104",   # IP externa encontrada en archivos
        "internal_ip": "",                 # Por determinar
        "services": {
            "tts_kyutai": {
                "url": "http://34.175.136.104:5002",  # Puerto TTS
                "description": "Servicio Kyutai TTS para síntesis de voz"
            },
            "mcp_server": {
                "url": "http://34.175.136.104:5003",  # Puerto MCP
                "description": "Model Context Protocol para enriquecimiento de contexto"
            },
            "n8n_server": {
                "url": "http://34.175.136.104:5678",  # Puerto N8n
                "description": "Servicio N8n para automatización de workflows"
            }
        }
    }
}

# Configuración principal para el conector
INTEGRATION_CONFIG = {
    # URLs principales
    "vllm_endpoint": VM_CONFIG["models-europe"]["services"]["vllm_multimodel"]["url"],
    "rag_bridge_endpoint": VM_CONFIG["rag3"]["services"]["rag_bridge"]["url"],
    "mcp_endpoint": VM_CONFIG["gpt-oss-20b"]["services"]["mcp_server"]["url"],
    "tts_endpoint": VM_CONFIG["gpt-oss-20b"]["services"]["tts_kyutai"]["url"],
    
    # Parámetros de conexión
    "connection_timeout": 30,  # segundos
    "max_retries": 3,
    "retry_delay": 1,  # segundos
    
    # Configuración de contexto
    "context_enrichment_threshold": 0.7,  # Umbral para usar MCP
    "rag_detection_threshold": 0.5,       # Umbral para usar RAG
    "max_context_tokens": 2000,           # Máximo de tokens para contexto
    "use_cache": True,
    "cache_ttl": 300,  # 5 minutos
    
    # Configuración de modelos
    "model_routing": {
        "general": ["phi4_fast"],
        "technical": ["mistral_balanced", "qwen_coder"],
        "coding": ["qwen_coder"],
        "multimodal": ["gemma3_multimodal"],
        "expert": ["gptoss_complex"]
    },
    
    # Configuración de optimización TOON (Token Optimization)
    "toon_config": {
        "enabled": True,
        "min_sources_for_toon": 5,
        "compression_ratio": 0.6,  # 60% del tamaño original
        "format": "compact"  # "compact", "structured", "json"
    },
    
    # Configuración de seguridad
    "auth_required": False,  # En entornos de producción se debería habilitar
    "rate_limiting": {
        "enabled": True,
        "requests_per_minute": 60,
        "burst_limit": 10
    }
}

# Configuración específica para pruebas
TEST_CONFIG = {
    "test_queries": [
        "¿Cómo funciona el modelo phi4_fast?",
        "Explica cómo implementar una red neuronal en Python",
        "¿Cuál es la diferencia entre un modelo multimodal y un modelo de texto?",
        "¿Qué es el razonamiento complejo en IA?",
        "Crea un ejemplo de código Python para manejar vectores",
        "Responde en español sobre técnicas de optimización ARM"
    ],
    
    "test_scenarios": [
        {
            "name": "Consulta general",
            "query": "Hola, ¿cómo estás?",
            "expected_model": "phi4_fast",
            "use_rag": False
        },
        {
            "name": "Consulta técnica",
            "query": "Explica cómo funciona un transformer en IA",
            "expected_model": "mistral_balanced",
            "use_rag": True
        },
        {
            "name": "Consulta de programación",
            "query": "Muestra un ejemplo de código Python con async/await",
            "expected_model": "qwen_coder",
            "use_rag": False
        }
    ]
}

# Validación de configuración
def validate_config():
    """Validar que la configuración es correcta"""
    required_fields = [
        "vllm_endpoint",
        "rag_bridge_endpoint", 
        "mcp_endpoint",
        "tts_endpoint"
    ]
    
    for field in required_fields:
        if not INTEGRATION_CONFIG.get(field):
            raise ValueError(f"Campo requerido faltante en configuración: {field}")
    
    print("✅ Configuración validada correctamente")


if __name__ == "__main__":
    validate_config()
    print("Configuración de integración:")
    print(json.dumps(INTEGRATION_CONFIG, indent=2, ensure_ascii=False))