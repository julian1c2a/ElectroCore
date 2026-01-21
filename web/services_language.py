#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de Lenguajes Formales
==============================

Proporciona operaciones para generar y manipular lenguajes formales
de longitud fija sobre un alfabeto dado.
"""

from typing import List, Set, Dict, Optional, Tuple, Any
from itertools import product

# Importar modelos de forma dinámica
def _load_models():
    """Carga los modelos de forma dinámica"""
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path
    
    models_path = Path(__file__).parent / 'models.py'
    spec = spec_from_file_location("formal_models_for_services_lang", models_path)
    formal_models = module_from_spec(spec)
    spec.loader.exec_module(formal_models)
    return formal_models

_models = _load_models()
Language = _models.Language


class LanguageService:
    """Servicio para gestionar lenguajes formales"""
    
    def __init__(self, alphabet_service):
        """
        Inicializa el servicio
        
        Args:
            alphabet_service: Referencia al AlphabetService
        """
        self.alphabet_service = alphabet_service
        self.languages: Dict[str, Language] = {}
    
    # ========================================================================
    # CRUD Básico
    # ========================================================================
    
    def create(self, name: str, alphabet_id: str, length: int,
              words: Optional[Set[str]] = None,
              conditions: str = "") -> Tuple[bool, str, Optional[Language]]:
        """
        Crea un nuevo lenguaje
        
        Args:
            name: Nombre del lenguaje
            alphabet_id: ID del alfabeto a usar
            length: Longitud fija de palabras
            words: Conjunto de palabras (opcional)
            conditions: Descripción de condiciones (opcional)
        
        Returns:
            (éxito, mensaje, lenguaje_creado)
        """
        # Validar que el alfabeto exista
        alphabet = self.alphabet_service.get(alphabet_id)
        if not alphabet:
            return False, "Alfabeto no encontrado", None
        
        if length < 1:
            return False, "Longitud debe ser >= 1", None
        
        # Crear lenguaje
        language = Language(
            name=name,
            alphabet_id=alphabet_id,
            length=length,
            words=words or set(),
            conditions=conditions
        )
        
        is_valid, msg = language.validate()
        if not is_valid:
            return False, msg, None
        
        self.languages[language.id] = language
        return True, "Lenguaje creado", language
    
    def get(self, language_id: str) -> Optional[Language]:
        """Obtiene un lenguaje por ID"""
        return self.languages.get(language_id)
    
    def get_all(self) -> List[Language]:
        """Obtiene todos los lenguajes"""
        return list(self.languages.values())
    
    def delete(self, language_id: str) -> Tuple[bool, str]:
        """Elimina un lenguaje"""
        if language_id not in self.languages:
            return False, "Lenguaje no encontrado"
        
        del self.languages[language_id]
        return True, "Lenguaje eliminado"
    
    # ========================================================================
    # Generación de Lenguajes
    # ========================================================================
    
    def generate_all_words(self, alphabet_id: str, length: int) -> Tuple[bool, str, Optional[Set[str]]]:
        """
        Genera todas las palabras de longitud 'length' sobre el alfabeto
        
        Nota: Para alfabetos grandes y longitudes grandes, esto puede
        resultar en millones de palabras.
        
        Args:
            alphabet_id: ID del alfabeto
            length: Longitud de palabras
        
        Returns:
            (éxito, mensaje, conjunto_palabras)
        """
        alphabet = self.alphabet_service.get(alphabet_id)
        if not alphabet:
            return False, "Alfabeto no encontrado", None
        
        # Limitar para evitar explosión combinatoria
        max_words = 100_000
        expected_count = alphabet.cardinality ** length
        if expected_count > max_words:
            return False, f"Demasiadas palabras ({expected_count:,} > {max_words:,})", None
        
        # Generar con product
        words = {''.join(w) for w in product(alphabet.symbols, repeat=length)}
        return True, f"Generadas {len(words)} palabras", words
    
    def generate_custom(self, alphabet_id: str, length: int,
                       condition: str) -> Tuple[bool, str, Optional[Set[str]]]:
        """
        Genera palabras que cumplen una condición personalizada
        
        Ejemplo de condiciones:
        - 'no_repeated': Sin símbolos repetidos
        - 'starts_with_0': Comienza con 0
        - 'ends_with_1': Termina con 1
        - 'palindrome': Es un palíndromo
        - 'even_zeros': Número par de ceros
        
        Args:
            alphabet_id: ID del alfabeto
            length: Longitud de palabras
            condition: Nombre de la condición
        
        Returns:
            (éxito, mensaje, conjunto_palabras)
        """
        alphabet = self.alphabet_service.get(alphabet_id)
        if not alphabet:
            return False, "Alfabeto no encontrado", None
        
        # Generar todas las palabras primero
        success, msg, all_words = self.generate_all_words(alphabet_id, length)
        if not success:
            return False, msg, None
        
        # Aplicar condición
        if condition == 'no_repeated':
            words = {w for w in all_words if len(set(w)) == len(w)}
        
        elif condition == 'starts_with_0':
            words = {w for w in all_words if w[0] == '0'}
        
        elif condition == 'ends_with_1':
            words = {w for w in all_words if w[-1] == '1'}
        
        elif condition == 'palindrome':
            words = {w for w in all_words if w == w[::-1]}
        
        elif condition == 'even_zeros':
            words = {w for w in all_words if w.count('0') % 2 == 0}
        
        elif condition == 'starts_with_1_ends_with_0':
            words = {w for w in all_words if w[0] == '1' and w[-1] == '0'}
        
        else:
            return False, f"Condición desconocida: {condition}", None
        
        return True, f"Generadas {len(words)} palabras con condición '{condition}'", words
    
    # ========================================================================
    # Análisis
    # ========================================================================
    
    def get_cardinality(self, language_id: str) -> Tuple[bool, int]:
        """Obtiene la cardinalidad de un lenguaje"""
        language = self.languages.get(language_id)
        if not language:
            return False, 0
        return True, language.cardinality
    
    def get_word_lengths(self, language_id: str) -> Tuple[bool, Dict[int, int]]:
        """
        Retorna distribución de longitudes de palabras
        
        (Ej: si todas son de longitud n, retorna {n: total_palabras})
        """
        language = self.languages.get(language_id)
        if not language:
            return False, {}
        
        lengths = {}
        for word in language.words:
            l = len(word)
            lengths[l] = lengths.get(l, 0) + 1
        
        return True, lengths
    
    def get_statistics(self, language_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Retorna estadísticas de un lenguaje"""
        language = self.languages.get(language_id)
        if not language:
            return False, {}
        
        alphabet = self.alphabet_service.get(language.alphabet_id)
        if not alphabet:
            return False, {}
        
        words_list = sorted(list(language.words))
        word_lengths = [len(w) for w in words_list]
        
        return True, {
            'cardinality': language.cardinality,
            'expected_max': alphabet.cardinality ** language.length,
            'length': language.length,
            'alphabet_cardinality': alphabet.cardinality,
            'avg_word_length': sum(word_lengths) / len(word_lengths) if word_lengths else 0,
            'min_word_length': min(word_lengths) if word_lengths else 0,
            'max_word_length': max(word_lengths) if word_lengths else 0,
        }
    
    def get_statistics_global(self) -> Dict[str, Any]:
        """Retorna estadísticas globales de lenguajes"""
        all_languages = self.get_all()
        
        total_words = sum(lang.cardinality for lang in all_languages)
        avg_cardinality = total_words / len(all_languages) if all_languages else 0
        
        return {
            'total_languages': len(all_languages),
            'total_words': total_words,
            'avg_cardinality': avg_cardinality,
        }
