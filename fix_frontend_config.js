// Script para corregir las URLs de conexión en el frontend de capibara6
// Este script actualiza las configuraciones para usar la URL correcta del backend

console.log('🔧 Corrigiendo configuración de frontend para conexión con backend...');

// 1. Actualizar config.js para usar el servidor backend correcto
const fs = require('fs');

// Ruta correcta del servidor backend
const CORRECT_BACKEND_URL = 'http://localhost:5000'; // Para desarrollo local, cambiar a IP real en producción
const CORRECT_SERVER_URL = 'http://localhost:5000/api/chat'; // URL correcta para el endpoint de chat

// Leer y actualizar config.js
const configPath = './web/config.js';
if (fs.existsSync(configPath)) {
    let configContent = fs.readFileSync(configPath, 'utf8');
    
    // Actualizar BACKEND_URL para desarrollo local
    configContent = configContent.replace(
        /BACKEND_URL: window\.location\.hostname === 'localhost'\s*\? '[^']*'/g,
        `BACKEND_URL: window.location.hostname === 'localhost' ? '${CORRECT_BACKEND_URL}'`
    );
    
    // Actualizar MODEL_CONFIG.serverUrl para apuntar al endpoint correcto
    configContent = configContent.replace(
        /serverUrl: 'https:\/\/www\.capibara6\.com\/api\/chat'/g,
        `serverUrl: '${CORRECT_SERVER_URL}'`
    );
    
    fs.writeFileSync(configPath, configContent);
    console.log('✅ Actualizado web/config.js con URLs correctas');
}

// 2. Actualizar chat-app.js si es necesario
const chatAppPath = './web/chat-app.js';
if (fs.existsSync(chatAppPath)) {
    let chatAppContent = fs.readFileSync(chatAppPath, 'utf8');
    
    // Actualizar MODEL_CONFIG.serverUrl en chat-app.js también
    chatAppContent = chatAppContent.replace(
        /serverUrl: 'https:\/\/www\.capibara6\.com\/api\/chat'/g,
        `serverUrl: '${CORRECT_SERVER_URL}'`
    );
    
    fs.writeFileSync(chatAppPath, chatAppContent);
    console.log('✅ Actualizado web/chat-app.js con URL correcta');
}

// 3. Actualizar script.js para usar la URL correcta
const scriptPath = './web/script.js';
if (fs.existsSync(scriptPath)) {
    let scriptContent = fs.readFileSync(scriptPath, 'utf8');
    
    // Actualizar URL local para desarrollo
    scriptContent = scriptContent.replace(
        /LOCAL: window\.location\.hostname === 'localhost'\s*\? '[^']*'/g,
        `LOCAL: window.location.hostname === 'localhost' ? '${CORRECT_BACKEND_URL}/api'`
    );
    
    fs.writeFileSync(scriptPath, scriptContent);
    console.log('✅ Actualizado web/script.js con URL correcta');
}

// 4. Actualizar chatbot.js para usar la URL correcta
const chatbotPath = './web/chatbot.js';
if (fs.existsSync(chatbotPath)) {
    let chatbotContent = fs.readFileSync(chatbotPath, 'utf8');
    
    // Actualizar la URL de fallback para health check
    chatbotContent = chatbotContent.replace(
        /const backendUrl = window\.location\.hostname === 'localhost'\s*\? '[^']*'/g,
        `const backendUrl = window.location.hostname === 'localhost' ? '${CORRECT_BACKEND_URL}'`
    );
    
    fs.writeFileSync(chatbotPath, chatbotContent);
    console.log('✅ Actualizado web/chatbot.js con URL correcta');
}

console.log('');
console.log('✅ Configuración de frontend actualizada correctamente');
console.log('');
console.log('📋 IMPORTANTE: Asegúrate de que el servidor backend esté corriendo en:');
console.log(`   ${CORRECT_BACKEND_URL}`);
console.log('');
console.log('📋 Para iniciar el servidor backend, puedes usar uno de estos comandos:');
console.log('   python backend/server.py');
console.log('   python backend/capibara6_integrated_server.py');
console.log('   python backend/cors_proxy.py');
console.log('');
console.log('📋 Si estás en producción, asegúrate de cambiar las URLs en los archivos a la IP pública');
console.log('   del servidor backend real.');