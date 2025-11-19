# vLLM Startup Commands for Capibara6 Models

# 1. Start Phi-4 Mini server
vllm serve microsoft/Phi-4-mini --host 0.0.0.0 --port 8001 --api-key EMPTY

# 2. Start Qwen2.5-Coder-1.5B server 
vllm serve Qwen/Qwen2.5-Coder-1.5B-Instruct --host 0.0.0.0 --port 8002 --api-key EMPTY

# 3. Start GPT-OSS-20B server (assuming it's available as a standard model or needs local path)
vllm serve gpt-oss-20b --host 0.0.0.0 --port 8000 --api-key EMPTY

# 4. Mistral v0.2 server (if needed for other services)
vllm serve mistralai/Mistral-7B-Instruct-v0.2 --host 0.0.0.0 --port 8003 --api-key EMPTY

# Or if using a single multi-model server:
vllm serve --model-dir /home/elect/models/ --host 0.0.0.0 --port 8000

# The models are available in /home/elect/models/ directory as:
# - /home/elect/models/phi-4-mini/
# - /home/elect/models/qwen2.5-coder-1.5b/
# - /home/elect/models/gpt-oss-20b/
# - /home/elect/models/mistral-7b-instruct-v0.2/