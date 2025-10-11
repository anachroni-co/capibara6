/**
 * TTS Integration for Capibara6
 * Prioridad 1: Kyutai TTS (Delayed Streams Modeling)
 * Fallback: Web Speech API del navegador
 */

const TTS_CONFIG = {
    enabled: true,
    // Usar Kyutai en producción, Web Speech API en desarrollo
    useKyutai: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',
    apiEndpoint: '/api/tts',
    language: 'es',
    rate: 1.0,      // Velocidad (0.5 - 2.0)
    pitch: 1.0,     // Tono (0 - 2)
    volume: 1.0,    // Volumen (0 - 1)
    preferredVoices: [
        'Google español',
        'Microsoft Helena',
        'Microsoft Laura',
        'es-ES-Neural2-A',
        'es-ES',
        'es-MX',
        'Spanish'
    ]
};

// Estado global
let currentUtterance = null;
let isSpeaking = false;
let currentSpeakingButton = null;

/**
 * Obtiene la mejor voz en español disponible
 */
function getBestSpanishVoice() {
    const voices = window.speechSynthesis.getVoices();
    
    // Intentar encontrar voces en orden de preferencia
    for (const preferred of TTS_CONFIG.preferredVoices) {
        const voice = voices.find(v => 
            v.name.includes(preferred) || v.lang.startsWith('es')
        );
        if (voice) return voice;
    }
    
    // Fallback: cualquier voz en español
    return voices.find(v => v.lang.startsWith('es')) || voices[0];
}

/**
 * Lee el texto usando Chirp 3 (si está disponible) o Web Speech API
 */
async function speakText(text, button) {
    // Si ya está hablando, detener
    if (isSpeaking) {
        stopSpeaking();
        return;
    }
    
    // Limpiar texto antes de leer
    const cleanText = text
        .replace(/```[\s\S]*?```/g, '')           // Eliminar bloques de código
        .replace(/`[^`]+`/g, '')                  // Eliminar código inline
        .replace(/In \[\d*\]:/g, '')              // Eliminar prompts de notebook
        .replace(/Out\[\d*\]:/g, '')              // Eliminar outputs de notebook
        .replace(/\*\*/g, '')                     // Eliminar negritas markdown
        .replace(/__/g, '')                       // Eliminar cursivas
        .replace(/[#\-\*\[\]]/g, '')              // Eliminar markdown y corchetes
        .replace(/https?:\/\/[^\s]+/g, '')       // Eliminar URLs
        .replace(/\n{3,}/g, '\n\n')               // Normalizar saltos
        .replace(/[^\w\s.,;:!?¿¡áéíóúñÁÉÍÓÚÑüÜ()\-]/g, ' ') // Solo caracteres válidos
        .replace(/\s+/g, ' ')                     // Normalizar espacios
        .trim()
        .substring(0, 500);                       // ✅ Limitar a 500 caracteres (más corto = más estable)
    
    if (!cleanText) {
        console.warn('⚠️ No hay texto para leer');
        return;
    }
    
    console.log(`🎙️ Texto limpio para TTS (${cleanText.length} chars): "${cleanText.substring(0, 100)}..."`);
    
    // Intentar usar Kyutai primero
    if (TTS_CONFIG.useKyutai) {
        try {
            await speakWithKyutai(cleanText, button);
            return;
        } catch (error) {
            console.warn('⚠️ Kyutai no disponible, usando Web Speech API:', error);
            // Continuar con fallback
        }
    }
    
    // Fallback: Web Speech API
    speakWithWebAPI(cleanText, button);
}

/**
 * Síntesis con Kyutai TTS (Delayed Streams Modeling)
 */
async function speakWithKyutai(text, button) {
    isSpeaking = true;
    currentSpeakingButton = button;
    updateButtonState(button, 'speaking');
    
    try {
        const response = await fetch(TTS_CONFIG.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                text,
                language: TTS_CONFIG.language 
            })
        });
        
        if (!response.ok) {
            throw new Error('Kyutai API error');
        }
        
        const data = await response.json();
        
        if (data.fallback) {
            throw new Error('API fallback activado');
        }
        
        // Kyutai devuelve WAV en base64
        const audioFormat = data.format || 'wav';
        const audioData = `data:audio/${audioFormat};base64,${data.audioContent}`;
        const audio = new Audio(audioData);
        
        audio.onplay = () => {
            console.log(`🔊 Kyutai DSM TTS reproduciendo... (${data.model || 'modelo desconocido'})`);
        };
        
        audio.onended = () => {
            isSpeaking = false;
            updateButtonState(button, 'idle');
            currentSpeakingButton = null;
            console.log('✅ Kyutai TTS completado');
        };
        
        audio.onerror = (error) => {
            console.error('❌ Error reproduciendo audio:', error);
            isSpeaking = false;
            updateButtonState(button, 'idle');
            currentSpeakingButton = null;
        };
        
        await audio.play();
        
    } catch (error) {
        isSpeaking = false;
        updateButtonState(button, 'idle');
        currentSpeakingButton = null;
        throw error; // Propagar para fallback
    }
}

/**
 * Síntesis con Web Speech API (fallback)
 */
function speakWithWebAPI(text, button, retryCount = 0) {
    // Si el texto es muy largo y es un retry, acortar más
    if (retryCount > 0 && text.length > 200) {
        text = text.substring(0, 200);
        console.log(`🔄 Retry ${retryCount}: texto acortado a 200 chars`);
    }
    
    // Crear utterance
    currentUtterance = new SpeechSynthesisUtterance(text);
    
    // Configurar voz
    const voice = getBestSpanishVoice();
    if (voice) {
        currentUtterance.voice = voice;
        currentUtterance.lang = voice.lang;
    } else {
        currentUtterance.lang = TTS_CONFIG.language;
    }
    
    // Configurar parámetros
    currentUtterance.rate = TTS_CONFIG.rate;
    currentUtterance.pitch = TTS_CONFIG.pitch;
    currentUtterance.volume = TTS_CONFIG.volume;
    
    // Event handlers
    currentUtterance.onstart = () => {
        isSpeaking = true;
        currentSpeakingButton = button;
        updateButtonState(button, 'speaking');
        console.log('🔊 Web Speech API iniciado');
    };
    
    currentUtterance.onend = () => {
        isSpeaking = false;
        updateButtonState(button, 'idle');
        currentSpeakingButton = null;
        currentUtterance = null;
        console.log('✅ Web Speech API completado');
    };
    
    currentUtterance.onerror = (event) => {
        console.error('❌ Error TTS:', event.error);
        
        // Intentar detener cualquier speech en curso
        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
        }
        
        isSpeaking = false;
        updateButtonState(button, 'idle');
        currentSpeakingButton = null;
        currentUtterance = null;
        
        // Manejo específico de errores
        if (event.error === 'synthesis-failed' && retryCount < 2) {
            console.warn('⚠️ Síntesis fallida. Reintentando con texto más corto...');
            
            // Reintentar con texto más corto (solo 2 veces máximo)
            setTimeout(() => {
                speakWithWebAPI(text, button, retryCount + 1);
            }, 500);
        } else if (event.error === 'synthesis-failed') {
            console.warn('⚠️ No se pudo sintetizar el texto después de varios intentos.');
            console.log('💡 Consejo: El texto puede tener caracteres especiales o ser muy complejo.');
        } else if (event.error === 'network') {
            console.warn('⚠️ Error de red. Verifica tu conexión.');
        } else {
            console.warn(`⚠️ Error TTS: ${event.error}`);
        }
    };
    
    // Iniciar lectura
    window.speechSynthesis.speak(currentUtterance);
}

/**
 * Detiene la lectura
 */
function stopSpeaking() {
    if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
    }
    
    if (currentSpeakingButton) {
        updateButtonState(currentSpeakingButton, 'idle');
    }
    
    isSpeaking = false;
    currentSpeakingButton = null;
    currentUtterance = null;
    console.log('⏹️ TTS detenido');
}

/**
 * Actualiza el estado visual del botón
 */
function updateButtonState(button, state) {
    // Validar que el botón existe
    if (!button) {
        console.warn('⚠️ updateButtonState: botón no encontrado');
        return;
    }

    const icon = button.querySelector('i');
    const text = button.querySelector('.btn-text');
    
    if (state === 'speaking') {
        if (icon) icon.setAttribute('data-lucide', 'volume-2');
        if (text) text.textContent = 'Detener';
        button.classList.add('speaking');
    } else {
        if (icon) icon.setAttribute('data-lucide', 'volume');
        if (text) text.textContent = 'Escuchar';
        button.classList.remove('speaking');
    }
    
    // Reinicializar iconos de Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

/**
 * Inicializar TTS
 */
function initTTS() {
    // Cargar voces (pueden tardar en cargar)
    if (window.speechSynthesis) {
        window.speechSynthesis.getVoices();
        
        // Evento cuando las voces estén listas
        window.speechSynthesis.onvoiceschanged = () => {
            const voices = window.speechSynthesis.getVoices();
            const spanishVoices = voices.filter(v => v.lang.startsWith('es'));
            console.log('🔊 Voces en español disponibles:', spanishVoices.length);
            console.log('🎯 Voz seleccionada:', getBestSpanishVoice()?.name);
        };
    } else {
        console.warn('⚠️ Web Speech API no disponible en este navegador');
    }
}

// Exportar funciones globalmente
window.speakText = speakText;
window.stopSpeaking = stopSpeaking;
window.initTTS = initTTS;

// Auto-inicializar
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTTS);
} else {
    initTTS();
}

console.log('🔊 TTS Integration cargado');
console.log('✅ Funciones disponibles: speakText, stopSpeaking');

