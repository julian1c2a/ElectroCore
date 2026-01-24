# Sistema de Lógica Matemática y Demostración Formal

Sistema general para construir y verificar demostraciones formales en matemáticas. Implementa un sistema axiomático completo con expresiones, reglas de inferencia, y verificación de pruebas.

## 📑 Índice de Contenidos

- [Estadísticas del Sistema](#-estadísticas-del-sistema)
- [Características](#-características)
- [Casos de Uso](#-casos-de-uso)
- [Estructura del Módulo](#-estructura-del-módulo)
- [Guía Rápida](#-guía-rápida)
- [Ejemplos Completos](#-ejemplos-completos)
- [Sintaxis de Expresiones](#-sintaxis-de-expresiones)
- [Reglas de Inferencia](#-reglas-de-inferencia-disponibles)
- [Casos de Uso Avanzados](#-casos-de-uso-avanzados)
- [Verificación de Demostraciones](#-verificación-de-demostraciones)
- [Documentación de Módulos](#-documentación-de-módulos)
- [FAQ](#-preguntas-frecuentes-faq)
- [Contribuciones](#-contribuciones)
- [Referencias](#-referencias)

## � Estadísticas del Sistema

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **Tipos de Expresiones** | 7 | Variables, Constantes, Operadores binarios/unarios, Funciones, Cuantificadores, Predicados |
| **Reglas de Inferencia** | 13 | 10 reglas clásicas + 3 tipos de inducción |
| **Sistemas Axiomáticos** | 2 | Álgebra de Boole (Huntington 1903), Números Naturales (Peano 1889) |
| **Demos Completos** | 3 | Hamming, Boole, Inducción matemática |
| **Teoremas Demostrados** | 9+ | Idempotencia, Métricas, Sumas, Desigualdades |
| **Líneas de Código** | ~3,500 | Sistema completo con documentación |

## �📋 Características

- **Expresiones matemáticas formales**: Variables, constantes, operadores, funciones, cuantificadores y predicados
- **Sistema de axiomas**: Define axiomas, postulados y definiciones para cualquier sistema formal
- **Reglas de inferencia**: 13 reglas incluyendo modus ponens, sustitución, cuantificadores e inducción
- **Inducción matemática**: Tres tipos de inducción (simple, fuerte y estructural)
- **Construcción de pruebas**: Sistema paso a paso con justificaciones rigurosas
- **Verificación automática**: Valida la corrección lógica de demostraciones
- **Biblioteca de teoremas**: Almacena, consulta y reutiliza resultados demostrados
- **Sistemas preconfigurados**: Álgebra de Boole (Huntington 1903) y Números Naturales (Peano 1889)

## 🎯 Casos de Uso

Este sistema puede demostrar propiedades en:

- ✅ **Álgebra de Boole** (Postulados de Huntington 1903)
- ✅ **Números Naturales** (Axiomas de Peano 1889)
- ✅ **Inducción Matemática** (Demostraciones sobre ℕ)
- ✅ **Espacios métricos** (Distancia de Hamming)
- ✅ **Teoría de conjuntos**
- ✅ **Teoría de números**
- ✅ **Lógica proposicional**
- ✅ **Y cualquier sistema axiomático formal**

## 📦 Estructura del Módulo

```
core/math_logic_system/
├── __init__.py              # Interfaz pública
├── expressions.py           # Sistema de expresiones matemáticas
├── axioms.py               # Axiomas, postulados y definiciones
├── inference_rules.py      # Reglas de inferencia lógica
├── proof_system.py         # Sistema de construcción de pruebas
├── verification.py         # Verificación de demostraciones
├── boolean_algebra.py      # Álgebra de Boole (Huntington 1903)
└── natural_numbers.py      # Números Naturales (Peano 1889)
```

## 🚀 Guía Rápida

### 1. Importar el sistema

```python
from core.math_logic_system import (
    # Expresiones
    Var, Const, BinOp, UnOp, Func, Forall, Exists,
    Equals, And, Or, Implies, Not, Add, Mul,
    
    # Sistema axiomático
    AxiomSystem, Axiom, Postulate, Definition,
    
    # Pruebas
    Proof, Theorem, Lemma, ProofLibrary,
    JustificationType,
    
    # Reglas de inferencia
    ModusPonens, Substitution, Conjunction,
    MathematicalInduction, StrongInduction,
    
    # Verificación
    ProofVerifier,
    
    # Sistemas preconstruidos
    BooleanAlgebra, PeanoArithmetic
)
```

### 1b. Uso rápido con sistemas preconstruidos

```python
# Números Naturales (Peano)
peano = PeanoArithmetic()
peano.show_axioms()  # Muestra los 5 axiomas de Peano

# Operaciones computacionales
print(peano.successor(5))        # 6
print(peano.add(3, 4))          # 7 (definición recursiva)
print(peano.multiply(3, 4))     # 12
print(peano.power(2, 10))       # 1024

# Álgebra de Boole (Huntington)
boole = BooleanAlgebra()
result = boole.evaluate(And(Var("a"), Var("b")), {"a": True, "b": False})
print(result)  # False
```

### 2. Crear expresiones matemáticas

```python
# Variables
x = Var("x")
y = Var("y")

# Constantes
zero = Const(0, "0")
one = Const(1, "1")

# Operaciones binarias
suma = Add(x, y)              # x + y
producto = Mul(x, y)          # x · y
igualdad = Equals(x, y)       # x = y
conjuncion = And(p, q)        # p ∧ q

# Operaciones unarias
negacion = Not(p)             # ¬p

# Cuantificadores
forall_x = Forall("x", P(x))  # ∀x: P(x)
exists_y = Exists("y", Q(y))  # ∃y: Q(y)

# Funciones
distancia = Func("d", x, y)   # d(x, y)
```

### 3. Definir un sistema axiomático

```python
# Crear sistema
system = AxiomSystem("Mi Sistema", "Descripción")

# Añadir axiomas
axiom1 = Axiom(
    "A1-Conmutatividad",
    Forall("x", Forall("y",
        Equals(Add(Var("x"), Var("y")), Add(Var("y"), Var("x")))
    )),
    "La suma es conmutativa",
    {"aritmética", "conmutativo"}
)
system.add_axiom(axiom1)

# Mostrar el sistema
print(system.show_summary())
```

### 4. Construir una demostración

```python
# Crear prueba
proof = Proof(
    Equals(Add(Var("a"), Var("a")), Var("a")),  # Objetivo
    "Idempotencia de la suma"
)
proof.set_axiom_system(system)

# Añadir pasos
proof.add_step(
    Equals(Var("a"), Add(Var("a"), Const(0, "0"))),
    "Por axioma de identidad",
    JustificationType.AXIOM
)

proof.add_step(
    Equals(Add(Var("a"), Const(0, "0")), Add(Var("a"), Var("a"))),
    "Por sustitución",
    JustificationType.INFERENCE,
    depends_on=[1]
)

# ... más pasos ...

proof.mark_complete()
```

### 5. Crear y almacenar teoremas

```python
# Crear teorema
theorem = Theorem(
    "Idempotencia",
    Equals(Add(Var("a"), Var("a")), Var("a")),
    proof,
    "La suma es idempotente",
    {"álgebra", "idempotencia"}
)

# Crear biblioteca
library = ProofLibrary("Mi Biblioteca")
library.add_theorem(theorem)

# Consultar
print(library.list_all())
```

### 6. Verificar demostraciones

```python
# Crear verificador
verifier = ProofVerifier(system)

# Verificar prueba
if verifier.verify(proof):
    print("✓ Demostración válida")
else:
    print("✗ Errores encontrados:")
    for error in verifier.get_errors():
        print(f"  • {error}")
```

## 📚 Ejemplos Completos

### Ejemplo 1: Distancia de Hamming es una Métrica

```bash
cd demos
python demo_hamming_metrica.py
```

Demuestra formalmente que la distancia de Hamming cumple las tres propiedades de una métrica:

1. No negatividad e identidad
2. Simetría
3. Desigualdad triangular

### Ejemplo 2: Álgebra de Boole (Huntington 1903)

```bash
cd demos
python demo_boolean_algebra.py
```

Muestra los postulados de Huntington (1903) y deriva teoremas del álgebra de Boole como:

- Idempotencia
- Absorción
- Leyes de De Morgan

### Ejemplo 3: Inducción Matemática (Axiomas de Peano 1889)

```bash
cd demos
python demo_induccion_naturales.py
```

Demuestra propiedades de los números naturales usando inducción matemática:

**Teorema 1 - Fórmula de Gauss**:

```
Σ(i=0 to n) i = n(n+1)/2
```

Caso base: 0 = 0·1/2 ✓  
Paso inductivo: sum(n+1) = sum(n) + (n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2 ✓

**Teorema 2 - Suma de cuadrados**:

```
Σ(i=1 to n) i² = n(n+1)(2n+1)/6
```

Validado para n = 0..10 ✓

**Teorema 3 - Serie geométrica**:

```
Σ(i=0 to n) 2^i = 2^(n+1) - 1
```

Ejemplo: 1+2+4+8+16 = 32-1 = 31 ✓

**Teorema 4 - Desigualdad exponencial**:

```
∀n ∈ ℕ: 2^n ≥ n + 1
```

Ejemplo: 2^10 = 1024 ≥ 11 (diferencia crece exponencialmente) ✓

Cada teorema incluye:

- Demostración formal paso a paso
- Validación computacional
- Visualización de resultados

## 🔧 Sintaxis de Expresiones

### Operadores Lógicos

```python
And(p, q)           # p ∧ q  (conjunción)
Or(p, q)            # p ∨ q  (disyunción)
Not(p)              # ¬p     (negación)
Implies(p, q)       # p ⟹ q (implicación)
Iff(p, q)           # p ⟺ q (doble implicación)
```

### Operadores Aritméticos

```python
Add(x, y)           # x + y  (suma)
Mul(x, y)           # x · y  (multiplicación)
```

### Predicados

```python
Equals(x, y)        # x = y
NotEquals(x, y)     # x ≠ y
LessEq(x, y)        # x ≤ y
GreaterEq(x, y)     # x ≥ y
```

### Cuantificadores

```python
Forall("x", P(x))                    # ∀x: P(x)
Forall("x", P(x), domain)            # ∀x ∈ domain: P(x)
Exists("x", Q(x))                    # ∃x: Q(x)
Exists("x", Q(x), domain)            # ∃x ∈ domain: Q(x)
```

## 🎓 Reglas de Inferencia Disponibles

### Reglas Clásicas (10)

| Regla | Forma | Descripción |
|-------|-------|-------------|
| **Modus Ponens** | P, P⟹Q ⊢ Q | Si P es verdadero y P implica Q, entonces Q es verdadero |
| **Modus Tollens** | ¬Q, P⟹Q ⊢ ¬P | Si Q es falso y P implica Q, entonces P es falso |
| **Sustitución** | P(x) ⊢ P(t) | Reemplazar variables por términos concretos |
| **Instanciación Universal** | ∀x:P(x) ⊢ P(t) | De una propiedad universal, derivar caso particular |
| **Generalización Existencial** | P(t) ⊢ ∃x:P(x) | De un caso particular, derivar existencia |
| **Conjunción** | P, Q ⊢ P∧Q | Combinar dos proposiciones verdaderas |
| **Eliminación de Conjunción** | P∧Q ⊢ P (o Q) | De una conjunción, extraer componente |
| **Disyunción** | P ⊢ P∨Q | Debilitar una proposición |
| **Silogismo Hipotético** | P⟹Q, Q⟹R ⊢ P⟹R | Encadenar implicaciones |
| **Doble Negación** | ¬¬P ⊢ P | Eliminar/introducir doble negación |

### Reglas de Inducción (3)

| Regla | Forma | Uso |
|-------|-------|-----|
| **Inducción Matemática** | P(0), ∀n:P(n)⟹P(S(n)) ⊢ ∀n:P(n) | Demostrar propiedades de números naturales |
| **Inducción Fuerte** | ∀n:(∀k<n:P(k))⟹P(n) ⊢ ∀n:P(n) | Cuando el paso inductivo necesita todos los casos anteriores |
| **Inducción Estructural** | P(base), ∀x:P(x)⟹P(constructor(x)) ⊢ ∀x:P(x) | Para listas, árboles y estructuras recursivas |

**Total**: 13 reglas de inferencia implementadas

## 💡 Casos de Uso Avanzados

### Definir tu propio sistema axiomático

```python
# Crear sistema para aritmética de Peano
peano = AxiomSystem("Aritmética de Peano", "Axiomas de los números naturales")

# P1: 0 es un número natural
peano.add_axiom(Axiom(
    "P1",
    Pred("∈", Const(0, "0"), Var("ℕ")),
    "0 es un número natural"
))

# P2: El sucesor de un natural es natural
peano.add_axiom(Axiom(
    "P2",
    Forall("n",
        Implies(
            Pred("∈", Var("n"), Var("ℕ")),
            Pred("∈", Func("S", Var("n")), Var("ℕ"))
        )
    ),
    "El sucesor preserva naturalidad"
))

# ... más axiomas ...
```

### Demostrar un teorema usando reglas de inferencia

```python
from core.math_logic_system import ModusPonens, Substitution

# Crear prueba
proof = Proof(goal, "Mi teorema")

# Paso 1: Premisa
step1 = proof.add_step(p, "Premisa", JustificationType.PREMISE)

# Paso 2: Implicación (de axioma)
step2 = proof.add_axiom_step("A1")

# Paso 3: Aplicar Modus Ponens
rule = ModusPonens()
conclusion = rule.apply(p, implication)
step3 = proof.add_inference_step(
    conclusion,
    rule,
    [step1, step2],
    "Por Modus Ponens"
)
```

### Demostrar por inducción matemática

```python
from core.math_logic_system import (
    MathematicalInduction, PeanoArithmetic, Var, Const, Func, Equals, Forall
)

# Cargar axiomas de Peano
peano = PeanoArithmetic()
system = peano.get_axioms()

# Objetivo: ∀n: P(n)
goal = Forall("n", predicate_P, Var("ℕ"))

proof = Proof(goal, "Teorema por inducción")
proof.set_axiom_system(system)

# CASO BASE: Demostrar P(0)
base_case = proof.add_step(
    predicate_P.substitute({"n": Const(0, "0")}),
    "Caso base: P(0) es verdadero",
    JustificationType.DEFINITION
)

# HIPÓTESIS INDUCTIVA: Asumir P(n)
hypothesis = proof.add_hypothesis(
    predicate_P,
    "Hipótesis inductiva: asumimos P(n)"
)

# PASO INDUCTIVO: Demostrar P(S(n)) usando P(n)
inductive_step = proof.add_step(
    predicate_P.substitute({"n": Func("S", Var("n"))}),
    "Por tanto, P(S(n)) es verdadero",
    JustificationType.INFERENCE,
    [hypothesis]
)

# APLICAR INDUCCIÓN
rule = MathematicalInduction()
conclusion = proof.add_step(
    goal,
    "Por el principio de inducción matemática (P5)",
    JustificationType.INFERENCE,
    [base_case, inductive_step]
)

proof.mark_complete()
```

## 🔬 Verificación de Demostraciones

El sistema puede verificar automáticamente si una demostración es válida:

```python
verifier = ProofVerifier(axiom_system)

if verifier.verify(proof):
    print("✓ La demostración es válida")
    theorem = Theorem("Mi Teorema", proof.goal, proof)
    library.add_theorem(theorem)
else:
    print("✗ La demostración tiene errores:")
    for error in verifier.get_errors():
        print(f"  {error}")
```

## 📖 Documentación de Módulos

### `expressions.py`

Define la sintaxis de expresiones matemáticas:

- `Expression`: Clase base abstracta
- `Variable`, `Constant`: Términos básicos
- `BinaryOp`, `UnaryOp`: Operadores
- `Function`: Aplicación de funciones
- `Quantifier`: ∀ y ∃
- `Predicate`: Relaciones

### `axioms.py`

Sistema de axiomas y postulados:

- `Axiom`: Proposición aceptada sin demostración
- `Postulate`: Sinónimo de axioma
- `Definition`: Introduce nuevos términos
- `AxiomSystem`: Colección de axiomas

### `inference_rules.py`

Reglas lógicas para derivar proposiciones:

- Todas las reglas de inferencia clásicas
- Sistema extensible para nuevas reglas

### `proof_system.py`

Sistema de construcción de demostraciones:

- `ProofStep`: Un paso con justificación
- `Proof`: Secuencia de pasos
- `Theorem`, `Lemma`, `Corollary`: Resultados
- `ProofLibrary`: Biblioteca de teoremas

### `verification.py`

Verificación automática de demostraciones:

- `ExpressionMatcher`: Pattern matching
- `Unifier`: Unificación de expresiones
- `ProofVerifier`: Valida demostraciones

### `boolean_algebra.py`

Implementación del álgebra de Boole:

- Postulados de Huntington (1903)
- Derivación de teoremas
- Evaluación de expresiones booleanas
- Clase `BooleanAlgebra` con operaciones

### `natural_numbers.py`

Implementación de los números naturales:

- **Axiomas de Peano (1889)**: 5 axiomas fundamentales
  - P1: 0 es un número natural
  - P2: Cada natural tiene un sucesor
  - P3: 0 no es sucesor de ningún número
  - P4: El sucesor es inyectivo
  - P5: Principio de inducción matemática
- **Definiciones recursivas**: Suma, multiplicación y orden
- **Clase `PeanoArithmetic`**: Operaciones computacionales
- **Demostraciones por inducción**: Teoremas clásicos sobre ℕ

## 🤝 Contribuciones

Para añadir nuevos sistemas axiomáticos:

1. Crea un nuevo archivo en `core/math_logic_system/`
2. Define el sistema usando `AxiomSystem`
3. Implementa funciones para derivar teoremas
4. Crea demos en `demos/`

## ❓ Preguntas Frecuentes (FAQ)

### ¿Qué puedo demostrar con este sistema?

Cualquier propiedad que pueda derivarse de axiomas mediante lógica de primer orden. Ejemplos:

- Propiedades algebraicas (conmutatividad, asociatividad, distributividad)
- Teoremas de números naturales (fórmulas de sumas, desigualdades)
- Propiedades de espacios métricos
- Teoremas de lógica proposicional
- Propiedades de estructuras de datos (por inducción estructural)

### ¿Cómo sé si mi demostración es correcta?

El sistema incluye un verificador automático (`ProofVerifier`) que comprueba:

1. Cada paso se justifica correctamente (axioma, premisa, inferencia)
2. Las reglas de inferencia se aplican correctamente
3. Las dependencias entre pasos son válidas
4. La conclusión coincide con el objetivo

### ¿Puedo exportar las demostraciones a LaTeX?

Actualmente, las demostraciones se pueden mostrar en texto. La exportación a LaTeX está planificada para versiones futuras.

### ¿Qué diferencia hay entre inducción simple y fuerte?

- **Inducción simple**: P(0) y [P(n) ⟹ P(n+1)] ⟹ ∀n:P(n)
  - Solo usas P(n) para demostrar P(n+1)
  - Ejemplo: Fórmula de Gauss Σi = n(n+1)/2

- **Inducción fuerte**: [∀k<n: P(k)] ⟹ P(n) ⟹ ∀n:P(n)
  - Usas P(0), P(1), ..., P(n-1) para demostrar P(n)
  - Ejemplo: Teorema fundamental de la aritmética (todo número es producto de primos)

### ¿Cómo agrego mis propios axiomas?

```python
system = AxiomSystem("Mi Sistema", "Descripción")

axiom = Axiom(
    "A1",
    Forall("x", Equals(Add(Var("x"), Const(0)), Var("x"))),
    "Elemento neutro de la suma",
    {"aritmética"}
)
system.add_axiom(axiom)
```

### ¿El sistema soporta lógica de segundo orden?

Actualmente solo lógica de primer orden. La lógica de segundo orden (cuantificación sobre predicados) está en consideración para futuras versiones.

### ¿Puedo usar este sistema para enseñar?

Sí, ese es uno de sus propósitos principales. El proyecto ElectroCore es educativo. Puedes:

- Mostrar demostraciones paso a paso
- Validar ejercicios de estudiantes
- Crear nuevos ejemplos pedagógicos
- Exportar a formatos legibles

## 📄 Licencia

Parte del proyecto ElectroCore - Fundamentos de Electrónica

## 🔗 Referencias

### Fundamentos

- **Peano, G.** (1889). "Arithmetices principia, nova methodo exposita" - Axiomas de los números naturales
- **Huntington, E.V.** (1903). "Sets of Independent Postulates for the Algebra of Logic" - Postulados del álgebra de Boole
- **Whitehead & Russell** (1910-1913). "Principia Mathematica" - Fundamentos de la matemática
- **Hilbert & Ackermann** (1928). "Grundzüge der theoretischen Logik" - Lógica matemática moderna

### Teoría de Conjuntos y Lógica

- Teoría de Conjuntos de Zermelo-Fraenkel (ZFC)
- Teoría de Modelos (Tarski)
- Teoría de la Demostración (Gentzen)

### Sistemas Implementados

- ✅ Axiomas de Peano (1889) - Números Naturales
- ✅ Postulados de Huntington (1903) - Álgebra de Boole
- ✅ Axiomas métricos - Espacios métricos
- 🔄 Axiomas de ZFC - Teoría de conjuntos (en desarrollo)

---

**Autor**: ElectroCore Project  
**Fecha**: Enero 2026  
**Versión**: 1.0.0
