# 🔥 Abrir Puerto 5678 para N8n - VM gpt-oss-20b

## 📋 Información

- **VM**: gpt-oss-20b
- **IP**: 34.175.136.104
- **Puerto**: 5678
- **Servicio**: N8n (Workflow Automation)
- **Proyecto**: mamba-001
- **Zona**: europe-southwest1-b

## 🚀 Opción 1: Usar el Script Automatizado

```bash
bash scripts/add_n8n_firewall_rule.sh
```

## 🔧 Opción 2: Comando Manual

```bash
gcloud compute firewall-rules create allow-n8n \
    --project=mamba-001 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:5678 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=gpt-oss-20b \
    --description="Allow N8n workflow automation on port 5678"
```

## ⚠️ Nota sobre Tags

Si la VM no tiene el tag `gpt-oss-20b`, puedes:

1. **Añadir el tag a la VM**:
```bash
gcloud compute instances add-tags gpt-oss-20b \
    --zone=europe-southwest1-b \
    --project=mamba-001 \
    --tags=gpt-oss-20b
```

2. **O crear la regla sin tag específico** (aplicará a todas las VMs):
```bash
gcloud compute firewall-rules create allow-n8n \
    --project=mamba-001 \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:5678 \
    --source-ranges=0.0.0.0/0 \
    --description="Allow N8n workflow automation on port 5678"
```

## ✅ Verificar la Regla

```bash
gcloud compute firewall-rules describe allow-n8n --project=mamba-001
```

## 🧪 Probar Conexión

Después de crear la regla, probar:

```bash
curl http://34.175.136.104:5678/healthz
```

O desde el navegador:
```
http://34.175.136.104:5678
```

## 📝 Actualizar Configuración

Una vez que el puerto esté abierto, la configuración en `web/config.js` ya está lista:

```javascript
N8N: window.location.hostname === 'localhost'
    ? 'http://34.175.136.104:5678'
    : null,
```

## 🔍 Verificar Reglas Existentes

```bash
gcloud compute firewall-rules list --project=mamba-001 --filter="name~allow"
```

