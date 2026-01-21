"""
FASE 1: Data Validator & Metadata Extractor

Responsabilidad: Validar JSON, extraer metadatos, preparar estructura.

Esta fase es fundamental: todas las siguientes dependen de que los datos
sean válidos y bien estructurados.

Salida: JSON "cleaned" y TEX con documentación de los datos.
"""

from typing import Dict, Any, Set
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class ValidationError(Exception):
    """Error en validación de datos del ejercicio."""
    pass


class Phase1DataValidator(ExerciseRendererPhase):
    """
    FASE 1: Validador de datos y extractor de metadatos.
    
    Responsabilidades:
    1. Validar que el JSON tiene estructura correcta
    2. Validar que el JSON tiene todos los campos requeridos
    3. Extraer y validar metadatos
    4. Preparar JSON "limpio" para siguientes fases
    5. Generar TEX documentativo para debugging
    
    Esta fase NO genera contenido visual, solo validación y documentación.
    """
    
    # Campos requeridos para cada tipo de ejercicio
    REQUIRED_FIELDS = {
        'ConversionRow': {
            'problem': {'label', 'val_decimal', 'target_col_idx', 'representable'},
            'solution': {'sol_bin', 'sol_c2', 'sol_sm', 'sol_bcd', 'target_val_str'},
            'metadata': {'exercise_type'}
        },
        'ArithmeticOp': {
            'problem': {'op_type', 'system', 'operand1', 'operand2', 'operator_symbol', 'val1_dec', 'val2_dec'},
            'solution': {'result_dec', 'result_bin', 'overflow', 'underflow', 'carry_bits'},
            'metadata': {'exercise_type'}
        }
    }
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Valida el ejercicio JSON y prepara estructura.
        
        Args:
            exercise_json: JSON del ejercicio
            is_solution: Si es para soluciones o enunciado
        
        Returns:
            PhaseOutput con JSON limpio + TEX documentativo
        
        Raises:
            ValidationError: Si la validación falla
        """
        
        # Extraer secciones
        problem = self._extract_problem(exercise_json)
        solution = self._extract_solution(exercise_json)
        metadata = self._extract_metadata(exercise_json)
        
        # Validar estructura básica
        self._validate_structure(exercise_json)
        
        # Obtener tipo de ejercicio
        exercise_type = metadata.get('exercise_type', 'Unknown')
        
        # Validar campos requeridos según tipo
        if exercise_type in self.REQUIRED_FIELDS:
            self._validate_required_fields(problem, solution, metadata, exercise_type)
        
        # Validar tipos de datos
        self._validate_data_types(problem, solution, exercise_type)
        
        # Extraer información de debugging
        debug_info = self._extract_debug_info(exercise_json)
        
        # Generar TEX documentativo
        latex = self._generate_debug_tex(debug_info, exercise_type)
        
        # Preparar JSON limpio para siguiente fase
        cleaned_json = {
            **exercise_json,
            'phase1_validation': {
                'status': 'valid',
                'exercise_type': exercise_type,
                'problem_fields': list(problem.keys()),
                'solution_fields': list(solution.keys()),
                'validated_at': 'phase1'
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=cleaned_json,
            phase_name="validador",
            tex_filename="00_fase1_validacion.tex"
        )
    
    @property
    def phase_name(self) -> str:
        return "validador"
    
    def _validate_structure(self, exercise_json: Dict[str, Any]) -> None:
        """Valida que el JSON tenga la estructura base correcta."""
        required_top_level = {'title', 'description', 'problem', 'solution', 'metadata'}
        missing = required_top_level - set(exercise_json.keys())
        
        if missing:
            raise ValidationError(
                f"Campos requeridos en nivel superior: {missing}\n"
                f"Campos presentes: {set(exercise_json.keys())}"
            )
    
    def _validate_required_fields(self, problem: Dict, solution: Dict, 
                                 metadata: Dict, exercise_type: str) -> None:
        """Valida que estén todos los campos requeridos según tipo."""
        required = self.REQUIRED_FIELDS.get(exercise_type)
        
        if not required:
            return  # No hay validación específica para este tipo
        
        # Validar campos del problema
        problem_required = required['problem']
        problem_missing = problem_required - set(problem.keys())
        if problem_missing:
            raise ValidationError(
                f"Campos faltantes en 'problem' para {exercise_type}: {problem_missing}"
            )
        
        # Validar campos de solución
        solution_required = required['solution']
        solution_missing = solution_required - set(solution.keys())
        if solution_missing:
            raise ValidationError(
                f"Campos faltantes en 'solution' para {exercise_type}: {solution_missing}"
            )
    
    def _validate_data_types(self, problem: Dict, solution: Dict, 
                            exercise_type: str) -> None:
        """Valida tipos de datos básicos."""
        
        if exercise_type == 'ConversionRow':
            # Validar tipos para ConversionRow
            if 'val_decimal' in problem:
                if not isinstance(problem['val_decimal'], (int, float)):
                    raise ValidationError(
                        f"problem.val_decimal debe ser numérico, "
                        f"pero es {type(problem['val_decimal']).__name__}"
                    )
            
            if 'representable' in problem:
                if not isinstance(problem['representable'], bool):
                    raise ValidationError(
                        f"problem.representable debe ser bool, "
                        f"pero es {type(problem['representable']).__name__}"
                    )
    
    def _extract_debug_info(self, exercise_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información para debugging."""
        return {
            'title': exercise_json.get('title', 'Sin título'),
            'description': exercise_json.get('description', 'Sin descripción'),
            'exercise_type': exercise_json.get('metadata', {}).get('exercise_type', 'Unknown'),
            'problem_fields': list(exercise_json.get('problem', {}).keys()),
            'problem_values': exercise_json.get('problem', {}),
            'solution_fields': list(exercise_json.get('solution', {}).keys()),
            'has_solution': len(exercise_json.get('solution', {})) > 0
        }
    
    def _generate_debug_tex(self, debug_info: Dict[str, Any], 
                           exercise_type: str) -> str:
        """Genera TEX documentativo con info de validación."""
        
        title = debug_info['title']
        desc = debug_info['description']
        ex_type = debug_info['exercise_type']
        problem_fields = debug_info['problem_fields']
        solution_fields = debug_info['solution_fields']
        has_solution = debug_info['has_solution']
        
        latex = f"""% ========================================
% FASE 1: VALIDACIÓN Y METADATOS
% ========================================

% Información del ejercicio
% Título: {title}
% Descripción: {desc}
% Tipo: {ex_type}

% Estado de validación: VÁLIDO ✓

% Campos del problema detectados:
% {', '.join(problem_fields) if problem_fields else '(ninguno)'}

% Campos de solución detectados:
% {', '.join(solution_fields) if solution_fields else '(ninguno)'}

% Solución disponible: {'SÍ' if has_solution else 'NO'}

% ========================================
% Nota: Esta es la salida de FASE 1
% Las siguientes fases construirán sobre esto
% ========================================
"""
        
        return latex
