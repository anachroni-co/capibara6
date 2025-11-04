// ============================================
// Digital Twin - Gemelo Digital
// Sistema de entrenamiento de ego sintético
// ============================================

// Estado del Gemelo Digital
const digitalTwinState = {
    uploadedSources: new Set(),
    encryptedData: {},
    trainingStatus: 'not_trained', // not_trained, training, trained
    trainingProgress: 0,
    encryptionKey: null
};

// ============================================
// Encriptación con Web Crypto API (AES-256-GCM)
// ============================================

/**
 * Genera una clave de encriptación única para el usuario
 */
async function generateEncryptionKey() {
    const key = await crypto.subtle.generateKey(
        {
            name: 'AES-GCM',
            length: 256
        },
        true,
        ['encrypt', 'decrypt']
    );

    // Exportar la clave para almacenarla
    const exportedKey = await crypto.subtle.exportKey('jwk', key);

    // Guardar en localStorage de forma segura (en producción, considerar más opciones)
    localStorage.setItem('dt_encryption_key', JSON.stringify(exportedKey));

    return key;
}

/**
 * Recupera la clave de encriptación del almacenamiento
 */
async function getEncryptionKey() {
    if (digitalTwinState.encryptionKey) {
        return digitalTwinState.encryptionKey;
    }

    const storedKey = localStorage.getItem('dt_encryption_key');

    if (storedKey) {
        const keyData = JSON.parse(storedKey);
        const key = await crypto.subtle.importKey(
            'jwk',
            keyData,
            {
                name: 'AES-GCM',
                length: 256
            },
            true,
            ['encrypt', 'decrypt']
        );
        digitalTwinState.encryptionKey = key;
        return key;
    }

    // Si no existe, generar una nueva
    const newKey = await generateEncryptionKey();
    digitalTwinState.encryptionKey = newKey;
    return newKey;
}

/**
 * Encripta datos usando AES-256-GCM
 */
async function encryptData(data) {
    try {
        const key = await getEncryptionKey();

        // Convertir datos a ArrayBuffer
        const encoder = new TextEncoder();
        const dataBuffer = encoder.encode(JSON.stringify(data));

        // Generar IV (Initialization Vector) aleatorio
        const iv = crypto.getRandomValues(new Uint8Array(12));

        // Encriptar
        const encryptedBuffer = await crypto.subtle.encrypt(
            {
                name: 'AES-GCM',
                iv: iv
            },
            key,
            dataBuffer
        );

        // Convertir a base64 para almacenamiento
        const encryptedArray = new Uint8Array(encryptedBuffer);
        const ivArray = Array.from(iv);
        const dataArray = Array.from(encryptedArray);

        return {
            iv: btoa(String.fromCharCode(...ivArray)),
            data: btoa(String.fromCharCode(...dataArray)),
            timestamp: Date.now()
        };
    } catch (error) {
        console.error('Error al encriptar datos:', error);
        throw error;
    }
}

/**
 * Desencripta datos usando AES-256-GCM
 */
async function decryptData(encryptedObj) {
    try {
        const key = await getEncryptionKey();

        // Convertir de base64 a ArrayBuffer
        const iv = new Uint8Array(atob(encryptedObj.iv).split('').map(c => c.charCodeAt(0)));
        const encryptedData = new Uint8Array(atob(encryptedObj.data).split('').map(c => c.charCodeAt(0)));

        // Desencriptar
        const decryptedBuffer = await crypto.subtle.decrypt(
            {
                name: 'AES-GCM',
                iv: iv
            },
            key,
            encryptedData
        );

        // Convertir de ArrayBuffer a string
        const decoder = new TextDecoder();
        const decryptedString = decoder.decode(decryptedBuffer);

        return JSON.parse(decryptedString);
    } catch (error) {
        console.error('Error al desencriptar datos:', error);
        throw error;
    }
}

// ============================================
// Manejo de carga de archivos
// ============================================

/**
 * Abre el diálogo de selección de archivos para una fuente específica
 */
window.uploadData = function(source) {
    console.log(`📤 Iniciando carga para: ${source}`);

    // Crear input file dinámico
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json,.txt,.zip,.csv';
    fileInput.multiple = true;

    fileInput.onchange = async (e) => {
        const files = Array.from(e.target.files);

        if (files.length === 0) return;

        console.log(`📁 Archivos seleccionados: ${files.length}`);

        // Mostrar indicador de carga
        showUploadProgress(source);

        try {
            // Procesar y encriptar cada archivo
            const processedFiles = [];

            for (const file of files) {
                const content = await readFileContent(file);
                const parsedData = parseDataBySource(source, content);

                // Encriptar los datos
                const encrypted = await encryptData(parsedData);

                processedFiles.push({
                    name: file.name,
                    size: file.size,
                    encrypted: encrypted,
                    source: source
                });
            }

            // Guardar en el estado
            if (!digitalTwinState.encryptedData[source]) {
                digitalTwinState.encryptedData[source] = [];
            }
            digitalTwinState.encryptedData[source].push(...processedFiles);

            // Guardar en localStorage (encriptado)
            await saveEncryptedDataToStorage();

            // Marcar como subido
            digitalTwinState.uploadedSources.add(source);

            // Actualizar UI
            updateSourceUI(source, processedFiles.length);
            checkTrainingReadiness();

            showNotification(`✅ ${files.length} archivo(s) de ${source} cargado(s) y encriptado(s) exitosamente`, 'success');

        } catch (error) {
            console.error('Error al procesar archivos:', error);
            showNotification(`❌ Error al cargar archivos de ${source}`, 'error');
        }
    };

    fileInput.click();
};

/**
 * Lee el contenido de un archivo
 */
function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);

        reader.readAsText(file);
    });
}

/**
 * Parsea los datos según la fuente
 */
function parseDataBySource(source, content) {
    try {
        // Intentar parsear como JSON
        const data = JSON.parse(content);

        // Extraer información relevante según la fuente
        const parsed = {
            source: source,
            timestamp: Date.now(),
            messages: []
        };

        // Lógica específica por plataforma
        switch (source) {
            case 'twitter':
                parsed.messages = parseTwitterData(data);
                break;
            case 'facebook':
                parsed.messages = parseFacebookData(data);
                break;
            case 'instagram':
                parsed.messages = parseInstagramData(data);
                break;
            case 'whatsapp':
                parsed.messages = parseWhatsAppData(data);
                break;
            case 'telegram':
                parsed.messages = parseTelegramData(data);
                break;
            case 'chatgpt':
                parsed.messages = parseChatGPTData(data);
                break;
            case 'claude':
                parsed.messages = parseClaudeData(data);
                break;
            default:
                parsed.messages = parseGenericData(data);
        }

        return parsed;
    } catch (error) {
        // Si no es JSON, tratar como texto plano
        return {
            source: source,
            timestamp: Date.now(),
            messages: [{
                text: content,
                type: 'text'
            }]
        };
    }
}

// Funciones de parseo específicas por plataforma
function parseTwitterData(data) {
    // Extraer tweets del usuario
    if (data.tweets) {
        return data.tweets.map(tweet => ({
            text: tweet.full_text || tweet.text,
            timestamp: new Date(tweet.created_at).getTime(),
            type: 'tweet'
        }));
    }
    return [];
}

function parseFacebookData(data) {
    // Extraer publicaciones y mensajes
    const messages = [];

    if (data.posts) {
        messages.push(...data.posts.map(post => ({
            text: post.data?.[0]?.post || post.post,
            timestamp: post.timestamp * 1000,
            type: 'post'
        })));
    }

    if (data.messages) {
        messages.push(...data.messages.map(msg => ({
            text: msg.content,
            timestamp: msg.timestamp_ms,
            type: 'message'
        })));
    }

    return messages;
}

function parseInstagramData(data) {
    const messages = [];

    if (data.media) {
        messages.push(...data.media.map(item => ({
            text: item.caption || '',
            timestamp: new Date(item.taken_at).getTime(),
            type: 'post'
        })));
    }

    return messages;
}

function parseWhatsAppData(data) {
    // WhatsApp suele exportar en formato texto
    if (typeof data === 'string') {
        const lines = data.split('\n');
        const regex = /\[?(\d{1,2}\/\d{1,2}\/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\]?\s*-?\s*([^:]+):\s*(.+)/;

        return lines.map(line => {
            const match = line.match(regex);
            if (match) {
                return {
                    text: match[4],
                    sender: match[3],
                    type: 'message'
                };
            }
            return null;
        }).filter(Boolean);
    }

    return data.messages || [];
}

function parseTelegramData(data) {
    if (data.messages) {
        return data.messages.map(msg => ({
            text: msg.text,
            timestamp: new Date(msg.date).getTime(),
            type: 'message'
        }));
    }
    return [];
}

function parseChatGPTData(data) {
    // ChatGPT exporta conversaciones
    const messages = [];

    if (Array.isArray(data)) {
        data.forEach(conversation => {
            if (conversation.mapping) {
                Object.values(conversation.mapping).forEach(node => {
                    if (node.message?.content?.parts) {
                        messages.push({
                            text: node.message.content.parts.join('\n'),
                            role: node.message.author.role,
                            timestamp: node.message.create_time * 1000,
                            type: 'chat'
                        });
                    }
                });
            }
        });
    }

    return messages;
}

function parseClaudeData(data) {
    // Claude exporta conversaciones
    if (data.conversations) {
        return data.conversations.flatMap(conv =>
            conv.messages?.map(msg => ({
                text: msg.content,
                role: msg.role,
                timestamp: new Date(msg.created_at).getTime(),
                type: 'chat'
            })) || []
        );
    }
    return [];
}

function parseGenericData(data) {
    // Intento genérico de extraer texto
    if (Array.isArray(data)) {
        return data.map(item => ({
            text: JSON.stringify(item),
            type: 'generic'
        }));
    }
    return [{
        text: JSON.stringify(data),
        type: 'generic'
    }];
}

// ============================================
// Almacenamiento y persistencia
// ============================================

async function saveEncryptedDataToStorage() {
    try {
        // Guardar el estado encriptado en localStorage
        const stateData = {
            uploadedSources: Array.from(digitalTwinState.uploadedSources),
            encryptedData: digitalTwinState.encryptedData,
            trainingStatus: digitalTwinState.trainingStatus,
            trainingProgress: digitalTwinState.trainingProgress
        };

        localStorage.setItem('dt_state', JSON.stringify(stateData));
        console.log('✅ Estado del Gemelo Digital guardado');
    } catch (error) {
        console.error('Error al guardar estado:', error);
    }
}

async function loadEncryptedDataFromStorage() {
    try {
        const savedState = localStorage.getItem('dt_state');

        if (savedState) {
            const stateData = JSON.parse(savedState);

            digitalTwinState.uploadedSources = new Set(stateData.uploadedSources || []);
            digitalTwinState.encryptedData = stateData.encryptedData || {};
            digitalTwinState.trainingStatus = stateData.trainingStatus || 'not_trained';
            digitalTwinState.trainingProgress = stateData.trainingProgress || 0;

            // Actualizar UI
            updateAllSourcesUI();
            updateTrainingStatus();
            checkTrainingReadiness();

            console.log('✅ Estado del Gemelo Digital cargado');
        }
    } catch (error) {
        console.error('Error al cargar estado:', error);
    }
}

// ============================================
// Actualización de UI
// ============================================

function updateSourceUI(source, fileCount) {
    const sourceItem = document.querySelector(`.source-item[data-source="${source}"]`);

    if (sourceItem) {
        sourceItem.classList.add('uploaded');

        const statusElement = sourceItem.querySelector('.source-status');
        if (statusElement) {
            statusElement.textContent = `${fileCount} archivo(s) subido(s)`;
            statusElement.setAttribute('data-i18n', '');
        }
    }
}

function updateAllSourcesUI() {
    digitalTwinState.uploadedSources.forEach(source => {
        const fileCount = digitalTwinState.encryptedData[source]?.length || 0;
        updateSourceUI(source, fileCount);
    });
}

function showUploadProgress(source) {
    // Aquí podrías añadir un indicador visual de progreso
    console.log(`⏳ Cargando datos de ${source}...`);
}

function checkTrainingReadiness() {
    const trainButton = document.getElementById('train-twin-btn');

    if (trainButton) {
        // Habilitar el botón si hay al menos una fuente cargada
        const hasData = digitalTwinState.uploadedSources.size > 0;
        trainButton.disabled = !hasData;
    }
}

function updateTrainingStatus() {
    const statusBadge = document.getElementById('twin-status');
    const trainingProgress = document.querySelector('.training-progress');
    const progressFill = document.getElementById('training-progress');
    const progressText = document.getElementById('progress-text');
    const exportButton = document.getElementById('export-twin-btn');

    if (!statusBadge) return;

    switch (digitalTwinState.trainingStatus) {
        case 'not_trained':
            statusBadge.className = 'status-badge';
            statusBadge.innerHTML = '<i data-lucide="circle" style="width: 8px; height: 8px;"></i><span>No entrenado</span>';
            if (trainingProgress) trainingProgress.style.display = 'none';
            if (exportButton) exportButton.disabled = true;
            break;

        case 'training':
            statusBadge.className = 'status-badge training';
            statusBadge.innerHTML = '<i data-lucide="loader" style="width: 8px; height: 8px;"></i><span>Entrenando...</span>';
            if (trainingProgress) trainingProgress.style.display = 'block';
            if (progressFill) progressFill.style.width = `${digitalTwinState.trainingProgress}%`;
            if (progressText) progressText.textContent = `${digitalTwinState.trainingProgress}%`;
            if (exportButton) exportButton.disabled = true;
            break;

        case 'trained':
            statusBadge.className = 'status-badge trained';
            statusBadge.innerHTML = '<i data-lucide="check-circle" style="width: 8px; height: 8px;"></i><span>Entrenado</span>';
            if (trainingProgress) trainingProgress.style.display = 'none';
            if (exportButton) exportButton.disabled = false;
            break;
    }

    // Reinicializar iconos de Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function showNotification(message, type = 'info') {
    // Crear notificación temporal
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10a37f' : type === 'error' ? '#ef4444' : '#3d3d3d'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ============================================
// Entrenamiento del Gemelo Digital
// ============================================

async function trainDigitalTwin() {
    console.log('🧠 Iniciando entrenamiento del Gemelo Digital...');

    // Cambiar estado a entrenando
    digitalTwinState.trainingStatus = 'training';
    digitalTwinState.trainingProgress = 0;
    updateTrainingStatus();

    const trainButton = document.getElementById('train-twin-btn');
    if (trainButton) {
        trainButton.disabled = true;
        trainButton.classList.add('training');
    }

    try {
        // Desencriptar y procesar todos los datos
        const allData = [];

        for (const [source, files] of Object.entries(digitalTwinState.encryptedData)) {
            for (const file of files) {
                const decrypted = await decryptData(file.encrypted);
                allData.push(decrypted);
            }

            // Actualizar progreso
            const progress = (Object.keys(digitalTwinState.encryptedData).indexOf(source) + 1) /
                           Object.keys(digitalTwinState.encryptedData).length * 50;
            digitalTwinState.trainingProgress = Math.round(progress);
            updateTrainingStatus();
        }

        // Simular procesamiento y entrenamiento
        // En producción, aquí se enviaría a un backend para entrenar el modelo
        await new Promise(resolve => {
            let progress = 50;
            const interval = setInterval(() => {
                progress += 10;
                digitalTwinState.trainingProgress = Math.min(progress, 100);
                updateTrainingStatus();

                if (progress >= 100) {
                    clearInterval(interval);
                    resolve();
                }
            }, 500);
        });

        // Marcar como entrenado
        digitalTwinState.trainingStatus = 'trained';
        await saveEncryptedDataToStorage();
        updateTrainingStatus();

        showNotification('✅ Gemelo Digital entrenado exitosamente', 'success');

    } catch (error) {
        console.error('Error al entrenar:', error);
        digitalTwinState.trainingStatus = 'not_trained';
        digitalTwinState.trainingProgress = 0;
        updateTrainingStatus();
        showNotification('❌ Error al entrenar el Gemelo Digital', 'error');
    } finally {
        if (trainButton) {
            trainButton.disabled = false;
            trainButton.classList.remove('training');
        }
    }
}

// ============================================
// Exportación de datos
// ============================================

async function exportDigitalTwin() {
    console.log('📦 Exportando Gemelo Digital...');

    try {
        // Preparar datos para exportar (encriptados)
        const exportData = {
            version: '1.0',
            timestamp: Date.now(),
            sources: Array.from(digitalTwinState.uploadedSources),
            trainingStatus: digitalTwinState.trainingStatus,
            encryptedData: digitalTwinState.encryptedData,
            metadata: {
                totalFiles: Object.values(digitalTwinState.encryptedData)
                    .reduce((sum, files) => sum + files.length, 0),
                totalSources: digitalTwinState.uploadedSources.size
            }
        };

        // Convertir a JSON y crear Blob
        const jsonString = JSON.stringify(exportData, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });

        // Crear enlace de descarga
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `gemelo-digital-${Date.now()}.json`;
        a.click();

        URL.revokeObjectURL(url);

        showNotification('✅ Gemelo Digital exportado exitosamente', 'success');

    } catch (error) {
        console.error('Error al exportar:', error);
        showNotification('❌ Error al exportar el Gemelo Digital', 'error');
    }
}

// ============================================
// Inicialización
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando módulo de Gemelo Digital...');

    // Cargar estado guardado
    loadEncryptedDataFromStorage();

    // Event listeners para botones
    const trainButton = document.getElementById('train-twin-btn');
    if (trainButton) {
        trainButton.addEventListener('click', trainDigitalTwin);
    }

    const exportButton = document.getElementById('export-twin-btn');
    if (exportButton) {
        exportButton.addEventListener('click', exportDigitalTwin);
    }

    // Inicializar clave de encriptación
    getEncryptionKey().then(() => {
        console.log('✅ Sistema de encriptación inicializado');
    });

    console.log('✅ Módulo de Gemelo Digital inicializado');
});
