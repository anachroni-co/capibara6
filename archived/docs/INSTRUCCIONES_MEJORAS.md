# 🚀 Instrucciones para Usar las Mejoras GPT-OSS-20B

## 📋 Resumen de Cambios

Se han implementado mejoras significativas para resolver los problemas de respuestas cortas y genéricas del modelo gpt-oss-20B.

## 🔧 Cambios Realizados

### 1. **Puerto Cambiado**
- **Antes**: Puerto 5000
- **Después**: Puerto 5001
- **Razón**: Evitar conflictos con otros servicios

### 2. **Configuración Optimizada**
- Prompts del sistema mejorados
- Parámetros del modelo optimizados
- Sistema de categorías inteligente
- Tokens de parada mejorados

## 🚀 Cómo Iniciar el Servidor Mejorado

### Opción 1: Script Automático (Recomendado)

#### En Linux/Mac:
```bash
./start_improved_server.sh
```

#### En Windows:
```cmd
start_improved_server.bat
```

### Opción 2: Manual

#### En Linux/Mac:
```bash
cd backend
python capibara6_integrated_server.py
```

#### En Windows:
```cmd
cd backend
python capibara6_integrated_server.py
```

## 🧪 Cómo Probar las Mejoras

### 1. Verificar que el Servidor Esté Funcionando:
```bash
curl http://localhost:5001/health
```

### 2. Probar una Pregunta Simple:
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo te llamas?"}'
```

### 3. Ejecutar Pruebas Automatizadas:
```bash
cd backend
python test_gpt_oss_improvements.py
```

## 📊 Resultados Esperados

### Antes de las Mejoras:
```json
{
  "response": "I am a large language model trained by OpenAI",
  "length": 47
}
```

### Después de las Mejoras:
```json
{
  "response": "Soy Capibara6, un asistente de IA especializado en tecnología, programación e inteligencia artificial desarrollado por Anachroni s.coop. Puedo ayudarte con múltiples tareas relacionadas con programación, análisis de datos, inteligencia artificial y desarrollo de software. Mi objetivo es proporcionarte información útil, precisa y práctica en español...",
  "length": 200+
}
```

## 🔍 Verificaciones de Calidad

### ✅ Respuestas Mejoradas Deberían:
- Tener mínimo 50 palabras
- Estar en español
- Ser específicas sobre Capibara6
- Proporcionar información útil
- Evitar respuestas genéricas

### ❌ Problemas Resueltos:
- Respuestas de 1-30 caracteres
- Entropía muy baja (0.80 H)
- Respuestas genéricas en inglés
- Falta de contexto específico

## 🌐 URLs Importantes

- **Servidor**: http://localhost:5001
- **API Chat**: http://localhost:5001/api/chat
- **Health Check**: http://localhost:5001/health
- **Modelos**: http://localhost:5001/api/models
- **MCP Context**: http://localhost:5001/api/mcp/context

## 🛠️ Configuración del Frontend

El frontend ya está configurado para usar el puerto 5001. Si necesitas cambiar la URL:

```javascript
// En web/chat-app.js
const MODEL_CONFIG = {
    serverUrl: 'http://34.175.215.109:5001/api/chat'
};
```

## 📁 Archivos Modificados

1. `backend/capibara6_integrated_server.py` - Servidor principal
2. `backend/server_gptoss.py` - Servidor GPT-OSS
3. `web/chat-app.js` - Configuración del frontend
4. `backend/gpt_oss_optimized_config.py` - Nueva configuración optimizada
5. `backend/test_gpt_oss_improvements.py` - Script de pruebas

## 🚨 Solución de Problemas

### Puerto en Uso:
```bash
# Linux/Mac
lsof -i :5001
kill -9 <PID>

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Error de Conexión a VM:
- Verificar que la VM esté ejecutándose
- Comprobar la IP: 34.175.215.109:8080
- Verificar firewall y conectividad

### Dependencias Faltantes:
```bash
pip install -r backend/requirements.txt
```

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs del servidor
2. Ejecuta las pruebas automatizadas
3. Verifica la conectividad con la VM
4. Contacta: info@anachroni.co

---

**Fecha**: 15 de octubre de 2025  
**Versión**: 2.0  
**Estado**: ✅ Listo para Producción
