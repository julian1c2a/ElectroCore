# 💻 CÓDIGO PARA COMENZAR - Semana 1, MON

**Inicio**: Lunes 15 de enero de 2026
**Tarea**: Implementar primer solver: Numeración con cálculo de acarreos

---

## 📋 CHECKLIST ANTES DE EMPEZAR

```bash
# 1. Verificar Python 3.9+
python --version

# 2. Instalar dependencias
pip install sympy pytest

# 3. Verificar estructura
ls modules/numeracion/
# Debe mostrar: generators.py, models.py

# 4. Verificar main_v2.py existe
ls main_v2.py
```

---

## 🎯 OBJETIVO DE HOY (MON)

Implementar sistema de cálculo de sumas con acarreo para el solver de Numeración.

```
Entrada:  123 (decimal) + 45 (decimal) en binario
Salida:   
  - Suma final: 168
  - Acarreos: [0, 1, 0, 1, ...]
  - Fórmula LaTeX: \text{Acarreo: } [0, 1, 0, 1, ...]
```

---

## 📝 ARCHIVO #1: Verificar estructura actual

Leer primero `modules/numeracion/generators.py`:

```bash
cat modules/numeracion/generators.py
```

Debe tener algo como:

```python
# modules/numeracion/generators.py (ACTUAL - incompleto)

class NumeracionExercise:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        # FALTA: self.solution = None  # ← AQUÍ VA EL CÁLCULO
```

---

## 💻 CÓDIGO PARA ESCRIBIR

### PASO 1: Agregar clase para cálculo de acarreo

**Archivo**: `modules/numeracion/generators.py`

```python
# NUEVO: Agregar al inicio del archivo
from typing import List, Tuple

class CarryCalculator:
    """Calcula acarreos en operaciones aritméticas binarias."""
    
    @staticmethod
    def addition_with_carry(num1: int, num2: int) -> dict:
        """
        Calcula suma con tracking de acarreos.
        
        Args:
            num1: Primer número (base 10)
            num2: Segundo número (base 10)
        
        Returns:
            {
                'result': 168,
                'carry_bits': [0, 1, 0, 1, 0, 1, 0, 0],
                'num1_binary': '01111011',
                'num2_binary': '00101101',
                'result_binary': '10101000',
                'latex_formula': '...'
            }
        """
        
        # Convertir a binario
        bin1 = bin(num1)[2:]  # Quitar '0b'
        bin2 = bin(num2)[2:]
        
        # Igualar longitudes (rellenar con 0s a la izquierda)
        max_len = max(len(bin1), len(bin2))
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)
        
        # Calcular suma con acarreos
        carry_bits = []
        carry = 0
        result_bits = []
        
        # Procesar de derecha a izquierda
        for i in range(max_len - 1, -1, -1):
            bit1 = int(bin1[i])
            bit2 = int(bin2[i])
            
            # Suma: bit1 + bit2 + carry_anterior
            suma = bit1 + bit2 + carry
            
            # Nuevo carry y bit de resultado
            new_carry = 1 if suma >= 2 else 0
            result_bit = suma % 2
            
            carry_bits.insert(0, carry)  # Acarreo anterior
            result_bits.insert(0, result_bit)
            carry = new_carry
        
        # Si hay carry final, agregarlo
        if carry:
            carry_bits.insert(0, carry)
            result_bits.insert(0, carry)
        
        result_binary = ''.join(map(str, result_bits))
        result_decimal = int(result_binary, 2)
        
        # Generar fórmula LaTeX
        latex_formula = CarryCalculator._generate_latex(
            bin1, bin2, result_binary, carry_bits
        )
        
        return {
            'result': result_decimal,
            'carry_bits': carry_bits,
            'num1_binary': bin1,
            'num2_binary': bin2,
            'result_binary': result_binary,
            'latex_formula': latex_formula
        }
    
    @staticmethod
    def _generate_latex(bin1: str, bin2: str, result: str, 
                        carries: List[int]) -> str:
        """Genera representación LaTeX de la suma."""
        
        latex = r"""
\begin{array}{r}
  \text{Acarreos:} & """ + " & ".join(map(str, carries)) + r""" \\
  & """ + " & ".join(bin1) + r""" \\
  + & """ + " & ".join(bin2) + r""" \\
  \hline
  & """ + " & ".join(result) + r"""
\end{array}
"""
        return latex.strip()


# AHORA: Actualizar la clase NumeracionExercise

class NumeracionExercise:
    """Ejercicio de numeración con solución calculada."""
    
    def __init__(self, exercise_type: str, num1: int = None, num2: int = None):
        self.exercise_type = exercise_type  # 'addition', 'conversion', etc.
        self.num1 = num1
        self.num2 = num2
        self.solution = None
        
        # Calcular solución automáticamente
        self._calculate_solution()
    
    def _calculate_solution(self):
        """Calcula la solución según el tipo de ejercicio."""
        
        if self.exercise_type == 'addition_with_carry':
            self.solution = CarryCalculator.addition_with_carry(
                self.num1, self.num2
            )
        elif self.exercise_type == 'binary_to_decimal':
            self.solution = {
                'result': int(self.num1, 2),
                'explanation': f'{self.num1} = {int(self.num1, 2)}'
            }
        elif self.exercise_type == 'decimal_to_binary':
            self.solution = {
                'result': bin(self.num1)[2:],
                'explanation': f'{self.num1} = {bin(self.num1)[2:]}'
            }
```

---

### PASO 2: Tests para verificar que funciona

**Archivo**: `test_numeracion_solver.py` (crear en raíz)

```python
# test_numeracion_solver.py

import pytest
from modules.numeracion.generators import CarryCalculator, NumeracionExercise

def test_carry_calculator_simple():
    """Test 1: Suma simple 3 + 2 = 5"""
    result = CarryCalculator.addition_with_carry(3, 2)
    
    assert result['result'] == 5
    assert result['result_binary'] == '101'
    print(f"✅ Test 1 passed: {3} + {2} = {result['result']}")

def test_carry_calculator_with_carries():
    """Test 2: Suma con acarreos 15 + 1 = 16"""
    result = CarryCalculator.addition_with_carry(15, 1)
    
    assert result['result'] == 16
    assert result['result_binary'] == '10000'
    assert 1 in result['carry_bits']  # Debe tener acarreos
    print(f"✅ Test 2 passed: {15} + {1} = {result['result']}")

def test_carry_calculator_larger():
    """Test 3: Suma más grande 123 + 45 = 168"""
    result = CarryCalculator.addition_with_carry(123, 45)
    
    assert result['result'] == 168
    assert result['result_binary'] == '10101000'
    print(f"✅ Test 3 passed: {123} + {45} = {result['result']}")

def test_numeracion_exercise():
    """Test 4: Ejercicio completo con solución"""
    exercise = NumeracionExercise('addition_with_carry', 123, 45)
    
    assert exercise.solution is not None
    assert exercise.solution['result'] == 168
    assert 'latex_formula' in exercise.solution
    print(f"✅ Test 4 passed: Exercise has solution with LaTeX")

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
```

---

## ▶️ EJECUTAR AHORA

### Paso 1: Copiar el código anterior a `modules/numeracion/generators.py`

```bash
# Abrir el editor y copiar desde "class CarryCalculator" hasta el final
# en modules/numeracion/generators.py
```

### Paso 2: Crear el archivo de tests

```bash
# Crear test_numeracion_solver.py en la raíz
# Copiar el código del archivo de tests anterior
```

### Paso 3: Ejecutar tests

```bash
# Opción 1: Con pytest
pytest test_numeracion_solver.py -v -s

# Opción 2: Sin pytest (solo Python)
python test_numeracion_solver.py
```

### Resultado esperado

```
test_numeracion_solver.py::test_carry_calculator_simple PASSED   ✅
test_numeracion_solver.py::test_carry_calculator_with_carries PASSED ✅
test_numeracion_solver.py::test_carry_calculator_larger PASSED   ✅
test_numeracion_solver.py::test_numeracion_exercise PASSED       ✅

====== 4 passed in 0.23s ======
```

---

## 🎯 CHECKPOINT: FIN DE HOY (MON)

### ✅ Debes tener

1. **CarryCalculator** funcionando con tests pasando
2. **NumeracionExercise** con solución calculada
3. **4 tests** en verde
4. **LaTeX formula** generándose

### 🚀 Siguiente paso (TUE)

Refinar el cálculo para casos especiales:

- Números muy grandes (100+ bits)
- Números con ceros
- Verificar LaTeX rendering

---

## 💡 TIPS

### Para debuggear

```python
# Agregar a tu código:
result = CarryCalculator.addition_with_carry(123, 45)
print("Result:", result)
print("Carry bits:", result['carry_bits'])
print("LaTeX:", result['latex_formula'])
```

### Para evitar errores

```python
# ❌ MALO:
bin1 = bin(123)  # Retorna '0b1111011'

# ✅ BUENO:
bin1 = bin(123)[2:]  # Retorna '1111011' (sin '0b')
```

---

## 📞 SI NO FUNCIONA

**Problema**: `ImportError: No module named 'modules'`

```bash
# Asegúrate de estar en la raíz del proyecto
cd c:\Users\julia\PycharmProjects\PythonProject\GeneratorFEExercises
python test_numeracion_solver.py
```

**Problema**: Tests fallan en 3 + 2 = 5

```bash
# Verifica que result_binary es correcto:
# 3 = 011, 2 = 010, suma = 101
# Revisa que no haya overflow
```

**Problema**: LaTeX genera algo raro

```python
# El LaTeX es opcional, lo importante es que:
# result['result'] == 5
# Puedes ignorar latex_formula por ahora
```

---

**Estado**: 🟢 LISTO PARA EJECUTAR HOY

Tiempo estimado: 2-3 horas (con debugging)
