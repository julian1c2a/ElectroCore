"""
Módulo de Punto Fijo (Fixed-Point Arithmetic)

Implementa operaciones aritméticas con formato Q(E,F):
- E: bits para la parte entera
- F: bits para la parte fraccionaria
- Valor representado: M * B^(-F), donde M es el valor natural del registro

Ejemplos:
    - Q(8,8) en base 2: 16 bits total, 8 enteros, 8 fraccionarios
    - Q(10,6) en base 10: 16 dígitos total, 10 enteros, 6 fraccionarios
"""

from typing import Tuple, Union, Optional
from decimal import Decimal, getcontext
import math


# Configurar precisión decimal para cálculos exactos
getcontext().prec = 50


class FixedPoint:
    """
    Representación de números racionales en formato punto fijo Q(E,F).
    
    Atributos:
        E (int): Número de dígitos/bits para la parte entera
        F (int): Número de dígitos/bits para la parte fraccionaria
        B (int): Base numérica (por defecto 2 para binario)
        value (Decimal): Valor representado como número decimal
        raw_value (int): Valor interno (sin escalar) M
    
    Formato: Q(E, F)
    - Rango (positivos): [B^(-F), B^E - B^(-F)] ∪ {0}
    - Épsilon (mínimo representable): ε = B^(-F)
    - Máximo representable: M_max = B^E - B^(-F)
    """
    
    def __init__(self, E: int, F: int, B: int = 2, value: Union[float, int, Decimal, str] = 0):
        """
        Inicializar un número en formato punto fijo Q(E,F).
        
        Args:
            E: Número de posiciones para parte entera
            F: Número de posiciones para parte fraccionaria
            B: Base numérica (default 2 para binario)
            value: Valor a representar
        
        Raises:
            ValueError: Si E < 0, F < 0, B < 2, o si el valor no cabe en Q(E,F)
        """
        if E < 0 or F < 0:
            raise ValueError(f"E y F deben ser no-negativos. E={E}, F={F}")
        if B < 2:
            raise ValueError(f"Base B debe ser >= 2. B={B}")
        
        self.E = E
        self.F = F
        self.B = B
        self._quantization_step = Decimal(B) ** (-F)  # ε = B^(-F)
        self._max_representable = Decimal(B) ** E - self._quantization_step
        self._L = E + F  # Longitud total
        
        # Convertir y cuantizar el valor
        self.value = self._quantize(Decimal(str(value)))
        self.raw_value = self._get_raw_value()
    
    # ========== PROPIEDADES DE Q(E,F) ==========
    
    @property
    def epsilon(self) -> Decimal:
        """Épsilon: valor mínimo (no cero) representable en Q(E,F)."""
        return self._quantization_step
    
    @property
    def max_value(self) -> Decimal:
        """Valor máximo representable en Q(E,F)."""
        return self._max_representable
    
    @property
    def min_value(self) -> Decimal:
        """Valor mínimo representable en Q(E,F) (cero)."""
        return Decimal(0)
    
    @property
    def range(self) -> Tuple[Decimal, Decimal]:
        """Rango de valores representables [min, max]."""
        return (self.min_value, self.max_value)
    
    @property
    def length(self) -> int:
        """Longitud total del registro: L = E + F."""
        return self._L
    
    @property
    def max_raw_value(self) -> int:
        """Valor máximo del registro sin escalar (M_max = B^L - 1)."""
        return self.B ** self._L - 1
    
    # ========== MÉTODOS INTERNOS ==========
    
    def _quantize(self, value: Decimal) -> Decimal:
        """
        Cuantizar un valor a la precisión Q(E,F).
        
        Redondea hacia el múltiplo más cercano de epsilon = B^(-F).
        """
        if value < 0:
            raise ValueError(f"Solo se aceptan valores no-negativos. Recibido: {value}")
        
        # Redondear al múltiplo más cercano de epsilon
        quantized = (value / self.epsilon).quantize(Decimal(1)) * self.epsilon
        
        # Verificar que cabe en el rango
        if quantized > self.max_value:
            raise OverflowError(
                f"Valor {value} no cabe en Q({self.E},{self.F}) base {self.B}. "
                f"Máximo: {self.max_value}"
            )
        
        return quantized
    
    def _get_raw_value(self) -> int:
        """Obtener el valor interno M = value * B^F."""
        raw = (self.value * (Decimal(self.B) ** self.F)).to_integral_value()
        return int(raw)
    
    @staticmethod
    def _from_raw(E: int, F: int, B: int, raw_value: int) -> 'FixedPoint':
        """Crear FixedPoint directamente desde valor crudo M."""
        fp = FixedPoint.__new__(FixedPoint)
        fp.E = E
        fp.F = F
        fp.B = B
        fp._L = E + F
        fp._quantization_step = Decimal(B) ** (-F)
        fp._max_representable = Decimal(B) ** E - fp._quantization_step
        fp.raw_value = raw_value
        fp.value = Decimal(raw_value) * (Decimal(B) ** (-F))
        return fp
    
    # ========== OPERACIONES ARITMÉTICAS ==========
    
    def __add__(self, other: Union['FixedPoint', int, float]) -> 'FixedPoint':
        """
        Suma: (M1 + M2) * B^(-F)
        
        Ambos deben tener el mismo formato Q(E,F) y base B.
        """
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        
        if self.E != other.E or self.F != other.F or self.B != other.B:
            raise ValueError(
                f"Formatos incompatibles: Q({self.E},{self.F}){self.B} "
                f"+ Q({other.E},{other.F}){other.B}"
            )
        
        # Suma de valores crudos
        result_raw = self.raw_value + other.raw_value
        
        # Verificar overflow
        if result_raw > self.max_raw_value:
            raise OverflowError(
                f"Suma provoca overflow: {self.value} + {other.value} = "
                f"{Decimal(result_raw) * self._quantization_step} > {self.max_value}"
            )
        
        return FixedPoint._from_raw(self.E, self.F, self.B, result_raw)
    
    def __sub__(self, other: Union['FixedPoint', int, float]) -> 'FixedPoint':
        """
        Resta: (M1 - M2) * B^(-F)
        
        Nota: Si el resultado es negativo, se lanza excepción (solo positivos).
        """
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        
        if self.E != other.E or self.F != other.F or self.B != other.B:
            raise ValueError(
                f"Formatos incompatibles: Q({self.E},{self.F}){self.B} "
                f"- Q({other.E},{other.F}){other.B}"
            )
        
        result_raw = self.raw_value - other.raw_value
        
        if result_raw < 0:
            raise ValueError(
                f"Resta daría resultado negativo: {self.value} - {other.value} = "
                f"{Decimal(result_raw) * self._quantization_step}"
            )
        
        return FixedPoint._from_raw(self.E, self.F, self.B, result_raw)
    
    def __mul__(self, other: Union['FixedPoint', int, float]) -> 'FixedPoint':
        """
        Multiplicación con reescalado: (M1 * M2) / B^F
        
        Resultado en Q(E,F). El cálculo intermedio usa B^(2F).
        
        Fórmula:
            (M1 * B^(-F)) * (M2 * B^(-F)) = (M1 * M2) * B^(-2F)
            Reescalado: (M1 * M2) * B^(-F) / B^F = (M1 * M2) / B^F
        """
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        
        if self.E != other.E or self.F != other.F or self.B != other.B:
            raise ValueError(
                f"Formatos incompatibles: Q({self.E},{self.F}){self.B} "
                f"* Q({other.E},{other.F}){other.B}"
            )
        
        # Multiplicación de valores crudos
        product_raw = self.raw_value * other.raw_value
        
        # Reescalado: dividir por B^F
        result_raw = product_raw // (self.B ** self.F)
        
        # Verificar overflow
        if result_raw > self.max_raw_value:
            raise OverflowError(
                f"Multiplicación provoca overflow: {self.value} * {other.value} = "
                f"{Decimal(result_raw) * self._quantization_step} > {self.max_value}"
            )
        
        return FixedPoint._from_raw(self.E, self.F, self.B, result_raw)
    
    def __truediv__(self, other: Union['FixedPoint', int, float]) -> 'FixedPoint':
        """
        División con reescalado: (M1 / M2) * B^F
        
        Resultado en Q(E,F).
        
        Fórmula:
            (M1 * B^(-F)) / (M2 * B^(-F)) = M1 / M2
            Reescalado para mantener precisión: (M1 * B^F) / M2
        """
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        
        if self.E != other.E or self.F != other.F or self.B != other.B:
            raise ValueError(
                f"Formatos incompatibles: Q({self.E},{self.F}){self.B} "
                f"/ Q({other.E},{other.F}){other.B}"
            )
        
        if other.raw_value == 0:
            raise ZeroDivisionError("División por cero en punto fijo")
        
        # Reescalado: multiplicar por B^F antes de dividir
        numerator = self.raw_value * (self.B ** self.F)
        result_raw = numerator // other.raw_value
        
        # Verificar overflow
        if result_raw > self.max_raw_value:
            raise OverflowError(
                f"División provoca overflow: {self.value} / {other.value}"
            )
        
        return FixedPoint._from_raw(self.E, self.F, self.B, result_raw)
    
    # ========== COMPARACIÓN ==========
    
    def __eq__(self, other: Union['FixedPoint', int, float]) -> bool:
        """Igualdad exacta: comparar valores crudos."""
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        return self.raw_value == other.raw_value
    
    def __lt__(self, other: Union['FixedPoint', int, float]) -> bool:
        """Menor que: comparar valores crudos."""
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        return self.raw_value < other.raw_value
    
    def __le__(self, other: Union['FixedPoint', int, float]) -> bool:
        """Menor o igual que."""
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        return self.raw_value <= other.raw_value
    
    def __gt__(self, other: Union['FixedPoint', int, float]) -> bool:
        """Mayor que."""
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        return self.raw_value > other.raw_value
    
    def __ge__(self, other: Union['FixedPoint', int, float]) -> bool:
        """Mayor o igual que."""
        if isinstance(other, (int, float)):
            other = FixedPoint(self.E, self.F, self.B, other)
        return self.raw_value >= other.raw_value
    
    # ========== CONVERSIÓN A STRING ==========
    
    def __str__(self) -> str:
        """Representación en decimal."""
        return f"{self.value}"
    
    def __repr__(self) -> str:
        """Representación completa."""
        return f"Q({self.E},{self.F})₍{self.B}₎[{self.value}]"
    
    def to_binary(self) -> str:
        """Convertir valor crudo a representación binaria."""
        if self.B != 2:
            raise ValueError(f"to_binary() solo válido para base 2. Base actual: {self.B}")
        return bin(self.raw_value)
    
    def to_hex(self) -> str:
        """Convertir valor crudo a representación hexadecimal."""
        if self.B != 2:
            raise ValueError(f"to_hex() solo válido para base 2. Base actual: {self.B}")
        return hex(self.raw_value)
    
    # ========== INFORMACIÓN Y ESTADÍSTICAS ==========
    
    def info(self) -> str:
        """Información detallada del número Q(E,F)."""
        lines = [
            f"Formato: Q({self.E},{self.F}) base {self.B}",
            f"Longitud total: L = E + F = {self._L} dígitos",
            f"Valor: {self.value}",
            f"Valor crudo: M = {self.raw_value}",
            f"Épsilon (mínimo no-cero): ε = {self.epsilon}",
            f"Máximo representable: {self.max_value}",
            f"Rango: [{self.min_value}, {self.max_value}]",
            f"Eficacia: 100% (sin representaciones repetidas)",
        ]
        if self.B == 2:
            lines.append(f"Binario: {self.to_binary()}")
            lines.append(f"Hexadecimal: {self.to_hex()}")
        return "\n".join(lines)
    
    @staticmethod
    def format_info(E: int, F: int, B: int = 2) -> str:
        """
        Información sobre un formato Q(E,F) sin crear una instancia.
        
        Useful para ver propiedades del formato sin un valor específico.
        """
        epsilon = Decimal(B) ** (-F)
        max_val = Decimal(B) ** E - epsilon
        L = E + F
        
        lines = [
            f"═══════════════════════════════════════",
            f"FORMATO Q({E},{F}) BASE {B}",
            f"═══════════════════════════════════════",
            f"Longitud total: L = {E} + {F} = {L} dígitos",
            f"Rango de valores: [0, {max_val}]",
            f"Épsilon (precisión): ε = {B}^(-{F}) = {epsilon}",
            f"Número máximo: {max_val}",
            f"Máximo valor crudo: M_max = {B}^{L} - 1 = {B**L - 1}",
            f"Eficacia: 100%",
            f"═══════════════════════════════════════",
        ]
        return "\n".join(lines)


# ========== FUNCIONES AUXILIARES ==========

def create_fixed_point(E: int, F: int, B: int = 2) -> dict:
    """
    Crear un diccionario con propiedades de Q(E,F).
    
    Útil para comparar diferentes formatos sin crear instancias.
    """
    epsilon = Decimal(B) ** (-F)
    max_val = Decimal(B) ** E - epsilon
    
    return {
        'format': f"Q({E},{F})",
        'base': B,
        'E': E,
        'F': F,
        'L': E + F,
        'epsilon': float(epsilon),
        'max_value': float(max_val),
        'min_value': 0.0,
        'max_raw_value': B ** (E + F) - 1,
    }


def compare_formats(*formats: Tuple[int, int, int]) -> None:
    """
    Comparar múltiples formatos Q(E,F).
    
    Args:
        *formats: Tuplas (E, F, B) para comparar
    
    Ejemplo:
        compare_formats((4, 4, 2), (8, 8, 2), (10, 6, 2))
    """
    import pandas as pd
    
    data = []
    for fmt in formats:
        E, F, B = fmt if len(fmt) == 3 else (fmt[0], fmt[1], 2)
        info = create_fixed_point(E, F, B)
        data.append(info)
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))


if __name__ == "__main__":
    # Demostración básica
    print(FixedPoint.format_info(8, 8))
    print("\n" + FixedPoint.format_info(16, 16))
    print("\n" + FixedPoint.format_info(10, 6, B=10))
