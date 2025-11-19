# Current Models Summary - Capibara6 System

## Overview
This document provides a complete summary of all models currently configured in the Capibara6 system after the vLLM migration.

## JavaScript/Node.js API Layer Models (model_config.json)
These models are used by the main API endpoints:

1. **fast_response**: `phi4:mini`
   - Description: Modelo más rápido para respuestas simples
   - Use cases: preguntas simples, respuestas rápidas, chistes, saludos, respuestas directas
   - Max tokens: 512
   - Timeout: 8000ms

2. **balanced**: `qwen2.3-coder:1.5b`  
   - Description: Modelo experto en código y tareas técnicas
   - Use cases: explicaciones, análisis intermedio, redacción, resumen corto, programación, análisis técnico
   - Max tokens: 1024
   - Timeout: 20000ms

3. **complex**: `gpt-oss:20b`
   - Description: Modelo más potente para tareas complejas
   - Use cases: análisis profundo, razonamiento complejo, planificación, análisis técnico
   - Max tokens: 2048
   - Timeout: 240000ms

## Python Backend Models (models_config.py)
These models are used by the Python backend services:

### Active Models (4/4 active):
1. **gpt-oss-20b**
   - Name: GPT-OSS-20B
   - Base Model: GPT-OSS-20B
   - Type: llama_cpp
   - Hardware: GPU
   - Status: active
   - Priority: 2
   - Server URL: http://34.175.215.109:8080/completion

2. **phi** (now Phi-4)
   - Name: Phi-4 Mini
   - Base Model: Microsoft Phi-4 Mini (14B) 
   - Type: vllm
   - Hardware: GPU
   - Status: active
   - Priority: 3
   - Server URL: http://34.175.215.109:8000/v1

3. **qwen2.3-coder**
   - Name: Qwen2.3-Coder 1.5B
   - Base Model: Qwen/Qwen2.5-Coder-1.5B-Instruct
   - Type: vllm
   - Hardware: GPU
   - Status: active
   - Priority: 2
   - Server URL: http://34.175.215.109:8000/v1

4. **mixtral**
   - Name: Mixtral 8x7B
   - Base Model: Mixtral-8x7B-Instruct-v0.1
   - Type: llama_cpp
   - Hardware: GPU
   - Status: active
   - Priority: 2
   - Server URL: http://34.175.215.109:8082/completion

### Inactive/Disabled Models:
- **capibara6**: Gemma3-12B (inactive)
- **gemma3-12b**: Gemma3-12B (inactive) 
- **oss-120b**: Open Source Supervised 120B (inactive)

## Prompt Templates Available (5):
1. **General**: Conversación general y preguntas abiertas
2. **Programación**: Ayuda con código, debugging y desarrollo
3. **Análisis**: Análisis de datos, investigación y pensamiento crítico
4. **Creativo**: Escritura creativa, storytelling y contenido
5. **Técnico**: Documentación técnica, arquitectura y sistemas

## System Configuration:
- Consensus enabled: Yes
- Fallback strategy: fast_response → balanced → complex
- Models preloaded: phi4:mini, qwen2.3-coder:1.5b
- API Endpoint: http://34.12.166.76:8000/v1 (vLLM compatible)

## Key Changes from Migration:
1. **phi3:mini** replaced with **phi4:mini** (upgraded from 3.8B to 14B parameters)
2. **mistral** replaced with **qwen2.3-coder:1.5b** (new coding expert model)
3. **Ollama API** replaced with **vLLM OpenAI-compatible API**
4. **gpt-oss:20b** remains unchanged as the complex reasoning model