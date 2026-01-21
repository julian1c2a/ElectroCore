# GeneratorFEExercises - Web UI (Fase 7)

## Descripción

Interfaz web interactiva para explorar y entender sistemas de representación de números.

## Características

### 1. Simulador IEEE754 Interactivo
- Visualización bit a bit de números en punto flotante
- Parámetros dinámicos (base, E_bits, F_bits)
- Representación de números especiales (∞, NaN, subnormales)
- Cálculo automático de características del sistema

### 2. Calculadora de Conversión de Bases
- Convertidor multi-base (binaria, octal, decimal, hexadecimal)
- Tabla de resultados con conversión automática
- Soporte para bases personalizadas

### 3. Visualizador de Distribución de Números
- Análisis de distribución en punto fijo
- Estadísticas: rango, epsilon, total de números
- Comparativa visual (próximamente con Chart.js)

## Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

1. Clonar el repositorio:
```bash
cd GeneratorFEExercises
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
cd web
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
cd web
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

### Acceder a los simuladores

- **Página principal:** http://localhost:5000
- **IEEE754 Simulador:** http://localhost:5000/ieee754
- **Calculadora de Bases:** http://localhost:5000/converter
- **Visualizador de Distribución:** http://localhost:5000/distribution

### Verificar salud del servidor

```bash
curl http://localhost:5000/api/health
```

## Estructura de Archivos

```
web/
├── app.py                  # Servidor Flask principal
├── requirements.txt        # Dependencias Python
├── static/                 # Archivos estáticos
│   ├── css/               # Estilos CSS
│   └── js/                # Scripts JavaScript
├── templates/             # Plantillas HTML
│   ├── index.html         # Página inicio
│   ├── ieee754.html       # Simulador IEEE754
│   ├── converter.html     # Calculadora bases
│   └── distribution.html  # Visualizador
└── api/                   # Módulos API (para expansión futura)
```

## API Endpoints

### IEEE754

**POST /api/ieee754/encode**
```json
Request:
{
    "value": 5.5,
    "base": 2,
    "E_bits": 8,
    "F_bits": 23
}

Response:
{
    "success": true,
    "value": 5.5,
    "bits": "01000001011000000000000000000000",
    "hex": "0x41600000",
    "sign": "0",
    "exponent": "10000010",
    "mantissa": "01100000000000000000000",
    "decoded": 5.5,
    "valid": true
}
```

**POST /api/ieee754/characteristics**
```json
Request:
{
    "base": 2,
    "E_bits": 8,
    "F_bits": 23
}

Response:
{
    "success": true,
    "total_bits": 32,
    "E_min": -126,
    "E_max": 127,
    "min_positive": 1.17549e-38,
    "max_positive": 3.40282e+38,
    "epsilon": 1.19209e-07
}
```

**POST /api/ieee754/special**
```json
Request:
{
    "base": 2,
    "E_bits": 8,
    "F_bits": 23
}

Response:
{
    "success": true,
    "positive_zero": "00000000000000000000000000000000",
    "negative_zero": "10000000000000000000000000000000",
    "positive_infinity": "01111111100000000000000000000000",
    "negative_infinity": "11111111100000000000000000000000",
    "qnan": "01111111110000000000000000000000",
    "snan": "11111111110000000000000000000001"
}
```

### Conversión de Bases

**POST /api/convert**
```json
Request:
{
    "value": "1234",
    "from_base": 10,
    "to_bases": [2, 8, 16]
}

Response:
{
    "success": true,
    "value": "1234",
    "from_base": 10,
    "decimal_equivalent": 1234,
    "results": {
        "2": {"value": "10011010010", "decimal": 1234},
        "8": {"value": "2322", "decimal": 1234},
        "16": {"value": "4D2", "decimal": 1234}
    }
}
```

### Distribución

**POST /api/distribution/fixed_point**
```json
Request:
{
    "E": 4,
    "F": 4,
    "representation": "unsigned"
}

Response:
{
    "success": true,
    "E": 4,
    "F": 4,
    "representation": "unsigned",
    "min_value": 0,
    "max_value": 15.9375,
    "epsilon": 0.0625,
    "total_bits": 8,
    "total_numbers": 256,
    "statistics": {...}
}
```

### Health

**GET /api/health**
```json
Response:
{
    "status": "ok",
    "version": "7.0.0",
    "message": "GeneratorFEExercises Web API - Fase 7"
}
```

## Desarrollo

### Dependencias para desarrollo

```bash
pip install flask-debugtoolbar
pip install pytest  # para testing
```

### Ejecutar en modo development

```bash
export FLASK_ENV=development
python app.py
```

### Agregar nuevas APIs

1. Crear función en `app.py`
2. Decorar con `@app.route(...)` 
3. Retornar JSON con estructura `{success: bool, ...}`

Ejemplo:
```python
@app.route('/api/custom', methods=['POST'])
def custom_endpoint():
    data = request.get_json()
    # ... procesar
    return jsonify({'success': True, 'result': ...})
```

## Próximas Mejoras

- [ ] Agregar Chart.js para gráficas interactivas
- [ ] Implementar visualización de pasos en conversiones
- [ ] Añadir temas (claro/oscuro)
- [ ] Exportar resultados a PDF
- [ ] Integración con base de datos para almacenar sesiones
- [ ] Más representaciones (BCD, Biquinarios, etc.)
- [ ] Mobile app (React Native)

## Testing

```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest tests/

# Con cobertura
pip install pytest-cov
pytest --cov=web tests/
```

## Troubleshooting

### Puerto 5000 en uso
```bash
# Cambiar puerto en app.py
app.run(port=5001)

# O eliminar proceso:
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Módulos core no encontrados
Asegurate que el proyecto está estructurado correctamente:
```
GeneratorFEExercises/
├── web/
│   └── app.py
├── core/
│   ├── ieee754.py
│   └── punto_fijo_unified.py
```

### CORS errors
El servidor Flask está configurado con `CORS(app)` por defecto. Si encuentras problemas:
```python
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
```

## Licencia

MIT - Ver LICENSE en el directorio raíz

## Contribución

¡Las contribuciones son bienvenidas! Abre un Issue o Pull Request.

---

**GeneratorFEExercises v7.0 | Web UI Phase**
