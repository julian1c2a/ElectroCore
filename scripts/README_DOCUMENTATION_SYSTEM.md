# 📚 Sistema de Generación de Documentación ElectroCore

## 🎯 Visión General

Este sistema genera automáticamente una estructura completa de documentación interconectada a partir del archivo `docs/CONTENIDOS_FE.md`, creando:

- **Árbol de directorios y archivos markdown** con navegación completa
- **Metadatos JSON** para cada nodo con referencias cruzadas
- **Vinculación con funciones Python** en `core/`
- **Catálogo centralizado** en `config/temario_catalogado.json`

## 🚀 Guía de Uso Rápida

### 1️⃣ Generar la Estructura de Documentación

Genera toda la estructura desde cero:

```bash
python scripts/build_documentation_tree.py --force
```

Esto creará:

- `docs/temario/` - Estructura completa de directorios y markdown
- `docs/temario/**/metadata.json` - Metadatos por directorio
- `config/temario_catalogado.json` - Catálogo actualizado

**Opciones:**

- `--force` - Sobrescribe el directorio existente
- `--dry-run` - Muestra lo que se haría sin ejecutar

### 2️⃣ Vincular Funciones Python

Después de generar la estructura, vincula funciones Python con los nodos de documentación:

```bash
# Modo interactivo
python scripts/link_python_functions.py

# Vincular a un nodo específico
python scripts/link_python_functions.py --node-id 6.1.2.2.1

# Generar vinculaciones automáticas de ejemplo
python scripts/link_python_functions.py --auto-generate
```

### 3️⃣ Navegar la Documentación

Abre `docs/temario/index.md` y navega usando los hipervínculos:

- **Breadcrumb**: Volver a niveles superiores
- **Anterior/Siguiente**: Navegar entre hermanos
- **Contenido**: Explorar hijos

## 📁 Estructura Generada

```
docs/temario/
├── index.md                                    # Índice principal
├── metadata.json                               # Metadatos raíz
├── modulo_1_introduccion.../
│   ├── index.md                                # Índice del módulo
│   ├── metadata.json                           # Metadatos del módulo
│   ├── introduccion_a_la_electronica/
│   │   ├── index.md
│   │   ├── metadata.json
│   │   ├── definicion_y_campo...md
│   │   ├── conceptos_de_senal...md
│   │   └── clasificacion_de_sistemas...md
│   └── ...
├── modulo_2_dispositivos.../
└── ...
```

## 🔗 Sistema de Vinculación Python

### En el Markdown

Cada nodo hoja incluye una sección con las funciones Python asociadas:

```markdown
## 🔧 Funciones Python Asociadas

- ✅ `conversion_algoritmos_detallados.conversion_base_10_a_base_b`
  - Conversión de decimal a base B mediante divisiones sucesivas
- ⚠️ `conversion_algoritmos_detallados.conversion_base_b_a_base_10`
  - Conversión de base B a decimal usando polinomio de Horner
```

**Iconos:**

- ✅ = Función implementada
- ⚠️ = Función pendiente (solo stub)

### En los Metadatos

`docs/temario/**/metadata.json`:

```json
{
  "directory": "modulo_6.../sistemas_de_numeracion/...",
  "nodes": [
    {
      "id": "6.1.2.2.1",
      "title": "Conversión de Base 10 a Base B",
      "python_refs": [
        {
          "module": "conversion_algoritmos_detallados",
          "function": "conversion_base_10_a_base_b",
          "description": "Conversión mediante divisiones sucesivas",
          "implemented": true
        }
      ]
    }
  ]
}
```

### En el Catálogo

`config/temario_catalogado.json`:

```json
{
  "temario_fe": {
    "items": [
      {
        "id": "6.1.2.2.1",
        "titulo": "Conversión de Base 10 a Base B",
        "md_path": "modulo_6.../conversion_de_base_10_a_base_b.md",
        "python_refs": [...]
      }
    ]
  }
}
```

## 🛠️ Flujo de Trabajo Completo

### Escenario: Añadir Nuevo Contenido

1. **Editar** `docs/CONTENIDOS_FE.md`:

   ```markdown
   ### 6.1 Sistemas de Representación
   
   - **6.1.1** Alfabetos y Lenguajes
   - **6.1.2** Sistemas de Numeración
   ```

2. **Regenerar** la estructura:

   ```bash
   python scripts/build_documentation_tree.py --force
   ```

3. **Vincular** funciones Python:

   ```bash
   python scripts/link_python_functions.py
   # Seleccionar nodo 6.1.2
   # Añadir: core.sistemas_numeracion_basicos.conversion_base_b
   ```

4. **Generar stubs** de código:

   ```bash
   # En el menú interactivo: opción "Generar stubs de código"
   ```

5. **Implementar** la función en `core/sistemas_numeracion_basicos.py`:

   ```python
   def conversion_base_b(**kwargs) -> Dict[str, Any]:
       """Conversión entre bases numéricas."""
       # Implementación aquí
   ```

6. **Actualizar estado** a "implementado":

   ```bash
   python scripts/link_python_functions.py --node-id 6.1.2
   # Marcar como implementado
   ```

## 📊 Metadatos de Nodos

Cada nodo contiene los siguientes metadatos:

```python
{
    "id": "6.1.2.2.1",                           # ID jerárquico
    "title": "Conversión de Base 10 a Base B",   # Título original
    "level": 5,                                   # Nivel de anidación
    "parent_id": "6.1.2.2",                      # ID del padre
    "children_ids": [],                           # IDs de hijos
    
    "md_path": "path/to/file.md",                # Ruta al markdown
    "relative_path": "modulo_6/.../file.md",     # Ruta relativa
    
    "python_refs": [...],                         # Referencias Python
    
    "status": "pending",                          # Estado: pending|in_progress|completed
    "has_exercises": false,                       # ¿Tiene ejercicios?
    "has_examples": false,                        # ¿Tiene ejemplos?
    
    "prev_id": "6.1.2.2.0",                      # ID del anterior
    "next_id": "6.1.2.2.2",                      # ID del siguiente
    
    "breadcrumb": [                               # Ruta de navegación
        {"id": "6", "title": "Módulo 6"},
        {"id": "6.1", "title": "Sistemas..."},
        ...
    ]
}
```

## 🎨 Personalización

### Modificar Plantillas

Edita `scripts/build_documentation_tree.py`:

```python
class Config:
    STUB_CONTENT = """
    ## 📝 Contenido Teórico
    
    *Tu plantilla aquí*
    """
```

### Añadir Sintaxis Especial

Actualmente se soporta:

- `{@python: module.function}` - Vincular función Python

Puedes añadir más patrones en `Config.PYTHON_LINK_PATTERN`.

## 🔍 Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `build_documentation_tree.py` | Genera la estructura completa desde CONTENIDOS_FE.md |
| `link_python_functions.py` | Vincula funciones Python de forma interactiva |
| `scaffold_docs.py` | Script legacy (reemplazado por build_documentation_tree.py) |
| `generate_doc_indices.py` | Script legacy para generar index.json |

## 📝 Formato de CONTENIDOS_FE.md

El parser reconoce:

```markdown
# Título Principal (Ignorado)

## Módulo 1: Nombre del Módulo

### 1.1 Sección

- **1.1.1** Subsección
  - Descripción adicional (ignorada)
```

**Reglas:**

- Headers (`##`, `###`) crean directorios
- Items de lista (`-`) crean archivos
- Los números al inicio se eliminan de los nombres de archivo
- Se preservan caracteres especiales en títulos originales

## 🧪 Testing

Para verificar que todo funciona:

```bash
# 1. Generar en modo dry-run
python scripts/build_documentation_tree.py --dry-run

# 2. Generar la estructura
python scripts/build_documentation_tree.py --force

# 3. Verificar la estructura
ls -R docs/temario/

# 4. Verificar el catálogo
cat config/temario_catalogado.json | python -m json.tool

# 5. Probar vinculación
python scripts/link_python_functions.py --auto-generate
```

## 🚧 Limitaciones Actuales

- No se parsean imágenes o enlaces incrustados en CONTENIDOS_FE.md
- Los metadatos `has_exercises` y `has_examples` son siempre `false` por ahora
- La sintaxis `{@python:...}` está definida pero no se parsea actualmente

## 🔮 Próximos Pasos

1. **Parser de sintaxis extendida**: Reconocer `{@python:...}` en CONTENIDOS_FE.md
2. **Generador de ejercicios**: Vincular con el sistema de generación de problemas
3. **Interfaz web**: Visualización interactiva de la documentación
4. **Validador**: Verificar que todas las funciones vinculadas existen
5. **Sincronizador**: Detectar cambios en CONTENIDOS_FE.md y actualizar solo lo necesario

## 📚 Recursos Adicionales

- [electrocore.agent.md](../electrocore.agent.md) - Reglas del proyecto
- [CONTENIDOS_FE.md](../docs/CONTENIDOS_FE.md) - Fuente de la documentación
- [temario_catalogado.json](../config/temario_catalogado.json) - Catálogo centralizado

## 🤝 Contribuir

Para añadir nuevos generadores de documentación:

1. Extender `DocumentationBuilder` en `build_documentation_tree.py`
2. Añadir nuevos tipos de metadatos en `NodeMetadata`
3. Actualizar las plantillas en `Config.STUB_CONTENT`

---

**Última actualización:** 22 de Enero de 2026  
**Versión:** 1.0.0
