#!/bin/bash
CSS="/home/elect/capibara6/web/chat-styles-neuromorphic-dark-v2.css"

# Backup
cp "$CSS" "$CSS.backup-$(date +%s)"

# ==========================================
# 1. AGREGAR ESTILOS BASE FALTANTES
# ==========================================

# Buscar la sección body y agregar color y background
sed -i '/^body {/,/^}/ {
    /font-family:/a\    color: var(--text-primary);\n    background-color: var(--bg-primary);
}' "$CSS"

# ==========================================
# 2. ACTUALIZAR COLORES ANTIGUOS QUE QUEDARON
# ==========================================

# Reemplazar todos los colores hexadecimales antiguos
sed -i 's/#16213e/#0f172a/g' "$CSS"
sed -i 's/#1a2332/#1e293b/g' "$CSS"
sed -i 's/#1e2940/#334155/g' "$CSS"
sed -i 's/#2563eb/#6366f1/g' "$CSS"
sed -i 's/#0ea5e9/#64748b/g' "$CSS"

# ==========================================
# 3. FIJAR MÁRGENES DEL CHAT COMPLETAMENTE
# ==========================================

# Eliminar márgenes y padding del wrapper principal
sed -i '/\.chat-page-wrapper/,/^}/ {
    /margin/d
    /padding/d
}' "$CSS"

# Asegurar que chat-main-content no tenga padding extra
sed -i '/\.chat-main-content {/,/transition:/ {
    s/padding:.*;/padding: 0;/
}' "$CSS"

# Asegurar márgenes consistentes en mensajes
sed -i '/\.chat-message {/,/^}/ {
    s/margin:.*/margin: 0;/
}' "$CSS"

# ==========================================
# 4. MEJORAR CONTRASTE DE TEXTO
# ==========================================

# Asegurar que todos los textos usen las variables correctas
cat >> "$CSS" << 'EOF'

/* ============================================
   CORRECCIONES FINALES - Color y Márgenes
   ============================================ */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Asegurar color correcto en todos los textos */
.chat-message,
.message-text,
.message-content,
p, span, div {
    color: inherit;
}

/* Textos en mensajes del usuario */
.message-user .message-text {
    color: var(--text-primary) !important;
}

/* Textos en mensajes del asistente */
.message-assistant .message-text {
    color: var(--text-primary) !important;
}

/* Input de texto */
.chat-input,
textarea {
    color: var(--text-primary) !important;
    background-color: var(--bg-secondary) !important;
}

/* Sidebar textos */
.sidebar,
.sidebar * {
    color: var(--text-primary);
}

/* Botones */
button {
    color: var(--text-primary);
}

/* Eliminar cualquier margen que cause "baile" */
.chat-messages-container {
    margin: 0 !important;
}

.chat-input-container {
    margin: 0 !important;
}

.chat-main-content {
    margin-left: var(--sidebar-width);
    padding: 0 !important;
}
EOF

echo "✅ Corregidos: Colores base + Texto visible + Márgenes fijos"
