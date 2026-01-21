# 📚 Generador de Ejercicios de Electrónica Digital

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-PDF-red?logo=latex&logoColor=white)](https://www.latex-project.org/)
[![Status](https://img.shields.io/badge/Status-Actively%20Developed-brightgreen)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Code](https://img.shields.io/badge/Código-Punto%20Fijo%20%2F%20Flotante-blue)](#)
[![Commits](https://img.shields.io/badge/Últimos%20Commits-IEEE754%2BBiquinarios-brightgreen)](#-roadmap)

Una **plataforma modular y extensible** para generar ejercicios de electrónica digital con documentación técnica completa. Cubre **sistemas de numeración, punto fijo, punto flotante, IEEE 754, códigos binarios, lógica combinacional y secuencial**.

---

## 🎯 Características Principales

- ✅ **Punto Fijo Completo** (Q(E,F)): Sin signo, Magnitud-Signo, Complemento a Base
- ✅ **Punto Flotante IEEE 754**: Normalizado, denormalizado, infinito, NaN (qNaN/sNaN)
- ✅ **IEEE754Gen**: Genérico para cualquier base, E_bits, F_bits
- ✅ **Códigos Biquinarios**: 7 bits (IBM 650), 5 bits (Univac), 6 bits (IBM 1401)
- ✅ **Documentación Exhaustiva**: 3000+ líneas teóricas + 2000+ líneas código
- ✅ **Generación Automática**: PDF profesionales y documentos editables
- ✅ **Modular y Extensible**: Diseño basado en plugins
- ✅ **45+ Ejemplos Prácticos**: Ejercicios resueltos paso a paso

---

## � Módulos Implementados

### 🔢 **Sección 2.1: Sistemas de Numeración**

#### 2.1.1-2.1.4: Números Sin Signo y Códigos

| Sistema | Archivo | Descripción | Demo |
|---------|---------|-------------|------|
| **Base B** | `sistemas_numeracion_basicos.py` | Conversión generalizada | ✅ |
| **Conversiones** | `conversion_*.py` | Algoritmos: Común, Relacionadas, Horner | ✅ |
| **BCD** | `sistemas_numeracion_basicos.py` | BCD 8421, Exceso-3, Aiken | ✅ |
| **Johnson** | `sistemas_numeracion_basicos.py` | Código Johnson validado | ✅ |
| **Biquinarios** | `biquinarios.py` | 7, 5, 6 bits + genérico | ✅ |

#### 2.1.1.7: Números Enteros con Signo

| Sistema | Archivo | Rango | Demo |
|---------|---------|-------|------|
| **Magnitud y Signo** | `enteros_signados.py` | ±(B^E - ε) | ✅ |
| **Complemento (B-1)** | `cb_representacion.py` | ±(B^E - ε) | ✅ |
| **Complemento a Base** | `cb_representacion.py` | ±B^E | ✅ |
| **Exceso a K** | `exceso_k_representacion.py` | [0, B^n) desplazado | ✅ |

---

### ➗ **Sección 2.1.5: Punto Fijo Q(E,F)**

| Aspecto | Archivo | Características |
|---------|---------|------------------|
| **Sin Signo** | `punto_fijo.py` | FixedPoint genérico, cualquier base |
| **Con Signo (M&S)** | `punto_fijo_con_signo.py` | FixedPointSignedMS |
| **Con Signo (Complemento)** | `punto_fijo_con_signo.py` | **FixedPointSignedComplement** ⭐ |
| **Conversión de Bases** | `conversion_bases_punto_fijo.py` | Regla: B'^F' ≥ B^F |

**Características:**

- ✅ Base configurable (2, 8, 10, 16, ...)
- ✅ E (enteros) y F (fraccionarios) configurables
- ✅ Operaciones aritméticas (suma, resta, mult, div)
- ✅ Conversión entre representaciones

---

### 🔬 **Sección 2.1.6: Punto Flotante**

| Clase | Archivo | Descripción |
|-------|---------|-------------|
| **FixedPointFloating** | `punto_flotante.py` | Normalización mantisa [1,B) |
| **IEEE754Gen** | `ieee754.py` | ⭐ IEEE 754 genérico |
| **IEEE754 Alias** | `ieee754.py` | Compatibilidad hacia atrás |

**IEEE754Gen - Características:**

- ✅ Base configurable (2, 10, 16, ...)
- ✅ E_bits y F_bits personalizables
- ✅ Números normalizados: ±1.M × B^E
- ✅ Números denormalizados: ±0.M × B^E_min (subnormales)
- ✅ Infinito: ±∞ (E=todos1s, M=0)
- ✅ NaN: qNaN (quiet) y sNaN (signaling)

---

### 🔄 **Códigos Especiales**

| Código | Clase | Archivo | Bits | Status |
|--------|-------|---------|------|--------|
| **Biquinario Genérico** | BiquinaryGen | `biquinarios.py` | Configurable | ✅ |
| **Biquinario 7 bits** | Biquinary7Bit | `biquinarios.py` | 7 (IBM 650) | ✅ |
| **Biquinario 5 bits** | Biquinary5Bit | `biquinarios.py` | 5 (Univac) | ✅ |
| **Biquinario 6 bits** | Biquinary6Bit | `biquinarios.py` | 6 (IBM 1401) | ✅ |

---

### 📚 **Documentación Principal**

| Archivo | Contenido | Líneas |
|---------|----------|--------|
| `IEEE754_Y_BIQUINARIOS.md` | Fundamentos IEEE 754 + biquinarios | 350+ |
| `CLASES_GENERICAS.md` | Especificación IEEE754Gen + BiquinaryGen | 387 |
| `RESUMEN_CLASES_GENERICAS.md` | Resumen ejecutivo con ejemplos | 230+ |
| `PUNTO_FIJO_CON_SIGNO.md` | Punto fijo con signo (M&S, complemento) | 250+ |

---

## 🔍 Ejemplos de Uso Rápido

### Punto Fijo Sin Signo

```python
from core.punto_fijo import FixedPoint

# Q(4,4) base 2
fp = FixedPoint(E=4, F=4, B=2, value=5.25)
print(fp.value)      # 5.25
print(fp.max_value)  # 15.9375
```

### Punto Fijo Con Signo (Complemento)

```python
from core.punto_fijo_con_signo import FixedPointSignedComplement

fp = FixedPointSignedComplement(E=4, F=4, base=2)
M_pos = fp.encode(5.25)      # 84
M_neg = fp.encode(-5.25)     # 428
print(fp.decode(84))         # 5.25
```

### IEEE754Gen (Genérico)

```python
from core.ieee754 import IEEE754Gen

# IEEE 754 Single (32 bits)
ieee = IEEE754Gen(E_bits=8, F_bits=23, base=2)
sign, exp, mant = ieee.encode_normalized(3.14159)
decoded = ieee.decode(sign, exp, mant)  # 3.14159

# Infinito
s, e, m = ieee.encode_infinity(positive=True)
print(ieee.decode(s, e, m))  # "inf"

# NaN
s, e, m = ieee.encode_nan(quiet=True)
print(ieee.decode(s, e, m))  # "qNaN"
```

### Códigos Biquinarios

```python
from core.biquinarios import Biquinary7Bit, Biquinary5Bit

# 7 bits (IBM 650)
bq7 = Biquinary7Bit()
codes = bq7.encode_number("314159")
decoded = bq7.decode_number(codes)  # "314159"

# 5 bits (Univac)
bq5 = Biquinary5Bit()
codes = bq5.encode_number("12345")
decoded = bq5.decode_number(codes)  # "12345"
```

---

## 📖 Documentación Disponible

### 📊 Reportes del Proyecto

- **[ESTADO_ACTUAL.md](ESTADO_ACTUAL.md)** - Situación completa v2.0 (80% completado)
- **[ROADMAP_v2.md](ROADMAP_v2.md)** - Fases 6-9 (próximos 3-6 meses)

### 🔍 Guías Técnicas Punto Fijo & IEEE 754

- **[IEEE754_Y_BIQUINARIOS.md](IEEE754_Y_BIQUINARIOS.md)** - Fundamentos teóricos (350 líneas)
- **[CLASES_GENERICAS.md](CLASES_GENERICAS.md)** - Especificación IEEE754Gen y BiquinaryGen (387 líneas)
- **[RESUMEN_CLASES_GENERICAS.md](RESUMEN_CLASES_GENERICAS.md)** - Resumen ejecutivo con ejemplos (230 líneas)
- **[PUNTO_FIJO_CON_SIGNO.md](PUNTO_FIJO_CON_SIGNO.md)** - Punto fijo con signo (M&S, complemento) (250 líneas)

### 📚 Documentación Heredada (Numeración, BCD, etc)

---

## 📊 Estadísticas de la Documentación

| Métrica | Valor |
|---------|-------|
| **Líneas de documentación** | 2550+ |
| **Archivos de documentación** | 15+ |
| **Ejemplos prácticos** | 45+ |
| **Fórmulas matemáticas** | 50+ |
| **Tablas comparativas** | 20+ |
| **Scripts de demostración** | 18+ |

---

## 🏗️ Estructura del Proyecto

```
GeneratorFEExercises/
├── docs/                          # 📄 Documentación técnica
│   ├── SECCION_2_1_1_*.md        # Números sin signo (6 archivos)
│   ├── SECCION_2_1_1_7_*.md      # Números con signo (4 archivos)
│   ├── SECCION_2_1_2_*.md        # Códigos BCD (3 archivos)
│   ├── SECCION_2_1_3_JOHNSON.md
│   ├── SECCION_2_1_4_BIQUINARIO.md
│   ├── SECCION_2_1_5_PUNTO_FIJO.md
│   ├── SECCION_2_1_6_PUNTO_FLOTANTE.md
│   ├── COMPARATIVA_PUNTO_FIJO_VS_FLOTANTE.md
│   └── INDICE_SECCIONES_2_1_5_2_1_6.md
├── demo_*.py                      # 🎬 Scripts de demostración
├── core/                          # 🔧 Código central
│   ├── sistemas_numeracion_basicos.py
│   ├── enteros_signados.py
│   ├── exceso_k_representacion.py
│   ├── generator_base.py
│   └── catalog.py
├── modules/                       # 📦 Ejercicios por tema
│   ├── numeracion/
│   ├── combinacional/
│   └── secuencial/
├── renderers/                     # 🎨 Generadores de PDF/DOCX
│   ├── latex/
│   └── docx/
└── config/                        # ⚙️ Configuración

```

---

## 🚀 Instalación y Uso Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/GeneratorFEExercises.git
cd GeneratorFEExercises

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución de Demostraciones

```bash
# Números sin signo
python demo_base_b.py
python demo_conversiones.py

# Números con signo
python demo_ms_simple.py
python demo_cb.py
python demo_exceso_k.py
python generar_tabla_comparativa.py

# Códigos especiales
python demo_bcd_validacion.py
python demo_validacion_johnson_biquinario.py
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Pasos:

1. **Fork** el repositorio
2. Crea una rama: `git checkout -b feature/tu-feature`
3. Realiza cambios y commitea: `git commit -m "feat: descripción clara"`
4. **Push**: `git push origin feature/tu-feature`
5. Abre un **Pull Request**

### Áreas de Contribución

- 📝 Adicionar más ejemplos prácticos
- 🐛 Reportar bugs encontrados
- 📚 Expandir secciones de documentación
- 🔬 Crear demostraciones interactivas
- 🧪 Agregar pruebas unitarias

---

## � Roadmap Detallado

### ✅ **Completado en Fase 5 (IEEE 754 + Biquinarios)**

- ✅ IEEE754Gen - Clase genérica para cualquier base/E_bits/F_bits
- ✅ Números normalizados, denormalizados, infinito, NaN
- ✅ BiquinaryGen + 3 variantes (7, 5, 6 bits)
- ✅ Documentación exhaustiva (3 documentos)
- ✅ Demostraciones interactivas (2 demos)
- ✅ 45+ ejemplos de uso

### ✅ **Completado en Fase 6 (Integración Punto Fijo)**

- ✅ **FixedPointUnified** (410 líneas) - Clase única que unifica 3 variantes
  - Parámetros: `E`, `F`, `base`, `signed`, `representation`
  - Elimina duplicación de código (FixedPoint, FixedPointSignedMS, FixedPointSignedComplement)
  - Uso: `FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')`
  - Operaciones completas: encode, decode, add, subtract, multiply, divide

- ✅ **FixedPointComparator** (300+ líneas) - Tablas comparativas renderizadas
  - Exporta a **LaTeX** (PDF), **HTML** (web), **JSON** (datos), **Texto** (CLI)
  - Análisis: rango, precisión, error relativo, epsilon
  - Métodos: `render_latex()`, `render_html()`, `export_json()`, `render_text()`
  - Utilidad: `compare_all_variants()` para comparación rápida

- ✅ **RepresentationValidator** (350+ líneas) - Validador universal
  - Valida punto fijo, IEEE754, biquinarios con reportes detallados
  - Validaciones: 6-7 checks por tipo (rango, epsilon, distribución, etc.)
  - Análisis de error: `compare_error()` entre dos representaciones
  - Batch validation: `batch_validate()` para múltiples configuraciones
  - Output: `ValidationReport` con issues, recomendaciones y metadata

- ✅ **Guía de Migración** (250+ líneas) - Documentación de transición
  - Tablas de comparación: API antigua vs nueva
  - 3 opciones de migración con ejemplos
  - Funciones helper: `from_fixedpoint()`, compatibilidad hacia atrás
  - Beneficios y checklist de adopción

- ✅ **Demo Fase 6** (180 líneas) - Demostración completa
  - 4 escenarios ejecutables: FixedPointUnified, Comparador, Validador, Batch
  - Genera archivos de salida: `comparison.{tex,html,json}`
  - Status: Ejecutado exitosamente, todos los 4 demos funcionan

### 📅 **Fase 7: Interfaz Web (3-4 semanas)**

- [ ] **Simulador IEEE754 Interactivo**
  - Visualización bit a bit en navegador
  - Controles: cambiar base, E_bits, F_bits
  - Mostrar: rango, epsilon machine, números especiales

- [ ] **Calculadora de Conversión de Bases**
  - Input: número + base origen
  - Output: representación en múltiples bases + punto fijo
  - Paso a paso de algoritmos (Horner, común, relacionadas)

- [ ] **Visualizador de Distribución**
  - Gráfica: densidad de números representables
  - Comparativa: FixedPoint vs IEEE754
  - Zoom interactivo

### 📅 **Fase 8: Testing y Documentación (2 semanas)**

- [ ] **Suite de Pruebas Completa**
  - Cobertura 90%+ para `core/`
  - Casos borde: infinito, NaN, desbordamiento, subnormales

- [ ] **Documentación en Inglés**
  - Traducir: CLASES_GENERICAS.md, IEEE754_Y_BIQUINARIOS.md
  - Audiencia internacional

- [ ] **Performance Benchmarks**
  - Conversión de bases (throughput, latencia)
  - Operaciones aritméticas en punto fijo
  - Codificación/decodificación IEEE754

### 📅 **Fase 9: Escalabilidad (1 mes)**

- [ ] **NumPy Array Support**
  - `FixedPointArray` con operaciones vectorizadas
  - `IEEE754Array` con control de excepciones

- [ ] **CI/CD Pipeline**
  - GitHub Actions: Python 3.8-3.12
  - Auto-publish a PyPI

- [ ] **IDE Plugins**
  - VS Code: visualizador punto fijo en debugger
  - IntelliSense: docstrings mejorados

---

## 📊 Estado Actual (Snapshot)

```
Proyecto:      GeneratorFEExercises v2.0
Completado:    ✅ 90% (Punto Fijo + Flotante + Biquinarios + Unificación)
En Progreso:   🔄 0% (Listo para Fase 7)
Pendiente:     ⏳ 10% (Interfaz Web interactiva - Fase 7)

Líneas de Código:     4,200+ (core + utils + nuevas clases)
Líneas de Docs:       4,000+ (markdown + docstrings)
Ejemplos Prácticos:   50+ (demos + uso)
Commits Recientes:    6 (Fase 6: FixedPointUnified, Comparator, Validator)
Tiempo Invertido:     6 semanas (fases 1-6)
```

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 📧 Contacto y Soporte

- 📝 **Issues**: [Reportar problemas](https://github.com/tu-usuario/GeneratorFEExercises/issues)
- 💬 **Discussions**: [Preguntas y sugerencias](https://github.com/tu-usuario/GeneratorFEExercises/discussions)

---

**Última actualización:** 2024 | **Versión:** 2.0
