#!/bin/bash

echo "🔄 Reiniciando servicio Capibara6 en la VM..."

gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001" --command="
    echo '🔄 Reiniciando servicio capibara6-integrated...'
    sudo systemctl restart capibara6-integrated
    
    echo '⏳ Esperando 5 segundos...'
    sleep 5
    
    echo '📊 Estado del servicio:'
    sudo systemctl status capibara6-integrated --no-pager
    
    echo '🌐 Verificando puerto 5000:'
    netstat -tlnp | grep :5000
"

echo "✅ Servicio reiniciado. Prueba ahora el frontend."
