#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeneratorFEExercises - Web Server (Fase 7)
Interfaz Web Interactiva para simuladores de números

Simuladores Disponibles:
  1. IEEE754 Interactivo - Visualización bit a bit
  2. Calculadora de Bases - Conversiones paso a paso
  3. Visualizador de Distribución - Gráficas comparativas

Uso:
    python app.py
    # Accede a http://localhost:5000
"""

import os
import sys
from pathlib import Path

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Agregar core/ al path para importar módulos
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
WEB_DIR = Path(__file__).parent
sys.path.insert(0, str(WEB_DIR))

try:
    from core.ieee754 import IEEE754Gen
    from core.punto_fijo_unified import FixedPointUnified
except ImportError as e:
    print(f"Error importando módulos core: {e}")
    sys.exit(1)

# Importar servicios de Lenguajes Formales
try:
    # Importar desde el módulo web.models (archivo web/models.py)
    from importlib.util import spec_from_file_location, module_from_spec
    
    # Cargar models.py desde el directorio web
    models_path = WEB_DIR / 'models.py'
    spec = spec_from_file_location("formal_models", models_path)
    formal_models = module_from_spec(spec)
    spec.loader.exec_module(formal_models)
    
    Alphabet = formal_models.Alphabet
    Language = formal_models.Language
    LanguageOrder = formal_models.LanguageOrder
    
    # Cargar servicios
    services_alpha_path = WEB_DIR / 'services_alphabet.py'
    spec = spec_from_file_location("formal_services_alphabet", services_alpha_path)
    formal_services_alphabet = module_from_spec(spec)
    spec.loader.exec_module(formal_services_alphabet)
    AlphabetService = formal_services_alphabet.AlphabetService
    
    services_lang_path = WEB_DIR / 'services_language.py'
    spec = spec_from_file_location("formal_services_language", services_lang_path)
    formal_services_language = module_from_spec(spec)
    spec.loader.exec_module(formal_services_language)
    LanguageService = formal_services_language.LanguageService
    
    services_analysis_path = WEB_DIR / 'services_analysis.py'
    spec = spec_from_file_location("formal_services_analysis", services_analysis_path)
    formal_services_analysis = module_from_spec(spec)
    spec.loader.exec_module(formal_services_analysis)
    AnalysisService = formal_services_analysis.AnalysisService
    
except Exception as e:
    print(f"Error importando servicios de Lenguajes Formales: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# Configuración Flask
# ============================================================================

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Habilitar CORS
CORS(app)

# Configuración
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# ============================================================================
# Inicializar Servicios de Lenguajes Formales
# ============================================================================

# Crear instancias de servicios
alphabet_service = AlphabetService()
language_service = LanguageService(alphabet_service)
analysis_service = AnalysisService(language_service, alphabet_service)

# ============================================================================
# Rutas principales (HTML)
# ============================================================================

@app.route('/')
def index():
    """Página principal - Menú de simuladores"""
    return render_template('index.html')

@app.route('/ieee754')
def ieee754_simulator():
    """Simulador IEEE754 Interactivo"""
    return render_template('ieee754.html')

@app.route('/converter')
def converter():
    """Calculadora de Conversión de Bases"""
    return render_template('converter.html')

@app.route('/distribution')
def distribution_visualizer():
    """Visualizador de Distribución de Números"""
    return render_template('distribution.html')

@app.route('/bcd-biquinario')
def bcd_biquinario():
    """Convertidor BCD y Biquinario"""
    return render_template('bcd-biquinario.html')

# Rutas para Lenguajes Formales
@app.route('/alphabets')
def alphabets_manager():
    """Gestor de Alfabetos - Lenguajes Formales"""
    return render_template('alphabets.html')

@app.route('/languages')
def languages_generator():
    """Generador de Lenguajes Formales"""
    return render_template('languages.html')

@app.route('/language-analysis')
def language_analysis():
    """Análisis de Lenguajes Formales"""
    return render_template('language-analysis.html')

@app.route('/language-order')
def language_order():
    """Ordenamientos y Significados de Lenguajes"""
    return render_template('language-order.html')

# ============================================================================
# API: IEEE754
# ============================================================================

@app.route('/api/ieee754/encode', methods=['POST'])
def ieee754_encode():
    """Codificar número decimal a IEEE754"""
    try:
        data = request.get_json()
        value = float(data.get('value'))
        base = int(data.get('base', 2))
        E_bits = int(data.get('E_bits', 8))
        F_bits = int(data.get('F_bits', 23))
        
        ieee = IEEE754Gen(E_bits=E_bits, F_bits=F_bits, base=base)
        encoded = ieee.encode(value)
        
        # Extraer componentes del entero codificado
        total_bits = 1 + E_bits + F_bits
        bits_str = bin(encoded)[2:].zfill(total_bits)
        
        sign_bit = int(bits_str[0])
        exponent_bits = bits_str[1:1+E_bits]
        mantissa_bits = bits_str[1+E_bits:]
        
        E_encoded = int(exponent_bits, 2) if exponent_bits else 0
        M_encoded = int(mantissa_bits, 2) if mantissa_bits else 0
        
        # Decodificar para obtener el valor
        decoded = ieee.decode(sign_bit, E_encoded, M_encoded)
        
        return jsonify({
            'success': True,
            'value': value,
            'bits': bits_str,
            'hex': hex(encoded),
            'sign': str(sign_bit),
            'exponent': exponent_bits,
            'mantissa': mantissa_bits,
            'decoded': str(decoded) if not isinstance(decoded, (int, float)) else decoded,
            'valid': True
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ieee754/characteristics', methods=['POST'])
def ieee754_characteristics():
    """Obtener características de IEEE754"""
    try:
        data = request.get_json()
        base = int(data.get('base', 2))
        E_bits = int(data.get('E_bits', 8))
        F_bits = int(data.get('F_bits', 23))
        
        ieee = IEEE754Gen(base=base, E_bits=E_bits, F_bits=F_bits)
        
        return jsonify({
            'success': True,
            'base': base,
            'E_bits': E_bits,
            'F_bits': F_bits,
            'total_bits': 1 + E_bits + F_bits,
            'E_min': ieee.E_min,
            'E_max': ieee.E_max,
            'min_positive': float(ieee.min_positive),
            'max_positive': float(ieee.max_positive),
            'epsilon': float(ieee.epsilon_machine)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ieee754/special', methods=['POST'])
def ieee754_special():
    """Obtener números especiales (∞, NaN, etc)"""
    try:
        data = request.get_json()
        base = int(data.get('base', 2))
        E_bits = int(data.get('E_bits', 8))
        F_bits = int(data.get('F_bits', 23))
        
        total_bits = 1 + E_bits + F_bits
        E_all_ones = (1 << E_bits) - 1
        
        # Representaciones especiales
        zero_bits = 0
        neg_zero_bits = 1 << (total_bits - 1)
        inf_bits = (E_all_ones << F_bits)
        neg_inf_bits = (1 << (total_bits - 1)) | inf_bits
        qnan_bits = inf_bits | (1 << (F_bits - 1))
        snan_bits = neg_inf_bits | 1
        
        def to_bits(value):
            return bin(value)[2:].zfill(total_bits)
        
        return jsonify({
            'success': True,
            'base': base,
            'E_bits': E_bits,
            'F_bits': F_bits,
            'total_bits': total_bits,
            'positive_zero': to_bits(zero_bits),
            'negative_zero': to_bits(neg_zero_bits),
            'positive_infinity': to_bits(inf_bits),
            'negative_infinity': to_bits(neg_inf_bits),
            'qnan': to_bits(qnan_bits),
            'snan': to_bits(snan_bits)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================================
# API: Convertidor de Bases
# ============================================================================

@app.route('/api/convert', methods=['POST'])
def convert_bases():
    """Convertir número entre múltiples bases"""
    try:
        data = request.get_json()
        value = str(data.get('value')).strip()
        from_base = int(data.get('from_base', 10))
        to_bases = data.get('to_bases', [2, 8, 10, 16])
        
        # Convertir a decimal
        if from_base == 10:
            decimal_value = int(value)
        else:
            decimal_value = int(value, from_base)
        
        # Convertir a cada base solicitada
        results = {}
        for target_base in to_bases:
            if target_base == 10:
                result_value = str(decimal_value)
            elif target_base == 2:
                result_value = bin(decimal_value)[2:]
            elif target_base == 8:
                result_value = oct(decimal_value)[2:]
            elif target_base == 16:
                result_value = hex(decimal_value)[2:].upper()
            else:
                # Conversión genérica
                if decimal_value == 0:
                    result_value = '0'
                else:
                    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    result_value = ''
                    temp = decimal_value
                    while temp > 0:
                        result_value = digits[temp % target_base] + result_value
                        temp //= target_base
            
            results[str(target_base)] = {
                'value': result_value,
                'decimal': decimal_value
            }
        
        return jsonify({
            'success': True,
            'value': value,
            'from_base': from_base,
            'decimal_equivalent': decimal_value,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================================
# API: Distribución
# ============================================================================

@app.route('/api/distribution/fixed_point', methods=['POST'])
def distribution_fixed_point():
    """Analizar distribución de números en punto fijo"""
    try:
        data = request.get_json()
        E = int(data.get('E', 4))
        F = int(data.get('F', 4))
        representation = data.get('representation', 'unsigned')
        
        fp = FixedPointUnified(E=E, F=F, base=2, 
                              signed=(representation != 'unsigned'),
                              representation=representation if representation != 'unsigned' else None)
        
        total_bits = E + F
        total_numbers = 2 ** total_bits
        
        return jsonify({
            'success': True,
            'E': E,
            'F': F,
            'representation': representation,
            'min_value': float(fp.min_value),
            'max_value': float(fp.max_value),
            'epsilon': float(fp.epsilon),
            'total_bits': total_bits,
            'total_numbers': total_numbers,
            'statistics': {
                'range': [float(fp.min_value), float(fp.max_value)],
                'gap_min': float(fp.epsilon),
                'gap_max': float(fp.epsilon),
                'uniform': True
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/distribution/chart-data', methods=['POST'])
def distribution_chart_data():
    """Obtener datos para gráfica de distribución (Chart.js compatible)"""
    try:
        data = request.get_json()
        
        # Obtener tipo de número
        tipo_numero = data.get('tipo_numero', 'fixed_point')
        base = int(data.get('base', 2))
        
        # Validar base
        if base < 2 or base > 36:
            return jsonify({
                'success': False,
                'error': 'Base inválida. Debe estar entre 2 y 36.'
            }), 400
        
        if tipo_numero == 'fixed_point':
            # ===== PUNTO FIJO =====
            E = int(data.get('E', 4))
            F = int(data.get('F', 4))
            representation_str = data.get('representation', 'unsigned')
            
            # Mapear valores de representación de la UI a los parámetros de la clase
            if representation_str == 'unsigned':
                signed = False
                representation = None
            elif representation_str == 'signed_magnitude':
                signed = True
                representation = 'ms'
            elif representation_str == 'twos_complement':
                signed = True
                representation = 'complement'
            elif representation_str == 'ones_complement':
                # Complemento a uno se maneja como complemento a base
                signed = True
                representation = 'complement'
            else:
                return jsonify({
                    'success': False,
                    'error': f'Representación desconocida: {representation_str}'
                }), 400
            
            try:
                # FixedPointUnified siempre necesita un representation válido
                rep = representation if representation else 'complement'
                fp = FixedPointUnified(E=E, F=F, base=base, 
                                      signed=signed,
                                      representation=rep)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({
                    'success': False,
                    'error': f'Error creando FixedPointUnified: {str(e)} (E={E}, F={F}, base={base}, signed={signed}, representation={representation})'
                }), 400
            
            total_bits = E + F
            total_numbers = 2 ** total_bits
            
            # Generar datos de frecuencia para gráfica de distribución
            # Dividir rango en 50 bins para visualización
            min_val = float(fp.min_value)
            max_val = float(fp.max_value)
            epsilon = float(fp.epsilon)
            
            # Crear bins
            num_bins = min(50, total_numbers)
            if max_val > min_val:
                bin_width = (max_val - min_val) / num_bins
            else:
                bin_width = 1.0
            
            labels = []
            frequencies = []
            
            for i in range(num_bins):
                bin_start = min_val + (i * bin_width)
                bin_end = bin_start + bin_width
                bin_center = (bin_start + bin_end) / 2
                
                # Estimar frecuencia (uniforme en punto fijo)
                if max_val > min_val:
                    frequency = total_numbers / num_bins
                else:
                    frequency = total_numbers
                
                labels.append(f"{bin_center:.2f}")
                frequencies.append(frequency)
            
            return jsonify({
                'success': True,
                'chart_type': 'bar',
                'E': E,
                'F': F,
                'representation': representation_str,
                'base': base,
                'tipo_numero': 'fixed_point',
                'labels': labels,
                'datasets': [
                    {
                        'label': f'Distribución ({representation_str})',
                        'data': frequencies,
                        'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1,
                        'tension': 0.1
                    }
                ],
                'statistics': {
                    'min': min_val,
                    'max': max_val,
                    'epsilon': epsilon,
                    'total_numbers': total_numbers,
                    'total_bits': total_bits,
                    'uniform': True,
                    'gap_type': 'uniforme'
                }
            })
        
        elif tipo_numero == 'floating_point':
            # ===== PUNTO FLOTANTE IEEE754 =====
            try:
                from core.ieee754 import IEEE754Gen
            except ImportError:
                return jsonify({
                    'success': False,
                    'error': 'Módulo IEEE754Gen no disponible'
                }), 400
            
            E = int(data.get('E', 8))
            F = int(data.get('F', 23))
            
            # Validar parámetros E y F
            if E < 1 or F < 1:
                return jsonify({
                    'success': False,
                    'error': f'E y F deben ser >= 1. E={E}, F={F}'
                }), 400
            
            try:
                ieee = IEEE754Gen(E_bits=E, F_bits=F, base=base)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({
                    'success': False,
                    'error': f'Error creando IEEE754Gen: {str(e)} (E={E}, F={F}, base={base})'
                }), 400
            
            total_bits = 1 + E + F  # sign + exponent + mantissa
            
            # Para IEEE754, la distribución es no-uniforme (logarítmica en magnitud)
            # Generar valores representables
            representable_values = []
            
            # Generar valores positivos
            # El rango de exponente depende de la base y E bits
            exp_min = 1 - ieee.bias
            exp_max = ieee.bias - 1
            
            for exponent in range(exp_min, exp_max + 1):
                for mantissa in range(0, min(base**F, 100)):  # Limitar para rendimiento
                    try:
                        # Normalizado: 1.M × B^E
                        val = (1 + mantissa / (base**F)) * (base ** exponent)
                        representable_values.append(val)
                        representable_values.append(-val)
                    except (OverflowError, ValueError, ZeroDivisionError):
                        pass
            
            representable_values = sorted(set([v for v in representable_values if v != 0]))
            
            # Crear bins logarítmicos para valores positivos
            num_bins = 50
            if representable_values:
                min_val = min([v for v in representable_values if v > 0])
                max_val = max([v for v in representable_values if v > 0])
                
                # Escala logarítmica en base correspondiente
                import math
                if base == 10:
                    log_func = math.log10
                elif base == 2:
                    log_func = math.log2
                else:
                    # Para otras bases, usar cambio de base
                    log_func = lambda x: math.log(x) / math.log(base)
                
                try:
                    log_min = log_func(min_val) if min_val > 0 else -10
                    log_max = log_func(max_val) if max_val > 0 else 10
                except (ValueError, ZeroDivisionError):
                    log_min = -10
                    log_max = 10
                
                labels = []
                frequencies = []
                
                for i in range(num_bins):
                    log_start = log_min + (i / num_bins) * (log_max - log_min)
                    log_end = log_min + ((i + 1) / num_bins) * (log_max - log_min)
                    
                    # Convertir de log a valor lineal según la base
                    try:
                        bin_start = base ** log_start
                        bin_end = base ** log_end
                        bin_center = (bin_start + bin_end) / 2
                        
                        # Contar valores en este bin
                        count = len([v for v in representable_values 
                                   if bin_start <= v < bin_end])
                    except (OverflowError, ValueError):
                        bin_center = 0
                        count = 0
                    
                    labels.append(f"{bin_center:.2e}")
                    frequencies.append(count)
                
                return jsonify({
                    'success': True,
                    'chart_type': 'bar',
                    'E': E,
                    'F': F,
                    'base': base,
                    'tipo_numero': 'floating_point',
                    'labels': labels,
                    'datasets': [
                        {
                            'label': f'Distribución IEEE754 ({E},{F})',
                            'data': frequencies,
                            'backgroundColor': 'rgba(200, 100, 150, 0.6)',
                            'borderColor': 'rgba(200, 100, 150, 1)',
                            'borderWidth': 1,
                            'tension': 0.1
                        }
                    ],
                    'statistics': {
                        'min': min_val,
                        'max': max_val,
                        'epsilon': 2**(-F),
                        'total_numbers': total_bits,
                        'total_bits': total_bits,
                        'uniform': False,
                        'gap_type': 'logarítmica'
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No se pudieron generar valores IEEE754'
                }), 400
        
        else:
            return jsonify({
                'success': False,
                'error': f'Tipo de número desconocido: {tipo_numero}'
            }), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 400

# ============================================================================
# API: Representaciones Especiales - BCD y Biquinarios
# ============================================================================

@app.route('/api/representations/bcd', methods=['POST'])
def bcd_conversion():
    """Convertir número decimal a BCD (Binary Coded Decimal)"""
    try:
        data = request.get_json()
        number = int(data.get('number', 0))
        
        # Validar rango
        if number < 0 or number > 9999:
            return jsonify({
                'success': False,
                'error': 'BCD soporta números de 0 a 9999'
            }), 400
        
        # Convertir a BCD
        bcd_str = ''
        temp = number
        for _ in range(4):
            digit = temp % 10
            bcd_str = format(digit, '04b') + bcd_str
            temp //= 10
        
        bcd_str = bcd_str.lstrip('0') or '0000'
        
        # Generar visualización de nibbles
        nibbles = []
        for digit in str(number).zfill(4):
            nibbles.append({
                'digit': int(digit),
                'binary': format(int(digit), '04b'),
                'hex': format(int(digit), 'x')
            })
        
        return jsonify({
            'success': True,
            'number': number,
            'bcd_binary': bcd_str,
            'bcd_hex': hex(int(bcd_str, 2)),
            'bcd_decimal': int(bcd_str, 2),
            'nibbles': nibbles,
            'total_bits': len(bcd_str),
            'info': {
                'name': 'Binary Coded Decimal',
                'description': 'Cada dígito decimal se codifica en 4 bits',
                'range': '0-9999',
                'bits_per_digit': 4
            }
        })
    
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Número inválido'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/representations/biquinario', methods=['POST'])
def biquinario_conversion():
    """Convertir número decimal a Biquinario (7 bits)"""
    try:
        data = request.get_json()
        number = int(data.get('number', 0))
        
        # Validar rango (0-99)
        if number < 0 or number > 99:
            return jsonify({
                'success': False,
                'error': 'Biquinario soporta números de 0 a 99'
            }), 400
        
        # Sistema Biquinario: 7 bits (5, 4, 3, 2, 1, 0)
        # Primeros 2 bits: quinario (0-4), últimos 5 bits: binario (0-1)
        
        quinary = number // 5      # Primer dígito (0-4 cuando number < 99)
        binary_part = number % 5   # Segundo dígito (0-4)
        
        # Binario de 3 bits para cada parte
        quinary_bin = format(quinary, '02b')
        binary_bin = format(binary_part, '03b')
        
        biquia_full = quinary_bin + binary_bin
        
        return jsonify({
            'success': True,
            'number': number,
            'biquinario': biquia_full,
            'biquinario_hex': hex(int(biquia_full, 2)),
            'biquinario_decimal': int(biquia_full, 2),
            'components': {
                'quinario_part': {
                    'value': quinary,
                    'binary': quinary_bin,
                    'position': '5-4'
                },
                'binary_part': {
                    'value': binary_part,
                    'binary': binary_bin,
                    'position': '3-2-1'
                }
            },
            'total_bits': len(biquia_full),
            'info': {
                'name': 'Biquinario',
                'description': 'Sistema de 2 dígitos: uno quinario (base 5) y otro binario',
                'range': '0-99',
                'structure': '2 bits quinario + 3 bits binario'
            }
        })
    
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Número inválido'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/representations/compare', methods=['POST'])
def compare_representations():
    """Comparar múltiples representaciones de un número"""
    try:
        data = request.get_json()
        number = int(data.get('number', 0))
        
        representations = {}
        
        # Binario
        try:
            representations['binary'] = format(number, 'b')
        except:
            representations['binary'] = 'N/A'
        
        # Octal
        try:
            representations['octal'] = oct(number)[2:]
        except:
            representations['octal'] = 'N/A'
        
        # Hexadecimal
        try:
            representations['hexadecimal'] = hex(number)[2:]
        except:
            representations['hexadecimal'] = 'N/A'
        
        # BCD (si está en rango)
        if 0 <= number <= 9999:
            bcd_str = ''
            temp = number
            for _ in range(4):
                digit = temp % 10
                bcd_str = format(digit, '04b') + bcd_str
                temp //= 10
            representations['bcd'] = bcd_str.lstrip('0') or '0000'
        
        # Biquinario (si está en rango)
        if 0 <= number <= 99:
            quinary = number // 5
            binary_part = number % 5
            biq = format(quinary, '02b') + format(binary_part, '03b')
            representations['biquinario'] = biq
        
        return jsonify({
            'success': True,
            'decimal': number,
            'representations': representations,
            'comparison': {
                'total_representations': len(representations),
                'max_bits': max(len(str(v)) for v in representations.values() if v != 'N/A')
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================================
# API: Health Check
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar que el servidor está activo"""
    return jsonify({
        'status': 'ok',
        'version': '7.0.0',
        'message': 'GeneratorFEExercises Web API - Fase 7'
    })

# ============================================================================
# API: LENGUAJES FORMALES - Alfabetos (7 endpoints)
# ============================================================================

@app.route('/api/alphabets', methods=['GET'])
def get_alphabets():
    """GET /api/alphabets - Listar todos los alfabetos"""
    alphabets = alphabet_service.get_all()
    return jsonify({
        'success': True,
        'total': len(alphabets),
        'alphabets': [a.to_dict() for a in alphabets]
    })

@app.route('/api/alphabets', methods=['POST'])
def create_alphabet():
    """POST /api/alphabets - Crear un nuevo alfabeto"""
    try:
        data = request.get_json()
        name = data.get('name', '')
        symbols = data.get('symbols', [])
        initial_symbol = data.get('initial_symbol', '')
        
        success, message, alphabet = alphabet_service.create(
            name=name,
            symbols=symbols,
            initial_symbol=initial_symbol
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'alphabet': alphabet.to_dict()
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alphabets/<alphabet_id>', methods=['GET'])
def get_alphabet(alphabet_id):
    """GET /api/alphabets/{id} - Obtener un alfabeto específico"""
    alphabet = alphabet_service.get(alphabet_id)
    
    if not alphabet:
        return jsonify({
            'success': False,
            'message': 'Alfabeto no encontrado'
        }), 404
    
    return jsonify({
        'success': True,
        'alphabet': alphabet.to_dict()
    })

@app.route('/api/alphabets/<alphabet_id>', methods=['PUT'])
def update_alphabet(alphabet_id):
    """PUT /api/alphabets/{id} - Actualizar un alfabeto"""
    try:
        data = request.get_json()
        name = data.get('name')
        symbols = data.get('symbols')
        initial_symbol = data.get('initial_symbol')
        
        success, message = alphabet_service.update(
            alphabet_id,
            name=name,
            symbols=symbols,
            initial_symbol=initial_symbol
        )
        
        if success:
            alphabet = alphabet_service.get(alphabet_id)
            return jsonify({
                'success': True,
                'message': message,
                'alphabet': alphabet.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alphabets/<alphabet_id>', methods=['DELETE'])
def delete_alphabet(alphabet_id):
    """DELETE /api/alphabets/{id} - Eliminar un alfabeto"""
    success, message = alphabet_service.delete(alphabet_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        })
    else:
        return jsonify({
            'success': False,
            'message': message
        }), 400

@app.route('/api/alphabets/presets/list', methods=['GET'])
def get_preset_alphabets():
    """GET /api/alphabets/presets - Obtener alfabetos preestablecidos"""
    presets = alphabet_service.get_presets()
    return jsonify({
        'success': True,
        'total': len(presets),
        'presets': presets
    })

@app.route('/api/alphabets/<alphabet_id>/validate', methods=['POST'])
def validate_alphabet_endpoint(alphabet_id):
    """POST /api/alphabets/{id}/validate - Validar un alfabeto"""
    alphabet = alphabet_service.get(alphabet_id)
    
    if not alphabet:
        return jsonify({
            'success': False,
            'message': 'Alfabeto no encontrado'
        }), 404
    
    is_valid, message = alphabet.validate()
    return jsonify({
        'success': is_valid,
        'valid': is_valid,
        'message': message,
        'alphabet': alphabet.to_dict()
    })

# ============================================================================
# API: LENGUAJES FORMALES - Lenguajes (5 endpoints)
# ============================================================================

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """GET /api/languages - Listar todos los lenguajes"""
    languages = language_service.get_all()
    return jsonify({
        'success': True,
        'total': len(languages),
        'languages': [l.to_dict() for l in languages]
    })

@app.route('/api/languages', methods=['POST'])
def create_language():
    """POST /api/languages - Crear un nuevo lenguaje"""
    try:
        data = request.get_json()
        name = data.get('name', '')
        alphabet_id = data.get('alphabet_id', '')
        length = int(data.get('length', 1))
        words = set(data.get('words', []))
        conditions = data.get('conditions', '')
        
        success, message, language = language_service.create(
            name=name,
            alphabet_id=alphabet_id,
            length=length,
            words=words,
            conditions=conditions
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'language': language.to_dict()
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/languages/<language_id>/generate', methods=['POST'])
def generate_language_words(language_id):
    """POST /api/languages/{id}/generate - Generar palabras de un lenguaje"""
    try:
        data = request.get_json()
        condition = data.get('condition', 'all')  # 'all' o nombre de condición
        
        language = language_service.get(language_id)
        if not language:
            return jsonify({
                'success': False,
                'message': 'Lenguaje no encontrado'
            }), 404
        
        if condition == 'all':
            success, message, words = language_service.generate_all_words(
                language.alphabet_id,
                language.length
            )
        else:
            success, message, words = language_service.generate_custom(
                language.alphabet_id,
                language.length,
                condition
            )
        
        if success:
            language.words = words
            return jsonify({
                'success': True,
                'message': message,
                'cardinality': len(words),
                'language': language.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/languages/<language_id>', methods=['GET'])
def get_language(language_id):
    """GET /api/languages/{id} - Obtener un lenguaje específico"""
    language = language_service.get(language_id)
    
    if not language:
        return jsonify({
            'success': False,
            'message': 'Lenguaje no encontrado'
        }), 404
    
    success, stats = language_service.get_statistics(language_id)
    
    return jsonify({
        'success': True,
        'language': language.to_dict(),
        'statistics': stats if success else {}
    })

@app.route('/api/languages/<language_id>', methods=['DELETE'])
def delete_language(language_id):
    """DELETE /api/languages/{id} - Eliminar un lenguaje"""
    success, message = language_service.delete(language_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        })
    else:
        return jsonify({
            'success': False,
            'message': message
        }), 400

# ============================================================================
# API: LENGUAJES FORMALES - Análisis (3 endpoints)
# ============================================================================

@app.route('/api/analysis/orders', methods=['GET'])
def get_orders():
    """GET /api/analysis/orders - Listar todos los ordenamientos"""
    orders = analysis_service.get_all_orders()
    return jsonify({
        'success': True,
        'total': len(orders),
        'orders': [o.to_dict() for o in orders]
    })

@app.route('/api/analysis/languages/<language_id>/analyze', methods=['GET'])
def analyze_language(language_id):
    """GET /api/analysis/languages/{id}/analyze - Analizar un lenguaje"""
    language = language_service.get(language_id)
    
    if not language:
        return jsonify({
            'success': False,
            'message': 'Lenguaje no encontrado'
        }), 404
    
    coverage = analysis_service.analyze_coverage(language_id)
    distribution = analysis_service.analyze_symbol_distribution(language_id)
    patterns = analysis_service.analyze_pattern_frequency(language_id, pattern_length=2)
    
    return jsonify({
        'success': True,
        'language_id': language_id,
        'coverage': coverage,
        'symbol_distribution': distribution,
        'pattern_frequency': patterns
    })

@app.route('/api/analysis/statistics', methods=['GET'])
def get_global_statistics():
    """GET /api/analysis/statistics - Obtener estadísticas globales"""
    stats = analysis_service.get_global_statistics()
    alphabet_stats = alphabet_service.get_statistics()
    language_stats = language_service.get_statistics_global()
    
    return jsonify({
        'success': True,
        'alphabets': alphabet_stats,
        'languages': language_stats,
        'orders': stats
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Manejar rutas no encontradas"""
    return jsonify({
        'success': False,
        'error': 'Ruta no encontrada',
        'status': 404
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Manejar errores del servidor"""
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor',
        'status': 500
    }), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("""
===================================================================
 GeneratorFEExercises - Web UI (Fase 7 + Lenguajes Formales)
===================================================================

  Iniciando servidor en http://localhost:5000

  Simuladores Disponibles:
    * IEEE754 Interactivo:    http://localhost:5000/ieee754
    * Calculadora de Bases:   http://localhost:5000/converter
    * Distribucion Numeros:   http://localhost:5000/distribution
    * BCD/Biquinario:         http://localhost:5000/bcd-biquinario

  API Endpoints (Lenguajes Formales):
    GET    /api/alphabets                    - List alphabets
    POST   /api/alphabets                    - Create alphabet
    GET    /api/languages                    - List languages
    POST   /api/languages                    - Create language
    POST   /api/languages/{id}/generate      - Generate words
    GET    /api/analysis/orders              - List orderings
    GET    /api/analysis/statistics          - Global stats

  Presiona CTRL+C para detener
===================================================================
    """)
    
    app.run(debug=True, host='localhost', port=5000)
