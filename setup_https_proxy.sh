#!/bin/bash

echo "🔒 Configurando HTTPS proxy en la VM..."

gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001" --command="
    echo '📦 Instalando nginx...'
    sudo apt update
    sudo apt install -y nginx
    
    echo '🔧 Configurando proxy HTTPS...'
    sudo tee /etc/nginx/sites-available/capibara6 > /dev/null <<EOF
server {
    listen 443 ssl;
    server_name 34.175.215.109;
    
    # SSL auto-signed (para desarrollo)
    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
    
    # Proxy al servidor Flask
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # CORS headers
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        add_header Access-Control-Allow-Headers 'Content-Type';
    }
}
EOF

    echo '🔗 Habilitando sitio...'
    sudo ln -sf /etc/nginx/sites-available/capibara6 /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    echo '🧪 Probando configuración...'
    sudo nginx -t
    
    echo '🔄 Reiniciando nginx...'
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    
    echo '📊 Estado de nginx:'
    sudo systemctl status nginx --no-pager
    
    echo '🌐 Verificando puerto 443:'
    netstat -tlnp | grep :443
"

echo "✅ HTTPS proxy configurado!"
echo "🌐 URLs disponibles:"
echo "  • HTTPS: https://34.175.215.109/api/chat"
echo "  • HTTP:  http://34.175.215.109:5000/api/chat"
