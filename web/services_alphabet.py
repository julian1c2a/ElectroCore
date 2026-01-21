#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de Alfabetos
=====================

Proporciona operaciones CRUD y utilidades para manejo de alfabetos.
"""

from typing import List, Dict, Optional, Tuple, Any
import uuid

# Importar modelos de forma dinámica para evitar conflictos de path
def _load_models():
    """Carga los modelos de forma dinámica"""
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path
    
    models_path = Path(__file__).parent / 'models.py'
    spec = spec_from_file_location("formal_models_for_services", models_path)
    formal_models = module_from_spec(spec)
    spec.loader.exec_module(formal_models)
    return formal_models

_models = _load_models()
Alphabet = _models.Alphabet
PRESET_ALPHABETS = _models.PRESET_ALPHABETS
get_preset_alphabets = _models.get_preset_alphabets


class AlphabetService:
    """Servicio para gestionar alfabetos"""
    
    def __init__(self):
        """Inicializa con alfabetos en memoria"""
        self.alphabets: Dict[str, Alphabet] = {}
        self._load_presets()
    
    def _load_presets(self):
        """Carga los alfabetos preestablecidos"""
        for key, alphabet in PRESET_ALPHABETS.items():
            self.alphabets[alphabet.id] = alphabet
    
    # ========================================================================
    # CRUD Básico
    # ========================================================================
    
    def create(self, name: str, symbols: List[str], 
              initial_symbol: str = "") -> Tuple[bool, str, Optional[Alphabet]]:
        """
        Crea un nuevo alfabeto
        
        Args:
            name: Nombre del alfabeto
            symbols: Lista de símbolos
            initial_symbol: Símbolo inicial (opcional)
        
        Returns:
            (éxito, mensaje, alfabeto_creado)
        """
        alphabet = Alphabet(
            name=name,
            symbols=symbols,
            initial_symbol=initial_symbol,
            is_preset=False
        )
        
        is_valid, msg = alphabet.validate()
        if not is_valid:
            return False, msg, None
        
        self.alphabets[alphabet.id] = alphabet
        return True, "Alfabeto creado", alphabet
    
    def get(self, alphabet_id: str) -> Optional[Alphabet]:
        """Obtiene un alfabeto por ID"""
        return self.alphabets.get(alphabet_id)
    
    def get_all(self) -> List[Alphabet]:
        """Obtiene todos los alfabetos"""
        return list(self.alphabets.values())
    
    def update(self, alphabet_id: str, name: Optional[str] = None,
              symbols: Optional[List[str]] = None,
              initial_symbol: Optional[str] = None) -> Tuple[bool, str]:
        """
        Actualiza un alfabeto
        
        Nota: No se pueden actualizar alfabetos preestablecidos
        """
        alphabet = self.alphabets.get(alphabet_id)
        if not alphabet:
            return False, "Alfabeto no encontrado"
        
        if alphabet.is_preset:
            return False, "No se pueden editar alfabetos preestablecidos"
        
        if name:
            alphabet.name = name
        if symbols:
            alphabet.symbols = symbols
        if initial_symbol is not None:
            alphabet.initial_symbol = initial_symbol
        
        is_valid, msg = alphabet.validate()
        if not is_valid:
            return False, f"Alfabeto inválido: {msg}"
        
        return True, "Alfabeto actualizado"
    
    def delete(self, alphabet_id: str) -> Tuple[bool, str]:
        """
        Elimina un alfabeto
        
        Nota: No se pueden eliminar alfabetos preestablecidos
        """
        alphabet = self.alphabets.get(alphabet_id)
        if not alphabet:
            return False, "Alfabeto no encontrado"
        
        if alphabet.is_preset:
            return False, "No se pueden eliminar alfabetos preestablecidos"
        
        del self.alphabets[alphabet_id]
        return True, "Alfabeto eliminado"
    
    # ========================================================================
    # Operaciones Especiales
    # ========================================================================
    
    def get_presets(self) -> Dict[str, Dict[str, Any]]:
        """Retorna los alfabetos preestablecidos"""
        return get_preset_alphabets()
    
    def validate_alphabet(self, name: str, symbols: List[str]) -> Tuple[bool, str]:
        """
        Valida parámetros antes de crear un alfabeto
        
        Returns:
            (es_válido, mensaje)
        """
        if not name or not name.strip():
            return False, "Nombre vacío"
        
        if not symbols:
            return False, "Debe haber al menos 1 símbolo"
        
        if len(symbols) > 36:
            return False, "Máximo 36 símbolos"
        
        if len(set(symbols)) != len(symbols):
            return False, "Símbolos duplicados"
        
        return True, "Válido"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas de alfabetos"""
        all_alphabets = self.get_all()
        preset_count = sum(1 for a in all_alphabets if a.is_preset)
        custom_count = sum(1 for a in all_alphabets if not a.is_preset)
        
        return {
            'total': len(all_alphabets),
            'presets': preset_count,
            'custom': custom_count,
            'avg_cardinality': sum(a.cardinality for a in all_alphabets) / len(all_alphabets) if all_alphabets else 0
        }
