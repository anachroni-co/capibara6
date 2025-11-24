# 🔍 Diagnóstico de Conexión - Capibara6

## ✅ Estado Actual

### Servicios Funcionando
- **Ollama en bounty2**: ✅ Puerto 11434 ACCESIBLE
  - Modelos disponibles: `mistral:latest`, `phi3:mini`, `gpt-oss:20b`
  - IP: `34.12.166.76:11434`

### Servicios NO Funcionando
- **Backend Flask en bounty2**: ❌ Puertos 5000 y 5001 NO ACCESIBLES
  - Puerto 5000: Connection refused
  - Puerto 5001: Connection refused
  - IP: `34.12.166.76:5001` (esperado)

## 🔧 Soluciones Posibles

### Opción 1: El backend no está corriendo

**Verificar si el backend está corriendo en bounty2:**
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
# Dentro de la VM:
ps aux | grep python | grep -E "(server|flask|capibara6)"
sudo ss -tulnp | grep -E "(5000|5001)"
```

**Si no está corriendo, iniciarlo:**
```bash
# Dentro de bounty2
cd ~/capibara6/backend
source venv/bin/activate  # Si tienes venv
python3 server.py  # O el archivo que corresponda
# O usar el script de inicio:
python3 capibara6_integrated_server_ollama.py
```

### Opción 2: El firewall está bloqueando los puertos

**Crear regla de firewall para permitir acceso externo:**
```bash
# Permitir puerto 5001 desde Internet
gcloud compute firewall-rules create allow-bounty2-backend-5001 \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --target-tags bounty2 \
    --project=mamba-001 \
    --description="Permitir acceso externo al backend de Capibara6 en puerto 5001"

# Permitir puerto 5000 también (por si acaso)
gcloud compute firewall-rules create allow-bounty2-backend-5000 \
    --allow tcp:5000 \
    --source-ranges 0.0.0.0/0 \
    --target-tags bounty2 \
    --project=mamba-001 \
    --description="Permitir acceso externo al backend de Capibara6 en puerto 5000"
```

**Verificar tags de la VM:**
```bash
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(tags.items)"
```

Si la VM no tiene el tag `bounty2`, añadirlo:
```bash
gcloud compute instances add-tags bounty2 \
    --zone=europe-west4-a \
    --tags=bounty2 \
    --project=mamba-001
```

### Opción 3: El backend está corriendo en otro puerto

**Verificar todos los puertos abiertos:**
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001" --command="sudo ss -tulnp | grep LISTEN"
```

Si encuentras el backend en otro puerto (ej: 8000, 8080), actualiza la configuración del frontend.

## 🚀 Solución Rápida: Usar Ollama directamente

Mientras tanto, puedes configurar el frontend para usar Ollama directamente:

### Actualizar `web/config.js` temporalmente:

```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://34.12.166.76:11434'  // Usar Ollama directamente
        : 'https://www.capibara6.com',
    // ...
};
```

**Nota**: Esto requiere modificar el código del frontend para usar la API de Ollama directamente en lugar de la API del backend Flask.

## 📋 Checklist de Acciones

- [ ] Verificar si el backend está corriendo en bounty2
- [ ] Verificar tags de la VM bounty2
- [ ] Crear reglas de firewall para puertos 5000 y 5001
- [ ] Verificar todos los puertos abiertos en bounty2
- [ ] Iniciar el backend si no está corriendo
- [ ] Probar conexión desde local después de cada cambio

## 🔗 Comandos Útiles

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Ver procesos Python
ps aux | grep python | grep -v grep

# Ver puertos abiertos
sudo ss -tulnp | grep LISTEN

# Verificar firewall
gcloud compute firewall-rules list --project=mamba-001 --filter="targetTags:bounty2"

# Probar conexión desde local
curl http://34.12.166.76:5001/health
curl http://34.12.166.76:11434/api/tags
```

