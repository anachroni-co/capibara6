# 🚀 Gestión de Servicios - Capibara6

## 📋 Índice

- [Scripts Disponibles](#scripts-disponibles)
- [Servicios del Sistema](#servicios-del-sistema)
- [Inicio Rápido](#inicio-rápido)
- [Comandos Útiles](#comandos-útiles)
- [Troubleshooting](#troubleshooting)

---

## 🛠️ Scripts Disponibles

### 1. **start-capibara6.sh** (Script Maestro - RECOMENDADO)

Script interactivo completo para gestionar todos los servicios.

```bash
./start-capibara6.sh
```

**Características:**
- ✅ Menú interactivo con 9 opciones
- ✅ Verificación de requisitos (Docker, Python)
- ✅ Estado detallado de todos los servicios
- ✅ Inicio/parada individual o completa
- ✅ Visualización de logs en tiempo real
- ✅ URLs de acceso rápido
- ✅ Colores y formato limpio

**Opciones del Menú:**
1. ▶️  Iniciar TODOS los servicios
2. 🐳 Iniciar solo servicios Docker
3. 🐍 Iniciar solo Backend Python
4. 🌐 Iniciar solo Frontend
5. 📊 Ver estado de servicios
6. 📜 Ver logs
7. 🔗 Mostrar URLs de acceso
8. ⏹️  Detener todos los servicios
9. 🔄 Reiniciar servicios
0. ❌ Salir

---

### 2. **quick-start.sh** (Inicio Rápido)

Script simplificado para desarrollo rápido.

```bash
./quick-start.sh
```

**Características:**
- Inicio rápido de todos los servicios
- Sin interacción requerida
- Perfecto para desarrollo

---

## 🐳 Servicios del Sistema

### **Servicios Docker (docker-compose.yml)**

| Servicio | Puerto | Descripción | Estado |
|----------|--------|-------------|--------|
| **capibara6-api** | 8000 | API REST Principal | ✅ |
| **capibara6-graphql** | 8001 | API GraphQL | ✅ |
| **capibara6-worker** | - | Workers Background (3 réplicas) | ✅ |
| **capibara6-postgres** | 5432 | PostgreSQL 15 | ✅ |
| **capibara6-timescaledb** | 5433 | TimescaleDB para métricas | ✅ |
| **capibara6-redis** | 6379 | Cache y colas | ✅ |
| **capibara6-nginx** | 80, 443 | Load Balancer | ✅ |
| **capibara6-prometheus** | 9090 | Métricas | ✅ |
| **capibara6-grafana** | 3000 | Dashboards | ✅ |
| **capibara6-jaeger** | 16686 | Tracing distribuido | ✅ |
| **capibara6-n8n** | 5678 | Automatización workflows | ✅ |

### **Servicios Python**

| Servicio | Puerto | Archivo | Descripción |
|----------|--------|---------|-------------|
| **Backend API** | 5000 | `server.py` | Servidor principal |
| **Frontend** | 8080 | Web simple | Interfaz web |

---

## ⚡ Inicio Rápido

### Opción 1: Script Maestro (Recomendado)

```bash
# Dar permisos de ejecución (solo primera vez)
chmod +x start-capibara6.sh

# Ejecutar
./start-capibara6.sh
```

Selecciona opción `1` para iniciar todos los servicios.

### Opción 2: Quick Start

```bash
# Dar permisos de ejecución (solo primera vez)
chmod +x quick-start.sh

# Ejecutar
./quick-start.sh
```

### Opción 3: Manual con Docker Compose

```bash
# Iniciar todos los servicios Docker
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Opción 4: Backend Python Standalone

```bash
cd backend

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# Iniciar servidor
python3 server.py
```

---

## 📍 URLs de Acceso

### Aplicación Principal

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Frontend | http://localhost:8080 | - |
| Backend API | http://localhost:5000 | - |
| API Docs | http://localhost:8000/docs | - |

### APIs

| Servicio | URL | Descripción |
|----------|-----|-------------|
| REST API | http://localhost:8000 | API Principal |
| GraphQL | http://localhost:8001/graphql | API GraphQL |
| GraphQL Playground | http://localhost:8001/graphql | IDE GraphQL |

### Automatización

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| n8n | http://localhost:5678 | Configurar en primer acceso |

### Monitorización

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Grafana | http://localhost:3000 | admin / capibara6_admin |
| Prometheus | http://localhost:9090 | - |
| Jaeger | http://localhost:16686 | - |

### Bases de Datos

| Servicio | Host | Puerto | Usuario | Password | Base de Datos |
|----------|------|--------|---------|----------|---------------|
| PostgreSQL | localhost | 5432 | capibara6 | capibara6_password | capibara6 |
| TimescaleDB | localhost | 5433 | capibara6 | capibara6_password | capibara6_metrics |
| Redis | localhost | 6379 | - | - | - |

---

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f capibara6-api
docker-compose logs -f capibara6-n8n

# Reiniciar un servicio
docker-compose restart capibara6-api

# Reconstruir imágenes
docker-compose build

# Iniciar con reconstrucción
docker-compose up -d --build

# Limpiar volúmenes (⚠️ CUIDADO: Borra datos)
docker-compose down -v
```

### Docker

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver logs de un contenedor
docker logs -f capibara6-api

# Entrar a un contenedor
docker exec -it capibara6-api bash
docker exec -it capibara6-postgres psql -U capibara6

# Ver uso de recursos
docker stats

# Ver redes
docker network ls

# Ver volúmenes
docker volume ls
```

### Backend Python

```bash
# Ver proceso corriendo
ps aux | grep server.py

# Detener proceso
kill $(cat backend/logs/backend.pid)

# Ver logs en tiempo real
tail -f backend/logs/backend.log

# Ver puerto usado
lsof -i :5000
```

---

## 🐛 Troubleshooting

### Problema: Docker no inicia

**Síntomas:**
```
Cannot connect to the Docker daemon
```

**Solución:**
```bash
# Verificar que Docker está corriendo
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker

# Habilitar Docker al inicio
sudo systemctl enable docker
```

---

### Problema: Puerto ya en uso

**Síntomas:**
```
Error: bind: address already in use
```

**Solución:**
```bash
# Ver qué proceso usa el puerto (ej: 5000)
lsof -i :5000

# Matar proceso
kill -9 <PID>

# O cambiar puerto en docker-compose.yml
```

---

### Problema: Contenedor no inicia

**Síntomas:**
Contenedor aparece como `Exited` o `Restarting`

**Solución:**
```bash
# Ver logs del contenedor
docker logs capibara6-api

# Ver detalles del error
docker inspect capibara6-api

# Reconstruir contenedor
docker-compose up -d --build capibara6-api
```

---

### Problema: Base de datos no conecta

**Síntomas:**
```
connection refused
could not connect to server
```

**Solución:**
```bash
# Verificar que PostgreSQL está corriendo
docker ps | grep postgres

# Ver logs de PostgreSQL
docker logs capibara6-postgres

# Reiniciar PostgreSQL
docker-compose restart postgres

# Verificar conexión
docker exec -it capibara6-postgres psql -U capibara6 -c "SELECT 1"
```

---

### Problema: n8n no guarda workflows

**Síntomas:**
Workflows se pierden al reiniciar

**Solución:**
```bash
# Verificar volumen de n8n
docker volume inspect capibara6_n8n_data

# Verificar permisos
docker exec capibara6-n8n ls -la /home/node/.n8n

# Recrear volumen (⚠️ perderás datos)
docker-compose down
docker volume rm capibara6_n8n_data
docker-compose up -d
```

---

### Problema: Frontend no carga

**Síntomas:**
`ERR_CONNECTION_REFUSED` en el navegador

**Solución:**
```bash
# Verificar que el servidor web está corriendo
lsof -i :8080

# Iniciar servidor web simple
cd web
python3 -m http.server 8080

# O usar el script
./start-capibara6.sh
```

---

### Problema: Backend API da error 500

**Síntomas:**
API responde con error interno

**Solución:**
```bash
# Ver logs del backend
tail -f backend/logs/backend.log

# O desde Docker
docker logs -f capibara6-api

# Verificar variables de entorno
docker exec capibara6-api env | grep -E "DATABASE|REDIS"

# Reiniciar backend
docker-compose restart capibara6-api
```

---

### Problema: Memoria/CPU alta

**Síntomas:**
Sistema lento, contenedores consumen muchos recursos

**Solución:**
```bash
# Ver uso de recursos
docker stats

# Limitar recursos en docker-compose.yml (ya configurado)
# Ver sección "deploy.resources"

# Reducir workers
docker-compose up -d --scale capibara6-worker=1

# Limpiar recursos no usados
docker system prune -a --volumes
```

---

## 📊 Verificar Estado Completo

### Opción 1: Script maestro

```bash
./start-capibara6.sh
# Seleccionar opción 5
```

### Opción 2: Manual

```bash
# Servicios Docker
docker-compose ps

# Backend Python
lsof -i :5000

# Frontend
lsof -i :8080

# Salud de n8n
curl http://localhost:5678/healthz

# Salud de API
curl http://localhost:8000/health
```

---

## 🔄 Flujo de Trabajo Recomendado

### Desarrollo

```bash
# 1. Iniciar servicios base (DB, Redis, etc.)
docker-compose up -d postgres redis timescaledb

# 2. Iniciar backend en modo desarrollo
cd backend
source venv/bin/activate
python3 server.py

# 3. Frontend
cd web
python3 -m http.server 8080
```

### Producción

```bash
# Usar script maestro
./start-capibara6.sh
# Opción 1: Iniciar TODOS los servicios
```

---

## 📝 Logs y Monitorización

### Ver todos los logs

```bash
# Docker Compose
docker-compose logs -f

# Solo errores
docker-compose logs -f | grep -i error

# Backend Python
tail -f backend/logs/backend.log

# Frontend
tail -f backend/logs/frontend.log
```

### Monitorización en Grafana

1. Acceder: http://localhost:3000
2. Login: `admin` / `capibara6_admin`
3. Navegar a Dashboards
4. Ver métricas de sistema

---

## 🎯 Próximos Pasos

Después de iniciar los servicios:

1. **Configurar n8n**
   - Acceder a http://localhost:5678
   - Crear cuenta admin
   - Importar templates desde `/backend/data/n8n/workflows/templates/`

2. **Verificar API**
   - Acceder a http://localhost:8000/docs
   - Probar endpoints

3. **Configurar Grafana**
   - Importar dashboards custom
   - Configurar alertas

4. **Frontend**
   - Abrir http://localhost:8080
   - Probar chat con modelos

---

## 📧 Soporte

Si encuentras problemas:

1. Revisa los logs
2. Consulta esta documentación
3. Revisa issues en GitHub
4. Contacta: info@anachroni.co

---

**¡Capibara6 listo para usar! 🦫🚀**
