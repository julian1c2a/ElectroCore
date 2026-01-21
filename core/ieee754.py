"""
IEEE 754 - Estándar Completo para Punto Flotante

Incluye:
1. Números normalizados: ±1.M × B^E (mantisa implícita)
2. Números denormalizados (subnormales): ±0.M × B^E_min
3. Infinito: ±∞ (exponente=B-1, mantisa=0)
4. NaN (Not a Number): qNaN y sNaN (exponente=B-1, mantisa≠0)

Bit de signo: 0 = positivo, 1 = negativo
Exponente: formato exceso K (bias)
Mantisa: implícito "1." para normalizados, "0." para denormalizados
"""

from decimal import Decimal
from typing import Tuple, Union
import math


class IEEE754Gen:
    """
    Punto flotante IEEE 754 genérico con especiales.
    
    Soporta cualquier:
    - Base (2, 10, 16, etc.)
    - Longitud de exponente E_bits
    - Longitud de mantisa F_bits
    
    Casos especiales:
    - Números normalizados: ±1.M × B^E (mantisa implícita)
    - Números denormalizados: ±0.M × B^E_min (subnormales)
    - Infinito: ±∞ (E=todos1s, M=0)
    - NaN: qNaN (MSB=1) y sNaN (MSB=0, M≠0)
    """
    
    def __init__(self, E_bits: int, F_bits: int, base: int = 2):
        """
        Crear representación IEEE 754 genérica.
        
        Args:
            E_bits: bits para exponente
            F_bits: bits para mantisa (fraccionaria)
            base: base numérica (2, 10, 16, etc.) - por defecto 2
        
        Ejemplo:
            ieee32 = IEEE754Gen(E_bits=8, F_bits=23, base=2)  # IEEE 754 single
            ieee64 = IEEE754Gen(E_bits=11, F_bits=52, base=2)  # IEEE 754 double
            ieee_decimal = IEEE754Gen(E_bits=8, F_bits=16, base=10)  # Decimal flotante
        """
        self.E_bits = E_bits
        self.F_bits = F_bits
        self.base = base
        
        # Validaciones
        if E_bits < 1 or F_bits < 1:
            raise ValueError("E_bits y F_bits deben ser >= 1")
        if base < 2:
            raise ValueError("base debe ser >= 2")
        
        # Bias para exponente (formato exceso K)
        # Bias = B^(E_bits-1) - 1
        self.bias = (base ** (E_bits - 1)) - 1
        
        # Valores extremos de exponente
        self.E_max_encoded = base ** E_bits - 1  # Todos 1s: para NaN e infinito
        self.E_min_encoded = 1  # Para denormalizados
        self.E_zero_encoded = 0  # Para denormalizados
        
        # Exponentes reales (después de restar bias)
        self.E_min = 1 - self.bias  # Exponente mínimo para denormalizados
        self.E_max = self.bias - 1  # Exponente máximo para normalizados
        
        # Precisión (máxima mantisa fraccionaria)
        self.epsilon = Decimal(base) ** (-F_bits)
        
    def __repr__(self) -> str:
        return f"IEEE754Gen(E_bits={self.E_bits}, F_bits={self.F_bits}, base={self.base})"
    
    @property
    def info(self) -> dict:
        """Información de la representación."""
        return {
            'E_bits': self.E_bits,
            'F_bits': self.F_bits,
            'total_bits': 1 + self.E_bits + self.F_bits,
            'bias': self.bias,
            'E_min': self.E_min,
            'E_max': self.E_max,
            'epsilon': float(self.epsilon),
            'normalized_min': float(Decimal(1) * Decimal(self.base) ** self.E_min),
            'denormalized_min': float(self.epsilon * Decimal(self.base) ** self.E_min),
            'max': float((Decimal(2) - self.epsilon) * Decimal(self.base) ** self.E_max),
        }
    
    def encode_normalized(self, value: float) -> Tuple[int, int, int]:
        """
        Codificar número normalizado.
        
        Returns:
            (sign, E_encoded, M_encoded)
        """
        if value == 0:
            return (0, 0, 0)
        
        # Signo
        sign = 0 if value >= 0 else 1
        value = abs(value)
        
        # Normalizar: encontrar E tal que 1 ≤ M < 2
        E = math.floor(math.log(value, self.base))
        M = value / (self.base ** E)
        
        # Codificar mantisa (solo fraccionaria, el 1 es implícito)
        M_frac = M - 1  # Parte fraccionaria
        M_encoded = int(M_frac * (self.base ** self.F_bits))
        
        # Codificar exponente (exceso K)
        E_encoded = E + self.bias
        
        # Validar rango
        if E_encoded < self.E_min_encoded:
            raise ValueError(f"Valor {value} es denormalizado, usar encode_denormalized()")
        if E_encoded >= self.E_max_encoded:
            raise ValueError(f"Valor {value} es infinito o fuera de rango")
        
        return (sign, E_encoded, M_encoded)
    
    def encode_denormalized(self, value: float) -> Tuple[int, int, int]:
        """
        Codificar número denormalizado (subnormal).
        
        Formato: ±0.M × B^E_min
        Usado para valores muy pequeños cerca de 0.
        """
        if value == 0:
            return (0, 0, 0)
        
        # Signo
        sign = 0 if value >= 0 else 1
        value = abs(value)
        
        # Para denormalizados: valor = 0.M × B^E_min
        # E_min = 1 - bias
        # M = valor / (B^E_min)
        E_min_real = self.E_min
        M = value / (self.base ** E_min_real)
        
        # Validar que M < 1
        if M >= 1:
            raise ValueError(f"Valor {value} no es denormalizado, es normalizado")
        
        # Codificar mantisa (0.M)
        M_encoded = int(M * (self.base ** self.F_bits))
        
        # Exponente encoded es 0 para denormalizados
        E_encoded = 0
        
        return (sign, E_encoded, M_encoded)
    
    def encode_infinity(self, positive: bool = True) -> Tuple[int, int, int]:
        """
        Codificar infinito.
        
        Args:
            positive: True para +∞, False para -∞
        """
        sign = 0 if positive else 1
        E_encoded = self.E_max_encoded  # Todos 1s
        M_encoded = 0  # Mantisa todo ceros
        
        return (sign, E_encoded, M_encoded)
    
    def encode_nan(self, quiet: bool = True) -> Tuple[int, int, int]:
        """
        Codificar NaN.
        
        Args:
            quiet: True para qNaN (quiet), False para sNaN (signaling)
        """
        sign = 0  # El signo no tiene significancia en NaN
        E_encoded = self.E_max_encoded  # Todos 1s
        
        if quiet:
            # qNaN: MSB de mantisa = 1
            M_encoded = self.base ** (self.F_bits - 1)  # MSB = 1, resto = 0
        else:
            # sNaN: MSB de mantisa = 0, pero mantisa ≠ 0
            M_encoded = 1  # Valor mínimo, MSB = 0
        
        return (sign, E_encoded, M_encoded)
    
    def encode(self, value: float) -> int:
        """
        Codificar un número flotante a su representación IEEE 754 de 32 bits.
        
        Este método determina automáticamente si el número es:
        - Normalizado
        - Denormalizado (subnormal)
        - Especial (infinito, NaN)
        
        Args:
            value: número flotante a codificar
            
        Returns:
            int: representación IEEE 754 completa como entero
        """
        # Casos especiales
        if math.isnan(value):
            sign, E_enc, M_enc = self.encode_nan(quiet=True)
        elif math.isinf(value):
            sign, E_enc, M_enc = self.encode_infinity(positive=(value > 0))
        else:
            # Intentar normalizado primero
            try:
                sign, E_enc, M_enc = self.encode_normalized(value)
            except ValueError:
                # Si no es normalizado, intenta denormalizado
                try:
                    sign, E_enc, M_enc = self.encode_denormalized(value)
                except ValueError:
                    # Si aún no cabe, es infinito
                    positive = value > 0
                    sign, E_enc, M_enc = self.encode_infinity(positive=positive)
        
        # Combinar en un entero: [signo|exponente|mantisa]
        total_bits = 1 + self.E_bits + self.F_bits
        result = (sign << (self.E_bits + self.F_bits)) | (E_enc << self.F_bits) | M_enc
        return result
    
    def decode(self, sign: int, E_encoded: int, M_encoded: int) -> Union[float, str]:
        """
        Decodificar IEEE 754.
        
        Returns:
            float: valor normal/denormalizado
            str: "inf", "-inf", "qNaN", "sNaN"
        """
        # Casos especiales
        if E_encoded == self.E_max_encoded:
            # Exponente = todos 1s
            if M_encoded == 0:
                # Infinito
                return float('inf') if sign == 0 else float('-inf')
            else:
                # NaN
                MSB = M_encoded >= (self.base ** (self.F_bits - 1))
                return "qNaN" if MSB else "sNaN"
        
        if E_encoded == 0:
            # Denormalizado o cero
            if M_encoded == 0:
                return 0.0
            else:
                # Denormalizado: ±0.M × B^E_min
                E_real = self.E_min
                M_frac = Decimal(M_encoded) / Decimal(self.base) ** self.F_bits
                value = float(M_frac * Decimal(self.base) ** E_real)
                return -value if sign == 1 else value
        
        # Normalizado: ±1.M × B^E
        E_real = E_encoded - self.bias
        M_frac = Decimal(M_encoded) / Decimal(self.base) ** self.F_bits
        M = 1 + M_frac  # Mantisa implícita
        value = float(M * Decimal(self.base) ** E_real)
        
        return -value if sign == 1 else value
    
    def is_special(self, E_encoded: int, M_encoded: int) -> bool:
        """Verificar si es un valor especial (infinito o NaN)."""
        return E_encoded == self.E_max_encoded
    
    def is_denormalized(self, E_encoded: int) -> bool:
        """Verificar si es denormalizado."""
        return E_encoded == 0
    
    def get_range_normalized(self) -> Tuple[float, float]:
        """Obtener rango de números normalizados."""
        min_norm = float(Decimal(1) * Decimal(self.base) ** self.E_min)
        max_norm = float((Decimal(2) - self.epsilon) * Decimal(self.base) ** self.E_max)
        return (min_norm, max_norm)
    
    def get_range_denormalized(self) -> Tuple[float, float]:
        """Obtener rango de números denormalizados."""
        min_denorm = float(self.epsilon * Decimal(self.base) ** self.E_min)
        max_denorm = float((1 - self.epsilon) * Decimal(self.base) ** self.E_min)
        return (min_denorm, max_denorm)


def demonstrate_ieee754():
    """Demostración de IEEE 754."""
    print("\n" + "="*80)
    print("IEEE 754 - NUMEROS NORMALIZADOS")
    print("="*80)
    
    # IEEE 754 simple: 8 bits exponente, 23 bits mantisa (32 bits total)
    ieee = IEEE754(E_bits=8, F_bits=23, base=2)
    
    print(f"\nRepresentación: {ieee}")
    info = ieee.info
    print(f"  Total bits: {info['total_bits']}")
    print(f"  Bias: {info['bias']}")
    print(f"  E_min: {info['E_min']}, E_max: {info['E_max']}")
    print(f"  Rango normalizado: [{info['normalized_min']:.2e}, {info['max']:.2e}]")
    print(f"  Rango denormalizado: [0, {info['denormalized_min']:.2e}]")
    
    print(f"\n--- NUMEROS NORMALIZADOS ---")
    test_values = [1.5, 100, 0.00001, 1e30]
    
    print(f"{'Valor':<15} {'Sign':<6} {'E_enc':<8} {'M_enc':<12} {'Decodificado':<15}")
    print("-" * 60)
    
    for value in test_values:
        try:
            s, e, m = ieee.encode_normalized(value)
            decoded = ieee.decode(s, e, m)
            print(f"{value:<15.6e} {s:<6d} {e:<8d} {m:<12d} {decoded:<15.6e}")
        except ValueError as err:
            print(f"{value:<15.6e} ERROR: {err}")
    
    print(f"\n--- NUMEROS DENORMALIZADOS (subnormales) ---")
    print(f"Formato: ±0.M × B^({ieee.E_min})")
    
    # Valores muy pequeños
    denorm_values = [1e-39, 1e-40, 1e-43, 1e-44]
    
    print(f"{'Valor':<15} {'Sign':<6} {'E_enc':<8} {'M_enc':<12} {'Decodificado':<15}")
    print("-" * 60)
    
    for value in denorm_values:
        try:
            s, e, m = ieee.encode_denormalized(value)
            decoded = ieee.decode(s, e, m)
            print(f"{value:<15.6e} {s:<6d} {e:<8d} {m:<12d} {decoded:<15.6e}")
        except ValueError:
            print(f"{value:<15.6e} (Fuera de rango denormalizado)")
    
    print(f"\n--- INFINITO ---")
    s_inf, e_inf, m_inf = ieee.encode_infinity(positive=True)
    s_ninf, e_ninf, m_ninf = ieee.encode_infinity(positive=False)
    
    print(f"  +inf: sign={s_inf}, E={e_inf}, M={m_inf} → {ieee.decode(s_inf, e_inf, m_inf)}")
    print(f"  -inf: sign={s_ninf}, E={e_ninf}, M={m_ninf} → {ieee.decode(s_ninf, e_ninf, m_ninf)}")
    
    print(f"\n--- NaN (Not a Number) ---")
    s_qnan, e_qnan, m_qnan = ieee.encode_nan(quiet=True)
    s_snan, e_snan, m_snan = ieee.encode_nan(quiet=False)
    
    print(f"  qNaN (quiet): sign={s_qnan}, E={e_qnan}, M={m_qnan} → {ieee.decode(s_qnan, e_qnan, m_qnan)}")
    print(f"  sNaN (signaling): sign={s_snan}, E={e_snan}, M={m_snan} → {ieee.decode(s_snan, e_snan, m_snan)}")
    
    print(f"\n--- PROPIEDADES DE NaN ---")
    print(f"  qNaN (quiet NaN):")
    print(f"    - No genera excepción al propagarse")
    print(f"    - MSB mantisa = 1")
    print(f"    - Usado para errores de operación anterior")
    print(f"  sNaN (signaling NaN):")
    print(f"    - GENERA EXCEPCION al usarse en operaciones")
    print(f"    - MSB mantisa = 0, pero mantisa ≠ 0")
    print(f"    - Usado para detectar operaciones inválidas")
    print(f"  NaN ≠ NaN (no comparable ni con igualdad)")


def demonstrate_denormalized_vs_normalized():
    """Comparar transición de normalizado a denormalizado."""
    print("\n" + "="*80)
    print("TRANSICION: NORMALIZADO → DENORMALIZADO")
    print("="*80)
    
    ieee = IEEE754(E_bits=5, F_bits=10, base=2)
    
    print(f"\nRepresentación: {ieee}")
    print(f"E_bits: {ieee.E_bits}, F_bits: {ieee.F_bits}")
    print(f"Bias: {ieee.bias}")
    
    min_norm, max_norm = ieee.get_range_normalized()
    min_denorm, max_denorm = ieee.get_range_denormalized()
    
    print(f"\nRangos:")
    print(f"  Normalizados:   [{min_norm:.6e}, {max_norm:.6e}]")
    print(f"  Denormalizados: [{min_denorm:.6e}, {max_denorm:.6e}]")
    print(f"  Gap: {min_norm - max_denorm:.6e}")
    
    print(f"\nSin denormalizados habría 'salto' de {max_denorm:.6e} a {min_norm:.6e}")
    print(f"Con denormalizados: transición suave desde {min_denorm:.6e}")
    
    print(f"\n--- VALORES CERCA DE CERO ---")
    test_values = [
        min_norm * 1.5,  # Normalizado
        min_norm * 0.5,  # Denormalizado
        min_denorm * 10,  # Denormalizado
        min_denorm * 0.1,  # Denormalizado muy pequeño
    ]
    
    print(f"{'Valor':<15} {'Tipo':<20} {'Decodificado':<15}")
    print("-" * 50)
    
    for value in test_values:
        try:
            s, e, m = ieee.encode_normalized(value)
            tipo = "Normalizado"
        except ValueError:
            try:
                s, e, m = ieee.encode_denormalized(value)
                tipo = "Denormalizado"
            except ValueError:
                tipo = "Fuera de rango"
        
        decoded = ieee.decode(s, e, m)
        print(f"{value:<15.6e} {tipo:<20} {decoded:<15.6e}")


if __name__ == "__main__":
    demonstrate_ieee754()
    demonstrate_denormalized_vs_normalized()


# Alias para compatibilidad hacia atrás
IEEE754 = IEEE754Gen
