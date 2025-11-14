// ============================================
// CAPIBARA6 CONSENSUS - FIX COMPLETO
// Este archivo reemplaza todos los JS faltantes
// ============================================

console.log('🦫 Capibara6 Consensus Fix cargado');

// Verificar si chat-app.js ya tiene la funcionalidad
if (typeof sendMessage === 'undefined') {
    console.log('⚠️ chat-app.js no detectado, creando funcionalidad básica...');
    
    // Función de envío básica
    window.sendMessage = async function() {
        const input = document.getElementById('message-input');
        const container = document.getElementById('messages-container');
        const chatArea = document.getElementById('chat-area');
        const emptyState = document.getElementById('empty-state');
        
        if (!input || !input.value.trim()) return;
        
        const mensaje = input.value.trim();
        input.value = '';
        
        // Mostrar área de chat
        if (emptyState) emptyState.style.display = 'none';
        if (chatArea) chatArea.style.display = 'block';
        
        // Agregar mensaje del usuario
        if (container) {
            container.innerHTML += `
                <div class="message user-message">
                    <div class="message-content">${mensaje}</div>
                </div>
            `;
        }
        
        // Enviar al backend
        try {
            const response = await fetch('http://localhost:5001/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: mensaje,
                    max_tokens: 500,
                    temperature: 0.7
                })
            });
            
            const data = await response.json();
            
            // Mostrar respuesta
            if (container) {
                container.innerHTML += `
                    <div class="message assistant-message">
                        <div class="message-content">${data.response || data.text || 'Sin respuesta'}</div>
                    </div>
                `;
                container.scrollTop = container.scrollHeight;
            }
        } catch (error) {
            console.error('Error:', error);
            if (container) {
                container.innerHTML += `
                    <div class="message error-message">
                        <div class="message-content">Error: No se pudo conectar con el servidor</div>
                    </div>
                `;
            }
        }
    };
    
    // Conectar botón de envío
    document.addEventListener('DOMContentLoaded', function() {
        const sendBtn = document.getElementById('send-btn');
        const messageInput = document.getElementById('message-input');
        
        if (sendBtn) {
            sendBtn.addEventListener('click', sendMessage);
            console.log('✅ Botón enviar conectado');
        }
        
        if (messageInput) {
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            console.log('✅ Enter conectado');
        }
    });
}

// Panel de servicios (placeholder)
window.toggleServicesPanel = function() {
    console.log('Panel de servicios - próximamente');
};

console.log('✅ Capibara6 Fix completo cargado');
