# Capibara6 Consensus System - vLLM Migration

## Servers Updated

### vm-bounty2/servers/server_gptoss.py - Complete vLLM Migration

#### Changes Made:

1. **Configuration Updated:**
   - Changed from OLLAMA_URL to VLLM_URL
   - Changed from OLLAMA_MODEL to VLLM_MODEL  
   - Updated API endpoint from `/api/generate` to `/v1/chat/completions`
   - Added backward compatibility for migration from Ollama

2. **Main Function Updated:**
   - `call_ollama()` renamed to `call_vllm()`
   - Request format changed from Ollama style to OpenAI-compatible format
   - Changed from `prompt`-based to `messages`-based format
   - Updated response parsing to extract from `choices[0].message.content`

3. **Streaming Function Updated:**
   - Payload format changed to use OpenAI-compatible format with messages
   - Response parsing updated to handle Server-Sent Events format from vLLM
   - Changed from content-based parsing to delta-based parsing for streaming

4. **API Endpoints Updated:**
   - Health check: `/api/tags` → `/models` 
   - Models endpoint: `/api/tags` → `/models`
   - Updated response format for vLLM models list

5. **HTML Template Updated:**
   - Changed references from "Ollama" to "vLLM"
   - Updated displayed model and URL variables

## Models Available in Capibara6 Consensus

### Active Models:
1. **phi4:mini** - Fast response model (replaced phi3:mini)
2. **qwen2.5-coder-1.5b** - Coding expert model (replaces mistral)
3. **gpt-oss-20b** - Complex reasoning model (unchanged)
4. **mixtral** - Available in backend (via vm-bounty2)

### Physical Models in /home/elect/models/:
- `gpt-oss-20b/` - GPT-OSS 20B model
- `mistral-7b-instruct-v0.2/` - Mistral 7B v0.2 (available but not primary)
- `phi-4-mini/` - Phi-4 Mini model (14B parameters)
- `qwen2.5-coder-1.5b/` - Qwen2.5 Coder 1.5B model

## Consensus Server
- File: `/home/elect/capibara6/vm-bounty2/servers/consensus_server.py`
- Uses weighted voting method to combine responses from multiple models
- Can query multiple models in parallel for consensus
- Currently configured with models from vm-bounty2/config/models_config.py

## Configuration Files Updated:
1. `/home/elect/capibara6/model_config.json` - Main API model configuration
2. `/home/elect/capibara6/ollama_client.js` → Now `VLLMClient.js` (in name only)
3. `/home/elect/capibara6/backend/ollama_client.py` → Now `VLLMClient.py`
4. `/home/elect/capibara6/backend/ollama_rag_integration.py` → Updated to use VLLMClient
5. `/home/elect/capibara6/vm-bounty2/servers/server_gptoss.py` → Updated to work with vLLM
6. `/home/elect/capibara6/vm-bounty2/config/models_config.py` - Backend model configuration

## API Changes:
- From: Ollama API (`/api/generate`)
- To: OpenAI-compatible vLLM API (`/v1/chat/completions`)
- Request format: `{prompt: "...", ...}` → `{messages: [{role: "user", content: "..."}], ...}`
- Response format: `response` field → `choices[0].message.content`

## Startup Commands for Models:
- Phi-4 Mini: `vllm serve /home/elect/models/phi-4-mini --host 0.0.0.0 --port 8001`
- Qwen2.5-Coder-1.5B: `vllm serve /home/elect/models/qwen2.5-coder-1.5b --host 0.0.0.0 --port 8002`
- GPT-OSS-20B: `vllm serve /home/elect/models/gpt-oss-20b --host 0.0.0.0 --port 8000`
- Mistral v0.2: `vllm serve /home/elect/models/mistral-7b-instruct-v0.2 --host 0.0.0.0 --port 8003`