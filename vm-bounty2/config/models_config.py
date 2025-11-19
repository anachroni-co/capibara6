#!/usr/bin/env python3
"""
Configuración de Modelos - Capibara6 Consensus
Soporte para múltiples modelos con diferentes configuraciones
"""

import os
from typing import Dict, List, Any

# ============================================
# CONFIGURACIÓN DE MODELOS
# ============================================

MODELS_CONFIG = {
    'gpt-oss-20b': {
        'name': 'GPT-OSS-20B',
        'base_model': 'GPT-OSS-20B',
        'server_url': 'http://34.12.166.76:8000/v1',  # vLLM endpoint
        'type': 'vllm',
        'hardware': 'GPU',
        'status': 'active',
        'priority': 2,
        'prompt_template': {
            'system': 'Eres un asistente experto en programación y análisis técnico.',
            'user': '{prompt}',
            'assistant': '',
            'stop_tokens': ['<|end|>', '']
        },
        'parameters': {
            'n_predict': 200,
            'temperature': 0.7,
            'top_p': 0.9,
            'repeat_penalty': 1.2,
            'stream': True
        }
    },

    'phi4': {
        'name': 'Phi-4 Mini',
        'base_model': 'Microsoft Phi-4 Mini (14B)',  # Upgraded to Phi-4 with more parameters
        'server_url': 'http://34.12.166.76:8001/v1',  # vLLM endpoint for Phi-4
        'type': 'vllm',
        'hardware': 'GPU',
        'status': 'active',
        'priority': 3,
        'prompt_template': {
            'system': 'You are a helpful AI assistant. Respond concisely and accurately.',
            'user': '{prompt}',
            'assistant': '',
            'stop_tokens': ['<|end|>', '']
        },
        'parameters': {
            'n_predict': 120,  # Updated for longer context
            'temperature': 0.5,
            'top_p': 0.85,
            'repeat_penalty': 1.2,
            'stream': True
        }
    },

    'qwen2.5-coder': {
        'name': 'Qwen2.5-Coder 1.5B',
        'base_model': 'Qwen/Qwen2.5-Coder-1.5B-Instruct',
        'server_url': 'http://34.12.166.76:8002/v1',  # vLLM endpoint for the code model
        'type': 'vllm',
        'hardware': 'GPU',
        'status': 'active',
        'priority': 2,
        'prompt_template': {
            'system': 'You are an expert code assistant. Provide accurate, efficient, and well-documented code solutions.',
            'user': '{prompt}',
            'assistant': '',
            'stop_tokens': ['<|end|>', '']
        },
        'parameters': {
            'n_predict': 200,  # Suitable for code tasks
            'temperature': 0.3,
            'top_p': 0.9,
            'repeat_penalty': 1.1,
            'stream': True
        }
    },

    'mixtral': {
        'name': 'Mixtral 8x7B',
        'base_model': 'Mixtral-8x7B-Instruct-v0.1',
        'server_url': 'http://34.12.166.76:8003/v1',  # vLLM endpoint for Mixtral
        'type': 'vllm',
        'hardware': 'GPU',
        'status': 'active',
        'priority': 2,
        'prompt_template': {
            'system': 'You are a creative and multilingual AI assistant. Provide detailed and engaging responses.',
            'user': '[INST] {prompt} [/INST]',
            'assistant': '',
            'stop_tokens': ['</s>', '[/INST]', '']
        },
        'parameters': {
            'n_predict': 250,
            'temperature': 0.7,
            'top_p': 0.95,
            'repeat_penalty': 1.1,
            'stream': True
        }
    }
}

# ============================================
# PLANTILLAS DE PROMPTS POR CATEGORÍA
# ============================================

PROMPT_TEMPLATES = {
    'general': {
        'name': 'General',
        'description': 'Conversación general y preguntas abiertas',
        'system_prompt': 'Eres un asistente útil y preciso. Responde de manera clara y concisa.',
        'models': ['phi4', 'qwen2.5-coder'],
        'requires_execution': False,
        'execution_context': 'none'
    },

    'coding': {
        'name': 'Programación',
        'description': 'Ayuda con código, debugging y desarrollo',
        'system_prompt': 'Eres un experto programador. Proporciona código limpio, bien documentado y con ejemplos. Si se requiere ejecución real del código, prepara código que pueda ser ejecutado en un entorno seguro de E2B.',
        'models': ['qwen2.5-coder', 'gpt-oss-20b'],
        'additional_instructions': 'Siempre usa bloques de código markdown con el lenguaje especificado. Detecta cuándo se necesita ejecución real del código.',
        'requires_execution': True,
        'execution_context': 'e2b_python'
    },

    'analysis': {
        'name': 'Análisis',
        'description': 'Análisis de datos, investigación y pensamiento crítico',
        'system_prompt': 'Eres un analista experto. Proporciona análisis estructurado, evidencia y conclusiones claras. Si se proporcionan datos para analizar, genera código que pueda ejecutarse en entorno E2B para procesamiento real.',
        'models': ['gpt-oss-20b', 'mixtral'],  # Mejores para análisis complejos
        'additional_instructions': 'Estructura tu respuesta con: 1) Resumen, 2) Análisis detallado, 3) Conclusiones. Genera código para análisis de datos cuando sea relevante.',
        'requires_execution': True,
        'execution_context': 'e2b_data_analysis'
    },

    'creative': {
        'name': 'Creativo',
        'description': 'Escritura creativa, storytelling y contenido',
        'system_prompt': 'Eres un escritor creativo y original. Crea contenido atractivo y bien estructurado.',
        'models': ['mixtral', 'gpt-oss-20b'],
        'additional_instructions': 'Usa un tono apropiado para el contexto y mantén la coherencia narrativa.',
        'requires_execution': False,
        'execution_context': 'none'
    },

    'technical': {
        'name': 'Técnico',
        'description': 'Documentación técnica, arquitectura y sistemas',
        'system_prompt': 'Eres un arquitecto de software experto. Proporciona documentación técnica precisa y detallada. Genera código de ejemplo que pueda ser ejecutado para verificar funcionalidad.',
        'models': ['gpt-oss-20b', 'qwen2.5-coder'],  # Mejores para documentación técnica
        'additional_instructions': 'Incluye diagramas en formato Mermaid cuando sea apropiado. Proporciona código de ejemplo que pueda ejecutarse en entorno E2B.',
        'requires_execution': True,
        'execution_context': 'e2b_code_example'
    }
}

# ============================================
# CONFIGURACIÓN DE CONSENSO
# ============================================

CONSENSUS_CONFIG = {
    'enabled': True,
    'min_models': 2,
    'max_models': 3,
    'voting_method': 'weighted',  # 'simple', 'weighted', 'confidence'
    'model_weights': {
        'phi4': 0.7,      # Modelo rápido y eficiente
        'qwen2.5-coder': 0.8,  # Modelo experto en código
        'gpt-oss-20b': 0.9,    # Modelo más potente
        'mixtral': 0.6      # Buen modelo general
    },
    'fallback_model': 'phi4',  # Modelo de respaldo si falla el consenso
    'timeout': 30  # Segundos para esperar respuestas
}

# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def get_active_models() -> List[str]:
    """Obtiene la lista de modelos activos"""
    return [model_id for model_id, config in MODELS_CONFIG.items()
            if config['status'] == 'active']

def get_model_config(model_id: str) -> Dict[str, Any]:
    """Obtiene la configuración de un modelo específico"""
    return MODELS_CONFIG.get(model_id, {})

def get_prompt_template(template_id: str) -> Dict[str, Any]:
    """Obtiene una plantilla de prompt específica"""
    return PROMPT_TEMPLATES.get(template_id, {})

def get_available_templates() -> List[str]:
    """Obtiene la lista de plantillas disponibles"""
    return list(PROMPT_TEMPLATES.keys())

def get_models_for_template(template_id: str) -> List[str]:
    """Obtiene los modelos recomendados para una plantilla"""
    template = get_prompt_template(template_id)
    return template.get('models', [])

def format_prompt(model_id: str, template_id: str, user_prompt: str) -> str:
    """Formatea un prompt usando la plantilla y configuración del modelo"""
    model_config = get_model_config(model_id)
    template = get_prompt_template(template_id)

    if not model_config or not template:
        return user_prompt

    # Obtener el template del modelo
    model_template = model_config.get('prompt_template', {})
    system_prompt = template.get('system_prompt', model_template.get('system', ''))

    # Verificar si se requiere ejecución de código
    requires_execution = template.get('requires_execution', False)

    if requires_execution:
        execution_context = template.get('execution_context', 'e2b_python')
        execution_instructions = f"\n\nNOTA IMPORTANTE: Esta consulta requiere ejecución de código. El código resultante será ejecutado en un entorno seguro E2B ({execution_context}). Asegúrate de que el código sea funcional y esté listo para ejecución."
        system_prompt += execution_instructions

    # Formatear según el tipo de modelo
    if model_id in ['gpt-oss-20b', 'phi4', 'qwen2.5-coder']:
        # Formato estándar para vLLM
        return f"{system_prompt}\n\n{user_prompt}"
    elif model_id == 'mixtral':
        # Formato específico para Mixtral
        return f"[INST] {system_prompt} {user_prompt} [/INST]"

    return user_prompt

# ============================================
# CONFIGURACIÓN DE DESARROLLO
# ============================================

def get_development_config():
    """Configuración para desarrollo local"""
    return {
        'models': {
            'gpt-oss-20b': {
                **MODELS_CONFIG['gpt-oss-20b'],
                'server_url': 'http://localhost:8000/v1'
            },
            'phi4': {
                **MODELS_CONFIG['phi4'],
                'server_url': 'http://localhost:8001/v1'
            },
            'qwen2.5-coder': {
                **MODELS_CONFIG['qwen2.5-coder'],
                'server_url': 'http://localhost:8002/v1'
            },
            'mixtral': {
                **MODELS_CONFIG['mixtral'],
                'server_url': 'http://localhost:8003/v1'
            }
        },
        'consensus': CONSENSUS_CONFIG
    }

def get_production_config():
    """Configuración para producción"""
    return {
        'models': MODELS_CONFIG,
        'consensus': CONSENSUS_CONFIG
    }

# ============================================
# INFORMACIÓN DEL SISTEMA
# ============================================

def get_system_info():
    """Obtiene información del sistema de modelos"""
    active_models = get_active_models()
    return {
        'total_models': len(MODELS_CONFIG),
        'active_models': len(active_models),
        'models_list': active_models,
        'consensus_enabled': CONSENSUS_CONFIG['enabled'],
        'available_templates': get_available_templates(),
        'hardware_info': {
            model_id: config['hardware']
            for model_id, config in MODELS_CONFIG.items()
            if config['status'] == 'active'
        }
    }

if __name__ == '__main__':
    print("🤖 Configuración de Modelos Capibara6")
    print("=" * 50)

    info = get_system_info()
    print(f"Modelos activos: {info['active_models']}/{info['total_models']}")
    print(f"Consenso habilitado: {info['consensus_enabled']}")
    print(f"Plantillas disponibles: {len(info['available_templates'])}")

    print("\n📋 Modelos configurados:")
    for model_id in info['models_list']:
        config = get_model_config(model_id)
        print(f"  • {config['name']} ({config['hardware']}) - {config['status']}")

    print("\n🎯 Plantillas disponibles:")
    for template_id in info['available_templates']:
        template = get_prompt_template(template_id)
        print(f"  • {template['name']}: {template['description']}")