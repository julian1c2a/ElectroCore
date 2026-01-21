#!/usr/bin/env python3
"""
Generar tabla comparativa visual de todas las representaciones de enteros signados
"""

def generar_tabla_comparativa():
    """Generar tabla comparativa de M&S, CB-1, CB, y ExcK en binario 4-bit"""
    
    print("\n" + "=" * 100)
    print("TABLA COMPARATIVA: TODAS LAS REPRESENTACIONES EN BINARIO 4-BIT")
    print("=" * 100)
    
    print("\n" + "-" * 100)
    print("| Decimal | Mag&Sign | CB-1    | CB (Two's) | ExcK(K=8) | Nota                          |")
    print("-" * 100)
    
    comparativa = [
        (-8, "NO", "NO", "10000", "0000", "ExcK minimo"),
        (-7, "10111", "11000", "10001", "0001", ""),
        (-6, "10110", "11001", "10010", "0010", ""),
        (-5, "10101", "11010", "10011", "0011", ""),
        (-4, "10100", "11011", "10100", "0100", ""),
        (-3, "10011", "11100", "10101", "0101", ""),
        (-2, "10010", "11101", "10110", "0110", ""),
        (-1, "10001", "11110", "11111", "0111", ""),
        (0, "00000", "00000", "00000", "1000", "ExcK representa 0 como 1000 (valor K)"),
        (0, "10000", "11111", "NO", "1000", "M&S y CB-1 tienen dos ceros"),
        (1, "00001", "00001", "00001", "1001", ""),
        (2, "00010", "00010", "00010", "1010", ""),
        (3, "00011", "00011", "00011", "1011", ""),
        (4, "00100", "00100", "00100", "1100", ""),
        (5, "00101", "00101", "00101", "1101", ""),
        (6, "00110", "00110", "00110", "1110", ""),
        (7, "00111", "00111", "00111", "1111", "ExcK maximo"),
    ]
    
    for entrada in comparativa:
        if len(entrada) == 5:
            decimal, ms, cb1, cb, exck, nota = entrada[0], entrada[1], entrada[2], entrada[3], entrada[4], entrada[5]
            print(f"| {decimal:7d} | {ms:8s} | {cb1:7s} | {cb:10s} | {exck:9s} | {nota:30s} |")
        else:
            decimal, ms, cb1, cb, exck, nota = entrada
            print(f"| {decimal:7d} | {ms:8s} | {cb1:7s} | {cb:10s} | {exck:9s} | {nota:30s} |")
    
    print("-" * 100)

    
    print("\n" + "=" * 100)
    print("ESTADÍSTICAS POR REPRESENTACIÓN (Binario 4-bit)")
    print("=" * 100)
    
    stats = [
        ("Magnitud y Signo", -7, 7, 15, 93.75, "Dos ceros (00000 y 10000)"),
        ("CB-1 (One's Complement)", -7, 7, 15, 93.75, "Dos ceros (00000 y 11111)"),
        ("CB (Two's Complement)", -8, 7, 16, 100.0, "Un cero (00000), estándar industrial"),
        ("Exceso a K (K=8)", -8, 7, 16, 100.0, "Un cero (01000), rango flexible"),
    ]
    
    print(f"\n{'Representación':<25} {'Minimo':>8} {'Maximo':>8} {'Capacidad':>10} {'Eficacia':>10} {'Nota':<40}")
    print("-" * 100)
    for nombre, min_v, max_v, cap, efic, nota in stats:
        print(f"{nombre:<25} {min_v:>8d} {max_v:>8d} {cap:>10d} {efic:>9.2f}% {nota:<40}")
    
    print("\n" + "=" * 100)
    print("CARACTERÍSTICAS OPERACIONALES")
    print("=" * 100)
    
    operaciones = [
        ("Suma", "M&S", "Suma simple + ajuste de signo", "Moderado"),
        ("", "CB-1", "Suma simple + end-around carry", "Moderado"),
        ("", "CB", "Suma simple", "Muy simple [STD]"),
        ("", "ExcK", "Suma simple - K", "Simple"),
        ("Multiplicación", "M&S", "Multiplicación de magnitud + signo", "Complejo"),
        ("", "CB-1", "Multiplicación compleja", "Muy complejo"),
        ("", "CB", "Multiplicación simple (modulo)", "Muy simple [STD]"),
        ("", "ExcK", "Multiplicación simple (+ conversiones)", "Simple"),
        ("Comparación", "M&S", "Necesita analizar el signo", "Complejo"),
        ("", "CB-1", "Compleja (dos ceros)", "Complejo"),
        ("", "CB", "Directo si se ignora MSB", "Simple"),
        ("", "ExcK", "Directo (valor natural = comparación)", "Muy simple [STD]"),
        ("Detección de rango", "M&S", "Especial para negativos", "Moderado"),
        ("", "CB-1", "Especial para dos ceros", "Complejo"),
        ("", "CB", "Verificar MSB y overflow", "Moderado"),
        ("", "ExcK", "Verificar solo overflow", "Simple"),
    ]
    
    print(f"\n{'Operación':<20} {'Representación':<15} {'Descripción':<40} {'Dificultad':<15}")
    print("-" * 95)
    for op, rep, desc, dif in operaciones:
        print(f"{op:<20} {rep:<15} {desc:<40} {dif:<15}")


if __name__ == "__main__":
    generar_tabla_comparativa()
    print("\n")

