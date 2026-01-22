"""
test_lenguajes.py

Tests completos para el modulo de lenguajes formales.

Cubre:
- Lenguaje universo
- Lenguajes con predicados
- Lenguajes con automatas
- Lenguajes explicitos
- Lenguajes de longitud fija
- Operaciones sobre lenguajes
- Distancia de Hamming
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from core.alfabetos import AlfabetosPredefinidos, AlfabetoExplicito
from core.lenguajes import (
    Lenguaje,
    LenguajeLongitudFija,
    LenguajeUniverso,
    LenguajePredicado,
    LenguajeAutomata,
    LenguajeExplicito,
    LenguajeExplicitoLongitudFija,
    LenguajeVacio,
    LenguajeInfinito,
    EstadoDecision,
    union,
    interseccion,
    complemento,
    diferencia,
    diferencia_simetrica,
    concatenacion,
    potencia,
    producto_cartesiano
)


class TestLenguajeUniverso:
    """Tests para LenguajeUniverso (Σ^l)."""
    
    def test_creacion_basica(self):
        """Test de creación de lenguaje universo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        
        assert L.longitud_fija
        assert L.longitud == 2
    
    def test_cardinal_correcto(self):
        """Test que cardinal es n^l."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        
        assert L.cardinal() == 2 ** 3  # 8
    
    def test_enumerar_completo(self):
        """Test enumeración de todas las palabras."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        palabras = L.enumerar()
        
        assert set(palabras) == {'00', '01', '10', '11'}
    
    def test_pertenece(self):
        """Test de pertenencia."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        
        assert L.pertenece('000')
        assert L.pertenece('111')
        assert L.pertenece('101')
        assert not L.pertenece('00')  # Longitud incorrecta
        assert not L.pertenece('1010')  # Longitud incorrecta
        assert not L.pertenece('abc')  # Símbolos inválidos
    
    def test_longitud_cero(self):
        """Test lenguaje de longitud 0 (palabra vacía)."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=0)
        
        assert L.cardinal() == 1
        assert L.enumerar() == ['']
    
    def test_longitud_negativa_invalida(self):
        """Test que longitud negativa es inválida."""
        alf = AlfabetosPredefinidos.binario()
        with pytest.raises(ValueError):
            LenguajeUniverso(alf, longitud=-1)


class TestLenguajePredicado:
    """Tests para LenguajePredicado."""
    
    def test_predicado_paridad(self):
        """Test lenguaje con paridad par de unos."""
        alf = AlfabetosPredefinidos.binario()
        predicado = lambda w: w.count('1') % 2 == 0
        L = LenguajePredicado(alf, longitud=3, predicado=predicado)
        
        assert L.pertenece('000')  # 0 unos (par)
        assert L.pertenece('011')  # 2 unos (par)
        assert not L.pertenece('001')  # 1 uno (impar)
        assert not L.pertenece('111')  # 3 unos (impar)
    
    def test_predicado_empieza_con_cero(self):
        """Test lenguaje que empieza con '0'."""
        alf = AlfabetosPredefinidos.binario()
        predicado = lambda w: w[0] == '0'
        L = LenguajePredicado(alf, longitud=3, predicado=predicado)
        
        assert L.pertenece('000')
        assert L.pertenece('011')
        assert not L.pertenece('100')
        assert not L.pertenece('111')
    
    def test_cardinal_sublenguaje(self):
        """Test que cardinal es menor o igual al universo."""
        alf = AlfabetosPredefinidos.binario()
        predicado = lambda w: w.count('1') >= 2
        L = LenguajePredicado(alf, longitud=3, predicado=predicado)
        
        assert L.cardinal() <= 2 ** 3
    
    def test_enumerar_filtra_correctamente(self):
        """Test que enumerar aplica el predicado."""
        alf = AlfabetosPredefinidos.binario()
        predicado = lambda w: w.count('1') == 2
        L = LenguajePredicado(alf, longitud=3, predicado=predicado)
        
        palabras = set(L.enumerar())
        assert palabras == {'011', '101', '110'}


class TestLenguajeAutomata:
    """Tests para LenguajeAutomata."""
    
    def test_automata_basico(self):
        """Test autómata que acepta palabras que terminan en '1'."""
        alf = AlfabetosPredefinidos.binario()
        
        def automata(w):
            if w.endswith('1'):
                return EstadoDecision.ACEPTAR
            else:
                return EstadoDecision.RECHAZAR
        
        L = LenguajeAutomata(alf, longitud=3, automata=automata)
        
        assert L.pertenece('001')
        assert L.pertenece('111')
        assert not L.pertenece('000')
        assert not L.pertenece('110')
    
    def test_automata_con_indeterminado(self):
        """Test autómata que puede retornar INDETERMINADO."""
        alf = AlfabetosPredefinidos.binario()
        
        def automata_parcial(w):
            if w.startswith('00'):
                return EstadoDecision.ACEPTAR
            elif w.startswith('11'):
                return EstadoDecision.RECHAZAR
            else:
                return EstadoDecision.INDETERMINADO
        
        L = LenguajeAutomata(alf, longitud=3, automata=automata_parcial)
        
        assert L.pertenece('000')  # ACEPTAR
        assert not L.pertenece('111')  # RECHAZAR
        # INDETERMINADO se trata como no pertenece por defecto
        assert not L.pertenece('010')
    
    def test_combinar_automatas(self):
        """Test combinación de autómatas para reducir INDETERMINADO."""
        alf = AlfabetosPredefinidos.binario()
        
        def automata1(w):
            if w.startswith('0'):
                return EstadoDecision.ACEPTAR
            return EstadoDecision.INDETERMINADO
        
        def automata2(w):
            if w.endswith('1'):
                return EstadoDecision.ACEPTAR
            return EstadoDecision.RECHAZAR
        
        L = LenguajeAutomata(alf, longitud=2, automata=automata1)
        L_combinado = L.combinar_con(automata2)
        
        assert L_combinado.pertenece('00')  # automata1 acepta
        assert L_combinado.pertenece('11')  # automata2 acepta
        assert not L_combinado.pertenece('10')  # ambos rechazan


class TestLenguajeExplicito:
    """Tests para LenguajeExplicito."""
    
    def test_creacion_basica(self):
        """Test de creación con conjunto explícito."""
        alf = AlfabetosPredefinidos.binario()
        palabras = {'00', '11', '01'}
        L = LenguajeExplicito(alf, palabras)
        
        assert L.cardinal() == 3
    
    def test_pertenece(self):
        """Test de pertenencia."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'000', '111'})
        
        assert L.pertenece('000')
        assert L.pertenece('111')
        assert not L.pertenece('001')
    
    def test_enumerar(self):
        """Test de enumeración ordenada."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'10', '00', '11'})
        
        palabras = L.enumerar()
        assert palabras == ['00', '10', '11']  # Ordenado
    
    def test_factory_longitud_fija(self):
        """Test que factory crea LenguajeExplicitoLongitudFija."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'00', '11'})
        
        assert isinstance(L, LenguajeExplicitoLongitudFija)
        assert L.longitud_fija
        assert L.longitud == 2
    
    def test_factory_longitud_variable(self):
        """Test que factory mantiene LenguajeExplicito para longitud variable."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'0', '11', '101'})
        
        assert isinstance(L, LenguajeExplicito)
        assert not L.longitud_fija
    
    def test_validacion_palabras_invalidas(self):
        """Test que rechaza palabras con símbolos inválidos."""
        alf = AlfabetosPredefinidos.binario()
        
        with pytest.raises(ValueError):
            LenguajeExplicito(alf, {'00', '11', '22'})  # '2' no está en binario


class TestLenguajeExplicitoLongitudFija:
    """Tests para LenguajeExplicitoLongitudFija."""
    
    def test_creacion_directa(self):
        """Test creación directa."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicitoLongitudFija(alf, {'00', '11'}, "Test")
        
        assert L.longitud == 2
        assert L.cardinal() == 2
    
    def test_longitudes_diferentes_invalida(self):
        """Test que rechaza palabras de diferentes longitudes."""
        alf = AlfabetosPredefinidos.binario()
        
        with pytest.raises(ValueError, match="misma longitud"):
            LenguajeExplicitoLongitudFija(alf, {'0', '00', '000'})


class TestLenguajeVacio:
    """Tests para LenguajeVacio."""
    
    def test_cardinal_cero(self):
        """Test que cardinal es 0."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeVacio(alf, longitud=3)
        
        assert L.cardinal() == 0
        assert L.es_vacio()
    
    def test_no_pertenece_ninguna(self):
        """Test que ninguna palabra pertenece."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeVacio(alf, longitud=2)
        
        assert not L.pertenece('00')
        assert not L.pertenece('01')
        assert not L.pertenece('10')
        assert not L.pertenece('11')
    
    def test_enumerar_vacio(self):
        """Test que enumerar retorna lista vacía."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeVacio(alf, longitud=3)
        
        assert L.enumerar() == []
    
    def test_singleton(self):
        """Test que es singleton por alfabeto y longitud."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeVacio(alf, longitud=3)
        L2 = LenguajeVacio(alf, longitud=3)
        
        assert L1 is L2


class TestDistanciaHamming:
    """Tests para distancia de Hamming."""
    
    def test_distancia_basica(self):
        """Test cálculo básico de distancia."""
        d = LenguajeLongitudFija.distancia_hamming("000", "111")
        assert d == 3
    
    def test_distancia_cero(self):
        """Test distancia a sí misma es 0."""
        d = LenguajeLongitudFija.distancia_hamming("101", "101")
        assert d == 0
    
    def test_distancia_uno(self):
        """Test distancia 1."""
        d = LenguajeLongitudFija.distancia_hamming("1010", "1011")
        assert d == 1
    
    def test_distancia_simetrica(self):
        """Test que distancia es simétrica."""
        d1 = LenguajeLongitudFija.distancia_hamming("00", "11")
        d2 = LenguajeLongitudFija.distancia_hamming("11", "00")
        assert d1 == d2
    
    def test_longitudes_diferentes_invalida(self):
        """Test que rechaza palabras de diferente longitud."""
        with pytest.raises(ValueError):
            LenguajeLongitudFija.distancia_hamming("00", "000")
    
    def test_distancia_minima_codigo(self):
        """Test cálculo de distancia mínima de código."""
        alf = AlfabetosPredefinidos.binario()
        # Código de repetición triple
        L = LenguajeExplicitoLongitudFija(alf, {"000", "111"})
        
        assert L.distancia_minima() == 3
    
    def test_peso_hamming(self):
        """Test cálculo de peso de Hamming."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=4)
        
        assert L.peso_hamming("0000") == 0
        assert L.peso_hamming("0001") == 1
        assert L.peso_hamming("0101") == 2
        assert L.peso_hamming("1111") == 4
    
    def test_distancia_minima_codigo_paridad(self):
        """Test distancia mínima de código de paridad."""
        alf = AlfabetosPredefinidos.binario()
        # Código de paridad simple (4 bits con paridad par)
        palabras = {'0000', '0011', '0101', '0110',
                   '1001', '1010', '1100', '1111'}
        L = LenguajeExplicitoLongitudFija(alf, palabras)
        
        assert L.distancia_minima() == 2  # Puede detectar 1 error


class TestOperacionesLenguajes:
    """Tests para operaciones sobre lenguajes."""
    
    def test_union(self):
        """Test unión de lenguajes."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01'})
        L2 = LenguajeExplicito(alf, {'10', '11'})
        
        L_union = union(L1, L2)
        
        assert L_union.pertenece('00')
        assert L_union.pertenece('01')
        assert L_union.pertenece('10')
        assert L_union.pertenece('11')
        assert L_union.cardinal() == 4
    
    def test_interseccion(self):
        """Test intersección de lenguajes."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01', '10'})
        L2 = LenguajeExplicito(alf, {'01', '10', '11'})
        
        L_intersec = interseccion(L1, L2)
        
        assert L_intersec.cardinal() == 2
        assert L_intersec.pertenece('01')
        assert L_intersec.pertenece('10')
        assert not L_intersec.pertenece('00')
        assert not L_intersec.pertenece('11')
    
    def test_complemento(self):
        """Test complemento de lenguaje."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'00', '11'})
        
        L_comp = complemento(L)
        
        assert not L_comp.pertenece('00')
        assert not L_comp.pertenece('11')
        assert L_comp.pertenece('01')
        assert L_comp.pertenece('10')
    
    def test_diferencia(self):
        """Test diferencia de lenguajes."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01', '10'})
        L2 = LenguajeExplicito(alf, {'01', '11'})
        
        L_dif = diferencia(L1, L2)
        
        assert L_dif.pertenece('00')
        assert L_dif.pertenece('10')
        assert not L_dif.pertenece('01')
        assert not L_dif.pertenece('11')
    
    def test_diferencia_simetrica(self):
        """Test diferencia simétrica (XOR)."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01'})
        L2 = LenguajeExplicito(alf, {'01', '10'})
        
        L_xor = diferencia_simetrica(L1, L2)
        
        assert L_xor.pertenece('00')  # En L1, no en L2
        assert L_xor.pertenece('10')  # En L2, no en L1
        assert not L_xor.pertenece('01')  # En ambos
    
    def test_concatenacion(self):
        """Test concatenación de lenguajes."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'0', '1'})
        L2 = LenguajeExplicito(alf, {'00', '11'})
        
        L_concat = concatenacion(L1, L2)
        
        assert L_concat.cardinal() == 4  # 2 * 2
        assert L_concat.pertenece('000')
        assert L_concat.pertenece('011')
        assert L_concat.pertenece('100')
        assert L_concat.pertenece('111')
    
    def test_potencia(self):
        """Test potencia de lenguaje."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'0', '1'})
        
        L2 = potencia(L, 2)
        assert set(L2.enumerar()) == {'00', '01', '10', '11'}
        
        L3 = potencia(L, 3)
        assert L3.cardinal() == 8
    
    def test_potencia_cero(self):
        """Test que L^0 = {ε}."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {'0', '1'})
        
        L0 = potencia(L, 0)
        assert L0.cardinal() == 1
        assert L0.pertenece('')
    
    def test_producto_cartesiano(self):
        """Test producto cartesiano."""
        alf = AlfabetoExplicito('a', 'b')
        L1 = LenguajeExplicito(alf, {'a', 'b'})
        L2 = LenguajeExplicito(alf, {'a', 'b'})
        
        L_prod = producto_cartesiano(L1, L2, separador=",")
        
        assert L_prod.cardinal() == 4
        assert L_prod.pertenece('a,a')
        assert L_prod.pertenece('a,b')
        assert L_prod.pertenece('b,a')
        assert L_prod.pertenece('b,b')


class TestRelacionesLenguajes:
    """Tests para relaciones entre lenguajes."""
    
    def test_sublenguaje(self):
        """Test relación de sublenguaje."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01'})
        L2 = LenguajeExplicito(alf, {'00', '01', '10', '11'})
        
        assert L1.es_sublenguaje_de(L2)
        assert not L2.es_sublenguaje_de(L1)
    
    def test_superlenguaje(self):
        """Test relación de superlenguaje."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01', '10'})
        L2 = LenguajeExplicito(alf, {'00', '01'})
        
        assert L1.es_superlenguaje_de(L2)
        assert not L2.es_superlenguaje_de(L1)
    
    def test_igualdad(self):
        """Test igualdad de lenguajes."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01', '10'})
        L2 = LenguajeExplicito(alf, {'10', '00', '01'})  # Orden diferente
        
        assert L1.es_igual_a(L2)
        assert L2.es_igual_a(L1)
    
    def test_operadores_python(self):
        """Test sobrecarga de operadores Python."""
        alf = AlfabetosPredefinidos.binario()
        L1 = LenguajeExplicito(alf, {'00', '01'})
        L2 = LenguajeExplicito(alf, {'00', '01', '10'})
        
        assert L1 <= L2  # __le__
        assert L2 >= L1  # __ge__
        assert L1 == L1  # __eq__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
