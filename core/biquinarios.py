"""
Códigos Biquinarios (Biquinary Codes)

DIFERENCIA CRÍTICA CON "2 ENTRE 5":
- "2 entre 5" (5421 code): código de peso, representa dígitos 0-9 directamente
- Biquinarios: separación en dos componentes: quinaria (×5) + binaria (×1)
  Representa un dígito decimal en dos grupos: grupo de 5 + grupo de 2

Implementaciones históricas de biquinarios:
1. 7 bits (2-5-4-2-1-0-0): IBM 650 y otras computadoras clásicas - IMPLEMENTADO
2. 5 bits (Univac 60, Univac 120 / Remington Rand) - IMPLEMENTADO
3. IBM 1401 (adaptada al hardware de 6 bits)
4. FACOM 128 (variante japonesa de 7 bits)

ESTRUCTURA TÍPICA 7 BITS:
- Bits 0-2: componente quinaria (cinco valores: 0,0; 0,1; 1,0; 1,1; ? - solo 5 usados)
- Bits 3-6: componente binaria (dos bits: 00, 01, 10, 11)
- Total: 5 × 2 = 10 combinaciones (0-9)

Ventaja: Detección de errores simple (comprobar paridad de cada grupo)
Desventaja: Menos eficiente que BCD (usa 7 bits para 10 valores, BCD usa 4)
"""

from typing import List, Tuple, Dict


class BiquinaryGen:
    """
    Código biquinario genérico.
    
    Separación en dos componentes: quinaria (selecciona grupo) + binaria (selecciona dentro del grupo).
    
    Parámetros:
    - total_bits: bits totales del código
    - quinaria_bits: bits para componente quinaria
    - binaria_bits: bits para componente binaria
    """
    
    def __init__(self, total_bits: int, quinaria_bits: int, binaria_bits: int, 
                 encode_table: Dict[int, Tuple[int, int]]):
        """
        Crear código biquinario genérico.
        
        Args:
            total_bits: bits totales (quinaria + binaria + relleno)
            quinaria_bits: bits para componente quinaria
            binaria_bits: bits para componente binaria
            encode_table: diccionario {dígito: (quinaria, binaria)}
        """
        self.total_bits = total_bits
        self.quinaria_bits = quinaria_bits
        self.binaria_bits = binaria_bits
        self.encode_table = encode_table
        self.decode_table = {v: k for k, v in encode_table.items()}
        
        # Máscaras
        self.quinaria_mask = (1 << quinaria_bits) - 1
        self.binaria_mask = (1 << binaria_bits) - 1
    
    def encode(self, digit: int) -> int:
        """
        Codificar dígito a biquinario.
        
        Returns:
            Código empaquetado en total_bits
        """
        if not 0 <= digit <= 9:
            raise ValueError(f"Dígito debe estar en [0,9], recibido {digit}")
        
        if digit not in self.encode_table:
            raise ValueError(f"Dígito {digit} no está en tabla de codificación")
        
        quinaria, binaria = self.encode_table[digit]
        
        # Empaquetar: [relleno][binaria][quinaria]
        code = (quinaria & self.quinaria_mask) | ((binaria & self.binaria_mask) << self.quinaria_bits)
        
        return code
    
    def decode(self, code: int) -> int:
        """Decodificar desde biquinario a dígito."""
        quinaria = code & self.quinaria_mask
        binaria = (code >> self.quinaria_bits) & self.binaria_mask
        
        key = (quinaria, binaria)
        if key not in self.decode_table:
            raise ValueError(f"Código biquinario inválido: {code:0{self.total_bits}b}")
        
        return self.decode_table[key]
    
    def encode_number(self, number: str) -> List[int]:
        """Codificar número (string de dígitos) a biquinario."""
        return [self.encode(int(d)) for d in number]
    
    def decode_number(self, codes: List[int]) -> str:
        """Decodificar lista de códigos biquinarios a número."""
        return ''.join(str(self.decode(c)) for c in codes)
    
    def __repr__(self) -> str:
        return f"BiquinaryGen(total_bits={self.total_bits}, quinaria={self.quinaria_bits}, binaria={self.binaria_bits})"


class Biquinary7Bit(BiquinaryGen):
    """Código biquinario de 7 bits (IBM 650 style)."""
    
    def __init__(self):
        """
        Estructura: [quinaria (3 bits)][binaria (2 bits)][relleno (2 bits)]
        Quinaria: selecciona 0-4 o 5-9
        Binaria: selecciona dentro del grupo (0-1 o 0-4)
        """
        # Tabla de codificación biquinaria 7 bits
        # Formato: dígito → (quinaria, binaria)
        encode_table = {
            0: (0b00, 0b01),  # Quinaria 00 (0-4), Binaria 01 → 0
            1: (0b00, 0b10),  # Quinaria 00 (0-4), Binaria 10 → 1
            2: (0b01, 0b01),  # Quinaria 01 (0-4), Binaria 01 → 2
            3: (0b01, 0b10),  # Quinaria 01 (0-4), Binaria 10 → 3
            4: (0b10, 0b01),  # Quinaria 10 (0-4), Binaria 01 → 4
            5: (0b10, 0b10),  # Quinaria 10 (5-9), Binaria 10 → 5
            6: (0b11, 0b01),  # Quinaria 11 (5-9), Binaria 01 → 6
            7: (0b11, 0b10),  # Quinaria 11 (5-9), Binaria 10 → 7
            8: (0b100, 0b01), # Quinaria 100 (5-9), Binaria 01 → 8
            9: (0b100, 0b10), # Quinaria 100 (5-9), Binaria 10 → 9
        }
        
        super().__init__(total_bits=7, quinaria_bits=3, binaria_bits=2, encode_table=encode_table)
    
    def __repr__(self) -> str:
        return "Biquinary7Bit(IBM 650 style)"


class Biquinary5Bit(BiquinaryGen):
    """Código biquinario de 5 bits (Univac 60/120 style)."""
    
    def __init__(self):
        """
        Estructura: [quinaria (2 bits)][binaria (3 bits)]
        Más compacto que 7 bits.
        """
        # Tabla de codificación biquinaria 5 bits
        # Quinaria: 2 bits (00, 01, 10, 11) - solo 3-4 usados para 0-4 y 5-9
        # Binaria: 3 bits para seleccionar dentro del grupo
        
        encode_table = {
            0: (0b00, 0b001),  # Grupo 0-4, posición 0
            1: (0b00, 0b010),  # Grupo 0-4, posición 1
            2: (0b00, 0b100),  # Grupo 0-4, posición 2
            3: (0b01, 0b001),  # Grupo 0-4, posición 3
            4: (0b01, 0b010),  # Grupo 0-4, posición 4
            5: (0b10, 0b001),  # Grupo 5-9, posición 0
            6: (0b10, 0b010),  # Grupo 5-9, posición 1
            7: (0b10, 0b100),  # Grupo 5-9, posición 2
            8: (0b11, 0b001),  # Grupo 5-9, posición 3
            9: (0b11, 0b010),  # Grupo 5-9, posición 4
        }
        
        super().__init__(total_bits=5, quinaria_bits=2, binaria_bits=3, encode_table=encode_table)
    
    
    def encode(self, digit: int) -> int:
        """
        Codificar dígito a biquinario 5 bits.
        
        Returns:
            5 bits: [quinaria(2)][binaria(3)]
        """
        if not 0 <= digit <= 9:
            raise ValueError(f"Dígito debe estar en [0,9], recibido {digit}")
        
        quinaria, binaria = self.encode_table[digit]
        
        # Empaquetar en 5 bits
        code = (binaria & 0b111) | ((quinaria & 0b11) << 3)
        
        return code
    
    def decode(self, code: int) -> int:
        """Decodificar desde biquinario 5 bits a dígito."""
        binaria = code & 0b111
        quinaria = (code >> 3) & 0b11
        
        key = (quinaria, binaria)
        if key not in self.decode_table:
            raise ValueError(f"Código biquinario inválido: {code:05b}")
        
        return self.decode_table[key]
    
    def encode_number(self, number: str) -> List[int]:
        """Codificar número (string de dígitos) a biquinario 5 bits."""
        return [self.encode(int(d)) for d in number]
    
    def decode_number(self, codes: List[int]) -> str:
        """Decodificar lista de códigos biquinarios a número."""
        return ''.join(str(self.decode(c)) for c in codes)
    
    def __repr__(self) -> str:
        return "Biquinary5Bit(Univac 60/120 style)"


class Biquinary6Bit(BiquinaryGen):
    """Código biquinario de 6 bits (IBM 1401 style)."""
    
    def __init__(self):
        """
        Estructura: [relleno (1 bit)][quinaria (2 bits)][binaria (3 bits)]
        Variante de 6 bits para máquinas de 6 bits.
        """
        encode_table = {
            0: (0b00, 0b001),
            1: (0b00, 0b010),
            2: (0b00, 0b100),
            3: (0b01, 0b001),
            4: (0b01, 0b010),
            5: (0b10, 0b001),
            6: (0b10, 0b010),
            7: (0b10, 0b100),
            8: (0b11, 0b001),
            9: (0b11, 0b010),
        }
        
        super().__init__(total_bits=6, quinaria_bits=2, binaria_bits=3, encode_table=encode_table)
    
    def encode(self, digit: int) -> int:
        """Codificar dígito a biquinario 6 bits."""
        if not 0 <= digit <= 9:
            raise ValueError(f"Dígito debe estar en [0,9], recibido {digit}")
        
        quinaria, binaria = self.encode_table[digit]
        code = (binaria & 0b111) | ((quinaria & 0b11) << 3)
        return code
    
    def decode(self, code: int) -> int:
        """Decodificar desde biquinario 6 bits a dígito."""
        binaria = code & 0b111
        quinaria = (code >> 3) & 0b11
        
        key = (quinaria, binaria)
        if key not in self.decode_table:
            raise ValueError(f"Código biquinario inválido: {code:06b}")
        
        return self.decode_table[key]
    
    def __repr__(self) -> str:
        return "Biquinary6Bit(IBM 1401 style)"


def demonstrate_biquinary7():
    """Demostración de biquinario 7 bits."""
    print("\n" + "="*80)
    print("BIQUINARIO 7 BITS (IBM 650 style)")
    print("="*80)
    
    bq = Biquinary7Bit()
    
    print(f"\nRepresentación: {bq}")
    print(f"Total bits: 7 (3 quinaria + 2 binaria + 2 relleno)")
    print(f"Valores representables: 10 (0-9)")
    print(f"Eficiencia: log_2(10) / 7 ~ 0.427 bits por digito")
    
    print(f"\n--- TABLA DE CODIFICACION ---")
    print(f"{'Dígito':<8} {'Quinar':<8} {'Binar':<8} {'Código 7-bit':<20}")
    print("-" * 45)
    
    for d in range(10):
        code = bq.encode(d)
        q, b = bq.encode_table[d]
        print(f"{d:<8} {q:03b}      {b:02b}      {code:07b}")
    
    print(f"\n--- CODIFICACION DE NUMEROS ---")
    test_numbers = ["12345", "67890", "31415"]
    
    for num in test_numbers:
        codes = bq.encode_number(num)
        decoded = bq.decode_number(codes)
        codes_bin = ' '.join(f"{c:07b}" for c in codes)
        print(f"\n{num}:")
        print(f"  Códigos: {codes_bin}")
        print(f"  Decodificado: {decoded}")
    
    print(f"\n--- PROPIEDADES DE BIQUINARIOS ---")
    print(f"✓ Detección de errores: verificar paridad de quinaria y binaria")
    print(f"✓ Componentes separados facilitan operaciones lógicas")
    print(f"✗ Menos eficiente que BCD (7 bits vs 4 bits para 10 valores)")


def demonstrate_biquinary5():
    """Demostración de biquinario 5 bits."""
    print("\n" + "="*80)
    print("BIQUINARIO 5 BITS (Univac 60/120 style)")
    print("="*80)
    
    bq = Biquinary5Bit()
    
    print(f"\nRepresentación: {bq}")
    print(f"Total bits: 5 (2 quinaria + 3 binaria)")
    print(f"Valores representables: 10 (0-9)")
    print(f"Eficiencia: log_2(10) / 5 ~ 0.664 bits por digito")
    print(f"\nMás compacto que 7 bits, pero aún menos eficiente que BCD (4 bits)")
    
    print(f"\n--- TABLA DE CODIFICACION ---")
    print(f"{'Dígito':<8} {'Quinar':<8} {'Binar':<8} {'Código 5-bit':<20}")
    print("-" * 45)
    
    for d in range(10):
        code = bq.encode(d)
        q, b = bq.encode_table[d]
        print(f"{d:<8} {q:02b}      {b:03b}      {code:05b}")
    
    print(f"\n--- CODIFICACION DE NUMEROS ---")
    test_numbers = ["12345", "67890", "31415"]
    
    for num in test_numbers:
        codes = bq.encode_number(num)
        decoded = bq.decode_number(codes)
        codes_bin = ' '.join(f"{c:05b}" for c in codes)
        print(f"\n{num}:")
        print(f"  Códigos: {codes_bin}")
        print(f"  Decodificado: {decoded}")


def compare_biquinary_vs_other():
    """Comparar biquinarios con otros códigos."""
    print("\n" + "="*80)
    print("COMPARACION: BIQUINARIOS vs OTROS CODIGOS")
    print("="*80)
    
    print(f"\n{'Código':<25} {'Bits':<8} {'Valores':<10} {'Eficiencia':<15}")
    print("-" * 60)
    
    codigos = [
        ("BCD (Natural)", 4, 10, "0.832"),
        ("Biquinario 5 bits", 5, 10, "0.664"),
        ("Biquinario 7 bits", 7, 10, "0.427"),
        ("2 entre 5 (5421)", 5, 10, "0.664"),
        ("2 entre 5 (Felber)", 5, 10, "0.664"),
    ]
    
    for codigo, bits, valores, eff in codigos:
        print(f"{codigo:<25} {bits:<8} {valores:<10} {eff:<15}")
    
    print(f"\n--- DIFERENCIA BIQUINARIOS vs '2 ENTRE 5' ---")
    print(f"""
BIQUINARIOS:
  - Estructura: componente quinaria (grupo de 5) + componente binaria (selección)
  - Dos partes funcionales separadas
  - Ejemplo: 7 = grupo 5-9 (quinaria) + posición 1 (binaria)
  - Ventaja: Detección de errores por paridad en cada componente
  - Implementaciones: IBM 650 (7 bits), Univac 60/120 (5 bits)

'2 ENTRE 5' (Cinco de los siguientes códigos):
  - Estructura: exactamente 2 unos en 5 bits
  - Código de peso: cada bit tiene un peso (5,4,2,1,0 en versión estándar)
  - Ejemplo: 7 = 10010 (pesos 4+1+2=7, dos unos)
  - Ventaja: Detección automática de errores (siempre hay 2 unos)
  - Muy bueno para transmisión

NO SON IGUALES:
  - Biquinarios usan 2-3 unos en su representación
  - "2 entre 5" SIEMPRE usa exactamente 2 unos
  - Biquinarios: separación lógica de componentes
  - "2 entre 5": código de peso con detección integrada
""")


if __name__ == "__main__":
    demonstrate_biquinary7()
    demonstrate_biquinary5()
    compare_biquinary_vs_other()
