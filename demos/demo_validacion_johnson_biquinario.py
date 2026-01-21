"""
Demo: Validación de Códigos Johnson y Biquinario

Este script demuestra las reglas de validación para:
1. Johnson: Máximo 1 transición (0→1 o 1→0)
2. Biquinario: Exactamente 2 bits encendidos

Se puede usar como apoyo directo a las explicaciones en:
- SECCION_2_1_3_JOHNSON.md
- SECCION_2_1_4_BIQUINARIO.md
"""

def count_transitions(word: str) -> int:
    """
    Cuenta el número de transiciones en una palabra binaria.
    
    Una transición es un cambio de 0→1 o 1→0.
    
    Ejemplos:
    - '00000' → 0 transiciones (todos iguales)
    - '00001' → 1 transición (0→1 al final)
    - '01000' → 2 transiciones (0→1→0)
    - '01010' → 4 transiciones (0→1→0→1→0)
    """
    transitions = 0
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            transitions += 1
    return transitions


def is_johnson_valid(word: str) -> bool:
    """
    Valida si una palabra de 5 bits es un código Johnson válido.
    
    Regla: Máximo 1 transición (cambio de 0→1 o 1→0)
    
    Johnson válido: secuencias de unos progresivos
    - 00000 → 0 transiciones ✅
    - 00001 → 1 transición ✅
    - 00011 → 1 transición ✅
    - 01000 → 2 transiciones ❌
    - 01010 → 4 transiciones ❌
    """
    if len(word) != 5:
        return False
    
    if not all(c in '01' for c in word):
        return False
    
    transitions = count_transitions(word)
    
    # Johnson válido si tiene 0 o 1 transición
    # (0 para 00000 o 11111, 1 para el resto)
    return transitions <= 1


def is_biquinario_valid(word: str) -> bool:
    """
    Valida si una palabra de 7 bits es un código Biquinario válido.
    
    Regla: Exactamente 2 bits encendidos (unos)
    
    Biquinario válido: exactamente 2 unos
    - 0100001 → 2 unos ✅ (dígito 0)
    - 0100010 → 2 unos ✅ (dígito 1)
    - 0100011 → 3 unos ❌ (error)
    - 0000000 → 0 unos ❌ (error)
    - 1111111 → 7 unos ❌ (error)
    """
    if len(word) != 7:
        return False
    
    if not all(c in '01' for c in word):
        return False
    
    # Biquinario: exactamente 2 bits encendidos
    return word.count('1') == 2


def demonstrate_johnson():
    """Demuestra la validación de Johnson con ejemplos."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: VALIDACIÓN DE CÓDIGO JOHNSON")
    print("="*70)
    print("\nRegla: Máximo 1 transición (cambio 0→1 o 1→0)")
    print("-" * 70)
    
    # Palabras Johnson válidas (de la codificación oficial)
    valid_johnson = [
        '00000',  # 0
        '00001',  # 1
        '00011',  # 2
        '00111',  # 3
        '01111',  # 4
        '11111',  # 5
        '11110',  # 6
        '11100',  # 7
        '11000',  # 8
        '10000',  # 9
    ]
    
    # Palabras Johnson inválidas (ejemplos de códigos prohibidos)
    invalid_johnson = [
        '01000',  # 2 transiciones
        '01001',  # 3 transiciones
        '01010',  # 4 transiciones
        '01011',  # 3 transiciones
        '01100',  # 2 transiciones
        '01101',  # 3 transiciones
        '10101',  # 4 transiciones
        '10110',  # 2 transiciones
    ]
    
    print("\n✅ CÓDIGOS VÁLIDOS (Johnson oficial):\n")
    for i, word in enumerate(valid_johnson):
        trans = count_transitions(word)
        valid = is_johnson_valid(word)
        print(f"  {word} → Dígito {i} | Transiciones: {trans} | Válido: {valid}")
    
    print("\n❌ CÓDIGOS INVÁLIDOS (prohibidos en Johnson):\n")
    for word in invalid_johnson:
        trans = count_transitions(word)
        valid = is_johnson_valid(word)
        print(f"  {word} | Transiciones: {trans} | Válido: {valid}")
    
    print("\n" + "-" * 70)
    print("Análisis: Los códigos válidos tienen máx. 1 transición")
    print("         Los inválidos tienen 2 o más transiciones")


def demonstrate_biquinario():
    """Demuestra la validación de Biquinario con ejemplos."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: VALIDACIÓN DE CÓDIGO BIQUINARIO")
    print("="*70)
    print("\nRegla: Exactamente 2 bits encendidos (unos)")
    print("-" * 70)
    
    # Palabras Biquinario válidas (de la codificación oficial de 7 bits)
    valid_biquinario = [
        '0100001',  # 0: Quina 01000, Binario 01
        '0100010',  # 1: Quina 01000, Binario 10
        '0100100',  # 2: Quina 01000, Binario 01 (diferente posición)
        '0101000',  # 3: Quina 01000, Binario 01 (otra posición)
        '0110000',  # 4: Quina 01000, Binario 10 (otra posición)
        '1000001',  # 5: Quina 10000, Binario 01
        '1000010',  # 6: Quina 10000, Binario 10
        '1000100',  # 7: Quina 10000, Binario 01 (diferente posición)
        '1001000',  # 8: Quina 10000, Binario 01 (otra posición)
        '1010000',  # 9: Quina 10000, Binario 10 (otra posición)
    ]
    
    # Palabras Biquinario inválidas (diferentes números de unos)
    invalid_biquinario = [
        '0000000',  # 0 unos: información perdida
        '0000001',  # 1 uno: error
        '0100011',  # 3 unos: error de transmisión
        '0101010',  # 3 unos: error
        '0111111',  # 6 unos: múltiples errores
        '1111111',  # 7 unos: todos encendidos (error grave)
        '1010101',  # 4 unos: error
        '1110111',  # 6 unos: error
    ]
    
    print("\n✅ CÓDIGOS VÁLIDOS (exactamente 2 unos):\n")
    for i, word in enumerate(valid_biquinario):
        count = word.count('1')
        valid = is_biquinario_valid(word)
        digito = i
        print(f"  {word} → Dígito {digito} | Unos: {count} | Válido: {valid}")
    
    print("\n❌ CÓDIGOS INVÁLIDOS (número diferente de 2 unos):\n")
    for word in invalid_biquinario:
        count = word.count('1')
        valid = is_biquinario_valid(word)
        print(f"  {word} | Unos: {count} | Válido: {valid}")
    
    print("\n" + "-" * 70)
    print("Análisis: Los códigos válidos tienen EXACTAMENTE 2 unos")
    print("         Los inválidos tienen diferente número de unos")


def demonstrate_error_detection():
    """Demuestra la capacidad de detección de errores."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: DETECCIÓN DE ERRORES")
    print("="*70)
    
    print("\n📌 JOHNSON: Detección por Transiciones")
    print("-" * 70)
    print("\nEjemplo: Transmisión de '00001' (dígito 1)")
    print("\nEscenario 1: Sin error")
    print(f"  Envío:        '00001'")
    print(f"  Recibo:       '00001'")
    print(f"  Transiciones: {count_transitions('00001')} → ✅ VÁLIDO")
    
    print("\nEscenario 2: Error en bit (flip de bit 1)")
    print(f"  Envío:        '00001'")
    print(f"  Recibo:       '00011' (cambió bit 1)")
    print(f"  Transiciones: {count_transitions('00011')} → ✅ SIGUE SIENDO VÁLIDO")
    print("  Nota: Johnson NO detectaría este tipo de error")
    
    print("\nEscenario 3: Error en bit (flip de bit central)")
    print(f"  Envío:        '00001'")
    print(f"  Recibo:       '01001' (cambió bit central)")
    print(f"  Transiciones: {count_transitions('01001')} → ❌ INVÁLIDO (error detectado)")
    
    print("\n📌 BIQUINARIO: Detección por Conteo de Unos")
    print("-" * 70)
    print("\nEjemplo: Transmisión de '0100001' (dígito 0)")
    print("\nEscenario 1: Sin error")
    print(f"  Envío:  '0100001'")
    print(f"  Recibo: '0100001'")
    print(f"  Unos:   {('0100001').count('1')} → ✅ VÁLIDO")
    
    print("\nEscenario 2: Error en 1 bit (flip de bit 0)")
    print(f"  Envío:  '0100001'")
    print(f"  Recibo: '0100000' (cambió bit 0)")
    print(f"  Unos:   {('0100000').count('1')} → ❌ INVÁLIDO (error detectado)")
    
    print("\nEscenario 3: Error en 1 bit (flip de bit 1)")
    print(f"  Envío:  '0100001'")
    print(f"  Recibo: '0100011' (cambió bit 1)")
    print(f"  Unos:   {('0100011').count('1')} → ❌ INVÁLIDO (error detectado)")
    
    print("\nEscenario 4: Error múltiple (2 bits simultáneos)")
    print(f"  Envío:  '0100001'")
    print(f"  Recibo: '0101010' (2 bits cambiaron)")
    print(f"  Unos:   {('0101010').count('1')} → ❌ INVÁLIDO (error detectado)")


def demonstrate_validation_rules():
    """Demuestra las reglas de validación de forma interactiva."""
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: REGLAS DE VALIDACIÓN")
    print("="*70)
    
    test_cases_johnson = [
        ('00000', True, 'Todos ceros - especial'),
        ('00001', True, 'Unos progresivos desde derecha'),
        ('00011', True, 'Unos progresivos'),
        ('00111', True, 'Unos progresivos'),
        ('01000', False, 'Transición en medio - inválido'),
        ('01010', False, 'Múltiples transiciones - inválido'),
        ('10101', False, 'Alternancia - inválido'),
        ('11111', True, 'Todos unos - especial'),
        ('11110', True, 'Unos progresivos desde izquierda'),
    ]
    
    print("\n📊 JOHNSON: Tabla de Validación")
    print("-" * 70)
    print(f"{'Palabra':<10} {'Esperado':<10} {'Transic.':<10} {'Resultado':<12} {'Descripción':<30}")
    print("-" * 70)
    
    for word, expected, desc in test_cases_johnson:
        trans = count_transitions(word)
        actual = is_johnson_valid(word)
        result = "✅ PASA" if actual == expected else "❌ FALLA"
        print(f"{word:<10} {str(expected):<10} {trans:<10} {result:<12} {desc:<30}")
    
    test_cases_biquinario = [
        ('0000000', False, 'Ceros - sin información'),
        ('0000001', False, '1 uno - error'),
        ('0000011', True, '2 unos - válido'),
        ('0100001', True, '2 unos - válido'),
        ('0100011', False, '3 unos - error detectado'),
        ('0101010', False, '3 unos - error'),
        ('1111111', False, '7 unos - error grave'),
        ('1100000', True, '2 unos - válido'),
        ('1010000', True, '2 unos - válido'),
    ]
    
    print("\n📊 BIQUINARIO: Tabla de Validación")
    print("-" * 70)
    print(f"{'Palabra':<10} {'Esperado':<10} {'Unos':<10} {'Resultado':<12} {'Descripción':<30}")
    print("-" * 70)
    
    for word, expected, desc in test_cases_biquinario:
        count = word.count('1')
        actual = is_biquinario_valid(word)
        result = "✅ PASA" if actual == expected else "❌ FALLA"
        print(f"{word:<10} {str(expected):<10} {count:<10} {result:<12} {desc:<30}")


if __name__ == "__main__":
    # Ejecutar demostraciones
    demonstrate_johnson()
    demonstrate_biquinario()
    demonstrate_error_detection()
    demonstrate_validation_rules()
    
    print("\n" + "="*70)
    print("FIN DE DEMOSTRACIONES")
    print("="*70)
    print("\n✅ Resumen:")
    print("  • Johnson: Máx. 1 transición (para unos progresivos)")
    print("  • Biquinario: Exactamente 2 bits encendidos")
    print("  • Ambos códigos detectan errores automáticamente")
    print("  • Útil para validar códigos en sistemas digitales")
    print()
