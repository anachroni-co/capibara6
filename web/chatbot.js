<<<<<<< HEAD
// chatbot.js - Funcionalidad para el chatbot de Capibara6 con integración CTM y e2b

let chatMessages = [];

// Variable para almacenar el estado del sistema
let systemStatus = {
    e2b_available: false,
    models: [],
    service: 'capibara6_integrated_server'
};

// Verificar el estado del sistema (CTM, e2b, modelos)
async function checkSystemStatus() {
    try {
        // Usar fetch directamente si makeApiRequest no está disponible
        let response;
        if (typeof makeApiRequest !== 'undefined') {
            response = await makeApiRequest('health', {}, 'local');
        } else {
            // Usar proxy local para evitar problemas CORS
            try {
                const localProxyUrl = 'http://localhost:8001/api/proxy';
                const backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
                    ? CHATBOT_CONFIG.BACKEND_URL 
                    : 'http://localhost:8001/api/proxy';  // Servidor en bounty2
                const proxyResponse = await fetch(localProxyUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        target_url: `${backendUrl}/api/health`,
                        method: 'GET'
                    })
                });
                response = await proxyResponse.json();
            } catch (proxyError) {
                // Si falla el proxy, usar conexión directa como fallback
                const backendUrl = window.location.hostname === 'localhost' 
                    ? 'http://localhost:8001/api/proxy'  // Servidor en bounty2
                    : 'https://www.capibara6.com';
                const healthResponse = await fetch(`${backendUrl}/api/health`);
                response = await healthResponse.json();
            }
        }
        if (response) {
            systemStatus = response;
            
            // Actualizar el estado de e2b
            const e2bStatusElement = document.getElementById('e2b-status-text');
            if (e2bStatusElement) {
                e2bStatusElement.textContent = response.e2b_available ? 'Disponible' : 'No disponible';
                e2bStatusElement.style.color = response.e2b_available ? '#2ecc71' : '#e74c3c';
            }
        }
    } catch (error) {
        console.error('Error al verificar el estado del sistema:', error);
        
        // Actualizar el estado de e2b como no disponible
        const e2bStatusElement = document.getElementById('e2b-status-text');
        if (e2bStatusElement) {
            e2bStatusElement.textContent = 'Error';
            e2bStatusElement.style.color = '#e74c3c';
        }
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const chatMessagesDiv = document.getElementById('chat-messages');
    
    if (sendButton && messageInput && chatMessagesDiv) {
        // Enviar mensaje al hacer clic en el botón
        sendButton.addEventListener('click', sendMessage);
        
        // Enviar mensaje al presionar Enter
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Cargar mensajes iniciales
    loadInitialMessages();
    
    // Verificar el estado del sistema
    await checkSystemStatus();
    
    // Actualizar periódicamente (cada 30 segundos)
    setInterval(checkSystemStatus, 30000);
});

function loadInitialMessages() {
    const chatMessagesDiv = document.getElementById('chat-messages');
    if (chatMessagesDiv) {
        chatMessagesDiv.innerHTML = '<div class="message bot">¡Hola! Soy Capibara6, tu asistente de IA con tecnología CTM y e2b. ¿En qué puedo ayudarte hoy?</div>';
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const chatMessagesDiv = document.getElementById('chat-messages');

    if (!messageInput || !chatMessagesDiv) return;

    const message = messageInput.value.trim();
    if (!message) return;

    // Añadir mensaje del usuario al chat
    addMessageToChat(message, 'user');
    messageInput.value = '';

    try {
        // Mostrar indicador de "escribiendo..."
        const thinkingElement = document.createElement('div');
        thinkingElement.className = 'message bot';
        thinkingElement.id = 'thinking-indicator';
        thinkingElement.textContent = 'Pensando...';
        chatMessagesDiv.appendChild(thinkingElement);
        chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

        // Hacer la solicitud al backend local que incluye CTM y e2b
        const response = await makeApiRequest('ai/generate', { 
            prompt: message,
            modelPreference: 'auto'  // Usar clasificación automática CTM
        }, 'local'); // Usar servidor local con CTM

        // Remover indicador de pensamiento
        const indicator = document.getElementById('thinking-indicator');
        if (indicator) indicator.remove();

        // Mostrar información sobre el modelo usado
        if (response && response.model_used) {
            const modelNameElement = document.getElementById('model-name');
            if (modelNameElement) {
                modelNameElement.textContent = response.model_used;
            }
        }

        // Mostrar información sobre el modelo usado
        if (response && response.model_used) {
            const modelNameElement = document.getElementById('model-name');
            if (modelNameElement) {
                modelNameElement.textContent = response.model_used;
            }
        }

        // Mostrar visualizaciones si están presentes en la respuesta
        if (response && response.output_files) {
            displayVisualizations(response.output_files);
        }

        // Añadir la respuesta del bot
        if (response && response.success && response.response) {
            addMessageToChat(response.response, 'bot');
        } else if (response && response.error) {
            addMessageToChat(`Error: ${response.error}`, 'bot');
        } else {
            addMessageToChat('Lo siento, no pude procesar tu solicitud en este momento.', 'bot');
        }
    } catch (error) {
        console.error('Error al enviar mensaje:', error);

        // Remover indicador de pensamiento
        const indicator = document.getElementById('thinking-indicator');
        if (indicator) indicator.remove();

        addMessageToChat('Lo siento, ocurrió un error al procesar tu solicitud.', 'bot');
    }
}

function addMessageToChat(message, sender) {
    const chatMessagesDiv = document.getElementById('chat-messages');
    if (!chatMessagesDiv) return;

    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    messageElement.textContent = message;

    chatMessagesDiv.appendChild(messageElement);
    chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
}

// Función para mostrar visualizaciones generadas en e2b
function displayVisualizations(outputFiles) {
    const vizContainer = document.getElementById('visualization-container');
    const vizContent = document.getElementById('visualization-content');
    const interactiveVizContainer = document.getElementById('interactive-visualizations');
    
    if (!vizContainer || !vizContent || !interactiveVizContainer) return;
    
    // Limpiar contenido anterior
    vizContent.innerHTML = '';
    interactiveVizContainer.innerHTML = '';
    
    let hasVisualizations = false;
    
    // Mostrar cada archivo de visualización
    for (const [filePath, content] of Object.entries(outputFiles)) {
        if (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.jpeg') || 
            filePath.endsWith('.gif') || filePath.endsWith('.svg')) {
            // Mostrar imágenes
            const img = document.createElement('img');
            img.src = content; // Ya viene en formato data:image/png;base64,...
            img.alt = `Visualización generada: ${filePath}`;
            img.className = 'visualization-image';
            vizContent.appendChild(img);
            hasVisualizations = true;
        } else if (filePath.endsWith('.csv') || filePath.endsWith('.json') || filePath.endsWith('.data')) {
            // Procesar y mostrar datos para visualización interactiva
            try {
                let data = null;
                
                if (filePath.endsWith('.json')) {
                    // Si es JSON, parsear directamente
                    data = JSON.parse(content);
                } else if (filePath.endsWith('.csv')) {
                    // Si es CSV, convertir a JSON (simplificado)
                    data = parseCSV(content);
                }
                
                if (data) {
                    // Crear visualización interactiva basada en los datos
                    createInteractiveVisualization(data, filePath);
                    hasVisualizations = true;
                }
            } catch (e) {
                console.error('Error procesando datos para visualización:', e);
                
                // Mostrar como texto si no se puede procesar
                const pre = document.createElement('pre');
                pre.textContent = `Datos generados en: ${filePath}\nError al procesar para visualización interactiva: ${e.message}`;
                vizContent.appendChild(pre);
                hasVisualizations = true;
            }
        } else if (typeof content === 'string' && (content.startsWith('{') || content.startsWith('['))) {
            // Si el contenido es un string que parece JSON, intentar parsearlo
            try {
                const data = JSON.parse(content);
                createInteractiveVisualization(data, 'data_output');
                hasVisualizations = true;
            } catch (e) {
                // Si no es JSON válido, mostrar como texto
                const pre = document.createElement('pre');
                pre.textContent = `Contenido generado: ${content.substring(0, 200)}...`;
                vizContent.appendChild(pre);
                hasVisualizations = true;
            }
        } else {
            // Otros tipos de archivos
            const div = document.createElement('div');
            div.innerHTML = `<p>Archivo generado: ${filePath}</p>`;
            vizContent.appendChild(div);
            hasVisualizations = true;
        }
    }
    
    // Mostrar u ocultar el contenedor según corresponda
    if (hasVisualizations) {
        vizContainer.style.display = 'block';
        // Hacer scroll al contenedor de visualización
        vizContainer.scrollIntoView({ behavior: 'smooth' });
    } else {
        vizContainer.style.display = 'none';
    }
}

// Función auxiliar para parsear CSV (simplificado)
function parseCSV(csvString) {
    const lines = csvString.trim().split('\n');
    if (lines.length < 2) return null;
    
    const headers = lines[0].split(',').map(header => header.trim());
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(value => value.trim());
        const row = {};
        for (let j = 0; j < headers.length; j++) {
            row[headers[j]] = values[j];
        }
        data.push(row);
    }
    
    return { headers, data };
}

// Función para crear visualizaciones interactivas basadas en datos
function createInteractiveVisualization(data, source) {
    const interactiveVizContainer = document.getElementById('interactive-visualizations');
    if (!interactiveVizContainer) return;
    
    // Crear un contenedor para esta visualización específica
    const vizDiv = document.createElement('div');
    vizDiv.className = 'interactive-viz-container';
    vizDiv.style.marginBottom = '20px';
    vizDiv.style.padding = '10px';
    vizDiv.style.border = '1px solid #ccc';
    vizDiv.style.borderRadius = '5px';
    
    // Determinar tipo de visualización según los datos
    if (data && Array.isArray(data) && data.length > 0) {
        // Si es un array de objetos, intentar crear un gráfico Chart.js
        createChartJSVisualization(vizDiv, data);
    } else if (data && data.data && Array.isArray(data.data)) {
        // Si tiene una estructura específica como {data: [...], headers: [...]}
        createChartJSVisualization(vizDiv, data.data, data.headers);
    } else if (data && data.x && data.y) {
        // Si tiene estructura x, y para Plotly
        createPlotlyVisualization(vizDiv, data);
    } else if (data && Array.isArray(data) && data.some(item => item.lat && item.lng)) {
        // Si hay datos geoespaciales, crear mapa
        createLeafletMap(vizDiv, data);
    } else {
        // Si no se puede determinar el tipo, mostrar mensaje
        vizDiv.innerHTML = '<p>Tipo de datos no reconocido para visualización interactiva</p>';
    }
    
    interactiveVizContainer.appendChild(vizDiv);
    interactiveVizContainer.style.display = 'block';
}

// Función para crear visualización con Chart.js
function createChartJSVisualization(container, data, headers = null) {
    // Crear canvas para el gráfico
    const canvas = document.createElement('canvas');
    canvas.id = `chart-${Date.now()}`;
    canvas.style.width = '100%';
    container.appendChild(canvas);
    
    // Preparar datos para Chart.js
    if (data.length > 0) {
        let labels = [];
        let datasets = [];
        
        if (headers) {
            // Si tenemos headers, usarlos como etiquetas
            labels = data.map((row, idx) => row[headers[0]] || `Item ${idx}`);
            
            // Crear datasets para cada columna numérica
            for (let i = 1; i < headers.length; i++) {
                const header = headers[i];
                // Verificar si es numérico
                if (!isNaN(parseFloat(data[0][header]))) {
                    datasets.push({
                        label: header,
                        data: data.map(row => parseFloat(row[header])),
                        borderColor: getRandomColor(),
                        backgroundColor: getRandomTransparentColor(),
                        borderWidth: 2
                    });
                }
            }
        } else {
            // Si no hay headers, asumir que cada objeto tiene propiedades x e y
            labels = data.map((item, idx) => item.label || `Item ${idx}`);
            
            // Agrupar por propiedades comunes
            const keys = Object.keys(data[0]).filter(key => key !== 'label');
            keys.forEach(key => {
                if (!isNaN(parseFloat(data[0][key]))) {
                    datasets.push({
                        label: key,
                        data: data.map(item => parseFloat(item[key])),
                        borderColor: getRandomColor(),
                        backgroundColor: getRandomTransparentColor(),
                        borderWidth: 2
                    });
                }
            });
        }
        
        // Crear el gráfico
        new Chart(canvas, {
            type: datasets.length > 1 ? 'line' : 'bar', // Usar línea si hay múltiples datasets, barra si es uno
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Función para crear visualización con Plotly
function createPlotlyVisualization(container, data) {
    const plotDiv = document.createElement('div');
    plotDiv.id = `plotly-${Date.now()}`;
    plotDiv.style.width = '100%';
    plotDiv.style.height = '400px';
    container.appendChild(plotDiv);
    
    const trace = {
        x: data.x,
        y: data.y,
        type: 'scatter',
        mode: 'lines+markers'
    };
    
    const layout = {
        title: 'Visualización Interactiva',
        width: '100%',
        height: 400
    };
    
    Plotly.newPlot(plotDiv, [trace], layout);
}

// Función para crear mapa con Leaflet
function createLeafletMap(container, locations) {
    const mapDiv = document.createElement('div');
    mapDiv.id = `map-${Date.now()}`;
    mapDiv.style.width = '100%';
    mapDiv.style.height = '400px';
    container.appendChild(mapDiv);
    
    // Crear el mapa
    const map = L.map(mapDiv).setView([0, 0], 2); // Vista inicial en el ecuador
    
    // Añadir capas base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Añadir marcadores para cada ubicación
    locations.forEach(location => {
        if (location.lat && location.lng) {
            const marker = L.marker([location.lat, location.lng]).addTo(map);
            if (location.name) {
                marker.bindPopup(location.name);
            }
        }
    });
}

// Función auxiliar para generar color aleatorio
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Función auxiliar para generar color transparente aleatorio
function getRandomTransparentColor() {
    const color = getRandomColor();
    return `${color}80`; // Agregar canal alfa (80 = 50% de opacidad)
=======
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

// Inicializar chatbot y exponer instancia global
let capibara6ChatInstance = null;

function initializeChatbot() {
    capibara6ChatInstance = new Capibara6Chat();
    // Exponer función global para abrir el chat desde otros lugares
    window.openChatbot = function() {
        if (capibara6ChatInstance) {
            // Si el chat está cerrado, abrirlo
            if (!capibara6ChatInstance.isOpen) {
                capibara6ChatInstance.toggleChat();
            }
            // Si ya está abierto, hacer scroll al chat
            else {
                const chatWindow = document.getElementById('chatbot-window');
                if (chatWindow) {
                    chatWindow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            }
        }
    };
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChatbot);
} else {
    initializeChatbot();
>>>>>>> feature/rag-infra
}