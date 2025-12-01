/**
 * Vercel Serverless Function - MCP Health Check
 * Verifica estado del MCP Server en services VM
 *
 * Model Context Protocol: Sistema para reducir alucinaciones
 * proporcionando contexto verificado a los modelos
 *
 * Endpoints:
 * - Puerto 5003: MCP API principal (/api/mcp/health)
 * - Puerto 5010: Smart MCP endpoint alternativo
 *
 * Actualizado: 2025-12-01
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
    // Intentar puerto 5003 primero (MCP API principal)
    const MCP_PRIMARY_URL = process.env.MCP_HEALTH_URL || 'http://34.175.255.139:5003/api/mcp/health';
    const MCP_FALLBACK_URL = process.env.MCP_FALLBACK_URL || 'http://34.175.255.139:5010/health';

    console.log(`🔍 Health check MCP puerto 5003: ${MCP_PRIMARY_URL}`);

    try {
      const response = await fetch(MCP_PRIMARY_URL, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        signal: AbortSignal.timeout(3000)
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ MCP disponible en puerto 5003');

        return res.status(200).json({
          ...data,
          vm: 'services',
          port: 5003
        });
      }
    } catch (primaryError) {
      console.log('⚠️ Puerto 5003 no responde, intentando puerto 5010...');
    }

    // Fallback: Intentar puerto 5010 (Smart MCP alternativo)
    console.log(`🔍 Intentando MCP puerto 5010: ${MCP_FALLBACK_URL}`);
    const fallbackResponse = await fetch(MCP_FALLBACK_URL, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
      signal: AbortSignal.timeout(3000)
    });

    if (fallbackResponse.ok) {
      const data = await fallbackResponse.json();
      console.log('✅ MCP disponible en puerto 5010 (fallback)');

      return res.status(200).json({
        ...data,
        vm: 'services',
        port: 5010,
        note: 'Using fallback port'
      });
    }

    throw new Error('Ambos puertos MCP no responden');

  } catch (error) {
    console.error('❌ MCP no disponible:', error.message);

    // Devolver respuesta que indica que MCP no está disponible
    return res.status(503).json({
      service: 'mcp-server',
      status: 'unavailable',
      error: error.message,
      vm: 'services',
      ports_tried: [5003, 5010]
    });
  }
}

