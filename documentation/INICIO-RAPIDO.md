# 🚀 Inicio Rápido - Capibara6

## Configuración Inicial (Solo Primera Vez)

```bash
# 1. Dar permisos de ejecución a los scripts
chmod +x start-capibara6.sh quick-start.sh stop-capibara6.sh

# 2. Verificar que Docker está corriendo
docker --version
docker-compose --version

# 3. Verificar Python 3
python3 --version
```

---

## 🎯 Opción Recomendada: Script Maestro

### Iniciar Todo

```bash
./start-capibara6.sh
```

Selecciona opción **1** para iniciar todos los servicios.

### Detener Todo

```bash
./stop-capibara6.sh
```

---

## ⚡ Opción Rápida: Quick Start

### Iniciar

```bash
./quick-start.sh
```

### Detener

```bash
./stop-capibara6.sh
```

---

## 🌐 URLs Principales

Una vez iniciados los servicios, accede a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:8080 | Interfaz web principal |
| **Backend** | http://localhost:5000 | API REST backend |
| **n8n** | http://localhost:5678 | Automatización workflows |
| **Grafana** | http://localhost:3000 | Monitorización (admin/capibara6_admin) |
| **API Docs** | http://localhost:8000/docs | Documentación API |

---

## 📋 ¿Qué se Inicia?

### Servicios Docker (11 contenedores)

- ✅ API REST Principal (puerto 8000)
- ✅ API GraphQL (puerto 8001)
- ✅ Workers Background (3 réplicas)
- ✅ PostgreSQL (puerto 5432)
- ✅ TimescaleDB (puerto 5433)
- ✅ Redis (puerto 6379)
- ✅ Nginx (puertos 80, 443)
- ✅ Prometheus (puerto 9090)
- ✅ Grafana (puerto 3000)
- ✅ Jaeger (puerto 16686)
- ✅ n8n (puerto 5678)

### Servicios Python

- ✅ Backend API (puerto 5000)
- ✅ Frontend Web (puerto 8080)

---

## 🔍 Verificar Estado

### Con el Script Maestro

```bash
./start-capibara6.sh
# Seleccionar opción 5
```

### Manual

```bash
# Ver todos los contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Verificar backend Python
curl http://localhost:5000/health
```

---

## 🐛 Problemas Comunes

### Puerto ya en uso

```bash
# Ver qué usa el puerto
lsof -i :5000

# Matar proceso
kill -9 <PID>
```

### Docker no responde

```bash
# Reiniciar Docker
sudo systemctl restart docker
```

### Servicios no inician

```bash
# Ver logs detallados
docker-compose logs -f <nombre-servicio>

# Ejemplo:
docker-compose logs -f capibara6-api
```

---

## 📚 Documentación Completa

Para más detalles, consulta:

- **[SERVICIOS.md](./SERVICIOS.md)** - Documentación completa de servicios
- **[docs/n8n/README.md](./docs/n8n/README.md)** - Guía de n8n
- **[docs/n8n/TEMPLATES.md](./docs/n8n/TEMPLATES.md)** - Plantillas de workflows

---

## 🎓 Primeros Pasos Después de Iniciar

### 1. Configurar n8n (Primera vez)

1. Acceder a http://localhost:5678
2. Crear cuenta de administrador
3. Importar templates:
   ```bash
   # Las plantillas están en:
   backend/data/n8n/workflows/templates/
   ```

### 2. Probar el Frontend

1. Acceder a http://localhost:8080
2. Abrir chat.html
3. Probar conversación con el modelo

### 3. Ver Métricas en Grafana

1. Acceder a http://localhost:3000
2. Login: `admin` / `capibara6_admin`
3. Navegar a Dashboards

### 4. Probar la API

```bash
# Health check
curl http://localhost:5000/health

# Enviar mensaje al chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola Capibara6"}'
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# API Keys
E2B_API_KEY=tu_api_key_aqui
GOOGLE_CLOUD_PROJECT=tu_proyecto_gcp

# n8n
N8N_WEBHOOK_URL=http://localhost:5678/
N8N_ENCRYPTION_KEY=tu_clave_encriptacion
N8N_EXECUTIONS_MODE=regular
```

### Cambiar Puertos

Edita `docker-compose.yml` para cambiar puertos:

```yaml
services:
  capibara6-api:
    ports:
      - "8000:8000"  # Cambiar el primer número
```

---

## 🛑 Detener Servicios

### Opción 1: Script de detención

```bash
./stop-capibara6.sh
```

### Opción 2: Script maestro

```bash
./start-capibara6.sh
# Seleccionar opción 8
```

### Opción 3: Manual

```bash
# Detener Docker
docker-compose down

# Detener backend
kill $(cat backend/logs/backend.pid)

# Detener frontend
kill $(cat backend/logs/frontend.pid)
```

---

## 🔄 Reiniciar Servicios

### Con script maestro

```bash
./start-capibara6.sh
# Seleccionar opción 9
```

### Manual

```bash
./stop-capibara6.sh
./quick-start.sh
```

---

## 📊 Comandos Útiles

```bash
# Ver uso de recursos
docker stats

# Ver logs de un servicio
docker logs -f capibara6-api

# Entrar a un contenedor
docker exec -it capibara6-api bash

# Ver todos los contenedores (incluso parados)
docker ps -a

# Limpiar recursos no usados (⚠️ cuidado)
docker system prune -a
```

---

## 🆘 Soporte

- **Documentación**: Ver [SERVICIOS.md](./SERVICIOS.md)
- **Issues**: GitHub Issues
- **Email**: info@anachroni.co
- **Website**: https://www.capibara6.com

---

**¡Ya estás listo para usar Capibara6! 🦫🚀**
