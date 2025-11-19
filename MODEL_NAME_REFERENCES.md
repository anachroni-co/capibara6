# Model Name References for vLLM

## Current Configuration vs Physical Models

### JavaScript model_config.json currently uses:
1. "phi4:mini" → should map to /home/elect/models/phi-4-mini/
2. "qwen2.3-coder:1.5b" → should map to /home/elect/models/qwen2.5-coder-1.5b/
3. "gpt-oss:20b" → should map to /home/elect/models/gpt-oss-20b/

### Python models_config.py currently uses:
1. "Microsoft Phi-4 Mini (14B)" → maps to /home/elect/models/phi-4-mini/
2. "Qwen/Qwen2.5-Coder-1.5B-Instruct" → maps to /home/elect/models/qwen2.5-coder-1.5b/
3. "GPT-OSS-20B" → maps to /home/elect/models/gpt-oss-20b/

## Recommended vLLM Model References:
When starting vLLM servers, you can use:

### Option 1: Hugging Face Hub names (if models are on HF)
- microsoft/Phi-4-mini
- Qwen/Qwen2.5-Coder-1.5B-Instruct
- (gpt-oss-20b - may need local path)

### Option 2: Local paths (recommended for local models)
- /home/elect/models/phi-4-mini
- /home/elect/models/qwen2.5-coder-1.5b
- /home/elect/models/gpt-oss-20b

### Option 3: Directory names (for models in HF format locally)
- phi-4-mini
- qwen2.5-coder-1.5b
- gpt-oss-20b

## Note about naming mismatch:
The JavaScript config uses "qwen2.3-coder:1.5b" but our actual model is "qwen2.5-coder-1.5b".
This should be updated to match the actual model, but both versions are from the Qwen2.5 series.