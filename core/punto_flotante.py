"""
Punto Flotante - Representación V = M × B^E

Donde:
  - M (mantisa): número normalizado en [1, 2) en base B
  - E (exponente): entero que escala el número
  - B: base numérica

Ventaja sobre punto fijo:
  - Error relativo constante: ε_rel = B^(-F_M) (precisión de la mantisa)
  - Rango dinámico: soporta números muy grandes y muy pequeños
  - Mejor para sistemas que cambian de escala

Al mantener M ∈ [1,2), el error relativo se mantiene constante independientemente
de la escala del número representado.
"""

from decimal import Decimal
from typing import Tuple
import math


class FixedPointFloating:
    """Punto flotante básico con mantisa normalizada en [1,2)."""
    
    def __init__(self, F_M: int, E_bits: int, base: int = 2, signed: bool = True):
        """
        Crear punto flotante.
        
        Args:
            F_M: bits/dígitos de precisión en la mantisa (después del punto)
            E_bits: bits/dígitos para el exponente
            base: base numérica (típicamente 2)
            signed: si True, usa M&S para mantisa y exponente con signo
        """
        self.F_M = F_M  # Precisión de mantisa
        self.E_bits = E_bits  # Bits para exponente
        self.base = base
        self.signed = signed
        
        # Propiedades de mantisa
        self.epsilon_mantisa = Decimal(base) ** (-F_M)  # Precisión mantisa
        # Mantisa normalizada está en [1, 2) en base 2
        self.mantisa_min = Decimal(1)  # inclusivo
        self.mantisa_max = Decimal(base)  # exclusivo (no se alcanza)
        
        # Propiedades de exponente
        if E_bits > 0:
            self.E_max_magnitude = base ** (E_bits - 1) if signed else base ** E_bits
            self.E_min = -self.E_max_magnitude if signed else 0
            self.E_max = self.E_max_magnitude - 1
        else:
            self.E_min = self.E_max = 0
        
        # Propiedades del número completo
        self.max_value = (self.mantisa_max - self.epsilon_mantisa) * Decimal(base) ** self.E_max
        self.min_positive = Decimal(1) * Decimal(base) ** self.E_min
        
    def __repr__(self) -> str:
        return f"FP(F_M={self.F_M}, E_bits={self.E_bits}, base={self.base}, signed={self.signed})"
    
    @property
    def info(self) -> dict:
        """Información de la representación."""
        return {
            'F_M': self.F_M,
            'E_bits': self.E_bits,
            'base': self.base,
            'signed': self.signed,
            'epsilon_mantisa': float(self.epsilon_mantisa),
            'mantisa_rango': f"[{self.mantisa_min}, {self.mantisa_max})",
            'exponente_rango': f"[{self.E_min}, {self.E_max}]",
            'max_value': float(self.max_value),
            'min_positive': float(self.min_positive),
        }
    
    def normalize(self, value: float) -> Tuple[float, int]:
        """
        Normalizar un número al formato V = M × B^E donde M ∈ [1, B).
        
        Returns:
            (mantisa, exponente)
        """
        if value == 0:
            return (0.0, 0)
        
        # Obtener signo
        sign = 1 if value >= 0 else -1
        value = abs(value)
        
        # Encontrar exponente tal que 1 ≤ |M| < B
        # value = M × B^E → log_B(value) = log_B(M) + E
        # Como log_B(M) ∈ [0, 1), E = floor(log_B(value))
        exponent = math.floor(math.log(value, self.base))
        
        # Calcular mantisa
        mantisa = Decimal(str(value)) / (Decimal(self.base) ** exponent)
        
        return (sign * float(mantisa), exponent)
    
    def denormalize(self, mantisa: float, exponent: int) -> float:
        """Reconstruir valor desde (M, E)."""
        return mantisa * (self.base ** exponent)
    
    def encode(self, value: float) -> Tuple[int, int]:
        """
        Codificar valor a (M_bits, E_bits).
        
        Returns:
            (M_encoded, E_encoded)
        """
        if value == 0:
            return (0, 0)
        
        # Normalizar
        mantisa, exponent = self.normalize(value)
        
        # Codificar mantisa (en M&S)
        sign = 0 if mantisa >= 0 else 1
        mantisa_abs = abs(mantisa)
        
        # Separar parte entera (siempre 1) y fraccionaria
        mantisa_frac = mantisa_abs - Decimal(1)  # Parte fraccionaria
        M_int = int(mantisa_frac * (Decimal(self.base) ** self.F_M))
        
        if self.signed:
            M_encoded = sign * (self.base ** self.F_M) + M_int
        else:
            M_encoded = M_int
        
        # Codificar exponente (en exceso)
        E_bias = self.base ** (self.E_bits - 1) if self.E_bits > 0 else 0
        E_encoded = exponent + E_bias
        
        return (M_encoded, E_encoded)
    
    def decode(self, M_encoded: int, E_encoded: int) -> float:
        """Decodificar desde (M_bits, E_bits) a valor."""
        if M_encoded == 0 and E_encoded == 0:
            return 0.0
        
        # Decodificar mantisa
        if self.signed:
            sign = M_encoded // (self.base ** self.F_M)
            M_frac = M_encoded % (self.base ** self.F_M)
            sign_mult = -1 if sign != 0 else 1
        else:
            M_frac = M_encoded
            sign_mult = 1
        
        # Reconstruir mantisa: 1.xxxxx
        mantisa_frac = Decimal(M_frac) / (Decimal(self.base) ** self.F_M)
        mantisa = Decimal(1) + mantisa_frac
        
        # Decodificar exponente (quitar exceso)
        E_bias = self.base ** (self.E_bits - 1) if self.E_bits > 0 else 0
        exponent = E_encoded - E_bias
        
        # Reconstruir valor
        value = sign_mult * float(mantisa) * (self.base ** exponent)
        return value
    
    def add(self, v1: float, v2: float) -> float:
        """
        Suma en punto flotante.
        
        Procedimiento:
        1. Normalizar ambos números
        2. Igualar exponentes (usando el mayor)
        3. Sumar mantisas
        4. Renormalizar si es necesario
        """
        if v1 == 0:
            return v2
        if v2 == 0:
            return v1
        
        # Normalizar
        m1, e1 = self.normalize(v1)
        m2, e2 = self.normalize(v2)
        
        # Igualar exponentes (usar el mayor)
        if e1 > e2:
            # Reducir mantisa 2
            m2 = m2 / (self.base ** (e1 - e2))
            e = e1
        else:
            # Reducir mantisa 1
            m1 = m1 / (self.base ** (e2 - e1))
            e = e2
        
        # Sumar mantisas
        m_sum = m1 + m2
        
        # Renormalizar si es necesario
        if m_sum != 0:
            m_result, e_correction = self.normalize(m_sum)
            e = e + e_correction
        else:
            m_result = 0
        
        # Reconstruir
        return self.denormalize(m_result, e)
    
    def subtract(self, v1: float, v2: float) -> float:
        """Resta en punto flotante."""
        return self.add(v1, -v2)
    
    def multiply(self, v1: float, v2: float) -> float:
        """
        Multiplicación en punto flotante.
        
        Procedimiento:
        1. Normalizar ambos números
        2. Multiplicar mantisas
        3. Sumar exponentes
        4. Renormalizar si es necesario
        """
        if v1 == 0 or v2 == 0:
            return 0.0
        
        # Normalizar
        m1, e1 = self.normalize(v1)
        m2, e2 = self.normalize(v2)
        
        # Multiplicar
        m_product = m1 * m2
        e_product = e1 + e2
        
        # Renormalizar (puede que |m_product| esté fuera de [1, base))
        if m_product != 0:
            m_result, e_correction = self.normalize(m_product)
            e_result = e_product + e_correction
        else:
            m_result = 0
            e_result = 0
        
        return self.denormalize(m_result, e_result)
    
    def divide(self, v1: float, v2: float) -> float:
        """División en punto flotante."""
        if v2 == 0:
            raise ValueError("División por cero")
        
        # Normalizar
        m1, e1 = self.normalize(v1)
        m2, e2 = self.normalize(v2)
        
        # Dividir
        m_quotient = m1 / m2
        e_quotient = e1 - e2
        
        # Renormalizar
        if m_quotient != 0:
            m_result, e_correction = self.normalize(m_quotient)
            e_result = e_quotient + e_correction
        else:
            m_result = 0
            e_result = 0
        
        return self.denormalize(m_result, e_result)
    
    def relative_error(self, true_value: float) -> float:
        """
        Calcular error relativo para un valor dado.
        
        El error relativo es aproximadamente epsilon_mantisa,
        independientemente de la escala.
        """
        if true_value == 0:
            return 0
        
        # Normalizar
        mantisa, exponent = self.normalize(true_value)
        
        # Error relativo ≈ ε_mantisa / 2 (por redondeo de mitad)
        # En el peor caso es ε_mantisa
        return float(self.epsilon_mantisa)
    
    def absolute_error(self, true_value: float) -> float:
        """
        Calcular error absoluto para un valor dado.
        
        Error absoluto = error relativo × |valor|
                       ≈ ε_mantisa × |valor|
        """
        return self.relative_error(true_value) * abs(true_value)


def demonstrate_normalization():
    """Demostrar normalización de mantisa."""
    print("\n" + "="*80)
    print("NORMALIZACION DE MANTISA")
    print("="*80)
    
    fp = FixedPointFloating(F_M=4, E_bits=5, base=2)
    print(f"\nRepresentacion: {fp}")
    print(f"Mantisa normalizada está en: [{fp.mantisa_min}, {fp.mantisa_max})")
    
    print(f"\n--- EJEMPLOS DE NORMALIZACION ---")
    test_values = [5.25, 0.125, 100, 0.001, 1024, 0.0001]
    
    print(f"{'Valor Original':<15} {'Mantisa':<12} {'Exponente':<12} {'Verificacion':<15}")
    print("-" * 55)
    
    for value in test_values:
        m, e = fp.normalize(value)
        reconstructed = fp.denormalize(m, e)
        verificacion = "✓" if abs(reconstructed - value) < 1e-10 else "✗"
        print(f"{value:<15.6f} {m:<12.8f} {e:<12d} {verificacion:<15}")
    
    # Verificar que mantisa está en [1, 2)
    print(f"\n--- VERIFICACION DE RANGO DE MANTISA ---")
    all_in_range = True
    for value in test_values:
        if value != 0:
            m, _ = fp.normalize(value)
            in_range = 1 <= abs(m) < fp.base
            all_in_range = all_in_range and in_range
            status = "✓" if in_range else "✗"
            print(f"  Valor {value:<8}: mantisa={abs(m):<12.8f} rango=[1,{fp.base}) {status}")
    
    print(f"\nTodas las mantisas en rango correcto: {'SI ✓' if all_in_range else 'NO ✗'}")


def demonstrate_error_stability():
    """Demostrar que error relativo es estable en punto flotante."""
    print("\n" + "="*80)
    print("ESTABILIDAD DE ERROR RELATIVO")
    print("="*80)
    
    # Comparar punto fijo vs punto flotante
    print(f"\n--- PUNTO FIJO Q(8,4) base 10 ---")
    epsilon_fixed = 10 ** (-4)
    print(f"Precision fija: epsilon = B^(-F) = {epsilon_fixed}")
    
    scales = [10**(-3), 10**(-1), 10**(0), 10**(2), 10**(6), 10**(10)]
    print(f"\n{'Escala':<15} {'Error Absoluto':<20} {'Error Relativo':<20}")
    print("-" * 55)
    
    for scale in scales:
        abs_error = epsilon_fixed
        rel_error = epsilon_fixed / scale
        print(f"{scale:<15.0e} {abs_error:<20.2e} {rel_error:<20.2e}")
    
    # Punto flotante
    print(f"\n--- PUNTO FLOTANTE FP(F_M=4, E_bits=5) base 2 ---")
    fp = FixedPointFloating(F_M=4, E_bits=5, base=2)
    epsilon_float = float(fp.epsilon_mantisa)
    print(f"Precision mantisa: epsilon = B^(-F_M) = {epsilon_float:.6f}")
    
    test_values = [0.001, 0.1, 1, 100, 1000000, 10**(10)]
    print(f"\n{'Valor':<15} {'Error Absoluto':<20} {'Error Relativo':<20}")
    print("-" * 55)
    
    for value in test_values:
        abs_error = fp.absolute_error(value)
        rel_error = fp.relative_error(value)
        print(f"{value:<15.2e} {abs_error:<20.2e} {rel_error:<20.6f}")
    
    print(f"\nObservacion: El error relativo es CONSTANTE en punto flotante")
    print(f"             El error absoluto cambia proporcionalmente al valor")


def demonstrate_operations():
    """Demostrar operaciones aritméticas."""
    print("\n" + "="*80)
    print("OPERACIONES ARITMETICAS EN PUNTO FLOTANTE")
    print("="*80)
    
    fp = FixedPointFloating(F_M=6, E_bits=6, base=2)
    print(f"\nRepresentacion: {fp}")
    
    # Suma
    print(f"\n--- SUMA (requiere igualar exponentes) ---")
    v1, v2 = 5.5, 0.125
    print(f"Calcular: {v1} + {v2}")
    
    m1, e1 = fp.normalize(v1)
    m2, e2 = fp.normalize(v2)
    print(f"  {v1} = {m1:.6f} × 2^{e1}")
    print(f"  {v2} = {m2:.6f} × 2^{e2}")
    
    result = fp.add(v1, v2)
    expected = v1 + v2
    print(f"  Resultado: {result:.6f}")
    print(f"  Esperado:  {expected:.6f}")
    print(f"  Error:     {abs(result - expected):.2e}")
    
    # Multiplicacion
    print(f"\n--- MULTIPLICACION (mas simple) ---")
    v1, v2 = 3.5, 2.25
    print(f"Calcular: {v1} × {v2}")
    
    m1, e1 = fp.normalize(v1)
    m2, e2 = fp.normalize(v2)
    print(f"  {v1} = {m1:.6f} × 2^{e1}")
    print(f"  {v2} = {m2:.6f} × 2^{e2}")
    print(f"  Multiplicar mantisas: {m1:.6f} × {m2:.6f} = {m1*m2:.6f}")
    print(f"  Sumar exponentes: {e1} + {e2} = {e1+e2}")
    
    result = fp.multiply(v1, v2)
    expected = v1 * v2
    print(f"  Resultado: {result:.6f}")
    print(f"  Esperado:  {expected:.6f}")
    print(f"  Error:     {abs(result - expected):.2e}")
    
    # Resto de operaciones
    print(f"\n--- RESTA Y DIVISION ---")
    test_cases = [
        (10, 3, "resta"),
        (15, 4, "division"),
        (100, 0.01, "suma grandes escalas"),
    ]
    
    for v1, v2, desc in test_cases:
        suma = fp.add(v1, v2)
        resta = fp.subtract(v1, v2)
        mult = fp.multiply(v1, v2)
        div = fp.divide(v1, v2)
        
        print(f"\n{v1} y {v2}:")
        print(f"  + : {suma:.8f} (esperado: {v1 + v2:.8f})")
        print(f"  - : {resta:.8f} (esperado: {v1 - v2:.8f})")
        print(f"  × : {mult:.8f} (esperado: {v1 * v2:.8f})")
        print(f"  / : {div:.8f} (esperado: {v1 / v2:.8f})")


if __name__ == "__main__":
    demonstrate_normalization()
    demonstrate_error_stability()
    demonstrate_operations()
