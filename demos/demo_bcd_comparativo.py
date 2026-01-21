#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_bcd_comparativo.py

Demostración comparativa de los 3 códigos BCD:
- BCD Natural (8-4-2-1)
- BCD Exceso-3
- BCD Aiken (2-4-2-1)

Muestra:
1. Codificación de dígitos individuales
2. Codificación de números completos
3. Operaciones básicas (suma, complemento a 9)
4. Propiedades (autocomplementariedad, pesos)
"""

def bcd_natural(digito):
    """Codificar dígito en BCD Natural (8421)"""
    if not 0 <= digito <= 9:
        raise ValueError(f"Dígito debe estar entre 0-9, recibido: {digito}")
    return format(digito, '04b')

def bcd_exceso3(digito):
    """Codificar dígito en BCD Exceso-3"""
    if not 0 <= digito <= 9:
        raise ValueError(f"Dígito debe estar entre 0-9, recibido: {digito}")
    valor = digito + 3
    return format(valor, '04b')

def bcd_aiken(digito):
    """Codificar dígito en BCD Aiken (2-4-2-1)"""
    tabla_aiken = {
        0: '0000', 1: '0001', 2: '0010', 3: '0011', 4: '0100',
        5: '1011', 6: '1100', 7: '1101', 8: '1110', 9: '1111'
    }
    if digito not in tabla_aiken:
        raise ValueError(f"Dígito debe estar entre 0-9, recibido: {digito}")
    return tabla_aiken[digito]

def invertir_bits(codigo_4bits):
    """Invertir todos los bits (complemento lógico)"""
    return ''.join('1' if bit == '0' else '0' for bit in codigo_4bits)

def numero_a_bcd_natural(numero):
    """Convertir número decimal a BCD Natural"""
    return ''.join(bcd_natural(int(d)) for d in str(numero))

def numero_a_bcd_exceso3(numero):
    """Convertir número decimal a BCD Exceso-3"""
    return ''.join(bcd_exceso3(int(d)) for d in str(numero))

def numero_a_bcd_aiken(numero):
    """Convertir número decimal a BCD Aiken"""
    return ''.join(bcd_aiken(int(d)) for d in str(numero))

def peso_aiken(b3, b2, b1, b0):
    """Calcular valor decimal usando pesos Aiken 2-4-2-1"""
    return 2*b3 + 4*b2 + 2*b1 + b0

def main():
    print("=" * 80)
    print("DEMOSTRACIÓN COMPARATIVA: CÓDIGOS BCD")
    print("=" * 80)
    
    # =========== PARTE 1: CODIFICACIÓN DE DÍGITOS ===========
    print("\n" + "="*80)
    print("PARTE 1: CODIFICACIÓN DE DÍGITOS INDIVIDUALES")
    print("="*80)
    
    print("\nTabla Maestra:")
    print("-" * 70)
    print(f"{'Dígito':<8} {'BCD Natural':<18} {'Exc-3':<18} {'Aiken':<18}")
    print("-" * 70)
    
    for digito in range(10):
        nat = bcd_natural(digito)
        exc3 = bcd_exceso3(digito)
        aik = bcd_aiken(digito)
        print(f"{digito:<8} {nat:<18} {exc3:<18} {aik:<18}")
    
    # =========== PARTE 2: AUTOCOMPLEMENTARIEDAD ===========
    print("\n" + "="*80)
    print("PARTE 2: AUTOCOMPLEMENTARIEDAD (Complemento a 9)")
    print("="*80)
    
    print("\n✅ BCD Exceso-3: Complemento a 9 = Invertir Bits")
    print("-" * 70)
    print(f"{'Dígito':<8} {'Exc3(d)':<18} {'~Exc3(d)':<18} {'Exc3(9-d)':<18} {'¿Iguales?':<10}")
    print("-" * 70)
    
    for digito in range(10):
        exc3_d = bcd_exceso3(digito)
        not_exc3_d = invertir_bits(exc3_d)
        exc3_comp = bcd_exceso3(9 - digito)
        match = "✅" if not_exc3_d == exc3_comp else "❌"
        print(f"{digito:<8} {exc3_d:<18} {not_exc3_d:<18} {exc3_comp:<18} {match:<10}")
    
    print("\n✅ BCD Aiken: Complemento a 9 = Invertir Bits")
    print("-" * 70)
    print(f"{'Dígito':<8} {'Aiken(d)':<18} {'~Aiken(d)':<18} {'Aiken(9-d)':<18} {'¿Iguales?':<10}")
    print("-" * 70)
    
    for digito in range(10):
        aik_d = bcd_aiken(digito)
        not_aik_d = invertir_bits(aik_d)
        aik_comp = bcd_aiken(9 - digito)
        match = "✅" if not_aik_d == aik_comp else "❌"
        print(f"{digito:<8} {aik_d:<18} {not_aik_d:<18} {aik_comp:<18} {match:<10}")
    
    # =========== PARTE 3: PESOS AIKEN ===========
    print("\n" + "="*80)
    print("PARTE 3: VERIFICACIÓN DE PESOS AIKEN (2-4-2-1)")
    print("="*80)
    
    print("\nVerificación: Valor = 2·b3 + 4·b2 + 2·b1 + b0")
    print("-" * 90)
    print(f"{'Dígito':<8} {'Aiken':<12} {'b3':<4} {'b2':<4} {'b1':<4} {'b0':<4} {'Cálculo':<30} {'Valor':<8}")
    print("-" * 90)
    
    for digito in range(10):
        aik_cod = bcd_aiken(digito)
        b3, b2, b1, b0 = [int(bit) for bit in aik_cod]
        valor = peso_aiken(b3, b2, b1, b0)
        calculo = f"2({b3})+4({b2})+2({b1})+{b0}"
        print(f"{digito:<8} {aik_cod:<12} {b3:<4} {b2:<4} {b1:<4} {b0:<4} {calculo:<30} {valor:<8}")
    
    # =========== PARTE 4: NÚMEROS MULTIDÍGITOS ===========
    print("\n" + "="*80)
    print("PARTE 4: CODIFICACIÓN DE NÚMEROS COMPLETOS")
    print("="*80)
    
    numeros = [42, 57, 130, 999]
    
    for numero in numeros:
        print(f"\nNúmero: {numero}")
        print("-" * 70)
        nat = numero_a_bcd_natural(numero)
        exc3 = numero_a_bcd_exceso3(numero)
        aik = numero_a_bcd_aiken(numero)
        
        print(f"BCD Natural: {nat} (espacios: {' '.join(nat[i:i+4] for i in range(0, len(nat), 4))})")
        print(f"BCD Exc-3:   {exc3} (espacios: {' '.join(exc3[i:i+4] for i in range(0, len(exc3), 4))})")
        print(f"BCD Aiken:   {aik} (espacios: {' '.join(aik[i:i+4] for i in range(0, len(aik), 4))})")
    
    # =========== PARTE 5: OPERACIONES ===========
    print("\n" + "="*80)
    print("PARTE 5: OPERACIONES BÁSICAS")
    print("="*80)
    
    # Negación en Exceso-3
    print("\n✅ Negación en Exceso-3: Invertir bits = Complemento a 9")
    print("-" * 70)
    
    numeros_negar = [5, 27, 42]
    for numero in numeros_negar:
        exc3_cod = numero_a_bcd_exceso3(numero)
        print(f"\nNúmero original: {numero}")
        print(f"Codificación Exc3: {' '.join(exc3_cod[i:i+4] for i in range(0, len(exc3_cod), 4))}")
        
        # Invertir bits
        negado_bits = ''.join(invertir_bits(exc3_cod[i:i+4]) for i in range(0, len(exc3_cod), 4))
        print(f"Invertir bits:     {' '.join(negado_bits[i:i+4] for i in range(0, len(negado_bits), 4))}")
        
        # Verificar que es el complemento a 9
        comp_a_9 = 10**len(str(numero)) - 1 - numero
        comp_a_9_exc3 = numero_a_bcd_exceso3(comp_a_9)
        print(f"Complemento a 9 de {numero} = {comp_a_9}")
        print(f"Codificación Exc3 del comp: {' '.join(comp_a_9_exc3[i:i+4] for i in range(0, len(comp_a_9_exc3), 4))}")
        print(f"¿Coinciden? {'✅ SÍ' if negado_bits == comp_a_9_exc3 else '❌ NO'}")
    
    # =========== PARTE 6: COMPARACIÓN DE PROPIEDADES ===========
    print("\n" + "="*80)
    print("PARTE 6: COMPARACIÓN DE PROPIEDADES")
    print("="*80)
    
    propiedades = {
        'BCD Natural (8-4-2-1)': {
            'Pesos': '8-4-2-1',
            'Autocomplementario': 'NO',
            'Comparación Directa': 'SÍ',
            'Suma Simple': 'NO',
            'Números Signados': 'Difícil',
            'Uso': 'I/O Decimal'
        },
        'BCD Exceso-3': {
            'Pesos': 'NO',
            'Autocomplementario': 'SÍ',
            'Comparación Directa': 'NO',
            'Suma Simple': 'NO',
            'Números Signados': 'Fácil',
            'Uso': 'Máquinas Antiguas'
        },
        'BCD Aiken (2-4-2-1)': {
            'Pesos': '2-4-2-1',
            'Autocomplementario': 'SÍ',
            'Comparación Directa': 'NO',
            'Suma Simple': 'NO',
            'Números Signados': 'Fácil',
            'Uso': 'Mark I (1944)'
        }
    }
    
    # Obtener todas las propiedades
    todas_props = set()
    for props in propiedades.values():
        todas_props.update(props.keys())
    todas_props = sorted(todas_props)
    
    # Header
    ancho_prop = 20
    print(f"\n{'':<{ancho_prop}} {'BCD Natural':<25} {'Exc-3':<25} {'Aiken':<25}")
    print("-" * 100)
    
    # Filas
    for prop in todas_props:
        nat = propiedades['BCD Natural (8-4-2-1)'].get(prop, '—')
        exc3 = propiedades['BCD Exceso-3'].get(prop, '—')
        aik = propiedades['BCD Aiken (2-4-2-1)'].get(prop, '—')
        print(f"{prop:<{ancho_prop}} {nat:<25} {exc3:<25} {aik:<25}")
    
    # =========== CONCLUSIÓN ===========
    print("\n" + "="*80)
    print("CONCLUSIÓN")
    print("="*80)
    
    print("""
Los 3 códigos BCD representan diferentes opciones de diseño:

✅ BCD NATURAL (8-4-2-1)
   - Mejor para: Entrada/salida, comparación
   - Características: Intuitivo, pesos estándar
   - Problema: Suma compleja, sin autocomplementariedad

✅ BCD EXCESO-3
   - Mejor para: Aritmética signada, máquinas antiguas
   - Características: Autocomplementario (invertir bits = comp. a 9)
   - Problema: Sin pesos, comparación difícil

✅ BCD AIKEN (2-4-2-1)
   - Mejor para: Balance entre eficiencia y funcionalidad
   - Características: Pesos + autocomplementario
   - Problema: Pesos irregulares, menos estándar

PRINCIPIO DE DISEÑO:
No existe un "mejor" código universal. La elección depende de:
1. Operaciones dominantes (suma, comparación, conversión)
2. Arquitectura del hardware (¿necesita pesos?)
3. Requisitos de números signados (¿sí o no?)
4. Contexto histórico/estándares del sistema
    """)
    
    print("="*80)
    print("FIN DE LA DEMOSTRACIÓN")
    print("="*80)

if __name__ == '__main__':
    main()
