// Chatbot capibara6 - Sistema de captura de leads empresariales
class Capibara6Chat {
    constructor() {
        this.toggle = document.getElementById('chatbot-toggle');
        this.window = document.getElementById('chatbot-window');
        this.close = document.getElementById('chatbot-close');
        this.input = document.getElementById('chatbot-input');
        this.send = document.getElementById('chatbot-send');
        this.messages = document.getElementById('chatbot-messages');
        this.isOpen = false;
        
        // Estado de conversación y captura de leads
        this.conversationState = null;
        this.leadCaptureState = {
            isActive: false,
            currentStep: null,
            collectedData: {},
            awaitingResponse: false
        };
        
        // Estados de flujo de leads
        this.leadSteps = {
            CONTACT_TYPE: 'contact_type',
            COMPANY_INFO: 'company_info',
            CONTACT_DETAILS: 'contact_details',
            PROJECT_DETAILS: 'project_details',
            BUDGET_RANGE: 'budget_range',
            TIMELINE: 'timeline',
            CONFIRMATION: 'confirmation'
        };
        
        // Datos del usuario
        this.userConversations = this.loadUserData();
        
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
        
        // Guardar mensaje del usuario
        this.saveUserMessage(message);
        
        setTimeout(() => {
            const response = this.getResponse(message);
            this.addMessage(response.text, 'bot', response.quickReplies);
        }, 600);
    }
    
    addMessage(text, type, quickReplies = null) {
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
        
        // Agregar botones de respuesta rápida si existen
        if (quickReplies && quickReplies.length > 0 && type === 'bot') {
            this.addQuickReplies(quickReplies);
        }
        
        this.messages.scrollTop = this.messages.scrollHeight;
    }
    
    addQuickReplies(replies) {
        // Eliminar botones de respuesta rápida anteriores si existen
        const existingReplies = this.messages.querySelector('.quick-replies');
        if (existingReplies) {
            existingReplies.remove();
        }
        
        const quickRepliesDiv = document.createElement('div');
        quickRepliesDiv.className = 'quick-replies';
        
        replies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'quick-reply-btn';
            button.textContent = reply.text;
            button.onclick = () => {
                this.handleQuickReply(reply.value);
                quickRepliesDiv.remove();
            };
            quickRepliesDiv.appendChild(button);
        });
        
        this.messages.appendChild(quickRepliesDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
    
    handleQuickReply(value) {
        // Simular que el usuario escribió la respuesta
        this.addMessage(value, 'user');
        
        setTimeout(() => {
            const response = this.getResponse(value);
            this.addMessage(response.text, 'bot', response.quickReplies);
        }, 600);
    }
    
    getResponse(message) {
        const lang = document.documentElement.getAttribute('data-lang') || 'es';
        const responses = this.responses[lang];
        const lowerMessage = message.toLowerCase();
        
        // Manejar respuestas rápidas especiales
        if (message === 'start_lead_capture') {
            return this.startLeadCapture(lang);
        } else if (message === 'email_only') {
            return {
                text: lang === 'es' 
                    ? 'Perfecto. Por favor, comparte tu email y nos pondremos en contacto contigo pronto. 📧'
                    : 'Perfect. Please share your email and we\'ll contact you soon. 📧',
                quickReplies: null
            };
        } else if (message === 'no_thanks') {
            return {
                text: lang === 'es' 
                    ? 'Entendido. Si cambias de opinión, estaré aquí para ayudarte. ¡Que tengas un buen día! 😊'
                    : 'Understood. If you change your mind, I\'ll be here to help. Have a great day! 😊',
                quickReplies: null
            };
        }
        
        // Manejar flujo de captura de leads
        if (this.leadCaptureState.isActive) {
            return this.handleLeadCaptureFlow(message, lang);
        }
        
        // Detectar si pregunta si somos capibara6 de verdad
        if ((lowerMessage.includes('eres') || lowerMessage.includes('are you')) && 
            (lowerMessage.includes('capibara6') || lowerMessage.includes('verdad') || 
             lowerMessage.includes('real') || lowerMessage.includes('de verdad'))) {
            return {
                text: lang === 'es'
                    ? 'Soy solo un chatbot, un asistente virtual para ayudarte con información sobre capibara6. 🤖'
                    : 'I\'m just a chatbot, a virtual assistant to help you with information about capibara6. 🤖',
                quickReplies: null
            };
        }
        
        // Buscar respuesta relevante para preguntas específicas
        for (const [keywords, response] of Object.entries(responses)) {
            if (keywords === 'default') continue; // Saltar el default en esta iteración
            
            const keywordList = keywords.split('|');
            if (keywordList.some(keyword => lowerMessage.includes(keyword))) {
                return response;
            }
        }
        
        // Si no hay pregunta específica, ofrecer contacto
        return responses.default();
    }
    
    handleLeadCaptureFlow(message, lang) {
        const lowerMessage = message.toLowerCase();
        
        switch (this.leadCaptureState.currentStep) {
            case this.leadSteps.CONTACT_TYPE:
                return this.handleContactTypeSelection(message, lang);
            case this.leadSteps.COMPANY_INFO:
                return this.handleCompanyInfo(message, lang);
            case this.leadSteps.CONTACT_DETAILS:
                return this.handleContactDetails(message, lang);
            case this.leadSteps.PROJECT_DETAILS:
                return this.handleProjectDetails(message, lang);
            case this.leadSteps.BUDGET_RANGE:
                return this.handleBudgetRange(message, lang);
            case this.leadSteps.TIMELINE:
                return this.handleTimeline(message, lang);
            case this.leadSteps.CONFIRMATION:
                return this.handleConfirmation(message, lang);
            default:
                return this.startLeadCapture(lang);
        }
    }
    
    startLeadCapture(lang) {
        this.leadCaptureState.isActive = true;
        this.leadCaptureState.currentStep = this.leadSteps.CONTACT_TYPE;
        this.leadCaptureState.collectedData = {};
        
        return {
            text: lang === 'es' 
                ? '¡Perfecto! Me gustaría conocer más sobre tu proyecto. ¿Qué tipo de contacto te interesa?'
                : 'Perfect! I\'d like to know more about your project. What type of contact interests you?',
            quickReplies: lang === 'es' 
                ? [
                    { text: '🏢 Consultoría Empresarial', value: 'enterprise_consulting' },
                    { text: '🤝 Colaboración Técnica', value: 'technical_collaboration' },
                    { text: '💼 Implementación capibara6', value: 'implementation' },
                    { text: '📚 Información General', value: 'general_info' }
                ]
                : [
                    { text: '🏢 Enterprise Consulting', value: 'enterprise_consulting' },
                    { text: '🤝 Technical Collaboration', value: 'technical_collaboration' },
                    { text: '💼 capibara6 Implementation', value: 'implementation' },
                    { text: '📚 General Information', value: 'general_info' }
                ]
        };
    }
    
    handleContactTypeSelection(message, lang) {
        const lowerMessage = message.toLowerCase();
        let contactType = '';
        
        if (lowerMessage.includes('consultoría') || lowerMessage.includes('enterprise') || lowerMessage.includes('empresarial')) {
            contactType = 'enterprise_consulting';
        } else if (lowerMessage.includes('colaboración') || lowerMessage.includes('collaboration') || lowerMessage.includes('técnica')) {
            contactType = 'technical_collaboration';
        } else if (lowerMessage.includes('implementación') || lowerMessage.includes('implementation')) {
            contactType = 'implementation';
        } else if (lowerMessage.includes('información') || lowerMessage.includes('general') || lowerMessage.includes('info')) {
            contactType = 'general_info';
        } else {
            // Si no se reconoce, usar el mensaje como tipo
            contactType = message;
        }
        
        this.leadCaptureState.collectedData.contactType = contactType;
        this.leadCaptureState.currentStep = this.leadSteps.COMPANY_INFO;
        
        return {
            text: lang === 'es'
                ? 'Excelente elección. ¿Podrías contarme el nombre de tu empresa u organización?'
                : 'Great choice. Could you tell me the name of your company or organization?',
            quickReplies: null
        };
    }
    
    handleCompanyInfo(message, lang) {
        this.leadCaptureState.collectedData.companyName = message;
        this.leadCaptureState.currentStep = this.leadSteps.CONTACT_DETAILS;
        
        return {
            text: lang === 'es'
                ? 'Perfecto. Ahora necesito tus datos de contacto. ¿Cuál es tu nombre completo y email?'
                : 'Perfect. Now I need your contact details. What\'s your full name and email?',
            quickReplies: null
        };
    }
    
    handleContactDetails(message, lang) {
        // Extraer email del mensaje
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
        const emails = message.match(emailRegex);
        
        if (emails && emails.length > 0) {
            this.leadCaptureState.collectedData.email = emails[0];
            this.leadCaptureState.collectedData.fullName = message.replace(emailRegex, '').trim();
        } else {
            this.leadCaptureState.collectedData.fullName = message;
        }
        
        this.leadCaptureState.currentStep = this.leadSteps.PROJECT_DETAILS;
        
        return {
            text: lang === 'es'
                ? 'Excelente. ¿Podrías describir brevemente tu proyecto o necesidades específicas con capibara6?'
                : 'Excellent. Could you briefly describe your project or specific needs with capibara6?',
            quickReplies: null
        };
    }
    
    handleProjectDetails(message, lang) {
        this.leadCaptureState.collectedData.projectDescription = message;
        this.leadCaptureState.currentStep = this.leadSteps.BUDGET_RANGE;
        
        return {
            text: lang === 'es'
                ? 'Entendido. ¿Cuál es el rango de presupuesto aproximado para tu proyecto?'
                : 'Understood. What\'s the approximate budget range for your project?',
            quickReplies: lang === 'es'
                ? [
                    { text: '💰 < 10K €', value: 'under_10k' },
                    { text: '💰 10K - 50K €', value: '10k_50k' },
                    { text: '💰 50K - 100K €', value: '50k_100k' },
                    { text: '💰 > 100K €', value: 'over_100k' },
                    { text: '🤐 Prefiero no decir', value: 'not_specified' }
                ]
                : [
                    { text: '💰 < $10K', value: 'under_10k' },
                    { text: '💰 $10K - $50K', value: '10k_50k' },
                    { text: '💰 $50K - $100K', value: '50k_100k' },
                    { text: '💰 > $100K', value: 'over_100k' },
                    { text: '🤐 Prefer not to say', value: 'not_specified' }
                ]
        };
    }
    
    handleBudgetRange(message, lang) {
        const lowerMessage = message.toLowerCase();
        let budgetRange = '';
        
        if (lowerMessage.includes('10k') || lowerMessage.includes('10 k')) {
            budgetRange = lowerMessage.includes('50k') || lowerMessage.includes('50 k') ? '10k_50k' : 'under_10k';
        } else if (lowerMessage.includes('50k') || lowerMessage.includes('50 k')) {
            budgetRange = lowerMessage.includes('100k') || lowerMessage.includes('100 k') ? '50k_100k' : 'over_100k';
        } else if (lowerMessage.includes('100k') || lowerMessage.includes('100 k')) {
            budgetRange = 'over_100k';
        } else if (lowerMessage.includes('no decir') || lowerMessage.includes('not to say') || lowerMessage.includes('prefiero')) {
            budgetRange = 'not_specified';
        } else {
            budgetRange = message;
        }
        
        this.leadCaptureState.collectedData.budgetRange = budgetRange;
        this.leadCaptureState.currentStep = this.leadSteps.TIMELINE;
        
        return {
            text: lang === 'es'
                ? 'Perfecto. ¿Cuál es el timeline aproximado para tu proyecto?'
                : 'Perfect. What\'s the approximate timeline for your project?',
            quickReplies: lang === 'es'
                ? [
                    { text: '⚡ Inmediato (< 1 mes)', value: 'immediate' },
                    { text: '📅 Corto plazo (1-3 meses)', value: 'short_term' },
                    { text: '📅 Medio plazo (3-6 meses)', value: 'medium_term' },
                    { text: '📅 Largo plazo (> 6 meses)', value: 'long_term' }
                ]
                : [
                    { text: '⚡ Immediate (< 1 month)', value: 'immediate' },
                    { text: '📅 Short term (1-3 months)', value: 'short_term' },
                    { text: '📅 Medium term (3-6 months)', value: 'medium_term' },
                    { text: '📅 Long term (> 6 months)', value: 'long_term' }
                ]
        };
    }
    
    handleTimeline(message, lang) {
        const lowerMessage = message.toLowerCase();
        let timeline = '';
        
        if (lowerMessage.includes('inmediato') || lowerMessage.includes('immediate')) {
            timeline = 'immediate';
        } else if (lowerMessage.includes('corto') || lowerMessage.includes('short')) {
            timeline = 'short_term';
        } else if (lowerMessage.includes('medio') || lowerMessage.includes('medium')) {
            timeline = 'medium_term';
        } else if (lowerMessage.includes('largo') || lowerMessage.includes('long')) {
            timeline = 'long_term';
        } else {
            timeline = message;
        }
        
        this.leadCaptureState.collectedData.timeline = timeline;
        this.leadCaptureState.currentStep = this.leadSteps.CONFIRMATION;
        
        // Mostrar resumen y confirmar
        const summary = this.generateLeadSummary(lang);
        
        return {
            text: summary,
            quickReplies: lang === 'es'
                ? [
                    { text: '✅ Confirmar y Enviar', value: 'confirm_send' },
                    { text: '✏️ Editar Información', value: 'edit_info' }
                ]
                : [
                    { text: '✅ Confirm and Send', value: 'confirm_send' },
                    { text: '✏️ Edit Information', value: 'edit_info' }
                ]
        };
    }
    
    handleConfirmation(message, lang) {
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('confirmar') || lowerMessage.includes('confirm') || lowerMessage.includes('enviar') || lowerMessage.includes('send')) {
            // Enviar datos al backend
            this.sendLeadToBackend();
            
            // Resetear estado
            this.leadCaptureState.isActive = false;
            this.leadCaptureState.currentStep = null;
            this.leadCaptureState.collectedData = {};
            
            return {
                text: lang === 'es'
                    ? '¡Perfecto! ✅ Hemos recibido tu información. Nuestro equipo se pondrá en contacto contigo en las próximas 24 horas. ¡Gracias por tu interés en capibara6! 🚀'
                    : 'Perfect! ✅ We\'ve received your information. Our team will contact you within the next 24 hours. Thank you for your interest in capibara6! 🚀',
                quickReplies: null
            };
        } else if (lowerMessage.includes('editar') || lowerMessage.includes('edit')) {
            // Volver al paso anterior
            this.leadCaptureState.currentStep = this.leadSteps.CONTACT_TYPE;
            return this.startLeadCapture(lang);
        }
        
        return this.handleConfirmation(message, lang);
    }
    
    generateLeadSummary(lang) {
        const data = this.leadCaptureState.collectedData;
        const contactTypeMap = {
            'enterprise_consulting': lang === 'es' ? 'Consultoría Empresarial' : 'Enterprise Consulting',
            'technical_collaboration': lang === 'es' ? 'Colaboración Técnica' : 'Technical Collaboration',
            'implementation': lang === 'es' ? 'Implementación capibara6' : 'capibara6 Implementation',
            'general_info': lang === 'es' ? 'Información General' : 'General Information'
        };
        
        const budgetMap = {
            'under_10k': lang === 'es' ? '< 10K €' : '< $10K',
            '10k_50k': lang === 'es' ? '10K - 50K €' : '$10K - $50K',
            '50k_100k': lang === 'es' ? '50K - 100K €' : '$50K - $100K',
            'over_100k': lang === 'es' ? '> 100K €' : '> $100K',
            'not_specified': lang === 'es' ? 'No especificado' : 'Not specified'
        };
        
        const timelineMap = {
            'immediate': lang === 'es' ? 'Inmediato (< 1 mes)' : 'Immediate (< 1 month)',
            'short_term': lang === 'es' ? 'Corto plazo (1-3 meses)' : 'Short term (1-3 months)',
            'medium_term': lang === 'es' ? 'Medio plazo (3-6 meses)' : 'Medium term (3-6 months)',
            'long_term': lang === 'es' ? 'Largo plazo (> 6 meses)' : 'Long term (> 6 months)'
        };
        
        return lang === 'es'
            ? `📋 **Resumen de tu consulta:**\n\n` +
              `🏢 **Empresa:** ${data.companyName || 'No especificado'}\n` +
              `👤 **Contacto:** ${data.fullName || 'No especificado'}\n` +
              `📧 **Email:** ${data.email || 'No especificado'}\n` +
              `🎯 **Tipo:** ${contactTypeMap[data.contactType] || data.contactType}\n` +
              `💰 **Presupuesto:** ${budgetMap[data.budgetRange] || data.budgetRange}\n` +
              `⏰ **Timeline:** ${timelineMap[data.timeline] || data.timeline}\n` +
              `📝 **Proyecto:** ${data.projectDescription || 'No especificado'}\n\n` +
              `¿Confirmas que esta información es correcta?`
            : `📋 **Summary of your inquiry:**\n\n` +
              `🏢 **Company:** ${data.companyName || 'Not specified'}\n` +
              `👤 **Contact:** ${data.fullName || 'Not specified'}\n` +
              `📧 **Email:** ${data.email || 'Not specified'}\n` +
              `🎯 **Type:** ${contactTypeMap[data.contactType] || data.contactType}\n` +
              `💰 **Budget:** ${budgetMap[data.budgetRange] || data.budgetRange}\n` +
              `⏰ **Timeline:** ${timelineMap[data.timeline] || data.timeline}\n` +
              `📝 **Project:** ${data.projectDescription || 'Not specified'}\n\n` +
              `Do you confirm this information is correct?`;
    }
    
    async sendLeadToBackend() {
        try {
            const backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
                ? CHATBOT_CONFIG.BACKEND_URL + CHATBOT_CONFIG.ENDPOINTS.SAVE_LEAD
                : (window.location.hostname === 'localhost' 
                    ? 'http://localhost:5000/api/save-lead'
                    : '/api/save-lead');
            
            const leadData = {
                ...this.leadCaptureState.collectedData,
                timestamp: new Date().toISOString(),
                source: 'chatbot',
                userAgent: navigator.userAgent,
                language: document.documentElement.getAttribute('data-lang') || 'es'
            };
            
            console.log('Enviando lead al backend:', leadData);
            
            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(leadData)
            });
            
            const result = await response.json();
            console.log('Respuesta del backend:', result);
            
            if (result.success) {
                console.log('✅ Lead guardado correctamente');
            } else {
                console.warn('⚠️ Error al guardar lead:', result.error);
            }
        } catch (error) {
            console.warn('⚠️ Error de conexión con backend:', error);
        }
    }
    
    getResponses() {
        return {
            es: {
                'hola|saludos|hey|hi': { 
                    text: '¡Hola! 👋 Soy el asistente de <strong>capibara6</strong>. ¿Te gustaría saber más sobre nuestra arquitectura híbrida, rendimiento o características?',
                    quickReplies: null
                },
                'precio|costo|coste|price': {
                    text: 'capibara6 es un proyecto de código abierto. Para uso enterprise, contáctanos en <a href="mailto:info@anachroni.co" style="color: var(--primary-light);">info@anachroni.co</a> para planes personalizados.',
                    quickReplies: null
                },
                'tpu|hardware|procesador': {
                    text: 'capibara6 está optimizado para <strong>Google TPU v5e/v6e-64</strong> (4,500+ tokens/sec) y <strong>Google ARM Axion</strong> (2,100+ tokens/sec). ¡Rendimiento enterprise-grade! ⚡',
                    quickReplies: null
                },
                'arquitectura|modelo|architecture': {
                    text: 'Usamos una arquitectura híbrida: <strong>70% Transformer</strong> (precisión) + <strong>30% Mamba SSM</strong> (velocidad O(n)). Lo mejor de ambos mundos! 🧠',
                    quickReplies: null
                },
                'contexto|tokens|ventana': {
                    text: '¡Tenemos la <strong>mayor ventana de contexto</strong> del mercado con más de <strong>10M tokens</strong>! Superamos a GPT-4 (128K), Claude (200K) y Gemini (1M). 🏆',
                    quickReplies: null
                },
                'compliance|gdpr|privacidad|seguridad': {
                    text: 'Cumplimos <strong>100%</strong> con GDPR, CCPA y AI Act de la UE. Certificado para empresas y <strong>administraciones públicas</strong>. 🔒',
                    quickReplies: null
                },
                'multimodal|imagen|video|audio': {
                    text: 'Sí! Procesamos <strong>texto, imagen y video</strong> con encoders especializados. También tenemos Text-to-Speech con contexto emocional. 🌐',
                    quickReplies: null
                },
                'mamba|transformer|moe': {
                    text: 'Nuestra arquitectura combina 32 expertos MoE con routing dinámico, más el balance Transformer/Mamba. Precisión del 97.8% con eficiencia O(n). 🎯',
                    quickReplies: null
                },
                'instalar|install|setup|comenzar': {
                    text: 'Para comenzar: <code>git clone https://github.com/anachroni-co/capibara6</code> y sigue nuestra <a href="#quickstart">guía rápida</a>. Necesitas Python 3.9+ y acceso a TPU/ARM Axion. 🚀',
                    quickReplies: null
                },
                'github|repo|repositorio|code': {
                    text: 'Nuestro repositorio está en <a href="https://github.com/anachroni-co/capibara6" target="_blank">github.com/anachroni-co/capibara6</a>. ¡Dale una ⭐ si te gusta!',
                    quickReplies: null
                },
                'anachroni|empresa|company': {
                    text: '<strong>Anachroni s.coop</strong> es una cooperativa española especializada en IA avanzada. Visita <a href="https://www.anachroni.co" target="_blank">www.anachroni.co</a> o escríbenos a info@anachroni.co 🇪🇸',
                    quickReplies: null
                },
                'demo|prueba|test': {
                    text: 'Estamos preparando demos interactivas. Mientras tanto, explora la <a href="#docs">documentación</a> o contacta con nosotros para un acceso anticipado. 🎪',
                    quickReplies: null
                },
                'contacto|contact|contactar|contactar|empresa|empresarial|proyecto|project|consultoría|consulting|colaborar|collaborate|implementar|implement': {
                    text: '¡Perfecto! Me encantaría ayudarte con información sobre nuestros servicios empresariales. ¿Te gustaría que te guíe a través de un breve formulario para conocer mejor tus necesidades?',
                    quickReplies: [
                        { text: '✅ Sí, empezar formulario', value: 'start_lead_capture' },
                        { text: '📧 Solo email de contacto', value: 'email_only' },
                        { text: '❌ No, gracias', value: 'no_thanks' }
                    ]
                },
                'default': () => {
                    return {
                        text: '¡Hola! 👋 Soy el asistente de <strong>capibara6</strong>. ¿Te interesa conocer más sobre nuestros servicios empresariales o tienes alguna pregunta específica?',
                        quickReplies: [
                            { text: '🏢 Servicios Empresariales', value: 'start_lead_capture' },
                            { text: '❓ Pregunta Técnica', value: 'technical_question' },
                            { text: '📚 Información General', value: 'general_info' }
                        ]
                    };
                }
            },
            en: {
                'hello|hi|hey|greetings': {
                    text: 'Hello! 👋 I\'m the <strong>capibara6</strong> assistant. Would you like to know more about our hybrid architecture, performance, or features?',
                    quickReplies: null
                },
                'price|cost|pricing': {
                    text: 'capibara6 is an open-source project. For enterprise use, contact us at <a href="mailto:info@anachroni.co" style="color: var(--primary-light);">info@anachroni.co</a> for custom plans.',
                    quickReplies: null
                },
                'tpu|hardware|processor': {
                    text: 'capibara6 is optimized for <strong>Google TPU v5e/v6e-64</strong> (4,500+ tokens/sec) and <strong>Google ARM Axion</strong> (2,100+ tokens/sec). Enterprise-grade performance! ⚡',
                    quickReplies: null
                },
                'architecture|model': {
                    text: 'We use a hybrid architecture: <strong>70% Transformer</strong> (precision) + <strong>30% Mamba SSM</strong> (O(n) speed). Best of both worlds! 🧠',
                    quickReplies: null
                },
                'context|tokens|window': {
                    text: 'We have the <strong>largest context window</strong> in the market with over <strong>10M tokens</strong>! We surpass GPT-4 (128K), Claude (200K), and Gemini (1M). 🏆',
                    quickReplies: null
                },
                'compliance|gdpr|privacy|security': {
                    text: 'We comply <strong>100%</strong> with GDPR, CCPA, and EU AI Act. Certified for enterprises and <strong>public administrations</strong>. 🔒',
                    quickReplies: null
                },
                'multimodal|image|video|audio': {
                    text: 'Yes! We process <strong>text, image, and video</strong> with specialized encoders. We also have Text-to-Speech with emotional context. 🌐',
                    quickReplies: null
                },
                'mamba|transformer|moe': {
                    text: 'Our architecture combines 32 MoE experts with dynamic routing, plus the Transformer/Mamba balance. 97.8% accuracy with O(n) efficiency. 🎯',
                    quickReplies: null
                },
                'install|setup|start|begin': {
                    text: 'To start: <code>git clone https://github.com/anachroni-co/capibara6</code> and follow our <a href="#quickstart">quick guide</a>. You need Python 3.9+ and TPU/ARM Axion access. 🚀',
                    quickReplies: null
                },
                'github|repo|repository|code': {
                    text: 'Our repository is at <a href="https://github.com/anachroni-co/capibara6" target="_blank">github.com/anachroni-co/capibara6</a>. Give us a ⭐ if you like it!',
                    quickReplies: null
                },
                'anachroni|company': {
                    text: '<strong>Anachroni s.coop</strong> is a Spanish cooperative specialized in advanced AI. Visit <a href="https://www.anachroni.co" target="_blank">www.anachroni.co</a> or write to info@anachroni.co 🇪🇸',
                    quickReplies: null
                },
                'demo|trial|test': {
                    text: 'We\'re preparing interactive demos. Meanwhile, explore the <a href="#docs">documentation</a> or contact us for early access. 🎪',
                    quickReplies: null
                },
                'contact|contacting|company|enterprise|project|consulting|collaborate|implement|implementation': {
                    text: 'Perfect! I\'d love to help you with information about our enterprise services. Would you like me to guide you through a brief form to better understand your needs?',
                    quickReplies: [
                        { text: '✅ Yes, start form', value: 'start_lead_capture' },
                        { text: '📧 Just contact email', value: 'email_only' },
                        { text: '❌ No, thanks', value: 'no_thanks' }
                    ]
                },
                'default': () => {
                    return {
                        text: 'Hello! 👋 I\'m the <strong>capibara6</strong> assistant. Are you interested in learning more about our enterprise services or do you have a specific question?',
                        quickReplies: [
                            { text: '🏢 Enterprise Services', value: 'start_lead_capture' },
                            { text: '❓ Technical Question', value: 'technical_question' },
                            { text: '📚 General Information', value: 'general_info' }
                        ]
                    };
                }
            }
        };
    }
    
    // Métodos para gestión de datos del usuario
    loadUserData() {
        const data = localStorage.getItem('capibara6_user_data');
        return data ? JSON.parse(data) : {
            emails: [],
            conversations: [],
            timestamp: new Date().toISOString()
        };
    }
    
    saveUserMessage(message) {
        const timestamp = new Date().toISOString();
        
        // Guardar el mensaje
        this.userConversations.conversations.push({
            message: message,
            timestamp: timestamp
        });
        
        // Detectar email
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
        const emails = message.match(emailRegex);
        
        if (emails) {
            emails.forEach(email => {
                if (!this.userConversations.emails.includes(email)) {
                    this.userConversations.emails.push(email);
                }
            });
        }
        
        // Guardar en localStorage
        localStorage.setItem('capibara6_user_data', JSON.stringify(this.userConversations));
        
        // Enviar al backend si hay email (solo si no estamos en flujo de leads)
        if (emails && emails.length > 0 && !this.leadCaptureState.isActive) {
            this.sendToBackend(emails[0]);
        }
    }
    
    async sendToBackend(email) {
        const lang = document.documentElement.getAttribute('data-lang') || 'es';
        
        // Mostrar mensaje de confirmación inmediatamente
        setTimeout(() => {
            const confirmMsg = lang === 'es' 
                ? '✅ ¡Gracias! Hemos guardado tu email. Te contactaremos pronto. 📧'
                : '✅ Thank you! We\'ve saved your email. We\'ll contact you soon. 📧';
            this.addMessage(confirmMsg, 'bot', null);
        }, 800);
        
        // Intentar enviar al backend en segundo plano
        try {
            const backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
                ? CHATBOT_CONFIG.BACKEND_URL + CHATBOT_CONFIG.ENDPOINTS.SAVE_CONVERSATION
                : (window.location.hostname === 'localhost' 
                    ? 'http://localhost:5000/api/save-conversation'
                    : '/api/save-conversation');
            
            console.log('Enviando email al backend:', email);
            console.log('URL del backend:', backendUrl);
            
            const response = await fetch(backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    conversations: this.userConversations.conversations
                })
            });
            
            const result = await response.json();
            console.log('Respuesta del backend:', result);
            
            if (result.success) {
                console.log('✅ Email guardado y enviado correctamente');
            } else {
                console.warn('⚠️ El backend respondió pero hubo un error:', result.error);
            }
        } catch (error) {
            // Solo registrar el error en consola, no mostrar al usuario
            console.warn('⚠️ Backend no disponible:', error);
        }
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