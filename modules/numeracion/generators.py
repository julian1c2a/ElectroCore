import random
from typing import Dict, Any
from core.generator_base import ExerciseGenerator, ExerciseRandomizer
from core.numeracion_utils import decimal_a_binario_con_pasos
from modules.numeracion.models import ConversionExerciseData, ConversionRow, ArithmeticOp

class ConversionRowRandomizer(ExerciseRandomizer):
    """ALEATORIZADOR: Genera parámetros del problema para ConversionRow."""
    
    def topic(self) -> str:
        return "Representación Numérica"
    
    def randomize(self, seed: int | None = None) -> Dict[str, Any]:
        """
        Genera parámetros del PROBLEMA de forma aleatoria.
        
        Returns:
            Dict con los parámetros del problema, listo para pasar al generador.
        """
        if seed is not None:
            random.seed(seed)
        
        n_bits = 8
        col_idx = random.choice([1, 1, 2, 3, 3, 4, 4, 5])
        val = 0
        text_val = ""
        
        es_signed = col_idx in [1, 3, 4]
        sign = -1 if (es_signed and random.random() < 0.7) else 1
        
        if col_idx == 1:  # Decimal
            val = sign * random.randint(0, 120)
            text_val = str(val)
        elif col_idx == 2:  # Binario Natural
            val = random.randint(0, 255)
            text_val = self._int_to_bin(val, n_bits)
        elif col_idx == 3:  # C2
            val = sign * random.randint(0, 127)
            text_val = self._int_to_bin(val, n_bits)
        elif col_idx == 4:  # SM
            val = sign * random.randint(0, 127)
            text_val = self._int_to_sm(val, n_bits)
        elif col_idx == 5:  # BCD
            val = random.randint(0, 99)
            text_val = self._int_to_bcd(val)
        
        # Retornar SOLO los parámetros del problema
        return {
            'label': random.choice(['a', 'b', 'c', 'd']),
            'val_decimal': val,
            'target_col_idx': col_idx,
            'representable': text_val != "NR"
        }
    
    def _int_to_bin(self, val: int, bits: int) -> str:
        return format(val if val >= 0 else (1 << bits) + val, f'0{bits}b')
    
    def _int_to_bcd(self, val: int) -> str:
        if not (0 <= val <= 99): return "NR"
        return f"{val // 10:04b} {val % 10:04b}"
    
    def _int_to_sm(self, val: int, bits: int) -> str:
        if val >= 0: return format(val, f'0{bits}b')
        return '1' + format(abs(val), f'0{bits - 1}b')


class ConversionExerciseGenerator(ExerciseGenerator):
    """GENERADOR: Calcula solución para ConversionRow."""
    
    def topic(self) -> str:
        return "Representación Numérica"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> ConversionRow:
        """
        DETERMINISTA: Recibe parámetros del problema y calcula solución.
        
        Args:
            problem_dict: {
                'label': 'a',
                'val_decimal': 157,
                'target_col_idx': 0,
                'representable': True
            }
        
        Returns:
            ConversionRow: Ejercicio completo (problema + solución).
        """
        label = problem_dict['label']
        val_decimal = problem_dict['val_decimal']
        target_col_idx = problem_dict['target_col_idx']
        representable = problem_dict['representable']
        
        n_bits = 8
        
        # CALCULAR SOLUCIÓN (determinista, basada en val_decimal)
        sol_bin = self._int_to_bin(val_decimal, n_bits) if 0 <= val_decimal <= 255 else "NR"
        sol_c2 = self._int_to_bin(val_decimal, n_bits) if -128 <= val_decimal <= 127 else "NR"
        sol_sm = self._int_to_sm(val_decimal, n_bits) if -127 <= val_decimal <= 127 else "NR"
        sol_bcd = self._int_to_bcd(val_decimal)
        
        # Determinar target_val_str según target_col_idx
        if target_col_idx == 1:  # Decimal
            target_val_str = str(val_decimal)
        elif target_col_idx == 2:  # Binario Natural
            target_val_str = sol_bin
        elif target_col_idx == 3:  # C2
            target_val_str = sol_c2
        elif target_col_idx == 4:  # SM
            target_val_str = sol_sm
        elif target_col_idx == 5:  # BCD
            target_val_str = sol_bcd
        else:
            target_val_str = "ERROR"
        
        return ConversionRow(
            title="Conversión entre Bases Numéricas",
            description=f"Convertir {val_decimal} a múltiples sistemas",
            label=label,
            val_decimal=val_decimal,
            target_col_idx=target_col_idx,
            representable=representable,
            target_val_str=target_val_str,
            sol_bin=sol_bin,
            sol_c2=sol_c2,
            sol_sm=sol_sm,
            sol_bcd=sol_bcd
        )
    
    def _int_to_bin(self, val: int, bits: int) -> str:
        return format(val if val >= 0 else (1 << bits) + val, f'0{bits}b')
    
    def _int_to_bcd(self, val: int) -> str:
        if not (0 <= val <= 99): return "NR"
        return f"{val // 10:04b} {val % 10:04b}"
    
    def _int_to_sm(self, val: int, bits: int) -> str:
        if val >= 0: return format(val, f'0{bits}b')
        return '1' + format(abs(val), f'0{bits - 1}b')


class BinaryConversionGenerator(ExerciseGenerator):
    """GENERADOR LEGACY: Compatible hacia atrás."""
    def topic(self) -> str:
        return "Representación Numérica"

    def _int_to_bin(self, val: int, bits: int) -> str:
        return format(val if val >= 0 else (1 << bits) + val, f'0{bits}b')

    def _int_to_bcd(self, val: int) -> str:
        if not (0 <= val <= 99): return "NR"
        return f"{val // 10:04b} {val % 10:04b}"

    def _int_to_sm(self, val: int, bits: int) -> str:
        if val >= 0: return format(val, f'0{bits}b')
        return '1' + format(abs(val), f'0{bits - 1}b')

    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> ConversionExerciseData:
        """
        NOTA: Este método no se usa en BinaryConversionGenerator (opera a nivel de ejercicio completo).
        """
        raise NotImplementedError("BinaryConversionGenerator opera a nivel de ejercicio completo")

    def generate(self, difficulty: int = 1) -> ConversionExerciseData:
        """
        MÉTODO LEGACY: Genera ejercicio completo con tabla de conversión.
        Utiliza aleatorizador internamente para mantener compatibilidad.
        """
        n_bits = 8
        rows = []
        labels = ['a', 'b', 'c', 'd']
        saved_vals = {}
        
        randomizer = ConversionRowRandomizer()

        for label in labels:
            # Usar aleatorizador
            problem = randomizer.randomize(seed=None)
            
            # Usar generador
            generator = ConversionExerciseGenerator()
            row = generator.generate_from_problem(problem)
            
            rows.append(row)
            saved_vals[label] = problem['val_decimal']

        ops = []
        if len(saved_vals) >= 2:
            for _ in range(2):
                l1 = random.choice(labels)
                l2 = random.choice([l for l in labels if l != l1])
                v1 = saved_vals[l1]
                v2 = saved_vals[l2]
                
                is_sum = random.choice([True, False])
                res = v1 + v2 if is_sum else v1 - v2
                
                ops.append(ArithmeticOp(
                    title="Operación Aritmética",
                    description=f"Realizar {'suma' if is_sum else 'resta'} en {random.choice(['binario', 'complemento a 2'])}",
                    op_type="suma" if is_sum else "resta",
                    system=random.choice(['binario', 'c2']),
                    operand1=l1,
                    operand2=l2,
                    operator_symbol="+" if is_sum else "-",
                    val1_dec=v1,
                    val2_dec=v2,
                    result_dec=res,
                    result_bin=self._int_to_bin(res, n_bits),
                    overflow=False,
                    underflow=False,
                    carry_bits=""
                ))

        return ConversionExerciseData(
            title="Sistemas de Representación",
            description=f"Complete la tabla. Registro de {n_bits} bits.",
            n_bits=n_bits,
            rows=rows,
            operations=ops
        )

# ============================================================================
# NUEVOS GENERADORES: Numeración Extendida
# ============================================================================


class MultiBaseExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios con múltiples bases (binario, octal, hexadecimal).
    Enfocado en operaciones en diferentes bases.
    """
    
    def topic(self) -> str:
        return "Sistemas Binarios, Octales y Hexadecimales"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de operaciones en múltiples bases."""
        base = problem_dict.get('target_base', random.choice([2, 8, 16]))
        operand1 = problem_dict.get('operand1', random.randint(10, 255))
        operand2 = problem_dict.get('operand2', random.randint(10, 255))
        operation = problem_dict.get('operation', random.choice(['add', 'subtract', 'multiply']))
        
        # Convertir a la base objetivo
        if base == 2:
            op1_str = bin(operand1)[2:]
            op2_str = bin(operand2)[2:]
            base_name = "Binario"
        elif base == 8:
            op1_str = oct(operand1)[2:]
            op2_str = oct(operand2)[2:]
            base_name = "Octal"
        else:  # base == 16
            op1_str = hex(operand1)[2:].upper()
            op2_str = hex(operand2)[2:].upper()
            base_name = "Hexadecimal"
        
        # Calcular resultado
        if operation == 'add':
            result = operand1 + operand2
            op_symbol = '+'
            op_name = 'suma'
        elif operation == 'subtract':
            result = max(0, operand1 - operand2)  # Evitar negativos para simplificar
            op_symbol = '-'
            op_name = 'resta'
        else:  # multiply
            result = operand1 * operand2
            op_symbol = '*'
            op_name = 'multiplicación'
        
        # Convertir resultado
        if base == 2:
            result_str = bin(result)[2:]
        elif base == 8:
            result_str = oct(result)[2:]
        else:
            result_str = hex(result)[2:].upper()
        
        return {
            'title': f'Operación en {base_name}',
            'description': f'Realiza la {op_name} en {base_name}: {op1_str} {op_symbol} {op2_str}',
            'problem': f'{op1_str} {op_symbol} {op2_str} = ?',
            'solution': result_str,
            'base': base,
            'base_name': base_name,
            'decimal_operands': (operand1, operand2),
            'decimal_result': result
        }


class FixedLengthExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre representación en longitud fija.
    Rango representable, overflow, underflow.
    """
    
    def topic(self) -> str:
        return "Representación en Longitud Fija"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de longitud fija."""
        n_bits = problem_dict.get('n_bits', 8)
        is_signed = problem_dict.get('is_signed', random.choice([True, False]))
        exercise_type = problem_dict.get('exercise_type', random.choice(['range', 'representability', 'conversion']))
        
        if is_signed:
            min_val = -(2 ** (n_bits - 1))
            max_val = 2 ** (n_bits - 1) - 1
            sign_info = "complemento a 2"
        else:
            min_val = 0
            max_val = 2 ** n_bits - 1
            sign_info = "sin signo"
        
        if exercise_type == 'range':
            problem_text = f"¿Cuál es el rango de números que se pueden representar con {n_bits} bits en {sign_info}?"
            solution = f"De {min_val} a {max_val}"
        
        elif exercise_type == 'representability':
            test_value = problem_dict.get('test_value', random.randint(min_val - 10, max_val + 10))
            can_represent = min_val <= test_value <= max_val
            problem_text = f"¿Se puede representar el número {test_value} con {n_bits} bits en {sign_info}?"
            solution = "Sí" if can_represent else "No"
            if not can_represent:
                if test_value > max_val:
                    solution += f" (exceede máximo: {max_val})"
                else:
                    solution += f" (menor que mínimo: {min_val})"
        
        else:  # conversion
            value = problem_dict.get('value', random.randint(min_val, max_val))
            if is_signed and value < 0:
                # Complemento a 2
                binary = format((1 << n_bits) + value, f'0{n_bits}b')
            else:
                binary = format(value, f'0{n_bits}b')
            problem_text = f"Convierte {value} a binario con {n_bits} bits ({sign_info})"
            solution = binary
        
        return {
            'title': 'Representación en Longitud Fija',
            'problem': problem_text,
            'solution': solution,
            'n_bits': n_bits,
            'is_signed': is_signed,
            'exercise_type': exercise_type,
            'range': (min_val, max_val)
        }


class SignedIntegerExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre números enteros con signo.
    Magnitud y signo, complemento a uno, complemento a dos.
    """
    
    def topic(self) -> str:
        return "Números Enteros con Signo"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de números con signo."""
        n_bits = problem_dict.get('n_bits', 8)
        representation = problem_dict.get('representation', random.choice(['SM', 'C1', 'C2']))
        exercise_type = problem_dict.get('exercise_type', random.choice(['decimal_to_rep', 'rep_to_decimal']))
        
        if exercise_type == 'decimal_to_rep':
            value = problem_dict.get('value', random.randint(-(2**(n_bits-1)-1), 2**(n_bits-1)-1))
            
            if representation == 'SM':  # Sign-Magnitude
                if value >= 0:
                    binary = format(value, f'0{n_bits}b')
                else:
                    binary = '1' + format(abs(value), f'0{n_bits-1}b')
                rep_name = "Magnitud y Signo"
            
            elif representation == 'C1':  # One's complement
                if value >= 0:
                    binary = format(value, f'0{n_bits}b')
                else:
                    binary = format((1 << n_bits) + value - 1, f'0{n_bits}b')
                rep_name = "Complemento a Uno"
            
            else:  # C2 - Two's complement
                if value >= 0:
                    binary = format(value, f'0{n_bits}b')
                else:
                    binary = format((1 << n_bits) + value, f'0{n_bits}b')
                rep_name = "Complemento a Dos"
            
            problem_text = f"Convierte {value} a {rep_name} con {n_bits} bits"
            solution = binary
        
        else:  # rep_to_decimal
            binary = problem_dict.get('binary', format(random.randint(0, 2**n_bits - 1), f'0{n_bits}b'))
            
            if representation == 'SM':
                if binary[0] == '0':
                    value = int(binary, 2)
                else:
                    value = -int(binary[1:], 2)
                rep_name = "Magnitud y Signo"
            
            elif representation == 'C1':
                if binary[0] == '0':
                    value = int(binary, 2)
                else:
                    value = -(((1 << n_bits) - 1) - int(binary, 2))
                rep_name = "Complemento a Uno"
            
            else:  # C2
                if binary[0] == '0':
                    value = int(binary, 2)
                else:
                    value = int(binary, 2) - (1 << n_bits)
                rep_name = "Complemento a Dos"
            
            problem_text = f"¿Qué valor decimal representa {binary} en {rep_name}?"
            solution = str(value)
        
        return {
            'title': 'Números Enteros con Signo',
            'problem': problem_text,
            'solution': solution,
            'n_bits': n_bits,
            'representation': representation,
            'exercise_type': exercise_type
        }


class ArithmeticOperationsExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Operaciones aritméticas en diferentes bases y representaciones.
    """
    
    def topic(self) -> str:
        return "Operaciones Aritméticas"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de operaciones aritméticas."""
        base = problem_dict.get('base', random.choice([2, 8, 10, 16]))
        operation = problem_dict.get('operation', random.choice(['add', 'subtract', 'multiply']))
        operand1 = problem_dict.get('operand1', random.randint(5, 100))
        operand2 = problem_dict.get('operand2', random.randint(5, 100))
        
        # Nombres de bases
        base_names = {2: 'binario', 8: 'octal', 10: 'decimal', 16: 'hexadecimal'}
        base_name = base_names[base]
        
        # Convertir operandos a la base
        if base == 2:
            op1_str = bin(operand1)[2:]
            op2_str = bin(operand2)[2:]
        elif base == 8:
            op1_str = oct(operand1)[2:]
            op2_str = oct(operand2)[2:]
        elif base == 16:
            op1_str = hex(operand1)[2:].upper()
            op2_str = hex(operand2)[2:].upper()
        else:
            op1_str = str(operand1)
            op2_str = str(operand2)
        
        # Calcular resultado
        if operation == 'add':
            result = operand1 + operand2
            op_symbol = '+'
            op_word = 'suma'
        elif operation == 'subtract':
            result = max(0, operand1 - operand2)
            op_symbol = '-'
            op_word = 'resta'
        else:
            result = operand1 * operand2
            op_symbol = '*'
            op_word = 'multiplicación'
        
        # Convertir resultado a la base
        if base == 2:
            result_str = bin(result)[2:]
        elif base == 8:
            result_str = oct(result)[2:]
        elif base == 16:
            result_str = hex(result)[2:].upper()
        else:
            result_str = str(result)
        
        return {
            'title': f'{op_word.capitalize()} en {base_name.capitalize()}',
            'problem': f'{op1_str} {op_symbol} {op2_str} = ?',
            'solution': result_str,
            'show_steps': True,
            'decimal_operands': (operand1, operand2),
            'decimal_result': result,
            'base': base,
            'operation': operation
        }


class FixedPointExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Números con parte fraccionaria (punto fijo).
    Conversiones y operaciones con punto fijo.
    """
    
    def topic(self) -> str:
        return "Números con Punto Fijo"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de punto fijo."""
        integer_bits = problem_dict.get('integer_bits', 4)
        fractional_bits = problem_dict.get('fractional_bits', 4)
        exercise_type = problem_dict.get('exercise_type', random.choice(['decimal_to_fixed', 'fixed_to_decimal', 'precision']))
        
        if exercise_type == 'decimal_to_fixed':
            # Generar número decimal con fracción
            integer_part = random.randint(0, 2**integer_bits - 1)
            fractional_part = random.randint(0, 2**fractional_bits - 1)
            decimal_value = integer_part + fractional_part / (2**fractional_bits)
            
            # Convertir a representación binaria fija
            fixed_int = format(integer_part, f'0{integer_bits}b')
            fixed_frac = format(fractional_part, f'0{fractional_bits}b')
            fixed_binary = f"{fixed_int}.{fixed_frac}"
            
            problem_text = f"Convierte {decimal_value:.4f} a punto fijo con {integer_bits} bits enteros y {fractional_bits} bits fraccionarios"
            solution = fixed_binary
        
        elif exercise_type == 'fixed_to_decimal':
            # Generar número en punto fijo
            fixed_int = format(random.randint(0, 2**integer_bits - 1), f'0{integer_bits}b')
            fixed_frac = format(random.randint(0, 2**fractional_bits - 1), f'0{fractional_bits}b')
            fixed_binary = f"{fixed_int}.{fixed_frac}"
            
            # Convertir a decimal
            integer_part = int(fixed_int, 2)
            fractional_part = int(fixed_frac, 2)
            decimal_value = integer_part + fractional_part / (2**fractional_bits)
            
            problem_text = f"¿Qué valor decimal representa {fixed_binary} en punto fijo (Q{integer_bits}.{fractional_bits})?"
            solution = f"{decimal_value:.4f}"
        
        else:  # precision
            max_precision = 2**(-fractional_bits)
            problem_text = f"¿Cuál es la precisión de representación en Q{integer_bits}.{fractional_bits}?"
            solution = f"2^(-{fractional_bits}) = {max_precision}"
        
        return {
            'title': 'Números en Punto Fijo',
            'problem': problem_text,
            'solution': solution,
            'integer_bits': integer_bits,
            'fractional_bits': fractional_bits,
            'exercise_type': exercise_type
        }


class FloatingPointExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Números en punto flotante (IEEE 754).
    Representación, normalización, denormalización, redondeo.
    """
    
    def topic(self) -> str:
        return "Números en Punto Flotante (IEEE 754)"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de punto flotante."""
        precision = problem_dict.get('precision', random.choice(['single', 'double']))  # 32-bit o 64-bit
        exercise_type = problem_dict.get('exercise_type', random.choice(['components', 'normalization', 'special_values']))
        
        if precision == 'single':
            sign_bits = 1
            exponent_bits = 8
            mantissa_bits = 23
            bias = 127
            precision_name = "Precisión Simple (32-bit)"
        else:
            sign_bits = 1
            exponent_bits = 11
            mantissa_bits = 52
            bias = 1023
            precision_name = "Precisión Doble (64-bit)"
        
        if exercise_type == 'components':
            # Generar un número flotante en binario
            sign_bit = random.randint(0, 1)
            exponent = format(random.randint(1, 2**exponent_bits - 2), f'0{exponent_bits}b')
            mantissa = format(random.randint(0, 2**mantissa_bits - 1), f'0{mantissa_bits}b')
            
            floating_point = f"{sign_bit} {exponent} {mantissa}"
            problem_text = f"Identifica los componentes de {floating_point} en {precision_name}"
            solution = f"Signo: {sign_bit} ('-' si 1), Exponente: {exponent} (bias={bias}), Mantisa: {mantissa}"
        
        elif exercise_type == 'normalization':
            # Generar un número que necesita normalización
            mantissa = random.randint(0, 2**mantissa_bits - 1)
            exponent = random.randint(1, bias + 50)
            
            problem_text = f"Normaliza el número con exponente {exponent} y mantisa {mantissa} en {precision_name}"
            solution = f"Exponente ajustado y mantisa reajustada según regla de normalización"
        
        else:  # special_values
            special_type = random.choice(['zero', 'infinity', 'denormalized', 'nan'])
            
            if special_type == 'zero':
                problem_text = f"¿Cómo se representa cero en IEEE 754 ({precision_name})?"
                solution = f"Exponente: {'0'*exponent_bits}, Mantisa: {'0'*mantissa_bits}"
            elif special_type == 'infinity':
                problem_text = f"¿Cómo se representa infinito en IEEE 754 ({precision_name})?"
                solution = f"Exponente: {'1'*exponent_bits}, Mantisa: {'0'*mantissa_bits}"
            elif special_type == 'denormalized':
                problem_text = f"¿Cuál es el número desnormalizado más pequeño en IEEE 754 ({precision_name})?"
                solution = f"2^(-{bias}) × 2^(-{mantissa_bits}) = 2^(-{bias + mantissa_bits})"
            else:  # NaN
                problem_text = f"¿Cómo se representa NaN en IEEE 754 ({precision_name})?"
                solution = f"Exponente: {'1'*exponent_bits}, Mantisa: cualquier valor != 0"
        
        return {
            'title': 'Números en Punto Flotante',
            'problem': problem_text,
            'solution': solution,
            'precision': precision,
            'exercise_type': exercise_type,
            'sign_bits': sign_bits,
            'exponent_bits': exponent_bits,
            'mantissa_bits': mantissa_bits,
            'bias': bias
        }