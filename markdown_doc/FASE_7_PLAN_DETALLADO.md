# 🚀 FASE 7: INTERFAZ WEB INTERACTIVA - PLAN DETALLADO

## 📋 Resumen Ejecutivo

**Objetivo:** Crear una interfaz web interactiva con 3 simuladores para visualizar y explorar sistemas de numeración.

**Duración Estimada:** 3-4 semanas  
**Tecnologías:** Python (Flask/FastAPI) + HTML/CSS/JavaScript  
**Usuarios Target:** Estudiantes de electrónica digital

---

## 🎯 Objetivos de Fase 7

### 1. Simulador IEEE754 Interactivo

- Visualización bit a bit
- Controles para cambiar: base, E_bits, F_bits
- Mostrar: rango, epsilon, números especiales
- Input: ingresar número decimal
- Output: representación en bits, hexadecimal, valor decodificado

### 2. Calculadora de Bases

- Convertidor multi-base interactivo
- Algoritmos paso a paso (Horner, común, relacionadas)
- Entrada: número + base origen
- Salida: representaciones en múltiples bases
- Visualización: tabla de cálculos intermedios

### 3. Visualizador de Distribución

- Gráfica: densidad de números representables
- Comparativa: FixedPoint vs IEEE754
- Zoom interactivo
- Estadísticas: rango, epsilon, distribución

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                  INTERFAZ WEB (HTML/CSS/JS)             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐   │
│  │ IEEE754     │  │ Calculadora  │  │ Visualizador│   │
│  │ Simulador   │  │ de Bases     │  │ Distribución│   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘   │
│         │                │                  │           │
│  ┌──────▼────────────────▼──────────────────▼──────┐   │
│  │     API REST Backend (Flask/FastAPI)           │   │
│  │  /api/ieee754  /api/convert  /api/distribute  │   │
│  └──────┬─────────────────────────────────────────┘   │
│         │                                              │
└─────────┼──────────────────────────────────────────────┘
          │
    ┌─────▼──────────────────┐
    │  CORE (Python)         │
    │  - IEEE754Gen          │
    │  - FixedPointUnified   │
    │  - ConversionEngine    │
    │  - Distribution Utils  │
    └────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
web/                          # Nueva carpeta para Fase 7
├── app.py                    # Servidor Flask/FastAPI principal
├── requirements.txt          # Dependencias web
├── static/
│   ├── css/
│   │   ├── style.css        # Estilos globales
│   │   ├── ieee754.css      # Estilos simulador IEEE754
│   │   ├── converter.css    # Estilos calculadora
│   │   └── distribution.css # Estilos visualizador
│   ├── js/
│   │   ├── ieee754.js       # Lógica simulador IEEE754
│   │   ├── converter.js     # Lógica calculadora
│   │   ├── distribution.js  # Lógica visualizador
│   │   └── api.js           # Cliente API REST
│   └── img/
│       ├── logo.png
│       └── icons/
├── templates/
│   ├── base.html            # Template base
│   ├── index.html           # Página inicio
│   ├── ieee754.html         # Simulador IEEE754
│   ├── converter.html       # Calculadora bases
│   └── distribution.html    # Visualizador
└── api/
    ├── __init__.py
    ├── ieee754_api.py       # Endpoints IEEE754
    ├── converter_api.py     # Endpoints convertidor
    └── distribution_api.py  # Endpoints distribución
```

---

## 🔧 Componentes Técnicos

### Backend (Python)

#### 1. Servidor Web

- Framework: Flask (simple) o FastAPI (moderno)
- Puertos: localhost:5000 o :8000
- CORS: Habilitado para requests desde JavaScript
- JSON: APIs REST con JSON

#### 2. Endpoints IEEE754

```python
POST /api/ieee754/encode
  Input:  {"value": 5.5, "base": 2, "E_bits": 8, "F_bits": 23}
  Output: {"bits": "01000001011000000000000000000000", "hex": "0x40B00000"}

GET /api/ieee754/characteristics
  Input:  {"base": 2, "E_bits": 8, "F_bits": 23}
  Output: {"range": [-3.4e38, 3.4e38], "epsilon": 1.19e-7}

POST /api/ieee754/special
  Input:  {"base": 2, "E_bits": 8, "F_bits": 23}
  Output: {
    "positive_infinity": "01111111100000000000000000000000",
    "negative_infinity": "11111111100000000000000000000000",
    "qnan": "01111111110000000000000000000000",
    "snan": "11111111110000000000000000000001"
  }
```

#### 3. Endpoints Convertidor

```python
POST /api/convert
  Input:  {"value": "1234", "from_base": 10, "to_bases": [2, 8, 16]}
  Output: {
    "decimal": {"value": 1234, "steps": []},
    "binary": {"value": "10011010010", "steps": [...]},
    "octal": {"value": "2322", "steps": [...]},
    "hex": {"value": "4D2", "steps": [...]}
  }

POST /api/convert/algorithm
  Input:  {"value": "1234", "from_base": 10, "to_base": 2, "algorithm": "horner"}
  Output: {"algorithm": "horner", "steps": [...], "result": "10011010010"}
```

#### 4. Endpoints Distribución

```python
GET /api/distribution/fixed_point
  Input:  {"E": 4, "F": 4, "type": "unsigned"}
  Output: {
    "numbers": [0, 0.0625, 0.125, ...],
    "gaps": [0.0625, 0.0625, ...],
    "statistics": {"min": 0, "max": 15.9375, "count": 256}
  }

GET /api/distribution/ieee754
  Input:  {"base": 2, "E_bits": 8, "F_bits": 23}
  Output: {"numbers": [...], "gaps": [...], "statistics": {...}}

POST /api/distribution/compare
  Input:  {"fp_E": 4, "fp_F": 4, "ieee_E": 8, "ieee_F": 23}
  Output: {"comparison": {...}, "chart_data": {...}}
```

### Frontend (HTML/JS)

#### 1. Simulador IEEE754

**Interfaz:**

```
┌─────────────────────────────────────────────────────┐
│          SIMULADOR IEEE754 INTERACTIVO              │
├─────────────────────────────────────────────────────┤
│ Input Número:   [  5.5  ] [Codificar]              │
│                                                     │
│ Parámetros:                                         │
│   Base:      [2      ▼] (2, 8, 10, 16, ...)       │
│   E_bits:    [8      ▼] (1-31)                     │
│   F_bits:    [23     ▼] (1-52)                     │
│                                                     │
│ Representación Binaria:                             │
│ ┌─────────────────────────────────────────────────┐ │
│ │ 0 10000010 10100000000000000000000             │ │
│ │ S E_bits   F_bits                              │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Hexadecimal: 0x41280000                            │
│ Decodificado: 5.5                                  │
│                                                     │
│ Características:                                    │
│   Rango: [-3.4e38, 3.4e38]                        │
│   Epsilon: 1.19e-7                                 │
│   Números especiales: ∞, NaN, subnormales         │
│                                                    │
│ [Mostrar Especiales] [Reset] [Descargar Tabla]   │
└─────────────────────────────────────────────────────┘
```

#### 2. Calculadora de Bases

**Interfaz:**

```
┌─────────────────────────────────────────────────────┐
│         CALCULADORA DE CONVERSIÓN DE BASES          │
├─────────────────────────────────────────────────────┤
│ Número:      [  1234    ]                          │
│ Base Origen: [10  ▼]                               │
│ Bases Destino: [x] 2 [x] 8 [x] 10 [x] 16         │
│                                                     │
│ Algoritmo: [Horner    ▼]                           │
│            [Común     ]                            │
│            [Relacionadas]                          │
│                                                     │
│ [Convertir]                                        │
│                                                     │
│ RESULTADOS:                                        │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Base 2:                                        │ │
│ │   10011010010                                  │ │
│ │   Pasos: 1234/2=617 r0, 617/2=308 r1, ...    │ │
│ │                                                 │ │
│ │ Base 8:                                        │ │
│ │   2322                                          │ │
│ │   Pasos: 1234/8=154 r2, ...                   │ │
│ │                                                 │ │
│ │ Base 16:                                       │ │
│ │   4D2                                           │ │
│ │   Pasos: 1234/16=77 r2, ...                   │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ [Descargar Tabla] [Copiar Resultados]             │
└─────────────────────────────────────────────────────┘
```

#### 3. Visualizador de Distribución

**Interfaz:**

```
┌─────────────────────────────────────────────────────┐
│        VISUALIZADOR DE DISTRIBUCIÓN DE NÚMEROS      │
├─────────────────────────────────────────────────────┤
│ Representación 1:  [Punto Fijo ▼]                  │
│   E: [4  ] F: [4  ] Base: [2  ]                   │
│                                                     │
│ Representación 2:  [IEEE754  ▼]                    │
│   Base: [2  ] E_bits: [8  ] F_bits: [23]          │
│                                                     │
│ [Generar Gráfica]                                   │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                        Zoom: 1x │ │
│ │                                                 │ │
│ │  Punto Fijo (256 números)   IEEE754 (∞ números)│ │
│ │  Densidad alta en [0,10]    Densidad variable  │ │
│ │                    │ ││││ ││ │                 │ │
│ │    0___5____10____15│ ││││ ││ │___10____100   │ │
│ │                    └────────────────┬──────────│ │
│ │  Gap en [10,16]:    Decrece con exp│onente    │ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Estadísticas:                                       │
│   Punto Fijo: Rango [0, 15.9375], Gap 0.0625     │
│   IEEE754: Rango [0, 3.4e38], Gap variable       │
│                                                     │
│ [Exportar PNG] [Datos JSON] [Reset]               │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

### Backend

- **Framework:** Flask (simple, rápido de aprender) o FastAPI (moderno)
- **Python:** 3.8+
- **Dependencias:**

  ```
  Flask==2.3.0
  flask-cors==4.0.0
  numpy==1.24.0  (para gráficas)
  matplotlib==3.7.0  (para generar gráficas)
  ```

### Frontend

- **HTML5:** Estructura semántica
- **CSS3:** Responsive, grid, flexbox
- **JavaScript (Vanilla):** Sin frameworks (más simple)
  - Fetch API para llamadas REST
  - Canvas o Chart.js para gráficas
  - Responsive design (mobile-first)

### Extras

- **Chart.js:** Para gráficas interactivas
- **Plotly.js:** Para gráficas avanzadas (opcional)

---

## 📅 Timeline Estimado

### Semana 1: Fundaciones

- [ ] Día 1-2: Estructura inicial Flask + carpetas
- [ ] Día 3-4: APIs IEEE754 backend
- [ ] Día 5: Frontend IEEE754 básico

### Semana 2: Componentes Adicionales

- [ ] Día 1-2: APIs convertidor backend
- [ ] Día 3-4: Frontend calculadora
- [ ] Día 5: APIs distribución backend

### Semana 3: Visualización + Integración

- [ ] Día 1-2: Frontend distribución
- [ ] Día 3-4: Integración y testing
- [ ] Día 5: Polish y documentación

### Semana 4: Refinamiento (si es necesario)

- [ ] Optimización de performance
- [ ] Mejoras de UX
- [ ] Documentación final

---

## ✅ Criterios de Éxito

- ✅ Simulador IEEE754 funcional con parámetros dinámicos
- ✅ Calculadora de bases mostrando pasos de cálculo
- ✅ Visualizador con gráficas comparativas
- ✅ API REST documentada
- ✅ Interfaz responsive (desktop + mobile)
- ✅ Sin errores críticos
- ✅ Documentación completa
- ✅ Demo ejecutable

---

## 🎨 Consideraciones de Diseño

### UX/UI

- **Colores:** Tema claro/oscuro
- **Responsive:** Mobile-first
- **Accesibilidad:** WCAG 2.1 AA
- **Feedback:** Loading indicators, error messages
- **Documentación Inline:** Help tooltips

### Performance

- **Caché:** Resultados comunes
- **Lazy Loading:** Para gráficas grandes
- **Optimización:** Minificar CSS/JS
- **Compresión:** Gzip para respuestas

### Seguridad

- **Validación Input:** Server-side
- **CORS:** Solo localhost durante dev
- **Rate Limiting:** Proteger APIs
- **Sanitización:** Prevenir inyecciones

---

## 🚀 Primera Tarea

Comenzaremos con:

1. Crear estructura de carpetas (web/)
2. Implementar servidor Flask básico
3. Crear primeras APIs (IEEE754)
4. Frontend IEEE754 básico

**Tiempo estimado:** 1-2 días de trabajo

---

**Status:** Listo para comenzar Fase 7
