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
                    : 'http://34.12.166.76:5000';  // Servidor en bounty2
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
                    ? 'http://34.12.166.76:5000'  // Servidor en bounty2
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
}