"""
Punto Fijo con Signo y Parte Fraccionaria - Q(E,F) Signed

Dos representaciones:
1. Magnitud y Signo (M&S):
   - MSD (dígito más significativo) es el signo: 0=+ , 1..B-1=-
   - Resto: magnitud del número
   - Rango: [-B^E + B^(-F), B^E - B^(-F)]
   - Nota: Cero tiene dos representaciones (+0 y -0)

2. Complemento a la Base (B's Complement):
   - Para positivos: representación directa
   - Para negativos: B^(E+F) + valor (complemento)
   - Rango: [-B^E, B^E - B^(-F)]
   - Números más negativo: -B^E
   - Nota: Cero tiene una única representación
"""

from decimal import Decimal
from typing import Tuple
import math


class FixedPointSignedMS:
    """Punto fijo con signo usando Magnitud y Signo (M&S)."""
    
    def __init__(self, E: int, F: int, base: int = 2):
        """
        Crear punto fijo con signo M&S.
        
        Args:
            E: bits/dígitos para parte entera
            F: bits/dígitos para parte fraccionaria
            base: base numérica (2, 8, 10, 16, etc.)
        """
        self.E = E
        self.F = F
        self.base = base
        self.total_bits = E + F + 1  # +1 para el signo
        
        # Propiedades
        self.epsilon = Decimal(base) ** (-F)  # Precisión
        self.max_value = Decimal(base) ** E - self.epsilon  # Máximo positivo
        self.min_value = -(Decimal(base) ** E - self.epsilon)  # Mínimo (más negativo)
        
    def __repr__(self) -> str:
        return f"Q({self.E},{self.F})_signed_MS base {self.base}"
    
    @property
    def info(self) -> dict:
        """Información de la representación."""
        return {
            'E': self.E,
            'F': self.F,
            'base': self.base,
            'total_bits': self.total_bits,
            'epsilon': float(self.epsilon),
            'max_value': float(self.max_value),
            'min_value': float(self.min_value),
            'representable_values': float(self.base ** self.total_bits)
        }
    
    def encode(self, value: float) -> int:
        """
        Codificar un número decimal a M&S.
        
        Format: [S][E dígitos enteros][F dígitos fraccionarios]
        S: signo (0=+, 1 a base-1 = -)
        
        Args:
            value: número decimal a codificar
            
        Returns:
            M: valor codificado (entero)
        """
        # Validar rango
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Valor {value} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        # Extraer signo y magnitud
        if value >= 0:
            sign_digit = 0
            magnitude = value
        else:
            sign_digit = 1  # o cualquier dígito 1..base-1
            magnitude = -value
        
        # Magnitud en Q(E,F)
        m = Decimal(str(magnitude)) * Decimal(self.base) ** self.F
        m_int = int(m)
        
        # Ensamblar: [S][Magnitud]
        # El signo ocupa el dígito más significativo
        M = sign_digit * (self.base ** (self.E + self.F)) + m_int
        
        return M
    
    def decode(self, M: int) -> float:
        """
        Decodificar desde M&S a número decimal.
        
        Args:
            M: valor codificado
            
        Returns:
            valor decimal
        """
        # Extraer signo
        sign_digit = M // (self.base ** (self.E + self.F))
        
        if sign_digit == 0:
            sign = 1
        else:
            sign = -1
        
        # Extraer magnitud
        magnitude_m = M % (self.base ** (self.E + self.F))
        value = Decimal(magnitude_m) * Decimal(self.base) ** (-self.F)
        
        return float(sign * value)
    
    def add(self, v1: float, v2: float) -> float:
        """Suma con punto fijo con signo."""
        return v1 + v2
    
    def subtract(self, v1: float, v2: float) -> float:
        """Resta con punto fijo con signo."""
        return v1 - v2
    
    def multiply(self, v1: float, v2: float) -> float:
        """Multiplicación con punto fijo con signo."""
        result = v1 * v2
        # Reescalar si es necesario
        return result
    
    def divide(self, v1: float, v2: float) -> float:
        """División con punto fijo con signo."""
        if v2 == 0:
            raise ValueError("División por cero")
        return v1 / v2


class FixedPointSignedComplement:
    """Punto fijo con signo usando Complemento a la Base."""
    
    def __init__(self, E: int, F: int, base: int = 2):
        """
        Crear punto fijo con signo usando complemento a base.
        
        Args:
            E: bits/dígitos para parte entera
            F: bits/dígitos para parte fraccionaria
            base: base numérica (2, 8, 10, 16, etc.)
        """
        self.E = E
        self.F = F
        self.base = base
        self.total_bits = E + F + 1  # +1 para el signo
        
        # Propiedades
        self.epsilon = Decimal(base) ** (-F)  # Precisión
        self.max_value = Decimal(base) ** E - self.epsilon  # Máximo positivo
        self.min_value = -Decimal(base) ** E  # Mínimo (más negativo)
        self.modulo = Decimal(base) ** (E + F + 1)  # Para complemento
        
    def __repr__(self) -> str:
        return f"Q({self.E},{self.F})_signed_complement base {self.base}"
    
    @property
    def info(self) -> dict:
        """Información de la representación."""
        return {
            'E': self.E,
            'F': self.F,
            'base': self.base,
            'total_bits': self.total_bits,
            'epsilon': float(self.epsilon),
            'max_value': float(self.max_value),
            'min_value': float(self.min_value),
            'representable_values': float(self.base ** self.total_bits),
            'modulo': float(self.modulo)
        }
    
    def encode(self, value: float) -> int:
        """
        Codificar un número decimal a complemento a base.
        
        Para positivos (value >= 0):
            M = value × base^F
        Para negativos (value < 0):
            M = base^(E+F+1) + value × base^F
        
        Args:
            value: número decimal a codificar
            
        Returns:
            M: valor codificado (entero)
        """
        # Validar rango
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Valor {value} fuera de rango [{self.min_value}, {self.max_value}]"
            )
        
        m = Decimal(str(value)) * Decimal(self.base) ** self.F
        m_int = int(m)
        
        if value < 0:
            # Complemento: M = modulo + m_int
            M = int(self.modulo) + m_int
        else:
            M = m_int
        
        return M
    
    def decode(self, M: int) -> float:
        """
        Decodificar desde complemento a base a número decimal.
        
        Args:
            M: valor codificado
            
        Returns:
            valor decimal
        """
        # Si M >= modulo/2, es negativo
        half_modulo = int(self.modulo) // 2
        
        if M >= half_modulo:
            # Es negativo: restar modulo
            m_int = M - int(self.modulo)
        else:
            m_int = M
        
        value = Decimal(m_int) * Decimal(self.base) ** (-self.F)
        return float(value)
    
    def add(self, v1: float, v2: float) -> float:
        """Suma con complemento a base."""
        # En complemento a base, suma es suma directa (módulo automático)
        result = v1 + v2
        
        # Si excede rango, wrapping ocurre automáticamente en la aritmética modular
        return result
    
    def subtract(self, v1: float, v2: float) -> float:
        """Resta con complemento a base."""
        return v1 - v2
    
    def multiply(self, v1: float, v2: float) -> float:
        """Multiplicación con complemento a base."""
        return v1 * v2
    
    def divide(self, v1: float, v2: float) -> float:
        """División con complemento a base."""
        if v2 == 0:
            raise ValueError("División por cero")
        return v1 / v2
    
    def complement(self, M: int) -> int:
        """
        Calcular complemento de un número en la representación.
        Para negación de un número.
        
        Args:
            M: valor codificado
            
        Returns:
            complemento de M
        """
        return (int(self.modulo) - M) % int(self.modulo)


def demonstrate_ms():
    """Demostración de Magnitud y Signo."""
    print("\n" + "="*80)
    print("MAGNITUD Y SIGNO (M&S)")
    print("="*80)
    
    fp = FixedPointSignedMS(E=4, F=4, base=2)
    print(f"\nRepresentación: {fp}")
    print(f"Total bits: {fp.total_bits}")
    print(f"Rango: [{fp.min_value}, {fp.max_value}]")
    print(f"Precisión (ε): {fp.epsilon}")
    
    # Ejemplos
    print("\n--- Codificación ---")
    examples = [5.25, -5.25, 0, -0.5, 7.9375, -7.9375]
    
    for value in examples:
        try:
            M = fp.encode(value)
            decoded = fp.decode(M)
            print(f"  Valor: {value:7.4f} → M: {M:4d} → Decodificado: {decoded:7.4f}")
        except ValueError as e:
            print(f"  Valor: {value:7.4f} → ERROR: {e}")
    
    # Operaciones
    print("\n--- Operaciones ---")
    v1, v2 = 3.5, 2.25
    print(f"  {v1} + {v2} = {fp.add(v1, v2)}")
    print(f"  {v1} - {v2} = {fp.subtract(v1, v2)}")
    print(f"  {-v1} + {v2} = {fp.add(-v1, v2)}")
    print(f"  {-v1} - {v2} = {fp.subtract(-v1, v2)}")


def demonstrate_complement():
    """Demostración de Complemento a Base."""
    print("\n" + "="*80)
    print("COMPLEMENTO A LA BASE")
    print("="*80)
    
    fp = FixedPointSignedComplement(E=4, F=4, base=2)
    print(f"\nRepresentacion: {fp}")
    print(f"Total bits: {fp.total_bits}")
    print(f"Rango: [{fp.min_value}, {fp.max_value}]")
    print(f"Precision (eps): {fp.epsilon}")
    print(f"Modulo: {fp.modulo} (= {fp.base}^{fp.E + fp.F + 1})")
    
    # Ejemplos
    print("\n--- Codificación ---")
    examples = [5.25, -5.25, 0, -0.5, 7.9375, -8.0, 7.9375]
    
    for value in examples:
        try:
            M = fp.encode(value)
            decoded = fp.decode(M)
            print(f"  Valor: {value:7.4f} → M: {M:4d} → Decodificado: {decoded:7.4f}")
        except ValueError as e:
            print(f"  Valor: {value:7.4f} → ERROR: {e}")
    
    # Operaciones
    print("\n--- Operaciones ---")
    v1, v2 = 3.5, 2.25
    print(f"  {v1} + {v2} = {fp.add(v1, v2)}")
    print(f"  {v1} - {v2} = {fp.subtract(v1, v2)}")
    print(f"  {-v1} + {v2} = {fp.add(-v1, v2)}")
    print(f"  {-v1} - {v2} = {fp.subtract(-v1, v2)}")
    
    # Complemento
    print("\n--- Complemento (Negación) ---")
    for value in [5.25, -5.25, 0]:
        try:
            M = fp.encode(value)
            M_comp = fp.complement(M)
            value_comp = fp.decode(M_comp)
            print(f"  ~({value:7.4f}) → M:{M:4d} → M_comp:{M_comp:4d} → {value_comp:7.4f}")
        except ValueError as e:
            print(f"  Valor: {value} → ERROR: {e}")


def compare_representations():
    """Comparar M&S vs Complemento."""
    print("\n" + "="*80)
    print("COMPARACION: M&S vs COMPLEMENTO A BASE")
    print("="*80)
    
    ms = FixedPointSignedMS(E=3, F=2, base=2)
    comp = FixedPointSignedComplement(E=3, F=2, base=2)
    
    print(f"\nM&S:        {ms}")
    print(f"Rango M&S:  [{ms.min_value}, {ms.max_value}]")
    
    print(f"\nComplemento: {comp}")
    print(f"Rango Comp:  [{comp.min_value}, {comp.max_value}]")
    
    print("\n--- Tabla de Codificaciones ---")
    print(f"{'Valor':<8} {'M&S':<6} {'Comp':<6} {'Notas':<30}")
    print("-" * 50)
    
    test_values = [-4.0, -3.75, -3.5, -3.25, -3.0, -2.75, -0.25, 0, 0.25, 2.75, 3.0, 3.25, 3.5, 3.75]
    
    for value in test_values:
        try:
            m_ms = ms.encode(value)
            m_comp = comp.encode(value)
            note = ""
            if value == 0:
                note = "Cero (único en comp, dual en MS)"
            elif value == comp.min_value:
                note = "Mínimo en complemento"
            print(f"{value:<8.2f} {m_ms:<6d} {m_comp:<6d} {note:<30}")
        except ValueError:
            note = "Fuera de rango"
            try:
                m_ms = ms.encode(value)
                print(f"{value:<8.2f} {m_ms:<6d} {'N/A':<6} {note:<30}")
            except:
                try:
                    m_comp = comp.encode(value)
                    print(f"{value:<8.2f} {'N/A':<6} {m_comp:<6d} {note:<30}")
                except:
                    pass


if __name__ == "__main__":
    demonstrate_ms()
    demonstrate_complement()
    compare_representations()
