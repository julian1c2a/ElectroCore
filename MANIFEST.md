# SERIE 1: LENGUAJES FORMALES - MANIFEST DE ARCHIVOS

## 📦 ARCHIVOS CREADOS / MODIFICADOS (Días 1-5)

### Fase 1: Backend (Días 1-2)

#### Modelos de Datos

- **web/models.py** (350 líneas)
  - `Alphabet` - Clase para representar alfabetos (2-36 símbolos)
  - `Language` - Clase para lenguajes formales con palabras
  - `LanguageOrder` - Clase para ordenamientos y significados
  - Presets: `BINARY_ALPHABET`, `DECIMAL_ALPHABET`, `HEXADECIMAL_ALPHABET`, `DNA_ALPHABET`

#### Servicios de Lógica

- **web/services_alphabet.py** (120 líneas)
  - `AlphabetService` - CRUD y operaciones sobre alfabetos
  
- **web/services_language.py** (200 líneas)
  - `LanguageService` - Generación de lenguajes con 6 condiciones
  
- **web/services_analysis.py** (150 líneas)
  - `AnalysisService` - Análisis de lenguajes y ordenamientos

#### API REST (15 endpoints)

- **web/app.py** (modificado)
  - 7 endpoints para alfabetos
  - 5 endpoints para lenguajes
  - 3 endpoints para análisis
  - 4 nuevas rutas HTML

#### Tests

- **web/test_formal_languages.py** (350 líneas)
  - 16 test cases para todos los endpoints

---

### Fase 2: Frontend (Días 3-5)

#### Páginas HTML Interactivas

1. **web/templates/alphabets.html** (450 líneas)
   - Gestor completo de alfabetos
   - CRUD operations
   - Presets management
   - Estadísticas en tiempo real

2. **web/templates/languages.html** (450 líneas)
   - Generador de lenguajes
   - 6 condiciones de generación
   - Visualización de palabras
   - Estadísticas por lenguaje

3. **web/templates/language-analysis.html** (400 líneas)
   - Análisis visual de lenguajes
   - Gráficos con Chart.js
   - Distribución de símbolos
   - Análisis de patrones

4. **web/templates/language-order.html** (350 líneas)
   - Creación de ordenamientos
   - Asignación de significados
   - Visualización de resultados
   - 3 tipos de ordenamiento + 2 tipos de significados

#### Página Principal

- **web/templates/index.html** (modificado)
  - 5 nuevas tarjetas para páginas de Lenguajes Formales
  - Estadísticas actualizadas (24 APIs, 9 simuladores)

---

## 📊 ESTADÍSTICAS TOTALES

| Métrica | Valor |
|---------|-------|
| **Líneas de código creadas** | 1,755 (frontend) |
| **Líneas de código backend** | 820 |
| **Total líneas nuevas** | 2,575 |
| **Archivos HTML nuevos** | 4 |
| **Archivos Python nuevos** | 3 (servicios) + 1 test |
| **Endpoints REST** | 15 |
| **Rutas Flask** | 4 |
| **Páginas del sitio** | 9 (5 anteriores + 4 nuevas) |
| **Simuladores disponibles** | 9 |

---

## 🗂️ ESTRUCTURA DE DIRECTORIOS

```
web/
├── templates/
│   ├── index.html (modificado)
│   ├── ieee754.html (existente)
│   ├── converter.html (existente)
│   ├── distribution.html (existente)
│   ├── bcd-biquinario.html (existente)
│   ├── alphabets.html (NEW)
│   ├── languages.html (NEW)
│   ├── language-analysis.html (NEW)
│   └── language-order.html (NEW)
├── app.py (modificado - agregadas 4 rutas + 15 endpoints)
├── models.py (NEW)
├── services_alphabet.py (NEW)
├── services_language.py (NEW)
├── services_analysis.py (NEW)
├── test_formal_languages.py (NEW)
├── static/
├── api/
└── __init__.py
```

---

## 🔌 APIS DISPONIBLES

### Alfabetos (7 endpoints)

```
GET    /api/alphabets                    - Listar todos
POST   /api/alphabets                    - Crear nuevo
GET    /api/alphabets/<id>               - Obtener detalles
PUT    /api/alphabets/<id>               - Actualizar
DELETE /api/alphabets/<id>               - Eliminar
GET    /api/alphabets/presets/list       - Listar presets
POST   /api/alphabets/<id>/validate      - Validar
```

### Lenguajes (5 endpoints)

```
GET    /api/languages                    - Listar todos
POST   /api/languages                    - Crear nuevo
POST   /api/languages/<id>/generate      - Generar palabras
GET    /api/languages/<id>               - Obtener detalles
DELETE /api/languages/<id>               - Eliminar
```

### Análisis (3 endpoints)

```
GET    /api/analysis/languages/<id>/analyze      - Análisis completo
POST   /api/analysis/orders                      - Crear ordenamiento
GET    /api/analysis/orders                      - Listar ordenamientos
```

---

## 🎨 CARACTERÍSTICAS FRONTEND

### Diseño Visual

- ✅ Gradientes lineales (púrpura-violeta)
- ✅ Transiciones suaves y animaciones
- ✅ Diseño responsivo (grid layout)
- ✅ Tablas con estilos alternos
- ✅ Barras de progreso dinámicas
- ✅ Hover effects y efectos visuales

### Componentes Interactivos

- ✅ Formularios con validación
- ✅ Selectores y checkboxes
- ✅ Tablas dinámicas
- ✅ Gráficos (Chart.js)
- ✅ Modales/Pop-ups
- ✅ Actualización en tiempo real

### Funcionalidades Avanzadas

- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validación de entrada (cliente + servidor)
- ✅ Manejo de errores robusto
- ✅ Estadísticas dinámicas
- ✅ Exportación de datos
- ✅ Generación combinatoria

---

## 🚀 RUTAS DEL SITIO WEB

| URL | Página | Descripción |
|-----|--------|-------------|
| `/` | index.html | Página principal con tarjetas |
| `/ieee754` | ieee754.html | Simulador IEEE754 |
| `/converter` | converter.html | Convertidor de bases |
| `/distribution` | distribution.html | Visualizador de distribución |
| `/bcd-biquinario` | bcd-biquinario.html | Convertidor BCD/Biquinario |
| **`/alphabets`** | alphabets.html | **Gestor de Alfabetos (NEW)** |
| **`/languages`** | languages.html | **Generador de Lenguajes (NEW)** |
| **`/language-analysis`** | language-analysis.html | **Análisis de Lenguajes (NEW)** |
| **`/language-order`** | language-order.html | **Ordenamientos y Significados (NEW)** |

---

## 📚 LIBRERÍAS EXTERNAS

### Frontend

- **Chart.js 3.9.1** - Visualización de gráficos
- **Fetch API** - Comunicación asíncrona (nativa)

### Backend

- **Flask** - Servidor web
- **Flask-CORS** - Manejo de CORS
- **Python 3.8+** - Lenguaje

---

## 🧪 TESTS INCLUIDOS

### Test File: `web/test_formal_languages.py`

- 16 test cases cubriendo:
  - CRUD de alfabetos
  - Creación de lenguajes
  - Generación de palabras (6 condiciones)
  - Análisis de lenguajes
  - Generación de significados
  - Casos de error

### Ejecución

```bash
python -m pytest web/test_formal_languages.py -v
```

---

## 📝 DOCUMENTACIÓN

- **DIA_1_2_COMPLETADO.md** - Resumen del backend (Días 1-2)
- **DIA_3_5_COMPLETADO.md** - Resumen del frontend (Días 3-5)
- **MANIFEST.md** (este archivo) - Índice completo de archivos
- **README.md** - Guía general del proyecto

---

## ⚙️ CÓMO EJECUTAR

### 1. Instalar dependencias

```bash
cd web
pip install -r requirements.txt
```

### 2. Iniciar servidor

```bash
python app.py
```

### 3. Acceder al sitio

```
http://localhost:5000
```

### 4. Ejecutar tests

```bash
python -m pytest test_formal_languages.py -v
```

---

## 🔍 PUNTOS TÉCNICOS CLAVE

### Validaciones

- Cardinales de alfabeto: 2-36 símbolos
- Longitud de palabras: 1-10
- Caracteres especiales permitidos: letras, números, símbolos
- Unicidad de alfabetos personalizados

### Rendimiento

- Caché de datos en JavaScript
- Lazy loading de tablas grandes
- Límite de 20 items mostrados por defecto
- Compresión de respuestas JSON

### Seguridad

- Validación de entrada (cliente + servidor)
- CORS habilitado pero restringido
- Sanitización de datos
- Manejo seguro de errores

---

## 📋 CHECKLIST DE DESARROLLO

### Backend (✅ Completado)

- ✅ Modelos de datos diseñados
- ✅ Servicios implementados
- ✅ 15 endpoints creados
- ✅ Tests escritos (16 casos)
- ✅ Documentación incluida

### Frontend (✅ Completado)

- ✅ 4 páginas HTML creadas
- ✅ Estilos CSS aplicados
- ✅ JavaScript funcional
- ✅ Integración API funcional
- ✅ Tablas y gráficos renderizados
- ✅ Rutas Flask agregadas
- ✅ Index.html actualizado

### Integración (✅ Completado)

- ✅ Todas las rutas funcionales
- ✅ APIs accesibles
- ✅ Estadísticas actualizadas
- ✅ Documentación completa

---

## 🎯 ESTADO FINAL

**Fase:** 8/9  
**Completitud:** 95%  
**APIs:** 24 (9 anteriores + 15 nuevas)  
**Simuladores:** 9 (5 anteriores + 4 nuevos)  
**Líneas de código:** ~4,750  

**SERIE 1: LENGUAJES FORMALES** ✅ **COMPLETADA**

---

*Última actualización: Día 5 (Fase 3-5)*
