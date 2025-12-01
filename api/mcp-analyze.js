/**
 * Vercel Serverless Function - MCP Analyze
 * Enriquece prompts con contexto verificado usando MCP Server
 *
 * Funcionalidad:
 * - Aumenta prompts con contexto de empresa, especificaciones técnicas
 * - Reduce alucinaciones con información verificada
 * - Proporciona fechas actuales y datos en tiempo real
 *
 * Endpoints MCP en services VM:
 * - /api/mcp/augment (puerto 5003) - Principal
 * - /analyze (puerto 5010) - Alternativo
 *
 * Actualizado: 2025-12-01
 */

export default async function handler(req, res) {
    // Solo permitir POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        const { prompt, query, contexts } = req.body;
        const userPrompt = prompt || query || '';

        if (!userPrompt) {
            return res.status(400).json({ error: 'Prompt or query is required' });
        }

        // URLs de MCP Server
        const MCP_PRIMARY_URL = process.env.MCP_AUGMENT_URL || 'http://34.175.255.139:5003/api/mcp/augment';
        const MCP_FALLBACK_URL = process.env.MCP_ANALYZE_URL || 'http://34.175.255.139:5010/analyze';

        console.log(`🔍 Enriqueciendo con MCP: ${userPrompt.substring(0, 50)}...`);

        // Intentar puerto 5003 primero (API principal)
        try {
            const response = await fetch(MCP_PRIMARY_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: userPrompt,
                    contexts: contexts || ['company_info', 'technical_specs', 'current_date']
                }),
                signal: AbortSignal.timeout(5000)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ MCP puerto 5003 exitoso');
                return res.status(200).json({
                    ...data,
                    vm: 'services',
                    port: 5003
                });
            }
        } catch (primaryError) {
            console.log('⚠️ Puerto 5003 no responde, intentando 5010...');
        }

        // Fallback: Puerto 5010
        const fallbackResponse = await fetch(MCP_FALLBACK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req.body),
            signal: AbortSignal.timeout(5000)
        });

        if (fallbackResponse.ok) {
            const data = await fallbackResponse.json();
            console.log('✅ MCP puerto 5010 exitoso (fallback)');
            return res.status(200).json({
                ...data,
                vm: 'services',
                port: 5010,
                note: 'Using fallback port'
            });
        }

        throw new Error('Ambos puertos MCP no responden');

    } catch (error) {
        console.error('❌ MCP Proxy error:', error);

        // Si falla, devolver query original (fallback)
        res.status(200).json({
            needs_context: false,
            original_query: req.body?.query || req.body?.prompt || '',
            augmented_prompt: req.body?.query || req.body?.prompt || '',
            contexts_added: 0,
            contexts_used: [],
            lightweight: true,
            fallback: true,
            error: 'MCP no disponible, usando prompt original'
        });
    }
}

