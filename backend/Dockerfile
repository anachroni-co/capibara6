# Dockerfile para Railway
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio de datos
RUN mkdir -p user_data

# Exponer puerto (Railway usa $PORT)
EXPOSE $PORT

# Comando de inicio
CMD gunicorn server:app --bind 0.0.0.0:$PORT

