# 🔄 Guía de Migración: Punto Fijo Unificado

**Fase 6 - Actualización de API**

Fecha: Enero 2025  
Compatibilidad: Total (las clases antiguas siguen funcionando)

---

## 📋 Resumen Ejecutivo

Se introdujo **FixedPointUnified**, una clase única que reemplaza las 3 anteriores:

- `FixedPoint` (sin signo)
- `FixedPointSignedMS` (magnitud-signo)
- `FixedPointSignedComplement` (complemento)

**Beneficios:**

- ✅ Interfaz unificada y consistente
- ✅ Menos código duplicado
- ✅ Comparación fácil entre variantes
- ✅ Retrocompatibilidad total (las viejas siguen funcionando)

---

## 🚀 Cómo Migrar (3 Opciones)

### Opción 1: Usar FixedPointUnified (Recomendado)

**Antes (FixedPoint):**

```python
from core.punto_fijo import FixedPoint

fp = FixedPoint(E=4, F=4, B=2, value=5.25)
encoded = fp.raw_value
decoded = fp.value
```

**Después (FixedPointUnified):**

```python
from core.punto_fijo_unified import FixedPointUnified

fp = FixedPointUnified(E=4, F=4, base=2, signed=False)
encoded = fp.encode(5.25)
decoded = fp.decode(encoded)
```

---

### Opción 2: Usar Conversor (Mantener Código Existente)

**Si tienes código que usa las clases viejas:**

```python
from core.punto_fijo_unified import from_fixedpoint

# Código existente con FixedPoint
old_fp = FixedPoint(E=4, F=4, B=2, value=5.25)

# Convertir a FixedPointUnified
new_fp = from_fixedpoint(old_fp)

# Ahora puedes usar new_fp con la interfaz nueva
```

---

### Opción 3: Mantener Clases Antiguas

Las clases antiguas **siguen funcionando sin cambios**:

- `core.punto_fijo.FixedPoint`
- `core.punto_fijo_con_signo.FixedPointSignedMS`
- `core.punto_fijo_con_signo.FixedPointSignedComplement`

No hay que cambiar nada si no quieres migrar.

---

## 📊 Tabla Comparativa de APIs

### Sin Signo

| Aspecto | Antiguo (FixedPoint) | Nuevo (FixedPointUnified) |
|---------|---|---|
| Importar | `from core.punto_fijo import FixedPoint` | `from core.punto_fijo_unified import FixedPointUnified` |
| Crear | `fp = FixedPoint(E=4, F=4, B=2, value=5.25)` | `fp = FixedPointUnified(E=4, F=4, base=2, signed=False)` |
| Codificar | `fp.raw_value` (automático) | `fp.encode(5.25)` → 84 |
| Decodificar | `fp.value` (automático) | `fp.decode(84)` → 5.25 |
| Sumar | `a + b` (overload) | `fp.add(a, b)` |
| Info | Atributos directos | `fp.info()` (método) |

### Con Signo - Magnitud y Signo

| Aspecto | Antiguo (FixedPointSignedMS) | Nuevo (FixedPointUnified) |
|---------|---|---|
| Importar | `from core.punto_fijo_con_signo import FixedPointSignedMS` | `from core.punto_fijo_unified import FixedPointUnified` |
| Crear | `fp = FixedPointSignedMS(E=4, F=4, base=2)` | `fp = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms')` |
| Codificar | `fp.encode(5.25)` → M | `fp.encode(5.25)` → M |
| Decodificar | `fp.decode(M)` → 5.25 | `fp.decode(M)` → 5.25 |
| Negar | `fp.complement(M)` → -M | `fp.encode(-5.25)` (directo) |

### Con Signo - Complemento a Base

| Aspecto | Antiguo (FixedPointSignedComplement) | Nuevo (FixedPointUnified) |
|---------|---|---|
| Importar | `from core.punto_fijo_con_signo import FixedPointSignedComplement` | `from core.punto_fijo_unified import FixedPointUnified` |
| Crear | `fp = FixedPointSignedComplement(E=4, F=4, base=2)` | `fp = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')` |
| Codificar | `fp.encode(5.25)` | `fp.encode(5.25)` |
| Decodificar | `fp.decode(M)` | `fp.decode(M)` |
| Sumar | `fp.add(a, b)` | `fp.add(a, b)` ✓ Igual |
| Restar | `fp.subtract(a, b)` | `fp.subtract(a, b)` ✓ Igual |
| Multiplicar | `fp.multiply(a, b)` | `fp.multiply(a, b)` ✓ Igual |

---

## 💡 Ejemplos de Migración Paso a Paso

### Ejemplo 1: Script Simple

**Antiguo:**

```python
from core.punto_fijo import FixedPoint

# Crear punto fijo
fp = FixedPoint(E=8, F=8, B=2, value=128.5)

# Usar
print(f"Valor: {fp.value}")
print(f"Máximo: {fp.max_value}")
print(f"Mínimo: {fp.min_value}")
```

**Nuevo:**

```python
from core.punto_fijo_unified import FixedPointUnified

# Crear punto fijo (misma forma, solo parámetro 'base' en vez de 'B')
fp = FixedPointUnified(E=8, F=8, base=2, signed=False)

# Usar (métodos y atributos similares)
print(f"Valor: {fp.decode(fp.encode(128.5))}")
print(f"Máximo: {fp.max_value}")
print(f"Mínimo: {fp.min_value}")
```

---

### Ejemplo 2: Comparar Variantes

**Antiguo (tedioso - necesitaba 3 clases):**

```python
from core.punto_fijo import FixedPoint
from core.punto_fijo_con_signo import FixedPointSignedMS, FixedPointSignedComplement

fp1 = FixedPoint(E=4, F=4, B=2, value=5.25)
fp2 = FixedPointSignedMS(E=4, F=4, base=2)
fp3 = FixedPointSignedComplement(E=4, F=4, base=2)

# Comparar... (manual, incómodo)
print(f"Sin signo: {fp1.max_value}")
print(f"M&S: {fp2.max_value}")
print(f"Complemento: {fp3.max_value}")
```

**Nuevo (fácil - una clase unificada):**

```python
from core.punto_fijo_unified import FixedPointUnified
from core.punto_fijo_comparator import FixedPointComparator

fp1 = FixedPointUnified(E=4, F=4, base=2, signed=False)
fp2 = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms')
fp3 = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')

# Comparar (automático, tabla genera)
comparator = FixedPointComparator()
print(comparator.render_text([fp1, fp2, fp3]))
```

---

### Ejemplo 3: Validar Representación

**Nuevo (Feature agregado):**

```python
from core.punto_fijo_unified import FixedPointUnified
from core.representation_validator import RepresentationValidator

fp = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')

validator = RepresentationValidator()
report = validator.validate_fixed_point(fp)

print(report.summary())
# Output: Status VALID, 6/6 chequeos pasados, recomendaciones si aplica
```

---

## ✅ Checklist de Migración

- [ ] Actualizar imports (cambiar módulos de origen)
- [ ] Cambiar parámetro `B` → `base`
- [ ] Para sin signo: agregar `signed=False`
- [ ] Para con signo: agregar `signed=True, representation='ms'` o `'complement'`
- [ ] Cambiar métodos si es necesario:
  - `fp.value` → `fp.decode(fp.encode(value))`
  - `fp.raw_value` → `fp.encode(value)`
- [ ] Ejecutar tests para verificar
- [ ] Opcionalmente: usar Comparator y Validator para mejores insights

---

## 🔧 Funciones Helper para Migración

Se proporcionan convertidores automáticos:

```python
from core.punto_fijo_unified import (
    from_fixedpoint,
    from_fixedpoint_signed_ms,
    from_fixedpoint_signed_complement
)

# Convertir instancias antiguas automáticamente
old_fp = FixedPoint(E=4, F=4, B=2, value=5.25)
new_fp = from_fixedpoint(old_fp)

# Ahora new_fp es FixedPointUnified con mismos parámetros
```

---

## 📈 Beneficios de Migrar

### Antes (3 clases)

- Interfaz inconsistente entre clases
- Código duplicado en operaciones
- Difícil comparar variantes
- Sin validación centralizada
- Sin tablas comparativas

### Después (1 clase unificada)

- ✅ Interfaz consistente
- ✅ Código compartido
- ✅ Comparación fácil
- ✅ Validador universal
- ✅ Tablas automáticas (LaTeX, HTML, JSON)

---

## 🎓 Nuevas Capacidades (Fase 6)

Con FixedPointUnified obtienes acceso a:

1. **FixedPointComparator**
   - Renderizar tablas en LaTeX, HTML, JSON
   - Comparar múltiples representaciones
   - Exportar a archivos

2. **RepresentationValidator**
   - Validar punto fijo
   - Detectar problemas
   - Recomendaciones automáticas

3. **batch_validate()**
   - Validar múltiples representaciones
   - Reportes consolidados

---

## 🤝 Soporte y Preguntas

### Si tengo código antiguo que no puedo cambiar

**Solución:** Las clases antiguas siguen funcionando. No es necesario migrar.

### Si quiero lo mejor pero con mínimos cambios

**Solución:** Usa los convertidores (funciones `from_fixedpoint*`)

### Si quiero toda la funcionalidad nueva

**Solución:** Migra completamente a FixedPointUnified

---

## 📚 Referencias

- **Archivo:** `core/punto_fijo_unified.py` (410 líneas, bien documentado)
- **Comparador:** `core/punto_fijo_comparator.py` (300+ líneas)
- **Validador:** `core/representation_validator.py` (350+ líneas)
- **Demo:** `demo_fase6.py` (ejemplos completos)

---

## 🎉 Conclusión

FixedPointUnified es el nuevo estándar. Ofrece:

- Una API simple y consistente
- Todas las variantes (sin signo, M&S, complemento)
- Herramientas poderosas (comparador, validador)
- Retrocompatibilidad total

**Recomendación:** Migra gradualmente, sin prisa.

---

**Última actualización:** Enero 2025  
**Versión:** 2.0-RC1 (Fase 6)
