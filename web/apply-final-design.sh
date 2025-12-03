#!/bin/bash
CSS="/home/elect/capibara6/web/chat-styles-neuromorphic-dark-v2.css"

# Backup antes de cambios finales
cp "$CSS" "$CSS.pre-final"

# ==========================================
# 1. CAMBIAR A FUENTE MANROPE
# ==========================================
sed -i "s/font-family: 'Roboto'/font-family: 'Manrope'/g" "$CSS"
sed -i "s/'Roboto'/'Manrope'/g" "$CSS"
sed -i "s/'Roboto Mono'/'JetBrains Mono'/g" "$CSS"

# ==========================================
# 2. PALETA GRIS NEUTRO MINIMALISTA
# ==========================================

# Colores principales -> Grises con acento sutil
sed -i 's/--primary: #2563eb;/--primary: #6366f1;/' "$CSS"
sed -i 's/--primary-dark: #1e40af;/--primary-dark: #4f46e5;/' "$CSS"
sed -i 's/--primary-light: #60a5fa;/--primary-light: #818cf8;/' "$CSS"
sed -i 's/--secondary: #0ea5e9;/--secondary: #64748b;/' "$CSS"
sed -i 's/--accent: #06b6d4;/--accent: #8b5cf6;/' "$CSS"

# Backgrounds -> Tonos grises oscuros minimalistas
sed -i 's/--bg-primary: #16213e;/--bg-primary: #0f172a;/' "$CSS"
sed -i 's/--bg-secondary: #1a2332;/--bg-secondary: #1e293b;/' "$CSS"
sed -i 's/--bg-tertiary: #1e2940;/--bg-tertiary: #334155;/' "$CSS"
sed -i 's/--bg-card: #1a2332;/--bg-card: #1e293b;/' "$CSS"
sed -i 's/--bg-elevated: #1f2937;/--bg-elevated: #334155;/' "$CSS"

# Textos -> Grises claros para contraste
sed -i 's/--text-primary: #f8fafc;/--text-primary: #f1f5f9;/' "$CSS"
sed -i 's/--text-secondary: #e2e8f0;/--text-secondary: #cbd5e1;/' "$CSS"
sed -i 's/--text-muted: #94a3b8;/--text-muted: #94a3b8;/' "$CSS"

# Gradientes -> Grises sutiles
sed -i 's/linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%)/linear-gradient(135deg, #334155 0%, #475569 100%)/' "$CSS"
sed -i 's/linear-gradient(135deg, #06b6d4 0%, #2563eb 100%)/linear-gradient(135deg, #475569 0%, #64748b 100%)/' "$CSS"

# Actualizar todos los rgba azules a grises
sed -i 's/rgba(37, 99, 235/rgba(99, 102, 241/g' "$CSS"
sed -i 's/rgba(14, 165, 233/rgba(100, 116, 139/g' "$CSS"

# ==========================================
# 3. CORREGIR MÁRGENES DEL CHAT
# ==========================================

# Eliminar padding excesivo en contenedor principal
sed -i '/\.chat-messages-container {/,/^}/ s/padding: 2.5rem 3rem;/padding: 1.5rem 2rem;/' "$CSS"

# Normalizar padding del input
sed -i '/\.chat-input-container {/,/^}/ s/padding: 1.75rem 2.5rem;/padding: 1.25rem 2rem;/' "$CSS"

# Ajustar margen izquierdo del chat main
sed -i '/\.chat-main-content {/,/transition:/ s/margin-left: var(--sidebar-width);/margin-left: var(--sidebar-width);\n    padding: 0;/' "$CSS"

# Corregir gap entre mensajes
sed -i '/\.chat-messages-container {/,/^}/ s/gap: 1.5rem;/gap: 1.25rem;/' "$CSS"

# Sidebar padding normalizado
sed -i '/\.sidebar-section {/,/^}/ s/padding: 1.25rem 1.5rem;/padding: 1rem 1.25rem;/' "$CSS"

echo "✅ Aplicados: Fuente Manrope + Paleta Gris Neutro + Márgenes corregidos"
