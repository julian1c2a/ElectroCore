#!/usr/bin/env python3
"""
link_python_functions.py

Script interactivo para vincular funciones Python con los nodos de documentación.

Permite:
1. Buscar nodos de documentación por ID o título
2. Añadir referencias a funciones Python en core/
3. Actualizar automáticamente los metadatos y el catálogo
4. Generar stubs de funciones Python si no existen

Uso:
    python scripts/link_python_functions.py
    python scripts/link_python_functions.py --node-id 6.1.2.2.1
    python scripts/link_python_functions.py --auto-generate
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import List, Dict, Optional, Any
import argparse


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class Config:
    TARGET_DIR = "docs/temario"
    CATALOG_JSON = "config/temario_catalogado.json"
    CORE_DIR = "core"
    METADATA_FILENAME = "metadata.json"


# ============================================================================
# GESTOR DE CATÁLOGO
# ============================================================================

class CatalogManager:
    """Gestiona el catálogo de temas."""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict[str, Any]:
        """Carga el catálogo desde el archivo JSON."""
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"No se encuentra el catálogo: {self.catalog_path}")
        
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self):
        """Guarda el catálogo al archivo JSON."""
        with open(self.catalog_path, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False)
    
    def find_node_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Busca un nodo por su ID."""
        for item in self.catalog.get("temario_fe", {}).get("items", []):
            if item.get("id") == node_id:
                return item
        return None
    
    def search_nodes(self, query: str) -> List[Dict[str, Any]]:
        """Busca nodos que contengan el query en su título."""
        results = []
        query_lower = query.lower()
        for item in self.catalog.get("temario_fe", {}).get("items", []):
            if query_lower in item.get("titulo", "").lower():
                results.append(item)
        return results
    
    def add_python_ref(self, node_id: str, module: str, function: str, 
                       description: str = "", implemented: bool = False):
        """Añade una referencia Python a un nodo."""
        node = self.find_node_by_id(node_id)
        if not node:
            raise ValueError(f"No se encuentra el nodo con ID: {node_id}")
        
        python_ref = {
            "module": module,
            "function": function,
            "description": description,
            "implemented": implemented
        }
        
        if "python_refs" not in node:
            node["python_refs"] = []
        
        # Evitar duplicados
        existing = any(
            ref["module"] == module and ref["function"] == function
            for ref in node["python_refs"]
        )
        
        if not existing:
            node["python_refs"].append(python_ref)
            return True
        return False


# ============================================================================
# GESTOR DE METADATOS
# ============================================================================

class MetadataManager:
    """Gestiona los archivos de metadatos en la estructura de documentación."""
    
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
    
    def update_node_metadata(self, node_id: str, python_refs: List[Dict[str, Any]]):
        """Actualiza los metadatos de un nodo específico."""
        # Buscar el archivo metadata.json que contiene este nodo
        for root, dirs, files in os.walk(self.target_dir):
            if Config.METADATA_FILENAME in files:
                metadata_path = os.path.join(root, Config.METADATA_FILENAME)
                
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Buscar el nodo en los metadatos
                updated = False
                for node in metadata.get("nodes", []):
                    if node.get("id") == node_id:
                        node["python_refs"] = python_refs
                        updated = True
                        break
                
                if updated:
                    with open(metadata_path, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2, ensure_ascii=False)
                    return True
        
        return False


# ============================================================================
# GENERADOR DE CÓDIGO PYTHON
# ============================================================================

class PythonCodeGenerator:
    """Genera stubs de código Python para funciones vinculadas."""
    
    def __init__(self, core_dir: str):
        self.core_dir = core_dir
    
    def generate_stub(self, module: str, function: str, description: str = "") -> str:
        """Genera el código stub para una función."""
        module_path = os.path.join(self.core_dir, f"{module}.py")
        
        # Verificar si el archivo ya existe
        if os.path.exists(module_path):
            # Verificar si la función ya existe
            if self._function_exists(module_path, function):
                return f"La función {function} ya existe en {module}.py"
        
        # Generar el stub
        stub_code = self._create_function_stub(function, description)
        
        # Añadir al archivo o crear nuevo
        if os.path.exists(module_path):
            with open(module_path, 'a', encoding='utf-8') as f:
                f.write("\n\n")
                f.write(stub_code)
        else:
            # Crear nuevo archivo con header
            os.makedirs(os.path.dirname(module_path), exist_ok=True)
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(self._create_module_header(module))
                f.write("\n\n")
                f.write(stub_code)
        
        return f"✅ Stub generado: {module_path}::{function}"
    
    def _function_exists(self, module_path: str, function_name: str) -> bool:
        """Verifica si una función ya existe en un módulo."""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return True
            return False
        except:
            return False
    
    def _create_module_header(self, module: str) -> str:
        """Crea el header para un nuevo módulo."""
        return f'''"""
{module}.py

Módulo generado automáticamente para {module}.

Este módulo contiene funciones relacionadas con el contenido del temario
de Fundamentos de Electrónica.
"""

from typing import List, Dict, Any, Optional, Tuple
import random
'''
    
    def _create_function_stub(self, function_name: str, description: str = "") -> str:
        """Crea el stub de una función."""
        desc = description or "Función pendiente de implementar"
        
        return f'''def {function_name}(**kwargs) -> Dict[str, Any]:
    """
    {desc}
    
    Args:
        **kwargs: Parámetros específicos de la función.
        
    Returns:
        Dict con el resultado de la operación.
        
    Example:
        >>> result = {function_name}()
        >>> print(result)
    """
    raise NotImplementedError("Esta función aún no ha sido implementada")
'''


# ============================================================================
# ACTUALIZADOR DE MARKDOWN
# ============================================================================

class MarkdownUpdater:
    """Actualiza los archivos markdown con las referencias Python."""
    
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
    
    def update_node_markdown(self, node_id: str, md_path: str, python_refs: List[Dict[str, Any]]):
        """Actualiza el archivo markdown de un nodo con las nuevas referencias Python."""
        full_path = os.path.join(self.target_dir, md_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  No se encuentra el archivo: {full_path}")
            return False
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generar la sección de funciones Python
        python_section = self._generate_python_section(python_refs)
        
        # Reemplazar o añadir la sección
        pattern = r'## 🔧 Funciones Python Asociadas\n\n.*?(?=\n## |\Z)'
        
        if re.search(pattern, content, re.DOTALL):
            # Reemplazar sección existente
            content = re.sub(
                pattern,
                f"## 🔧 Funciones Python Asociadas\n\n{python_section}",
                content,
                flags=re.DOTALL
            )
        else:
            # Añadir nueva sección antes de "Recursos Adicionales" si existe
            if "## 📚 Recursos Adicionales" in content:
                content = content.replace(
                    "## 📚 Recursos Adicionales",
                    f"## 🔧 Funciones Python Asociadas\n\n{python_section}\n\n## 📚 Recursos Adicionales"
                )
            else:
                # Añadir al final
                content += f"\n\n## 🔧 Funciones Python Asociadas\n\n{python_section}"
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    def _generate_python_section(self, python_refs: List[Dict[str, Any]]) -> str:
        """Genera el markdown de la sección de funciones Python."""
        if not python_refs:
            return "*No hay funciones Python asociadas aún*"
        
        lines = []
        for ref in python_refs:
            module = ref.get("module", "")
            function = ref.get("function", "")
            description = ref.get("description", "")
            implemented = ref.get("implemented", False)
            
            status_icon = "✅" if implemented else "⚠️"
            full_path = f"{module}.{function}"
            
            lines.append(f"- {status_icon} `{full_path}`")
            if description:
                lines.append(f"  - {description}")
        
        return "\n".join(lines)


# ============================================================================
# INTERFAZ INTERACTIVA
# ============================================================================

class InteractiveLinker:
    """Interfaz interactiva para vincular funciones."""
    
    def __init__(self):
        self.catalog_mgr = CatalogManager(Config.CATALOG_JSON)
        self.metadata_mgr = MetadataManager(Config.TARGET_DIR)
        self.code_gen = PythonCodeGenerator(Config.CORE_DIR)
        self.md_updater = MarkdownUpdater(Config.TARGET_DIR)
    
    def run(self, node_id: Optional[str] = None):
        """Ejecuta el proceso interactivo."""
        print("=" * 70)
        print("🔗 ElectroCore - Vinculador de Funciones Python")
        print("=" * 70)
        
        if node_id:
            # Modo directo: vincular a un nodo específico
            self._link_to_node(node_id)
        else:
            # Modo interactivo
            self._interactive_mode()
    
    def _interactive_mode(self):
        """Modo interactivo de vinculación."""
        while True:
            print("\n" + "-" * 70)
            print("Opciones:")
            print("  1. Buscar nodo por ID")
            print("  2. Buscar nodo por título")
            print("  3. Listar todos los nodos")
            print("  0. Salir")
            
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                node_id = input("Introduce el ID del nodo: ").strip()
                self._link_to_node(node_id)
            elif choice == "2":
                query = input("Introduce el término de búsqueda: ").strip()
                self._search_and_select(query)
            elif choice == "3":
                self._list_all_nodes()
            else:
                print("❌ Opción no válida")
        
        # Guardar cambios al salir
        self.catalog_mgr.save()
        print("\n✅ Cambios guardados")
    
    def _link_to_node(self, node_id: str):
        """Vincula funciones Python a un nodo específico."""
        node = self.catalog_mgr.find_node_by_id(node_id)
        
        if not node:
            print(f"❌ No se encuentra el nodo con ID: {node_id}")
            return
        
        print(f"\n📄 Nodo seleccionado:")
        print(f"   ID: {node['id']}")
        print(f"   Título: {node['titulo']}")
        print(f"   Nivel: {node['nivel']}")
        
        # Mostrar referencias existentes
        existing_refs = node.get("python_refs", [])
        if existing_refs:
            print(f"\n🔧 Referencias existentes:")
            for i, ref in enumerate(existing_refs, 1):
                status = "✅" if ref.get("implemented") else "⚠️"
                print(f"   {i}. {status} {ref['module']}.{ref['function']}")
        
        print("\n¿Qué deseas hacer?")
        print("  1. Añadir nueva referencia")
        print("  2. Generar stubs de código")
        print("  0. Volver")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            self._add_reference(node_id)
        elif choice == "2":
            self._generate_stubs(node_id, existing_refs)
    
    def _add_reference(self, node_id: str):
        """Añade una nueva referencia Python a un nodo."""
        print("\n➕ Añadir nueva referencia Python\n")
        
        module = input("Nombre del módulo (ej: sistemas_numeracion_basicos): ").strip()
        function = input("Nombre de la función (ej: conversion_base_10_a_base_b): ").strip()
        description = input("Descripción breve (opcional): ").strip()
        implemented = input("¿Ya está implementada? (s/n): ").strip().lower() == 's'
        
        if not module or not function:
            print("❌ El módulo y la función son obligatorios")
            return
        
        # Añadir al catálogo
        added = self.catalog_mgr.add_python_ref(
            node_id, module, function, description, implemented
        )
        
        if added:
            print(f"✅ Referencia añadida: {module}.{function}")
            
            # Actualizar metadatos
            node = self.catalog_mgr.find_node_by_id(node_id)
            if node:
                self.metadata_mgr.update_node_metadata(node_id, node.get("python_refs", []))
                
                # Actualizar markdown
                md_path = node.get("md_path", "")
                if md_path:
                    self.md_updater.update_node_markdown(node_id, md_path, node.get("python_refs", []))
                    print(f"✅ Markdown actualizado")
        else:
            print("⚠️  La referencia ya existe")
    
    def _generate_stubs(self, node_id: str, refs: List[Dict[str, Any]]):
        """Genera stubs de código para las referencias no implementadas."""
        print("\n🔨 Generando stubs de código...\n")
        
        for ref in refs:
            if not ref.get("implemented", False):
                module = ref["module"]
                function = ref["function"]
                description = ref.get("description", "")
                
                result = self.code_gen.generate_stub(module, function, description)
                print(f"  {result}")
    
    def _search_and_select(self, query: str):
        """Busca nodos y permite seleccionar uno."""
        results = self.catalog_mgr.search_nodes(query)
        
        if not results:
            print(f"❌ No se encontraron nodos que coincidan con: {query}")
            return
        
        print(f"\n🔍 Resultados de búsqueda ({len(results)}):\n")
        for i, node in enumerate(results, 1):
            print(f"  {i}. [{node['id']}] {node['titulo']}")
        
        try:
            idx = int(input("\nSelecciona un nodo (0 para cancelar): ").strip())
            if 1 <= idx <= len(results):
                selected_node = results[idx - 1]
                self._link_to_node(selected_node['id'])
        except ValueError:
            print("❌ Selección no válida")
    
    def _list_all_nodes(self):
        """Lista todos los nodos del catálogo."""
        items = self.catalog_mgr.catalog.get("temario_fe", {}).get("items", [])
        
        print(f"\n📚 Total de nodos: {len(items)}\n")
        
        for item in items[:20]:  # Mostrar solo los primeros 20
            status = "✅" if item.get("python_refs") else "⚪"
            print(f"  {status} [{item['id']}] {item['titulo']}")
        
        if len(items) > 20:
            print(f"\n  ... y {len(items) - 20} más")


# ============================================================================
# AUTO-GENERACIÓN
# ============================================================================

def auto_generate_links():
    """Genera automáticamente algunas vinculaciones básicas basándose en el temario."""
    linker = InteractiveLinker()
    
    # Ejemplos de vinculaciones automáticas para Módulo 6
    auto_links = [
        {
            "node_id": "6.1.2.2.1",
            "module": "conversion_algoritmos_detallados",
            "function": "conversion_base_10_a_base_b",
            "description": "Conversión de decimal a base B mediante divisiones sucesivas"
        },
        {
            "node_id": "6.1.2.2.2",
            "module": "conversion_algoritmos_detallados",
            "function": "conversion_base_b_a_base_10",
            "description": "Conversión de base B a decimal usando polinomio de Horner"
        },
        {
            "node_id": "6.1.2.2.3",
            "module": "conversiones_bases_relacionadas",
            "function": "conversion_bases_relacionadas",
            "description": "Conversión entre bases relacionadas (B1=b^m, B2=b^n)"
        },
    ]
    
    print("🤖 Generación automática de vinculaciones...\n")
    
    for link in auto_links:
        try:
            added = linker.catalog_mgr.add_python_ref(
                link["node_id"],
                link["module"],
                link["function"],
                link["description"],
                implemented=False
            )
            
            if added:
                print(f"✅ {link['node_id']}: {link['module']}.{link['function']}")
                
                # Actualizar metadatos y markdown
                node = linker.catalog_mgr.find_node_by_id(link["node_id"])
                if node:
                    linker.metadata_mgr.update_node_metadata(
                        link["node_id"], 
                        node.get("python_refs", [])
                    )
                    
                    md_path = node.get("md_path", "")
                    if md_path:
                        linker.md_updater.update_node_markdown(
                            link["node_id"],
                            md_path,
                            node.get("python_refs", [])
                        )
        except Exception as e:
            print(f"❌ Error en {link['node_id']}: {e}")
    
    # Guardar cambios
    linker.catalog_mgr.save()
    print("\n✅ Vinculaciones automáticas completadas")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Vincula funciones Python con nodos de documentación"
    )
    parser.add_argument(
        '--node-id',
        help="ID del nodo al que vincular funciones"
    )
    parser.add_argument(
        '--auto-generate',
        action='store_true',
        help="Genera vinculaciones automáticas básicas"
    )
    
    args = parser.parse_args()
    
    try:
        if args.auto_generate:
            auto_generate_links()
        else:
            linker = InteractiveLinker()
            linker.run(node_id=args.node_id)
    except KeyboardInterrupt:
        print("\n\n👋 Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
