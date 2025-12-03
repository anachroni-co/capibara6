#!/bin/bash
OUT="/home/elect/capibara6/web/chat-styles-neuromorphic-dark-v2.css"

# Aplicar efectos neuromorphic a componentes clave
sed -i 's/box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);/box-shadow: var(--neuro-flat);/' "$OUT"
sed -i 's/box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);/box-shadow: var(--neuro-raised);/' "$OUT"
sed -i 's/box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);/box-shadow: var(--neuro-raised);/' "$OUT"
sed -i 's/box-shadow: var(--shadow-md);/box-shadow: var(--neuro-flat);/' "$OUT"
sed -i 's/box-shadow: var(--shadow-lg);/box-shadow: var(--neuro-hover);/' "$OUT"

# Aplicar efecto pressed a inputs
sed -i '/\.chat-input-wrapper {/,/^}/ s/transition: var(--transition);/transition: var(--transition);\n    box-shadow: var(--neuro-pressed);/' "$OUT"

# Aplicar efecto pressed a otros inputs
sed -i '/\.form-input,/,/^}/ s/transition: var(--transition);/transition: var(--transition);\n    box-shadow: var(--neuro-pressed);/' "$OUT"

echo "Neuromorphic effects applied!"
