# 🔧 Resumen de Errores y Soluciones

## ❌ Errores Detectados en el Frontend

### 1. Error CORS en `/api/ai/classify`
```
Access to fetch at 'http://34.12.166.76:5001/api/ai/classify' 
blocked by CORS policy
```

**Causa**: 
- El frontend intenta usar `/api/ai/classify` que puede no existir
- El backend no tiene CORS configurado para `localhost:8000`

**Solución Aplicada**:
- ✅ Actualizado `chat-page.js` para usar `/api/health` directamente
- ✅ Añadido modo CORS correcto en la petición

**Solución Pendiente**:
- Verificar que el backend en bounty2 tenga CORS configurado:
```python
CORS(app, origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://www.capibara6.com"
])
```

### 2. ERR_CONNECTION_REFUSED en Backend
```
POST http://34.12.166.76:5001/api/ai/classify net::ERR_FAILED
```

**Causa**: El backend no está corriendo en bounty2 puerto 5001

**Solución**:
```bash
# Conectarse a bounty2
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001

# Iniciar backend
cd ~/capibara6/backend
screen -dmS backend python3 capibara6_integrated_server.py

# Verificar que escucha en 0.0.0.0, no solo 127.0.0.1
```

### 3. ERR_CONNECTION_REFUSED en MCP (puerto 5010)
```
GET http://34.175.136.104:5010/health net::ERR_CONNECTION_REFUSED
```

**Causa**: El servicio MCP en gpt-oss-20b puerto 5010 no está corriendo

**Solución**:
```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001

# Iniciar servicios
cd ~/capibara6
./check_and_start_gpt_oss_20b.sh
```

## ✅ Cambios Realizados

1. **`web/chat-page.js`**: Actualizado para usar `/api/health` en lugar de `/api/ai/classify`
2. **`web/config.js`**: Configuración actualizada con IPs de las VMs
3. **Scripts creados**: Para verificar e iniciar servicios en cada VM

## 🚀 Próximos Pasos

### Paso 1: Iniciar Backend en bounty2

```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001
cd ~/capibara6/backend
screen -dmS backend python3 capibara6_integrated_server.py
```

**IMPORTANTE**: Verificar que el código tenga:
```python
app.run(host='0.0.0.0', port=5001)  # ✅ Correcto
# NO: app.run(host='127.0.0.1', port=5001)  # ❌ Incorrecto
```

### Paso 2: Iniciar Servicios en gpt-oss-20b

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001
cd ~/capibara6
./check_and_start_gpt_oss_20b.sh
```

### Paso 3: Verificar CORS en Backend

Asegurar que el backend tiene CORS configurado:

```python
from flask_cors import CORS

CORS(app, origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://www.capibara6.com"
])
```

### Paso 4: Probar desde el Frontend

1. Recargar `http://localhost:8000/chat.html`
2. Abrir consola del navegador (F12)
3. Verificar que no haya errores CORS
4. Verificar que se conecta al backend

## 📝 Checklist Final

- [ ] Backend corriendo en bounty2 (puerto 5001)
- [ ] Backend escuchando en 0.0.0.0
- [ ] CORS configurado para localhost:8000
- [ ] Servicios corriendo en gpt-oss-20b (5000, 5002, 5003, 5010, 5678)
- [ ] Firewall configurado para permitir tu IP
- [ ] Frontend puede conectarse sin errores CORS

---

**Última actualización**: Noviembre 2025

