/**
 * Vercel Serverless Function - Chat Completions (Legacy)
 * Esta función ahora está reemplazada por gateway-proxy.js
 * Este archivo se mantiene para compatibilidad pero no se usa directamente
 */

export default async function handler(req, res) {
    // Esta función ya no se usa directamente gracias a la reescritura en vercel.json
    // Pero se mantiene por si acaso

    res.status(503).json({
        error: 'Función reemplazada',
        message: 'Usar /api/gateway-proxy directamente o mediante reescritura en vercel.json',
        details: 'La funcionalidad se ha movido a /api/gateway-proxy.js'
    });
}

