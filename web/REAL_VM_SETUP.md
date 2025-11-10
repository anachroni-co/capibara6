# 🚀 Configuración Real de Conexión a VM bounty2

Esta guía explica cómo identificar los servicios reales corriendo en la VM bounty2 y configurar adecuadamente la conexión desde el frontend.

## 🔍 Servicios Identificados

### 1. Ollama
- **Proceso**: `/usr/local/bin/ollama serve`
- **PID**: 91293
- **Puerto típico**: 11434
- **Comprobación**:
  ```bash
  # Verificar puerto de Ollama
  ss -tuln | grep 11434
  # o
  curl http://localhost:11434/api/tags
  ```

### 2. Capibara6 Integrated Server  
- **Proceso**: `python /home/elect/capibara6/backend/capibara6_integrated_server_ollama.py`
- **PID**: 711187
- **Puerto típico**: 5001 (Flask por defecto)
- **Comprobación**:
  ```bash
  # Verificar puerto de servidor Flask
  ss -tuln | grep 5001
  # o buscar el puerto exacto
  lsof -i -p 711187
  ```

### 3. Servidor BB (Node.js)
- **Proceso**: `node server.js`
- **PID**: 285392
- **Puerto típico**: 3000 o personalizado
- **Comprobación**:
  ```bash
  ss -tuln | grep -E "(3000|300[1-9])"
  # o
  lsof -i -p 285392
  ```

### 4. Otro servidor Python
- **Proceso**: `python -m main`
- **PID**: 760087  
- **Puerto**: Variable
- **Comprobación**:
  ```bash
  lsof -i -p 760087
  ```

## 🛠️ Comandos para Identificar Puertos Reales

Ejecuta estos comandos en la VM bounty2 para obtener la información real:

```bash
# Ver todos los puertos abiertos
sudo ss -tulnp

# Ver puertos específicos usados por los procesos
sudo lsof -i -p 711187    # Capibara6 Integrated Server
sudo lsof -i -p 91293     # Ollama
sudo lsof -i -p 285392    # Node BB Server
sudo lsof -i -p 760087    # Python main

# Ver puertos en uso por Python
sudo lsof -i -c python

# Ver puertos en uso por Node
sudo lsof -i -c node
```

## 🌐 IP Pública de la VM bounty2

Para obtener la IP pública real de la VM bounty2:

```bash
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

## 🔄 Actualización de Configuración Frontend

Una vez que tengas los puertos reales, actualiza los archivos de frontend:

### Para conexión directa a Capibara6 Integrated Server:
- Si está en puerto 5001: `http://[IP_PUBLICA_BOUNTY2]:5001`
- Endpoints:
  - `/api/chat` - Chat principal
  - `/api/mcp/status` - Estado MCP
  - `/api/mcp/tools/list` - Herramientas MCP
  - `/api/save-conversation` - Guardar conversaciones
  - `/api/save-lead` - Guardar leads

### Para conexión a Ollama directamente:
- Si está en puerto 11434: `http://[IP_PUBLICA_BOUNTY2]:11434`
- Endpoints:
  - `/api/tags` - Modelos disponibles
  - `/api/generate` - Generación de texto

## ✅ Prueba de Conexión

Después de configurar con los puertos reales:

```bash
# Prueba de conexión al servidor Capibara6
curl -X POST http://[IP_PUBLICA_BOUNTY2]:[PUERTO_REAL]/api/health

# Prueba de conexión a Ollama
curl http://[IP_PUBLICA_BOUNTY2]:11434/api/tags
```

## 🚨 Consideraciones de Firewall

Asegúrate de que los puertos necesarios estén abiertos en el firewall de Google Cloud:

```bash
# Ejemplo de regla de firewall para permitir acceso externo
gcloud compute firewall-rules create allow-bounty2-ports \
  --allow tcp:5001,tcp:8080,tcp:11434 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2
```

## 📞 Soporte

Si necesitas ayuda con la configuración:
1. Ejecuta los comandos de verificación de puertos
2. Consulta los logs de los servicios
3. Verifica el estado del firewall