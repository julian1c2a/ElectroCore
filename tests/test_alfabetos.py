"""
test_alfabetos.py

Tests completos para el modulo de alfabetos.

Cubre:
- Alfabetos explicitos
- Alfabetos estandar
- Alfabeto binario
- Alfabetos predefinidos
- Alfabetos jerarquicos
- Operaciones y comparaciones
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from core.alfabetos import (
    Alfabeto,
    AlfabetoExplicito,
    AlfabetoEstandar,
    AlfabetoBinario,
    AlfabetosPredefinidos,
    AlfabetoDesdeLenguaje,
    crear_alfabeto_explicito,
    crear_alfabeto_estandar_desde_cardinal,
    unir_alfabetos
)
from core.lenguajes import LenguajeUniverso, LenguajeExplicito


class TestAlfabetoExplicito:
    """Tests para AlfabetoExplicito."""
    
    def test_creacion_basica(self):
        """Test de creación básica con símbolos."""
        alf = AlfabetoExplicito('a', 'b', 'c')
        assert alf.cardinal == 3
        assert alf.simbolos == ['a', 'b', 'c']
    
    def test_indices_correctos(self):
        """Test de asignación de índices."""
        alf = AlfabetoExplicito('x', 'y', 'z')
        assert alf.indice_de('x') == 0
        assert alf.indice_de('y') == 1
        assert alf.indice_de('z') == 2
    
    def test_contiene_simbolo(self):
        """Test de pertenencia de símbolos."""
        alf = AlfabetoExplicito('0', '1', '2')
        assert alf.contiene('0')
        assert alf.contiene('1')
        assert not alf.contiene('3')
        assert not alf.contiene('a')
    
    def test_validar_palabra(self):
        """Test de validación de palabras."""
        alf = AlfabetoExplicito('a', 'b')
        assert alf.validar_palabra('aabba')
        assert alf.validar_palabra('')  # Palabra vacía válida
        assert not alf.validar_palabra('abc')  # 'c' no está
    
    def test_generar_palabras_longitud_0(self):
        """Test de generación de palabra vacía."""
        alf = AlfabetoExplicito('0', '1')
        palabras = alf.generar_palabras(0)
        assert palabras == ['']
    
    def test_generar_palabras_longitud_1(self):
        """Test de generación de palabras de longitud 1."""
        alf = AlfabetoExplicito('a', 'b')
        palabras = alf.generar_palabras(1)
        assert set(palabras) == {'a', 'b'}
    
    def test_generar_palabras_longitud_2(self):
        """Test de generación de palabras de longitud 2."""
        alf = AlfabetoExplicito('0', '1')
        palabras = alf.generar_palabras(2)
        assert set(palabras) == {'00', '01', '10', '11'}
    
    def test_simbolo_en_posicion(self):
        """Test de acceso a símbolo por índice."""
        alf = AlfabetoExplicito('x', 'y', 'z')
        assert alf.simbolo_en(0) == 'x'
        assert alf.simbolo_en(1) == 'y'
        assert alf.simbolo_en(2) == 'z'
    
    def test_simbolo_en_fuera_de_rango(self):
        """Test de acceso fuera de rango."""
        alf = AlfabetoExplicito('a', 'b')
        with pytest.raises(IndexError):
            alf.simbolo_en(5)
    
    def test_alfabeto_vacio_invalido(self):
        """Test que no se puede crear alfabeto vacío."""
        with pytest.raises(ValueError):
            AlfabetoExplicito()
    
    def test_simbolos_duplicados_ignorados(self):
        """Test que símbolos duplicados se ignoran."""
        alf = AlfabetoExplicito('a', 'b', 'a', 'c', 'b')
        assert alf.cardinal == 3
        assert set(alf.simbolos) == {'a', 'b', 'c'}


class TestAlfabetoEstandar:
    """Tests para AlfabetoEstandar."""
    
    def test_binario(self):
        """Test alfabeto binario base 2."""
        alf = AlfabetoEstandar(2)
        assert alf.cardinal == 2
        assert alf.simbolos == ['0', '1']
    
    def test_octal(self):
        """Test alfabeto octal base 8."""
        alf = AlfabetoEstandar(8)
        assert alf.cardinal == 8
        assert alf.simbolos == ['0', '1', '2', '3', '4', '5', '6', '7']
    
    def test_decimal(self):
        """Test alfabeto decimal base 10."""
        alf = AlfabetoEstandar(10)
        assert alf.cardinal == 10
        assert alf.simbolos == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    def test_hexadecimal_mayusculas(self):
        """Test alfabeto hexadecimal con mayúsculas."""
        alf = AlfabetoEstandar(16, mayusculas=True)
        assert alf.cardinal == 16
        assert 'A' in alf.simbolos
        assert 'F' in alf.simbolos
        assert 'a' not in alf.simbolos
    
    def test_hexadecimal_minusculas(self):
        """Test alfabeto hexadecimal con minúsculas."""
        alf = AlfabetoEstandar(16, mayusculas=False)
        assert 'a' in alf.simbolos
        assert 'f' in alf.simbolos
        assert 'A' not in alf.simbolos
    
    def test_base_maxima(self):
        """Test base máxima permitida (36)."""
        alf = AlfabetoEstandar(36)
        assert alf.cardinal == 36
        assert '0' in alf.simbolos
        assert '9' in alf.simbolos
        assert 'Z' in alf.simbolos
    
    def test_base_invalida_menor(self):
        """Test base menor a 2 no válida."""
        with pytest.raises(ValueError):
            AlfabetoEstandar(1)
    
    def test_base_invalida_mayor(self):
        """Test base mayor a 36 no válida."""
        with pytest.raises(ValueError):
            AlfabetoEstandar(37)
    
    def test_valor_numerico(self):
        """Test de conversión de símbolo a valor numérico."""
        alf = AlfabetoEstandar(16)
        assert alf.valor_numerico('0') == 0
        assert alf.valor_numerico('9') == 9
        assert alf.valor_numerico('A') == 10
        assert alf.valor_numerico('F') == 15


class TestAlfabetoBinario:
    """Tests para AlfabetoBinario especializado."""
    
    def test_creacion(self):
        """Test de creación de alfabeto binario."""
        alf = AlfabetoBinario()
        assert alf.cardinal == 2
        assert alf.simbolos == ['0', '1']
    
    def test_indices_fijos(self):
        """Test que índices son 0 y 1 exactamente."""
        alf = AlfabetoBinario()
        assert alf.indice_de('0') == 0
        assert alf.indice_de('1') == 1
    
    def test_valor_numerico(self):
        """Test de valores numéricos."""
        alf = AlfabetoBinario()
        assert alf.valor_numerico('0') == 0
        assert alf.valor_numerico('1') == 1


class TestAlfabetosPredefinidos:
    """Tests para alfabetos predefinidos."""
    
    def test_binario(self):
        """Test alfabeto binario predefinido."""
        alf = AlfabetosPredefinidos.binario()
        assert isinstance(alf, AlfabetoBinario)
        assert alf.cardinal == 2
    
    def test_octal(self):
        """Test alfabeto octal predefinido."""
        alf = AlfabetosPredefinidos.octal()
        assert alf.cardinal == 8
    
    def test_decimal(self):
        """Test alfabeto decimal predefinido."""
        alf = AlfabetosPredefinidos.decimal()
        assert alf.cardinal == 10
    
    def test_hexadecimal(self):
        """Test alfabeto hexadecimal predefinido."""
        alf = AlfabetosPredefinidos.hexadecimal()
        assert alf.cardinal == 16
        assert 'A' in alf.simbolos
    
    def test_bcd(self):
        """Test alfabeto BCD predefinido."""
        alf = AlfabetosPredefinidos.bcd()
        assert alf.cardinal == 10
        assert '0000' in alf.simbolos
        assert '1001' in alf.simbolos
        assert '1010' not in alf.simbolos  # BCD solo 0-9


class TestComparacionSimbolos:
    """Tests para comparación de símbolos."""
    
    def test_comparar_simbolos_menor(self):
        """Test de comparación menor."""
        alf = AlfabetoExplicito('a', 'b', 'c')
        assert alf.comparar_simbolos('a', 'b') == -1
        assert alf.comparar_simbolos('b', 'c') == -1
    
    def test_comparar_simbolos_igual(self):
        """Test de comparación igual."""
        alf = AlfabetoExplicito('x', 'y', 'z')
        assert alf.comparar_simbolos('x', 'x') == 0
        assert alf.comparar_simbolos('y', 'y') == 0
    
    def test_comparar_simbolos_mayor(self):
        """Test de comparación mayor."""
        alf = AlfabetoExplicito('0', '1', '2')
        assert alf.comparar_simbolos('2', '1') == 1
        assert alf.comparar_simbolos('1', '0') == 1
    
    def test_es_menor(self):
        """Test de operador <."""
        alf = AlfabetosPredefinidos.decimal()
        assert alf.es_menor('3', '7')
        assert not alf.es_menor('7', '3')
        assert not alf.es_menor('5', '5')
    
    def test_es_igual(self):
        """Test de operador =."""
        alf = AlfabetosPredefinidos.decimal()
        assert alf.es_igual('5', '5')
        assert not alf.es_igual('5', '6')
    
    def test_es_mayor(self):
        """Test de operador >."""
        alf = AlfabetosPredefinidos.decimal()
        assert alf.es_mayor('9', '2')
        assert not alf.es_mayor('2', '9')
        assert not alf.es_mayor('5', '5')


class TestComparacionPalabras:
    """Tests para comparación lexicográfica de palabras."""
    
    def test_comparar_palabras_iguales(self):
        """Test de palabras iguales."""
        alf = AlfabetosPredefinidos.binario()
        assert alf.comparar_palabras_lexicografico('101', '101') == 0
    
    def test_comparar_palabras_menor(self):
        """Test palabra1 < palabra2."""
        alf = AlfabetosPredefinidos.binario()
        assert alf.comparar_palabras_lexicografico('000', '001') < 0
        assert alf.comparar_palabras_lexicografico('101', '110') < 0
    
    def test_comparar_palabras_mayor(self):
        """Test palabra1 > palabra2."""
        alf = AlfabetosPredefinidos.binario()
        assert alf.comparar_palabras_lexicografico('111', '110') > 0
        assert alf.comparar_palabras_lexicografico('10', '01') > 0
    
    def test_comparar_palabras_prefijo(self):
        """Test cuando una es prefijo de otra."""
        alf = AlfabetosPredefinidos.binario()
        # Palabra más corta es menor
        assert alf.comparar_palabras_lexicografico('10', '101') < 0
        assert alf.comparar_palabras_lexicografico('101', '10') > 0
    
    def test_comparar_palabras_decimal(self):
        """Test comparación en decimal."""
        alf = AlfabetosPredefinidos.decimal()
        assert alf.comparar_palabras_lexicografico('123', '456') < 0
        assert alf.comparar_palabras_lexicografico('999', '1000') > 0  # Lexicográfico!


class TestFactories:
    """Tests para funciones factory."""
    
    def test_crear_alfabeto_explicito(self):
        """Test factory de alfabeto explícito."""
        alf = crear_alfabeto_explicito('p', 'q', 'r')
        assert isinstance(alf, AlfabetoExplicito)
        assert alf.cardinal == 3
    
    def test_crear_alfabeto_estandar(self):
        """Test factory de alfabeto estándar."""
        alf = crear_alfabeto_estandar_desde_cardinal(8)
        assert isinstance(alf, AlfabetoEstandar)
        assert alf.cardinal == 8
    
    def test_unir_alfabetos(self):
        """Test de unión de alfabetos."""
        alf1 = AlfabetoExplicito('a', 'b')
        alf2 = AlfabetoExplicito('b', 'c')
        union = unir_alfabetos(alf1, alf2)
        
        assert union.cardinal == 3
        assert set(union.simbolos) == {'a', 'b', 'c'}
    
    def test_unir_alfabetos_sin_duplicados(self):
        """Test que unión elimina duplicados."""
        alf1 = AlfabetoExplicito('x', 'y')
        alf2 = AlfabetoExplicito('y', 'z')
        union = unir_alfabetos(alf1, alf2)
        
        # 'y' no debe duplicarse
        assert union.cardinal == 3


class TestAlfabetoDesdeLenguaje:
    """Tests para alfabetos jerárquicos."""
    
    def test_creacion_basica(self):
        """Test de creación desde lenguaje."""
        alf_bin = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf_bin, longitud=2)
        alf_jer = AlfabetoDesdeLenguaje(L, separador=" ")
        
        assert alf_jer.cardinal == 4
        assert set(alf_jer.simbolos) == {'00', '01', '10', '11'}
    
    def test_lenguaje_fuente(self):
        """Test acceso al lenguaje fuente."""
        alf_bin = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf_bin, longitud=2)
        alf_jer = AlfabetoDesdeLenguaje(L)
        
        assert alf_jer.lenguaje_fuente is L
    
    def test_separador_configurado(self):
        """Test que separador se guarda correctamente."""
        alf_bin = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf_bin, longitud=2)
        alf_jer = AlfabetoDesdeLenguaje(L, separador="-")
        
        assert alf_jer.separador == "-"
    
    def test_generar_palabras_con_separador(self):
        """Test generación de palabras con separador."""
        alf_bin = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf_bin, {"0", "1"})
        alf_jer = AlfabetoDesdeLenguaje(L, separador=" ")
        
        palabras = alf_jer.generar_palabras(2)
        assert "0 0" in palabras
        assert "0 1" in palabras
        assert "1 0" in palabras
        assert "1 1" in palabras
    
    def test_validar_palabra_con_separador(self):
        """Test validación con separador."""
        alf_bin = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf_bin, {"00", "11"})
        alf_jer = AlfabetoDesdeLenguaje(L, separador=" ")
        
        assert alf_jer.validar_palabra("00 11")
        assert alf_jer.validar_palabra("11 00")
        assert not alf_jer.validar_palabra("00 01")  # '01' no es símbolo
    
    def test_lenguaje_infinito_invalido(self):
        """Test que no se puede crear desde lenguaje infinito."""
        from core.lenguajes import LenguajeInfinito
        
        class LenguajeInfinitoTest(LenguajeInfinito):
            def pertenece(self, palabra):
                return True  # Acepta cualquier palabra para el test
            
            def generar_hasta(self, n):
                return [str(i) for i in range(n)]
        
        alf_bin = AlfabetosPredefinidos.binario()
        L_inf = LenguajeInfinitoTest(alf_bin, "test")
        
        with pytest.raises(ValueError, match="infinito"):
            AlfabetoDesdeLenguaje(L_inf)
    
    def test_lenguaje_vacio_invalido(self):
        """Test que no se puede crear desde lenguaje vacío."""
        from core.lenguajes import LenguajeVacio
        
        alf_bin = AlfabetosPredefinidos.binario()
        L_vacio = LenguajeVacio(alf_bin, longitud=3)
        
        with pytest.raises(ValueError, match="vacío"):
            AlfabetoDesdeLenguaje(L_vacio)


class TestPropiedadesMatematicas:
    """Tests para propiedades matematicas."""
    
    def test_cardinal_correcto(self):
        """Test que cardinal es correcto."""
        alf = AlfabetoExplicito('a', 'b', 'c')
        assert alf.cardinal == len(alf.simbolos)
    
    def test_indices_unicos(self):
        """Test que todos los índices son únicos."""
        alf = AlfabetoExplicito('x', 'y', 'z', 'w')
        indices = [alf.indice_de(s) for s in alf.simbolos]
        assert len(indices) == len(set(indices))  # Sin duplicados
    
    def test_simbolos_unicos(self):
        """Test que todos los símbolos son únicos."""
        alf = AlfabetoExplicito('a', 'b', 'c', 'd')
        assert len(alf.simbolos) == len(set(alf.simbolos))
    
    def test_numero_palabras_longitud_n(self):
        """Test que |Σ|^n palabras de longitud n."""
        alf = AlfabetoExplicito('0', '1', '2')
        n = 3
        palabras = alf.generar_palabras(n)
        assert len(palabras) == alf.cardinal ** n


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
