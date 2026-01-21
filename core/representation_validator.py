"""
RepresentationValidator: Validador universal para todas las representaciones numéricas.

Valida:
- Punto Fijo (todas las variantes)
- IEEE754 (normalizado, denormalizado, infinito, NaN)
- Biquinarios (7, 5, 6 bits)

Proporciona:
- Reporte de validez
- Recomendaciones de uso
- Análisis de errores

Ejemplo:
    >>> from core.punto_fijo_unified import FixedPointUnified
    >>> from core.representation_validator import RepresentationValidator
    >>> 
    >>> fp = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')
    >>> validator = RepresentationValidator()
    >>> report = validator.validate_fixed_point(fp)
    >>> print(report.summary())
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ValidationLevel(Enum):
    """Niveles de validación."""
    PASS = "✅ VÁLIDO"
    WARNING = "⚠️  ADVERTENCIA"
    ERROR = "❌ ERROR"


@dataclass
class ValidationReport:
    """Reporte de validación."""
    representation_type: str
    is_valid: bool
    checks_passed: int = 0
    checks_failed: int = 0
    checks_total: int = 0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_issue(self, level: ValidationLevel, message: str) -> None:
        """Agrega un problema al reporte."""
        self.issues.append(f"{level.value}: {message}")
        if level == ValidationLevel.ERROR:
            self.checks_failed += 1
            self.is_valid = False
        self.checks_total += 1
    
    def add_recommendation(self, message: str) -> None:
        """Agrega una recomendación."""
        self.recommendations.append(f"💡 {message}")
    
    def summary(self) -> str:
        """Retorna resumen del reporte."""
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"VALIDACIÓN: {self.representation_type}")
        lines.append(f"{'='*70}")
        lines.append(f"Estado: {'✅ VÁLIDO' if self.is_valid else '❌ INVÁLIDO'}")
        lines.append(f"Chequeos: {self.checks_passed}/{self.checks_total} pasados")
        
        if self.issues:
            lines.append("\nProblemas:")
            for issue in self.issues:
                lines.append(f"  {issue}")
        
        if self.recommendations:
            lines.append("\nRecomendaciones:")
            for rec in self.recommendations:
                lines.append(f"  {rec}")
        
        if self.metadata:
            lines.append("\nMetadatos:")
            for key, value in self.metadata.items():
                lines.append(f"  {key}: {value}")
        
        lines.append(f"{'='*70}\n")
        return "\n".join(lines)


class RepresentationValidator:
    """Validador universal de representaciones numéricas."""
    
    def validate_fixed_point(self, fp) -> ValidationReport:
        """
        Valida punto fijo unificado.
        
        Args:
            fp: FixedPointUnified
            
        Returns:
            ValidationReport
        """
        report = ValidationReport(
            representation_type=f"FixedPoint Q({fp.E},{fp.F}) base {fp.base}",
            is_valid=True
        )
        
        # Chequeo 1: Parámetros válidos
        try:
            if fp.E <= 0:
                report.add_issue(ValidationLevel.ERROR, "E (bits enteros) debe ser > 0")
            else:
                report.checks_passed += 1
            
            if fp.F < 0:
                report.add_issue(ValidationLevel.ERROR, "F (bits fraccionarios) debe ser >= 0")
            else:
                report.checks_passed += 1
            
            if fp.base < 2:
                report.add_issue(ValidationLevel.ERROR, "Base debe ser >= 2")
            else:
                report.checks_passed += 1
            
            report.checks_total = 3
        except Exception as e:
            report.add_issue(ValidationLevel.ERROR, f"Error en parámetros: {e}")
        
        # Chequeo 2: Consistencia de rango
        if fp.signed:
            if fp.representation == 'ms':
                # M&S: rango debe ser simétrico (excepto por cero duplicado)
                abs_min = abs(fp.min_value)
                abs_max = abs(fp.max_value)
                if abs(abs_min - abs_max) > fp.epsilon * 2:
                    report.add_issue(
                        ValidationLevel.WARNING,
                        f"Magnitud-Signo: rango no perfectamente simétrico (|min|={abs_min}, |max|={abs_max})"
                    )
                else:
                    report.checks_passed += 1
            else:  # complemento
                # Complemento: rango debe ser [-B^E, B^E - ε]
                expected_min = -fp.base_power_E
                if abs(fp.min_value - expected_min) < fp.epsilon:
                    report.checks_passed += 1
                else:
                    report.add_issue(
                        ValidationLevel.WARNING,
                        f"Complemento: mínimo esperado {expected_min}, obtenido {fp.min_value}"
                    )
            report.checks_total += 1
        
        # Chequeo 3: Epsilon válido
        expected_epsilon = fp.base ** (-fp.F)
        if abs(fp.epsilon - expected_epsilon) < 1e-10:
            report.checks_passed += 1
        else:
            report.add_issue(
                ValidationLevel.ERROR,
                f"Epsilon inválido: esperado {expected_epsilon}, obtenido {fp.epsilon}"
            )
        report.checks_total += 1
        
        # Chequeo 4: Total bits consistente
        if fp.signed:
            expected_bits = fp.E + fp.F + 1
        else:
            expected_bits = fp.E + fp.F
        
        if fp.total_bits == expected_bits:
            report.checks_passed += 1
        else:
            report.add_issue(
                ValidationLevel.ERROR,
                f"Total bits inconsistente: esperado {expected_bits}, obtenido {fp.total_bits}"
            )
        report.checks_total += 1
        
        # Recomendaciones
        if fp.signed and fp.representation == 'ms':
            report.add_recommendation(
                "Magnitud-Signo tiene dos representaciones de cero. "
                "Considera usar Complemento a Base para mejor eficiencia."
            )
        
        if fp.base != 2 and fp.F == 0:
            report.add_recommendation(
                f"Base {fp.base} sin fraccionarios: considera usar base 10 o 16 "
                "para mejor legibilidad en entrada/salida."
            )
        
        if fp.total_bits > 64:
            report.add_recommendation(
                f"Total de {fp.total_bits} bits. Considera reducir E o F "
                "para facilitar implementación en hardware."
            )
        
        # Metadata
        report.metadata = {
            'min_value': fp.min_value,
            'max_value': fp.max_value,
            'epsilon': fp.epsilon,
            'range_span': fp.max_value - fp.min_value,
        }
        
        return report
    
    def validate_ieee754(self, ieee754) -> ValidationReport:
        """
        Valida IEEE754.
        
        Args:
            ieee754: IEEE754Gen
            
        Returns:
            ValidationReport
        """
        report = ValidationReport(
            representation_type=f"IEEE754 base {ieee754.base} ({ieee754.E_bits} exp, {ieee754.F_bits} frac)",
            is_valid=True
        )
        
        # Chequeo 1: Parámetros válidos
        if ieee754.E_bits > 0 and ieee754.F_bits >= 0 and ieee754.base >= 2:
            report.checks_passed += 1
        else:
            report.add_issue(ValidationLevel.ERROR, "Parámetros IEEE754 inválidos")
        report.checks_total += 1
        
        # Chequeo 2: Casos especiales implementados
        try:
            # Normalizado
            s, e, m = ieee754.encode_normalized(1.5)
            report.checks_passed += 1
            
            # Infinito
            s, e, m = ieee754.encode_infinity()
            report.checks_passed += 1
            
            # NaN
            s, e, m = ieee754.encode_nan()
            report.checks_passed += 1
            
            report.checks_total += 3
        except Exception as e:
            report.add_issue(ValidationLevel.ERROR, f"Error en casos especiales: {e}")
            report.checks_total += 3
        
        # Recomendaciones
        if ieee754.base != 2:
            report.add_recommendation(
                f"IEEE754 base {ieee754.base} no es el estándar. "
                "Considera usar base 2 para máxima compatibilidad."
            )
        
        # Metadata
        report.metadata = {
            'total_bits': ieee754.E_bits + ieee754.F_bits + 1,
            'max_exponent': ieee754.base ** ieee754.E_bits - 1,
            'mantissa_precision': ieee754.F_bits,
        }
        
        return report
    
    def validate_biquinary(self, biquinary) -> ValidationReport:
        """
        Valida código biquinario.
        
        Args:
            biquinary: BiquinaryGen o variante
            
        Returns:
            ValidationReport
        """
        report = ValidationReport(
            representation_type=f"Biquinario {biquinary.bits} bits",
            is_valid=True
        )
        
        # Chequeo 1: Bits válido
        if hasattr(biquinary, 'bits') and biquinary.bits > 0:
            report.checks_passed += 1
        else:
            report.add_issue(ValidationLevel.ERROR, "Bits no válido")
        report.checks_total += 1
        
        # Chequeo 2: Regla de validez (2 bits = 1)
        try:
            # Probar con valores 0-9
            for digit in range(10):
                code = biquinary.encode_digit(digit)
                # Contar bits en 1
                ones = bin(code).count('1')
                if ones != 2:
                    report.add_issue(
                        ValidationLevel.ERROR,
                        f"Dígito {digit}: código {code:0{biquinary.bits}b} tiene {ones} bits en 1 (esperado 2)"
                    )
                    report.is_valid = False
            
            report.checks_passed += 1
            report.checks_total += 1
        except Exception as e:
            report.add_issue(ValidationLevel.ERROR, f"Error en validación biquinaria: {e}")
            report.checks_total += 1
        
        # Chequeo 3: Decodificación inversa
        try:
            for digit in range(10):
                code = biquinary.encode_digit(digit)
                decoded = biquinary.decode_digit(code)
                if decoded != digit:
                    report.add_issue(
                        ValidationLevel.ERROR,
                        f"Decodificación falló: {digit} → {code} → {decoded}"
                    )
            report.checks_passed += 1
            report.checks_total += 1
        except Exception as e:
            report.add_issue(ValidationLevel.WARNING, f"Error en decodificación: {e}")
        
        # Recomendaciones
        report.add_recommendation(
            f"Biquinario {biquinary.bits} bits: verifica si es estándar en tu aplicación."
        )
        
        # Metadata
        report.metadata = {
            'bits': biquinary.bits,
            'max_codes': 2 ** biquinary.bits,
            'valid_codes': 10,  # 0-9
        }
        
        return report
    
    def compare_error(self, value: float, fp1, fp2) -> Dict:
        """
        Compara error de representación entre dos sistemas.
        
        Args:
            value: valor a representar
            fp1, fp2: representaciones a comparar
            
        Returns:
            dict con análisis de errores
        """
        try:
            # Codificar en ambos sistemas
            code1 = fp1.encode(value)
            code2 = fp2.encode(value)
            
            # Decodificar
            decoded1 = fp1.decode(code1)
            decoded2 = fp2.decode(code2)
            
            # Calcular errores
            error_abs_1 = abs(value - decoded1)
            error_abs_2 = abs(value - decoded2)
            
            error_rel_1 = error_abs_1 / abs(value) if value != 0 else 0
            error_rel_2 = error_abs_2 / abs(value) if value != 0 else 0
            
            return {
                'value': value,
                'fp1': {
                    'name': str(fp1),
                    'decoded': decoded1,
                    'error_absolute': error_abs_1,
                    'error_relative': error_rel_1,
                },
                'fp2': {
                    'name': str(fp2),
                    'decoded': decoded2,
                    'error_absolute': error_abs_2,
                    'error_relative': error_rel_2,
                },
                'winner': 'fp1' if error_rel_1 < error_rel_2 else 'fp2' if error_rel_2 < error_rel_1 else 'tie',
            }
        except Exception as e:
            return {'error': str(e)}


def batch_validate(representations: List[Any]) -> List[ValidationReport]:
    """
    Valida múltiples representaciones.
    
    Args:
        representations: lista de representaciones
        
    Returns:
        lista de reportes
    """
    validator = RepresentationValidator()
    reports = []
    
    for rep in representations:
        if hasattr(rep, 'E') and hasattr(rep, 'F'):  # FixedPoint
            reports.append(validator.validate_fixed_point(rep))
        elif hasattr(rep, 'E_bits'):  # IEEE754
            reports.append(validator.validate_ieee754(rep))
        elif hasattr(rep, 'bits'):  # Biquinario
            reports.append(validator.validate_biquinary(rep))
    
    return reports
