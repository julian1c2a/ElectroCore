# !/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
FASE 4 RESUMEN: Distancia Hamming y Análisis de Lenguajes de Longitud Fija

Propósito
----------

Implementar un sistema genérico y robusto para trabajar con lenguajes de longitud
fija, basado en la distancia Hamming, que permite:

1. Calcular diferencias entre palabras de un código
2. Verificar propiedades matemáticas (adyacencia, ciclicidad)
3. Analizar y comparar diferentes sistemas de codificación
4. Crear nuevos lenguajes personalizados fácilmente

Implementación
---------------

1. FUNCIÓN DISTANCIA_HAMMING
   - Calcula número de posiciones diferentes entre dos palabras
   - Soporta cualquier alfabeto (no solo binario)
   - Validación de entrada (palabras de igual longitud)

2. CLASE LENGUAJE (Genérica)
   Atributos:
   - alfabeto: Lista de símbolos disponibles
   - longitud: Longitud fija de palabras
   - predicado: Función para validar palabras
   - valor_cero: Palabra inicial
   - siguiente: Función para generar palabra siguiente (con wrap-around)
   - nombre: Identificador descriptivo

   Métodos principales:
   - es_valida(palabra): Verifica pertenencia
   - siguiente_palabra(palabra): Obtiene siguiente con ciclo
   - distancia_hamming(p_a, p_b): Calcula Hamming
   - son_adyacentes(p_a, p_b): Verifica si distancia=1
   - generar_todas_palabras(): Lista palabras válidas (con caché)
   - analizar_adyacencia(): Análisis completo de propiedades

3. LENGUAJES ESPECÍFICOS (Constructores)

   a) Binario Natural (saturado)
      - Toda palabra de longitud L es válida
      - Orden: incremento binario con wrap-around
      - Propiedades: 100% eficacia, NO adyacente, NO cíclico

   b) BCD (Binary Coded Decimal)
      - Solo dígitos 0-9 (10 palabras válidas)
      - Orden: 0000→0001→...→1001→0000
      - Propiedades: 62.5% eficacia, NO adyacente, NO cíclico

   c) Johnson (Cíclico Adyacente)
      - 10 palabras: 00000, 00001, 00011, 00111, ..., 10000
      - Patrón: bloque de 1s desplazándose
      - Propiedades: 31.2% eficacia, SÍ adyacente, SÍ cíclico

   d) Biquinario (2 entre 5)
      - Exactamente 2 bits encendidos en 5 posiciones
      - C(5,2) = 10 combinaciones válidas
      - Propiedades: 31.2% eficacia, NO adyacente, NO cíclico
      - Capacidad: Detección de errores (cualquier desviación es error)

Casos de Uso
-------------

1. Medir diferencias: ¿Cuánto cambia 0111 a 1000? → 4 bits
2. Verificar adyacencia: ¿00001 y 00011 son adyacentes? → Sí (distancia=1)
3. Determinar propiedades: ¿Johnson es cíclico? → Sí
4. Comparar códigos: Tabla de eficacia, adyacencia, ciclicidad
5. Detectar errores: Biquinario rechaza cualquier no-2-bits
6. Crear códigos personalizados: Definir predicado propio

Matemáticas Formales
---------------------

Distancia Hamming:
  d_H(a, b) = Σ[a_i ≠ b_i] para i en [0, L-1]

Código Adyacente:
  d_H(p_i, p_{i+1}) = 1 para todo i

Código Cíclico:
  d_H(p_{n-1}, p_0) = 1 (además de adyacente)

Código Saturado:
  |palabras_válidas| = |alfabeto|^L

Eficacia:
  E = |palabras_válidas| / |alfabeto|^L

Característica Distintiva
-----------

Los lenguajes se diferencian no por alfabeto ni longitud, sino por SEMANTICA:

- Binario y Gray usan el MISMO alfabeto {0,1} y longitud 4
- Pero asignan DIFERENTES significados (orden) a las 16 combinaciones
- Johnson y Biquinario usan 5 bits pero solo 10 combinaciones (NO saturados)

Archivos Creados/Modificados
-----------------------------

1. core/sistemas_numeracion_basicos.py
   - Agregadas ~410 líneas (funciones + clase)
   - Compatibilidad total con código anterior

2. tests/test_hamming_lenguaje.py (NUEVO)
   - 41 tests exhaustivos
   - Cobertura: 6 clases de tests
   - Validación: distancia, adyacencia, propiedades de lenguajes

3. demo_hamming_lenguaje.py (NUEVO)
   - 6 demostraciones ejecutables
   - Ejemplos prácticos para cada lenguaje
   - Tabla comparativa final

4. CONTENIDOS_FE.md
   - Nueva sección 2.1.1.6.1.8 (250+ líneas)
   - Concepto, fórmulas, ejemplos
   - Documentación de clase y métodos
   - Casos de uso

Validación
-----------

✓ 41 tests nuevos: TODOS PASANDO
✓ 47 tests anteriores: TODOS PASANDO
✓ Total: 88 tests, 0 fallos
✓ Demo ejecutable sin errores
✓ Documentación completa e integrada

Extensibilidad
---------------

Es muy fácil crear nuevos lenguajes personalizados:

  def crear_mi_lenguaje():
      def mi_predicado(palabra):
          # Tu lógica de validación
          return True or False

      def mi_siguiente(palabra):
          # Tu lógica de generación del siguiente
          return palabra_siguiente
      
      return Lenguaje(
          alfabeto=['0', '1'],
          longitud=5,
          predicado=mi_predicado,
          valor_cero='00000',
          siguiente=mi_siguiente,
          nombre="Mi Lenguaje Personalizado"
      )

Próximas Fases (Opcionales)
----------------------------

1. Códigos Correctores de Errores
   - Implementar Hamming(7,4), Hamming(8,4)
   - Cálculo de distancia mínima (corrección)
   - Matriz de paridad y síndrome

2. Gray Generalizado
   - Gray para n bits arbitrarios
   - Propiedades de reflexión

3. Análisis Avanzado
   - Distancia mínima entre palabras distintas
   - Capacidad correctora: t = floor((d_min - 1) / 2)
   - Matriz de distancias entre pares

4. Visualización
   - Gráfos de transición (vertices=palabras, aristas=adyacencias)
   - Matriz de Hamming (todas vs todas)
   - Diagrama de Hasse para relaciones de orden

5. Optimización
   - Búsqueda de códigos óptimos por propiedades
   - Generador de códigos de longitud fija eficientes

Conclusión
-----------

Se ha implementado un framework robusto y genérico para análisis matemático
de lenguajes de longitud fija basado en distancia Hamming. El sistema es:

- GENÉRICO: Funciona con cualquier alfabeto y longitud
- EFICIENTE: Cachea resultados para lenguajes pequeños
- ROBUSTO: Validación exhaustiva de entrada
- EXTENSIBLE: Fácil crear nuevos lenguajes
- DOCUMENTADO: Docstrings, ejemplos, tests completos
- VALIDADO: 88 tests, todas pasan

La implementación prepara el camino para análisis más avanzados de códigos
correctores de errores y sistemas de codificación óptimos.
"""

if __name__ == '__main__':
    print(__doc__)
