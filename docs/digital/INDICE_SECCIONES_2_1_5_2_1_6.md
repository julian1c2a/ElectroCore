# Índice de Navegación - Secciones 2.1.5 y 2.1.6

**Documentación sobre Representación de Fracciones en Punto Fijo y Punto Flotante**

---

## 📚 Estructura de Contenidos

### Sección 2.1.5 - Punto Fijo

**[SECCION_2_1_5_PUNTO_FIJO.md](SECCION_2_1_5_PUNTO_FIJO.md)** ← Documentación completa

#### Temas Cubiertos

1. **Concepto Fundamental**
   - Definición de Punto Fijo
   - Formato E,F (número de dígitos enteros, número de dígitos fraccionarios)
   - Ejemplo Q(3,4) en binario

2. **Representación en Base B Genérica**
   - Formato general en base B
   - Ejemplos: base 10, base 2, base 16
   - Estructura general matemática

3. **Conversión entre Bases** ⭐ IMPORTANTE
   - Regla de conservación: $B'^{F'} \geq B^F$
   - Cálculo de F' mínimo: $F'_{min} = \lceil F \cdot \log_{B'} B \rceil$
   - Ejemplos: Base 2→10, Base 10→2, Base 8→16
   - Algoritmo de multiplicación repetida

4. **Punto Fijo con Signo**
   - Magnitud y Signo (M&S)
   - Complemento a la Base (más común)
   - Rango en Q(E,F)

5. **Análisis de Errores**
   - Error máximo representable: $\epsilon_{max} = 2^{-F}$
   - Error de redondeo
   - Representabilidad de números

6. **Errores en Operaciones**
   - Error en suma/resta (overflow)
   - Error en multiplicación (expansión de bits)
   - Manejo de overflow

7. **Tabla Comparativa de Formatos Q**
   - Q(4,4), Q(8,8), Q(16,16), Q(24,8)
   - Rango, precisión, uso

8. **Ventajas y Desventajas**
   - Cuándo usar punto fijo
   - Limitaciones

---

### Sección 2.1.6 - Punto Flotante

**[SECCION_2_1_6_PUNTO_FLOTANTE.md](SECCION_2_1_6_PUNTO_FLOTANTE.md)** ← Documentación completa

#### Temas Cubiertos

1. **Concepto Fundamental**
   - Definición: $V = M \times B^E$
   - Estructura general: Signo, Exponente, Mantisa
   - Cada componente explicado en detalle

2. **Formato Generalizado en Base B**
   - Definición matemática completa
   - Sesgo del exponente (Bias)
   - Mantisa normalizada: [1, B)

3. **Ejemplos en Diferentes Formatos**
   - IEEE 754 - Precisión simple (32 bits)
   - IEEE 754 - Precisión doble (64 bits)
   - Punto flotante genérico (base 10, e=4, m=6)

4. **Números Especiales** ⭐ CRÍTICO
   - Números normalizados (E ∈ [1, 2^e-2])
   - Números denormalizados (E=0, M≠0)
   - Cero (E=0, M=0): ±0
   - Infinito (E=máx, M=0): ±∞
   - NaN (E=máx, M≠0)
   - Tabla de especiales

5. **Operaciones Aritméticas**
   - Suma/Resta: Alineación, suma, normalización, redondeo
   - Multiplicación: Multiplicar M, sumar E, normalizar
   - División: Similar a multiplicación
   - Ejemplos prácticos

6. **Errores en Punto Flotante**
   - Error de representación
   - Error relativo vs absoluto
   - Pérdida de dígitos significativos
   - Compaación: Punto fijo vs punto flotante

7. **Normalización Post-Operación** ⭐ IMPORTANTE
   - Por qué normalizar
   - Necesidad después de suma/resta
   - Necesidad después de multiplicación

8. **Tabla Comparativa: Punto Fijo vs Flotante**
   - 8 aspectos diferentes
   - Rango 32 bits, precisión, mejor para qué

9. **Ventajas y Desventajas**
   - Cuándo usar punto flotante
   - Limitaciones y peligros

10. **IEEE 754 - Referencia Rápida**
    - Simple, Doble, Extendida
    - Rango y precisión de cada una

---

## 🔗 Documento Comparativo

**[COMPARATIVA_PUNTO_FIJO_VS_FLOTANTE.md](COMPARATIVA_PUNTO_FIJO_VS_FLOTANTE.md)** ← Análisis cruzado

### Contenidos

1. **Tabla Comparativa Completa**
   - Estructuras, rango, precisión
   - Operaciones aritméticas
   - Hardware requerido

2. **Análisis de Errores**
   - Error de representación en ambos
   - Gráficos del error relativo
   - Comparación cuantitativa

3. **Eficiencia de Almacenamiento**
   - Representación de números extremos
   - Cuál es mejor para cada valor

4. **Casos de Uso Específicos**
   - Cuándo usar Punto Fijo
   - Cuándo usar Punto Flotante
   - Matriz decisional

5. **Ejemplos Prácticos**
   - Procesamiento de imagen (Punto Fijo mejor)
   - Integración numérica (Punto Flotante mejor)

6. **Resumen Decisional**
   - Matriz de decisión final
   - ¿Cuándo dudar? → Usa Punto Flotante

---

## 🎯 Mapa de Temas Clave

```
PUNTO FIJO (Sección 2.1.5)
├─ Estructura: Q(E,F)
├─ Representación en base B
├─ Conversión entre bases ⭐
│  └─ Regla: B'^F' ≥ B^F
├─ Con signo: Complemento a base
├─ Errores: ε_max = 2^-F (constante)
├─ Operaciones: Rápidas, problemas de overflow
└─ Mejor para: Embebidos, tiempo real, velocidad

PUNTO FLOTANTE (Sección 2.1.6)
├─ Estructura: V = M × B^E
├─ Números especiales: ±0, ±∞, NaN
├─ Normalización ⭐ (crítica)
├─ Errores: ε_rel ≈ 2^-m (constante)
├─ Operaciones: Más lenta, requiere normalizar
├─ IEEE 754: Standard universal
└─ Mejor para: Científica, rango amplio, generalidad

COMPARATIVA
├─ Rango: Flotante gana (10^76 vs 10^6)
├─ Precisión: Depende del número
├─ Velocidad: Punto Fijo gana (sin FPU)
├─ Facilidad: Punto Flotante gana (automático)
└─ Decisión: ¿Rango amplio? → Flotante
             ¿Velocidad crítica? → Fijo
```

---

## 📖 Flujo de Lectura Recomendado

### Para Principiantes

1. Lee [Comparativa](COMPARATIVA_PUNTO_FIJO_VS_FLOTANTE.md) primero (5 min)
   - Entiende las diferencias básicas

2. Lee [Punto Fijo](SECCION_2_1_5_PUNTO_FIJO.md) (30 min)
   - Más simple de entender
   - Buena base conceptual

3. Lee [Punto Flotante](SECCION_2_1_6_PUNTO_FLOTANTE.md) (30 min)
   - Ahora tiene sentido después de punto fijo
   - Entiende por qué se necesita

### Para Expertos

1. Ve directo a [Punto Flotante](SECCION_2_1_6_PUNTO_FLOTANTE.md)
   - Números especiales (±0, ±∞, NaN)
   - Normalización post-operación

2. Lee [Conversión entre bases](SECCION_2_1_5_PUNTO_FIJO.md#-conversión-entre-bases)
   - La matemática más interesante

3. Consulta [Comparativa](COMPARATIVA_PUNTO_FIJO_VS_FLOTANTE.md) para decisiones

---

## 🔍 Temas Especiales Destacados

### ⭐ Conversión entre Bases (Sección 2.1.5)

**Por qué es importante:**

- Necesario convertir entre bases sin perder información
- La regla $B'^{F'} \geq B^F$ es fundamental
- Aplicable a cualquier base, no solo 2 y 10

**Conceptos clave:**

- Precisión mínima en cada base
- Cálculo de F' mínimo
- Algoritmo de multiplicación repetida

**Ejemplo práctico:**

- Convertir 0.625 (decimal) a binario manualmente
- Verificar que la conversión es exacta

---

### ⭐ Números Especiales en Punto Flotante (Sección 2.1.6)

**Por qué es importante:**

- IEEE 754 incluye ±0, ±∞, NaN
- Cambio de paradigma vs punto fijo
- Requiere lógica especial

**Conceptos clave:**

- ±0: Dos ceros (usualmente equivalentes)
- ±∞: Resultado de overflow, no error
- NaN: "Not a Number" (resultado indefinido)
- Denormalizados: Llenan el hueco hacia 0

**Aplicaciones:**

- Manejo de casos especiales en código
- División por cero → ∞ (no error)
- 0/0 → NaN (operación inválida)

---

### ⭐ Normalización Post-Operación (Sección 2.1.6)

**Por qué es importante:**

- Mantiene la precisión máxima
- Requiere después de CADA suma/resta y multiplicación
- Costo computacional importante

**Concepto clave:**

- Mantisa siempre en rango [1, 2) en base 2
- Después de sumar: puede crecer a 2
- Después de multiplicar: puede crecer a 4
- Hay que "normalizar" (renormalizar)

**Comparación:**

- Punto Fijo: No requiere normalización
- Punto Flotante: SIEMPRE requiere normalización
- Es por eso que punto flotante es más lento

---

## 🎓 Preguntas de Autoevaluación

### Punto Fijo

- [ ] ¿Qué es Q(E,F) y qué representan E y F?
- [ ] ¿Cuál es el error máximo en punto fijo?
- [ ] ¿Cómo se convierte entre bases sin perder precisión?
- [ ] ¿Por qué 32 bits en punto fijo no es suficiente para cálculos científicos?

### Punto Flotante

- [ ] ¿Cuál es la estructura: V = M × B^E?
- [ ] ¿Qué son los números denormalizados y para qué sirven?
- [ ] ¿Cuál es la diferencia entre normalizado y denormalizado?
- [ ] ¿Por qué se necesita normalizar después de cada operación?
- [ ] ¿Qué es NaN y cómo se genera?

### Comparativa

- [ ] ¿Cuándo error absoluto vs error relativo?
- [ ] ¿Por qué punto flotante tiene mejor rango pero punto fijo es más rápido?
- [ ] ¿Para qué son mejores cada uno?

---

## 🔗 Conexiones con Otras Secciones

**Anteriormente (Sección 2.1.1-2.1.4):**

- Sistemas de numeración básicos
- Sistemas enteros signados
- Códigos BCD, Johnson, Biquinario

**Ahora (Sección 2.1.5-2.1.6):**

- Representación de fracciones (punto fijo)
- Representación con rango dinámico (punto flotante)

**Próximos (Si se documentan):**

- Aritmética extendida (más de 64 bits)
- Códigos de corrección de errores (Hamming, CRC)
- Criptografía y representación segura

---

## 📊 Estadísticas de Documentación

| Sección | Archivo | Líneas | Temas | Ejemplos |
|---------|---------|--------|-------|----------|
| 2.1.5 | PUNTO_FIJO.md | 850+ | 10 | 15+ |
| 2.1.6 | PUNTO_FLOTANTE.md | 1100+ | 11 | 20+ |
| Comparativa | COMPARATIVA.md | 600+ | 8 | 10+ |
| **Total** | **3 archivos** | **2550+** | **29** | **45+** |

---

## ✅ Estado de Documentación

- ✅ Punto Fijo: Completo
- ✅ Punto Flotante: Completo
- ✅ Comparativa: Completo
- ✅ Ejemplos: 45+ casos diferentes
- ✅ Formulas: Todas justificadas matemáticamente
- ⏳ Funciones de validación: A crear (próxima sesión)
- ⏳ Demo interactivo: A crear (próxima sesión)

---

## 🚀 Próximas Acciones

Para mañana (cuando continúes):

1. **Crear funciones Python:**
   - Conversión entre bases
   - Validación de punto fijo
   - Validación de punto flotante
   - Simuladores de operaciones

2. **Crear demostraciones:**
   - Errores en operaciones
   - Comparación visual
   - Casos de uso

3. **Crear tests:**
   - Validar conversiones
   - Verificar errores calculados
   - Casos extremos

---

## 📝 Notas Importantes

```
⭐ Puntos Clave a Recordar:

Punto Fijo:
  • Error absoluto = 2^-F (uniforme)
  • Conversión entre bases: B'^F' ≥ B^F
  • Overflow es abrupto
  • Muy rápido, predecible

Punto Flotante:
  • Error relativo ≈ 2^-m (uniforme)
  • Números especiales: ±0, ±∞, NaN
  • Requiere normalización después de CADA operación
  • Más lento pero más flexible

Decisión:
  • ¿Rango amplio? → Flotante
  • ¿Velocidad crítica? → Fijo
  • ¿No seguro? → Flotante (más seguro)
```

---

## 🎯 Resumen Ejecutivo

Esta documentación cubre **dos sistemas complementarios** para representar números:

1. **Punto Fijo:** Posición decimal fija, preciso para rango limitado, muy rápido
2. **Punto Flotante:** Exponente variable, maneja rango amplio, más lento

Ambos son fundamentales en computación moderna. La elección depende del contexto específico.

Para mañana: Código funcional que implemente estas teorías.
