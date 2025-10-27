# 🚀 Instrucciones para Desplegar Mejoras en la VM

## 📋 Resumen

Las mejoras para GPT-OSS-20B están listas para desplegar en tu VM de Google Cloud.

## 🔧 Opciones de Despliegue

### **Opción 1: Despliegue Automático (Recomendado)**

#### En Windows:
```cmd
deploy_improvements_to_vm.bat
```

#### En Linux/Mac:
```bash
chmod +x deploy_improvements_to_vm.sh
./deploy_improvements_to_vm.sh
```

### **Opción 2: Despliegue Rápido**

```bash
chmod +x quick_deploy.sh
./quick_deploy.sh
```

### **Opción 3: Conectar y Desplegar**

```bash
chmod +x connect_and_deploy.sh
./connect_and_deploy.sh
```

## 📦 Archivos que se Suben

### **Backend:**
- `backend/capibara6_integrated_server.py` - Servidor principal mejorado
- `backend/gpt_oss_optimized_config.py` - Nueva configuración optimizada
- `backend/server_gptoss.py` - Servidor GPT-OSS mejorado
- `backend/test_gpt_oss_improvements.py` - Script de pruebas

### **Frontend:**
- `web/chat-app.js` - Configuración actualizada

### **Scripts:**
- `start_improved_server.sh` - Script de inicio
- `test_quick.sh` - Script de prueba rápida

## 🖥️ Comandos en la VM

Una vez que los archivos estén en la VM, ejecuta:

```bash
# Conectar a la VM
ssh gmarco@34.175.215.109

# Ir al directorio del proyecto
cd /home/elect

# Hacer scripts ejecutables
chmod +x start_improved_server.sh test_quick.sh

# Iniciar servidor mejorado
./start_improved_server.sh
```

## 🧪 Probar las Mejoras

### **En la VM (terminal separada):**
```bash
# Conectar a la VM
ssh gmarco@34.175.215.109

# Ir al directorio
cd /home/elect

# Ejecutar prueba rápida
./test_quick.sh
```

### **Desde tu laptop:**
```bash
# Probar API directamente
curl -X POST http://34.175.215.109:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo te llamas?"}'
```

## 🔍 Verificaciones

### **1. Servidor Funcionando:**
```bash
curl http://34.175.215.109:5001/health
```

### **2. Respuesta Mejorada:**
```bash
curl -X POST http://34.175.215.109:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo te llamas?"}'
```

**Resultado esperado:**
- Respuesta de 200+ caracteres
- Menciona "Capibara6"
- Está en español
- No es genérica

## 🚨 Solución de Problemas

### **Error de Conexión SSH:**
```bash
# Verificar que la VM esté ejecutándose
gcloud compute instances list

# Verificar firewall
gcloud compute firewall-rules list
```

### **Puerto 5001 en Uso:**
```bash
# En la VM:
lsof -i :5001
kill -9 <PID>
```

### **Python no Encontrado:**
```bash
# En la VM:
which python3
which python
```

## 📊 Resultados Esperados

### **Antes:**
```json
{
  "response": "I am a large language model trained by OpenAI",
  "length": 47
}
```

### **Después:**
```json
{
  "response": "Soy Capibara6, un asistente de IA especializado en tecnología, programación e inteligencia artificial desarrollado por Anachroni s.coop. Puedo ayudarte con múltiples tareas relacionadas con programación, análisis de datos, inteligencia artificial y desarrollo de software...",
  "length": 200+
}
```

## 🌐 URLs de Acceso

- **Servidor**: http://34.175.215.109:5001
- **API Chat**: http://34.175.215.109:5001/api/chat
- **Health Check**: http://34.175.215.109:5001/health
- **Frontend**: http://34.175.215.109:8000 (si está configurado)

## 📞 Soporte

Si encuentras problemas:
1. Verifica la conexión SSH
2. Revisa los logs del servidor en la VM
3. Ejecuta las pruebas automatizadas
4. Contacta: info@anachroni.co

---

**🎉 ¡Las mejoras están listas para desplegar en la VM!**
