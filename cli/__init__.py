"""
CLI Module para gestión de problemas.

Proporciona interfaz de línea de comandos para operaciones CRUD,
búsqueda, backup, restore y verificación de integridad.
"""

from cli.problems import ProblemsCLI, main

__all__ = ['ProblemsCLI', 'main']
