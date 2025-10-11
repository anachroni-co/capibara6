/**
 * Vercel Serverless Function
 * Proxy para Google Cloud Text-to-Speech API (Chirp 3)
 */

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        const { text } = req.body;

        if (!text) {
            return res.status(400).json({ error: 'Text is required' });
        }

        // API Key de Google Cloud (configurar en Vercel Environment Variables)
        const API_KEY = process.env.GOOGLE_CLOUD_API_KEY;

        if (!API_KEY) {
            return res.status(500).json({ 
                error: 'API key no configurada',
                fallback: true 
            });
        }

        // Llamar a Google Cloud Text-to-Speech API
        const response = await fetch(
            `https://texttospeech.googleapis.com/v1/text:synthesize?key=${API_KEY}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input: { text },
                    voice: {
                        languageCode: 'es-ES',
                        name: 'es-ES-Chirp-3-HD',  // Chirp 3 de alta calidad
                        ssmlGender: 'FEMALE'
                    },
                    audioConfig: {
                        audioEncoding: 'MP3',
                        speakingRate: 1.0,
                        pitch: 0,
                        volumeGainDb: 0,
                        effectsProfileId: ['headphone-class-device']
                    }
                })
            }
        );

        if (!response.ok) {
            const error = await response.text();
            console.error('Google TTS error:', error);
            return res.status(response.status).json({ 
                error: 'Error al generar audio',
                fallback: true 
            });
        }

        const data = await response.json();

        // Devolver audio en base64
        res.status(200).json({
            audioContent: data.audioContent,
            provider: 'Google Chirp 3 HD'
        });

    } catch (error) {
        console.error('TTS Proxy error:', error);
        res.status(500).json({ 
            error: error.message,
            fallback: true 
        });
    }
}

