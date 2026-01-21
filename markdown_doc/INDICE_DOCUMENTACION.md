# 📚 ÍNDICE DE DOCUMENTACIÓN - Generador de Exámenes v2.1

## 📖 Orden de Lectura Recomendado

### 1. **PLAN DE ACCIÓN** (📋 15 min)

**Archivo**: [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md)

Qué leer: Todo el documento
Objetivo: Entender qué se va a hacer en las próximas 2 semanas
Preguntas que responde:

- ¿Cuál es el plan de desarrollo?
- ¿Qué tareas hay cada día?
- ¿Cuál es la métrica de éxito?

---

### 2. **RESPUESTA: ARQUITECTURA DE RENDERERS** (✅ 20 min)

**Archivo**: [RESPUESTA_ARQUITECTURA_RENDERERS.md](RESPUESTA_ARQUITECTURA_RENDERERS.md)

Qué leer: Secciones "LA PREGUNTA" y "LA SOLUCIÓN"
Objetivo: Entender por qué necesitamos separación de responsabilidades
Preguntas que responde:

- ¿Por qué los renderers actuales son problemáticos?
- ¿Cómo separar responsabilidades?
- ¿Qué beneficios aporta?

---

### 3. **RESUMEN ARQUITECTURA** (🎯 10 min)

**Archivo**: [RESUMEN_ARQUITECTURA_RENDERERS.md](RESUMEN_ARQUITECTURA_RENDERERS.md)

Qué leer: "¿Por qué es importante?" y "Las 4 Capas Principales"
Objetivo: Visión rápida de la arquitectura propuesta
Preguntas que responde:

- ¿Cómo se estructura la nueva arquitectura?
- ¿Cuál es el impacto?
- ¿Cómo cambiar un estilo?

---

### 4. **ARQUITECTURA DETALLADA** (🏗️ 40 min)

**Archivo**: [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md)

Qué leer: "COMPONENTES PRINCIPALES" (secciones 1-4)
Objetivo: Especificación técnica completa
Preguntas que responde:

- ¿Cómo implementar StyleManager?
- ¿Cómo implementar ContentFactory?
- ¿Cómo crear BaseLatexRenderer?
- ¿Cómo refactorizar los renderers existentes?

---

### 4B. **ROADMAP QUINE-McCLUSKEY** (🔮 30 min - FUTURO)

**Archivo**: [ROADMAP_QUINE_McCLUSKEY.md](ROADMAP_QUINE_McCLUSKEY.md)

Qué leer: "¿CUÁNDO SE NECESITA?" y "ARQUITECTURA PROPUESTA"
Objetivo: Planificar la fase opcional de Semana 3+
Preguntas que responde:

- ¿Necesitamos Quine-McCluskey?
- ¿Por qué SymPy es suficiente ahora?
- ¿Cómo implementar QM cuando sea necesario?
- ¿Cuál es el timeline y esfuerzo?

**Nota**: Este documento es para REFERENCIA FUTURA. En Semana 1-2 usamos SymPy.

---

### 5. **ROADMAP GENERAL** (📊 30 min)

**Archivo**: [ROADMAP.md](ROADMAP.md)

Qué leer: "FASES DE IMPLEMENTACIÓN INMEDIATA" y "ANÁLISIS DEL ESTADO ACTUAL"
Objetivo: Contexto general del proyecto
Preguntas que responde:

- ¿Cuál es el estado actual del proyecto?
- ¿Qué deuda técnica existe?
- ¿Cuál es el plan para 2 semanas?
- ¿Cuál es el plan para después?

---

## 🗂️ DOCUMENTACIÓN POR TIPO

### 🎯 ALTO NIVEL (Para decisiones)

- [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md) - Plan de acción diario
- [ROADMAP.md](ROADMAP.md) - Hoja de ruta general
- [ROADMAP_QUINE_McCLUSKEY.md](ROADMAP_QUINE_McCLUSKEY.md) - Roadmap futuro (Semana 3+)

### 🏗️ ARQUITECTURA (Para diseño)

- [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md) - Especificación técnica
- [RESPUESTA_ARQUITECTURA_RENDERERS.md](RESPUESTA_ARQUITECTURA_RENDERERS.md) - Justificación

### 🎨 VISUAL (Para entendimiento rápido)

- [RESUMEN_ARQUITECTURA_RENDERERS.md](RESUMEN_ARQUITECTURA_RENDERERS.md) - Resumen visual

### 📋 PROYECTO (Para contexto)

- [EnQuéConsisteEsteProyecto.md](EnQuéConsisteEsteProyecto.md) - Descripción general del proyecto

---

## 📍 UBICACIÓN DE ARCHIVOS EN PROYECTO

```
GeneratorFEExercises/
├── 📋 PLAN_ACCION_2SEMANAS.md              ← ¿QUÉ vamos a hacer?
├── 📚 ROADMAP.md                           ← Hoja de ruta general
├── ✅ RESPUESTA_ARQUITECTURA_RENDERERS.md ← ¿POR QUÉ separar?
├── 🎯 RESUMEN_ARQUITECTURA_RENDERERS.md   ← Visión rápida
├── 🏗️ ARQUITECTURA_RENDERERS.md           ← ¿CÓMO implementar?
├── 📖 EnQuéConsisteEsteProyecto.md        ← Contexto del proyecto
│
├── main_v2.py                              ← Orquestador principal
├── config/
├── core/                                   ← Lógica de construcción
│   ├── exam_builder.py
│   ├── generator_base.py
│   └── catalog.py
├── modules/                                ← Generadores (Solvers)
│   ├── numeracion/
│   ├── combinacional/
│   └── secuencial/
└── renderers/                              ← 🔧 Aquí va la refactorización
    └── latex/
        ├── main_renderer.py                ← A refactorizar
        ├── combinacional_renderer.py       ← A refactorizar
        ├── secuencial_renderer.py          ← A refactorizar
        ├── numeracion_renderer.py          ← A refactorizar
        └── utils/
            ├── asset_manager.py            ← Existente
            ├── karnaugh.py                 ← Existente
            ├── truth_table.py              ← Existente
            ├── timing.py                   ← Existente
            ├── compiler.py                 ← 🆕 A crear (Semana 1)
            ├── style_manager.py            ← 🆕 A crear (Semana 2)
            ├── content_factory.py          ← 🆕 A crear (Semana 2)
            ├── base_renderer.py            ← 🆕 A crear (Semana 2)
            └── renderer_factory.py         ← 🆕 A crear (Semana 2)
```

---

## 🎯 GUÍA RÁPIDA POR ROL

### 👨‍💼 PROJECT MANAGER

Lee: [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md)

- Checkpoint diario
- Métricas de éxito
- Riesgos y mitigación

### 👨‍💻 DESARROLLADOR (Semana 1)

Lee: [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md#-semana-1-solvers--compilador-35-horas)
Tareas:

- Implementar solvers (Numeración, Combinacional, Secuencial)
- Crear compilador LaTeX
- Tests de solvers

### 👨‍💻 DESARROLLADOR (Semana 2)

Lee: [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md) + [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md#-semana-2-refactorización-renderers--integración-40-horas)
Tareas:

- Crear StyleManager, ContentFactory, BaseLatexRenderer
- Refactorizar 4 renderers existentes
- Tests de regresión

### 🔍 QA / TESTING

Lee: [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md#-fase-4-tests-de-regresión)
Tareas:

- Escribir tests unitarios para componentes nuevos
- Tests de regresión (output LaTeX debe ser igual)
- Tests end-to-end (pipeline completo)

### 📚 DOCUMENTADOR

Lee: Todos los archivos en orden
Tareas:

- Actualizar docstrings
- Crear guía de "cómo agregar un renderer"
- Ejemplos de uso

---

## ⚡ QUICK START (5 MINUTOS)

**Si tienes 5 minutos**: Lee [RESUMEN_ARQUITECTURA_RENDERERS.md](RESUMEN_ARQUITECTURA_RENDERERS.md)

**Si tienes 15 minutos**: Lee [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md)

**Si tienes 1 hora**: Lee todo en orden de "Orden de lectura recomendado"

---

## 🔗 DOCUMENTOS EXTERNOS REFERENCIADOS

- [SymPy Logic Documentation](https://docs.sympy.org/latest/modules/logic/index.html)
- [TikZ Manual](https://tikz.dev/)
- [CircuiTikZ Package](https://ctan.org/pkg/circuitikz)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns (GoF)](https://refactoring.guru/design-patterns)

---

## 🚀 CÓMO USAR ESTA DOCUMENTACIÓN

### Escenario 1: "Voy a empezar mañana, ¿por dónde comienzo?"

1. Lee [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md) - Semana 1
2. Scansiona [ROADMAP.md](ROADMAP.md) - Estado actual
3. Comienza con primera tarea: "Instalar sympy"

### Escenario 2: "Necesito entender por qué refactorizar renderers"

1. Lee [RESPUESTA_ARQUITECTURA_RENDERERS.md](RESPUESTA_ARQUITECTURA_RENDERERS.md) - La pregunta y solución
2. Lee [RESUMEN_ARQUITECTURA_RENDERERS.md](RESUMEN_ARQUITECTURA_RENDERERS.md) - Visión rápida

### Escenario 3: "Voy a implementar los componentes nuevos"

1. Lee [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md) - Especificación técnica
2. Copia código de ejemplos
3. Ejecuta tests

### Escenario 4: "Algo no funciona, ¿dónde busco?"

1. [PLAN_ACCION_2SEMANAS.md](PLAN_ACCION_2SEMANAS.md) - ¿Qué se esperaba?
2. [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md) - ¿Cómo se supone que debe ser?
3. [ROADMAP.md](ROADMAP.md) - ¿Hay riesgos conocidos?

---

## 📊 ESTADÍSTICAS DOCUMENTACIÓN

```
Documentos nuevos:          5
Líneas totales:             ~3,500
Diagramas ASCII:            ~15
Ejemplos de código:         ~20
Tablas comparativas:        ~8
Checklists:                 ~30

Tiempo lectura completa:    ~2 horas
Tiempo lectura rápida:      ~30 minutos
```

---

## ✅ PRÓXIMOS PASOS

1. **Lectura**: Distribuye documentación al equipo
2. **Discusión**: Revisar plan en reunión de 30 minutos
3. **Planificación**: Estimar tiempo/recursos reales
4. **Ejecución**: Empezar Semana 1 con lista de tareas

---

**Versión**: 1.0
**Fecha**: 15 de enero de 2026
**Estado**: ✅ Completa
