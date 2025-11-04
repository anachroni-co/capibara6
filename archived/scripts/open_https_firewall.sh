#!/bin/bash

echo "🔒 Abriendo puerto HTTPS (443) en el firewall..."

gcloud compute firewall-rules create allow-capibara6-https --allow tcp:443 --source-ranges 0.0.0.0/0 --description "Allow Capibara6 HTTPS on port 443"

echo "✅ Firewall configurado!"
echo "🌐 Ahora puedes usar: https://34.175.215.109"
