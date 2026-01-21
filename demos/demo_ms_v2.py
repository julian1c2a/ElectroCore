"""
DEMOSTRACION: MAGNITUD Y SIGNO (M&S)
Seccion 2.1.1.7.1: Numeros Enteros con Signo
"""

from core.enteros_signados import (
    # Rango y Capacidad
    rango_ms,
    analizar_ms,
    
    # Conversion
    decimal_a_ms,
    ms_a_decimal,
    explicar_conversion_ms,
    
    # Operaciones
    negacion_ms,
    es_positivo_ms,
    es_negativo_ms,
    es_cero_ms,
    valor_absoluto_ms,
    comparar_ms,
    
    # Analisis
    validar_representacion_ms,
    analizar_representacion_ms,
    
    # Constructores
    crear_cero_positivo_ms,
    crear_cero_negativo_ms,
    generar_tabla_ms,
    mostrar_tabla_ms,
)


print("""
================================================================================
                   DEMOSTRACION: MAGNITUD Y SIGNO (M&S)
================================================================================

Este script demuestra todos los aspectos del sistema de Magnitud y Signo
para representacion de numeros enteros con signo en binario.

Seccion: 2.1.1.7.1 - Magnitud y Signo
Tema: Numeros Enteros con Signo
================================================================================
""")

# ==============================================================================
# DEMO 1: CONCEPTOS BASICOS
# ==============================================================================

print("\nDEMO 1: CONCEPTOS BASICOS")
print("-" * 80)

print("""
En Magnitud y Signo:
  * Bit n-1 (MSB): Signo (0=positivo, 1=negativo)
  * Bits n-2...0: Magnitud (valor absoluto)

Ejemplos en M&S de 8 bits:
""")

ejemplos = [
    (86, 8, "Numero positivo"),
    (-86, 8, "Numero negativo"),
    (0, 8, "Cero positivo"),
    (127, 8, "Maximo positivo (M&S8)"),
    (-127, 8, "Minimo negativo (M&S8)"),
]

for decimal, n_bits, descripcion in ejemplos:
    ms = decimal_a_ms(decimal, n_bits)
    print(f"  {decimal:6} (dec) -> {ms} (M&S{n_bits})  [{descripcion}]")
    
    # Mostrar estructura
    signo = "+" if ms[0] == '0' else "-"
    magnitud = int(ms[1:], 2)
    print(f"           Signo: {signo}  |  Magnitud: {magnitud} (dec), {ms[1:]} (bin)")
    print()

# ==============================================================================
# DEMO 2: RANGO Y CAPACIDAD
# ==============================================================================

print("\n\nDEMO 2: RANGO Y CAPACIDAD")
print("-" * 80)

print("\nAnalisis para diferentes tamanos:\n")

for n_bits in [4, 8, 16]:
    info = rango_ms(n_bits)
    print(f"M&S{n_bits}:")
    print(f"  Rango negativos:      [{info['min_negativo']:10}, {info['max_negativo']:10}]")
    print(f"  Rango positivos:      [{info['min_positivo']:10}, {info['max_positivo']:10}]")
    print(f"  Valores unicos:       {info['capacidad']:10} (2^{n_bits} - 1)")
    eficacia_porcentaje = info['eficacia'] * 100
    print(f"  Eficacia:             {eficacia_porcentaje:10.2f}%")
    print(f"  (Una combinacion desperdiciada: +0 y -0)")
    print()

# ==============================================================================
# DEMO 3: CONVERSIONES PASO A PASO
# ==============================================================================

print("\nDEMO 3: CONVERSIONES PASO A PASO")
print("-" * 80)

numeros = [42, -42, 0, 1, -1]

for numero in numeros:
    print(f"\nConvertir {numero:4} a M&S8:")
    print("-" * 60)
    
    explicacion = explicar_conversion_ms(numero, 8)
    
    print(f"  Paso 1: {explicacion['paso_1_signo']['descripcion']}")
    print(f"          Numero: {numero}")
    print(f"          Signo: {explicacion['paso_1_signo']['signo']}")
    print(f"          Bit de signo: {explicacion['paso_1_signo']['bit_signo']}")
    
    print(f"\n  Paso 2: {explicacion['paso_2_magnitud']['descripcion']}")
    print(f"          Magnitud: {explicacion['paso_2_magnitud']['magnitud']} (dec)")
    print(f"          Binario: {explicacion['paso_2_magnitud']['conversion_binaria']['magnitud_binaria']} (bin)")
    
    print(f"\n  Paso 3: {explicacion['paso_3_combinacion']['descripcion']}")
    print(f"          Signo + Magnitud = {explicacion['paso_3_combinacion']['representacion_final']}")
    
    print(f"\n  Resultado: {explicacion['resultado_final']['representacion']} ({explicacion['resultado_final']['formato']})")

# ==============================================================================
# DEMO 4: OPERACIONES EN M&S
# ==============================================================================

print("\n\nDEMO 4: OPERACIONES EN M&S")
print("-" * 80)

# Negacion
print("\n4.1 NEGACION (Multiplicar por -1)")
print("En M&S, negacion = flip del bit de signo\n")

test_negacion = ['00101010', '10101010', '00000000', '10000000']
for ms in test_negacion:
    valor_original = ms_a_decimal(ms)
    negado = negacion_ms(ms)
    valor_negado = ms_a_decimal(negado)
    print(f"  {ms} ({valor_original:4}) -> flip bit signo -> {negado} ({valor_negado:4})")

# Predicados
print("\n4.2 CONSULTAS SOBRE VALORES")
print("-" * 60)

test_valores = ['01010110', '11010110', '00000000', '10000000']
for ms in test_valores:
    valor = ms_a_decimal(ms)
    es_pos = es_positivo_ms(ms)
    es_neg = es_negativo_ms(ms)
    es_cero = es_cero_ms(ms)
    
    print(f"\n  {ms} = {valor:4}")
    print(f"    Es positivo: {es_pos:5} | Es negativo: {es_neg:5} | Es cero: {es_cero}")

# Comparacion
print("\n4.3 COMPARACION")
print("-" * 60)
print("En M&S, la comparacion es compleja (invertida para negativos)\n")

pares = [
    ('00101010', '00110010'),  # 42 vs 50
    ('10101010', '10110010'),  # -42 vs -50
    ('00000000', '10000000'),  # +0 vs -0
]

for a, b in pares:
    val_a = ms_a_decimal(a)
    val_b = ms_a_decimal(b)
    resultado = comparar_ms(a, b)
    relacion = '<' if resultado < 0 else ('=' if resultado == 0 else '>')
    print(f"  {a} ({val_a:4}) {relacion} {b} ({val_b:4})")

# ==============================================================================
# DEMO 5: VENTAJAS Y DESVENTAJAS
# ==============================================================================

print("\n\nDEMO 5: VENTAJAS Y DESVENTAJAS")
print("-" * 80)

print("""
VENTAJAS:
  + Intuitivo (como escribimos numeros a mano)
  + Negacion es simple (solo flip del bit de signo)
  + Facil de entender conceptualmente
  + Multiplicacion/division directa sobre magnitudes

DESVENTAJAS:
  - DOS REPRESENTACIONES PARA CERO (+0 y -0)
    -> Desperdicia una combinacion
    -> Comparacion de igualdad mas compleja
  
  - SUMA Y RESTA COMPLICADAS
    -> Requieren diferentes algoritmos segun signos
    -> Mucho mas lento que Complemento a 2
  
  - COMPARACION INVERTIDA PARA NEGATIVOS
    -> Mas compleja y lenta
    -> Requiere logica especial en hardware
  
  - BAJA EFICIENCIA TEORICA
    -> Capacidad = 2^n - 1 (no 2^n)
    -> Eficacia = 1 - (1/2^n)

CONCLUSION:
  M&S es pedagogicamente util para ENTENDER el concepto,
  pero NO es usado en hardware moderno.
  
  -> Los procesadores usan Complemento a 2 (C2)
  -> C2 resuelve todos estos problemas
""")

# Mostrar tabla comparativa de los dos ceros
print("\nEjemplo: Los dos ceros en M&S8")
print("-" * 60)

cero_positivo = crear_cero_positivo_ms(8)
cero_negativo = crear_cero_negativo_ms(8)

print(f"\n  Representacion de +0: {cero_positivo}")
print(f"  Representacion de -0: {cero_negativo}")
print(f"\n  Ambas se interpretan como: {ms_a_decimal(cero_positivo)}")
print(f"  iDos combinaciones diferentes para el mismo valor!")

# ==============================================================================
# DEMO 6: TABLAS
# ==============================================================================

print("\n\nDEMO 6: TABLAS DE VALORES")
print("-" * 80)

print("\nTabla M&S4 (rango [-7, 7]) - muestra parcial:")
tabla = generar_tabla_ms(4)
print(f"\n  Decimal  |  M&S  | Magnitud | Signo")
print("  " + "-" * 40)
for fila in tabla[:8]:  # Primeros 8
    print(f"  {fila['decimal']:7} | {fila['ms']:5} | {fila['magnitud']:8} | {fila['signo']}")
print("  " + "-" * 40)
print("  ...")
for fila in tabla[-3:]:  # Ultimos 3
    print(f"  {fila['decimal']:7} | {fila['ms']:5} | {fila['magnitud']:8} | {fila['signo']}")

# ==============================================================================
# DEMO 7: ANALISIS COMPLETO
# ==============================================================================

print("\n\nDEMO 7: ANALISIS COMPLETO")
print("-" * 80)

representaciones = ['01010110', '11010110', '00000000']

for rep in representaciones:
    print(f"\nAnalizando: {rep}")
    print("-" * 60)
    
    valor = ms_a_decimal(rep)
    es_pos = es_positivo_ms(rep)
    es_neg = es_negativo_ms(rep)
    es_cero = es_cero_ms(rep)
    
    signo = "+" if rep[0] == '0' else "-"
    magnitud = int(rep[1:], 2)
    
    print(f"  Valor decimal: {valor}")
    print(f"  Signo: {signo}")
    print(f"  Magnitud: {magnitud}")
    print(f"  Es positivo: {es_pos}")
    print(f"  Es negativo: {es_neg}")
    print(f"  Es cero: {es_cero}")

# ==============================================================================
# CONCLUSION
# ==============================================================================

print("\n\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print("""
M&S es la forma MAS INTUITIVA de representar numeros con signo:
  + Conceptualmente clara: signo separado de magnitud
  + Facil de entender para principiantes
  + Base conceptual para otros sistemas

PERO tiene PROBLEMAS PRACTICOS:
  - Dos ceros (desperdicio)
  - Suma/resta complicadas
  - Comparacion invertida para negativos

POR ESO, en HARDWARE MODERNO se usa:
  --> COMPLEMENTO A 2 (C2)
  --> Que resuelve todos estos problemas

La progresion pedagogica es:
  1. M&S (entender concepto) --> 
  2. C1 (transicion) --> 
  3. C2 (moderno)

iProximo: Complemento a 1 (C1)!

================================================================================
""")

print("\nDemostracion completada exitosamente!")
