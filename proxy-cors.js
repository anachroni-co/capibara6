const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});

const TARGETS = {
  '/api/ai': 'http://34.12.166.76:5001',
  '/api/chat': 'http://34.12.166.76:5001',
  '/api/mcp': 'http://34.175.136.104:5003',
  '/api/n8n': 'http://34.175.136.104:5678',
  '/api/tts': 'http://34.175.136.104:5002',
  '/api/rag': 'http://10.154.0.2:8000',
  '/health': 'http://34.12.166.76:5001'
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
