# Sistema de Lógica Matemática y Demostración Formal

Sistema general para construir y verificar demostraciones formales en matemáticas. Implementa un sistema axiomático completo con expresiones, reglas de inferencia, y verificación de pruebas.

## 📋 Características

- **Expresiones matemáticas formales**: Variables, constantes, operadores, funciones, cuantificadores y predicados
- **Sistema de axiomas**: Define axiomas, postulados y definiciones
- **Reglas de inferencia**: Modus ponens, modus tollens, sustitución, cuantificadores, etc.
- **Construcción de pruebas**: Sistema paso a paso con justificaciones
- **Verificación automática**: Valida la corrección de demostraciones
- **Biblioteca de teoremas**: Almacena y consulta resultados demostrados

## 🎯 Casos de Uso

Este sistema puede demostrar propiedades en:

- ✅ **Álgebra de Boole** (Postulados de Huntington 1903)
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
└── boolean_algebra.py      # Álgebra de Boole (Huntington 1903)
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
    
    # Verificación
    ProofVerifier
)
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

- **Modus Ponens**: De P y P⟹Q, derivar Q
- **Modus Tollens**: De ¬Q y P⟹Q, derivar ¬P
- **Sustitución**: Reemplazar variables por expresiones
- **Instanciación Universal**: De ∀x:P(x), derivar P(t)
- **Generalización Existencial**: De P(t), derivar ∃x:P(x)
- **Introducción de Conjunción**: De P y Q, derivar P∧Q
- **Eliminación de Conjunción**: De P∧Q, derivar P (o Q)
- **Introducción de Disyunción**: De P, derivar P∨Q
- **Silogismo Hipotético**: De P⟹Q y Q⟹R, derivar P⟹R
- **Doble Negación**: ¬¬P ⟺ P

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
- Evaluación de expresiones

## 🤝 Contribuciones

Para añadir nuevos sistemas axiomáticos:

1. Crea un nuevo archivo en `core/math_logic_system/`
2. Define el sistema usando `AxiomSystem`
3. Implementa funciones para derivar teoremas
4. Crea demos en `demos/`

## 📄 Licencia

Parte del proyecto ElectroCore - Fundamentos de Electrónica

## 🔗 Referencias

- Huntington, E.V. (1903). "Sets of Independent Postulates for the Algebra of Logic"
- Principia Mathematica (Whitehead & Russell, 1910-1913)
- Teoría de Conjuntos (Zermelo-Fraenkel)
- Lógica Matemática (Hilbert & Ackermann, 1928)

---

**Autor**: ElectroCore Project  
**Fecha**: Enero 2026  
**Versión**: 1.0.0
