# Arquitectura Fase A: Mappers Agnósticos

## Diagrama de Conversión

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EJERCICIO GENERADO                                 │
│                                                                              │
│  ConversionRow                KarnaughExerciseData      LogicProblemData   │
│  ArithmeticOp                 MSIExerciseData          SequentialData       │
│                                                                              │
│  [Objetos Python específicos de cada tipo]                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
                                    │
                    ┌───────────────┼───────────────┐
                    │                               │
                 MAPPER_1                        MAPPER_2                 MAPPER_N
            (ConversionRow)                    (Karnaugh)              (Secuencial)
                    │                               │
                    └───────────────┬───────────────┘
                                    ↓
         ┌─────────────────────────────────────────────────────────┐
         │           PROBLEM (Agnóstico Universal)                 │
         │                                                          │
         │  {                                                       │
         │    "id": "uuid-123",                                    │
         │    "type": "numeracion",                               │
         │    "metadata": {...},                                  │
         │    "statement": {                                       │
         │      "text": "...",                                    │
         │      "problem_fields": {...}                           │
         │    },                                                   │
         │    "solution": {                                        │
         │      "explanation": "...",                             │
         │      "solution_fields": {...}                          │
         │    }                                                    │
         │  }                                                       │
         │                                                          │
         │  [Un formato para TODOS los tipos]                      │
         └─────────────────────────────────────────────────────────┘
                                    ↓
                         problem.to_json_string()
                                    ↓
         ┌─────────────────────────────────────────────────────────┐
         │                    JSON STRING                           │
         │                                                          │
         │  Serializable, persitable, agnóstico                    │
         │  Pronto será guardado en DB (Fase B)                   │
         └─────────────────────────────────────────────────────────┘
                                    ↓
                    Problem.from_json_string(json)
                                    ↓
         ┌─────────────────────────────────────────────────────────┐
         │       Problem (restaurado idénticamente)                │
         └─────────────────────────────────────────────────────────┘
                                    ↓
                    mapper.problem_to_exercise()
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                  ExerciseData (Restaurado Idénticamente)                     │
│                                                                              │
│  ConversionRow (todos los campos intactos)                                 │
│  KarnaughExerciseData (todos los campos intactos)                          │
│  ... etc para otros tipos                                                   │
│                                                                              │
│  ROUND-TRIP VERIFICADO: Original == Restaurado                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Estructura Problem Agnóstico

```
Problem
├── id: UUID
├── type: ProblemType (ENUM)
├── metadata: Metadata
│   ├── title: str
│   ├── topic: str (heredado de ProblemType)
│   ├── difficulty: int (1-5)
│   ├── tags: List[str]
│   ├── created_at: datetime
│   ├── updated_at: datetime
│   ├── version: str
│   ├── author: Optional[str]
│   └── source: Optional[str]
│
├── statement: Statement
│   ├── text: str (descripción del problema)
│   ├── instructions: Optional[str]
│   ├── hints: List[str]
│   └── problem_fields: Dict[str, Any]  <-- AGNÓSTICO POR TIPO
│
├── solution: Solution
│   ├── explanation: Optional[str]
│   ├── steps: List[str]
│   └── solution_fields: Dict[str, Any]  <-- AGNÓSTICO POR TIPO
│
└── generator_params: GeneratorParams
    ├── seed: Optional[int]
    ├── generator_id: Optional[str]
    └── randomizer_config: Dict[str, Any]
```

## Registro de Mappers

```
┌───────────────────────────────────────────────────────────────┐
│                    MAPPERS (Registro)                         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ProblemType.NUMERACION    → ConversionRowMapper()           │
│  ProblemType.KARNAUGH      → KarnaughMapper()                │
│  ProblemType.LOGIC         → LogicProblemMapper()            │
│  ProblemType.MSI           → MSIMapper()                     │
│  ProblemType.SECUENCIAL    → SequentialMapper()              │
│                                                               │
│  Función helper:                                             │
│      mapper = get_mapper(ProblemType.NUMERACION)             │
│      problem = mapper.exercise_to_problem(exercise_data)     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Flujo Temporal

```
TIEMPO 1: GENERACION (actual)
══════════════════════════════════════════════════════════════
Generador
  ↓
ExerciseData (en memoria)
  ↓
Renderers (LaTeX)
  ↗ (EnunciadoRenderer, SolucionRenderer)

PROBLEMA: Después termina y desaparece ❌


TIEMPO 2: CON FASE A (nuevo)
══════════════════════════════════════════════════════════════
Generador
  ↓
ExerciseData (en memoria)
  ↓
Mapper.exercise_to_problem()
  ↓
Problem (agnóstico)
  ↓
Renderers (LaTeX)  ←─────────┐
  ↗ (EnunciadoRenderer)       │
  ↗ (SolucionRenderer)        │
  ↓                           │
Repository.save()            │
  ↓                           │
DATABASE (persistencia) ✅    │
                            │
Carga posterior:             │
Repository.load() ──────────→─→ Problem
  ↓
Mapper.problem_to_exercise()
  ↓
ExerciseData (restaurado)
  ↓
Renderers nuevamente ✅


TIEMPO 3: CON FASE B (próximo)
══════════════════════════════════════════════════════════════
Repository Pattern
  - save(problem)
  - load(id)
  - list(filters)
  - delete(id)
  - update(id, data)

Múltiples backends:
  - FileProblemRepository (JSON en disco)
  - SQLiteProblemRepository (SQLite local)
  - MongoDBProblemRepository (MongoDB nube)

Query:
  problems = repo.list({"type": "numeracion", "difficulty": 3})
```

## Mappers: Template Method Pattern

```
ProblemMapper (Abstract Base)
│
├── exercise_to_problem(exercise, seed)  [TEMPLATE METHOD]
│   ├─ _extract_metadata(exercise)
│   ├─ _extract_statement(exercise)
│   ├─ _extract_solution(exercise)
│   └─ _serialize_exercise(exercise)
│       ↓ (return Problem)
│
├── problem_to_exercise(problem)  [TEMPLATE METHOD]
│   ├─ Validar tipo
│   ├─ Si tiene original_data:
│   │   └─ _deserialize_exercise(data)
│   └─ Si no:
│       └─ _reconstruct_from_problem_fields(problem)
│       ↓ (return ExerciseData)
│
└── [SUBCLASES implementan métodos abstractos]
    ├── ConversionRowMapper
    ├── KarnaughMapper
    ├── LogicProblemMapper
    ├── MSIMapper
    └── SequentialMapper
```

## Problem Fields: Agnósticismo

### Numeración (ConversionRow)

```python
problem_fields = {
    'label': 'a',
    'val_decimal': 157,
    'target_col_idx': 0,
    'representable': True
}

solution_fields = {
    'target_val_str': '10011101',
    'sol_bin': '10011101',
    'sol_c2': '10011101',
    'sol_sm': '10011101',
    'sol_bcd': 'NR'
}
```

### Karnaugh

```python
problem_fields = {
    'vars_name': ['A', 'B', 'C', 'D'],
    'out_name': 'F',
    'truth_table_outputs': [0,1,1,0,...],
    'canon_type': 'Miniterminos',
    'gate_type': 'NAND'
}

solution_fields = {
    'minterms': [1,3,4,6,...],
    'maxterms': [0,2,5,7,...],
    'simplified_sop': 'F = A\'BD + AC\'D + ...',
    'simplified_pos': 'F = (A+B\'+C)(A\'+B+C)...',
    'simplified_nand': '...',
    'simplified_nor': '...'
}
```

### Logic Problem

```python
problem_fields = {
    'context_title': 'Sistema de Riego',
    'variables_desc': ['H: Humedad (1=Seco)', ...],
    'output_desc': 'R: Riego',
    'logic_description': 'Riega SI (Seco Y Deposito lleno)...',
    'vars_clean': ['H', 'L', 'D', 'T'],
    'out_clean': 'R'
}

solution_fields = {
    'truth_table_outputs': [0,1,0,1,...],
    'simplified_solution': 'R = H·D + T·D'
}
```

El patrón se repite para MSI y Secuencial, cada uno con sus fields específicos.

## Ventajas de la Arquitectura Agnóstica

| Aspecto | Beneficio |
|---------|-----------|
| **Un formato para todos** | No hay 5 sistemas de persistencia diferentes |
| **Extensible** | Nuevo tipo = nuevo mapper, resto sin cambios |
| **Tipo-seguro** | ProblemType enum evita errores |
| **Serializable** | JSON limpio, agnóstico, versionable |
| **Bidireccional** | ExerciseData ↔ Problem ↔ JSON ↔ Problem ↔ ExerciseData |
| **Validación** | Mappers validan conversión |
| **Reproducible** | Seeds guardados permiten regenerar |
| **Agnóstico DB** | Mismo Problem cabe en File, SQLite, MongoDB, etc |

## Próxima Fase: Fase B (Repository)

```
Problem (Agnóstico)
    ↓
Repositorio Abstracto
    ├─ save(problem) → problem_id
    ├─ load(problem_id) → problem
    ├─ list(filters) → [problems]
    ├─ delete(problem_id) → bool
    └─ update(problem_id, data) → problem
    ↓
Múltiples Implementaciones
    ├─ FileProblemRepository
    │   └─ problems/
    │       ├─ numeracion/
    │       ├─ karnaugh/
    │       └─ ...
    │
    ├─ SQLiteProblemRepository
    │   └─ problems.db
    │       └─ problems (tabla)
    │           ├─ id
    │           ├─ type
    │           ├─ data (JSON)
    │           └─ metadata
    │
    └─ MongoDBProblemRepository (opcional)
        └─ Colección 'problems'
            └─ Documentos Problem
```

---

**Estado**: Fase A PRODUCTION READY  
**Próximo**: Fase B Repository (3-4 horas)
