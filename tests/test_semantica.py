"""
test_semantica.py

Tests completos para el modulo de semantica.

Cubre:
- Semantica lexicografica
- Semantica por peso de Hamming
- Semantica por longitud
- Semantica personalizada
- Operaciones: minimo, maximo, supremo, infimo
- Ordenamiento
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from core.alfabetos import AlfabetosPredefinidos
from core.lenguajes import LenguajeUniverso, LenguajeExplicito
from core.semantica import (
    Semantica,
    SemanticaLexicografica,
    SemanticaPesoHamming,
    SemanticaLongitud,
    SemanticaPersonalizada,
    RelacionOrden
)


class TestSemanticaLexicografica:
    """Tests para orden lexicográfico."""
    
    def test_creacion(self):
        """Test de creación básica."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.lenguaje is L
    
    def test_comparar_menor(self):
        """Test comparación menor."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.comparar("000", "001") == RelacionOrden.MENOR
        assert sem.comparar("010", "100") == RelacionOrden.MENOR
    
    def test_comparar_igual(self):
        """Test comparación igual."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.comparar("01", "01") == RelacionOrden.IGUAL
        assert sem.comparar("11", "11") == RelacionOrden.IGUAL
    
    def test_comparar_mayor(self):
        """Test comparación mayor."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.comparar("111", "110") == RelacionOrden.MAYOR
        assert sem.comparar("101", "001") == RelacionOrden.MAYOR
    
    def test_minimo(self):
        """Test elemento mínimo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.minimo() == "000"
    
    def test_maximo(self):
        """Test elemento máximo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.maximo() == "111"
    
    def test_ordenar(self):
        """Test ordenamiento de palabras."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        desordenado = ["11", "00", "10", "01"]
        ordenado = sem.ordenar(desordenado)
        
        assert ordenado == ["00", "01", "10", "11"]
    
    def test_es_menor(self):
        """Test método es_menor."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.es_menor("00", "01")
        assert not sem.es_menor("11", "10")
        assert not sem.es_menor("01", "01")
    
    def test_es_mayor(self):
        """Test método es_mayor."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.es_mayor("11", "10")
        assert not sem.es_mayor("00", "01")
        assert not sem.es_mayor("10", "10")
    
    def test_es_igual(self):
        """Test método es_igual."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.es_igual("10", "10")
        assert not sem.es_igual("10", "01")
    
    def test_palabra_no_en_lenguaje(self):
        """Test que rechaza palabra fuera del lenguaje."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"00", "11"})
        sem = SemanticaLexicografica(L, alf)
        
        with pytest.raises(ValueError):
            sem.comparar("00", "01")  # "01" no está en L


class TestSemanticaPesoHamming:
    """Tests para orden por peso de Hamming."""
    
    def test_creacion(self):
        """Test de creación."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        assert sem.lenguaje is L
    
    def test_comparar_pesos_diferentes(self):
        """Test comparación con pesos diferentes."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=4)
        sem = SemanticaPesoHamming(L)
        
        # peso 0 < peso 1
        assert sem.comparar("0000", "0001") == RelacionOrden.MENOR
        # peso 2 < peso 3
        assert sem.comparar("0011", "0111") == RelacionOrden.MENOR
        # peso 4 > peso 3
        assert sem.comparar("1111", "0111") == RelacionOrden.MAYOR
    
    def test_comparar_mismo_peso_incomparables(self):
        """Test que mismo peso son incomparables."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=4)
        sem = SemanticaPesoHamming(L)
        
        # Ambos peso 2
        assert sem.comparar("0011", "0101") == RelacionOrden.INCOMPARABLE
        assert sem.comparar("1010", "1001") == RelacionOrden.INCOMPARABLE
    
    def test_minimo_peso_cero(self):
        """Test que mínimo es palabra de peso 0."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        assert sem.minimo() == "000"
    
    def test_maximo_peso_maximo(self):
        """Test que máximo es palabra de peso máximo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        assert sem.maximo() == "111"
    
    def test_supremo(self):
        """Test supremo de conjunto."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        conjunto = {"001", "010"}  # Ambos peso 1
        sup = sem.supremo(conjunto)
        
        # Supremo debe tener peso >= 1
        # En este caso, cualquier palabra de peso 1 es cota superior minimal
        peso_sup = L.peso_hamming(sup)
        assert peso_sup >= 1
    
    def test_infimo(self):
        """Test ínfimo de conjunto."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        conjunto = {"011", "101"}  # Ambos peso 2
        inf = sem.infimo(conjunto)
        
        # Ínfimo debe tener peso <= 2
        peso_inf = L.peso_hamming(inf)
        assert peso_inf <= 2
    
    def test_requiere_longitud_fija(self):
        """Test que requiere LenguajeLongitudFija."""
        from core.lenguajes import LenguajeExplicito
        
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"0", "11", "101"})  # Longitud variable
        
        with pytest.raises(TypeError):
            SemanticaPesoHamming(L)


class TestSemanticaLongitud:
    """Tests para orden por longitud."""
    
    def test_comparar_longitudes_diferentes(self):
        """Test comparación con longitudes diferentes."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"0", "00", "000", "01", "10"})
        sem = SemanticaLongitud(L)
        
        assert sem.comparar("0", "00") == RelacionOrden.MENOR
        assert sem.comparar("00", "000") == RelacionOrden.MENOR
        assert sem.comparar("000", "00") == RelacionOrden.MAYOR
    
    def test_comparar_misma_longitud_incomparables(self):
        """Test que misma longitud son incomparables."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"00", "01", "10", "11"})
        sem = SemanticaLongitud(L)
        
        assert sem.comparar("00", "01") == RelacionOrden.INCOMPARABLE
        assert sem.comparar("10", "11") == RelacionOrden.INCOMPARABLE
    
    def test_minimo_longitud_menor(self):
        """Test que mínimo es palabra más corta."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"0", "00", "000"})
        sem = SemanticaLongitud(L)
        
        assert sem.minimo() == "0"
    
    def test_maximo_longitud_mayor(self):
        """Test que máximo es palabra más larga."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"0", "00", "000"})
        sem = SemanticaLongitud(L)
        
        assert sem.maximo() == "000"


class TestSemanticaPersonalizada:
    """Tests para orden personalizado."""
    
    def test_orden_suma_digitos(self):
        """Test orden por suma de dígitos."""
        alf = AlfabetosPredefinidos.decimal()
        L = LenguajeUniverso(alf, longitud=2)
        
        def comparar_suma(w1, w2):
            s1 = sum(int(c) for c in w1)
            s2 = sum(int(c) for c in w2)
            
            if s1 < s2:
                return RelacionOrden.MENOR
            elif s1 > s2:
                return RelacionOrden.MAYOR
            elif w1 == w2:
                return RelacionOrden.IGUAL
            else:
                return RelacionOrden.INCOMPARABLE
        
        sem = SemanticaPersonalizada(L, comparar_suma)
        
        # "00" suma 0 < "11" suma 2
        assert sem.comparar("00", "11") == RelacionOrden.MENOR
        # "12" suma 3 = "21" suma 3, pero diferentes → incomparables
        assert sem.comparar("12", "21") == RelacionOrden.INCOMPARABLE
    
    def test_orden_numero_transiciones(self):
        """Test orden por número de transiciones (cambios de símbolo)."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=4)
        
        def contar_transiciones(w):
            return sum(1 for i in range(len(w)-1) if w[i] != w[i+1])
        
        def comparar_transiciones(w1, w2):
            t1 = contar_transiciones(w1)
            t2 = contar_transiciones(w2)
            
            if t1 < t2:
                return RelacionOrden.MENOR
            elif t1 > t2:
                return RelacionOrden.MAYOR
            elif w1 == w2:
                return RelacionOrden.IGUAL
            else:
                return RelacionOrden.INCOMPARABLE
        
        sem = SemanticaPersonalizada(L, comparar_transiciones)
        
        # "0000" tiene 0 transiciones < "0101" tiene 3 transiciones
        assert sem.comparar("0000", "0101") == RelacionOrden.MENOR
        # "0011" tiene 1 transición = "1100" tiene 1 transición → incomparables
        assert sem.comparar("0011", "1100") == RelacionOrden.INCOMPARABLE


class TestPropiedadesOrdenParcial:
    """Tests para verificar propiedades del orden parcial."""
    
    def test_reflexividad(self):
        """Test que w ≤ w (reflexiva)."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        for palabra in L.enumerar():
            assert sem.es_menor_o_igual(palabra, palabra)
    
    def test_antisimetria(self):
        """Test que si w1 ≤ w2 y w2 ≤ w1 entonces w1 = w2."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        palabras = L.enumerar()
        for w1 in palabras:
            for w2 in palabras:
                if sem.es_menor_o_igual(w1, w2) and sem.es_menor_o_igual(w2, w1):
                    assert w1 == w2
    
    def test_transitividad(self):
        """Test que si w1 ≤ w2 y w2 ≤ w3 entonces w1 ≤ w3."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"000", "001", "010", "011"})
        sem = SemanticaLexicografica(L, alf)
        
        palabras = L.enumerar()
        for w1 in palabras:
            for w2 in palabras:
                for w3 in palabras:
                    if sem.es_menor_o_igual(w1, w2) and sem.es_menor_o_igual(w2, w3):
                        assert sem.es_menor_o_igual(w1, w3)
    
    def test_existencia_minimo(self):
        """Test que existe elemento mínimo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        minimo = sem.minimo()
        
        # El mínimo es menor o igual a todas las palabras
        for palabra in L.enumerar():
            assert sem.es_menor_o_igual(minimo, palabra)
    
    def test_existencia_maximo(self):
        """Test que existe elemento máximo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        maximo = sem.maximo()
        
        # El máximo es mayor o igual a todas las palabras
        for palabra in L.enumerar():
            assert sem.es_menor_o_igual(palabra, maximo)


class TestSupremoInfimo:
    """Tests para supremo e ínfimo."""
    
    def test_supremo_conjunto_vacio(self):
        """Test supremo de conjunto vacío es el mínimo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        sup = sem.supremo(set())
        assert sup == sem.minimo()
    
    def test_infimo_conjunto_vacio(self):
        """Test ínfimo de conjunto vacío es el máximo."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        inf = sem.infimo(set())
        assert inf == sem.maximo()
    
    def test_supremo_singleton(self):
        """Test supremo de {w} es w."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        sup = sem.supremo({"01"})
        assert sup == "01"
    
    def test_infimo_singleton(self):
        """Test ínfimo de {w} es w."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        inf = sem.infimo({"10"})
        assert inf == "10"


class TestCasosLimite:
    """Tests para casos límite."""
    
    def test_lenguaje_un_elemento(self):
        """Test lenguaje con un solo elemento."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"101"})
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.minimo() == "101"
        assert sem.maximo() == "101"
        assert sem.comparar("101", "101") == RelacionOrden.IGUAL
    
    def test_lenguaje_dos_elementos(self):
        """Test lenguaje con dos elementos."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeExplicito(alf, {"00", "11"})
        sem = SemanticaLexicografica(L, alf)
        
        assert sem.minimo() == "00"
        assert sem.maximo() == "11"
        assert sem.comparar("00", "11") == RelacionOrden.MENOR
    
    def test_cache_minimo_maximo(self):
        """Test que mínimo y máximo se cachean."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaLexicografica(L, alf)
        
        # Primera llamada calcula
        min1 = sem.minimo()
        # Segunda llamada usa caché
        min2 = sem.minimo()
        
        assert min1 == min2
        assert min1 is sem._cache_minimo


class TestComparabilidad:
    """Tests para verificar comparabilidad."""
    
    def test_todas_comparables_orden_total(self):
        """Test que en orden lexicográfico todas son comparables."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=2)
        sem = SemanticaLexicografica(L, alf)
        
        palabras = L.enumerar()
        for w1 in palabras:
            for w2 in palabras:
                assert sem.es_comparable(w1, w2)
    
    def test_algunas_incomparables_orden_parcial(self):
        """Test que en orden por peso hay incomparables."""
        alf = AlfabetosPredefinidos.binario()
        L = LenguajeUniverso(alf, longitud=3)
        sem = SemanticaPesoHamming(L)
        
        # Mismo peso → incomparables
        assert not sem.es_comparable("001", "010")
        assert not sem.es_comparable("011", "101")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
