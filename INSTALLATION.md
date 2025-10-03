# Instalación y Configuración de capibara6

## Tabla de Contenidos
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Clonación del Repositorio](#clonación-del-repositorio)
- [Instalación del Backend](#instalación-del-backend)
- [Instalación del Frontend](#instalación-del-frontend)
- [Configuración del Sistema](#configuración-del-sistema)
- [Variables de Entorno](#variables-de-entorno)
- [Configuración del Servidor de Correo](#configuración-del-servidor-de-correo)
- [Ejecución del Sistema](#ejecución-del-sistema)
- [Verificación de la Instalación](#verificación-de-la-instalación)
- [Solución de Problemas](#solución-de-problemas)
- [Mantenimiento y Actualización](#mantenimiento-y-actualización)

## Requisitos del Sistema

### Hardware Requerido
- **Procesador**: Google TPU v5e-64 o v6e-64 (recomendado para entrenamiento)
- **Alternativa de Inferencia**: Google ARM Axion o AWS Graviton3
- **Memoria RAM**: 32GB o más
- **Almacenamiento**: SSD NVMe de 500GB o más
- **Conexión de Red**: Estable y de alta velocidad para acceso a servicios en la nube

### Software Requerido
- **Sistema Operativo**: Linux (Ubuntu 20.04+ o Debian 11+), Windows 10+ o macOS 10.15+
- **Python**: Versión 3.9 o superior
- **Node.js**: Versión 18 o superior (para herramientas de desarrollo)
- **Git**: Para control de versiones
- **Docker**: Opcional, para despliegue por contenedores
- **CUDA**: Opcional, para GPUs NVIDIA (no requerido para TPU/ARM)

## Clonación del Repositorio

```bash
# Clonar el repositorio principal
git clone https://github.com/anachroni/capibara6
cd capibara6
```

### Estructura del Proyecto
```
capibara6/
├── backend/              # Servidor Flask para gestión de conversaciones
├── web/                  # Código frontend del sitio web
├── user_data/            # Directorio para almacenamiento local de datos
├── datasets/             # Datasets especializados
├── README.md            # Documentación general del proyecto
├── DOCS.md              # Documentación completa
├── API.md               # Documentación de la API
├── INSTALLATION.md      # Guía de instalación (este archivo)
└── ARCHITECTURE.md      # Documentación de arquitectura
```

## Instalación del Backend

### 1. Navegar al directorio del backend

```bash
cd backend
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\\Scripts\\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias principales incluyen:
- Flask (framework web)
- Flask-CORS (gestión de CORS)
- python-dotenv (gestión de variables de entorno)
- smtplib (para envío de correos)
- requests (para llamadas HTTP)
- gunicorn (para producción)

### 4. Verificar instalación

```bash
python -c "import flask; print('Flask instalado correctamente')"
```

## Instalación del Frontend

El frontend de capibara6 no requiere instalación de dependencias especiales más allá de un servidor web simple, ya que está construido principalmente con HTML, CSS y JavaScript vanilla.

Puedes servirlo localmente con Python:

```bash
cd web
python -m http.server 8000
```

O con Node.js:

```bash
cd web
npx serve
```

## Configuración del Sistema

### 1. Copiar archivo de ejemplo de configuración

```bash
# Desde el directorio backend
cp .env.example .env
```

### 2. Crear directorio de datos

```bash
mkdir -p user_data
```

Este directorio se usará para almacenar las conversaciones localmente.

### 3. Ajustar permisos de directorio

```bash
chmod -R 755 user_data/
```

## Variables de Entorno

Editar el archivo `.env` en el directorio `backend/`:

```env
# Configuración SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=info@anachroni.co
SMTP_PASSWORD=tu_contraseña_de_aplicacion
FROM_EMAIL=info@anachroni.co

# Configuración del servidor
FLASK_APP=server.py
FLASK_ENV=development
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0

# Opcional: Configuración de logs
LOG_LEVEL=INFO
LOG_FILE=backend.log
```

### Configuración SMTP por Proveedor

#### Gmail
1. Activar 2FA en tu cuenta
2. Ir a https://myaccount.google.com/apppasswords
3. Generar una "Contraseña de aplicación"
4. Usar esa contraseña en `SMTP_PASSWORD`

#### Outlook/Hotmail
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

#### Yahoo
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

#### Otros Proveedores
Consultar la documentación de tu proveedor de correo para los valores correctos de `SMTP_SERVER` y `SMTP_PORT`.

## Configuración del Servidor de Correo

### 1. Obtener credenciales SMTP

Dependiendo de tu proveedor de correo, necesitarás:

- **Servidor SMTP**: Dirección del servidor SMTP (ej. `smtp.gmail.com`)
- **Puerto**: Puerto para conexión (generalmente 587 para TLS)
- **Usuario**: Tu dirección de correo completa
- **Contraseña**: Contraseña de aplicación (no la contraseña principal)

### 2. Probar configuración de correo

Puedes usar el script de prueba incluido:

```bash
cd backend
python send_test.py
```

O usar el script alternativo:

```bash
cd backend
python test_email.py
```

### 3. Configuración de seguridad

Asegúrate de no subir el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

## Ejecución del Sistema

### 1. Iniciar el backend

```bash
cd backend
# Asegúrate de tener el entorno virtual activado
source venv/bin/activate  # o venv\\Scripts\\activate en Windows
python server.py
```

El servidor backend estará disponible en `http://localhost:5000`.

### 2. Iniciar el frontend (en otra terminal)

```bash
cd web
python -m http.server 8000
```

El sitio web frontend estará disponible en `http://localhost:8000`.

### 3. Alternativa: Usar el servidor de desarrollo de Flask para ambos

Puedes configurar Flask para servir también los archivos estáticos del frontend, o usar un proxy inverso para combinar ambos servicios.

## Verificación de la Instalación

### 1. Verificar que el backend está corriendo

```bash
curl http://localhost:5000/api/health
```

Deberías recibir una respuesta como:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-03T12:00:00.000Z"
}
```

### 2. Acceder al frontend

Abre `http://localhost:8000` en tu navegador y verifica que la página principal de capibara6 se carga correctamente.

### 3. Probar la integración

1. Abre el chatbot en la página web
2. Envía algunos mensajes
3. Proporciona una dirección de correo válida
4. Verifica que recibes un correo de confirmación
5. Revisa el archivo `user_data/` para confirmar que se crearon archivos de conversación

### 4. Verificar archivos generados

Después de una conversación exitosa, deberías ver archivos en `backend/user_data/`:

```bash
ls -la backend/user_data/
# Debería mostrar:
# - conversations.json (archivo JSON con todas las conversaciones)
# - Archivos de texto con nombre basado en timestamp (ej. user_YYYYMMDD_HHMMSS.txt)
```

## Solución de Problemas

### Problemas Comunes

#### Error de autenticación SMTP
- Verifica que la contraseña sea correcta
- Asegúrate de usar una "Contraseña de aplicación" en lugar de la contraseña principal de Gmail
- Verifica que el servidor y puerto SMTP sean correctos para tu proveedor

#### Error de conexión
- Verifica que el firewall permita conexiones SMTP (puerto 587 normalmente)
- Algunos ISPs bloquean el puerto 587; prueba con un servidor VPN o contacto a tu proveedor

#### CORS errors
- El servidor ya tiene CORS habilitado
- Verifica que la URL del frontend sea correcta
- Asegúrate de que no haya errores en la consola del navegador

#### Error al iniciar Flask
- Asegúrate de que todas las dependencias estén instaladas
- Verifica que el entorno virtual esté activado
- Revisa el archivo `requirements.txt` y reinstala si es necesario

### Comandos de diagnóstico

```bash
# Verificar versión de Python
python --version

# Verificar dependencias instaladas
pip list

# Verificar variables de entorno
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('SMTP_USER'))"

# Verificar conectividad de red
curl -I http://localhost:5000
```

### Verificación de logs

Los logs del servidor se pueden ver en la terminal donde se ejecutó `python server.py`. Para un registro más permanente, configura el archivo de log en `.env`.

## Mantenimiento y Actualización

### Actualización del código

```bash
git pull origin main
```

Después de actualizar, es recomendable reinstalar dependencias:

```bash
pip install -r requirements.txt
```

### Limpieza de datos

Para limpiar conversaciones antiguas:

```bash
# Eliminar archivos de conversación antiguos (conserva los últimos 30 días)
find backend/user_data/ -name "*.txt" -mtime +30 -delete
```

### Copias de seguridad

Para respaldar las conversaciones:

```bash
# Copiar directorio de datos a un lugar seguro
cp -r backend/user_data/ /ruta/a/respaldo/user_data_$(date +%Y%m%d)
```

### Monitoreo de recursos

```bash
# Verificar uso de memoria
free -h

# Verificar procesos
ps aux | grep python

# Verificar uso de disco
df -h
```