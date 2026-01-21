# Guía Rápida - Generador de Filtros RC

## Uso Rápido

### 1. **Generar Examen Básico de RC Filters**

```bash
python main_v2.py config/test_exam_rc_filter.json
```

Esto genera:

- `build/latex/analogica/Examen_V2.tex` - Examen (preguntas)
- `build/latex/analogica/Solucion_V2.tex` - Soluciones
- `out/analogica/Examen_V2.pdf` - PDF del examen
- `out/analogica/Solucion_V2.pdf` - PDF de soluciones

### 2. **Configuración Personalizada**

Crear un archivo JSON como `config/mi_examen.json`:

```json
{
  "title": "Mi Examen de Filtros RC",
  "work_type": "analogica",
  "seed": 42,
  "exercises": [
    {
      "id": "rc_filter",
      "qty": 5,
      "difficulty": 2,
      "points": 20
    }
  ]
}
```

Luego:

```bash
python main_v2.py config/mi_examen.json
```

### 3. **Parámetros**

#### `work_type`

- `"digital"` - Circuitos digitales
- `"analogica"` - Circuitos analógicos (incluyendo RC Filters)

#### `difficulty` (para RC Filters)

- `1` - Componentes simples, valores comunes (kΩ, µF)
- `2` - Mix de valores estándar
- `3` - Rango amplio, valores variados

#### `qty`

- Número de ejercicios a generar

#### `seed` (opcional)

- Semilla para reproducibilidad
- Si se omite, es aleatorio

## Tipos de Problemas Generados Automáticamente

El sistema genera aleatoriamente:

### 1. **find_gain** (40%)

Dado R, C y frecuencia de prueba → hallar ganancia

```
Enunciado:
"Se proporciona un filtro Pasa Bajos con R=2200Ω y C=1.000µF.
 La frecuencia de corte es fc=72.3Hz.
 Determine la ganancia a la frecuencia f=723.4Hz."

Se pide:
a) Ganancia lineal
b) Ganancia en dB
c) Desplazamiento de fase
```

### 2. **find_component** (25%)

Dado fc y uno de (R o C) → hallar el otro

```
Enunciado:
"Se proporciona un filtro Pasa Bajos con R=1000Ω.
 La frecuencia de corte debe ser fc=100Hz.
 Calcule el valor de C necesario."

Se pide:
a) Valor de C
b) Verificar con fc = 1/(2πRC)
```

### 3. **find_fc** (20%)

Dado R, C → hallar fc, ωc, τ

```
Enunciado:
"Se proporciona un filtro Pasa Bajos con R=1000Ω y C=1.000µF.
 Determine la frecuencia de corte (fc) y la frecuencia angular (ωc)."

Se pide:
a) Frecuencia de corte (fc) en Hz
b) Frecuencia angular (ωc) en rad/s
c) Constante de tiempo (τ)
d) Ganancia a fc
```

### 4. **identify** (15%)

Dado diagrama → identificar tipo y fc

```
Enunciado:
"Se proporciona un diagrama de Bode de un filtro RC.
 Identifique si es pasa bajos o pasa altos,
 y determine su frecuencia de corte aproximada."

Se pide:
a) ¿Pasa bajos o pasa altos? ¿Por qué?
b) Frecuencia de corte aproximada a -3dB
c) Pendiente de la asíntota
```

## Filtros Soportados

- **Pasa Bajos (Low-Pass)** 50%
  - Fórmula: `H(jω) = 1 / √(1 + (ω/ωc)²)`
  - Uso: Eliminación de ruido de alta frecuencia

- **Pasa Altos (High-Pass)** 50%
  - Fórmula: `H(jω) = (ω/ωc) / √(1 + (ω/ωc)²)`
  - Uso: Eliminación de offset DC, paso de señales rápidas

## Fórmulas Clave Utilizadas

```
Frecuencia de Corte:        fc = 1 / (2πRC)
Frecuencia Angular:         ωc = 2πfc
Constante de Tiempo:        τ = RC

Ganancia Lineal:            G = |H(jω)|
Ganancia en dB:             G_dB = 20 log₁₀(|H(jω)|)

A la frecuencia de corte:   |H(jωc)| = 0.707 = -3.01 dB
```

## Scripts de Prueba Disponibles

### 1. Prueba Básica

```bash
python test_rc_filter.py
```

Genera 4 ejercicios y muestra parámetros.

### 2. Prueba Completa

```bash
python test_rc_filter_full.py
```

Genera + Renderiza + Guarda LaTeX.

### 3. Demostración Completa

```bash
python test_rc_filter_demo.py
```

Muestra:

- Múltiples dificultades
- Distribución de tipos de problemas
- Variedad de filtros

## Estructura de Directorios Generados

```
build/
└── latex/
    └── analogica/
        ├── Examen_V2.tex        ← Enunciado
        ├── Solucion_V2.tex      ← Soluciones
        └── componentes/
            ├── ej1_rc_filter.tex
            ├── ej2_rc_filter.tex
            └── ...

out/
└── analogica/
    ├── Examen_V2.pdf
    └── Solucion_V2.pdf
```

## Ejemplos de Ejercicios Generados

### Ejemplo 1: Find Frequency

```
R = 1000 Ω
C = 1.000 µF
fc = 159.2 Hz
ωc = 1000 rad/s

Pregunta: Calcula fc si R y C son dados
Respuesta: fc = 1/(2π·1000·1e-6) = 159.2 Hz
```

### Ejemplo 2: Find Gain at Frequency

```
R = 2200 Ω
C = 1.000 µF  
fc = 72.3 Hz
Test freq = 723.4 Hz (10×fc)

Pregunta: Ganancia a 723.4 Hz
Respuesta: G = 1/√(1+(72.3/7.23)²) = 0.0995 = -20.04 dB
```

### Ejemplo 3: Find Component

```
R = 1000 Ω
Target fc = 100 Hz
Pregunta: ¿Qué C se necesita?
Respuesta: C = 1/(2π·1000·100) = 1.591 µF
```

## Personalización Avanzada

### Cambiar Distribución de Dificultades

Editar `config/test_exam_rc_filter.json`:

```json
{
  "exercises": [
    {
      "id": "rc_filter",
      "qty": 3,
      "difficulty": 1,    ← Cambiar aquí
      "points": 20
    }
  ]
}
```

### Mezclar con Otros Ejercicios

```json
{
  "exercises": [
    {
      "id": "rc_filter",
      "qty": 3,
      "difficulty": 2,
      "points": 20
    },
    {
      "id": "thevenin_analysis",
      "qty": 2,
      "difficulty": 1,
      "points": 20
    }
  ]
}
```

### Reproducibilidad

Usar mismo `seed`:

```json
{
  "seed": 12345,  ← Mismo seed = mismo examen siempre
  "exercises": [...]
}
```

## Validación de Salida

Verificar que el archivo LaTeX se generó:

```bash
ls -lh build/latex/analogica/Examen_V2.tex
```

Verificar contenido:

```bash
grep "Filtro RC" build/latex/analogica/Examen_V2.tex
```

Compilar PDF (requiere LaTeX):

```bash
cd build/latex/analogica
pdflatex -interaction=nonstopmode Examen_V2.tex
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'modules.analogica'"

→ Asegúrate de estar en el directorio raíz del proyecto

### El PDF tiene errores LaTeX

→ Verifica: `grep -i "error" build/latex/analogica/Examen_V2.log`

### No se generan números aleatorios diferentes

→ El sistema usa semilla fija por defecto. Quita el campo `"seed"` para aleatoriedad

## Contribución / Extensión

Para agregar más tipos de ejercicios de análógica:

1. Crear modelo en `modules/analogica/models.py`
2. Crear generador en `modules/analogica/generators.py`
3. Crear renderer en `renderers/latex/analogica_renderer.py`
4. Registrar en `core/analogica_catalog.py`

Referencia: [RC_FILTER_IMPLEMENTATION.md](RC_FILTER_IMPLEMENTATION.md)

---

**Última actualización:** 2024
**Versión:** 2.0 (RC Filter Generator)
