/**
 * Vercel Serverless Function - TTS Proxy
 * Proxy HTTPS para Coqui TTS Server en services VM
 *
 * Endpoint: services VM (10.204.0.5:5002)
 * Tecnología: Coqui TTS / gTTS
 * Fallback: Web Speech API del navegador
 *
 * Actualizado: 2025-12-01
 */

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle OPTIONS (preflight)
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // Only accept POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, language = 'es', voice_id } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Limitar caracteres (TTS tiene límites de procesamiento)
    const truncatedText = text.length > 3000 ? text.substring(0, 3000) : text;

    // URL del servidor TTS en services VM
    // Puerto 5002 según especificaciones de red VPC
    const TTS_URL = process.env.TTS_URL || 'http://34.175.255.139:5002/speak';

    console.log(`📝 Proxy TTS: ${truncatedText.length} caracteres -> services VM:5002`);

    // Reenviar request a la VM services
    const response = await fetch(TTS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: truncatedText,
        language: language,
        voice_id: voice_id || 'sofia'
      }),
      signal: AbortSignal.timeout(30000) // 30 segundos timeout
    });

    if (!response.ok) {
      throw new Error(`TTS server responded with status ${response.status}`);
    }

    // Si es audio binario, reenviarlo directamente
    if (response.headers.get('content-type')?.includes('audio')) {
      const audioBuffer = await response.arrayBuffer();
      res.setHeader('Content-Type', 'audio/mpeg');
      return res.status(200).send(Buffer.from(audioBuffer));
    }

    // Si es JSON (respuesta con URL o datos)
    const data = await response.json();
    console.log('✅ TTS exitoso desde services VM');

    return res.status(200).json({
      ...data,
      provider: 'Coqui TTS',
      vm: 'services'
    });

  } catch (error) {
    console.error('❌ Error en proxy TTS:', error.message);

    // Devolver fallback para que el frontend use Web Speech API
    return res.status(200).json({
      error: error.message,
      fallback: true,
      provider: 'Web Speech API',
      message: 'TTS server no disponible, usando síntesis del navegador'
    });
  }
}

