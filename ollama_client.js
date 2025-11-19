const axios = require('axios');
const { TaskClassifier } = require('./task_classifier.js');

class VLLMClient {
  constructor(config) {
    this.endpoint = config.api_settings.vllm_endpoint || config.api_settings.ollama_endpoint;
    this.models = config.models;
    this.fallbackEnabled = config.fallback_strategy.enabled;
    this.fallbackOrder = config.fallback_strategy.order;
  }

  async generateWithFallback(prompt, options = {}) {
    const preferredModelTier = options.modelTier || 'auto';
    let modelToUse;

    if (preferredModelTier === 'auto') {
      modelToUse = TaskClassifier.classifyTask(prompt);
    } else {
      modelToUse = preferredModelTier;
    }

    // Intentar con el modelo clasificado
    const result = await this.generate(prompt, modelToUse, options);

    // Si falla y está habilitado el fallback, intentar con el siguiente modelo
    if (!result.success && this.fallbackEnabled) {
      const currentIndex = this.fallbackOrder.indexOf(modelToUse);
      for (let i = currentIndex + 1; i < this.fallbackOrder.length; i++) {
        console.log(`Fallback al modelo: ${this.fallbackOrder[i]}`);
        try {
          return await this.generate(prompt, this.fallbackOrder[i], options);
        } catch (error) {
          console.log(`Fallback fallido para: ${this.fallbackOrder[i]}`);
          continue;
        }
      }
    }

    return result;
  }

  async generate(prompt, modelTier, options = {}) {
    const modelConfig = this.models[modelTier];
    if (!modelConfig) {
      throw new Error(`Modelo no encontrado: ${modelTier}`);
    }

    // Convert to OpenAI-compatible format for vLLM
    const requestData = {
      model: modelConfig.name,
      messages: [{ role: 'user', content: prompt }],
      temperature: options.temperature || 0.7,
      max_tokens: Math.min(options.max_tokens || modelConfig.max_tokens, 2048),
      top_p: options.top_p || 0.9,
      top_k: options.top_k || 40,
      stream: false
    };

    try {
      const timeout = options.timeout || modelConfig.timeout;

      const response = await axios.post(
        `${this.endpoint}/chat/completions`,
        requestData,
        {
          timeout: timeout,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer EMPTY'  // vLLM typically doesn't require auth in basic setup
          }
        }
      );

      return {
        success: true,
        model: modelConfig.name,
        response: response.data.choices[0].message.content,
        total_duration: response.headers['openai-processing-ms'] || response.data.usage?.total_tokens,
        token_count: response.data.usage?.completion_tokens
      };
    } catch (error) {
      console.error(`Error con modelo ${modelConfig.name}:`, error.message);
      return {
        success: false,
        error: error.message,
        model: modelConfig.name
      };
    }
  }

  async streamWithModel(prompt, modelTier, onData, onEnd) {
    const modelConfig = this.models[modelTier];
    if (!modelConfig) {
      throw new Error(`Modelo no encontrado: ${modelTier}`);
    }

    const response = await fetch(`${this.endpoint}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer EMPTY'
      },
      body: JSON.stringify({
        model: modelConfig.name,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7,
        max_tokens: modelConfig.max_tokens,
        stream: true
      })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep the incomplete line in buffer

        for (const line of lines) {
          if (line.trim() && line.startsWith('data:')) {
            const dataStr = line.slice(5); // Remove 'data: ' prefix
            if (dataStr.trim() === '[DONE]') {
              onEnd();
              break;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.choices && data.choices[0].delta?.content) {
                onData(data.choices[0].delta.content);
              }
            } catch (e) {
              console.error('Error parsing stream data:', e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }
}

// Exportar la clase para que sea utilizada en otros módulos
module.exports = { VLLMClient };