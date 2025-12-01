#!/bin/bash
# Script para convertir CSS a neuromorphic dark

INPUT="/home/elect/capibara6/web/chat-styles.backup.css"
OUTPUT="/home/elect/capibara6/web/chat-styles-neuromorphic-dark-v2.css"

# Copiar el archivo original
cp "$INPUT" "$OUTPUT"

# Reemplazar variables de color para dark neuromorphic
sed -i 's/--bg-primary: #0f172a/--bg-primary: #16213e/' "$OUTPUT"
sed -i 's/--bg-secondary: #1e293b/--bg-secondary: #1a2332/' "$OUTPUT"
sed -i 's/--bg-tertiary: #334155/--bg-tertiary: #1e2940/' "$OUTPUT"
sed -i 's/--bg-card: #1e293b/--bg-card: #1a2332/' "$OUTPUT"
sed -i 's/--bg-elevated: #273549/--bg-elevated: #1f2937/' "$OUTPUT"

# Agregar variables neuromorphic después de la línea de shadow-xl
sed -i '/--shadow-xl:/a\    \n    /* Neuromorphic shadows */\n    --shadow-light: rgba(255, 255, 255, 0.05);\n    --shadow-dark: rgba(0, 0, 0, 0.6);\n    --neuro-raised: 6px 6px 12px var(--shadow-dark), -4px -4px 8px var(--shadow-light);\n    --neuro-pressed: inset 4px 4px 8px var(--shadow-dark), inset -2px -2px 4px var(--shadow-light);\n    --neuro-flat: 4px 4px 8px var(--shadow-dark), -2px -2px 6px var(--shadow-light);\n    --neuro-hover: 8px 8px 16px var(--shadow-dark), -6px -6px 12px var(--shadow-light);' "$OUTPUT"

echo "Neuromorphic CSS created: $OUTPUT"
