# GUÍA DE INSTALACIÓN Y USO

**Versión**: 1.0 | **Fecha**: 15 Enero 2026 | **Status**: ✅ Listo para Producción

---

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Primeros Pasos](#primeros-pasos)
4. [Uso del CLI](#uso-del-cli)
5. [Uso desde Python](#uso-desde-python)
6. [Ejemplos Comunes](#ejemplos-comunes)
7. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

### Sistema Operativo

- Windows 10/11
- macOS 10.14+
- Linux (cualquier distribución)

### Software Requerido

- **Python 3.9 o superior**
- **Git** (opcional, para actualizar)

### Verificar Instalación

```bash
python --version
# Debe mostrar: Python 3.9.x o superior

pip --version
# Debe mostrar: pip 20.x o superior
```

---

## Instalación

### Opción 1: Desde Git (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/julian1c2a/exam_generator.git
cd exam_generator

# Cambiar a rama correcta
git checkout GeneratorFEExercises

# ¡Listo! No requiere dependencias adicionales
```

### Opción 2: Descarga Manual

1. Descargar ZIP del repositorio
2. Extraer en carpeta local
3. Abrir terminal en la carpeta
4. ¡Listo!

### Verificar Instalación

```bash
# Desde la carpeta del proyecto
python -c "from cli import ProblemsCLI; print('[OK] Sistema instalado correctamente')"
```

---

## Primeros Pasos

### 1. Ver la Ayuda

```bash
python -m cli --help
```

### 2. Ejecutar Demo

```bash
python FASE_D_DEMO_SIMPLE.py
```

Esto ejecutará 3 demostraciones completas del sistema.

### 3. Crear Repositorio

```bash
# Crear directorio de problemas
mkdir problems_db

# El repositorio se inicializa automáticamente al primer uso
```

---

## Uso del CLI

### Sintaxis General

```bash
python -m cli COMANDO [OPCIONES]
```

### Comando: list (Listar)

```bash
# Listar todos
python -m cli list

# Listar con filtros
python -m cli list --type numeracion
python -m cli list --difficulty 2
python -m cli list --tag conversion

# Combinar filtros
python -m cli list --type numeracion --difficulty 2 --limit 10

# Modo verbose (detallado)
python -m cli list --verbose
```

### Comando: search (Buscar)

```bash
# Buscar por texto
python -m cli search "conversion"

# Buscar en tipo específico
python -m cli search "binario" --type numeracion

# Limitar resultados
python -m cli search "karnaugh" --limit 5
```

### Comando: stats (Estadísticas)

```bash
# Estadísticas básicas
python -m cli stats

# Estadísticas detalladas
python -m cli stats --detailed
```

### Comando: export (Exportar)

```bash
# Exportar todo a JSON
python -m cli export json all_problems.json

# Exportar a CSV
python -m cli export csv problems.csv

# Exportar solo un tipo
python -m cli export json numeracion.json --type numeracion
```

### Comando: import (Importar)

```bash
# Importar desde JSON
python -m cli import problems.json

# Importar sin duplicados
python -m cli import problems.json --skip_duplicates
```

### Comando: delete (Eliminar)

```bash
# Eliminar un problema
python -m cli delete <problem_id>

# Eliminar sin confirmación
python -m cli delete <problem_id> --confirm

# Eliminar por tipo
python -m cli delete --type logic --confirm

# Eliminar por dificultad
python -m cli delete --difficulty 5 --confirm
```

### Comando: backup (Backup)

```bash
# Crear backup
python -m cli backup

# Crear backup comprimido
python -m cli backup --compress
```

Los backups se guardan en `./backups/backup_YYYYMMDD_HHMMSS/`

### Comando: restore (Restaurar)

```bash
# Restaurar desde backup
python -m cli restore ./backups/backup_20240115_103000

# Restaurar sin confirmación
python -m cli restore ./backups/backup_20240115_103000 --confirm
```

### Comando: verify (Verificar)

```bash
# Verificar integridad
python -m cli verify

# Verificar y reparar automáticamente
python -m cli verify --repair
```

---

## Uso desde Python

### Importar y Usar

```python
from cli import ProblemsCLI
from database.file_repo import FileProblemRepository
from database.sqlite_repo import SQLiteProblemRepository
from models.problem import Problem
from models.problem_type import ProblemType

# Crear repositorio (File)
repo = FileProblemRepository("./problems_db")

# O usar SQLite
repo = SQLiteProblemRepository("./problems.db")

# Crear CLI
cli = ProblemsCLI(repo)
```

### Operaciones CRUD

```python
# Listar problemas
problems = repo.list()

# Filtrar
filtered = repo.list({
    'problem_type': 'numeracion',
    'difficulty': 2,
    'limit': 10
})

# Contar
total = repo.count()

# Verificar existencia
exists = repo.exists(problem_id)

# Cargar problema
problem = repo.load(problem_id)

# Información
info = repo.info()
print(f"Total: {info['total']}")
```

### Crear y Guardar Problema

```python
problem = Problem(
    type=ProblemType.NUMERACION,
    metadata=Problem.Metadata(
        title="Conversión Decimal a Binario",
        topic="Bases Numéricas",
        difficulty=2,
        tags=["conversion", "binario"]
    ),
    statement=Problem.Statement(
        text="Convierte 157 a binario",
        problem_fields={"decimal": 157}
    ),
    solution=Problem.Solution(
        explanation="157 = 10011101",
        solution_fields={"result": "10011101"}
    )
)

problem_id = repo.save(problem)
```

---

## Ejemplos Comunes

### Caso 1: Exportar para Análisis

```bash
# Exportar todos los problemas de Karnaugh
python -m cli export json karnaugh_problems.json --type karnaugh

# Abrir en Excel/Google Sheets
# Convertir JSON a CSV manualmente
python -m cli export csv karnaugh_problems.csv --type karnaugh
```

### Caso 2: Backup Automático

```bash
#!/bin/bash
# crear_backup.sh

cd /path/to/project
python -m cli backup
echo "Backup creado en ./backups/"
```

### Caso 3: Verificar Integridad Diaria

```bash
# Ejecutar cada día
python -m cli verify --repair
```

### Caso 4: Sincronizar Entre Máquinas

```bash
# En máquina 1: exportar
python -m cli export json sync.json

# Transferir sync.json a máquina 2

# En máquina 2: importar
python -m cli import sync.json --skip_duplicates
```

### Caso 5: Estadísticas Semanales

```python
from database.file_repo import FileProblemRepository

repo = FileProblemRepository("./problems_db")
info = repo.info()

print(f"Total de problemas: {info['total']}")
print(f"Por tipo: {info['by_type']}")
print(f"Por dificultad: {info['by_difficulty']}")

# Guardar en archivo
with open("stats_weekly.txt", "w") as f:
    f.write(f"Total: {info['total']}\n")
    for dtype, count in info['by_type'].items():
        f.write(f"  {dtype}: {count}\n")
```

---

## Estructura de Directorios

```
exam_generator/
├── cli/                    # Interfaz CLI
│   ├── __init__.py
│   ├── __main__.py
│   └── problems.py         # ProblemsCLI
│
├── database/               # Repository pattern
│   ├── repository.py       # Abstract base
│   ├── file_repo.py        # JSON backend
│   └── sqlite_repo.py      # SQLite backend
│
├── models/                 # Modelos agnósticos
│   ├── problem.py
│   ├── problem_type.py
│   └── mappers/            # 5 tipos de ejercicio
│
├── core/                   # ExamBuilder
│   ├── exam_builder.py
│   └── generator_base.py
│
├── problems_db/            # Base de datos (se crea automáticamente)
│
├── backups/                # Backups (se crea automáticamente)
│
└── INSTALACION_Y_USO.md    # Este archivo
```

---

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'cli'"

**Causa**: No está en la carpeta correcta

**Solución**:

```bash
# Asegúrate de estar en la raíz del proyecto
cd /path/to/exam_generator
python -m cli list
```

### Problema: "Repository not initialized"

**Causa**: Falta directorio de problemas

**Solución**:

```bash
# Se crea automáticamente al primer uso
# Pero puedes crearlo manualmente
mkdir problems_db
```

### Problema: "Corrupted problem file"

**Causa**: Problema JSON dañado

**Solución**:

```bash
# Reparar automáticamente
python -m cli verify --repair
```

### Problema: "Duplicate ID"

**Causa**: Problema ya existe

**Solución**:

```bash
# Usar --skip_duplicates al importar
python -m cli import file.json --skip_duplicates
```

### Problema: Encoding Unicode en Windows

**Causa**: Codificación de terminal

**Solución**: Usar PowerShell en lugar de CMD

```bash
# En PowerShell
chcp 65001  # UTF-8
python -m cli list
```

---

## Configuración Avanzada

### Usar Repositorio SQLite por Defecto

```bash
# Crear CLI con SQLite
export PROBLEMA_REPO=sqlite
python -m cli list
```

### Especificar Ruta Personalizada

```python
from cli import ProblemsCLI

cli = ProblemsCLI("/custom/path/problems.db", backend="sqlite")
```

### Integración con ExamBuilder

```python
from core.exam_builder import ExamBuilder
from database.file_repo import FileProblemRepository

generators = {...}  # Tus generadores
repo = FileProblemRepository("./problems")

exam = ExamBuilder(generators).build(
    num_problems=50,
    problem_repository=repo,
    use_repository=True,
    reuse_probability=0.3
)
```

---

## Actualizar a Nuevas Versiones

```bash
# Actualizar desde Git
git pull origin GeneratorFEExercises

# Verificar que todo funciona
python FASE_D_DEMO_SIMPLE.py
```

---

## Soporte y Documentación

### Documentación Disponible

- **FASE_D_GUIA_RAPIDA.md** - Referencia rápida
- **FASE_D_COMPLETADA.md** - Guía completa y detallada
- **ESTADO_FINAL_PROYECTO.md** - Arquitectura y diseño
- **README.md** - Overview del proyecto

### Reportar Problemas

Crear issue en GitHub con:

- Versión de Python
- Sistema operativo
- Pasos para reproducir
- Mensaje de error completo

---

## Quick Reference

```bash
# Los 5 comandos más usados:

# 1. Listar
python -m cli list --limit 10

# 2. Buscar
python -m cli search "conversion"

# 3. Exportar
python -m cli export json data.json

# 4. Backup
python -m cli backup

# 5. Restaurar
python -m cli restore ./backups/backup_20240115_103000 --confirm
```

---

**¿Necesitas ayuda?** Consulta la documentación completa o reporta un issue en GitHub.

*Última actualización: 15 Enero 2026*
