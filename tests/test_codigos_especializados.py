"""
Tests para códigos especializados (Biquinario, Johnson, Gray)

Verifica conversiones, propiedades y eficacias de empaquetado.
"""

import pytest
from core.sistemas_numeracion_basicos import (
    biquinario_a_entero,
    johnson_a_entero,
    entero_a_gray_4bits,
    gray_4bits_a_entero,
    analisis_codigo_especializado,
    comparar_codigos_5bits,
    CODIGO_BIQUINARIO,
    CODIGO_JOHNSON,
    CODIGO_GRAY_4BITS
)


class TestBiquinario:
    """Tests para código biquinario (2 entre 5)"""
    
    def test_biquinario_basico(self):
        """Conversión básica biquinario a entero"""
        assert biquinario_a_entero('00110') == 0
        assert biquinario_a_entero('01010') == 1
        assert biquinario_a_entero('01100') == 2
        assert biquinario_a_entero('10010') == 3
    
    def test_biquinario_todos_valores(self):
        """Todos los valores 0-9 funcionan"""
        for valor in range(10):
            codigo = CODIGO_BIQUINARIO[valor]
            assert biquinario_a_entero(codigo) == valor
    
    def test_biquinario_dos_bits_encendidos(self):
        """Verifica que exactamente 2 bits estén encendidos"""
        for codigo in CODIGO_BIQUINARIO.values():
            assert codigo.count('1') == 2, f"Código {codigo} no tiene exactamente 2 bits encendidos"
    
    def test_biquinario_inválido_un_bit(self):
        """Rechaza código con un solo bit encendido"""
        with pytest.raises(ValueError):
            biquinario_a_entero('00001')
    
    def test_biquinario_inválido_tres_bits(self):
        """Rechaza código con tres bits encendidos"""
        with pytest.raises(ValueError):
            biquinario_a_entero('00111')
    
    def test_biquinario_inválido_longitud(self):
        """Rechaza código de longitud incorrecta"""
        with pytest.raises(ValueError):
            biquinario_a_entero('001001')
    
    def test_biquinario_inválido_caracteres(self):
        """Rechaza caracteres inválidos"""
        with pytest.raises(ValueError):
            biquinario_a_entero('001a1')
    
    def test_biquinario_tabla_completa(self):
        """Verifica tabla CODIGO_BIQUINARIO"""
        assert len(CODIGO_BIQUINARIO) == 10
        assert CODIGO_BIQUINARIO[0] == '00110'
        assert CODIGO_BIQUINARIO[5] == '11000'
        assert CODIGO_BIQUINARIO[9] == '00011'
    
    def test_biquinario_eficacia(self):
        """Eficacia de biquinario = 10/32 = 31.25%"""
        capacidad = len(CODIGO_BIQUINARIO)
        bits = len(CODIGO_BIQUINARIO[0])
        eficacia = capacidad / (2 ** bits)
        assert abs(eficacia - 0.3125) < 0.0001


class TestJohnson:
    """Tests para código Johnson (cíclico)"""
    
    def test_johnson_basico(self):
        """Conversión básica Johnson a entero"""
        assert johnson_a_entero('00000') == 0
        assert johnson_a_entero('00001') == 1
        assert johnson_a_entero('00011') == 2
        assert johnson_a_entero('00111') == 3
    
    def test_johnson_todos_valores(self):
        """Todos los valores 0-9 funcionan"""
        for valor in range(10):
            codigo = CODIGO_JOHNSON[valor]
            assert johnson_a_entero(codigo) == valor
    
    def test_johnson_adyacencia(self):
        """Valores adyacentes difieren en exactamente 1 bit"""
        for valor in range(10):
            codigo_actual = CODIGO_JOHNSON[valor]
            codigo_siguiente = CODIGO_JOHNSON[(valor + 1) % 10]
            
            # Contar bits diferentes
            diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_actual, codigo_siguiente))
            assert diferencias == 1, f"Johnson {valor}→{(valor+1)%10} no es adyacente"
    
    def test_johnson_ciclico(self):
        """Último valor (9) se envuelve al primero (0) en 1 bit"""
        codigo_0 = CODIGO_JOHNSON[0]      # '00000'
        codigo_9 = CODIGO_JOHNSON[9]      # '10000'
        
        diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_0, codigo_9))
        assert diferencias == 1, "Johnson no es cíclico"
    
    def test_johnson_estructura(self):
        """Verifica estructura: 0s seguidos de 1s para primeros valores"""
        assert CODIGO_JOHNSON[0] == '00000'
        assert CODIGO_JOHNSON[1] == '00001'
        assert CODIGO_JOHNSON[2] == '00011'
        assert CODIGO_JOHNSON[3] == '00111'
        assert CODIGO_JOHNSON[4] == '01111'
        assert CODIGO_JOHNSON[5] == '11111'
    
    def test_johnson_inválido(self):
        """Rechaza códigos inválidos"""
        with pytest.raises(ValueError):
            johnson_a_entero('10101')  # No es válido Johnson
    
    def test_johnson_tabla_completa(self):
        """Verifica tabla CODIGO_JOHNSON"""
        assert len(CODIGO_JOHNSON) == 10
        assert CODIGO_JOHNSON[0] == '00000'
        assert CODIGO_JOHNSON[9] == '10000'
    
    def test_johnson_eficacia(self):
        """Eficacia de Johnson = 10/32 = 31.25%"""
        capacidad = len(CODIGO_JOHNSON)
        bits = len(CODIGO_JOHNSON[0])
        eficacia = capacidad / (2 ** bits)
        assert abs(eficacia - 0.3125) < 0.0001


class TestGray4Bits:
    """Tests para código Gray de 4 bits"""
    
    def test_gray_basico(self):
        """Conversión básica entero a Gray"""
        assert entero_a_gray_4bits(0) == '0000'
        assert entero_a_gray_4bits(1) == '0001'
        assert entero_a_gray_4bits(2) == '0011'
        assert entero_a_gray_4bits(3) == '0010'
    
    def test_gray_todos_valores(self):
        """Todos los valores 0-15 funcionan"""
        for valor in range(16):
            codigo = entero_a_gray_4bits(valor)
            assert gray_4bits_a_entero(codigo) == valor
    
    def test_gray_inversa(self):
        """Gray a entero es inversa de entero a Gray"""
        for valor in range(16):
            codigo = entero_a_gray_4bits(valor)
            restaurado = gray_4bits_a_entero(codigo)
            assert restaurado == valor, f"Gray no es biyectivo para {valor}"
    
    def test_gray_tabla_completa(self):
        """Verifica tabla CODIGO_GRAY_4BITS"""
        assert len(CODIGO_GRAY_4BITS) == 16
        assert CODIGO_GRAY_4BITS[0] == '0000'
        assert CODIGO_GRAY_4BITS[15] == '1000'
    
    def test_gray_adyacencia(self):
        """Valores adyacentes difieren en exactamente 1 bit"""
        for valor in range(16):
            codigo_actual = entero_a_gray_4bits(valor)
            codigo_siguiente = entero_a_gray_4bits((valor + 1) % 16)
            
            diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_actual, codigo_siguiente))
            assert diferencias == 1, f"Gray {valor}→{(valor+1)%16} no es adyacente"
    
    def test_gray_ciclico(self):
        """Último valor (15) se envuelve al primero (0) en 1 bit"""
        codigo_0 = entero_a_gray_4bits(0)   # '0000'
        codigo_15 = entero_a_gray_4bits(15) # '1000'
        
        diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_0, codigo_15))
        assert diferencias == 1, "Gray no es cíclico"
    
    def test_gray_especular(self):
        """Verifica simetría especular (reflejada)"""
        # Primera mitad (0-7)
        primeros = [entero_a_gray_4bits(i) for i in range(8)]
        # Segunda mitad (8-15) invertida
        segundos = [entero_a_gray_4bits(i) for i in range(15, 7, -1)]
        
        # En código Gray reflejado, la segunda mitad es negación de la primera
        for i in range(8):
            primero = primeros[i]
            segundo = segundos[i]
            # Verificar que primer bit es diferente (reflejo)
            assert primero[0] != segundo[0], f"Gray no es especular en posición {i}"
    
    def test_gray_valores_especificos(self):
        """Verifica valores específicos conocidos"""
        assert entero_a_gray_4bits(0) == '0000'
        assert entero_a_gray_4bits(1) == '0001'
        assert entero_a_gray_4bits(2) == '0011'
        assert entero_a_gray_4bits(3) == '0010'
        assert entero_a_gray_4bits(4) == '0110'
        assert entero_a_gray_4bits(5) == '0111'
        assert entero_a_gray_4bits(6) == '0101'
        assert entero_a_gray_4bits(7) == '0100'
        assert entero_a_gray_4bits(8) == '1100'
        assert entero_a_gray_4bits(15) == '1000'
    
    def test_gray_inválido_fuera_rango(self):
        """Rechaza valores fuera de rango"""
        with pytest.raises(ValueError):
            entero_a_gray_4bits(16)
        with pytest.raises(ValueError):
            entero_a_gray_4bits(-1)
    
    def test_gray_inválido_tipo(self):
        """Rechaza tipos inválidos"""
        with pytest.raises((ValueError, TypeError)):
            entero_a_gray_4bits("cinco")
    
    def test_gray_entero_inválido_longitud(self):
        """Rechaza Gray de longitud incorrecta"""
        with pytest.raises(ValueError):
            gray_4bits_a_entero('00001')
    
    def test_gray_entero_inválido_caracteres(self):
        """Rechaza caracteres inválidos"""
        with pytest.raises(ValueError):
            gray_4bits_a_entero('001a')
    
    def test_gray_eficacia(self):
        """Eficacia de Gray 4-bit = 16/16 = 100%"""
        capacidad = len(CODIGO_GRAY_4BITS)
        bits = len(CODIGO_GRAY_4BITS[0])
        eficacia = capacidad / (2 ** bits)
        assert abs(eficacia - 1.0) < 0.0001


class TestAnalisisCodigoEspecializado:
    """Tests para función de análisis"""
    
    def test_analisis_biquinario(self):
        """Análisis completo de biquinario"""
        resultado = analisis_codigo_especializado('00110', 'biquinario')
        
        assert resultado['tipo'] == 'biquinario'
        assert resultado['codigo'] == '00110'
        assert resultado['valor'] == 0
        assert resultado['capacidad'] == 10
        assert abs(resultado['eficacia'] - 0.3125) < 0.0001
    
    def test_analisis_johnson(self):
        """Análisis completo de Johnson"""
        resultado = analisis_codigo_especializado('00001', 'johnson')
        
        assert resultado['tipo'] == 'johnson'
        assert resultado['codigo'] == '00001'
        assert resultado['valor'] == 1
        assert resultado['capacidad'] == 10
        assert abs(resultado['eficacia'] - 0.3125) < 0.0001
        assert 'Adyacente' in resultado['caracteristicas'][1]
        assert 'Cíclico' in resultado['caracteristicas'][0] or 'cíclico' in str(resultado['caracteristicas']).lower()
    
    def test_analisis_gray(self):
        """Análisis completo de Gray"""
        resultado = analisis_codigo_especializado('0011', 'gray')
        
        assert resultado['tipo'] == 'gray'
        assert resultado['codigo'] == '0011'
        assert resultado['valor'] == 2
        assert resultado['capacidad'] == 16
        assert abs(resultado['eficacia'] - 1.0) < 0.0001
        assert 'reflejado' in str(resultado['caracteristicas']).lower()
    
    def test_analisis_tipo_inválido(self):
        """Rechaza tipos inválidos"""
        with pytest.raises(ValueError):
            analisis_codigo_especializado('00100', 'invalido')


class TestCompararCodigos:
    """Tests para función de comparación"""
    
    def test_comparar_estructura(self):
        """Comparación retorna dict con todos los códigos"""
        resultado = comparar_codigos_5bits()
        
        assert 'biquinario' in resultado
        assert 'johnson' in resultado
        assert 'gray_4bits' in resultado
    
    def test_comparar_biquinario_propiedades(self):
        """Verifica propiedades de biquinario en comparación"""
        resultado = comparar_codigos_5bits()
        biqu = resultado['biquinario']
        
        assert biqu['nombre'] == 'Código Biquinario (2 entre 5)'
        assert biqu['capacidad'] == 10
        assert biqu['bits'] == 5
        assert abs(biqu['eficacia'] - 0.3125) < 0.0001
    
    def test_comparar_johnson_propiedades(self):
        """Verifica propiedades de Johnson en comparación"""
        resultado = comparar_codigos_5bits()
        john = resultado['johnson']
        
        assert john['nombre'] == 'Código Johnson (Cíclico)'
        assert john['capacidad'] == 10
        assert john['bits'] == 5
        assert abs(john['eficacia'] - 0.3125) < 0.0001
        assert john['adyacente'] is True
        assert john['ciclico'] is True
    
    def test_comparar_gray_propiedades(self):
        """Verifica propiedades de Gray en comparación"""
        resultado = comparar_codigos_5bits()
        gray = resultado['gray_4bits']
        
        assert gray['nombre'] == 'Código Gray (4 bits)'
        assert gray['capacidad'] == 16
        assert gray['bits'] == 4
        assert abs(gray['eficacia'] - 1.0) < 0.0001
        assert gray['especular'] is True
        assert gray['adyacente'] is True
        assert gray['ciclico'] is True


class TestEquivalenciasEntreCodigos:
    """Tests de equivalencia y propiedades cruzadas"""
    
    def test_ambos_5bits_misma_eficacia(self):
        """Biquinario y Johnson tienen la misma eficacia"""
        biqu_cap = len(CODIGO_BIQUINARIO)
        john_cap = len(CODIGO_JOHNSON)
        
        bits = 5
        eficacia_biqu = biqu_cap / (2 ** bits)
        eficacia_john = john_cap / (2 ** bits)
        
        assert abs(eficacia_biqu - eficacia_john) < 0.0001
    
    def test_gray_mas_eficiente(self):
        """Gray es 100% eficiente, codes 5-bit son 31.25%"""
        eficacia_5bits = 10 / 32
        eficacia_gray = 16 / 16
        
        assert eficacia_gray > eficacia_5bits
        assert abs(eficacia_gray - 1.0) < 0.0001
    
    def test_biquinario_detecta_errores_johnson_no(self):
        """Biquinario puede detectar errores, Johnson no"""
        # Biquinario con error (no tiene exactamente 2 bits)
        codigo_error = '00001'  # Un solo 1
        
        with pytest.raises(ValueError):
            biquinario_a_entero(codigo_error)
        
        # Johnson con error (código inválido)
        with pytest.raises(ValueError):
            johnson_a_entero('10101')
    
    def test_johnson_gray_ambos_adyacentes(self):
        """Johnson y Gray tienen propiedad adyacente"""
        # Johnson: verificar adyacencia
        for valor in range(10):
            codigo_j = CODIGO_JOHNSON[valor]
            codigo_j_next = CODIGO_JOHNSON[(valor + 1) % 10]
            diff_j = sum(c1 != c2 for c1, c2 in zip(codigo_j, codigo_j_next))
            assert diff_j == 1
        
        # Gray: verificar adyacencia
        for valor in range(16):
            codigo_g = entero_a_gray_4bits(valor)
            codigo_g_next = entero_a_gray_4bits((valor + 1) % 16)
            diff_g = sum(c1 != c2 for c1, c2 in zip(codigo_g, codigo_g_next))
            assert diff_g == 1
    
    def test_gray_es_especular(self):
        """Gray tiene propiedad especular, otros no"""
        # Verificar que Gray es especular/reflejado
        for i in range(8):
            gray_i = entero_a_gray_4bits(i)
            gray_15_minus_i = entero_a_gray_4bits(15 - i)
            
            # En código Gray reflejado, primer bit debe ser diferente
            assert gray_i[0] != gray_15_minus_i[0]


class TestEdgeCases:
    """Tests de casos límite"""
    
    def test_gray_codigos_consecutivos_diferentes(self):
        """Todos los códigos Gray consecutivos son diferentes"""
        codigos = set()
        for i in range(16):
            codigo = entero_a_gray_4bits(i)
            assert codigo not in codigos, f"Código Gray duplicado para {i}"
            codigos.add(codigo)
    
    def test_johnson_codigos_consecutivos_diferentes(self):
        """Todos los códigos Johnson consecutivos son diferentes"""
        codigos = set(CODIGO_JOHNSON.values())
        assert len(codigos) == 10
    
    def test_biquinario_codigos_consecutivos_diferentes(self):
        """Todos los códigos Biquinario consecutivos son diferentes"""
        codigos = set(CODIGO_BIQUINARIO.values())
        assert len(codigos) == 10
    
    def test_gray_simetria_visual(self):
        """Primera y segunda mitad de Gray son simétricas"""
        primeros_bits = [entero_a_gray_4bits(i)[0] for i in range(8)]
        segundos_bits = [entero_a_gray_4bits(i)[0] for i in range(8, 16)]
        
        # Primer bit de 0-7 debe ser inverso de 8-15
        for i in range(8):
            assert primeros_bits[i] != segundos_bits[i]


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
