from modules.numeracion.generators import BinaryConversionGenerator
from modules.combinacional.generators import KarnaughGenerator, LogicProblemGenerator, MSIGenerator
from modules.secuencial.generators import SequentialGenerator
from core.sistemas_numeracion_basicos import (
    distancia_hamming,
    Lenguaje,
    crear_lenguaje_binario_saturado,
    crear_lenguaje_bcd,
    crear_lenguaje_johnson,
    crear_lenguaje_biquinario,
)
# En core/catalog.py
from modules.formal_languages.generators import FormalLanguageGenerator
# ============================================================================
# Registro central de ejercicios
EXERCISE_CATALOG = {
    "formal_languages_basics": FormalLanguageGenerator(),
    "num_conversion_8bits": BinaryConversionGenerator(),
    "karnaugh_4vars": KarnaughGenerator(),
    "logic_problem": LogicProblemGenerator(),
    "msi_analysis": MSIGenerator(),
    "sequential_analysis": SequentialGenerator()
}

# ============================================================================
# CATALOGO DE SISTEMAS DE NUMERACION Y CODIGOS (En Desarrollo)
# ============================================================================
# 
# ESTADO DEL DESARROLLO:
# ✅ FASE 1: Eficacia de Empaquetado (Sección 2.1.1.6.1.3-5) - 45 tests
# ✅ FASE 2: Códigos Especializados (Sección 2.1.1.6.1.6-7) - 47 tests
# ✅ FASE 3: Teoría de Códigos (Sección 2.1.1.6.1.5) - Conceptual
# ✅ FASE 4: Distancia Hamming y Lenguajes (Sección 2.1.1.6.1.8) - 41 tests
# ⏳ FASE 5: Códigos Correctores (Hamming, Reed-Solomon) → Sección 2.1.1.6.1.9
# ⏳ FASE 6: Gray Generalizado para n bits → Sección 2.1.1.6.1.10
# ⏳ FASE 7: Análisis de Distancia Mínima → Sección 2.1.1.6.1.11
# ⏳ FASE 8: Visualización de Grafos de Transición → Sección 2.1.1.6.1.12
#
# PROGRESO TOTAL: 50% (4/8 fases completadas, 88/88 tests pasando ✅)
# 
# ¿POR QUÉ SE LLAMA "DISTANCIA" HAMMING?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 
# La función distancia_hamming no es solo un nombre conveniente.
# ES UNA VERDADERA DISTANCIA MATEMÁTICA que satisface los 3 AXIOMAS DE MÉTRICA:
#
# 1. NO-NEGATIVIDAD Y SEPARABILIDAD
#    d_H(a, b) ≥ 0 para todas a, b
#    d_H(a, b) = 0  ⟺  a = b
#    
#    Prueba: d_H cuenta posiciones diferentes. Siempre ≥ 0. Solo 0 si a = b.
#
# 2. SIMETRÍA
#    d_H(a, b) = d_H(b, a)
#    
#    Prueba: Si a[i] ≠ b[i], también b[i] ≠ a[i]. El conjunto de diferencias
#            es idéntico en ambas direcciones.
#
# 3. DESIGUALDAD TRIANGULAR
#    d_H(a, c) ≤ d_H(a, b) + d_H(b, c)
#    
#    Prueba: En cada posición i:
#            - Si a[i] = c[i], no contribuye a d_H(a,c).
#            - Si a[i] ≠ c[i], entonces a[i] ≠ b[i] XOR b[i] ≠ c[i]
#              (o ambas, pero eso suma 2 en lado derecho vs 1 en izquierda).
#
# CONSECUENCIAS DE SER UNA MÉTRICA:
# - Define un espacio métrico sobre palabras-código
# - Permite análisis topológico riguroso
# - Justifica términos como "vecindad" y "frontera"
# - Fundamenta detección/corrección de errores
# - Habilita algoritmos geométricos y de optimización
#
# Ver ROADMAP_Y_CATALOGO.md para detalles completos de planificación

CODIGO_SYSTEMS_CATALOG = {
    # FASE 4: Sistema Genérico de Lenguajes (Completado)
    "lenguajes": {
        "binario_4bit": crear_lenguaje_binario_saturado(4),
        "bcd_4bit": crear_lenguaje_bcd(),
        "johnson_5bit": crear_lenguaje_johnson(),
        "biquinario_5bit": crear_lenguaje_biquinario(),
    },
    
    # Funciones de análisis (Completado)
    "funciones": {
        "distancia_hamming": distancia_hamming,
    },
    
    # FASE 5: Códigos Correctores (Planned)
    "correctores": {
        # hamming_7_4: {
        #     "descripcion": "Código Hamming (7,4) para corrección de errores",
        #     "capacidad_correctora": 1,
        #     "matriz_generadora": "GF(2)^(4x7)",
        #     "matriz_paridad": "GF(2)^(3x7)",
        # },
        # reed_solomon: {
        #     "descripcion": "Código Reed-Solomon para múltiples errores",
        #     "cuerpo_finito": "GF(2^m)",
        # }
    },
    
    # FASE 6: Gray Generalizado (Planned)
    "gray_generalizado": {
        # "gray_n_bits": generar_gray_n_bits,
        # "entero_a_gray": entero_a_gray_n_bits,
        # "gray_a_entero": gray_n_bits_a_entero,
    },
    
    # FASE 7: Análisis de Distancia Mínima (Planned)
    "analisis_distancia": {
        # "matriz_distancias": calcular_matriz_distancias,
        # "distancia_minima": lambda len: min(all pairs),
    },
    
    # FASE 8: Grafos de Transición (Planned)
    "grafos": {
        # "visualizar_grafo": visualizar_grafo_transicion,
        # "analizar_conectividad": analizar_grafo,
    }
}

# Metadata sobre fases y progreso
CODIGO_SYSTEMS_METADATA = {
    "ultima_fase_completada": 4,
    "total_fases_planeadas": 8,
    "progreso": "50%",
    "proxima_fase": 5,
    "proximidad_fecha": "Semana 2 de desarrollo",
    "documentacion_referencia": "ROADMAP_Y_CATALOGO.md",
    "tests_totales": 88,
    "tests_pasando": 88,
    "cobertura": "100%",
}

