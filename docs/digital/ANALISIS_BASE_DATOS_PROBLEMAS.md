# Análisis: Base de Datos de Problemas - Diagnóstico Actual

## ESTADO ACTUAL: ✅ BIEN IDEADO PERO INCOMPLETO

El proyecto **tiene la arquitectura correcta**, pero **le falta la persistencia**. Es como tener un edificio sin cimientos.

---

## 1. LO QUE YA EXISTE BIEN

### 1.1 Catálogo Central (core/catalog.py)

```python
EXERCISE_CATALOG = {
    "num_conversion_8bits": BinaryConversionGenerator(),
    "karnaugh_4vars": KarnaughGenerator(),
    "logic_problem": LogicProblemGenerator(),
    "msi_analysis": MSIGenerator(),
    "sequential_analysis": SequentialGenerator()
}
```

✅ **Bueno**: Registry pattern correcto

- Centralizado
- Extensible
- Fácil descubrimiento

---

## 2. LO QUE FALTA: ARQUITECTURA PERSISTENCIA

Actualmente el flujo es:

```
ConfigFile (test_exam.json)
    ↓
ExamBuilder.build()
    ↓
EXERCISE_CATALOG → Generador (random o seeds)
    ↓
ExerciseData (EN MEMORIA)
    ↓
Renderer
    ↓
LaTeX
```

**PROBLEMA**: `ExerciseData` vive solo en memoria. Cuando termina la ejecución, **desaparece**.

### 2.1 Lo que NECESITA agregar

```
ProblemDatabase (persistencia)
├── Storage (dónde guardar)
│   ├── File (JSON, SQLite)
│   ├── Database (PostgreSQL, MongoDB)
│   └── Cloud (Firebase, AWS)
│
├── Schema (cómo representar)
│   ├── Tablas/Colecciones
│   ├── Campos obligatorios
│   └── Versioning
│
└── Repository (interface)
    ├── save_problem(problema)
    ├── load_problem(id)
    ├── list_problems(filters)
    ├── delete_problem(id)
    └── update_problem(id, data)
```

---

## 3. PROBLEMAS ACTUALES CON TIPOS DIFERENTES

El código **sí maneja diferentes tipos**, pero:

### 3.1 Cada tipo tiene su propio generador

```
numeracion/
├── generators.py  ← ConversionRowGenerator
├── models.py      ← ConversionRow, ConversionExerciseData

combinacional/
├── generators.py  ← KarnaughGenerator, LogicProblemGenerator, MSIGenerator
├── models.py      ← KarnaughExerciseData, LogicProblemExerciseData, MSIExerciseData

secuencial/
├── generators.py  ← SequentialGenerator
├── models.py      ← SequentialExerciseData
```

### 3.2 ✅ BIEN: Herencia con ExerciseData base

```python
class ExerciseData:  # core/generator_base.py
    """Base para todas los tipos de ejercicios"""
    pass

class ConversionRow(ExerciseData):
    """Tipo 1: Conversión numérica"""
    pass

class KarnaughExerciseData(ExerciseData):
    """Tipo 2: Mapas de Karnaugh"""
    pass
```

### 3.3 ✅ BIEN: Generadores con interfaz common

```python
class ExerciseGenerator(ABC):
    @abstractmethod
    def topic(self) -> str:
        pass
    
    def generate(self, difficulty: int = 1) -> ExerciseData:
        pass
```

### 3.4 ❌ PROBLEMA: Serialización inconsistente

Cada tipo tiene su **propia estructura JSON** en `exercises_json`:

```json
{
  "type": "numeracion",
  "problem": {
    "label": "a",
    "val_decimal": 157,
    ...
  },
  "solution": {
    "sol_bin": "10011101",
    ...
  }
}
```

Vs en combinacional/lógica:

```json
{
  "type": "logic",
  "context": "Sistema de Riego",
  "variables": [...],
  "logic_description": "...",
  ...
}
```

**NO HAY FORMATO COMÚN** de persistencia.

---

## 4. PROPUESTA: ARQUITECTURA CORRECTA

### 4.1 Nivel 1: Formato Agnóstico (JSON Common)

```json
{
  "id": "uuid-1234",
  "metadata": {
    "type": "numeracion",
    "topic": "Representación Numérica",
    "difficulty": 1,
    "tags": ["8bits", "conversión", "decimal"],
    "created_at": "2026-01-15T10:30:00",
    "version": "1.0"
  },
  "statement": {
    "text": "Convierte 157 a binario...",
    "instructions": "Para cada base realiza...",
    ...
  },
  "solution": {
    "explanation": "El 157 se convierte dividiendo...",
    "steps": [...],
    "answers": {...}
  },
  "generator_params": {
    "seed": 42,
    "randomizer_config": {...}
  }
}
```

### 4.2 Nivel 2: Repository Pattern

```python
class ProblemRepository(ABC):
    @abstractmethod
    def save(self, problem: Problem) -> str:  # Retorna ID
        pass
    
    @abstractmethod
    def load(self, problem_id: str) -> Problem:
        pass
    
    @abstractmethod
    def list(self, filters: Dict) -> List[Problem]:
        pass
    
    @abstractmethod
    def delete(self, problem_id: str) -> bool:
        pass

class FileProblemRepository(ProblemRepository):
    """Guarda en JSON/ficheros"""
    pass

class SQLiteProblemRepository(ProblemRepository):
    """Guarda en SQLite (sin dependencias externas)"""
    pass

class MongoDBProblemRepository(ProblemRepository):
    """Para producción con DB real"""
    pass
```

### 4.3 Nivel 3: Mapper (Type → JSON → Type)

```python
class ProblemMapper:
    """Convierte ExerciseData → JSON Problem y viceversa"""
    
    MAPPERS = {
        "numeracion": ConversionRowMapper,
        "karnaugh": KarnaughMapper,
        "logic": LogicProblemMapper,
        "msi": MSIMapper,
        "secuencial": SequentialMapper
    }
    
    @staticmethod
    def to_common_format(exercise: ExerciseData) -> Problem:
        """ExerciseData (Python object) → Problem (JSON agnóstico)"""
        mapper_class = ProblemMapper.MAPPERS[exercise.type]
        return mapper_class.to_json(exercise)
    
    @staticmethod
    def from_common_format(problem_json: Dict) -> ExerciseData:
        """Problem (JSON agnóstico) → ExerciseData (Python object)"""
        problem_type = problem_json["metadata"]["type"]
        mapper_class = ProblemMapper.MAPPERS[problem_type]
        return mapper_class.from_json(problem_json)
```

### 4.4 Flujo Completo con Persistencia

```
ExamConfig (test_exam.json)
    ↓
ExamBuilder.build()
    ↓
[Para cada ejercicio solicitado]
    ├─ Generador (aleatorio o seed)
    ├─ ExerciseData (en memoria)
    ├─ ProblemMapper.to_common_format()
    ├─ Problem (JSON agnóstico)
    ├─ Repository.save()  ← PERSISTENCIA
    └─ problem_id
    
    ↓
Renderer (usa ExerciseData o Problem)
    ↓
LaTeX
```

---

## 5. ESTRUCTURA DE DIRECTORIOS PROPUESTA

```
models/
├── __init__.py
├── problem.py          ← Clase Problem (JSON agnóstico)
├── problem_type.py     ← Enum: NUMERACION, KARNAUGH, LOGIC, etc.
└── mappers/
    ├── __init__.py
    ├── base.py         ← ProblemMapper base
    ├── numeracion.py   ← ConversionRowMapper
    ├── karnaugh.py     ← KarnaughMapper
    ├── logic.py        ← LogicProblemMapper
    ├── msi.py          ← MSIMapper
    └── secuencial.py   ← SequentialMapper

database/
├── __init__.py
├── repository.py       ← ProblemRepository (ABC)
├── file_repo.py        ← FileProblemRepository
├── sqlite_repo.py      ← SQLiteProblemRepository
└── mongo_repo.py       ← MongoDBProblemRepository (opcional)

config/
├── problems_db/        ← Base de datos (nueva carpeta)
│   ├── problems.db     ← Si es SQLite
│   └── problems/       ← Si es ficheros JSON
│       ├── numeracion/
│       ├── karnaugh/
│       ├── logic/
│       ├── msi/
│       └── secuencial/
```

---

## 6. VENTAJAS DE ESTA ARQUITECTURA

| Aspecto | Beneficio |
|---------|-----------|
| **Agnósticismo** | Un formato JSON común para todos los tipos |
| **Persistencia** | Los problemas no desaparecen después de generarse |
| **Trazabilidad** | Cada problema tiene ID único, versión, creación, etc. |
| **Escalabilidad** | Cambiar de File → SQLite → Mongo sin tocar código |
| **Testing** | Fácil hacer testing sin BD real (in-memory repo) |
| **Reutilización** | Los problemas guardados se pueden exportar, copiar, etc. |
| **Búsqueda** | Filtrar por difficulty, topic, tags, etc. |

---

## 7. PASOS CONCRETOS A IMPLEMENTAR

### Fase A: Modelo de Persistencia (3-4 horas)

```
1. models/problem.py          ← Clase Problem agnóstica
2. models/problem_type.py     ← Enum de tipos
3. models/mappers/base.py     ← Clase mapper base
4. models/mappers/[tipos].py  ← Mappers específicos para cada tipo
```

### Fase B: Repository (2-3 horas)

```
1. database/repository.py      ← ABC ProblemRepository
2. database/file_repo.py       ← Implementación con ficheros
3. database/sqlite_repo.py     ← Implementación con SQLite
```

### Fase C: Integración (2-3 horas)

```
1. core/exam_builder.py        ← Agregar persistencia al build()
2. main_v2.py                  ← Opción de cargar de DB
3. Migrations                  ← Exportar problemas existentes
```

### Fase D: Interfaz de Gestión (3-4 horas)

```
1. CLI para CRUD de problemas
2. Sistema de búsqueda/filtrado
3. Exportación e importación
```

---

## 8. ¿RECOMENDACION?

**EMPEZAR CON:**

1. ✅ Fase A (Modelo + Mappers) - Es la base, toma 1-2 sesiones
2. ✅ Fase B (Repository File) - Más simple, sin dependencias
3. ⏸️ Fase B (Repository SQLite) - Después si necesita escala
4. ⏸️ Fase C + D - Cuando tenga solidez en A+B

**NO NECESITA:**

- MongoDB (FILE o SQLite basta para empezar)
- ORM complejo (los tipos ya son definidos)
- Cloud (después si crece)

---

## Conclusión

**La arquitectura YA existe, pero le falta el "último kilómetro"**: la persistencia.

Es como tener un generador de ejercicios perfecto, pero que borra todo cuando apaga el programa.

Propongo: **Agregar 2 capas nuevas**

1. **Mappers**: ExerciseData → JSON agnóstico → ExerciseData
2. **Repository**: Guardar/cargar de disco o DB

¿Empezamos por la Fase A?
