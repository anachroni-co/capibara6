// Chatbot capibara6
class Capibara6Chat {
    constructor() {
        this.toggle = document.getElementById('chatbot-toggle');
        this.window = document.getElementById('chatbot-window');
        this.close = document.getElementById('chatbot-close');
        this.input = document.getElementById('chatbot-input');
        this.send = document.getElementById('chatbot-send');
        this.messages = document.getElementById('chatbot-messages');
        this.isOpen = false;
        
        this.responses = this.getResponses();
        
        this.init();
    }
    
    init() {
        this.toggle.addEventListener('click', () => this.toggleChat());
        this.close.addEventListener('click', () => this.toggleChat());
        this.send.addEventListener('click', () => this.sendMessage());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        this.window.classList.toggle('open', this.isOpen);
        if (this.isOpen) {
            this.input.focus();
        }
    }
    
    sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.input.value = '';
        
        setTimeout(() => {
            const response = this.getResponse(message);
            this.addMessage(response, 'bot');
        }, 600);
    }
    
    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'bot' ? '<i data-lucide="bot" style="width: 20px; height: 20px;"></i>' : '<i data-lucide="user" style="width: 20px; height: 20px;"></i>';
        
        // Inicializar el icono de Lucide
        if (typeof lucide !== 'undefined') {
            setTimeout(() => lucide.createIcons(), 0);
        }
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `<p>${text}</p>`;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
    
    getResponse(message) {
        const lang = document.documentElement.getAttribute('data-lang') || 'es';
        const responses = this.responses[lang];
        const lowerMessage = message.toLowerCase();
        
        // Buscar respuesta relevante
        for (const [keywords, response] of Object.entries(responses)) {
            const keywordList = keywords.split('|');
            if (keywordList.some(keyword => lowerMessage.includes(keyword))) {
                return typeof response === 'function' ? response() : response;
            }
        }
        
        return responses.default();
    }
    
    getResponses() {
        return {
            es: {
                'hola|saludos|hey|hi': '¡Hola! 👋 Soy el asistente de <strong>capibara6</strong>. ¿Te gustaría saber más sobre nuestra arquitectura híbrida, rendimiento o características?',
                'precio|costo|coste|price': 'capibara6 es un proyecto de código abierto. Para uso enterprise, contáctanos en <a href="mailto:info@anachroni.co" style="color: var(--primary-light);">info@anachroni.co</a> para planes personalizados.',
                'tpu|hardware|procesador': 'capibara6 está optimizado para <strong>Google TPU v5e/v6e-64</strong> (4,500+ tokens/sec) y <strong>Google ARM Axion</strong> (2,100+ tokens/sec). ¡Rendimiento enterprise-grade! ⚡',
                'arquitectura|modelo|architecture': 'Usamos una arquitectura híbrida: <strong>70% Transformer</strong> (precisión) + <strong>30% Mamba SSM</strong> (velocidad O(n)). Lo mejor de ambos mundos! 🧠',
                'contexto|tokens|ventana': '¡Tenemos la <strong>mayor ventana de contexto</strong> del mercado con más de <strong>10M tokens</strong>! Superamos a GPT-4 (128K), Claude (200K) y Gemini (1M). 🏆',
                'compliance|gdpr|privacidad|seguridad': 'Cumplimos <strong>100%</strong> con GDPR, CCPA y AI Act de la UE. Certificado para empresas y <strong>administraciones públicas</strong>. 🔒',
                'multimodal|imagen|video|audio': 'Sí! Procesamos <strong>texto, imagen y video</strong> con encoders especializados. También tenemos Text-to-Speech con contexto emocional. 🌐',
                'mamba|transformer|moe': 'Nuestra arquitectura combina 32 expertos MoE con routing dinámico, más el balance Transformer/Mamba. Precisión del 97.8% con eficiencia O(n). 🎯',
                'instalar|install|setup|comenzar': 'Para comenzar: <code>git clone https://github.com/anachroni-co/capibara6</code> y sigue nuestra <a href="#quickstart">guía rápida</a>. Necesitas Python 3.9+ y acceso a TPU/ARM Axion. 🚀',
                'github|repo|repositorio|code': 'Nuestro repositorio está en <a href="https://github.com/anachroni-co/capibara6" target="_blank">github.com/anachroni-co/capibara6</a>. ¡Dale una ⭐ si te gusta!',
                'anachroni|empresa|company': '<strong>Anachroni s.coop</strong> es una cooperativa española especializada en IA avanzada. Visita <a href="https://www.anachroni.co" target="_blank">www.anachroni.co</a> o escríbenos a info@anachroni.co 🇪🇸',
                'demo|prueba|test': 'Estamos preparando demos interactivas. Mientras tanto, explora la <a href="#docs">documentación</a> o contacta con nosotros para un acceso anticipado. 🎪',
                'default': () => {
                    const defaults = [
                        'Interesante pregunta. Te recomiendo explorar nuestra <a href="#features">sección de características</a> o la <a href="#docs">documentación</a>. 📚',
                        'Para información más específica, visita <a href="https://github.com/anachroni-co/capibara6">nuestro GitHub</a> o escríbenos a info@anachroni.co 📧',
                        'Puedo ayudarte con: arquitectura, rendimiento, TPU, compliance, multimodal, instalación. ¿Qué te interesa? 🤔'
                    ];
                    return defaults[Math.floor(Math.random() * defaults.length)];
                }
            },
            en: {
                'hello|hi|hey|greetings': 'Hello! 👋 I\'m the <strong>capibara6</strong> assistant. Would you like to know more about our hybrid architecture, performance, or features?',
                'price|cost|pricing': 'capibara6 is an open-source project. For enterprise use, contact us at <a href="mailto:info@anachroni.co" style="color: var(--primary-light);">info@anachroni.co</a> for custom plans.',
                'tpu|hardware|processor': 'capibara6 is optimized for <strong>Google TPU v5e/v6e-64</strong> (4,500+ tokens/sec) and <strong>Google ARM Axion</strong> (2,100+ tokens/sec). Enterprise-grade performance! ⚡',
                'architecture|model': 'We use a hybrid architecture: <strong>70% Transformer</strong> (precision) + <strong>30% Mamba SSM</strong> (O(n) speed). Best of both worlds! 🧠',
                'context|tokens|window': 'We have the <strong>largest context window</strong> in the market with over <strong>10M tokens</strong>! We surpass GPT-4 (128K), Claude (200K), and Gemini (1M). 🏆',
                'compliance|gdpr|privacy|security': 'We comply <strong>100%</strong> with GDPR, CCPA, and EU AI Act. Certified for enterprises and <strong>public administrations</strong>. 🔒',
                'multimodal|image|video|audio': 'Yes! We process <strong>text, image, and video</strong> with specialized encoders. We also have Text-to-Speech with emotional context. 🌐',
                'mamba|transformer|moe': 'Our architecture combines 32 MoE experts with dynamic routing, plus the Transformer/Mamba balance. 97.8% accuracy with O(n) efficiency. 🎯',
                'install|setup|start|begin': 'To start: <code>git clone https://github.com/anachroni-co/capibara6</code> and follow our <a href="#quickstart">quick guide</a>. You need Python 3.9+ and TPU/ARM Axion access. 🚀',
                'github|repo|repository|code': 'Our repository is at <a href="https://github.com/anachroni-co/capibara6" target="_blank">github.com/anachroni-co/capibara6</a>. Give us a ⭐ if you like it!',
                'anachroni|company': '<strong>Anachroni s.coop</strong> is a Spanish cooperative specialized in advanced AI. Visit <a href="https://www.anachroni.co" target="_blank">www.anachroni.co</a> or write to info@anachroni.co 🇪🇸',
                'demo|trial|test': 'We\'re preparing interactive demos. Meanwhile, explore the <a href="#docs">documentation</a> or contact us for early access. 🎪',
                'default': () => {
                    const defaults = [
                        'Interesting question. I recommend exploring our <a href="#features">features section</a> or the <a href="#docs">documentation</a>. 📚',
                        'For more specific information, visit <a href="https://github.com/anachroni-co/capibara6">our GitHub</a> or write to info@anachroni.co 📧',
                        'I can help you with: architecture, performance, TPU, compliance, multimodal, installation. What interests you? 🤔'
                    ];
                    return defaults[Math.floor(Math.random() * defaults.length)];
                }
            }
        };
    }
}

// Inicializar chatbot
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Capibara6Chat();
    });
} else {
    new Capibara6Chat();
}

