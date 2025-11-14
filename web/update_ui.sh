#!/bin/bash
echo "Actualizando UI de Capibara6..."

# Backup
cp chat.html chat.html.backup.$(date +%Y%m%d)
cp chat.css chat.css.backup.$(date +%Y%m%d) 2>/dev/null || true

# Descargar desde el servidor de Claude (si está disponible)
# O aplicar cambios manualmente

echo "Aplicando cambios al CSS..."

# Buscar y reemplazar en chat.css
if [ -f "chat.css" ]; then
    # Cambiar el background
    sed -i 's/background: #212121;/background: linear-gradient(135deg, #1a0b2e 0%, #2d1b4e 100%);/' chat.css
    echo "✓ Fondo actualizado"
fi

echo "Cambios aplicados. Recarga el navegador con Ctrl+Shift+R"
