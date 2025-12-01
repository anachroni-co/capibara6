/**
 * Vercel Serverless Function - AI Classify
 * Clasifica el tipo de petición del usuario usando IA
 *
 * Usado por el frontend para determinar el mejor modelo o servicio
 *
 * Actualizado: 2025-12-01
 */

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, message, query } = req.body;
    const userInput = text || message || query || '';

    if (!userInput) {
      return res.status(400).json({ error: 'Text, message or query is required' });
    }

    // Clasificación simple basada en keywords
    // En producción esto debería usar un modelo de clasificación
    const classification = classifyInput(userInput);

    console.log(`📊 Clasificación: ${classification.category} (confidence: ${classification.confidence})`);

    return res.status(200).json({
      category: classification.category,
      subcategory: classification.subcategory,
      confidence: classification.confidence,
      suggested_model: classification.suggested_model,
      needs_context: classification.needs_context,
      needs_rag: classification.needs_rag
    });

  } catch (error) {
    console.error('❌ Error en AI Classify:', error);

    // Fallback: clasificación genérica
    return res.status(200).json({
      category: 'general',
      subcategory: 'conversation',
      confidence: 0.5,
      suggested_model: 'phi4_fast',
      needs_context: false,
      needs_rag: false,
      fallback: true
    });
  }
}

/**
 * Clasificación simple basada en keywords
 */
function classifyInput(text) {
  const lowerText = text.toLowerCase();

  // Programación / Código
  if (/\b(código|code|programar|función|class|def|import|script|python|javascript|java)\b/i.test(text)) {
    return {
      category: 'coding',
      subcategory: 'programming',
      confidence: 0.9,
      suggested_model: 'qwen_coder',
      needs_context: false,
      needs_rag: false
    };
  }

  // Análisis técnico / complejo
  if (/\b(analizar|análisis|explicar|detallado|complejo|arquitectura|diseño)\b/i.test(text)) {
    return {
      category: 'technical',
      subcategory: 'analysis',
      confidence: 0.85,
      suggested_model: 'gemma3_multimodal',
      needs_context: true,
      needs_rag: false
    };
  }

  // Multilingüe / Traducción
  if (/\b(traducir|translate|inglés|english|francés|alemán)\b/i.test(text)) {
    return {
      category: 'multilingual',
      subcategory: 'translation',
      confidence: 0.9,
      suggested_model: 'aya_expanse_multilingual',
      needs_context: false,
      needs_rag: false
    };
  }

  // Preguntas sobre Capibara6 / Empresa
  if (/\b(capibara|anachroni|empresa|producto|quién eres|qué eres)\b/i.test(text)) {
    return {
      category: 'company',
      subcategory: 'information',
      confidence: 0.95,
      suggested_model: 'phi4_fast',
      needs_context: true,
      needs_rag: false
    };
  }

  // Conversación general (por defecto)
  return {
    category: 'general',
    subcategory: 'conversation',
    confidence: 0.7,
    suggested_model: 'phi4_fast',
    needs_context: false,
    needs_rag: false
  };
}
