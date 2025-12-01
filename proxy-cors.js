const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});

// Configuración actualizada - VMs en VPC default (10.204.0.0/24)
// Zona: europe-southwest1-b - Actualizado: 2025-11-27
const TARGETS = {
  // vLLM Multi-Model Server en models-europe (10.204.0.9:8080) - PRINCIPAL
  '/api/ai': 'http://10.204.0.9:8080',
  '/api/chat': 'http://10.204.0.9:8080',
  '/api/vllm': 'http://10.204.0.9:8080',
  '/v1/chat': 'http://10.204.0.9:8080',
  '/v1/completions': 'http://10.204.0.9:8080',

  // Ollama en models-europe (10.204.0.9:11434) - ALTERNATIVO
  '/api/ollama': 'http://10.204.0.9:11434',

  // Bridge API y RAG en rag-europe (10.204.0.10)
  '/api/rag': 'http://10.204.0.10:8000',
  '/api/bridge': 'http://10.204.0.10:8000',
  '/api/milvus': 'http://10.204.0.10:8000',
  '/api/nebula': 'http://10.204.0.10:8000',

  // Servicios en services (10.204.0.5)
  '/api/mcp': 'http://10.204.0.5:5003',
  '/api/n8n': 'http://10.204.0.5:5678',
  '/api/tts': 'http://10.204.0.5:5001',
  '/api/flask': 'http://10.204.0.5:5000',

  // Health check
  '/health': 'http://10.204.0.5:5000'
};

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  let target = null;
  for (const [path, url] of Object.entries(TARGETS)) {
    if (req.url.startsWith(path)) {
      target = url;
      break;
    }
  }

  if (target) {
    console.log(`🔀 Proxy: ${req.url} -> ${target}`);
    proxy.web(req, res, { target });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(8001, () => {
  console.log('🚀 CORS Proxy listening on port 8001');
  console.log('📡 Targets:', TARGETS);
});
