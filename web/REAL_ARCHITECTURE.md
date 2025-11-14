# 🏗️ Arquitectura Real de las VMs de Capibara6

Después del análisis de las VMs, se ha descubierto la siguiente arquitectura real:

## 🖥️ VM `gpt-oss-20b` - `34.175.136.104` (europe-southwest1-b)
**PURPOTA**: Servidor principal de Capibara6
**SERVICIOS**:
- Puerto 5000: `server.py` (PID 2014617) - Servidor Capibara6 Principal
- Puerto 8080: Servidor Llama (modelo gpt-oss-20b)
- Puerto 5010: Posible MCP Server (según firewall)
- Puerto 5003: Posible MCP Server (según firewall)

## 🖥️ VM `bounty2` - `34.12.166.76` (europe-west4-a)  
**PROPÓSITO**: Backend de modelos y procesamiento
**SERVICIOS**:
- Puerto 8000: `python3 -m http.server 8000` - Servidor HTTP simple

## 🔌 Conexión entre sistemas
**Frontend** (`localhost:8000`) → **VM gpt-oss-20b** (`34.175.136.104:5000`) → **Modelos y MCP**

## 📝 Configuración actualizada
Los archivos han sido actualizados para usar `http://34.175.136.104:5000` como backend principal para chat y servicios.

## 🧪 Pruebas
Para probar la conexión real:
1. Ejecuta el frontend localmente en la VM bounty2 (puerto 8000)
2. Hará peticiones a `http://34.175.136.104:5000` para servicios de Capibara6
3. Se comunicará con los modelos en `http://34.175.136.104:8080` internamente

## ⚠️ Importante
Asegúrate de que el puerto 5000 en `gpt-oss-20b` esté accesible desde `bounty2` y viceversa según las reglas de firewall.