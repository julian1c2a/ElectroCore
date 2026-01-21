# Opción C: BCD & Biquinarios - Documentación

## Resumen

Implementación de dos representaciones especiales de números: **BCD (Binary Coded Decimal)** y **Biquinario (sistema de 7 bits)**.

## 1. Sistema BCD (Binary Coded Decimal)

### Concepto

BCD es un sistema donde cada dígito decimal (0-9) se codifica independientemente en 4 bits binarios.

#### Ejemplo

```
Número Decimal: 42
Dígito 4 → 0100 (4 en binario)
Dígito 2 → 0010 (2 en binario)
BCD:     → 0100 0010
```

#### Características

- **Rango:** 0-9999 (hasta 4 dígitos)
- **Bits por dígito:** 4 bits (nibble)
- **Total de bits:** 4, 8, 12, 16 (según dígitos)
- **Ventaja:** Conversión directa de números decimales
- **Desventaja:** Menos eficiente que binario puro

### API Endpoint

**POST** `/api/representations/bcd`

**Request:**

```json
{
    "number": 42
}
```

**Response:**

```json
{
    "success": true,
    "number": 42,
    "bcd_binary": "01000010",
    "bcd_hex": "0x42",
    "bcd_decimal": 66,
    "nibbles": [
        {"digit": 4, "binary": "0100", "hex": "4"},
        {"digit": 2, "binary": "0010", "hex": "2"}
    ],
    "total_bits": 8,
    "info": {
        "name": "Binary Coded Decimal",
        "description": "Cada dígito decimal se codifica en 4 bits",
        "range": "0-9999",
        "bits_per_digit": 4
    }
}
```

## 2. Sistema Biquinario

### Concepto

Biquinario es un sistema histórico que usa 2 bits quinarios (base 5) + 3 bits binarios, totalizando 7 bits.

#### Estructura

```
[Parte Quinaria (2 bits)] [Parte Binaria (3 bits)]

Ejemplo con 42:
42 ÷ 5 = 8 resto 2
8 en 2 bits:  10
2 en 3 bits:  010
Biquinario:   10010
```

#### Características

- **Rango:** 0-99
- **Total de bits:** 7 bits (5 quinarios + 2 binarios)
- **Componentes:**
  - Parte Quinaria: 2 bits (0-3, pero representa 0-4 si se usa el primer digit)
  - Parte Binaria: 3 bits (0-7, pero limita a 0-4)

### API Endpoint

**POST** `/api/representations/biquinario`

**Request:**

```json
{
    "number": 42
}
```

**Response:**

```json
{
    "success": true,
    "number": 42,
    "biquinario": "1000010",
    "biquinario_hex": "0x42",
    "biquinario_decimal": 66,
    "components": {
        "quinario_part": {
            "value": 8,
            "binary": "10",
            "position": "5-4"
        },
        "binary_part": {
            "value": 2,
            "binary": "010",
            "position": "3-2-1"
        }
    },
    "total_bits": 7,
    "info": {
        "name": "Biquinario",
        "description": "Sistema de 2 dígitos: uno quinario (base 5) y otro binario",
        "range": "0-99",
        "structure": "2 bits quinario + 3 bits binario"
    }
}
```

## 3. Comparación de Representaciones

Endpoint para visualizar cómo un número se representa en múltiples sistemas simultáneamente.

### API Endpoint

**POST** `/api/representations/compare`

**Request:**

```json
{
    "number": 42
}
```

**Response:**

```json
{
    "success": true,
    "decimal": 42,
    "representations": {
        "binary": "101010",
        "octal": "52",
        "hexadecimal": "2a",
        "bcd": "01000010",
        "biquinario": "1000010"
    },
    "comparison": {
        "total_representations": 5,
        "max_bits": 8
    }
}
```

## 4. Interfaz de Usuario

### Página: `/bcd-biquinario`

Interfaz con tres tabs:

#### Tab 1: BCD (4-8 bits)

- **Input:** Número decimal (0-9999)
- **Outputs:**
  - Visualización binaria con nibbles coloreados
  - Desglose de cada dígito
  - Valor hexadecimal
  - Total de bits

#### Tab 2: Biquinario (7 bits)

- **Input:** Número decimal (0-99)
- **Outputs:**
  - Visualización binaria (7 bits)
  - Componentes (parte quinaria y binaria)
  - Valor hexadecimal
  - Total de bits

#### Tab 3: Comparación

- **Input:** Número decimal (0-99)
- **Outputs:**
  - Tabla comparativa de todas las representaciones
  - Binario, Octal, Hexadecimal, BCD, Biquinario

### Características de la Interfaz

✅ **Visualización de Bits** - Bits coloreados (0=gris, 1=azul)  
✅ **Componentes Desglosados** - Cada parte separada visualmente  
✅ **Información Contextual** - Detalles de cada sistema  
✅ **Tema Oscuro** - Compatible con dark mode  
✅ **Responsive** - Funciona en móviles y tablets  
✅ **Animaciones** - Transiciones suaves  

## 5. Casos de Uso

### BCD

- **Sistemas heredados** - Muchos sistemas vintage usan BCD
- **Displays de 7 segmentos** - Controladores BCD específicos
- **Verificación de dígitos** - Facilita validación de cada dígito
- **Sistemas contables** - Cálculos que requieren precisión decimal

### Biquinario

- **Máquinas perforadoras** - Tarjetas perforadas IBM
- **Sistemas históricos** - Computadoras antiguas (ENIAC)
- **Investigación** - Estudios de sistemas numéricos antiguos
- **Educación** - Enseñanza de representaciones alternativas

## 6. Implementación Técnica

### Archivos Modificados

#### `web/app.py`

- Agregados 3 nuevos endpoints REST
- ~150 líneas de código
- Validación de rangos
- Manejo de errores

#### `web/templates/bcd-biquinario.html`

- 500+ líneas HTML/CSS/JavaScript
- 3 tabs funcionales
- Visualización interactiva de bits
- Componentes animados

#### `web/templates/index.html`

- Nuevo card para BCD/Biquinarios
- Actualizado contador de simuladores (3→4)
- Actualizado contador de APIs (6→9)

#### `web/test_api.py`

- Agregados 3 nuevos tests
- Validación de todos los endpoints

### Stack Tecnológico

```
Frontend:   HTML5 + CSS3 + Vanilla JavaScript
Backend:    Flask 2.3.3 (Python)
APIs:       REST JSON
Testing:    pytest compatible
Styling:    CSS Variables + Dark Mode
```

## 7. Ejemplos de Uso

### Ejemplo 1: Convertir 123 a BCD

```bash
curl -X POST http://localhost:5000/api/representations/bcd \
  -H "Content-Type: application/json" \
  -d '{"number": 123}'
```

Resultado:

```
123 → 0001 0010 0011 (BCD)
```

### Ejemplo 2: Analizar 99 en Biquinario

```bash
curl -X POST http://localhost:5000/api/representations/biquinario \
  -H "Content-Type: application/json" \
  -d '{"number": 99}'
```

Resultado:

```
99 → 1100011 (Biquinario)
Quinaria: 11 (3)
Binaria: 011 (3)
```

### Ejemplo 3: Comparar 50

```bash
curl -X POST http://localhost:5000/api/representations/compare \
  -H "Content-Type: application/json" \
  -d '{"number": 50}'
```

Resultado:

```
Binario:     110010
Octal:       62
Hexadecimal: 32
BCD:         01010000
Biquinario:  1010010
```

## 8. Limitaciones Conocidas

### BCD

- ⚠️ Máximo 9999 (4 dígitos)
- ⚠️ Menos eficiente que binario puro
- ⚠️ Requiere 4 bits por dígito siempre

### Biquinario

- ⚠️ Máximo 99 (solo 2 dígitos efectivos)
- ⚠️ Sistema histórico, poco usado modernamente
- ⚠️ Menos intuitivo que binario/BCD

## 9. Mejoras Futuras

### Corto Plazo (Próximas 2 semanas)

- [ ] Agregar más representaciones especiales (Gray, Excess-3)
- [ ] Visualización paso a paso de conversión
- [ ] Exportar resultados a CSV/PDF
- [ ] Ejemplos interactivos

### Medio Plazo (1-2 meses)

- [ ] Historia de conversiones recientes
- [ ] Generador de problemas con BCD
- [ ] Validador de BCD
- [ ] Calculadora BCD (suma, resta, multiplicación)

### Largo Plazo

- [ ] Editor visual de números en diferentes bases
- [ ] Conversiones de múltiples números simultáneamente
- [ ] Integración con otras representaciones
- [ ] Benchmark de eficiencia

## 10. Recursos Educativos

### Wikipedia

- [Binary Coded Decimal](https://en.wikipedia.org/wiki/Binary-coded_decimal)
- [Bijinary (Spanish)](https://es.wikipedia.org/wiki/C%C3%B3digo_biquinario)

### Libros

- "Digital Computer Fundamentals" - Thomas C. Bartee
- "Electrónica Digital" - Lloydsmith & Tocci

### Vídeos Recomendados

- MIT OpenCourseWare: Digital Systems
- Khan Academy: Number Systems

---

**Status:** ✅ Opción C Completada  
**Tiempo Estimado:** 3-4 horas  
**APIs Agregadas:** 3 nuevos endpoints  
**Líneas de Código:** 650+  
**Nuevas Representaciones:** 2 (BCD, Biquinario)  

**Próximo:** Fase 7 - Completa al 40%  
**Después:** Fase 8 - Testing & Documentation
