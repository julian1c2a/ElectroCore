"""
Ejemplo Educativo: Polinomios y Método de Horner

Aprende dos formas diferentes de convertir de base B a decimal:
1. Polinomio (forma estándar) - Intuitivo pero con potencias
2. Horner (forma anidada) - Más eficiente, sin potencias

Esto demuestra un principio importante: 
¡Existen DIFERENTES ALGORITMOS para resolver el mismo problema!
Algunos son más eficientes que otros.
"""

from core.numeracion_utils import (
    base_b_a_decimal_simple,
    base_b_a_decimal_con_polinomio,
    base_b_a_decimal_con_horner,
    comparar_metodos_conversion
)


def main():
    print("\n" + "=" * 80)
    print("  POLINOMIOS Y HORNER: Dos Formas de Convertir a Decimal")
    print("=" * 80)
    
    # ========================================================================
    # NIVEL 1: CONVERSIÓN SIMPLE
    # ========================================================================
    print("\n[NIVEL 1] CONVERSIÓN SIMPLE (Solo resultado)")
    print("-" * 80)
    
    numero = "1101"
    base = 2
    
    resultado = base_b_a_decimal_simple(numero, base)
    print(f"\n{numero} en base {base} = {resultado} en decimal")
    
    # ========================================================================
    # NIVEL 2: MÉTODO DEL POLINOMIO
    # ========================================================================
    print("\n\n[NIVEL 2] MÉTODO DEL POLINOMIO (Forma Estándar)")
    print("-" * 80)
    print(f"\nProblem: Convierte {numero} desde binario a decimal\n")
    
    resultado_poli = base_b_a_decimal_con_polinomio(numero, base)
    
    print("EXPLICACIÓN:")
    print(f"\nCada dígito tiene un VALOR según su POSICIÓN.")
    print(f"Posición 0 (derecha): multiplicado por {base}^0 = 1")
    print(f"Posición 1: multiplicado por {base}^1 = {base}")
    print(f"Posición 2: multiplicado por {base}^2 = {base**2}")
    print(f"Posición 3 (izquierda): multiplicado por {base}^3 = {base**3}")
    
    print(f"\nPolinomio:")
    print(f"  {resultado_poli['polinomio_str']}")
    
    print(f"\nCálculos:")
    for i, calc in enumerate(resultado_poli['calculos'], 1):
        print(f"  {i}. {calc}")
    
    print(f"\nSuma: {' + '.join(c.split('=')[1].strip() for c in resultado_poli['calculos'])} = {resultado_poli['decimal']}")
    
    # ========================================================================
    # NIVEL 3: MÉTODO DE HORNER
    # ========================================================================
    print("\n" + "=" * 80)
    print("[NIVEL 3] MÉTODO DE HORNER (Más Eficiente)")
    print("-" * 80)
    print(f"\nEl método de Horner REORDENA el cálculo para EVITAR potencias.\n")
    
    resultado_horner = base_b_a_decimal_con_horner(numero, base)
    
    print("IDEA PRINCIPAL:")
    print("  Polinomio:  d₀×b^4 + d₁×b^3 + d₂×b^2 + d₃×b^1")
    print("  Horner:     (((d₀×b + d₁)×b + d₂)×b + d₃)")
    print("\n  Notice: ¡Sin potencias! Solo multiplicaciones y sumas.")
    
    print(f"\nForma de Horner:")
    print(f"  {resultado_horner['forma_horner']}")
    
    print(f"\nEvaluación paso a paso:")
    print(f"  Partimos de izquierda a derecha, tomando cada dígito en orden.\n")
    
    for paso in resultado_horner['pasos_horner']:
        print(f"  Paso {paso['paso']}: Dígito '{paso['digito']}' (valor {paso['valor_digito']})")
        
        if paso['paso'] == 1:
            print(f"    Primero: tomamos el primer dígito = {paso['valor_digito']}")
        else:
            print(f"    Anteriormente teníamos: {paso['resultado_anterior']}")
            print(f"    Multiplicamos por la base: {paso['resultado_anterior']} × {paso['base']} = {paso['multiplicacion']}")
            print(f"    Sumamos el nuevo dígito: {paso['multiplicacion']} + {paso['valor_digito']} = {paso['resultado_actual']}")
        
        print()
    
    print(f"  RESPUESTA: {resultado_horner['decimal']}")
    
    # ========================================================================
    # COMPARACIÓN
    # ========================================================================
    print("\n" + "=" * 80)
    print("COMPARACIÓN: ¿Cuál es mejor?")
    print("=" * 80)
    
    comparacion = comparar_metodos_conversion(numero, base)
    print(f"\n{comparacion['explicacion']}")
    
    # ========================================================================
    # EJEMPLO CON NÚMERO MÁS GRANDE
    # ========================================================================
    print("\n" + "=" * 80)
    print("CASO REAL: Número más grande (ventaja de Horner)")
    print("=" * 80)
    
    numero_grande = "11111111"  # 8 bits
    base_grande = 2
    
    print(f"\nNúmero: {numero_grande} (8 dígitos binarios)")
    
    comparacion_grande = comparar_metodos_conversion(numero_grande, base_grande)
    print(f"\n{comparacion_grande['explicacion']}")
    
    print("\nNOTA IMPORTANTE:")
    print("─" * 80)
    print("Con 8 dígitos:")
    print(f"  • Polinomio: Necesita calcular 8^4, 8^5, 8^6, 8^7 (potencias costosas)")
    print(f"  • Horner: Solo 7 multiplicaciones simples (¡mucho más rápido!)")
    print("\n  ¡Imagina con 1000 dígitos! Horner sería ENORMEMENTE más eficiente.")
    
    # ========================================================================
    # RESUMEN EDUCATIVO
    # ========================================================================
    print("\n" + "=" * 80)
    print("RESUMEN: Lecciones Aprendidas")
    print("=" * 80)
    
    print("""
1. NOTACIÓN POSICIONAL
   ────────────────────
   Cada dígito representa un valor según su posición.
   Ejemplo: 1101₂ = 1×2³ + 1×2² + 0×2¹ + 1×2⁰
   
2. DOS ALGORITMOS DIFERENTES
   ─────────────────────────
   Polinomio: Calcula potencias explícitamente
   Horner:    Reordena para evitar potencias
   
3. LA EFICIENCIA IMPORTA
   ──────────────────────
   Ambos dan la MISMA RESPUESTA.
   Pero Horner es MÁS RÁPIDO porque:
   • Evita cálculos de potencias
   • Solo usa multiplicación y suma
   • Importante con números grandes
   
4. LECCIÓN GENERAL
   ────────────────
   Muchos problemas pueden resolverse de varias formas.
   Algunos algoritmos son más eficientes que otros.
   Un buen programador conoce MÚLTIPLES SOLUCIONES.
""")
    
    # ========================================================================
    # TABLA COMPARATIVA
    # ========================================================================
    print("\nTABLA: Operaciones según número de dígitos")
    print("-" * 80)
    print(f"{'Dígitos':<10} | {'Polinomio (Expo)':<20} | {'Horner':<20} | {'Diferencia':<15}")
    print("-" * 80)
    
    for n in [2, 4, 8, 16, 32]:
        ops_poli = n  # exponenciaciones
        ops_horner = n - 1  # multiplicaciones
        diferencia = ops_poli - ops_horner
        print(f"{n:<10} | {ops_poli} exponenciaciones{'':<6} | {ops_horner} multiplicaciones{'':<6} | Ahorro: {diferencia}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
