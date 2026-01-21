# 🔮 ROADMAP: Quine-McCluskey + Petrick (Fase Futura - Semana 3+)

## 📋 DESCRIPCIÓN

Implementación de **Quine-McCluskey completo con Método de Petrick** para:

1. **Encontrar TODAS las soluciones minimales** (no solo una)
2. **Propósito pedagógico**: Ejercicios que ENSEÑAN estos algoritmos
3. **Mayor control**: Alternativa a SymPy para casos especializados

---

## 🎯 CUÁNDO SE NECESITA

### ❌ NO necesitas QM en Semana 1-2

```
✅ SymPy es suficiente para:
   • Ejercicios normales de Karnaugh
   • Simplificación de 2-8 variables
   • Funciones aleatorias
   • 95% de los casos pedagógicos
```

### ✅ NECESITAS QM en Semana 3+ si

```
✅ Quieres ejercicios DE Quine-McCluskey (enseñanza)
✅ Necesitas mostrar proceso paso a paso
✅ Quieres múltiples soluciones minimales
✅ Valor pedagógico en Petrick
✅ Mayor control sobre simplificación
```

---

## 📊 COMPLEJIDAD ANÁLISIS

### Por Número de Variables

```
VARIABLES   MINTERMS    PRIMOS IMP.   TIEMPO QM    TIEMPO PETRICK   VIABLE?
─────────────────────────────────────────────────────────────────────────
2           4           2-4           < 1ms        < 1ms            ✅ Trivial
3           8           3-8           1ms          1ms              ✅ Fácil
4           16          5-15          2ms          2ms              ✅ Fácil
5           32          8-25          5ms          5ms              ✅ Fácil
6           64          15-50         20ms         20ms             ✅ Viable
7           128         25-100        100ms        100ms            ✅ Viable
8           256         50-200        500ms        500ms-2s         ⚠️ Lento
9           512         100-300       2s           5-10s            ❌ Muy lento
10+         1024+       200+          10s+         30s+             ❌ Impractico
```

**Recomendación**: QM funcional hasta **8 variables**, suficiente para Electrónica Digital.

---

## 🏗️ ARQUITECTURA PROPUESTA

### Módulo Nuevo: `modules/combinacional/quine_mccluskey.py`

```
modules/combinacional/
├── generators.py                    (Usa SymPy - Semana 1)
├── models.py
├── quine_mccluskey.py              (🆕 Semana 3)
│   ├── QuineMcCluskey
│   │   ├── find_prime_implicants()
│   │   ├── build_coverage_matrix()
│   │   └── petrick_method()
│   │
│   ├── QuineMcCluskeyExplained     (🆕 Didáctico)
│   │   ├── show_grouping()
│   │   ├── show_primes()
│   │   ├── show_coverage()
│   │   └── show_petrick_steps()
│   │
│   └── PetrickSolver
│       └── find_all_minimal_covers()
```

---

## 💻 CÓDIGO ESQUELETO

### 1. CLASE PRINCIPAL: QuineMcCluskey

```python
from typing import List, Set, Tuple, Dict
from dataclasses import dataclass

@dataclass
class PrimeImplicant:
    """Representa un primo implicante."""
    terms: Set[int]           # {0, 1, 4, 5}
    binary: str               # "0XX1"
    coverage: Set[int]        # Qué minterms cubre
    is_essential: bool = False

class QuineMcCluskey:
    """Implementación de Quine-McCluskey + Petrick."""
    
    def __init__(self, num_vars: int):
        self.num_vars = num_vars
        self.var_names = [chr(ord('A') + i) for i in range(num_vars)]
    
    def simplify(self, minterms: List[int], 
                 dont_cares: List[int] = None,
                 return_all: bool = False) -> Dict:
        """
        Simplifica función booleana.
        
        Args:
            minterms: Posiciones donde f=1, ej: [0, 2, 5, 7]
            dont_cares: Posiciones indiferentes, ej: [1, 3]
            return_all: Si True, retorna TODAS las soluciones minimales
        
        Returns:
            {
                'prime_implicants': List[PrimeImplicant],
                'essential': List[PrimeImplicant],
                'minimal_forms': List[List[str]],  # Todas las soluciones
                'num_solutions': int
            }
        """
        
        # PASO 1: Inicializar
        all_ones = set(minterms)
        all_dc = set(dont_cares) if dont_cares else set()
        all_terms = all_ones | all_dc
        
        # PASO 2: Quine-McCluskey (generar primos implicantes)
        primes = self._quine_mccluskey(all_ones, all_dc)
        # Retorna: Lista de PrimeImplicant
        
        # PASO 3: Identificar esenciales
        essentials = self._find_essential(primes, all_ones)
        
        # PASO 4: Tabla de cobertura
        matrix = self._build_coverage_matrix(primes, all_ones)
        
        # PASO 5: Método de Petrick (TODAS las soluciones)
        minimal_covers = self._petrick_method(matrix, primes)
        
        return {
            'prime_implicants': primes,
            'essential_implicants': essentials,
            'minimal_forms': minimal_covers,
            'num_solutions': len(minimal_covers),
            'complexity': self._estimate_complexity(primes, all_ones)
        }
    
    def _quine_mccluskey(self, minterms: Set[int], 
                        dont_cares: Set[int]) -> List[PrimeImplicant]:
        """
        Implementa algoritmo Quine-McCluskey.
        
        Pasos:
        1. Agrupar términos por número de 1s (Hamming weight)
        2. Combinar grupos adyacentes (diferencia de 1 bit)
        3. Marcar términos combinados
        4. Retornar términos sin combinar (primos)
        
        Complejidad: O(n² log n) donde n = |minterms|
        Para 256 términos: ~65,000 ops → ~10-50ms
        """
        all_terms = minterms | dont_cares
        
        # Agrupar por Hamming weight
        groups = self._group_by_hamming_weight(all_terms)
        
        # Iterar hasta convergencia
        current_terms = groups
        used_terms = set()
        
        iteration = 0
        while iteration < self.num_vars and current_terms:
            next_terms = []
            
            # Combinar grupos adyacentes
            for i in range(len(current_terms) - 1):
                combined = self._combine_terms(
                    current_terms[i], 
                    current_terms[i+1],
                    minterms, dont_cares
                )
                if combined:
                    next_terms.append(combined)
                    used_terms.update([t.terms for t in combined])
            
            current_terms = next_terms
            iteration += 1
        
        # Primos: términos que NO se combinaron
        primes = [t for t in current_terms if t.terms not in used_terms]
        return primes
    
    def _build_coverage_matrix(self, primes: List[PrimeImplicant],
                              minterms: Set[int]) -> Dict:
        """
        Crea matriz de cobertura.
        
        Filas: Primos implicantes
        Cols: Minterms
        Valor: 1 si primo cubre minterm
        
        Complejidad: O(n × m) donde n=primos, m=minterms
        Típico: 50 × 256 = 12,800 ops → ~1ms
        """
        
        matrix = {}
        for i, prime in enumerate(primes):
            matrix[i] = {m: (m in prime.coverage) for m in minterms}
        
        return matrix
    
    def _petrick_method(self, matrix: Dict, 
                       primes: List[PrimeImplicant]) -> List[List[str]]:
        """
        Método de Petrick: encuentra TODAS las cubiertas minimales.
        
        Algoritmo:
        1. Para cada minterm, crear suma de primos que lo cubren
        2. Multiplicar todas las sumas (expansión booleana)
        3. Simplificar usando absorción
        4. Retornar TODAS las términos mínimos
        
        Ejemplo:
        Minterms: {0, 1, 2}
        - Minterm 0 cubierto por: P1 + P2
        - Minterm 1 cubierto por: P2 + P3
        - Minterm 2 cubierto por: P1 + P3
        
        Función Petrick: (P1 + P2) · (P2 + P3) · (P1 + P3)
        Expandir: P1·P2·P1 + P1·P2·P3 + ...
        Simplificar: P1·P2 + P1·P3 + P2·P3 + ...
        Mínimos: [P1·P2, P1·P3, ...] (2 términos cada uno)
        
        Complejidad: O(2^n) worst case, pero típicamente O(n³)
        Para 50 primos: ~125,000 ops → ~100-500ms
        """
        
        # Construir función Petrick como lista de listas
        petrick_expr = []
        for minterm in sorted(matrix[0].keys()):
            covering_primes = [
                i for i in range(len(primes))
                if matrix[i][minterm]
            ]
            if covering_primes:
                petrick_expr.append(covering_primes)
        
        # Expandir producto booleano
        minimal_covers = self._expand_boolean_product(petrick_expr, primes)
        
        # Simplificar usando absorción
        minimal_covers = self._simplify_covers(minimal_covers)
        
        return minimal_covers
    
    def _expand_boolean_product(self, expr: List[List[int]], 
                               primes: List[PrimeImplicant]) -> List[Set[int]]:
        """
        Expande (P1+P2)·(P2+P3)·... retornando todas las cubiertas.
        
        Usa método recursivo con memoización.
        """
        if not expr:
            return [set()]
        
        result = []
        rest = self._expand_boolean_product(expr[1:], primes)
        
        for prime_idx in expr[0]:
            for cover in rest:
                new_cover = {prime_idx} | cover
                result.append(new_cover)
        
        return result
    
    def _simplify_covers(self, covers: List[Set[int]]) -> List[Set[int]]:
        """
        Simplifica usando absorción (P ⊆ Q → elimina Q).
        """
        unique = list(covers)  # Eliminar duplicados
        unique = [c for c in unique if not any(
            c != other and c <= other for other in unique
        )]
        return sorted(unique, key=lambda x: len(x))


class QuineMcCluskeyExplained(QuineMcCluskey):
    """
    Versión didáctica: muestra todos los pasos.
    Perfecto para ejercicios de enseñanza.
    """
    
    def __init__(self, num_vars: int, verbose: bool = True):
        super().__init__(num_vars)
        self.verbose = verbose
        self.steps = []  # Guardar pasos para mostrar
    
    def show_grouping(self) -> str:
        """Retorna tabla de agrupación por Hamming weight."""
        # HTML/LaTeX con agrupación inicial
        pass
    
    def show_primes(self) -> str:
        """Retorna lista de primos implicantes."""
        # HTML/LaTeX con los primos encontrados
        pass
    
    def show_coverage_matrix(self) -> str:
        """Retorna matriz de cobertura como tabla."""
        # HTML/LaTeX con tabla de cobertura
        pass
    
    def show_petrick_steps(self) -> str:
        """Retorna pasos del método de Petrick."""
        # HTML/LaTeX con expansión booleana paso a paso
        pass
```

---

## 🧪 TESTING

### Test Cases Básicos

```python
def test_quine_mccluskey():
    """Tests para QM."""
    
    qm = QuineMcCluskey(3)
    
    # Test 1: AND (F = AB)
    result = qm.simplify([3])  # Solo minterm 3 = 011
    assert len(result['minimal_forms']) == 1
    assert result['minimal_forms'][0] == {'ABC'}
    
    # Test 2: OR (F = A + B)
    result = qm.simplify([1, 2, 3])  # Minterms donde A O B
    assert len(result['minimal_forms']) == 1
    # Algunas formas posibles: {AB, AC, BC} (esperar múltiples)
    
    # Test 3: Múltiples soluciones
    result = qm.simplify([0, 2, 5, 7], return_all=True)
    assert len(result['minimal_forms']) > 1
    # Verificar que TODAS son de igual complejidad
    assert all(len(c) == len(result['minimal_forms'][0]) 
              for c in result['minimal_forms'])
    
    # Test 4: Con don't cares
    result = qm.simplify([0, 1, 2], dont_cares=[3, 5])
    # Debería simplificar más gracias a los don't cares
    
    # Test 5: 8 variables (máximo recomendado)
    result = qm.simplify(list(range(128)))  # 128 minterms
    assert result is not None
    assert result['complexity'] <= 1.0  # No exceder 1 segundo
```

---

## 📅 PLAN DE IMPLEMENTACIÓN (SEMANA 3+)

### Fase 3A: Implementar QM Básico (20h)

**Semana 3, Lunes-Martes**:

- [ ] Implementar `QuineMcCluskey` con Petrick
- [ ] Tests unitarios exhaustivos
- [ ] Documentación de API
- [ ] Validación con casos conocidos

### Fase 3B: Versión Didáctica (15h)

**Semana 3, Miércoles-Jueves**:

- [ ] Implementar `QuineMcCluskeyExplained`
- [ ] Generadores de ejercicios QM
- [ ] Renderizado LaTeX de pasos
- [ ] Tests end-to-end

### Fase 3C: Integración Generadores (10h)

**Semana 3, Viernes**:

- [ ] Crear `modules/combinacional/qm_exercise_generator.py`
- [ ] Ejercicios: "Simplifica usando Quine-McCluskey"
- [ ] Ejercicios: "Encuentra todas las soluciones con Petrick"
- [ ] Tests finales

---

## 📊 MÉTRICAS ESPERADAS

```
IMPLEMENTACIÓN: ~45 horas (Semana 3)
TESTING:        ~10 horas
DOCUMENTACIÓN:  ~5 horas
TOTAL:          ~60 horas (1.5 semanas)

COBERTURA SYMPY: 95% casos
COBERTURA QM:    5% casos especializados + pedagogía

VALOR PEDAGÓGICO: Alto (enseñanza de algoritmos)
COMPLEJIDAD IMPL: Media (algoritmo bien conocido)
MANTENIMIENTO:    Bajo (código estable)
```

---

## 🎓 EJERCICIOS GENERADOS CON QM

### Tipo 1: Quine-McCluskey Manual

```
Problema: Simplifica F = Σ(0,2,5,7) usando Quine-McCluskey

Solución esperada (mostrar pasos):
├─ Tabla inicial (4 minterms)
├─ Primera iteración (agrupación)
├─ Primos implicantes encontrados
├─ Tabla de cobertura
└─ Forma minimal: [AB + C, ...]
```

### Tipo 2: Múltiples Soluciones

```
Problema: Encuentra TODAS las formas minimales de F = Σ(0,1,2,3)

Solución:
├─ Primos: {A, B}
├─ Soluciones minimales: [A + B] (única)
└─ Explicación: Ambos primos son esenciales
```

### Tipo 3: Petrick Avanzado

```
Problema: Usa el método de Petrick para...

Solución (mostrar expansión booleana):
├─ Función Petrick: (P1 + P2) · (P2 + P3) · ...
├─ Expansión: P1·P2 + P1·P3 + ...
├─ Simplificación: [P1·P2, P1·P3]
└─ Todas tienen 2 términos → ambas minimales
```

---

## 🔗 INTEGRACIÓN CON SYMPY

### Comparativa: ¿SymPy o QM?

```python
# SEMANA 1-2: SymPy (por defecto)
from sympy.logic import SOPform
expr = SOPform(vars, minterms)
# Rápido, confiable, suficiente

# SEMANA 3+: QM (cuando se pida específicamente)
from modules.combinacional.quine_mccluskey import QuineMcCluskey
qm = QuineMcCluskey(num_vars)
result = qm.simplify(minterms, return_all=True)
# Todas las soluciones, propósito didáctico
```

---

## 📚 REFERENCIAS

- Quine, W. V. (1952). "The Problem of Simplifying Truth Functions"
- McCluskey Jr., E. J. (1956). "Minimization of Boolean Functions"
- Petrick, S. R. (1956). "A Direct Determination of the Irredundant Forms of a Boolean Function"
- "Digital Logic Design" - Morris Mano, Michael Ciletti

---

## ✅ CONCLUSIÓN

**Quine-McCluskey es OPCIONAL pero RECOMENDADO para:**

- Máximo valor pedagógico
- Enseñanza de algoritmos de minimización
- Encontrar múltiples soluciones minimales

**Timing**: Semana 3+ (después de solidificar MVP con SymPy)

**Esfuerzo**: ~60 horas (manejable, no crítico)

**Impacto**: Alto en educación, bajo en funcionalidad (SymPy ya lo hace)

---

**Estado**: 🟢 PLANIFICADO para Semana 3
**Prioridad**: 🟡 Media (después de Fase 1-2)
