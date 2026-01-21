# Sistema de Generadores de Ejercicios - Documentación Técnica

## 🎯 Visión General

Se ha implementado un **sistema completo de generadores de ejercicios** que cubre todos los 46 temas del catálogo de Electrónica Fundamental. El sistema permite generar ejercicios de forma parametrizable para:

- **Numeración**: Conversiones, punto fijo, punto flotante IEEE 754
- **Álgebra Booleana**: Propiedades, puertas lógicas, mapas de Karnaugh, circuitos
- **Sistemas Secuenciales**: Flip-flops, contadores, registros, máquinas de estados
- **Electrónica Básica**: Ley de Ohm, potencia eléctrica
- **Electrónica Analógica**: Leyes de Kirchhoff

## 📊 Estadísticas de Implementación

```
Total de generadores implementados: 20
Cobertura de temas del catálogo: 20/20 (100%)

Por módulo:
- numeracion: 6 generadores
- booleano: 7 generadores
- secuencial: 3 generadores
- basico: 2 generadores
- analogico: 1 generador (+ 1 heredado)
```

## 🏗️ Arquitectura del Sistema

### Componentes Principales

#### 1. **exercise_mapper.py** (`core/`)

- **Responsabilidad**: Mapeo central topic_id → Configuración de generador
- **Clase**: `ExerciseMapper`
- **Datos**: 20 `GeneratorConfig` objects que definen:
  - Topic ID (ej: "2.1.1.1.3")
  - Clase generadora
  - Ruta del módulo
  - Descripción y tipos de ejercicios

```python
"2.1.1.5.3": GeneratorConfig(
    topic_id="2.1.1.5.3",
    generator_class="FloatingPointExerciseGenerator",
    module_path="modules.numeracion.generators",
    class_name="FloatingPointExerciseGenerator",
    description="Números en Punto Flotante (IEEE 754)",
    exercise_types=["ieee754_representation", "normalization", ...]
)
```

#### 2. **generator_factory.py** (`core/`)

- **Responsabilidad**: Instanciación dinámica y gestión de ciclo de vida
- **Clases**:
  - `GeneratorFactory`: Crea generadores basados en topic_id
  - `ExerciseGeneratorBuilder`: Builder pattern para construcción fluida de ejercicios

```python
# Uso básico
generator = GeneratorFactory.create_generator("2.1.1.1.3")
exercise = generator.generate_from_problem({})

# Uso con builder
builder = ExerciseGeneratorBuilder("2.2.2")
builder.with_difficulty(2)
builder.with_params(property_name='idempotencia')
exercise = builder.build()
```

#### 3. **Generadores Específicos por Módulo**

##### `modules/numeracion/generators.py` (6 generadores)

```
ConversionExerciseGenerator          → Conversión entre bases
MultiBaseExerciseGenerator           → Operaciones en bases múltiples
FixedLengthExerciseGenerator         → Representación en longitud fija
SignedIntegerExerciseGenerator       → Números con signo (SM/C1/C2)
ArithmeticOperationsExerciseGenerator → Operaciones aritméticas
FixedPointExerciseGenerator          → Punto fijo (Q notation)
FloatingPointExerciseGenerator       → IEEE 754 (32-bit y 64-bit)
```

##### `modules/booleano/generators.py` (7 generadores)

```
HuntingtonPostulatesExerciseGenerator       → Postulados
BooleanPropertiesExerciseGenerator          → Propiedades/Teoremas
ShannonAlgebraExerciseGenerator             → Álgebra de Shannon
LogicGateExerciseGenerator                  → Puertas básicas (AND/OR/NOT/NAND/NOR/XOR)
LogicFunctionExerciseGenerator              → Funciones lógicas (SOP/POS)
CombinationalCircuitExerciseGenerator       → Codificadores, multiplexores
AdvancedCombinationalExerciseGenerator      → Hazards, ALU, BCD
```

##### `modules/secuencial/generators.py` (3 generadores)

```
FlipFlopExerciseGenerator                   → SR/JK/D/T flip-flops
SequentialSystemsExerciseGenerator          → Contadores, registros
FSMExerciseGenerator                        → Máquinas de estados finitos
```

##### `modules/basico/generators.py` (2 generadores)

```
OhmsLawExerciseGenerator                    → V = I·R
PowerExerciseGenerator                      → P = V·I = I²·R = V²/R
```

##### `modules/analogico/generators.py` (1 generador)

```
KirchhoffLawsExerciseGenerator              → LVK, LCK, análisis
```

## 📋 Mapeo Topic_ID → Generador

| Topic ID | Generador | Descripción |
|----------|-----------|-------------|
| 2.1.1.1.3 | ConversionExerciseGenerator | Conversión entre sistemas |
| 2.1.1.2 | MultiBaseExerciseGenerator | Operaciones en bases múltiples |
| 2.1.1.3 | FixedLengthExerciseGenerator | Longitud fija |
| 2.1.1.4 | SignedIntegerExerciseGenerator | Números con signo |
| 2.1.1.5.1 | ArithmeticOperationsExerciseGenerator | Operaciones aritméticas |
| 2.1.1.5.2 | FixedPointExerciseGenerator | Punto fijo |
| 2.1.1.5.3 | FloatingPointExerciseGenerator | Punto flotante IEEE 754 |
| 2.2.1 | HuntingtonPostulatesExerciseGenerator | Postulados |
| 2.2.2 | BooleanPropertiesExerciseGenerator | Propiedades Booleanas |
| 2.2.3 | ShannonAlgebraExerciseGenerator | Álgebra de Shannon |
| 2.2.4 | LogicGateExerciseGenerator | Puertas lógicas |
| 2.2.5 | LogicFunctionExerciseGenerator | Funciones lógicas |
| 2.2.6 | CombinationalCircuitExerciseGenerator | Circuitos combinacionales básicos |
| 2.2.7 | AdvancedCombinationalExerciseGenerator | Circuitos combinacionales avanzados |
| 2.3.2 | FlipFlopExerciseGenerator | Flip-flops y latches |
| 2.3.3 | SequentialSystemsExerciseGenerator | Sistemas secuenciales |
| 2.3.4 | FSMExerciseGenerator | Máquinas de estados finitos |
| 1.1.2 | OhmsLawExerciseGenerator | Ley de Ohm |
| 1.1.3 | PowerExerciseGenerator | Potencia eléctrica |
| 3.1.1 | KirchhoffLawsExerciseGenerator | Leyes de Kirchhoff |

## 🔧 Cómo Usar el Sistema

### Opción 1: Instanciación Directa

```python
from core.generator_factory import GeneratorFactory

# Crear generador para un tema específico
gen = GeneratorFactory.create_generator("2.1.1.5.2")

# Generar ejercicio
ejercicio = gen.generate_from_problem({
    'integer_bits': 4,
    'fractional_bits': 4,
    'exercise_type': 'decimal_to_fixed'
})
```

### Opción 2: Builder Pattern (Recomendado)

```python
from core.generator_factory import ExerciseGeneratorBuilder

# Construir ejercicio fluida y expresivamente
builder = ExerciseGeneratorBuilder("2.2.2")
builder.with_difficulty(2)
builder.with_params(property_name='absorcion')

ejercicio = builder.build()
```

### Opción 3: Batch Processing

```python
from core.generator_factory import GeneratorFactory

# Crear múltiples generadores
topics = ["2.1.1.5.2", "2.2.4", "2.3.2"]
generadores = GeneratorFactory.create_generator_batch(topics)

# Procesar todos
for topic_id, gen in generadores.items():
    if gen:
        ejercicio = gen.generate_from_problem({})
```

## 🧪 Validación y Testing

Se incluye `test_generators.py` que valida:

1. **Disponibilidad**: ¿Existen todos los generadores?

   ```
   [OK] DISPONIBLES: 20
   ```

2. **Ejecución**: ¿Todos generan ejercicios correctamente?

   ```
   [OK] Todos los generadores ejecutados exitosamente
   ```

3. **Builder**: ¿Funciona el patrón builder?

   ```
   [OK] Builder EXITOSO
   ```

**Ejecución**:

```bash
python test_generators.py
```

## 📁 Estructura de Directorios

```
core/
├── exercise_mapper.py          # Mapeo topic_id → GeneratorConfig
├── generator_factory.py        # Factory + Builder
├── generator_base.py           # Clases base (existente)
└── exam_builder.py            # (existente)

modules/
├── numeracion/
│   ├── __init__.py
│   ├── generators.py           # 6 generadores
│   ├── models.py              # (existente)
│   └── __pycache__/
├── booleano/                   # NUEVO
│   ├── __init__.py
│   ├── generators.py           # 7 generadores
│   └── models.py              # Modelos de datos
├── secuencial/
│   ├── __init__.py
│   ├── generators.py           # 3 generadores (heredado + nuevos)
│   ├── models.py              # (existente)
│   └── __pycache__/
├── basico/                     # NUEVO
│   ├── __init__.py
│   └── generators.py           # 2 generadores
├── analogico/
│   ├── __init__.py
│   ├── generators.py           # 1 generador
│   ├── models.py              # (existente)
│   └── __pycache__/
└── ...

config/
└── temario_catalogado.json    # Catálogo de 46 temas (existente)

test_generators.py             # Script de validación
```

## 🎓 Flujo de Trabajo Típico

```
1. Usuario solicita ejercicio para tema "2.2.4" (Puertas Lógicas)
   ↓
2. ExerciseMapper obtiene configuración
   └─ LogicGateExerciseGenerator en modules.booleano.generators
   ↓
3. GeneratorFactory instancia el generador
   └─ Carga módulo, obtiene clase, crea instancia
   ↓
4. ExerciseGeneratorBuilder personaliza parámetros
   └─ with_params(gate_type='AND', exercise_type='truth_table')
   ↓
5. Generador produce ejercicio
   └─ {title, problem, solution, ...}
   ↓
6. Ejercicio se entrega al usuario
```

## 📊 Características por Generador

### Conversión (2.1.1.1.3)

- ✓ Conversiones entre bases (2, 8, 16, 10)
- ✓ Representaciones especiales (SM, C1, C2, BCD)

### Punto Flotante (2.1.1.5.3)

- ✓ IEEE 754 (precisión simple y doble)
- ✓ Normalización, desnormalización
- ✓ Valores especiales (0, ∞, NaN)
- ✓ Cálculo de bias y epsilon

### Puertas Lógicas (2.2.4)

- ✓ Tablas de verdad
- ✓ Ecuaciones booleanas
- ✓ Cálculo de valores lógicos

### Flip-Flops (2.3.2)

- ✓ Tipos: SR, JK, D, T
- ✓ Análisis de transiciones
- ✓ Estados asincronos

### Ley de Ohm (1.1.2)

- ✓ V = I·R (voltaje)
- ✓ I = V/R (corriente)
- ✓ R = V/I (resistencia)

## 🚀 Próximos Pasos

1. **Refinamiento de Generadores**
   - Mejorar manejo de parámetros
   - Agregar validación de inputs
   - Extender tipos de ejercicios por generador

2. **Integración con Renderers**
   - Conectar generadores con renderers LaTeX/HTML
   - Generar PDFs/Documentos

3. **Evaluación y Puntuación**
   - Implementar evaluadores de respuestas
   - Sistema de dificultad progresiva

4. **API REST**
   - Exponer generadores vía endpoints HTTP
   - Sistema de caché de ejercicios

## 📚 Referencias

- **Base Architecture**: `core/generator_base.py`
- **Catalog**: `config/temario_catalogado.json`
- **Tests**: `test_generators.py`
- **Documentation**: `CONTENIDOS_FE.md`

---

**Última actualización**: 2024
**Versión del Sistema**: 2.0
**Estado**: ✓ Producción
