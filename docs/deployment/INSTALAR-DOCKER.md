# 🐳 Instalar Docker en WSL

## El Problema

Estás en **WSL (Windows Subsystem for Linux)** y necesitas Docker para ejecutar los servicios de Capibara6.

## ✅ Scripts Ya Corregidos

Los scripts ya están listos. El problema de `\r` (fin de línea Windows) ha sido solucionado.

Si vuelves a tener este problema en el futuro, ejecuta:

```bash
./fix-line-endings.sh
```

---

## 🐳 Instalar Docker en WSL

### Opción 1: Docker Desktop (Recomendado para Windows)

1. **Descargar Docker Desktop**
   - Ir a: https://www.docker.com/products/docker-desktop
   - Descargar e instalar para Windows

2. **Configurar WSL 2 Integration**
   - Abrir Docker Desktop
   - Settings → Resources → WSL Integration
   - Activar tu distribución de WSL (Ubuntu, Debian, etc.)
   - Apply & Restart

3. **Verificar desde WSL**
   ```bash
   docker --version
   docker-compose --version
   ```

---

### Opción 2: Docker Engine en WSL (Sin Docker Desktop)

```bash
# 1. Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar dependencias
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Añadir GPG key de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Añadir repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Iniciar Docker
sudo service docker start

# 7. Añadir tu usuario al grupo docker
sudo usermod -aG docker $USER

# 8. Aplicar cambios de grupo (o reiniciar WSL)
newgrp docker

# 9. Verificar instalación
docker --version
docker compose version
```

---

## 🚀 Después de Instalar Docker

Una vez instalado Docker, puedes usar los scripts:

### Opción 1: Script Maestro (Interactivo)

```bash
./start-capibara6.sh
```

Selecciona opción **1** para iniciar todos los servicios.

### Opción 2: Inicio Rápido

```bash
./quick-start.sh
```

---

## 🔧 Problemas Comunes en WSL

### Docker daemon no inicia

```bash
# Iniciar manualmente
sudo service docker start

# O con systemd (WSL 2)
sudo systemctl start docker
```

### Permisos denegados

```bash
# Añadir usuario a grupo docker
sudo usermod -aG docker $USER

# Cerrar y reabrir terminal, o:
newgrp docker
```

### Error de conexión

```bash
# Verificar que Docker está corriendo
sudo service docker status

# Reiniciar Docker
sudo service docker restart
```

---

## 📋 Verificar Todo

Después de instalar Docker, ejecuta:

```bash
./verify.sh
```

Deberías ver:
```
✓ Python instalado
✓ Docker instalado
✓ Docker Compose instalado
```

---

## 🎯 Flujo Completo

```bash
# 1. Instalar Docker (elegir Opción 1 o 2 arriba)

# 2. Verificar instalación
docker --version
docker-compose --version

# 3. Iniciar Capibara6
./start-capibara6.sh

# 4. Acceder a los servicios
# Frontend: http://localhost:8080
# Backend:  http://localhost:5000
# n8n:      http://localhost:5678
```

---

## 🆘 Si Sigues Teniendo Problemas

### Problema: Error de fin de línea (`\r`)

```bash
./fix-line-endings.sh
```

### Problema: Docker no está instalado

Sigue las instrucciones de instalación arriba.

### Problema: Puertos ocupados

```bash
# Ver qué usa el puerto
lsof -i :5000

# O en Windows (PowerShell)
netstat -ano | findstr :5000
```

---

## 📚 Documentación

- **INICIO-RAPIDO.md** - Guía rápida
- **SERVICIOS.md** - Documentación completa
- **verify.sh** - Verificar instalación

---

**Una vez Docker esté instalado, todo funcionará! 🚀**
