# Guía Rápida: Cambiar entre Digital y Análógica

## 🎯 Opción 1: Crear Configuración Personalizada

### Digital Personalizado

Crear archivo `config/mi_examen_digital.json`:

```json
{
  "title": "Mi Examen Digital Personalizado",
  "work_type": "digital",
  "seed": 99999,
  "exercises": [
    {"id": "num_conversion_8bits", "qty": 2, "difficulty": 1},
    {"id": "karnaugh_4vars", "qty": 1, "difficulty": 2},
    {"id": "sequential_analysis", "qty": 1, "difficulty": 3}
  ]
}
```

### Análógica Personalizado

Crear archivo `config/mi_examen_analogica.json`:

```json
{
  "title": "Mi Examen de Circuitos Análógicos",
  "work_type": "analogica",
  "seed": 11111,
  "exercises": [
    {"id": "thevenin_analysis", "qty": 2, "difficulty": 1},
    {"id": "rc_circuit_analysis", "qty": 2, "difficulty": 2}
  ]
}
```

---

## 🚀 Opción 2: Modificar main_v2.py

### Usar Análógica Permanentemente

Editar línea en `main_v2.py`:

**Antes:**

```python
default_config = os.path.join("config", "test_exam.json")
```

**Después:**

```python
default_config = os.path.join("config", "test_exam_analogica.json")
```

Ejecutar:

```bash
python main_v2.py
```

---

## 🎛️ Opción 3: Parámetro por Línea de Comandos (Avanzado)

Modificar `main_v2.py` para aceptar parámetro:

```python
import sys

def main():
    # ... limpieza ...
    
    # Elegir config por parámetro
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "test_exam.json"
    
    default_config = os.path.join("config", config_name)
    
    # ... resto del código ...

if __name__ == "__main__":
    main()
```

Uso:

```bash
# Digital (default)
python main_v2.py

# Análógica
python main_v2.py test_exam_analogica.json

# Personalizado
python main_v2.py mi_examen_digital.json
```

---

## 📋 Ejercicios Disponibles

### Digital (core/catalog.py)

```python
- num_conversion_8bits        → Conversión numérica (8 bits)
- karnaugh_4vars              → Mapa de Karnaugh (4 variables)
- logic_problem               → Problema de lógica
- msi_analysis                → Análisis MSI
- sequential_analysis         → Análisis secuencial
```

### Análógica (core/analogica_catalog.py)

```python
- thevenin_analysis           → Teorema de Thévenin
- divider_circuit             → Divisor de voltaje/corriente
- rc_circuit_analysis         → Análisis de circuito RC
```

---

## 🔧 Cambiar Parámetros de Ejercicios

### Dificultad

```json
{
  "id": "thevenin_analysis",
  "qty": 1,
  "difficulty": 1    // 1 (básico) a 5 (avanzado)
}
```

### Cantidad

```json
{
  "id": "karnaugh_4vars",
  "qty": 3,           // Generar 3 ejercicios iguales (con variaciones)
  "difficulty": 2
}
```

### Puntos (opcional)

```json
{
  "id": "rc_circuit_analysis",
  "qty": 1,
  "difficulty": 2,
  "points": 3.5       // Para scoring
}
```

---

## 📊 Ejemplo: Examen Mixto (Estructura Preparada)

En el futuro, será posible mezclar digital + análógica. Estructura esperada:

```json
{
  "title": "Examen Integrado: Digital + Análógica",
  "work_type": "mixed",
  "seed": 55555,
  "sections": [
    {
      "type": "digital",
      "exercises": [
        {"id": "num_conversion_8bits", "qty": 1},
        {"id": "karnaugh_4vars", "qty": 2}
      ]
    },
    {
      "type": "analogica",
      "exercises": [
        {"id": "thevenin_analysis", "qty": 1},
        {"id": "rc_circuit_analysis", "qty": 2}
      ]
    }
  ]
}
```

---

## 🐛 Troubleshooting

### "No module named 'modules.analogica'"

- Asegúrate que el directorio es `modules/analogica/` (minúsculas)
- Ejecuta desde la raíz del proyecto

### "El archivo de configuración no existe"

- Verifica que la ruta es correcta
- Usa rutas relativas desde la raíz: `config/test_exam.json`

### "work_type no reconocido"

- Solo valores válidos: `"digital"` o `"analogica"`
- Revisa que no hay espacios o mayúsculas extras

### Componentes no se generan

- Verifica que `build/latex/` existe
- Verifica permisos de escritura en el directorio

---

## 📝 Checklist para Crear Nuevo Ejercicio Análógico

- [ ] Crear dataclass en `modules/analogica/models.py`
- [ ] Crear generator class en `modules/analogica/generators.py`
- [ ] Registrar en `core/analogica_catalog.py`
- [ ] Agregar método render en `renderers/latex/analogica_renderer.py`
- [ ] Probar con configuración personalizada
- [ ] Documentar en esta guía

---

## 💬 Soporte

Para dudas sobre:

- **Estructura**: Ver `SUMMARY.md`
- **Detalles técnicos**: Ver `REFACTORING_V2.md`
- **Cambios Fase 1**: Ver `REFACTORING_LOG.md`
