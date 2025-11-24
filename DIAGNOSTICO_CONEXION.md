# 🔍 Diagnóstico de Conexión - Capibara6

## ❌ Error Actual

```
ERR_CONNECTION_REFUSED en http://34.12.166.76:5001/api/ai/classify
```

## 🔧 Soluciones Implementadas

### 1. Código Actualizado

- ✅ `web/chat-page.js` - Actualizado para usar `/api/health` en lugar de `/api/ai/classify`
- ✅ Mejor manejo de errores con mensajes descriptivos
- ✅ Timeout configurado (5 segundos)

### 2. Página de Diagnóstico

Abre en tu navegador:
```
http://localhost:8000/test_backend_connection.html
```

Esta página probará automáticamente varios endpoints para identificar cuál está disponible.

## 🔍 Verificación Manual

### Paso 1: Verificar que el servicio está corriendo en bounty2

Conéctate a la VM:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

Luego verifica:
```bash
# Ver qué procesos están corriendo
ps aux | grep -E "(python|ollama|node)"

# Ver qué puertos están escuchando
sudo netstat -tuln | grep -E "(5001|5000|11434)"

# O usar ss
sudo ss -tuln | grep -E "(5001|5000|11434)"

# Probar localmente en la VM
curl http://localhost:5001/api/health
curl http://localhost:11434/api/tags
```

### Paso 2: Verificar Firewall de Google Cloud

El firewall debe permitir conexiones desde tu IP local al puerto 5001:

```bash
# Ver reglas de firewall actuales
gcloud compute firewall-rules list --project=mamba-001

# Crear regla si no existe (reemplaza TU_IP_LOCAL)
gcloud compute firewall-rules create allow-backend-dev \
  --allow tcp:5001 \
  --source-ranges TU_IP_LOCAL/32 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso al backend desde desarrollo local"
```

### Paso 3: Verificar IP Correcta

Obtén la IP actual de bounty2:
```bash
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

Si la IP es diferente, actualiza `web/config.js`:
```javascript
BOUNTY2: 'NUEVA_IP',
```

### Paso 4: Probar Conexión desde tu Portátil

```bash
# Probar conectividad básica
ping 34.12.166.76

# Probar puerto 5001
curl -v http://34.12.166.76:5001/api/health

# Probar puerto 11434 (Ollama)
curl http://34.12.166.76:11434/api/tags
```

## 🎯 Posibles Causas del Error

### 1. Servicio no está corriendo
**Solución**: Iniciar el servicio en bounty2
```bash
# En bounty2
cd /ruta/al/proyecto/backend
python3 server.py
# O
python3 capibara6_integrated_server.py
```

### 2. Puerto incorrecto
**Solución**: Verificar qué puerto está usando realmente el servicio
- Puede ser 5000 en lugar de 5001
- Puede ser otro puerto según la configuración

### 3. Firewall bloqueando
**Solución**: Configurar regla de firewall en Google Cloud

### 4. IP incorrecta
**Solución**: Obtener IP actual y actualizar configuración

### 5. Servicio escuchando solo en localhost
**Solución**: Asegurar que el servicio escuche en `0.0.0.0`:
```python
app.run(host='0.0.0.0', port=5001)  # No '127.0.0.1'
```

## 📝 Checklist de Verificación

- [ ] Servicio corriendo en bounty2
- [ ] Puerto correcto identificado
- [ ] IP pública correcta de bounty2
- [ ] Firewall configurado correctamente
- [ ] Servicio escuchando en 0.0.0.0 (no solo localhost)
- [ ] CORS configurado en el backend
- [ ] Conectividad desde portátil verificada

## 🆘 Siguiente Paso

1. Abre `http://localhost:8000/test_backend_connection.html`
2. Revisa qué endpoints responden
3. Comparte los resultados para diagnóstico adicional

---

**Última actualización**: Noviembre 2025

