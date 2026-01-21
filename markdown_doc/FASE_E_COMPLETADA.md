# FASE E: INTERFAZ WEB - DOCUMENTACIÓN COMPLETA

**Status**: ✅ COMPLETADA | **Fecha**: 15 Enero 2026 | **Versión**: 1.0

---

## 📋 Tabla de Contenidos

1. [Overview](#overview)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Endpoints API](#endpoints-api)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Overview

**Fase E** proporciona una interfaz web moderna para gestionar problemas de examen.

### Características

✅ **Dashboard Interactivo**
- Listar, buscar, filtrar problemas
- Estadísticas en tiempo real
- Visualización gráfica por tipo y dificultad

✅ **API REST Completa**
- 15+ endpoints
- Operaciones CRUD completas
- Exportar/importar JSON/CSV
- Búsqueda avanzada

✅ **Integración Total**
- Conecta con Repository (File o SQLite)
- Compatible con CLI y ExamBuilder
- Datos persistentes

✅ **Deployment**
- Docker Compose incluido
- Sin dependencias adicionales
- Pronto a producción

---

## Requisitos

### Sistema
- Python 3.9+
- Docker + Docker Compose (opcional)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### Software
```bash
fastapi>=0.95.0
uvicorn[standard]>=0.21.0
```

---

## Instalación

### Opción 1: Sin Docker (Recomendado para desarrollo)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servidor
python -m uvicorn web.app:app --reload

# 3. Abrir en navegador
# http://localhost:8000
```

### Opción 2: Con Docker (Recomendado para producción)

```bash
# 1. Construir imagen
docker build -t exam-generator .

# 2. Iniciar contenedor
docker run -p 8000:8000 \
  -v $(pwd)/problems_db:/app/problems_db \
  -v $(pwd)/backups:/app/backups \
  exam-generator
```

### Opción 3: Docker Compose (Más fácil)

```bash
# Iniciar todo
docker-compose up -d

# Logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## Uso

### Dashboard Web

**URL**: `http://localhost:8000`

#### Pestaña 1: Listar Problemas

- Muestra todos los problemas
- Tarjetas interactivas con:
  - Título
  - Tipo (badge)
  - Dificultad
  - Tema
  - Botones: Ver, Borrar

#### Pestaña 2: Buscar

- Búsqueda por texto libre
- Busca en título, tema y tags
- Resultados en tiempo real
- Máximo 20 resultados

#### Pestaña 3: Estadísticas

- Total de problemas
- Desglose por tipo
- Desglose por dificultad
- Tabla comparativa

#### Pestaña 4: Exportar

- **JSON**: Todos los problemas en JSON
- **CSV**: Tabla para Excel/Sheets

#### Pestaña 5: Importar

- Seleccionar archivo JSON
- Opción: Saltar duplicados
- Confirmación de importación

---

## Endpoints API

### Problemas

#### GET `/api/problems`

Listar problemas con filtros.

**Query Parameters**:
```
?problem_type=numeracion
?difficulty=2
?limit=50
?offset=0
```

**Ejemplo**:
```bash
curl http://localhost:8000/api/problems?limit=10
```

**Respuesta**:
```json
{
  "success": true,
  "count": 10,
  "problems": [
    {
      "id": "prob_001",
      "type": "numeracion",
      "metadata": {
        "title": "Conversión",
        "difficulty": 2,
        "topic": "Bases",
        "tags": ["conversion", "binario"]
      },
      "statement": {...},
      "solution": {...}
    }
  ]
}
```

#### GET `/api/problems/{problem_id}`

Obtener problema específico.

```bash
curl http://localhost:8000/api/problems/prob_001
```

#### POST `/api/problems`

Crear nuevo problema.

**Body**:
```json
{
  "type": "numeracion",
  "metadata": {
    "title": "Nuevo Problema",
    "difficulty": 3,
    "topic": "Conversión",
    "tags": ["conversion"]
  },
  "statement": {
    "text": "Convierte...",
    "problem_fields": {}
  },
  "solution": {
    "explanation": "La respuesta es...",
    "solution_fields": {}
  }
}
```

#### PUT `/api/problems/{problem_id}`

Actualizar problema.

```bash
curl -X PUT http://localhost:8000/api/problems/prob_001 \
  -H "Content-Type: application/json" \
  -d '{"type": "numeracion", ...}'
```

#### DELETE `/api/problems/{problem_id}`

Eliminar problema.

```bash
curl -X DELETE "http://localhost:8000/api/problems/prob_001?confirm=true"
```

### Búsqueda

#### GET `/api/search`

Buscar problemas.

**Query Parameters**:
```
?q=conversion
?limit=20
```

**Ejemplo**:
```bash
curl "http://localhost:8000/api/search?q=binario&limit=5"
```

### Estadísticas

#### GET `/api/stats`

Obtener estadísticas.

```bash
curl http://localhost:8000/api/stats
```

**Respuesta**:
```json
{
  "success": true,
  "stats": {
    "total": 150,
    "by_type": {
      "numeracion": 50,
      "karnaugh": 40,
      "logic": 30,
      "msi": 20,
      "secuencial": 10
    },
    "by_difficulty": {
      "1": 25,
      "2": 50,
      "3": 40,
      "4": 20,
      "5": 15
    }
  }
}
```

### Exportación

#### GET `/api/export/json`

Exportar a JSON.

```bash
curl http://localhost:8000/api/export/json > problems.json
```

#### GET `/api/export/csv`

Exportar a CSV.

```bash
curl http://localhost:8000/api/export/csv > problems.csv
```

### Importación

#### POST `/api/import`

Importar archivo JSON.

```bash
curl -X POST -F "file=@problems.json" \
  http://localhost:8000/api/import
```

**Parámetros**:
```
?skip_duplicates=true
```

### Configuración

#### POST `/api/config/repo`

Cambiar repositorio.

```bash
curl -X POST http://localhost:8000/api/config/repo \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/path/to/repo", "backend": "file"}'
```

### Health Check

#### GET `/api/health`

Verificar estado del servidor.

```bash
curl http://localhost:8000/api/health
```

**Respuesta**:
```json
{
  "status": "healthy",
  "backend": "FileProblemRepository",
  "problems_count": 150
}
```

---

## Deployment

### Producción con Docker

#### 1. Configurar Nginx (proxy reverso)

```nginx
server {
    listen 80;
    server_name exam-generator.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 2. Iniciar con Docker Compose

```bash
docker-compose up -d
```

#### 3. Configurar SSL (Certbot)

```bash
certbot certonly --standalone -d exam-generator.com
```

#### 4. Docker Compose mejorado

```yaml
version: '3.8'
services:
  web:
    image: exam-generator:latest
    ports:
      - "8000:8000"
    volumes:
      - ./problems_db:/app/problems_db
      - ./backups:/app/backups
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=info
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Heroku

```bash
# 1. Crear Procfile
echo "web: python -m uvicorn web.app:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Desplegar
git push heroku main
```

### AWS Lambda (con Mangum)

```bash
pip install mangum
```

```python
# web/handler.py
from mangum import Mangum
from web.app import app

handler = Mangum(app)
```

---

## Ejemplos de Uso

### Ejemplo 1: Listar y exportar problemas de Numeración

```python
import requests

# Listar
response = requests.get("http://localhost:8000/api/problems?problem_type=numeracion")
problems = response.json()["problems"]

# Exportar JSON
response = requests.get("http://localhost:8000/api/export/json")
with open("numeracion.json", "wb") as f:
    f.write(response.content)
```

### Ejemplo 2: Buscar y crear problema

```bash
# Buscar
curl "http://localhost:8000/api/search?q=karnaugh" | jq

# Crear nuevo
curl -X POST http://localhost:8000/api/problems \
  -H "Content-Type: application/json" \
  -d '{
    "type": "karnaugh",
    "metadata": {
      "title": "Simplificación K-Map",
      "difficulty": 3,
      "topic": "Álgebra Digital",
      "tags": ["karnaugh", "simplificacion"]
    },
    "statement": {
      "text": "Simplifica la función usando Karnaugh",
      "problem_fields": {}
    },
    "solution": {
      "explanation": "La función simplificada es...",
      "solution_fields": {}
    }
  }'
```

### Ejemplo 3: Backup automático diario

```bash
#!/bin/bash
# backup_diario.sh

cd /path/to/exam_generator

# Exportar
curl http://localhost:8000/api/export/json > \
  backups/daily_$(date +%Y%m%d).json

# Comprimir
gzip backups/daily_*.json

# Enviar a cloud (opcional)
aws s3 cp backups/ s3://my-bucket/backups/ --recursive
```

---

## Troubleshooting

### Problema: Puerto 8000 en uso

**Solución**:
```bash
# Usar otro puerto
python -m uvicorn web.app:app --port 8001

# O liberar puerto
lsof -i :8000
kill -9 <PID>
```

### Problema: Error de permisos en Docker

**Solución**:
```bash
# Dar permisos
sudo chmod 755 problems_db
docker-compose down
docker-compose up -d
```

### Problema: Repositorio no inicializa

**Solución**:
```bash
# Crear directorio
mkdir -p problems_db

# Inicializar desde CLI
python -m cli list
```

### Problema: Búsqueda lenta

**Solución**: Usar SQLite en lugar de File
```bash
curl -X POST http://localhost:8000/api/config/repo \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "problems.db", "backend": "sqlite"}'
```

### Problema: CORS en cliente JavaScript externo

**Solución**: Añadir CORSMiddleware a `web/app.py`
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Próximas Mejoras (Fase F+)

- [ ] Autenticación y autorización
- [ ] Rate limiting
- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Integración con ExamBuilder en interfaz web
- [ ] Análisis avanzado y reportes
- [ ] API GraphQL
- [ ] Mobile app
- [ ] Generación de PDFs

---

## Resumen de Arquitectura

```
┌─────────────────────────────────────────────┐
│         NAVEGADOR WEB                       │
│  (HTML + CSS + JavaScript)                  │
└────────────────┬────────────────────────────┘
                 │ HTTP/REST
                 ↓
┌─────────────────────────────────────────────┐
│         FASTAPI (web/app.py)                │
│  - 15+ Endpoints                            │
│  - Validación                               │
│  - Serialización JSON                       │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│    REPOSITORY PATTERN                       │
│  ┌──────────────────────────────────────┐  │
│  │  FileProblemRepository (JSON)        │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │  SQLiteProblemRepository             │  │
│  └──────────────────────────────────────┘  │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│      ALMACENAMIENTO PERSISTENTE             │
│  - ./problems_db/ (JSON)                    │
│  - problems.db (SQLite)                     │
└─────────────────────────────────────────────┘
```

---

## Archivos de Fase E

```
web/
├── __init__.py          # Inicialización
├── app.py              # FastAPI app (500+ líneas)
└── static/
    ├── app.js          # Frontend JavaScript (400+ líneas)
    └── style.css       # Estilos CSS (400+ líneas)
templates/              # Plantillas HTML (futuro)

docker-compose.yml      # Orchestración Docker
Dockerfile             # Imagen Docker

requirements.txt       # Dependencias actualizadas
```

---

## Estadísticas

- **Código Backend**: 500+ líneas (FastAPI)
- **Código Frontend**: 400+ líneas (JavaScript)
- **Estilos**: 400+ líneas (CSS)
- **Endpoints**: 15+
- **Funcionalidades**: 10
- **Dependencias**: 2 (fastapi, uvicorn)

---

## Conclusión

**Fase E** completa el stack de Exam Generator con una interfaz web moderna, API REST completa y deployment ready.

La arquitectura es escalable, mantenible y lista para producción.

**Estado**: ✅ COMPLETADA Y PROBADA

*Para más información, consultar INSTALACION_Y_USO.md*

---

**Fecha de Creación**: 15 Enero 2026
**Última Actualización**: 15 Enero 2026
**Versión**: 1.0
