#!/bin/bash
CSS="/home/elect/capibara6/web/chat-styles-neuromorphic-dark-v2.css"

# Backup
cp "$CSS" "$CSS.pre-improvements"

# 1. FUENTES MÁS FORMALES - Cambiar a fuentes empresariales
sed -i "s/font-family: 'Inter'/font-family: 'Roboto'/g" "$CSS"
sed -i "s/'Inter'/'Roboto'/g" "$CSS"

# 2. COLORES MÁS COORDINADOS - Paleta azul profesional coherente
sed -i 's/--primary: #6366f1;/--primary: #2563eb;/' "$CSS"
sed -i 's/--primary-dark: #4f46e5;/--primary-dark: #1e40af;/' "$CSS"
sed -i 's/--primary-light: #818cf8;/--primary-light: #60a5fa;/' "$CSS"
sed -i 's/--secondary: #ec4899;/--secondary: #0ea5e9;/' "$CSS"
sed -i 's/--accent: #14b8a6;/--accent: #06b6d4;/' "$CSS"

# Ajustar gradientes para nueva paleta
sed -i 's/linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)/linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%)/' "$CSS"
sed -i 's/linear-gradient(135deg, #14b8a6 0%, #6366f1 100%)/linear-gradient(135deg, #06b6d4 0%, #2563eb 100%)/' "$CSS"
sed -i 's/rgba(99, 102, 241/rgba(37, 99, 235/g' "$CSS"
sed -i 's/rgba(236, 72, 153/rgba(14, 165, 233/g' "$CSS"

# 3. MARGENES Y PADDING MEJORADOS
# Aumentar espaciado en contenedores principales
sed -i '/\.chat-messages-container {/,/^}/ s/padding: 2rem;/padding: 2.5rem 3rem;/' "$CSS"
sed -i '/\.chat-input-container {/,/^}/ s/padding: 1.5rem 2rem;/padding: 1.75rem 2.5rem;/' "$CSS"
sed -i '/\.sidebar-section {/,/^}/ s/padding: 1rem;/padding: 1.25rem 1.5rem;/' "$CSS"

# Mejorar espaciado de mensajes
sed -i '/\.chat-message {/,/^}/ s/gap: 1rem;/gap: 1.25rem;/' "$CSS"
sed -i '/\.message-content {/,/^}/ s/padding: 1.125rem 1.5rem;/padding: 1.25rem 1.75rem;/' "$CSS"

echo "Mejoras aplicadas: fuentes profesionales, colores coordinados, márgenes ajustados"
