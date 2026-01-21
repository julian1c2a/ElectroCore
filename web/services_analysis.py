#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de Análisis
====================

Proporciona análisis avanzados de lenguajes y ordenamientos.
"""

from typing import Dict, List, Tuple, Any, Optional

# Importar modelos de forma dinámica
def _load_models():
    """Carga los modelos de forma dinámica"""
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path
    
    models_path = Path(__file__).parent / 'models.py'
    spec = spec_from_file_location("formal_models_for_services_analysis", models_path)
    formal_models = module_from_spec(spec)
    spec.loader.exec_module(formal_models)
    return formal_models

_models = _load_models()
LanguageOrder = _models.LanguageOrder


class AnalysisService:
    """Servicio para análisis avanzados de lenguajes"""
    
    def __init__(self, language_service, alphabet_service):
        """
        Inicializa el servicio
        
        Args:
            language_service: Referencia al LanguageService
            alphabet_service: Referencia al AlphabetService
        """
        self.language_service = language_service
        self.alphabet_service = alphabet_service
        self.orders: Dict[str, LanguageOrder] = {}
    
    # ========================================================================
    # Gestión de Ordenamientos
    # ========================================================================
    
    def create_order(self, language_id: str, order_type: str,
                    ordered_words: Optional[List[str]] = None,
                    meanings: Optional[Dict[str, Any]] = None) -> Tuple[bool, str, Optional[LanguageOrder]]:
        """
        Crea un ordenamiento para un lenguaje
        
        Args:
            language_id: ID del lenguaje
            order_type: 'lexicographic', 'numeric', o 'custom'
            ordered_words: Lista de palabras ordenadas (para custom)
            meanings: Diccionario de significados (opcional)
        
        Returns:
            (éxito, mensaje, ordenamiento_creado)
        """
        language = self.language_service.get(language_id)
        if not language:
            return False, "Lenguaje no encontrado", None
        
        # Si es lexicográfico, ordenar automáticamente
        if order_type == 'lexicographic':
            ordered_words = sorted(list(language.words))
        
        # Si es numérico, convertir a int y ordenar
        elif order_type == 'numeric':
            try:
                ordered_words = sorted(list(language.words), 
                                     key=lambda w: int(w, 10))
            except ValueError:
                return False, "No se puede ordenar numéricamente (palabras no son números)", None
        
        # Si es custom, debe proporcionarse
        elif order_type == 'custom':
            if not ordered_words:
                return False, "Debe proporcionar ordered_words para tipo custom", None
        
        else:
            return False, f"Tipo de ordenamiento inválido: {order_type}", None
        
        # Crear ordenamiento
        order = LanguageOrder(
            language_id=language_id,
            order_type=order_type,
            ordered_words=ordered_words or [],
            meanings=meanings or {}
        )
        
        is_valid, msg = order.validate()
        if not is_valid:
            return False, msg, None
        
        self.orders[order.id] = order
        return True, "Ordenamiento creado", order
    
    def get_order(self, order_id: str) -> Optional[LanguageOrder]:
        """Obtiene un ordenamiento por ID"""
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[LanguageOrder]:
        """Obtiene todos los ordenamientos"""
        return list(self.orders.values())
    
    def delete_order(self, order_id: str) -> Tuple[bool, str]:
        """Elimina un ordenamiento"""
        if order_id not in self.orders:
            return False, "Ordenamiento no encontrado"
        del self.orders[order_id]
        return True, "Ordenamiento eliminado"
    
    # ========================================================================
    # Generación de Significados
    # ========================================================================
    
    def generate_meanings(self, order_id: str, start_value: int = 0,
                         prefix: str = "") -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Genera significados automáticos para las palabras de un ordenamiento
        
        Args:
            order_id: ID del ordenamiento
            start_value: Valor inicial (para significados numéricos)
            prefix: Prefijo para significados (ej: "Palabra ")
        
        Returns:
            (éxito, mensaje, meanings_dict)
        """
        order = self.orders.get(order_id)
        if not order:
            return False, "Ordenamiento no encontrado", None
        
        meanings = {}
        for idx, word in enumerate(order.ordered_words):
            meanings[word] = f"{prefix}{start_value + idx}"
        
        order.meanings = meanings
        return True, f"Generados {len(meanings)} significados", meanings
    
    def generate_numeric_meanings(self, order_id: str) -> Tuple[bool, str]:
        """
        Asigna valores numéricos a palabras (0, 1, 2, ...)
        """
        return self.generate_meanings(order_id, start_value=0, prefix="")
    
    def generate_binary_meanings(self, order_id: str) -> Tuple[bool, str]:
        """
        Asigna representaciones binarias a palabras
        """
        order = self.orders.get(order_id)
        if not order:
            return False, "Ordenamiento no encontrado"
        
        meanings = {}
        for idx, word in enumerate(order.ordered_words):
            meanings[word] = bin(idx)[2:]  # Remover prefijo '0b'
        
        order.meanings = meanings
        return True, f"Generados {len(meanings)} significados binarios"
    
    # ========================================================================
    # Análisis de Propiedades
    # ========================================================================
    
    def analyze_coverage(self, language_id: str) -> Dict[str, Any]:
        """
        Analiza qué porcentaje del espacio total de palabras
        cubre el lenguaje
        """
        language = self.language_service.get(language_id)
        if not language:
            return {'error': 'Lenguaje no encontrado'}
        
        alphabet = self.alphabet_service.get(language.alphabet_id)
        if not alphabet:
            return {'error': 'Alfabeto no encontrado'}
        
        total_possible = alphabet.cardinality ** language.length
        actual = language.cardinality
        coverage = (actual / total_possible * 100) if total_possible > 0 else 0
        
        return {
            'total_possible': total_possible,
            'actual': actual,
            'coverage_percentage': round(coverage, 2),
            'missing': total_possible - actual
        }
    
    def analyze_symbol_distribution(self, language_id: str) -> Dict[str, Any]:
        """
        Analiza la distribución de símbolos en el lenguaje
        """
        language = self.language_service.get(language_id)
        if not language:
            return {'error': 'Lenguaje no encontrado'}
        
        alphabet = self.alphabet_service.get(language.alphabet_id)
        if not alphabet:
            return {'error': 'Alfabeto no encontrado'}
        
        symbol_count = {sym: 0 for sym in alphabet.symbols}
        total_positions = 0
        
        for word in language.words:
            total_positions += len(word)
            for sym in word:
                if sym in symbol_count:
                    symbol_count[sym] += 1
        
        distribution = {}
        for sym, count in symbol_count.items():
            pct = (count / total_positions * 100) if total_positions > 0 else 0
            distribution[sym] = {
                'count': count,
                'percentage': round(pct, 2)
            }
        
        return {
            'symbol_distribution': distribution,
            'total_positions': total_positions
        }
    
    def analyze_pattern_frequency(self, language_id: str, pattern_length: int) -> Dict[str, Any]:
        """
        Analiza la frecuencia de patrones de longitud dada
        en las palabras del lenguaje
        """
        language = self.language_service.get(language_id)
        if not language:
            return {'error': 'Lenguaje no encontrado'}
        
        pattern_count = {}
        
        for word in language.words:
            for i in range(len(word) - pattern_length + 1):
                pattern = word[i:i + pattern_length]
                pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
        
        # Ordenar por frecuencia
        sorted_patterns = sorted(pattern_count.items(), 
                               key=lambda x: x[1], 
                               reverse=True)
        
        return {
            'pattern_length': pattern_length,
            'unique_patterns': len(pattern_count),
            'patterns': [{'pattern': p, 'frequency': f} for p, f in sorted_patterns]
        }
    
    def get_order_comparison(self) -> Dict[str, Any]:
        """
        Compara diferentes órdenes de los lenguajes
        """
        orders_by_language = {}
        
        for order in self.get_all_orders():
            lang_id = order.language_id
            if lang_id not in orders_by_language:
                orders_by_language[lang_id] = []
            
            orders_by_language[lang_id].append({
                'id': order.id,
                'type': order.order_type,
                'word_count': len(order.ordered_words)
            })
        
        return {
            'total_orders': len(self.orders),
            'orders_by_language': orders_by_language
        }
    
    # ========================================================================
    # Estadísticas Globales
    # ========================================================================
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas globales del sistema"""
        all_languages = self.language_service.get_all()
        all_orders = self.get_all_orders()
        
        return {
            'languages': len(all_languages),
            'orders': len(all_orders),
            'total_words': sum(lang.cardinality for lang in all_languages),
            'alphabets': len(self.alphabet_service.get_all()),
        }
