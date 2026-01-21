# FASE D - GUÍA RÁPIDA

## ¿Qué es Fase D?

Interfaz **CLI profesional** para gestionar problemas almacenados en repositorios.

## ¿Qué Hace?

**Operaciones CRUD** + **Búsqueda** + **Export/Import** + **Backup/Restore** + **Verificación**

## Instalación

```bash
# No requiere instalación, usar como-es
python -m cli --help
```

## 9 Comandos Disponibles

### 1. **list** - Listar problemas

```bash
python -m cli list [opciones]
  --type TYPE           Filtrar por tipo (numeracion, karnaugh, etc)
  --difficulty N        Filtrar por dificultad (1-5)
  --tag TAG            Filtrar por etiqueta
  --limit N            Máximo de resultados (default: 20)
  --offset N           Saltar N resultados
  -v, --verbose        Mostrar información detallada
```

**Ejemplo**:

```bash
python -m cli list --type numeracion --difficulty 2 --limit 10
```

### 2. **search** - Buscar

```bash
python -m cli search QUERY [opciones]
  --type TYPE          Limitar a tipo específico
  --limit N            Máximo resultados
```

**Ejemplo**:

```bash
python -m cli search "conversion"
```

### 3. **stats** - Estadísticas

```bash
python -m cli stats [--detailed]
```

Muestra:

- Total de problemas
- Desglose por tipo
- Desglose por dificultad

### 4. **export** - Exportar

```bash
python -m cli export FORMAT ARCHIVO [opciones]
  FORMAT               json o csv
  ARCHIVO             nombre del archivo de salida
  --type TYPE         Exportar solo un tipo
```

**Ejemplo**:

```bash
python -m cli export json problems.json
python -m cli export csv numeracion.csv --type numeracion
```

### 5. **import** - Importar

```bash
python -m cli import ARCHIVO [opciones]
  ARCHIVO                 Archivo JSON a importar
  --skip_duplicates      No importar si ya existen
```

**Ejemplo**:

```bash
python -m cli import problems.json --skip_duplicates
```

### 6. **delete** - Eliminar

```bash
python -m cli delete ID|--type TYPE|--difficulty DIFF [--confirm]
  ID                  ID del problema a eliminar
  --type TYPE         Eliminar todos de un tipo
  --difficulty DIFF   Eliminar todos de una dificultad
  --confirm          No preguntar confirmación
```

**Ejemplo**:

```bash
python -m cli delete prob_123456 --confirm
python -m cli delete --type logic --confirm
```

### 7. **backup** - Crear Backup

```bash
python -m cli backup [--compress]
```

Crea directorio timestampeado en `./backups/`

### 8. **restore** - Restaurar Backup

```bash
python -m cli restore RUTA_BACKUP [--confirm]
```

**Ejemplo**:

```bash
python -m cli restore ./backups/backup_20240115_103000 --confirm
```

### 9. **verify** - Verificar Integridad

```bash
python -m cli verify [--repair]
  --repair           Eliminar problemas corruptos automáticamente
```

---

## Uso desde Python

```python
from cli import ProblemsCLI
from database.file_repo import FileProblemRepository

# Crear CLI con repositorio
repo = FileProblemRepository("./problems")
cli = ProblemsCLI(repo)

# Acceso directo
problems = cli.repo.list()
for p in problems:
    print(f"{p.metadata.title} ({p.type.value})")

# Estadísticas
info = cli.repo.info()
print(f"Total: {info['total']}")
```

---

## Backends Disponibles

### File (JSON)

```python
from database.file_repo import FileProblemRepository
repo = FileProblemRepository("./problems_db")
```

### SQLite

```python
from database.sqlite_repo import SQLiteProblemRepository
repo = SQLiteProblemRepository("./problems.db")
```

---

## Casos de Uso Comunes

### Listar todos los problemas de numeración

```bash
python -m cli list --type numeracion
```

### Buscar problemas sobre "conversión"

```bash
python -m cli search "conversion"
```

### Exportar para análisis

```bash
python -m cli export json analysis.json --type karnaugh
```

### Hacer backup regular

```bash
python -m cli backup
```

### Verificar y reparar

```bash
python -m cli verify --repair
```

### Hacer backup de solo problemas fáciles

```bash
python -m cli export json easy_problems.json --difficulty 1
```

---

## Estructura de Datos

### Problema (Problem)

```python
class Problem:
    id: str                     # UUID único
    type: ProblemType          # Tipo de ejercicio
    metadata: Metadata         # Información común
    statement: Statement       # El problema
    solution: Solution         # La respuesta
```

### Tipos Soportados

- **numeracion**: Conversión de bases, aritmética
- **karnaugh**: Mapas de Karnaugh
- **logic**: Lógica combinacional
- **msi**: Circuitos integrados
- **secuencial**: Circuitos secuenciales

### Dificultad

- 1: Fácil
- 2: Medio-fácil
- 3: Medio
- 4: Medio-difícil
- 5: Difícil

---

## Documentación Completa

Ver **FASE_D_COMPLETADA.md** para:

- Guía detallada de cada comando
- Especificaciones técnicas
- Ejemplos avanzados
- Solución de problemas

---

## Demo Rápida

```bash
python FASE_D_DEMO_SIMPLE.py
```

Ejecuta 3 demostraciones:

1. Repository basado en archivos
2. Repository SQLite
3. Interfaz CLI

**Resultado**: Todos los tests pasan ✅

---

## Requisitos

- Python 3.9+
- SQLite3 (incluido en Python)
- Sin dependencias externas

---

## Instalación Rápida

```bash
# 1. Clonar/Descargar proyecto
cd /path/to/project

# 2. Ejecutar demo
python FASE_D_DEMO_SIMPLE.py

# 3. Usar CLI
python -m cli list

# 4. Crear CLI personalizado
from cli import ProblemsCLI
```

---

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Repository not found` | Ruta incorrecta | Crear directorio primero |
| `Problem invalid` | Estructura incorrecta | Ver ejemplos de Problem |
| `Corrupted file` | JSON inválido | Ejecutar `verify --repair` |
| `Duplicate ID` | ID existe ya | Usar `--skip_duplicates` en import |

---

## Próximas Mejoras

- Interfaz web
- Búsqueda avanzada
- Reportes PDF
- Sincronización

---

**Status**: ✅ Listo para usar
**Versión**: 1.0
**Última actualización**: 15 Enero 2026
