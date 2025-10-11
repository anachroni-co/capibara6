# ✅ Activar Smart MCP - Pasos Finales

## 🎯 Estado Actual

| Servicio | Estado en VM | Estado en Frontend |
|----------|--------------|-------------------|
| Coqui TTS | ✅ Corriendo (5002) | ✅ Funciona (si variables configuradas) |
| Smart MCP | ✅ Corriendo (5010) | ❌ No disponible |

**Mensaje actual:** `ℹ️ Smart MCP no disponible (se usará modo directo)`

---

## 🔧 Problema

Smart MCP está **corriendo en la VM** pero el frontend **no puede conectarse** porque:

1. ❌ Firewall puerto 5010 no abierto
2. ❌ Variable `SMART_MCP_URL` no configurada en Vercel

---

## ✅ Solución - 3 Pasos

### PASO 1: Abrir Firewall (Desde tu PC)

```bash
gcloud compute firewall-rules create allow-smart-mcp-5010 --allow=tcp:5010 --source-ranges=0.0.0.0/0 --description="Smart MCP Server"
```

### PASO 2: Configurar Variable en Vercel

Ve a: https://vercel.com → Settings → Environment Variables

**Agregar:**

```
Name:  SMART_MCP_URL
Value: http://34.175.104.187:5010/analyze
```

Marcar: ✅ Production ✅ Preview ✅ Development

**Guardar**

### PASO 3: Re-deploy y Recargar

1. En Vercel: Deployments → Redeploy
2. En navegador: `Ctrl + Shift + R`

---

## 🎉 Resultado Esperado

Después de configurar verás:

### ANTES:
```javascript
ℹ️ Smart MCP no disponible (se usará modo directo)
```

### DESPUÉS:
```javascript
✅ Smart MCP activo: Selective RAG
🔍 Analizando query con Smart MCP...
✅ Contexto agregado desde Smart MCP
```

---

## 🧪 Test Manual

Desde tu PC:

```bash
# Test directo al servidor MCP
curl http://34.175.104.187:5010/health

# Debería responder (después de abrir firewall):
{
  "service": "capibara6-mcp",
  "status": "healthy",
  "contexts_available": 3,
  "tools_available": 3
}
```

---

## 📊 Beneficios de Smart MCP

Una vez activo:

✅ **Contexto verificado** sobre Capibara6  
✅ **Fecha actual** correcta  
✅ **Cálculos matemáticos** precisos  
✅ **Reduce alucinaciones**  
✅ **Solo agrega contexto cuando es necesario** (Selective RAG)  

---

## 🎯 Resumen con Tu IP

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VARIABLES EN VERCEL (2 variables):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name:  SMART_MCP_URL
Value: http://34.175.104.187:5010/analyze

Name:  KYUTAI_TTS_URL
Value: http://34.175.104.187:5002/tts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Ejecuta el comando de firewall y configura la variable SMART_MCP_URL en Vercel.** 🚀

