# 🚀 PROPUESTA: Agregar Lenguajes Formales a la Calculadora Web

## 1. VISIÓN GENERAL

Transformar la calculadora web de un **gestor de representaciones numéricas** a una **herramienta completa de Teoría de Lenguajes Formales**.

```
ANTES (Actual):
Calculadora → Bases → IEEE754 → Distribución → BCD/Biquinarios
              └─ Enfoque: Representación numérica

DESPUÉS (Propuesto):
Calculadora → Lenguajes Formales → Alfabetos → Generación → Análisis
              └─ Enfoque: Teoría de Lenguajes + Números
```

---

## 2. NUEVAS FUNCIONALIDADES

### 2.1 Página: Gestor de Alfabetos (`/alphabets`)

#### Interfaz Visual

```
┌─────────────────────────────────────────────────┐
│  GESTOR DE ALFABETOS                      🌙   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─ Crear Nuevo Alfabeto ─────────────────┐   │
│  │                                         │   │
│  │ Nombre: [Binario Extendido    ]        │   │
│  │                                         │   │
│  │ Símbolos (2-36):                        │   │
│  │ [0] [1] [X] [+]                        │   │
│  │ [Agregar símbolo] [Remover]            │   │
│  │                                         │   │
│  │ Orden de Símbolos:                      │   │
│  │ 1. 0 (valor: 0)                         │   │
│  │ 2. 1 (valor: 1)                         │   │
│  │ 3. X (valor: 2)                         │   │
│  │ 4. + (valor: 3)                         │   │
│  │ [Reordenar]                             │   │
│  │                                         │   │
│  │ Símbolo Inicial: [0 ▼]                  │   │
│  │                                         │   │
│  │ [Guardar]  [Cancelar]                   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─ Alfabetos Guardados ──────────────────┐   │
│  │                                         │   │
│  │ ✓ Binario          (2 símbolos)        │   │
│  │   {0, 1}           [Usar] [X]           │   │
│  │                                         │   │
│  │ ✓ Decimal          (10 símbolos)       │   │
│  │   {0, 1, ..., 9}   [Usar] [X]           │   │
│  │                                         │   │
│  │ ✓ Hexadecimal      (16 símbolos)       │   │
│  │   {0-9, A-F}       [Usar] [X]           │   │
│  │                                         │   │
│  │ ● Binario Extendido (4 símbolos)       │   │
│  │   {0, 1, X, +}     [Usar] [Editar] [X] │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Funcionalidades

✅ **Crear alfabetos personalizados**

- 2-36 símbolos
- Símbolos de cualquier carácter
- Definir orden de símbolos
- Símbolo inicial

✅ **Presets incluidos**

- Binario: {0, 1}
- Octal: {0-7}
- Decimal: {0-9}
- Hexadecimal: {0-9, A-F}

✅ **Operaciones CRUD**

- Crear, Editar, Eliminar
- Validación (2-36 símbolos, sin duplicados)
- Exportar/Importar

✅ **Reordenamiento**

- Arrastrar para cambiar orden
- Vista de precedencia visual

---

### 2.2 Página: Generador de Lenguajes (`/languages`)

#### Interfaz Visual

```
┌─────────────────────────────────────────────────┐
│  GENERADOR DE LENGUAJES FORMALES         🌙   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─ Especificar Lenguaje ─────────────────┐   │
│  │                                         │   │
│  │ Nombre: [Números pares 2 bits ]        │   │
│  │                                         │   │
│  │ Alfabeto: [Binario ▼]                   │   │
│  │                                         │   │
│  │ Longitud: [2 ▼] (palabras de 2 bits)   │   │
│  │                                         │   │
│  │ Condiciones (opcional):                 │   │
│  │ [x] Aplicar condición                   │   │
│  │                                         │   │
│  │ Tipo:                                   │   │
│  │ ○ Ninguna (todas las palabras)          │   │
│  │ ○ Patrón (regex): [ ___________]        │   │
│  │ ○ Propiedad (función):                  │   │
│  │   [Seleccionar...]                      │   │
│  │   - Solo pares                          │   │
│  │   - Solo impares                        │   │
│  │   - Palíndromos                         │   │
│  │   - Personalizado: [___________]        │   │
│  │                                         │   │
│  │ [Generar]  [Limpiar]                    │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─ Resultado ────────────────────────────┐   │
│  │                                         │   │
│  │ Lenguaje: L = Σ*[2] donde σ = 2       │   │
│  │ (todas las palabras de longitud 2)     │   │
│  │                                         │   │
│  │ Cardinalidad: |L| = 4                   │   │
│  │ Total de palabras: 4                    │   │
│  │                                         │   │
│  │ Palabras:                               │   │
│  │ ┌─────────────────────────────┐         │   │
│  │ │ 00, 01, 10, 11              │         │   │
│  │ └─────────────────────────────┘         │   │
│  │                                         │   │
│  │ [Copiar]  [Exportar CSV]  [Ver Tabla]   │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Funcionalidades

✅ **Especificar lenguajes**

- Seleccionar alfabeto
- Longitud de palabras (L)
- Condiciones (regex, propiedades)

✅ **Generar palabras**

- Todas las palabras posibles
- Contar cardinalidad
- Visualizar en tabla o lista

✅ **Condiciones predefinidas**

- Pares/Impares
- Palíndromos
- Patrones específicos
- Expresiones regulares

✅ **Exportar**

- Copiar al portapapeles
- Descargar CSV
- Visualizar tabla

---

### 2.3 Página: Ordenador & Significados (`/language-order`)

#### Interfaz Visual

```
┌─────────────────────────────────────────────────┐
│  ORDENADOR DE LENGUAJES                  🌙   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Lenguaje: [Números pares 2 bits ▼]            │
│                                                 │
│  ┌─ Tipo de Orden ────────────────────────┐   │
│  │                                         │   │
│  │ ○ Lexicográfico (alfabético)            │   │
│  │   Ejemplo: 00, 01, 10, 11               │   │
│  │                                         │   │
│  │ ○ Numérico (valor)                      │   │
│  │   Ejemplo: 00(0), 10(2), 01(1), 11(3)   │   │
│  │                                         │   │
│  │ ○ Personalizado (definir orden)         │   │
│  │   Arrastra para reordenar:              │   │
│  │   1. [00 ↕] → 0                         │   │
│  │   2. [01 ↕] → 1                         │   │
│  │   3. [10 ↕] → 2                         │   │
│  │   4. [11 ↕] → 3                         │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─ Asignar Significados ────────────────┐   │
│  │                                         │   │
│  │ [x] Asignar valores automáticos         │   │
│  │                                         │   │
│  │ Modo:                                   │   │
│  │ ○ Índice (0, 1, 2, 3, ...)              │   │
│  │ ○ Binario (0, 1, 2, 3, ...)             │   │
│  │ ○ Decimal equivalente                   │   │
│  │ ○ Personalizado: [Tabla editable]       │   │
│  │                                         │   │
│  │ Tabla de Significados:                  │   │
│  │ ┌──────┬──────────┬────────────┐        │   │
│  │ │ Pos. │ Palabra  │ Significado│        │   │
│  │ ├──────┼──────────┼────────────┤        │   │
│  │ │ 1    │ 00       │ 0          │        │   │
│  │ │ 2    │ 01       │ 1          │        │   │
│  │ │ 3    │ 10       │ 2          │        │   │
│  │ │ 4    │ 11       │ 3          │        │   │
│  │ └──────┴──────────┴────────────┘        │   │
│  │ [Editar célula] [Recargar]              │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [Guardar Orden]  [Cancelar]  [Exportar]       │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Funcionalidades

✅ **Ordenamientos predefinidos**

- Lexicográfico
- Numérico
- Por índice

✅ **Ordenamiento personalizado**

- Arrastrar para cambiar orden
- Vista visual de precedencia

✅ **Asignar significados**

- Automático (índice, binario, decimal)
- Manual (tabla editable)
- Fórmulas personalizadas

✅ **Análisis de orden**

- Visualizar relaciones
- Validar consistencia
- Exportar mapa

---

### 2.4 Página: Análisis de Lenguajes (`/language-analysis`)

#### Interfaz Visual

```
┌─────────────────────────────────────────────────┐
│  ANÁLISIS DE LENGUAJES FORMALES          🌙   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Lenguaje: [Números pares 2 bits ▼]            │
│                                                 │
│  ┌─ Estadísticas ─────────────────────────┐   │
│  │                                         │   │
│  │ Cardinalidad (|L|):      4              │   │
│  │ Longitud de palabras:    2              │   │
│  │ Densidad en Σ*[n]:       25%            │   │
│  │ Máximo valor (si numérico): 3           │   │
│  │ Mínimo valor:            0              │   │
│  │ Promedio:                1.5            │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─ Gráficas ─────────────────────────────┐   │
│  │                                         │   │
│  │ Distribución de Palabras:               │   │
│  │   00 ██████ (25%)                       │   │
│  │   01 ██████ (25%)                       │   │
│  │   10 ██████ (25%)                       │   │
│  │   11 ██████ (25%)                       │   │
│  │                                         │   │
│  │ Densidad Relativa:                      │   │
│  │   Σ*[2] = 4 palabras posibles           │   │
│  │   L ⊆ Σ*[2] con 4 palabras → 100%      │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─ Propiedades Teóricas ─────────────────┐   │
│  │                                         │   │
│  │ ✓ Es determinístico (sin ambigüedad)   │   │
│  │ ✓ Es regular (Σ*[2])                    │   │
│  │ ✓ Es finito (|L| = 4)                   │   │
│  │ ✓ Está ordenado lexicográficamente     │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Funcionalidades

✅ **Estadísticas**

- Cardinalidad
- Densidad
- Valores min/max/promedio

✅ **Visualizaciones**

- Distribución de palabras
- Densidad relativa
- Gráficas comparativas

✅ **Análisis teórico**

- ¿Es regular?
- ¿Es finito/infinito?
- ¿Es determinístico?
- Propiedades formales

✅ **Exportar análisis**

- PDF con gráficas
- CSV con datos
- LaTeX para documentos

---

## 3. NUEVOS ENDPOINTS API

### 3.1 Alfabetos API

```python
# GET  /api/alphabets
#      Listar todos los alfabetos
#      Response: [{ id, name, symbols, cardinality, ... }, ...]

# POST /api/alphabets
#      Crear alfabeto
#      Body: { name, symbols, symbol_order, initial_symbol }
#      Response: { id, ... }

# GET  /api/alphabets/{id}
#      Obtener alfabeto específico
#      Response: { id, name, symbols, ... }

# PUT  /api/alphabets/{id}
#      Editar alfabeto
#      Body: { name, symbols, symbol_order, initial_symbol }
#      Response: { id, ... }

# DELETE /api/alphabets/{id}
#      Eliminar alfabeto
#      Response: { success: true }

# GET  /api/alphabets/presets
#      Obtener alfabetos predefinidos
#      Response: [
#          { name: "Binario", symbols: ["0", "1"] },
#          { name: "Octal", symbols: ["0"-"7"] },
#          ...
#      ]

# POST /api/alphabets/{id}/validate
#      Validar alfabeto
#      Body: { symbols: [...] }
#      Response: { valid: true/false, error: "..." }
```

### 3.2 Lenguajes API

```python
# GET  /api/languages
#      Listar todos los lenguajes
#      Response: [{ id, name, alphabet_id, length, ... }, ...]

# POST /api/languages
#      Crear lenguaje
#      Body: { name, alphabet_id, length, conditions }
#      Response: { id, ... }

# GET  /api/languages/{id}
#      Obtener lenguaje específico
#      Response: { id, name, words, cardinality, ... }

# PUT  /api/languages/{id}
#      Editar lenguaje
#      Body: { name, length, conditions }
#      Response: { id, ... }

# DELETE /api/languages/{id}
#      Eliminar lenguaje
#      Response: { success: true }

# POST /api/languages/{id}/generate
#      Generar todas las palabras del lenguaje
#      Response: { words: [...], count: 4, density: 0.25 }

# POST /api/languages/{id}/apply-conditions
#      Aplicar condiciones de pertenencia
#      Body: { condition_type, condition_value }
#      Response: { filtered_words: [...], count: 2 }

# POST /api/languages/{id}/order
#      Aplicar ordenamiento
#      Body: { order_type, custom_order }
#      Response: { ordered_words: [...] }

# POST /api/languages/{id}/assign-meanings
#      Asignar significados/valores
#      Body: { meanings: { "word": value, ... } }
#      Response: { meanings: {...} }
```

### 3.3 Análisis API

```python
# GET  /api/languages/{id}/analysis
#      Análisis completo del lenguaje
#      Response: { stats: {...}, properties: {...}, visualizations: {...} }

# GET  /api/languages/{id}/statistics
#      Estadísticas del lenguaje
#      Response: { cardinality, density, min, max, avg, ... }

# GET  /api/languages/{id}/properties
#      Propiedades teóricas
#      Response: { is_finite, is_regular, is_deterministic, ... }

# GET  /api/languages/{id}/comparison
#      Comparar con otros lenguajes
#      Query: ?other_ids=id1,id2,id3
#      Response: { comparison_table: [...] }
```

---

## 4. MODELOS DE DATOS

### Backend (Python - Flask/SQLAlchemy)

```python
# models/alphabet.py
class Alphabet(db.Model):
    __tablename__ = 'alphabets'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbols = db.Column(db.JSON, nullable=False)  # ['0', '1', ...]
    cardinality = db.Column(db.Integer)           # len(symbols)
    symbol_order = db.Column(db.JSON)             # {'0': 0, '1': 1, ...}
    initial_symbol = db.Column(db.String(10))
    is_preset = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    languages = db.relationship('Language', backref='alphabet', cascade='all, delete-orphan')
    
    @property
    def is_valid(self):
        return 2 <= len(self.symbols) <= 36 and len(set(self.symbols)) == len(self.symbols)

# models/language.py
class Language(db.Model):
    __tablename__ = 'languages'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alphabet_id = db.Column(db.String(36), db.ForeignKey('alphabets.id'))
    length = db.Column(db.Integer, nullable=False)
    conditions = db.Column(db.String(500))        # regex o descripción
    words = db.Column(db.JSON, nullable=False)    # ["00", "01", "10", "11"]
    cardinality = db.Column(db.Integer)           # len(words)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    order_id = db.Column(db.String(36), db.ForeignKey('language_orders.id'))
    order = db.relationship('LanguageOrder', backref='language', uselist=False)
    
    @property
    def density(self):
        """Densidad relativa a Σ*[n]"""
        max_words = self.alphabet.cardinality ** self.length
        return self.cardinality / max_words if max_words > 0 else 0

# models/language_order.py
class LanguageOrder(db.Model):
    __tablename__ = 'language_orders'
    
    id = db.Column(db.String(36), primary_key=True)
    language_id = db.Column(db.String(36), db.ForeignKey('languages.id'))
    order_type = db.Column(db.String(50))         # 'lexicographic', 'numeric', 'custom'
    ordered_words = db.Column(db.JSON)            # [palabra en orden]
    meanings = db.Column(db.JSON)                 # {"palabra": valor, ...}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 5. ESTRUCTURA DE CARPETAS NECESARIA

```
web/
├── app.py                     (modificado - agregar rutas)
├── requirements.txt           (modificado - agregar dependencias)
├── static/
│   ├── css/
│   │   ├── alphabets.css      (NUEVO)
│   │   ├── languages.css      (NUEVO)
│   │   └── analysis.css       (NUEVO)
│   └── js/
│       ├── alphabets.js       (NUEVO)
│       ├── languages.js       (NUEVO)
│       ├── analysis.js        (NUEVO)
│       └── alphabet-builder.js (NUEVO)
├── templates/
│   ├── alphabets.html         (NUEVO)
│   ├── languages.html         (NUEVO)
│   ├── language-order.html    (NUEVO)
│   └── language-analysis.html (NUEVO)
├── models/
│   ├── alphabet.py            (NUEVO)
│   ├── language.py            (NUEVO)
│   └── language_order.py      (NUEVO)
├── services/
│   ├── alphabet_service.py    (NUEVO)
│   ├── language_service.py    (NUEVO)
│   └── analysis_service.py    (NUEVO)
└── routes/
    ├── alphabet_routes.py     (NUEVO)
    ├── language_routes.py     (NUEVO)
    └── analysis_routes.py     (NUEVO)
```

---

## 6. PLAN DE IMPLEMENTACIÓN

### Fase 7.1: Alfabetos (2 días)

```
Día 1:
  - Modelos (Alphabet)
  - Rutas API (CRUD)
  - Presets
  - Validación

Día 2:
  - Frontend: /alphabets
  - Interfaz CRUD
  - Gestor visual de símbolos
  - Tests
```

### Fase 7.2: Lenguajes (3 días)

```
Día 1:
  - Modelos (Language)
  - Generador de palabras
  - Rutas API

Día 2:
  - Condiciones (regex, propiedades)
  - Filtrado de palabras
  - Cálculo de cardinalidad

Día 3:
  - Frontend: /languages
  - Interfaz de especificación
  - Visualización de palabras
  - Tests
```

### Fase 7.3: Ordenamiento (2 días)

```
Día 1:
  - Modelos (LanguageOrder)
  - Algoritmos de ordenamiento
  - Asignación de significados
  - Rutas API

Día 2:
  - Frontend: /language-order
  - Interfaz de reordenamiento
  - Tabla de significados
  - Tests
```

### Fase 7.4: Análisis (2 días)

```
Día 1:
  - Service de análisis
  - Cálculo de propiedades
  - Estadísticas
  - Rutas API

Día 2:
  - Frontend: /language-analysis
  - Gráficas con Chart.js
  - Visualización de propiedades
  - Tests
```

### Total Estimado: 9 días de desarrollo

---

## 7. INTEGRACIÓN CON HOME PAGE

Modificar `/` para incluir enlace a nuevas funcionalidades:

```html
<!-- AGREGAR en index.html -->

<!-- Gestor de Alfabetos -->
<div class="simulator-card">
    <div class="simulator-header">
        <div class="icon">🔤</div>
        <h2>Gestor de Alfabetos</h2>
        <p>Crear y gestionar alfabetos (2-36 símbolos)</p>
    </div>
    <div class="simulator-body">
        <ul>
            <li>Crear alfabetos personalizados</li>
            <li>Presets (Bin, Oct, Dec, Hex)</li>
            <li>Definir orden de símbolos</li>
            <li>Validación automática</li>
        </ul>
        <button class="btn-primary" onclick="window.location.href='/alphabets'">
            Crear Alfabeto
        </button>
    </div>
</div>

<!-- Generador de Lenguajes -->
<div class="simulator-card">
    <div class="simulator-header">
        <div class="icon">📚</div>
        <h2>Generador de Lenguajes</h2>
        <p>Generar lenguajes formales con condiciones</p>
    </div>
    <div class="simulator-body">
        <ul>
            <li>Especificar longitud de palabras</li>
            <li>Aplicar condiciones de pertenencia</li>
            <li>Generar todas las palabras</li>
            <li>Calcular cardinalidad y densidad</li>
        </ul>
        <button class="btn-primary" onclick="window.location.href='/languages'">
            Crear Lenguaje
        </button>
    </div>
</div>

<!-- Ordenador de Lenguajes -->
<div class="simulator-card">
    <div class="simulator-header">
        <div class="icon">📊</div>
        <h2>Ordenador de Lenguajes</h2>
        <p>Asignar orden y significados</p>
    </div>
    <div class="simulator-body">
        <ul>
            <li>Ordenar lexicográficamente</li>
            <li>Ordenar numéricamente</li>
            <li>Asignar significados/valores</li>
            <li>Definir precedencia de símbolos</li>
        </ul>
        <button class="btn-primary" onclick="window.location.href='/language-order'">
            Ordenar Lenguaje
        </button>
    </div>
</div>

<!-- Análisis de Lenguajes -->
<div class="simulator-card">
    <div class="simulator-header">
        <div class="icon">🔬</div>
        <h2>Análisis de Lenguajes</h2>
        <p>Propiedades teóricas y estadísticas</p>
    </div>
    <div class="simulator-body">
        <ul>
            <li>Cardinalidad y densidad</li>
            <li>Propiedades teóricas</li>
            <li>Visualizaciones gráficas</li>
            <li>Comparación con otros lenguajes</li>
        </ul>
        <button class="btn-primary" onclick="window.location.href='/language-analysis'">
            Analizar Lenguaje
        </button>
    </div>
</div>
```

---

## 8. CONCLUSIÓN

### Transformación de la Aplicación

**DE:**

```
Calculadora de números
├── IEEE754
├── Conversión de bases
├── Distribuciones
└── BCD/Biquinarios
```

**A:**

```
Sistema completo de Lenguajes Formales
├── Números (existente)
├── Alfabetos (nuevo)
├── Lenguajes (nuevo)
├── Ordenamientos (nuevo)
└── Análisis teórico (nuevo)
```

### Impacto

- ✅ **Completitud:** De 75% a 95%
- ✅ **Cobertura:** De números a teoría de lenguajes
- ✅ **Utilidad educativa:** Se multiplica
- ✅ **Alcance académico:** Licenciatura → Postgrado

### Recomendación: **IMPLEMENTAR EN FASE 7.1-7.4**

Esto completaría la aplicación como una herramienta de teoría de lenguajes formal profesional.
