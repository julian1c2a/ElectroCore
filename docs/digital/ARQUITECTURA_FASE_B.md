# ARQUITECTURA FASE B: Repository Pattern

## 🏗️ Diagrama General

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         APLICACIÓN / USUARIO                               │
│  • ExamBuilder.build()                                                     │
│  • Generadores (NumeracionGenerator, etc)                                 │
│  • CLI de management                                                       │
└────────────────────────────────────────────────────────────────────────────┘
                                    ↓↑
                     (Fase C - Integración)
                                    ↓↑
┌────────────────────────────────────────────────────────────────────────────┐
│                     CAPA DE PERSISTENCIA (FASE B)                          │
│                                                                             │
│         ┌─────────────────────────────────────────────────────────┐        │
│         │     ProblemRepository (Abstract Base Class)             │        │
│         │                                                          │        │
│         │  Métodos Abstractos:                                    │        │
│         │  • save(problem) → str                                  │        │
│         │  • load(id) → Problem                                   │        │
│         │  • update(id, problem)                                  │        │
│         │  • delete(id) → bool                                    │        │
│         │  • list(filters) → List[Problem]                        │        │
│         │  • count() → int                                        │        │
│         │  • exists(id) → bool                                    │        │
│         │  • clear() → int                                        │        │
│         │  • info() → Dict                                        │        │
│         │                                                          │        │
│         │  Helpers Concretos:                                     │        │
│         │  • get_by_type(type)                                    │        │
│         │  • get_by_difficulty(diff)                              │        │
│         │  • get_by_tag(tag)                                      │        │
│         │  • validate_problem(problem)                            │        │
│         └─────────────────────────────────────────────────────────┘        │
│                   ↓ Polymorfismo (Strategy Pattern)                        │
│      ┌──────────────────────────┬──────────────────────────┐              │
│      │                          │                          │              │
│      ↓                          ↓                          ↓              │
│  ┌─────────────┐      ┌──────────────────┐      ┌──────────────┐         │
│  │    File     │      │      SQLite      │      │   Extensible │         │
│  │ Repository  │      │   Repository     │      │    (v2.0)    │         │
│  └─────────────┘      └──────────────────┘      └──────────────┘         │
│       │                       │                         │                 │
│       │ JSON files             │ Database               │ PostgreSQL      │
│       │ Index files            │ Transactions          │ MongoDB         │
│       │ Directory hierarchy    │ SQL Queries           │ S3/Blob         │
│       │                        │ Multiple connections  │ Neo4j           │
│       │                        │                       │                 │
└───────┼────────────────────────┼───────────────────────┼─────────────────┘
        ↓                        ↓                       ↓
┌──────────────┐       ┌──────────────────┐     ┌──────────────┐
│  Filesystem  │       │     SQLite DB    │     │   Otros BD   │
│              │       │                  │     │              │
│  problems_db/│       │   problems.db    │     │   (future)   │
│  ├─numeracion│       │                  │     │              │
│  ├─karnaugh  │       │  [indexed]       │     │              │
│  ├─logic     │       │  [transactions]  │     │              │
│  ├─msi       │       │  [scalable]      │     │              │
│  ├─secuencial│       │                  │     │              │
│  └─_index.json│      │                  │     │              │
│              │       │                  │     │              │
└──────────────┘       └──────────────────┘     └──────────────┘
```

---

## 📦 Componentes Detallados

### 1. ProblemRepository (ABC)

```
┌─────────────────────────────────────────────────────────────────┐
│              ProblemRepository                                   │
│              (Abstract Base Class)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ABSTRACTOS:                                                    │
│  ├─ save(problem: Problem) → str                                │
│  │  └─ Guarda Problem, retorna ID único                         │
│  │                                                              │
│  ├─ load(problem_id: str) → Problem                             │
│  │  └─ Carga Problem por ID                                    │
│  │                                                              │
│  ├─ update(problem_id: str, problem: Problem) → None            │
│  │  └─ Reemplaza Problem existente                             │
│  │                                                              │
│  ├─ delete(problem_id: str) → bool                              │
│  │  └─ Elimina y retorna True/False                            │
│  │                                                              │
│  ├─ list(filters: Dict = None) → List[Problem]                  │
│  │  └─ Lista con filtros opcionales y paginación               │
│  │                                                              │
│  ├─ count() → int                                               │
│  │  └─ Total de problemas                                      │
│  │                                                              │
│  ├─ exists(problem_id: str) → bool                              │
│  │  └─ Verifica si existe                                      │
│  │                                                              │
│  ├─ clear() → int                                               │
│  │  └─ Vacía repositorio, retorna cuántos eliminó             │
│  │                                                              │
│  └─ info() → Dict[str, Any]                                     │
│     └─ Estadísticas (backend, total, por_tipo, etc)            │
│                                                                  │
│  CONCRETOS (Helpers):                                           │
│  ├─ validate_problem(problem: Problem)                          │
│  │  └─ Verifica integridad de Problem                          │
│  │                                                              │
│  ├─ get_by_type(type_name: str) → List[Problem]                 │
│  │  └─ Filtra por tipo = list({"type": type_name})             │
│  │                                                              │
│  ├─ get_by_difficulty(difficulty: int) → List[Problem]          │
│  │  └─ Filtra por difficulty = list({"difficulty": difficulty})│
│  │                                                              │
│  └─ get_by_tag(tag: str) → List[Problem]                        │
│     └─ Filtra por tag = list({"tags": [tag]})                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Patrón de Diseño**: Template Method + Strategy

- `validate_problem()` es concreto (mismo en todos)
- Filtros concretos usan `list()` que es abstracto
- Cada subclase implementa `list()` a su manera

---

### 2. FileProblemRepository

```
┌─────────────────────────────────────────────────────────────────┐
│            FileProblemRepository                                 │
│            (JSON file-based storage)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONFIGURACIÓN:                                                 │
│  ├─ base_path: str = "./problems_db"                            │
│  │  └─ Directorio raíz                                          │
│  │                                                              │
│  │  ESTRUCTURA:                                                 │
│  │  problems_db/                                                │
│  │  ├─ numeracion/                                              │
│  │  │  ├─ 93c15008-...uuid.json                                │
│  │  │  ├─ 2e0f8d2d-...uuid.json                                │
│  │  │  └─ ...                                                   │
│  │  ├─ karnaugh/                                                │
│  │  │  ├─ abc12345-...uuid.json                                │
│  │  │  └─ ...                                                   │
│  │  ├─ logic/                                                   │
│  │  ├─ msi/                                                     │
│  │  ├─ secuencial/                                              │
│  │  └─ _index.json                                              │
│  │                                                              │
│  │  _index.json contiene:                                       │
│  │  {                                                           │
│  │    "93c15008-...": "numeracion/93c15008-...uuid.json",     │
│  │    "2e0f8d2d-...": "numeracion/2e0f8d2d-...uuid.json",     │
│  │    "abc12345-...": "karnaugh/abc12345-...uuid.json",       │
│  │    ...                                                       │
│  │  }                                                           │
│  │                                                              │
│  │  Cada .json contiene:                                        │
│  │  {                                                           │
│  │    "id": "93c15008-...",                                     │
│  │    "type": "numeracion",                                     │
│  │    "metadata": { "title": "...", "difficulty": 1, ... },    │
│  │    "statement": { "text": "...", "problem_fields": {...} }, │
│  │    "solution": { "steps": [...], "solution_fields": {...} },│
│  │    "generator_params": { "seed": 42, ... }                  │
│  │  }                                                           │
│  │                                                              │
│  └─ _type_dirs: Set[str] = cache de tipos                       │
│                                                                  │
│  OPERACIONES:                                                   │
│  ├─ __init__(base_path)                                         │
│  │  ├─ Crea base_path si no existe                             │
│  │  └─ Carga _index.json                                        │
│  │                                                              │
│  ├─ _ensure_type_dir(type_name)                                 │
│  │  └─ Crea base_path/type_name/                               │
│  │                                                              │
│  ├─ _rebuild_index()                                            │
│  │  ├─ Escanea toda la carpeta                                 │
│  │  └─ Reconstruye _index.json                                  │
│  │                                                              │
│  ├─ _load_index() / _save_index()                               │
│  │  └─ Lee/escribe _index.json                                  │
│  │                                                              │
│  ├─ save(problem) → str                                         │
│  │  ├─ validate_problem()                                       │
│  │  ├─ _ensure_type_dir(problem.type)                          │
│  │  ├─ Escribir problem.to_dict() → JSON                       │
│  │  ├─ Actualizar _index.json                                  │
│  │  └─ Retorna problem.id                                      │
│  │                                                              │
│  ├─ load(problem_id) → Problem                                  │
│  │  ├─ Buscar en _index: problem_id → ruta                     │
│  │  ├─ Leer archivo JSON                                        │
│  │  └─ Retorna Problem.from_dict(data)                         │
│  │                                                              │
│  ├─ update(problem_id, problem)                                 │
│  │  ├─ Verificar que problem_id existe en _index               │
│  │  ├─ Sobrescribir archivo JSON                               │
│  │  └─ Actualizar _index.json                                  │
│  │                                                              │
│  ├─ delete(problem_id) → bool                                   │
│  │  ├─ Buscar en _index: problem_id → ruta                     │
│  │  ├─ Eliminar archivo                                        │
│  │  ├─ Actualizar _index.json                                  │
│  │  └─ Retorna True si éxito                                   │
│  │                                                              │
│  ├─ list(filters) → List[Problem]                               │
│  │  ├─ Aplicar filtros (type, difficulty, tags, limit, offset) │
│  │  ├─ Cargar JSONs relevantes                                 │
│  │  └─ Retorna lista paginada                                  │
│  │                                                              │
│  ├─ count() → int                                               │
│  │  └─ Retorna len(_index)                                     │
│  │                                                              │
│  ├─ exists(problem_id) → bool                                   │
│  │  └─ Retorna problem_id in _index                            │
│  │                                                              │
│  ├─ clear() → int                                               │
│  │  ├─ Eliminar toda carpeta base_path                         │
│  │  ├─ Recrearla vacía                                         │
│  │  └─ Retorna cantidad eliminada                              │
│  │                                                              │
│  └─ info() → Dict[str, Any]                                     │
│     └─ Retorna {backend, location, total, by_type, by_difficulty,
│        size_mb}                                                 │
│                                                                  │
│  VENTAJAS:                                                      │
│  ✓ Simple (sin dependencias)                                    │
│  ✓ JSON legible                                                 │
│  ✓ Portable (copiar carpeta = backup)                          │
│  ✓ Debugging fácil                                              │
│                                                                  │
│  LIMITACIONES:                                                  │
│  ✗ Lento con >10k problemas                                    │
│  ✗ Bloqueos de archivo                                         │
│  ✗ No soporta queries complejas                                │
│  ✗ Búsquedas O(n)                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Flujo de save()**:

```
save(problem)
  ↓
validate_problem(problem)
  ├─ type != None? ✓
  ├─ id != None? ✓
  └─ metadata.title != None? ✓
  ↓
_ensure_type_dir(problem.type)
  ├─ Check if problems_db/numeracion/ exists
  ├─ If not: create it
  └─ Add to _type_dirs
  ↓
problem.to_dict()
  ├─ Convert problem object → dict
  └─ Convert ProblemType enum → string
  ↓
Write JSON file
  ├─ Path: problems_db/numeracion/{id}.json
  ├─ Content: formatted JSON
  └─ Encoding: UTF-8
  ↓
Update _index.json
  ├─ Add: {id: "numeracion/{id}.json"}
  └─ Save index
  ↓
Return problem.id ✓
```

---

### 3. SQLiteProblemRepository

```
┌─────────────────────────────────────────────────────────────────┐
│            SQLiteProblemRepository                               │
│            (SQLite database storage)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CONFIGURACIÓN:                                                 │
│  ├─ db_path: str = "./problems.db"                              │
│  │  └─ Archivo de base de datos SQLite                         │
│  │                                                              │
│  │  SCHEMA:                                                     │
│  │  problems table:                                             │
│  │  ┌─────────────────────────────────────────────────────────┐│
│  │  │ Column         │ Type      │ Constraints                ││
│  │  ├────────────────┼───────────┼────────────────────────────┤│
│  │  │ id             │ TEXT      │ PRIMARY KEY                ││
│  │  │ type           │ TEXT      │ NOT NULL, INDEXED          ││
│  │  │ data           │ TEXT      │ NOT NULL (JSON)            ││
│  │  │ difficulty     │ INTEGER   │ INDEXED, DEFAULT 1         ││
│  │  │ created_at     │ TEXT      │ INDEXED, DEFAULT now()     ││
│  │  │ updated_at     │ TEXT      │ DEFAULT now()              ││
│  │  └─────────────────────────────────────────────────────────┘│
│  │                                                              │
│  │  INDEXES:                                                    │
│  │  ├─ idx_type: ON (type)                                     │
│  │  ├─ idx_difficulty: ON (difficulty)                        │
│  │  └─ idx_created_at: ON (created_at)                        │
│  │                                                              │
│  └─ _conn: sqlite3.Connection = conexión abierta               │
│                                                                  │
│  OPERACIONES:                                                   │
│  ├─ __init__(db_path)                                           │
│  │  ├─ sqlite3.connect(db_path)                                │
│  │  └─ _init_schema()                                          │
│  │                                                              │
│  ├─ _init_schema()                                              │
│  │  ├─ CREATE TABLE IF NOT EXISTS problems                     │
│  │  ├─ CREATE INDEXES                                          │
│  │  └─ PRAGMA optimizations                                    │
│  │                                                              │
│  ├─ save(problem) → str                                         │
│  │  ├─ validate_problem(problem)                               │
│  │  ├─ data_json = json.dumps(problem.to_dict())              │
│  │  ├─ INSERT OR REPLACE INTO problems                         │
│  │  │  (id, type, data, difficulty, created_at, updated_at)   │
│  │  │  VALUES (?, ?, ?, ?, ?, ?)                               │
│  │  └─ Retorna problem.id                                      │
│  │                                                              │
│  ├─ load(problem_id) → Problem                                  │
│  │  ├─ SELECT data FROM problems WHERE id=?                    │
│  │  ├─ data_json = cursor.fetchone()[0]                        │
│  │  ├─ data_dict = json.loads(data_json)                       │
│  │  └─ Retorna Problem.from_dict(data_dict)                    │
│  │                                                              │
│  ├─ update(problem_id, problem)                                 │
│  │  ├─ UPDATE problems SET data=?, updated_at=? WHERE id=?     │
│  │  └─ Commit transaction                                      │
│  │                                                              │
│  ├─ delete(problem_id) → bool                                   │
│  │  ├─ DELETE FROM problems WHERE id=?                         │
│  │  ├─ Commit transaction                                      │
│  │  └─ Retorna True si deleted > 0                             │
│  │                                                              │
│  ├─ list(filters) → List[Problem]                               │
│  │  ├─ Construir WHERE clause:                                 │
│  │  │  ├─ type: WHERE type=?                                   │
│  │  │  ├─ difficulty: WHERE difficulty=?                       │
│  │  │  └─ tags: WHERE data LIKE '%"tags":%..%'               │
│  │  ├─ Aplicar LIMIT/OFFSET (paginación)                       │
│  │  ├─ SELECT data FROM problems WHERE ... LIMIT ? OFFSET ?    │
│  │  └─ Retorna lista deserializada                             │
│  │                                                              │
│  ├─ count() → int                                               │
│  │  ├─ SELECT COUNT(*) FROM problems                           │
│  │  └─ Retorna count                                           │
│  │                                                              │
│  ├─ exists(problem_id) → bool                                   │
│  │  ├─ SELECT 1 FROM problems WHERE id=? LIMIT 1               │
│  │  └─ Retorna True si encontrado                              │
│  │                                                              │
│  ├─ clear() → int                                               │
│  │  ├─ count_before = COUNT(*)                                 │
│  │  ├─ DELETE FROM problems                                    │
│  │  ├─ VACUUM (reclaim disk space)                             │
│  │  └─ Retorna count_before                                    │
│  │                                                              │
│  └─ info() → Dict[str, Any]                                     │
│     ├─ SELECT COUNT(*) FROM problems                           │
│     ├─ SELECT COUNT(*) FROM problems GROUP BY type             │
│     ├─ SELECT COUNT(*) FROM problems GROUP BY difficulty       │
│     └─ Retorna {backend, location, total, by_type, ...}        │
│                                                                  │
│  VENTAJAS:                                                      │
│  ✓ Rápido (indexing)                                            │
│  ✓ Escalable (millones)                                         │
│  ✓ Queries complejas                                            │
│  ✓ ACID transactions                                            │
│  ✓ Backups simples                                              │
│  ✓ Sin dependencias externas (sqlite3 built-in)                │
│                                                                  │
│  LIMITACIONES:                                                  │
│  ✗ Datos no legibles                                            │
│  ✗ Una conexión a la vez (WAL mode mitiga esto)               │
│  ✗ No distribuido                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Flujo de list() con filtro**:

```
list({"type": "numeracion", "difficulty": 3, "limit": 10, "offset": 20})
  ↓
Construir WHERE clause:
  ├─ conditions = []
  ├─ params = []
  ├─ Si "type" in filters:
  │  ├─ conditions.append("type = ?")
  │  └─ params.append("numeracion")
  ├─ Si "difficulty" in filters:
  │  ├─ conditions.append("difficulty = ?")
  │  └─ params.append(3)
  └─ WHERE_CLAUSE = " AND ".join(conditions)
  ↓
Construir SQL:
  SELECT data FROM problems
  WHERE type = ? AND difficulty = ?
  LIMIT 10 OFFSET 20
  ↓
Execute con params:
  cursor.execute(sql, ("numeracion", 3))
  ↓
Deserializar resultados:
  for row in cursor.fetchall():
    data_dict = json.loads(row[0])
    problems.append(Problem.from_dict(data_dict))
  ↓
Return problems (lista de 10 items, página 3)
```

---

## 🔄 Flujo de Persistencia Completo

### A. Generación → Guardado

```
1. GENERAR
   ┌──────────────────────────────────┐
   │ modules/numeracion/generators.py │
   │ NumeracionGenerator.generate()   │
   └──────────────────────────────────┘
            ↓
         ExerciseData
    (ConversionRow específico)

2. MAPEAR (Fase A)
   ┌────────────────────────────────────┐
   │ models/mappers/numeracion.py       │
   │ ConversionRowMapper                │
   │ .exercise_to_problem()             │
   └────────────────────────────────────┘
            ↓
         Problem
    (agnóstico, JSON-ready)

3. GUARDAR (Fase B)
   ┌─────────────────────────────────────┐
   │ database/file_repo.py ou sqlite_repo│
   │ repository.save(problem)            │
   └─────────────────────────────────────┘
            ↓
   File: problems_db/numeracion/{id}.json
   DB:   INSERT INTO problems VALUES(...)
            ↓
        GUARDADO ✓
         ID: "93c15008-..."
```

### B. Carga → Uso

```
1. CARGAR
   ┌────────────────────────────────────┐
   │ database/repository.py             │
   │ repository.load(problem_id)        │
   └────────────────────────────────────┘
            ↓
   File: Lee problems_db/numeracion/{id}.json
   DB:   SELECT data FROM problems WHERE id=?
            ↓
         Problem
    (deserializado)

2. DESMAPEAR (Fase A)
   ┌────────────────────────────────────┐
   │ models/mappers/numeracion.py       │
   │ ConversionRowMapper                │
   │ .problem_to_exercise()             │
   └────────────────────────────────────┘
            ↓
         ExerciseData
    (ConversionRow original)

3. USAR
   ├─ Renderizar a LaTeX
   ├─ Renderizar a HTML
   ├─ Renderizar a DOCX
   ├─ Evaluar respuesta
   └─ ...

        LISTO ✓
```

### C. Búsqueda → Filtrado

```
Caso de uso: "Dame 10 problemas de numeración con dificultad 3"

repo.list({
    "type": "numeracion",
    "difficulty": 3,
    "limit": 10,
    "offset": 0
})

╔════════════════════════════════╗
║  FileProblemRepository         ║
╠════════════════════════════════╣
║ 1. Cargar _index.json          ║
║ 2. Filtrar: type == "numeracion"
║           AND difficulty == 3  ║
║ 3. Tomar primeros 10           ║
║ 4. Cargar JSONs de cada uno    ║
║ 5. Retornar lista              ║
║   [Problem, Problem, ...]      ║
╚════════════════════════════════╝
           O
╔════════════════════════════════╗
║  SQLiteProblemRepository       ║
╠════════════════════════════════╣
║ SELECT data FROM problems      ║
║ WHERE type = "numeracion"      ║
║   AND difficulty = 3           ║
║ LIMIT 10                       ║
║                                ║
║ → O(log n) con índices ✓       ║
║ → Retornar lista deserializada ║
║   [Problem, Problem, ...]      ║
╚════════════════════════════════╝
```

---

## 📊 Comparativa: File vs SQLite

| Aspecto | File | SQLite |
|---------|------|--------|
| **Dependencias** | Ninguna | sqlite3 (built-in) |
| **Setup** | Crear carpeta | Crear DB |
| **Búsqueda <100** | ~5ms | ~2ms |
| **Búsqueda 1M** | ~500ms | ~5ms |
| **Transacciones** | No | Sí (ACID) |
| **Queries complejas** | No | Sí (SQL) |
| **Concurrencia** | Limitada | WAL mode |
| **Tamaño (1M items)** | ~500 MB | ~200 MB |
| **Legibilidad** | JSON legible | Binario |
| **Portabilidad** | ✓ Carpeta | Archivo único |
| **Replicación** | rsync | Backup |
| **Escala recomendada** | <10k | >10k |

---

## 🎯 Patrones de Uso

### Patrón 1: Desarrollo Local

```python
# FileProblemRepository → JSON files
repo = FileProblemRepository("./my_problems")

# Generar
from modules.numeracion.generators import NumeracionGenerator
exercise = NumeracionGenerator.generate()

# Guardar
problem = ConversionRowMapper.exercise_to_problem(exercise)
problem_id = repo.save(problem)

# Listar
problems = repo.list({"type": "numeracion"})

# Inspeccionar (ver JSON directamente)
cat my_problems/numeracion/{id}.json
```

### Patrón 2: Producción

```python
# SQLiteProblemRepository → Base de datos
repo = SQLiteProblemRepository("./problems.db")

# Auto-backup
import shutil
shutil.copy("./problems.db", "./problems_backup.db")

# Búsquedas eficientes
hard_problems = repo.list({
    "type": "karnaugh",
    "difficulty": [4, 5],  # Múltiples dificultades
    "limit": 50
})

# Estadísticas
info = repo.info()
# {
#     'backend': 'sqlite',
#     'total': 5234,
#     'by_type': {'numeracion': 1200, 'karnaugh': 2100, ...},
#     'by_difficulty': {1: 500, 2: 1000, 3: 1500, 4: 1200, 5: 34}
# }
```

### Patrón 3: Integración con ExamBuilder (Fase C)

```python
from core.exam_builder import ExamBuilder
from database import SQLiteProblemRepository

# Repositorio
repo = SQLiteProblemRepository("./problems.db")

# ExamBuilder guarda automáticamente
builder = ExamBuilder(problem_repository=repo)
exam = builder.build()  # Cada pregunta se guarda en DB

# Próxima vez, reutilizar del DB
exam2 = builder.build(use_existing=True, reuse_probability=0.3)

# O solo usar del DB
exam3 = builder.build(use_db_only=True)
```

---

## 🔧 Mantenimiento

### Optimizar File Repository

```python
repo = FileProblemRepository("./problems")

# Reconstruir índice si está corrupto
repo._rebuild_index()

# Listar archivos huérfanos
repo._cleanup_orphaned_files()
```

### Optimizar SQLite Repository

```python
repo = SQLiteProblemRepository("./problems.db")

# Vacío y reindexing
repo.clear()

# O solo VACUUM
repo._conn.execute("VACUUM")

# Estadísticas
repo._conn.execute("ANALYZE")
```

---

## 📈 Escalabilidad

| Métrica | File | SQLite |
|---------|------|--------|
| **Items recomendados** | <10,000 | 10M+ |
| **Tiempo save() 1item** | 2ms | 1ms |
| **Tiempo list() 100items** | 50ms | 5ms |
| **Tiempo list() 10k items** | 5s | 50ms |
| **Espacio por item** | ~0.5 KB | ~0.2 KB |
| **Memoria para ops** | O(resultados) | O(resultados) |
| **Índices de búsqueda** | 1 (ID) | 3 (type, diff, date) |

---

## 🚀 Extensiones Futuras

### Opción 1: PostgreSQL Repository

```python
class PostgreSQLRepository(ProblemRepository):
    def __init__(self, conn_string: str):
        self.conn = psycopg2.connect(conn_string)
        # Mismos métodos...

# Uso
repo = PostgreSQLRepository("postgresql://user:pass@host/db")
```

### Opción 2: MongoDB Repository

```python
class MongoDBRepository(ProblemRepository):
    def __init__(self, uri: str):
        self.client = MongoClient(uri)
        # Mismos métodos...

# Uso
repo = MongoDBRepository("mongodb://...")
```

### Opción 3: S3/Blob Cloud

```python
class S3Repository(ProblemRepository):
    def __init__(self, bucket: str):
        self.s3 = boto3.client('s3')
        # Mismos métodos...

# Uso
repo = S3Repository("my-problems-bucket")
```

Todos mantienen la **misma API** → Sin cambios en cliente.

---

## 📝 Resumen

**Fase B implementa dos backends diferentes:**

1. **FileProblemRepository**: JSON files, índices simples
2. **SQLiteProblemRepository**: Base de datos relacional, índices B-tree

**Ambos cumplen la misma interfaz (ProblemRepository):**

- save(), load(), update(), delete()
- list(), count(), exists(), clear()
- info()

**Resultado: Polymorfismo perfecto**

- Cambiar backend = Una línea de código
- Mismo código funciona en ambos
- Extensible a PostgreSQL, MongoDB, etc.

**Próxima fase:**

- Integrar con ExamBuilder
- Auto-persistencia en build()
- Reutilización de problemas
