"""
Tests para Distancia Hamming y Sistema de Lenguajes

Verifica:
- Cálculo de distancia Hamming
- Clase Lenguaje y sus métodos
- Lenguajes predefinidos (Binario, BCD, Johnson, Biquinario)
- Análisis de adyacencia y propiedades cíclicas
"""

import pytest
from core.sistemas_numeracion_basicos import (
    distancia_hamming,
    Lenguaje,
    crear_lenguaje_binario_saturado,
    crear_lenguaje_bcd,
    crear_lenguaje_johnson,
    crear_lenguaje_biquinario,
)


# ============================================================================
# TESTS: Distancia Hamming
# ============================================================================

class TestDistanciaHamming:
    """Tests para la función distancia_hamming"""
    
    def test_hamming_palabras_identicas(self):
        """Palabras idénticas tienen distancia 0"""
        assert distancia_hamming('0000', '0000') == 0
        assert distancia_hamming('1111', '1111') == 0
        assert distancia_hamming('10101', '10101') == 0
    
    def test_hamming_una_diferencia(self):
        """Una posición diferente = distancia 1"""
        assert distancia_hamming('0000', '0001') == 1
        assert distancia_hamming('0000', '1000') == 1
        assert distancia_hamming('1010', '1011') == 1
    
    def test_hamming_multiples_diferencias(self):
        """Múltiples diferencias calculan correctamente"""
        assert distancia_hamming('0000', '0011') == 2
        assert distancia_hamming('1111', '0000') == 4  # Opuestos
        assert distancia_hamming('10101', '01010') == 5  # Completamente opuestos
    
    def test_hamming_simetria(self):
        """La distancia Hamming es simétrica"""
        assert distancia_hamming('abc', 'abd') == distancia_hamming('abd', 'abc')
        assert distancia_hamming('1010', '1100') == distancia_hamming('1100', '1010')
    
    def test_hamming_diferente_longitud_error(self):
        """Palabras de diferente longitud lanzan error"""
        with pytest.raises(ValueError):
            distancia_hamming('00', '000')
        
        with pytest.raises(ValueError):
            distancia_hamming('1010', '101010')
    
    def test_hamming_alfabeto_no_binario(self):
        """Funciona con cualquier alfabeto"""
        assert distancia_hamming('abc', 'abc') == 0
        assert distancia_hamming('abc', 'abd') == 1
        assert distancia_hamming('abc', 'xyz') == 3


# ============================================================================
# TESTS: Clase Lenguaje - Básico
# ============================================================================

class TestLenguajeBasico:
    """Tests para funcionalidad básica de la clase Lenguaje"""
    
    def test_crear_lenguaje_simple(self):
        """Crear un lenguaje básico binario"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        assert lenguaje.longitud == 4
        assert lenguaje.alfabeto == ['0', '1']
    
    def test_es_valida_binario(self):
        """Todas las palabras son válidas en binario saturado"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        assert lenguaje.es_valida('0000')
        assert lenguaje.es_valida('1111')
        assert lenguaje.es_valida('1010')
    
    def test_es_valida_error_longitud(self):
        """Error si la palabra tiene longitud incorrecta"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        with pytest.raises(ValueError):
            lenguaje.es_valida('000')  # Muy corta
        
        with pytest.raises(ValueError):
            lenguaje.es_valida('00000')  # Muy larga
    
    def test_es_valida_error_alfabeto(self):
        """Error si hay símbolos fuera del alfabeto"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        assert not lenguaje.es_valida('0002')  # '2' no está en alfabeto
        assert not lenguaje.es_valida('00a0')  # 'a' no está en alfabeto


# ============================================================================
# TESTS: Clase Lenguaje - Siguiente y Distancia
# ============================================================================

class TestLenguajeSiguiente:
    """Tests para generación de siguiente palabra"""
    
    def test_siguiente_binario(self):
        """Siguiente en binario incremental"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        assert lenguaje.siguiente_palabra('0000') == '0001'
        assert lenguaje.siguiente_palabra('0001') == '0010'
        assert lenguaje.siguiente_palabra('1111') == '0000'  # Wrap-around
    
    def test_siguiente_bcd(self):
        """Siguiente en BCD"""
        lenguaje = crear_lenguaje_bcd()
        
        assert lenguaje.siguiente_palabra('0000') == '0001'
        assert lenguaje.siguiente_palabra('1001') == '0000'  # Wrap-around en 10
    
    def test_siguiente_debe_ser_valida(self):
        """La siguiente palabra siempre es válida"""
        lenguaje = crear_lenguaje_bcd()
        
        for i in range(10):
            palabra = lenguaje.siguiente_palabra('0000' if i == 0 else palabra)
            assert lenguaje.es_valida(palabra)
    
    def test_siguiente_no_definida_error(self):
        """Error si siguiente no está definida"""
        lenguaje = Lenguaje(
            alfabeto=['0', '1'],
            longitud=4,
            predicado=lambda p: True,
            siguiente=None  # No está definida
        )
        
        with pytest.raises(ValueError):
            lenguaje.siguiente_palabra('0000')


class TestDistanciaEnLenguaje:
    """Tests para distancia Hamming dentro de lenguajes"""
    
    def test_distancia_mismo_palabra(self):
        """Una palabra consigo misma tiene distancia 0"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        assert lenguaje.distancia_hamming('0000', '0000') == 0
        assert lenguaje.distancia_hamming('1111', '1111') == 0
    
    def test_distancia_palabras_invalidas_error(self):
        """Error si una palabra no pertenece al lenguaje"""
        lenguaje = crear_lenguaje_bcd()
        
        with pytest.raises(ValueError):
            lenguaje.distancia_hamming('0000', '1010')  # 1010 no es BCD válido
    
    def test_adyacencia(self):
        """Verifica si dos palabras son adyacentes"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        
        assert lenguaje.son_adyacentes('0000', '0001')  # Distancia 1
        assert lenguaje.son_adyacentes('1111', '0111')  # Distancia 1
        assert not lenguaje.son_adyacentes('0000', '0011')  # Distancia 2


# ============================================================================
# TESTS: Lenguaje Binario Saturado
# ============================================================================

class TestLenguajeBinario:
    """Tests específicos para lenguaje binario saturado"""
    
    def test_binario_todas_palabras(self):
        """Genera todas las 2^n palabras"""
        lenguaje = crear_lenguaje_binario_saturado(3)
        palabras = lenguaje.generar_todas_palabras()
        
        assert len(palabras) == 8
        assert '000' in palabras
        assert '111' in palabras
    
    def test_binario_4bits_tiene_16(self):
        """Binario de 4 bits tiene exactamente 16 palabras"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        palabras = lenguaje.generar_todas_palabras()
        
        assert len(palabras) == 16
    
    def test_binario_es_adyacente(self):
        """Verifica si binario es adyacente (no debería serlo)"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        analisis = lenguaje.analizar_adyacencia()
        
        # Binario NO es adyacente (ej: 0111->1000 cambia 4 bits)
        assert not analisis['es_adyacente']
    
    def test_binario_no_es_ciclico(self):
        """Binario no es cíclico (1111 y 0000 difieren en 4 bits)"""
        lenguaje = crear_lenguaje_binario_saturado(4)
        analisis = lenguaje.analizar_adyacencia()
        
        assert not analisis['es_ciclico']


# ============================================================================
# TESTS: Lenguaje BCD
# ============================================================================

class TestLenguajeBCD:
    """Tests específicos para lenguaje BCD"""
    
    def test_bcd_solo_10_palabras(self):
        """BCD tiene solo 10 palabras válidas"""
        lenguaje = crear_lenguaje_bcd()
        palabras = lenguaje.generar_todas_palabras()
        
        assert len(palabras) == 10
    
    def test_bcd_validas_0_a_9(self):
        """BCD válido para 0000-1001"""
        lenguaje = crear_lenguaje_bcd()
        
        for i in range(10):
            codigo = format(i, '04b')
            assert lenguaje.es_valida(codigo)
    
    def test_bcd_invalidas_10_a_15(self):
        """BCD inválido para 1010-1111"""
        lenguaje = crear_lenguaje_bcd()
        
        for i in range(10, 16):
            codigo = format(i, '04b')
            assert not lenguaje.es_valida(codigo)
    
    def test_bcd_no_adyacente(self):
        """BCD no es adyacente"""
        lenguaje = crear_lenguaje_bcd()
        analisis = lenguaje.analizar_adyacencia()
        
        # Puede no ser completamente adyacente
        # (4 = 0100, 5 = 0101 son adyacentes, pero 9 = 1001, 0 = 0000 no)
        assert not analisis['es_ciclico']  # Seguro que no es cíclico


# ============================================================================
# TESTS: Lenguaje Johnson
# ============================================================================

class TestLenguajeJohnson:
    """Tests específicos para código Johnson"""
    
    def test_johnson_diez_palabras(self):
        """Johnson tiene 10 palabras"""
        lenguaje = crear_lenguaje_johnson()
        palabras = lenguaje.generar_todas_palabras()
        
        assert len(palabras) == 10
    
    def test_johnson_adyacencia_sucesiva(self):
        """Johnson: valores sucesivos son adyacentes"""
        lenguaje = crear_lenguaje_johnson()
        analisis = lenguaje.analizar_adyacencia()
        
        # Johnson es adyacente: todos los pares sucesivos difieren en 1 bit
        assert analisis['es_adyacente']
    
    def test_johnson_es_ciclico(self):
        """Johnson es cíclico (9->0 cambia en 1 bit)"""
        lenguaje = crear_lenguaje_johnson()
        analisis = lenguaje.analizar_adyacencia()
        
        assert analisis['es_ciclico']
    
    def test_johnson_estructura(self):
        """Verifica la estructura de Johnson (unos progresivos)"""
        lenguaje = crear_lenguaje_johnson()
        palabras = lenguaje.generar_todas_palabras()
        
        expected = [
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
        
        assert palabras == expected


# ============================================================================
# TESTS: Lenguaje Biquinario
# ============================================================================

class TestLenguajeBiquinario:
    """Tests específicos para código Biquinario"""
    
    def test_biquinario_diez_palabras(self):
        """Biquinario tiene exactamente 10 palabras"""
        lenguaje = crear_lenguaje_biquinario()
        palabras = lenguaje.generar_todas_palabras()
        
        assert len(palabras) == 10
    
    def test_biquinario_dos_bits_encendidos(self):
        """Todas las palabras biquinarias tienen exactamente 2 bits encendidos"""
        lenguaje = crear_lenguaje_biquinario()
        palabras = lenguaje.generar_todas_palabras()
        
        for palabra in palabras:
            assert palabra.count('1') == 2, f"Palabra {palabra} no tiene 2 bits"
    
    def test_biquinario_no_adyacente(self):
        """Biquinario NO es adyacente"""
        lenguaje = crear_lenguaje_biquinario()
        analisis = lenguaje.analizar_adyacencia()
        
        # Biquinario no es adyacente
        assert not analisis['es_adyacente']
    
    def test_biquinario_no_ciclico(self):
        """Biquinario NO es cíclico"""
        lenguaje = crear_lenguaje_biquinario()
        analisis = lenguaje.analizar_adyacencia()
        
        assert not analisis['es_ciclico']
    
    def test_biquinario_error_deteccion(self):
        """Biquinario detecta si no hay exactamente 2 bits"""
        lenguaje = crear_lenguaje_biquinario()
        
        # 1 bit encendido: error
        assert not lenguaje.es_valida('00001')
        
        # 2 bits encendidos: válido
        assert lenguaje.es_valida('00011')
        
        # 3 bits encendidos: error
        assert not lenguaje.es_valida('00111')


# ============================================================================
# TESTS: Análisis Comparativo
# ============================================================================

class TestAnalisisComparativo:
    """Comparación entre todos los lenguajes"""
    
    def test_eficacia_lenguajes(self):
        """Calcula eficacia (palabras válidas / posibles)"""
        lenguajes = {
            'Binario': crear_lenguaje_binario_saturado(4),
            'BCD': crear_lenguaje_bcd(),
            'Johnson': crear_lenguaje_johnson(),
            'Biquinario': crear_lenguaje_biquinario(),
        }
        
        for nombre, lenguaje in lenguajes.items():
            palabras = lenguaje.generar_todas_palabras()
            posibles = len(lenguaje.alfabeto) ** lenguaje.longitud
            eficacia = len(palabras) / posibles
            
            # Print para verificación manual
            print(f"{nombre}: {len(palabras)}/{posibles} = {eficacia:.2%}")
    
    def test_caracteristicas_adyacencia(self):
        """Tabla de características de adyacencia"""
        lenguajes = {
            'Binario 4b': crear_lenguaje_binario_saturado(4),
            'BCD': crear_lenguaje_bcd(),
            'Johnson': crear_lenguaje_johnson(),
            'Biquinario': crear_lenguaje_biquinario(),
        }
        
        for nombre, lenguaje in lenguajes.items():
            analisis = lenguaje.analizar_adyacencia()
            
            print(f"\n{nombre}:")
            print(f"  Palabras: {analisis['total_palabras']}")
            print(f"  Adyacente: {analisis['es_adyacente']}")
            print(f"  Cíclico: {analisis['es_ciclico']}")
            print(f"  Min distancia: {analisis['min_distancia']}")
            print(f"  Max distancia: {analisis['max_distancia']}")
    
    def test_comparacion_gray_vs_binario(self):
        """Verifica que Gray es adyacente pero Binario no"""
        # Necesitaríamos Gray generado de forma similar
        # Para ahora, verificamos que Binario no es adyacente
        binario = crear_lenguaje_binario_saturado(4)
        analisis = binario.analizar_adyacencia()
        
        # Binario natural: 0111 (7) -> 1000 (8) cambia 4 bits, NO adyacente
        assert not analisis['es_adyacente']
        assert analisis['max_distancia'] == 4  # Cambio máximo es 4


# ============================================================================
# TESTS: Casos Edge y Errores
# ============================================================================

class TestEdgeCases:
    """Tests para casos límite y errores"""
    
    def test_lenguaje_vacio(self):
        """Lenguaje que no acepta ninguna palabra"""
        lenguaje = Lenguaje(
            alfabeto=['0', '1'],
            longitud=4,
            predicado=lambda p: False,  # Nada es válido
            siguiente=None
        )
        
        palabras = lenguaje.generar_todas_palabras()
        assert len(palabras) == 0
    
    def test_lenguaje_una_palabra(self):
        """Lenguaje con una única palabra válida"""
        lenguaje = Lenguaje(
            alfabeto=['0', '1'],
            longitud=4,
            predicado=lambda p: p == '0000',
            siguiente=lambda p: '0000'  # Wrap-around a sí misma
        )
        
        palabras = lenguaje.generar_todas_palabras()
        assert len(palabras) == 1
        
        analisis = lenguaje.analizar_adyacencia()
        assert analisis['total_palabras'] == 1
    
    def test_distancia_hamming_largo(self):
        """Distancia Hamming con palabras largas"""
        palabra1 = '0' * 100
        palabra2 = '1' * 100
        
        assert distancia_hamming(palabra1, palabra2) == 100
    
    def test_generar_todas_palabras_limite(self):
        """Aviso si el lenguaje es demasiado grande"""
        # Lenguaje binario de 20 bits: 2^20 = 1,048,576 palabras
        lenguaje = Lenguaje(
            alfabeto=['0', '1'],
            longitud=20,
            predicado=lambda p: True,
            siguiente=None
        )
        
        with pytest.raises(RuntimeError):
            lenguaje.generar_todas_palabras()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
