// ============================================
// LOGIN AUTHENTICATION
// ============================================

// Configuración OAuth
// Desarrollo (localhost)
const AUTH_SERVER_URL = 'http://localhost:5001';

// Producción (comentado para activar más tarde)
// const AUTH_SERVER_URL = 'https://api.capibara6.com';
const OAUTH_CONFIG = {
    github: {
        authUrl: `${AUTH_SERVER_URL}/auth/github`
    },
    google: {
        authUrl: `${AUTH_SERVER_URL}/auth/google`
    }
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar iconos de Lucide
    lucide.createIcons();
    
    // Verificar si ya está autenticado
    checkAuthStatus();
    
    // Configurar event listeners
    setupEventListeners();
});

// ============================================
// Event Listeners
// ============================================
function setupEventListeners() {
    // Cerrar modales al hacer clic fuera
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
    
    // Cerrar modales con Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeAllModals();
        }
    });
}

// ============================================
// Authentication Functions
// ============================================
function checkAuthStatus() {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('user_data');
    
    if (token && user) {
        // Ya está autenticado, redirigir al chat
        window.location.href = 'chat.html';
    }
}

function loginWithGitHub() {
    window.location.href = OAUTH_CONFIG.github.authUrl;
}

function loginWithGoogle() {
    window.location.href = OAUTH_CONFIG.google.authUrl;
}

function generateState() {
    const state = Math.random().toString(36).substring(2, 15) + 
                  Math.random().toString(36).substring(2, 15);
    localStorage.setItem('oauth_state', state);
    return state;
}

// ============================================
// Modal Functions
// ============================================
function showTerms() {
    document.getElementById('terms-modal').style.display = 'block';
}

function showPrivacy() {
    document.getElementById('privacy-modal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
}

// ============================================
// Utility Functions
// ============================================
function showError(message) {
    // Crear notificación de error
    const notification = document.createElement('div');
    notification.className = 'error-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i data-lucide="alert-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    lucide.createIcons();
    
    // Mostrar notificación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Ocultar después de 5 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

function showSuccess(message) {
    // Crear notificación de éxito
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i data-lucide="check-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    lucide.createIcons();
    
    // Mostrar notificación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// ============================================
// Development Mode (para testing sin OAuth)
// ============================================
function loginAsGuest() {
    const guestUser = {
        id: 'guest_' + Date.now(),
        name: 'Usuario Invitado',
        email: 'guest@capibara6.local',
        avatar: 'https://via.placeholder.com/40/10a37f/ffffff?text=G',
        provider: 'guest'
    };
    
    localStorage.setItem('auth_token', 'guest_token_' + Date.now());
    localStorage.setItem('user_data', JSON.stringify(guestUser));
    
    showSuccess('Sesión iniciada como invitado');
    setTimeout(() => {
        window.location.href = 'chat.html';
    }, 1000);
}

// Agregar botón de invitado en modo desarrollo
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    document.addEventListener('DOMContentLoaded', function() {
        const authButtons = document.querySelector('.auth-buttons');
        const guestBtn = document.createElement('button');
        guestBtn.className = 'auth-btn guest-btn';
        guestBtn.innerHTML = `
            <i data-lucide="user"></i>
            <span>Continuar como Invitado (Dev)</span>
        `;
        guestBtn.onclick = loginAsGuest;
        
        authButtons.appendChild(guestBtn);
        lucide.createIcons();
    });
}
