"""
FixedPointUnified: Clase unificada para punto fijo (sin signo, M&S, complemento).

Reemplaza las 3 clases anteriores (FixedPoint, FixedPointSignedMS, FixedPointSignedComplement)
con una interfaz única y flexible.

Parámetros:
- E: bits enteros
- F: bits fraccionarios
- base: base numérica (2, 8, 10, 16, ...)
- signed: bool - ¿Es representación con signo?
- representation: str - 'ms' (magnitud-signo) o 'complement' (complemento a base)

Ejemplo:
    >>> # Sin signo
    >>> fp = FixedPointUnified(E=4, F=4, base=2, signed=False)
    >>> fp.encode(5.25)
    84
    >>> fp.decode(84)
    5.25
    
    >>> # Con signo (complemento) - RECOMENDADO
    >>> fp = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')
    >>> fp.encode(5.25)
    84
    >>> fp.encode(-5.25)
    428
    >>> fp.decode(428)
    -5.25
"""

from dataclasses import dataclass
from typing import Union, Tuple
import math


@dataclass
class FixedPointConfig:
    """Configuración de punto fijo."""
    E: int  # bits enteros
    F: int  # bits fraccionarios
    base: int = 2
    signed: bool = False
    representation: str = 'complement'  # 'ms' o 'complement'
    
    def __post_init__(self):
        if self.E <= 0 or self.F < 0:
            raise ValueError(f"E debe ser > 0, F debe ser >= 0. Got E={self.E}, F={self.F}")
        if self.base < 2:
            raise ValueError(f"base debe ser >= 2. Got {self.base}")
        if self.signed and self.representation not in ('ms', 'complement'):
            raise ValueError(f"representation debe ser 'ms' o 'complement'. Got {self.representation}")


class FixedPointUnified:
    """
    Clase unificada para punto fijo con cualquier configuración.
    
    Soporta:
    - Punto fijo sin signo: [0, B^E)
    - Punto fijo con signo M&S: ±(B^E - ε)
    - Punto fijo con signo complemento: [-B^E, B^E - ε]
    """
    
    def __init__(self, E: int, F: int, base: int = 2, 
                 signed: bool = False, representation: str = 'complement'):
        """
        Inicializar punto fijo unificado.
        
        Args:
            E: bits enteros
            F: bits fraccionarios
            base: base numérica (2, 8, 10, 16, ...)
            signed: ¿Es con signo?
            representation: 'ms' (magnitud-signo) o 'complement' (complemento a base)
        """
        self.config = FixedPointConfig(E, F, base, signed, representation)
        self.E = E
        self.F = F
        self.base = base
        self.signed = signed
        self.representation = representation
        
        # Precalcular valores importantes
        self.epsilon = self.base ** (-F)  # Resolución mínima
        self.base_power_E = self.base ** E
        self.base_power_F = self.base ** F
        self.total_bits = E + F + (1 if signed else 0)
        
        # Calcular rango
        if not signed:
            self.min_value = 0
            self.max_value = self.base_power_E - self.epsilon
        elif representation == 'ms':
            self.min_value = -(self.base_power_E - self.epsilon)
            self.max_value = self.base_power_E - self.epsilon
        else:  # complemento
            self.min_value = -self.base_power_E
            self.max_value = self.base_power_E - self.epsilon
    
    def encode(self, value: float) -> int:
        """
        Codifica un valor decimal a su representación interna.
        
        Args:
            value: valor decimal a codificar
            
        Returns:
            representación interna (raw_value)
            
        Raises:
            ValueError: si el valor está fuera de rango
        """
        # Validar rango
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Valor {value} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        if not self.signed:
            # Punto fijo sin signo: raw = value * base^F
            raw = int(round(value * self.base_power_F))
            return raw
        
        # Punto fijo con signo: primero convertir a magnitud
        sign = 1 if value >= 0 else -1
        abs_value = abs(value)
        magnitude = int(round(abs_value * self.base_power_F))
        
        if self.representation == 'ms':
            # Magnitud y signo: MSB = signo
            max_magnitude = int(self.base_power_E * self.base_power_F)
            if magnitude > max_magnitude:
                raise ValueError(f"Magnitud fuera de rango: {magnitude} > {max_magnitude}")
            
            if sign == 1:
                return magnitude
            else:
                return (1 << self.total_bits) - magnitude - 1 + 1  # Complemento en signo
        
        else:  # complemento a base
            # Complemento a base: rango [-B^E, B^E)
            max_positive = int(self.base_power_E * self.base_power_F)
            
            if sign == 1:
                return magnitude
            else:
                # Negativo: complemento a base
                # -x se representa como base^(E+F) - magnitude
                complement = (self.base ** (self.E + self.F)) - magnitude
                return complement
    
    def decode(self, raw_value: int) -> float:
        """
        Decodifica una representación interna a valor decimal.
        
        Args:
            raw_value: representación interna
            
        Returns:
            valor decimal
        """
        if not self.signed:
            # Sin signo: directo
            return raw_value / self.base_power_F
        
        # Con signo: detectar signo según representación
        max_positive = int(self.base_power_E * self.base_power_F)
        
        if self.representation == 'ms':
            # Magnitud y signo: si raw > max_positive, es negativo
            if raw_value <= max_positive:
                return raw_value / self.base_power_F
            else:
                # Negativo
                magnitude = ((1 << self.total_bits) - raw_value - 1 + 1)
                return -magnitude / self.base_power_F
        
        else:  # complemento a base
            # Complemento a base: si raw > max_positive, es negativo
            if raw_value <= max_positive:
                return raw_value / self.base_power_F
            else:
                # Negativo: complemento a base
                magnitude = (self.base ** (self.E + self.F)) - raw_value
                return -magnitude / self.base_power_F
    
    def add(self, a: float, b: float) -> float:
        """
        Suma dos números en punto fijo.
        
        Args:
            a, b: operandos
            
        Returns:
            a + b
            
        Raises:
            ValueError: si el resultado desborda
        """
        result = a + b
        
        # Validar rango
        if result < self.min_value or result > self.max_value:
            raise ValueError(
                f"Resultado {result} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        # Codificar → decodificar para simular hardware
        M_a = self.encode(a)
        M_b = self.encode(b)
        M_result = M_a + M_b
        
        # Manejar overflow (complemento a base)
        max_raw = (1 << (self.E + self.F + (1 if self.signed else 0))) - 1
        if M_result > max_raw:
            M_result = M_result & ((1 << (self.E + self.F + (1 if self.signed else 0))) - 1)
        
        return self.decode(M_result)
    
    def subtract(self, a: float, b: float) -> float:
        """
        Resta dos números en punto fijo.
        
        Args:
            a, b: operandos
            
        Returns:
            a - b
        """
        return self.add(a, -b)
    
    def multiply(self, a: float, b: float) -> float:
        """
        Multiplica dos números en punto fijo.
        
        Args:
            a, b: operandos
            
        Returns:
            a * b
            
        Raises:
            ValueError: si el resultado desborda
        """
        result = a * b
        
        # Validar rango
        if result < self.min_value or result > self.max_value:
            raise ValueError(
                f"Resultado {result} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        return result
    
    def divide(self, a: float, b: float) -> float:
        """
        Divide dos números en punto fijo.
        
        Args:
            a, b: operandos (b != 0)
            
        Returns:
            a / b
            
        Raises:
            ValueError: si b == 0 o resultado desborda
        """
        if b == 0:
            raise ValueError("División por cero")
        
        result = a / b
        
        # Validar rango
        if result < self.min_value or result > self.max_value:
            raise ValueError(
                f"Resultado {result} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        return result
    
    def error_absolute(self, true_value: float) -> float:
        """Error absoluto de representación."""
        encoded = self.encode(true_value)
        decoded = self.decode(encoded)
        return abs(true_value - decoded)
    
    def error_relative(self, true_value: float) -> float:
        """Error relativo de representación."""
        if true_value == 0:
            return 0.0
        return self.error_absolute(true_value) / abs(true_value)
    
    def __repr__(self) -> str:
        signed_str = f"signed={self.representation}" if self.signed else "unsigned"
        return (
            f"FixedPointUnified(E={self.E}, F={self.F}, base={self.base}, "
            f"{signed_str}, range=[{self.min_value}, {self.max_value}])"
        )
    
    def info(self) -> str:
        """Información detallada sobre la configuración."""
        lines = [
            f"FixedPointUnified Q({self.E},{self.F}) Base {self.base}",
            f"{'='*50}",
            f"Tipo: {'Con signo (' + self.representation + ')' if self.signed else 'Sin signo'}",
            f"Total bits: {self.total_bits}",
            f"Rango: [{self.min_value}, {self.max_value}]",
            f"Epsilon (resolución): {self.epsilon}",
            f"Valor máximo positivo: {self.max_value}",
            f"Valor mínimo: {self.min_value}",
        ]
        return "\n".join(lines)


# Funciones auxiliares para compatibilidad con versiones heredadas
def from_fixedpoint(fp_old) -> FixedPointUnified:
    """Crea FixedPointUnified desde FixedPoint (sin signo)."""
    return FixedPointUnified(
        E=fp_old.E,
        F=fp_old.F,
        base=fp_old.B,
        signed=False
    )


def from_fixedpoint_signed_ms(fp_old) -> FixedPointUnified:
    """Crea FixedPointUnified desde FixedPointSignedMS."""
    return FixedPointUnified(
        E=fp_old.E,
        F=fp_old.F,
        base=fp_old.base,
        signed=True,
        representation='ms'
    )


def from_fixedpoint_signed_complement(fp_old) -> FixedPointUnified:
    """Crea FixedPointUnified desde FixedPointSignedComplement."""
    return FixedPointUnified(
        E=fp_old.E,
        F=fp_old.F,
        base=fp_old.base,
        signed=True,
        representation='complement'
    )
