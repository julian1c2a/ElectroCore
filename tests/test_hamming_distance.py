"""
Tests unitarios para la distancia de Hamming y propiedades relacionadas.

Este módulo contiene tests exhaustivos para:
- Cálculo de distancia de Hamming
- Propiedades métricas (no negatividad, identidad, simetría, desigualdad triangular)
- Peso de Hamming
- Esferas de Hamming
- Códigos correctores
- Volumen de esferas

NOTA: Las funciones de análisis han sido migradas a core.formal_languages
"""

import pytest
from typing import List, Set
import itertools

# ============================================================================
# IMPORTAR FUNCIONES DESDE EL CORE DEL PROYECTO
# ============================================================================
from core.formal_languages import (
    hamming_distance,
    hamming_weight,
    min_distance_of_language,
    hamming_sphere,
    binomial_coefficient,
    sphere_volume,
)


# ============================================================================
# Fixtures y utilidades
# ============================================================================

@pytest.fixture
def binary_words():
    """Palabras binarias de prueba."""
    return [
        "000", "001", "010", "011",
        "100", "101", "110", "111"
    ]


@pytest.fixture
def hamming_7_4_code():
    """Código de Hamming (7,4) completo."""
    return [
        "0000000", "1101000", "0110100", "1011100",
        "0011010", "1110010", "0101110", "1000110",
        "0001101", "1100101", "0111001", "1010001",
        "0010111", "1111111", "0100011", "1001011"
    ]


@pytest.fixture
def repetition_code():
    """Código de repetición triple."""
    return ["000", "111"]


# ============================================================================
# Tests para hamming_distance()
# ============================================================================

class TestHammingDistance:
    """Tests para la función de distancia de Hamming."""
    
    def test_identical_words(self):
        """Distancia entre palabras idénticas debe ser 0."""
        assert hamming_distance("000", "000") == 0
        assert hamming_distance("111", "111") == 0
        assert hamming_distance("101010", "101010") == 0
    
    def test_completely_different(self):
        """Distancia máxima cuando todas las posiciones difieren."""
        assert hamming_distance("000", "111") == 3
        assert hamming_distance("0000", "1111") == 4
        assert hamming_distance("00000000", "11111111") == 8
    
    def test_one_bit_difference(self):
        """Distancia 1 cuando solo difiere un bit."""
        assert hamming_distance("000", "001") == 1
        assert hamming_distance("000", "010") == 1
        assert hamming_distance("000", "100") == 1
    
    def test_multiple_differences(self):
        """Casos con múltiples diferencias."""
        assert hamming_distance("1010", "0101") == 4
        assert hamming_distance("1100", "0011") == 4
        assert hamming_distance("1010", "1100") == 2
    
    def test_length_mismatch(self):
        """Debe lanzar error si las longitudes no coinciden."""
        with pytest.raises(ValueError, match="igual longitud"):
            hamming_distance("00", "000")
        with pytest.raises(ValueError):
            hamming_distance("1010", "10")
    
    def test_non_binary_alphabets(self):
        """Funciona con alfabetos no binarios."""
        assert hamming_distance("abc", "abc") == 0
        assert hamming_distance("abc", "def") == 3
        assert hamming_distance("123", "124") == 1
    
    def test_empty_strings(self):
        """Distancia entre strings vacíos es 0."""
        assert hamming_distance("", "") == 0


# ============================================================================
# Tests para propiedades métricas
# ============================================================================

class TestMetricProperties:
    """Tests para verificar que d_H es una métrica."""
    
    def test_non_negativity(self, binary_words):
        """M1: d(x, y) ≥ 0 para todo x, y."""
        for x, y in itertools.combinations(binary_words, 2):
            assert hamming_distance(x, y) >= 0
    
    def test_identity_of_indiscernibles(self, binary_words):
        """M1: d(x, y) = 0 ⟺ x = y."""
        # Si x = y, entonces d(x, y) = 0
        for word in binary_words:
            assert hamming_distance(word, word) == 0
        
        # Si x ≠ y, entonces d(x, y) > 0
        for x, y in itertools.combinations(binary_words, 2):
            if x != y:
                assert hamming_distance(x, y) > 0
    
    def test_symmetry(self, binary_words):
        """M2: d(x, y) = d(y, x)."""
        for x, y in itertools.combinations(binary_words, 2):
            assert hamming_distance(x, y) == hamming_distance(y, x)
    
    def test_triangle_inequality(self, binary_words):
        """M3: d(x, z) ≤ d(x, y) + d(y, z)."""
        # Probar todas las tripletas
        for x, y, z in itertools.combinations(binary_words, 3):
            d_xz = hamming_distance(x, z)
            d_xy = hamming_distance(x, y)
            d_yz = hamming_distance(y, z)
            assert d_xz <= d_xy + d_yz, f"Falla para x={x}, y={y}, z={z}"
    
    def test_not_ultrametric(self):
        """Hamming NO es ultramétrica: contraejemplo."""
        x, y, z = "000", "111", "100"
        d_xy = hamming_distance(x, y)  # 3
        d_xz = hamming_distance(x, z)  # 1
        d_yz = hamming_distance(y, z)  # 2
        
        # Para ser ultramétrica: d(x,y) ≤ max(d(x,z), d(y,z))
        # 3 ≤ max(1, 2) = 2 → Falso
        assert d_xy > max(d_xz, d_yz), "Debería fallar la propiedad ultramétrica"


# ============================================================================
# Tests para peso de Hamming
# ============================================================================

class TestHammingWeight:
    """Tests para el peso de Hamming."""
    
    def test_zero_weight(self):
        """Peso de palabra nula es 0."""
        assert hamming_weight("000") == 0
        assert hamming_weight("0000") == 0
        assert hamming_weight("00000000") == 0
    
    def test_full_weight(self):
        """Peso de palabra con todos unos."""
        assert hamming_weight("111") == 3
        assert hamming_weight("1111") == 4
        assert hamming_weight("11111111") == 8
    
    def test_mixed_weight(self):
        """Casos mixtos."""
        assert hamming_weight("1010") == 2
        assert hamming_weight("1100") == 2
        assert hamming_weight("10110101") == 5
    
    def test_weight_equals_distance_to_zero(self):
        """w_H(x) = d_H(x, 0...0)."""
        test_cases = ["101", "1111", "1010", "00001111"]
        for word in test_cases:
            zeros = "0" * len(word)
            assert hamming_weight(word) == hamming_distance(word, zeros)
    
    def test_distance_via_xor_weight(self):
        """Para binarios: d_H(x, y) = w_H(x ⊕ y)."""
        test_pairs = [
            ("000", "111"),
            ("101", "010"),
            ("1100", "0011"),
        ]
        for x, y in test_pairs:
            # Simular XOR bit a bit
            xor = ''.join('1' if x[i] != y[i] else '0' for i in range(len(x)))
            assert hamming_distance(x, y) == hamming_weight(xor)


# ============================================================================
# Tests para esferas de Hamming
# ============================================================================

class TestHammingSphere:
    """Tests para esferas de Hamming."""
    
    def test_radius_zero(self):
        """Esfera de radio 0 solo contiene el centro."""
        center = "101"
        sphere = hamming_sphere(center, 0)
        assert len(sphere) == 1
        assert center in sphere
    
    def test_radius_one(self):
        """Esfera de radio 1 contiene centro + vecinos a distancia 1."""
        center = "000"
        sphere = hamming_sphere(center, 1)
        
        # Para n=3, debe haber C(3,0) + C(3,1) = 1 + 3 = 4 palabras
        assert len(sphere) == 4
        assert "000" in sphere
        assert "001" in sphere
        assert "010" in sphere
        assert "100" in sphere
    
    def test_sphere_volume_formula(self):
        """Verificar fórmula de volumen V(n, r)."""
        test_cases = [
            (3, 0, 1),   # C(3,0) = 1
            (3, 1, 4),   # C(3,0) + C(3,1) = 1 + 3 = 4
            (5, 1, 6),   # C(5,0) + C(5,1) = 1 + 5 = 6
            (5, 2, 16),  # 1 + 5 + 10 = 16
        ]
        for n, r, expected_volume in test_cases:
            calculated = sphere_volume(n, r, alphabet_size=2)
            assert calculated == expected_volume
    
    def test_all_words_in_sphere(self):
        """Todas las palabras en esfera cumplen la distancia."""
        center = "1010"
        radius = 2
        sphere = hamming_sphere(center, radius)
        
        for word in sphere:
            assert hamming_distance(center, word) <= radius


# ============================================================================
# Tests para códigos correctores
# ============================================================================

class TestErrorCorrectingCodes:
    """Tests para códigos correctores de errores."""
    
    def test_repetition_code_distance(self, repetition_code):
        """Código de repetición triple tiene d_min = 3."""
        d_min = min_distance_of_language(repetition_code)
        assert d_min == 3
    
    def test_hamming_7_4_distance(self, hamming_7_4_code):
        """Código de Hamming (7,4) tiene d_min = 3."""
        d_min = min_distance_of_language(hamming_7_4_code)
        assert d_min == 3
    
    def test_detection_capability(self):
        """Un código con d_min puede detectar d_min - 1 errores."""
        code = ["000", "111"]  # d_min = 3
        d_min = min_distance_of_language(code)
        
        # Puede detectar hasta 2 errores
        assert d_min >= 2 + 1
    
    def test_correction_capability(self):
        """Un código con d_min = 2t+1 puede corregir t errores."""
        code = ["000", "111"]  # d_min = 3
        d_min = min_distance_of_language(code)
        
        # Puede corregir t = (d_min - 1) // 2 = 1 error
        t = (d_min - 1) // 2
        assert t == 1
    
    def test_nearest_neighbor_decoding(self, repetition_code):
        """Decodificación por vecino más cercano."""
        def decode(received, code):
            min_dist = float('inf')
            closest = None
            for codeword in code:
                d = hamming_distance(received, codeword)
                if d < min_dist:
                    min_dist = d
                    closest = codeword
            return closest
        
        # Error en 1 posición debe corregirse
        assert decode("101", repetition_code) == "111"
        assert decode("001", repetition_code) == "000"
        assert decode("010", repetition_code) == "000"


# ============================================================================
# Tests para Hamming Bound
# ============================================================================

class TestHammingBound:
    """Tests para la cota de Hamming (sphere-packing bound)."""
    
    def test_hamming_bound_formula(self):
        """Verificar que |C| ≤ 2^n / V(n, t)."""
        # Código de Hamming (7,4) con t=1
        n, k, t = 7, 4, 1
        volume = sphere_volume(n, t, alphabet_size=2)
        max_codewords = (2 ** n) / volume
        
        # Código de Hamming (7,4) tiene 2^4 = 16 palabras
        assert 16 <= max_codewords
    
    def test_perfect_code_equality(self, hamming_7_4_code):
        """Código perfecto alcanza la igualdad en Hamming bound."""
        n = 7
        t = 1  # d_min = 3 → t = (3-1)/2 = 1
        
        volume = sphere_volume(n, t, alphabet_size=2)
        max_codewords = (2 ** n) / volume
        
        # Código de Hamming (7,4) es perfecto
        assert len(hamming_7_4_code) == max_codewords


# ============================================================================
# Tests para teoremas avanzados
# ============================================================================

class TestAdvancedTheorems:
    """Tests para teoremas avanzados."""
    
    def test_singleton_bound(self):
        """Cota de Singleton: |C| ≤ |Σ|^(n-d+1)."""
        # Para alfabeto binario: |C| ≤ 2^(n-d+1)
        n, d = 7, 3
        max_codewords = 2 ** (n - d + 1)  # 2^5 = 32
        
        # Código de Hamming (7,4) tiene 16 ≤ 32
        assert 16 <= max_codewords
    
    def test_plotkin_bound(self):
        """Cota de Plotkin para d > n/2."""
        # Para código con n=4, d=3 (d > n/2 = 2)
        n, d = 4, 3
        if d > n / 2:
            max_codewords = (2 * d) / (2 * d - n)
            # 6 / 2 = 3
            assert max_codewords == 3


# ============================================================================
# Tests de integración
# ============================================================================

class TestIntegration:
    """Tests de integración que combinan múltiples funcionalidades."""
    
    def test_code_verification_workflow(self):
        """Workflow completo: crear código, verificar propiedades, corregir errores."""
        # 1. Crear código
        code = ["0000", "1111"]
        
        # 2. Calcular distancia mínima
        d_min = min_distance_of_language(code)
        assert d_min == 4
        
        # 3. Determinar capacidad
        t = (d_min - 1) // 2
        assert t == 1  # Corrige 1 error
        
        # 4. Generar esfera de decodificación
        sphere = hamming_sphere("0000", t)
        assert len(sphere) == 5  # C(4,0) + C(4,1) = 1 + 4
        
        # 5. Verificar que esferas no se solapan
        sphere1 = hamming_sphere("0000", t)
        sphere2 = hamming_sphere("1111", t)
        assert len(sphere1 & sphere2) == 0, "Las esferas deben ser disjuntas"
    
    def test_average_distance(self):
        """Distancia promedio entre palabras aleatorias."""
        # Para alfabeto binario: E[d_H] = n/2
        n = 4
        binary_words = [format(i, f'0{n}b') for i in range(2**n)]
        
        total_distance = 0
        count = 0
        for x, y in itertools.combinations(binary_words, 2):
            total_distance += hamming_distance(x, y)
            count += 1
        
        average = total_distance / count
        expected = n / 2
        
        # Verificar que está cerca del valor teórico (tolerancia de 0.2)
        assert abs(average - expected) < 0.2, f"Promedio={average:.2f}, Esperado={expected}"


# ============================================================================
# Tests parametrizados
# ============================================================================

@pytest.mark.parametrize("x,y,expected", [
    ("000", "000", 0),
    ("000", "111", 3),
    ("101", "010", 3),
    ("1100", "0011", 4),
    ("10110", "10010", 1),
])
def test_hamming_distance_parametrized(x, y, expected):
    """Tests parametrizados para distancia de Hamming."""
    assert hamming_distance(x, y) == expected


@pytest.mark.parametrize("word,expected_weight", [
    ("000", 0),
    ("111", 3),
    ("1010", 2),
    ("10110101", 5),
])
def test_hamming_weight_parametrized(word, expected_weight):
    """Tests parametrizados para peso de Hamming."""
    assert hamming_weight(word) == expected_weight


@pytest.mark.parametrize("n,k,expected", [
    (5, 0, 1),
    (5, 1, 5),
    (5, 2, 10),
    (5, 5, 1),
    (7, 3, 35),
])
def test_binomial_coefficient_parametrized(n, k, expected):
    """Tests parametrizados para coeficiente binomial."""
    assert binomial_coefficient(n, k) == expected


# ============================================================================
# Ejecución principal
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
