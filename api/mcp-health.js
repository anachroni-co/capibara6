/**
 * Vercel Serverless Function - MCP Health Check
 * Verifica si Smart MCP está disponible en la VM
 */

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  try {
    // URL del Smart MCP en la VM
    const MCP_URL = process.env.SMART_MCP_URL || 'http://34.175.104.187:5010/health';

    console.log(`🔍 Health check MCP: ${MCP_URL}`);

    // Check health de la VM
    const response = await fetch(MCP_URL, {
      method: 'GET',
      signal: AbortSignal.timeout(2000)
    });

    if (!response.ok) {
      throw new Error(`MCP responded with status ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ MCP disponible');
    
    return res.status(200).json(data);

  } catch (error) {
    console.error('❌ MCP no disponible:', error.message);

    // Devolver respuesta que indica que MCP no está disponible
    return res.status(503).json({
      service: 'smart-mcp',
      status: 'unavailable',
      error: error.message
    });
  }
}

