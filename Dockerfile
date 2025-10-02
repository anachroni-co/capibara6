# Dockerfile para Railway - Backend capibara6
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copiar todo el código del backend
COPY backend/ .

# Comando de inicio
CMD gunicorn server:app --bind 0.0.0.0:$PORT

