# Índice Completo: Sección 2.1.1 - Sistemas de Numeración

## 🎯 Guía de Referencia Rápida

Esta es la **estructura numérica completa** de la sección 2.1.1. Úsala para referenciar cualquier punto específico en discusiones.

---

## 📊 Estructura Jerárquica Completa

### 2.1.1 Sistemas de Numeración Posicionales y No Posicionales

#### 2.1.1.1 Sistemas Posicionales y No Posicionales

- **2.1.1.1.1** Definiciones de sistemas posicionales vs no posicionales
- **2.1.1.1.2** Sistemas No Posicionales - Números Romanos
- **2.1.1.1.3** Sistemas Posicionales con Potencias - Base 5
- **2.1.1.1.4** Sistemas Posicionales con Bases Mixtas - Tiempo Babilónico
  - **2.1.1.1.4.1** Definición y estructura
  - **2.1.1.1.4.2** Cálculo y conversión
  - **2.1.1.1.4.3** Aplicaciones históricas

#### 2.1.1.2 Unicidad de la Representación

- **2.1.1.2.1** Teorema Fundamental - Unicidad
- **2.1.1.2.2** Prueba mediante Divisiones Sucesivas
- **2.1.1.2.3** Tabla de Verificación (1994 en múltiples bases)
  - **2.1.1.2.3.1** Verificación en base 2
  - **2.1.1.2.3.2** Verificación en base 5
  - **2.1.1.2.3.3** Verificación en base 8
  - **2.1.1.2.3.4** Verificación en base 16
- **2.1.1.2.4** Aplicación en Computación Digital

#### 2.1.1.3 Conversión entre Sistemas de Numeración

- **2.1.1.3.1** Algoritmo de Divisiones Sucesivas (Decimal → Base B)
  - **2.1.1.3.1.1** Descripción del algoritmo
  - **2.1.1.3.1.2** Ejemplo: 1994₁₀ → 30434₅
  - **2.1.1.3.1.3** Implementación paso a paso
  
- **2.1.1.3.2** Método del Polinomio (Base B → Decimal)
  - **2.1.1.3.2.1** Forma polinómica
  - **2.1.1.3.2.2** Cálculo directo
  - **2.1.1.3.2.3** Ejemplo: 30434₅ → 1994₁₀
  
- **2.1.1.3.3** Método de Horner (Base B → Decimal)
  - **2.1.1.3.3.1** Algoritmo optimizado
  - **2.1.1.3.3.2** Comparación de eficiencia
  - **2.1.1.3.3.3** Ejemplo: 30434₅ → 1994₁₀
  
- **2.1.1.3.4** Conversión entre Bases Relacionadas (B^l ↔ B^k)
  - **2.1.1.3.4.1** Teoría de bases relacionadas
  - **2.1.1.3.4.2** Algoritmo GCD-optimizado
  - **2.1.1.3.4.3** Ejemplos: 2↔4, 2↔8, 2↔16, 8↔16

#### 2.1.1.4 Calculadora: Números Romanos ↔ Decimal

- **2.1.1.4.1** Características del Módulo
- **2.1.1.4.2** Función: `decimal_a_romano(n)`
- **2.1.1.4.3** Función: `romano_a_decimal(s)`
- **2.1.1.4.4** Función: `explicar_romano(n)` y `explicar_base5(n)`
- **2.1.1.4.5** Script Demostrativo
- **2.1.1.4.6** Tabla de Ejemplos
- **2.1.1.4.7** Notas Importantes

---

#### 2.1.1.5 Sistemas Binarios, Octales y Hexadecimales

- **2.1.1.5.1** Sistemas de Numeración Binaria
  - **2.1.1.5.1.1** Definición y características
  - **2.1.1.5.1.2** Conversión binario ↔ decimal
  - **2.1.1.5.1.3** Rango de representación
  - **2.1.1.5.1.4** Aplicaciones en computación
  
- **2.1.1.5.2** Sistemas de Numeración Octal y Hexadecimal
  - **2.1.1.5.2.1** Base 8: Octal ($8 = 2^3$)
  - **2.1.1.5.2.2** Base 16: Hexadecimal ($16 = 2^4$)
  - **2.1.1.5.2.3** Conversión octal/hexadecimal ↔ decimal
  - **2.1.1.5.2.4** Usos en sistemas informáticos
  
- **2.1.1.5.3** Conversión entre Binario, Octal y Hexadecimal
  - **2.1.1.5.3.1** Agrupación de dígitos binarios
  - **2.1.1.5.3.2** Conversión binario ↔ octal (grupos de 3)
  - **2.1.1.5.3.3** Conversión binario ↔ hexadecimal (grupos de 4)
  - **2.1.1.5.3.4** Tabla de equivalencias
  
- **2.1.1.5.4** Conversión entre Representación de Bases Relacionadas
  - **2.1.1.5.4.1** Concepto de bases relacionadas
  - **2.1.1.5.4.2** Algoritmo de conversión
  - **2.1.1.5.4.3** Ejemplos prácticos

#### 2.1.1.6 Representación en Longitud Fija

- **2.1.1.6.1** Representación de Números Naturales
  - **2.1.1.6.1.1** Capacidad de representación para longitud n y base B
    - **2.1.1.6.1.1.1** Definición: capacidad = $B^n$
    - **2.1.1.6.1.1.2** Función capacidad(B, n)
    - **2.1.1.6.1.1.3** Ejemplos de capacidades en diferentes bases
  - **2.1.1.6.1.2** Rango de valores representables
    - **2.1.1.6.1.2.1** Definición: rango = [0, $B^n - 1$]
    - **2.1.1.6.1.2.2** Justificación matemática (mínimo y máximo)
    - **2.1.1.6.1.2.3** Tabla de rangos por base y longitud
    - **2.1.1.6.1.2.4** Función longitud(x, B) - logaritmo entero
  - **2.1.1.6.1.3** Comparación en sistemas con bits (base 2) hasta base 16
  - **2.1.1.6.1.4** Sistemas BCD - Codificación Decimal Binaria
  - **2.1.1.6.1.5** Sistemas de representación binaria en base 2
  
- **2.1.1.6.2** Relación Base-Dígitos-Rango
  - **2.1.1.6.2.1** Fórmula: rango = $B^n$
  - **2.1.1.6.2.2** Tabla de valores máximos
  - **2.1.1.6.2.3** Implicaciones prácticas

#### 2.1.1.7 Números Enteros con Signo

- **2.1.1.7.1** Magnitud y Signo
  - **2.1.1.7.1.1** Estructura: 1 bit de signo + n-1 bits de magnitud
  - **2.1.1.7.1.2** Rango representable
  - **2.1.1.7.1.3** Ventajas y desventajas
  
- **2.1.1.7.2** Complemento a la Base B
  - **2.1.1.7.2.1** Complemento a 2 en base B=2
    - **2.1.1.7.2.1.1** Definición y cálculo
    - **2.1.1.7.2.1.2** Rango representable
    - **2.1.1.7.2.1.3** Ventajas (una representación del cero)
  - **2.1.1.7.2.2** Complemento a 10 en base 10
    - **2.1.1.7.2.2.1** Cálculo y aplicación
  - **2.1.1.7.2.3** BCD Exceso a 3 y BCD Aitken
    - **2.1.1.7.2.3.1** Códigos especializados para BCD
  
- **2.1.1.7.3** Exceso a un Sesgo k
  - **2.1.1.7.3.1** Concepto de sesgo (bias)
  - **2.1.1.7.3.2** Representación con sesgo
  - **2.1.1.7.3.3** Aplicación en punto flotante

#### 2.1.1.8 Operaciones Aritméticas

- **2.1.1.8.1** Comparación de Números
  - **2.1.1.8.1.1** Comparación en representación magnitud-signo
  - **2.1.1.8.1.2** Comparación en complemento a 2
  - **2.1.1.8.1.3** Comparación en representación exceso-k
  
- **2.1.1.8.2** Suma y Resta de Números Naturales
  - **2.1.1.8.2.1** Algoritmo de suma en base B
  - **2.1.1.8.2.2** Propagación de acarreo
  - **2.1.1.8.2.3** Desbordamiento (overflow)
  - **2.1.1.8.2.4** Algoritmo de resta en base B
  
- **2.1.1.8.3** Operaciones de Complementación
  - **2.1.1.8.3.1** Complemento a la base B (CB)
  - **2.1.1.8.3.2** Complemento a la base B menos 1 (CB-1)
  - **2.1.1.8.3.3** Métodos de cálculo rápido
  
- **2.1.1.8.4** Inversión de Signo
  - **2.1.1.8.4.1** Inversión en representación magnitud-signo
  - **2.1.1.8.4.2** Inversión en complemento a B
  - **2.1.1.8.4.3** Inversión en representación exceso-k
  
- **2.1.1.8.5** Suma y Resta de Números Enteros
  - **2.1.1.8.5.1** En representación magnitud-signo
  - **2.1.1.8.5.2** En complemento a B
    - **2.1.1.8.5.2.1** Suma simple en complemento a 2
    - **2.1.1.8.5.2.2** Manejo de acarreo final
    - **2.1.1.8.5.2.3** Detección de overflow
  - **2.1.1.8.5.3** En representación exceso-k
  
- **2.1.1.8.6** Multiplicación de Números Naturales
  - **2.1.1.8.6.1** Algoritmo de multiplicación en base B
  - **2.1.1.8.6.2** Generación de productos parciales
  - **2.1.1.8.6.3** Suma de productos parciales
  
- **2.1.1.8.7** División y Resto
  - **2.1.1.8.7.1** Algoritmo de división larga en base B=2
  - **2.1.1.8.7.2** Cálculo del resto
  - **2.1.1.8.7.3** Casos especiales (divisor = 0)

#### 2.1.1.9 Representación de Números con Parte Fraccionaria

- **2.1.1.9.1** Representación Fija (Fixed-Point)
  - **2.1.1.9.1.1** Concepto: E dígitos enteros, F dígitos fraccionarios
  - **2.1.1.9.1.2** Notación posicional con pesos negativos
  - **2.1.1.9.1.3** Conversión a decimal
  
- **2.1.1.9.2** Conversiones entre Formatos
  - **2.1.1.9.2.1** Conversión E,L-E (cambio de punto decimal)
  - **2.1.1.9.2.2** Conversión entre bases B y B' en punto fijo
  - **2.1.1.9.2.3** Conversión específica: bases 10 ↔ 2
  - **2.1.1.9.2.4** Conversión entre bases que son potencias de base común
  - **2.1.1.9.2.5** Tabla de conversión: bases 2, 4, 8, 16
  - **2.1.1.9.2.6** Tabla de conversión: bases 3, 9, 27
  
- **2.1.1.9.3** Rango y Precisión
  - **2.1.1.9.3.1** Rango representable para longitud L, parte entera E, base B
  - **2.1.1.9.3.2** Épsilon (precisión mínima) en punto fijo
  - **2.1.1.9.3.3** Error de representación
  
- **2.1.1.9.4** Representación en Punto Flotante
  - **2.1.1.9.4.1** Concepto: mantisa y exponente (mantissa × base^exponent)
  - **2.1.1.9.4.2** Estándar IEEE 754
    - **2.1.1.9.4.2.1** Formato binary32 (simple precisión)
    - **2.1.1.9.4.2.2** Formato binary64 (doble precisión)
  - **2.1.1.9.4.3** Épsilon en punto flotante IEEE 754
  - **2.1.1.9.4.4** Rangos máximos y mínimos IEEE 754
  - **2.1.1.9.4.5** Formas normalizadas y denormalizadas
    - **2.1.1.9.4.5.1** Números normalizados (mantisa ∈ [1, 2))
    - **2.1.1.9.4.5.2** Números denormalizados (mantisa < 1)
    - **2.1.1.9.4.5.3** Ceros, infinitos y NaN
  
- **2.1.1.9.5** Operaciones en Punto Flotante
  - **2.1.1.9.5.1** Operaciones de redondeo y truncamiento
    - **2.1.1.9.5.1.1** Round to nearest even
    - **2.1.1.9.5.1.2** Round towards zero
    - **2.1.1.9.5.1.3** Round up/down
  - **2.1.1.9.5.2** Función 'normalizar' en punto flotante
    - **2.1.1.9.5.2.1** Conversión a forma normalizada
    - **2.1.1.9.5.2.2** Ajuste de exponente
  - **2.1.1.9.5.3** Conversión entre punto fijo y punto flotante
    - **2.1.1.9.5.3.1** De punto fijo a punto flotante
    - **2.1.1.9.5.3.2** De punto flotante a punto fijo
  - **2.1.1.9.5.4** Operaciones aritméticas en punto flotante
    - **2.1.1.9.5.4.1** Suma y resta
    - **2.1.1.9.5.4.2** Multiplicación
    - **2.1.1.9.5.4.3** División
    - **2.1.1.9.5.4.4** Manejo de errores de redondeo

---

## 💡 Ejemplos de Referencia

Para referenciar un punto específico en una discusión:

- ✅ **"Según 2.1.1.3.3.2, el método de Horner es más eficiente"**
- ✅ **"En 2.1.1.7.2.1.2, vemos que el rango en complemento a 2 es..."**
- ✅ **"La sección 2.1.1.9.4.5.3 explica los casos especiales (NaN, infinito)"**
- ✅ **"Ver comparación en 2.1.1.5.3.4 - tabla de equivalencias"**

---

## 📍 Localización en Archivos

| Sección | Archivo | Líneas |
|---------|---------|--------|
| 2.1.1.1-2.1.1.4 | CONTENIDOS_FE.md | 14-170 |
| 2.1.1.5-2.1.1.9 | CONTENIDOS_FE.md | 170-320 |
| Navegación | SISTEMAS_NUMERACION_NAVEGACION.md | 1-418 |
| Resumen | SISTEMAS_NUMERACION_RESUMEN.md | 1-280 |
| Código | core/sistemas_numeracion_basicos.py | 1-400+ |
| Demos | demo_sistemas_numeracion_basicos.py | 1-240+ |

---

## 🔗 Relaciones entre Conceptos

```
2.1.1.1 (Sistemas básicos)
    ↓
2.1.1.2 (Unicidad → garantiza no ambigüedad)
    ↓
2.1.1.3 (Conversión → implementa unicidad)
    ↓
2.1.1.4 (Calculadora → aplicación de 2.1.1.1-2.1.1.3)
    ↓
2.1.1.5 (Binario/Octal/Hex → casos especiales de 2.1.1.3)
    ↓
2.1.1.6 (Longitud fija → restricción práctica)
    ↓
2.1.1.7 (Con signo → extensión con magnitud)
    ↓
2.1.1.8 (Operaciones → aplica 2.1.1.6-2.1.1.7)
    ↓
2.1.1.9 (Punto flotante → extensión de 2.1.1.8)
```

---

## ✅ Verificación de Concordancia

**Documentos Verificados**:

- ✅ CONTENIDOS_FE.md - Estructura numérica 4 niveles
- ✅ SISTEMAS_NUMERACION_NAVEGACION.md - Actualizado con 2.1.1.5-2.1.1.9
- ✅ SISTEMAS_NUMERACION_RESUMEN.md - Referencias concordantes
- ✅ core/sistemas_numeracion_basicos.py - Comentarios con referencias
- ✅ demo_sistemas_numeracion_basicos.py - Referencias en docstrings
- ✅ COMPLETADO_SECCION_2_1_1.md - Actualizado con nuevas secciones

**Estado**: ✅ TODOS LOS DOCUMENTOS EN CONCORDANCIA
