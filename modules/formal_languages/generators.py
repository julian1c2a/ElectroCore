import random
from typing import List, Optional
from core.generator_base import ExerciseGenerator, ExerciseData
from core.formal_languages import ExplicitAlphabet, FixedLengthLanguage, LexicographicalSemantics
from modules.formal_languages.models import LanguageExerciseData

class FormalLanguageGenerator(ExerciseGenerator):
    """
    Generador para Tema 4.1: Alfabetos y Lenguajes.
    Crea ejercicios de:
    - Listado (Listing): Enumerar todas las palabras.
    - Conteo (Counting): Calcular cardinalidad.
    - Ordenación (Ordering): Ordenar lexicográficamente.
    """
    
    def topic(self) -> str:
        return "Teoría de Lenguajes Formales"

    def generate(self, difficulty: int = 1) -> ExerciseData:
        # 1. Configuración por Dificultad
        if difficulty == 1:
            # Nivel Básico: Binario, conteo simple
            symbols = ['0', '1']
            length = random.randint(2, 3)
            p_type = 'listing'
        elif difficulty == 2:
            # Nivel Medio: Alfabetos abstractos (a,b,c)
            symbols = ['a', 'b', 'c']
            length = 2
            p_type = 'counting'
        else:
            # Nivel Avanzado: Símbolos exóticos y ordenación
            symbols = ['@', '#', '&', '$']
            length = 3
            p_type = 'ordering'

        # 2. Lógica Matemática (Usando el CORE que acabamos de crear)
        # Aquí instanciamos las clases matemáticas reales
        alpha = ExplicitAlphabet(symbols)
        lang = FixedLengthLanguage(alpha, length)
        
        # El Core se encarga de la combinatoria compleja
        all_words = list(lang.generate_words())
        
        # 3. Construcción del Problema específico
        words_subset = None
        ordered_sol = None
        desc = ""
        explanation = ""
        
        if p_type == 'ordering':
            # Seleccionamos un subconjunto aleatorio para que el alumno lo ordene
            # (El modelo solo pide List[str], así que pasamos strings crudos)
            words_subset = random.sample(all_words, k=min(5, len(all_words)))
            
            # Usamos la Semántica del Core para calcular la solución correcta
            sem = LexicographicalSemantics(lang)
            ordered_sol = sorted(words_subset, key=sem.evaluate)
            
            desc = (f"Dado el alfabeto $\\Sigma = \\{{ {', '.join(symbols)} \\}}$, "
                    f"ordene lexicográficamente las siguientes palabras: "
                    f"**{', '.join(words_subset)}**.")
            explanation = "El orden lexicográfico se basa en el orden definido de los símbolos en el alfabeto."
            
        elif p_type == 'counting':
            desc = (f"Calcule cuántas palabras de longitud $L={length}$ "
                    f"se pueden formar con el alfabeto $\\Sigma = \\{{ {', '.join(symbols)} \\}}$.")
            explanation = (f"La cardinalidad es $|\\Sigma|^L$. "
                           f"Aquí: ${len(symbols)}^{length} = {lang.size}$.")
            
        else: # listing
            desc = (f"Enumere todas las palabras de longitud $L={length}$ "
                    f"que se pueden formar con el alfabeto $\\Sigma = \\{{ {', '.join(symbols)} \\}}$.")
            explanation = "Se utiliza el producto cartesiano del alfabeto consigo mismo $L$ veces."

        # 4. Empaquetado (Usando el MODELO DTO)
        # Convertimos los objetos matemáticos en datos planos para el JSON
        return LanguageExerciseData(
            title="Lenguajes Formales",
            description=desc,
            alphabet_symbols=symbols,
            word_length=length,
            problem_type=p_type,
            words_to_order=words_subset,
            total_words=lang.size,
            valid_words=all_words, # Solución completa
            ordered_words=ordered_sol,
            explanation=explanation
        )