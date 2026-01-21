FROM python:3.9-slim

WORKDIR /app

# Copiar proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir fastapi uvicorn

# Crear directorios
RUN mkdir -p problems_db backups static templates

# Puerto
EXPOSE 8000

# Comando
CMD ["python", "-m", "uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
