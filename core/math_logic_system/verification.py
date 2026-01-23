"""
Sistema de Verificación de Pruebas

Verifica la validez de demostraciones formales, incluyendo:
- Matching de expresiones con patrones
- Unificación de variables
- Verificación de pasos de inferencia

Autor: ElectroCore Project
"""

from typing import Dict, Optional, List, Set
from .expressions import Expression, Variable, Constant, BinaryOp, UnaryOp, Function, Quantifier, Predicate
from .proof_system import Proof, ProofStep, JustificationType
from .axioms import AxiomSystem


class ExpressionMatcher:
    """
    Verifica si dos expresiones son equivalentes bajo sustitución de variables.
    """
    
    @staticmethod
    def match(pattern: Expression, expr: Expression, bindings: Dict[str, Expression] = None) -> Optional[Dict[str, Expression]]:
        """
        Intenta hacer match de una expresión con un patrón.
        
        Args:
            pattern: Expresión patrón (puede contener variables)
            expr: Expresión concreta
            bindings: Bindings previos de variables
            
        Returns:
            Diccionario de bindings si hay match, None en caso contrario
        """
        if bindings is None:
            bindings = {}
        
        # Si el patrón es una variable
        if isinstance(pattern, Variable):
            if pattern.name in bindings:
                # Verificar consistencia
                return bindings if bindings[pattern.name] == expr else None
            else:
                # Nuevo binding
                new_bindings = bindings.copy()
                new_bindings[pattern.name] = expr
                return new_bindings
        
        # Si el patrón es una constante
        if isinstance(pattern, Constant):
            if isinstance(expr, Constant) and pattern.value == expr.value:
                return bindings
            return None
        
        # Si el patrón es un operador binario
        if isinstance(pattern, BinaryOp):
            if not isinstance(expr, BinaryOp) or pattern.operator != expr.operator:
                return None
            
            # Match recursivo en ambos lados
            left_bindings = ExpressionMatcher.match(pattern.left, expr.left, bindings)
            if left_bindings is None:
                return None
            
            return ExpressionMatcher.match(pattern.right, expr.right, left_bindings)
        
        # Si el patrón es un operador unario
        if isinstance(pattern, UnaryOp):
            if not isinstance(expr, UnaryOp) or pattern.operator != expr.operator:
                return None
            
            return ExpressionMatcher.match(pattern.operand, expr.operand, bindings)
        
        # Si el patrón es una función
        if isinstance(pattern, Function):
            if not isinstance(expr, Function) or pattern.name != expr.name:
                return None
            
            if len(pattern.arguments) != len(expr.arguments):
                return None
            
            current_bindings = bindings
            for p_arg, e_arg in zip(pattern.arguments, expr.arguments):
                current_bindings = ExpressionMatcher.match(p_arg, e_arg, current_bindings)
                if current_bindings is None:
                    return None
            
            return current_bindings
        
        # Si el patrón es un predicado
        if isinstance(pattern, Predicate):
            if not isinstance(expr, Predicate) or pattern.name != expr.name:
                return None
            
            if len(pattern.arguments) != len(expr.arguments):
                return None
            
            current_bindings = bindings
            for p_arg, e_arg in zip(pattern.arguments, expr.arguments):
                current_bindings = ExpressionMatcher.match(p_arg, e_arg, current_bindings)
                if current_bindings is None:
                    return None
            
            return current_bindings
        
        # Si el patrón es un cuantificador
        if isinstance(pattern, Quantifier):
            if not isinstance(expr, Quantifier) or pattern.type != expr.type:
                return None
            
            # Renombrar variables si es necesario
            # (simplificado: asumimos que las variables tienen el mismo nombre)
            if pattern.variable != expr.variable:
                return None
            
            domain_bindings = bindings
            if pattern.domain and expr.domain:
                domain_bindings = ExpressionMatcher.match(pattern.domain, expr.domain, bindings)
                if domain_bindings is None:
                    return None
            
            return ExpressionMatcher.match(pattern.body, expr.body, domain_bindings)
        
        # Tipos no coinciden
        return None


class Unifier:
    """
    Realiza unificación de expresiones.
    """
    
    @staticmethod
    def unify(expr1: Expression, expr2: Expression, subst: Dict[str, Expression] = None) -> Optional[Dict[str, Expression]]:
        """
        Encuentra la sustitución más general que hace que expr1 y expr2 sean iguales.
        
        Args:
            expr1: Primera expresión
            expr2: Segunda expresión
            subst: Sustitución parcial
            
        Returns:
            Diccionario de sustituciones si la unificación es posible, None en caso contrario
        """
        if subst is None:
            subst = {}
        
        # Aplicar sustituciones actuales
        expr1 = Unifier._apply_substitution(expr1, subst)
        expr2 = Unifier._apply_substitution(expr2, subst)
        
        # Si son iguales, no hay nada que unificar
        if expr1 == expr2:
            return subst
        
        # Si una es variable
        if isinstance(expr1, Variable):
            if expr1.name in expr2.free_variables():
                return None  # Occur check
            new_subst = subst.copy()
            new_subst[expr1.name] = expr2
            return new_subst
        
        if isinstance(expr2, Variable):
            if expr2.name in expr1.free_variables():
                return None  # Occur check
            new_subst = subst.copy()
            new_subst[expr2.name] = expr1
            return new_subst
        
        # Si ambas son operadores binarios
        if isinstance(expr1, BinaryOp) and isinstance(expr2, BinaryOp):
            if expr1.operator != expr2.operator:
                return None
            
            left_subst = Unifier.unify(expr1.left, expr2.left, subst)
            if left_subst is None:
                return None
            
            return Unifier.unify(expr1.right, expr2.right, left_subst)
        
        # Si ambas son operadores unarios
        if isinstance(expr1, UnaryOp) and isinstance(expr2, UnaryOp):
            if expr1.operator != expr2.operator:
                return None
            
            return Unifier.unify(expr1.operand, expr2.operand, subst)
        
        # Si ambas son funciones
        if isinstance(expr1, Function) and isinstance(expr2, Function):
            if expr1.name != expr2.name or len(expr1.arguments) != len(expr2.arguments):
                return None
            
            current_subst = subst
            for arg1, arg2 in zip(expr1.arguments, expr2.arguments):
                current_subst = Unifier.unify(arg1, arg2, current_subst)
                if current_subst is None:
                    return None
            
            return current_subst
        
        # No se pueden unificar
        return None
    
    @staticmethod
    def _apply_substitution(expr: Expression, subst: Dict[str, Expression]) -> Expression:
        """Aplica una sustitución a una expresión."""
        if isinstance(expr, Variable) and expr.name in subst:
            return subst[expr.name]
        
        return expr


class ProofVerifier:
    """
    Verifica la validez de una demostración formal.
    """
    
    def __init__(self, axiom_system: Optional[AxiomSystem] = None):
        self.axiom_system = axiom_system
        self.errors: List[str] = []
    
    def verify(self, proof: Proof) -> bool:
        """
        Verifica si una prueba es válida.
        
        Returns:
            True si la prueba es válida, False en caso contrario
        """
        self.errors = []
        
        # Verificar que hay pasos
        if not proof.steps:
            self.errors.append("La prueba no tiene pasos")
            return False
        
        # Verificar que el último paso coincide con el objetivo
        last_step = proof.steps[-1]
        if last_step.statement != proof.goal:
            self.errors.append(
                f"El último paso no coincide con el objetivo.\n"
                f"  Último paso: {last_step.statement}\n"
                f"  Objetivo: {proof.goal}"
            )
            return False
        
        # Verificar cada paso
        valid_statements = set(proof.premises + proof.hypotheses)
        
        for i, step in enumerate(proof.steps, 1):
            if not self._verify_step(step, i, valid_statements, proof):
                return False
            
            # Añadir este paso a las declaraciones válidas
            valid_statements.add(step.statement)
        
        return True
    
    def _verify_step(self,
                     step: ProofStep,
                     step_number: int,
                     valid_statements: Set[Expression],
                     proof: Proof) -> bool:
        """Verifica un paso individual."""
        
        # Verificar según el tipo de justificación
        if step.justification_type == JustificationType.AXIOM:
            return self._verify_axiom_step(step, step_number)
        
        elif step.justification_type == JustificationType.PREMISE:
            if step.statement not in proof.premises:
                self.errors.append(f"Paso {step_number}: Premisa no declarada")
                return False
        
        elif step.justification_type == JustificationType.HYPOTHESIS:
            if step.statement not in proof.hypotheses:
                self.errors.append(f"Paso {step_number}: Hipótesis no declarada")
                return False
        
        elif step.justification_type == JustificationType.INFERENCE:
            return self._verify_inference_step(step, step_number, proof.steps)
        
        elif step.justification_type == JustificationType.PREVIOUS_STEP:
            # Verificar que las dependencias son válidas
            for dep in step.depends_on:
                if dep < 1 or dep > step_number - 1:
                    self.errors.append(
                        f"Paso {step_number}: Dependencia inválida (paso {dep})"
                    )
                    return False
        
        return True
    
    def _verify_axiom_step(self, step: ProofStep, step_number: int) -> bool:
        """Verifica que un paso cita correctamente un axioma."""
        if not self.axiom_system:
            self.errors.append(
                f"Paso {step_number}: Se cita un axioma pero no hay sistema axiomático"
            )
            return False
        
        # Buscar el axioma en el sistema
        # (simplificado: asumimos que la expresión coincide exactamente)
        found = False
        for axiom in self.axiom_system.list_axioms():
            if axiom.statement == step.statement:
                found = True
                break
        
        if not found:
            for postulate in self.axiom_system.list_postulates():
                if postulate.statement == step.statement:
                    found = True
                    break
        
        if not found:
            self.errors.append(
                f"Paso {step_number}: El axioma citado no se encuentra en el sistema"
            )
            return False
        
        return True
    
    def _verify_inference_step(self,
                               step: ProofStep,
                               step_number: int,
                               all_steps: List[ProofStep]) -> bool:
        """Verifica que una inferencia es válida."""
        if not step.rule:
            self.errors.append(
                f"Paso {step_number}: Inferencia sin regla especificada"
            )
            return False
        
        # Obtener las premisas de los pasos dependientes
        premises = []
        for dep in step.depends_on:
            if dep < 1 or dep > len(all_steps):
                self.errors.append(
                    f"Paso {step_number}: Dependencia inválida (paso {dep})"
                )
                return False
            premises.append(all_steps[dep - 1].statement)
        
        # Aplicar la regla
        result = step.rule.apply(*premises)
        
        if result is None:
            self.errors.append(
                f"Paso {step_number}: La regla {step.rule.name()} no puede aplicarse"
            )
            return False
        
        if result != step.statement:
            self.errors.append(
                f"Paso {step_number}: El resultado de la regla no coincide.\n"
                f"  Esperado: {step.statement}\n"
                f"  Obtenido: {result}"
            )
            return False
        
        return True
    
    def get_errors(self) -> List[str]:
        """Obtiene la lista de errores encontrados."""
        return self.errors
