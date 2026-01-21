#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos para Lenguajes Formales
==============================

Define las estructuras de datos para:
- Alfabetos (2-36 símbolos)
- Lenguajes de longitud fija
- Ordenamiento y significados
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional
from datetime import datetime
import uuid


@dataclass
class Alphabet:
    """
    Modelo de Alfabeto
    
    Representa un conjunto finito de símbolos para construir palabras.
    Soporta cualquier cardinalidad de 2 a 36.
    
    Atributos:
        id: Identificador único
        name: Nombre del alfabeto
        symbols: Lista de símbolos (en orden)
        cardinality: Número de símbolos
        initial_symbol: Símbolo inicial (para significados)
        is_preset: Si es un alfabeto predefinido
        created_at: Timestamp de creación
    """
    name: str
    symbols: List[str]
    initial_symbol: str = ""
    is_preset: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def cardinality(self) -> int:
        """Cardinalidad del alfabeto (número de símbolos)"""
        return len(self.symbols)
    
    @property
    def symbol_order(self) -> Dict[str, int]:
        """Mapa de símbolo -> índice de orden"""
        return {sym: idx for idx, sym in enumerate(self.symbols)}
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida el alfabeto
        
        Returns:
            (es_válido, mensaje)
        """
        if not self.symbols:
            return False, "Alfabeto debe tener al menos 1 símbolo"
        
        if len(self.symbols) > 36:
            return False, "Alfabeto no puede exceder 36 símbolos"
        
        if len(set(self.symbols)) != len(self.symbols):
            return False, "Alfabeto no puede tener símbolos duplicados"
        
        if self.initial_symbol and self.initial_symbol not in self.symbols:
            return False, "Símbolo inicial debe pertenecer al alfabeto"
        
        return True, "Válido"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el alfabeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'symbols': self.symbols,
            'cardinality': self.cardinality,
            'symbol_order': self.symbol_order,
            'initial_symbol': self.initial_symbol,
            'is_preset': self.is_preset,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class Language:
    """
    Modelo de Lenguaje Formal
    
    Representa un lenguaje formal de palabras de longitud fija.
    Las palabras se generan a partir de un alfabeto.
    
    Atributos:
        id: Identificador único
        name: Nombre del lenguaje
        alphabet_id: ID del alfabeto usado
        length: Longitud fija de las palabras
        words: Conjunto de palabras válidas
        conditions: Descripción de condiciones (p.ej. "sin símbolos repetidos")
        cardinality: Número de palabras
        created_at: Timestamp de creación
    """
    name: str
    alphabet_id: str
    length: int
    words: Set[str] = field(default_factory=set)
    conditions: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def cardinality(self) -> int:
        """Cardinalidad del lenguaje (número de palabras)"""
        return len(self.words)
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida el lenguaje
        
        Returns:
            (es_válido, mensaje)
        """
        if not self.name:
            return False, "Lenguaje debe tener nombre"
        
        if self.length < 1:
            return False, "Longitud debe ser >= 1"
        
        if not self.words:
            return False, "Lenguaje debe tener al menos una palabra"
        
        return True, "Válido"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el lenguaje a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'alphabet_id': self.alphabet_id,
            'length': self.length,
            'words': sorted(list(self.words)),
            'cardinality': self.cardinality,
            'conditions': self.conditions,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class LanguageOrder:
    """
    Modelo de Ordenamiento y Significados
    
    Define un ordenamiento de las palabras de un lenguaje y asigna
    significados a cada palabra.
    
    Atributos:
        id: Identificador único
        language_id: ID del lenguaje
        order_type: Tipo de ordenamiento ('lexicographic', 'numeric', 'custom')
        ordered_words: Lista de palabras en orden
        meanings: Diccionario palabra -> significado
        created_at: Timestamp de creación
    """
    language_id: str
    order_type: str
    ordered_words: List[str] = field(default_factory=list)
    meanings: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida el ordenamiento
        
        Returns:
            (es_válido, mensaje)
        """
        if not self.ordered_words:
            return False, "Debe haber palabras ordenadas"
        
        valid_types = {'lexicographic', 'numeric', 'custom'}
        if self.order_type not in valid_types:
            return False, f"Tipo inválido. Debe ser uno de: {valid_types}"
        
        return True, "Válido"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el ordenamiento a diccionario"""
        return {
            'id': self.id,
            'language_id': self.language_id,
            'order_type': self.order_type,
            'ordered_words': self.ordered_words,
            'meanings': self.meanings,
            'created_at': self.created_at.isoformat()
        }


# ==============================================================================
# DATOS PREESTABLECIDOS
# ==============================================================================

PRESET_ALPHABETS = {
    'binary': Alphabet(
        name='Binario',
        symbols=['0', '1'],
        initial_symbol='0',
        is_preset=True
    ),
    'decimal': Alphabet(
        name='Decimal',
        symbols=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        initial_symbol='0',
        is_preset=True
    ),
    'hexadecimal': Alphabet(
        name='Hexadecimal',
        symbols=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F'],
        initial_symbol='0',
        is_preset=True
    ),
    'dna': Alphabet(
        name='ADN',
        symbols=['A', 'T', 'G', 'C'],
        initial_symbol='A',
        is_preset=True
    ),
}


def get_preset_alphabets() -> Dict[str, Dict[str, Any]]:
    """Retorna los alfabetos preestablecidos en formato diccionario"""
    return {key: alphabet.to_dict() for key, alphabet in PRESET_ALPHABETS.items()}
