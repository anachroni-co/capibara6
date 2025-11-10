// chat-page.js
// ==============================
// Control principal de la página de chat de Capibara6
// ==============================

class Capibara6ChatPage {
    constructor() {
      this.messages = [];
      this.apiUrl = '/api';
      console.log('💬 Capibara6ChatPage inicializada');
    }
  
    // ------------------------------
    // Normaliza el contenido de un mensaje
    // ------------------------------
    normalizeMessageContent(content) {
      if (typeof content !== 'string') return '';
      return content.trim().replace(/\s+/g, ' ');
    }
  
    // ------------------------------
    // Corta texto de forma segura
    // ------------------------------
    safeSubstring(text, length) {
      if (typeof text !== 'string') return '';
      return text.length > length ? text.substring(0, length) + '…' : text;
    }
  
    // ------------------------------
    // Envía un mensaje al servidor
    // ------------------------------
    async sendMessage(text) {
      try {
        const response = await fetch(`${this.apiUrl}/send-message`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
  
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }
  
        const result = await response.json();
        console.log('📨 Respuesta del servidor:', result);
        return result;
      } catch (err) {
        console.error('💥 Error enviando mensaje:', err);
        throw err;
      }
    }
  
    // ------------------------------
    // Guarda el historial del chat localmente y opcionalmente lo envía al backend
    // ------------------------------
    async saveChats() {
      try {
        if (!this.messages || this.messages.length === 0) {
          console.warn('⚠️ No hay mensajes para guardar.');
          return;
        }
  
        const firstText = this.normalizeMessageContent(this.messages[0]?.text || '');
        const lastText = this.normalizeMessageContent(this.messages.at(-1)?.text || '');
  
        const chatSummary = {
          id: Date.now(),
          date: new Date().toISOString(),
          firstText: this.safeSubstring(firstText, 80),
          lastText: this.safeSubstring(lastText, 80),
          messageCount: this.messages.length
        };
  
        // Guardar localmente
        const existingChats = JSON.parse(localStorage.getItem('savedChats') || '[]');
        existingChats.push(chatSummary);
        localStorage.setItem('savedChats', JSON.stringify(existingChats));
  
        console.log('✅ Conversación guardada localmente:', chatSummary);
  
        // Enviar al backend
        const response = await fetch(`${this.apiUrl}/save-conversation`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: this.messages,
            summary: chatSummary
          })
        });
  
        if (!response.ok) {
          throw new Error(`Error del servidor: ${response.status}`);
        }
  
        const result = await response.json().catch(() => ({}));
        console.log('📤 Respuesta del servidor (save):', result);
  
      } catch (err) {
        console.error('💥 Error guardando conversación:', err);
      }
    }
  
    // ------------------------------
    // Agrega un mensaje al chat (localmente)
    // ------------------------------
    addMessage(text, sender = 'user') {
      if (!text) return;
      const message = {
        text,
        sender,
        timestamp: new Date().toISOString()
      };
      this.messages.push(message);
      console.log(`🗨️ Nuevo mensaje (${sender}):`, text);
    }
  }
  
  // Inicialización global
  window.addEventListener('DOMContentLoaded', () => {
    window.capibaraChat = new Capibara6ChatPage();
    console.log('🦫 Capibara6ChatPage lista para usar.');
  });
  