#!/usr/bin/env python3
"""
validate_integration.py

Script de validación para verificar la integración completa de un nodo
con el sistema de documentación ElectroCore.

Verifica:
1. Presencia en temario_catalogado.json
2. Referencias Python correctas
3. Metadatos JSON actualizados
4. Navegación interconectada en el archivo markdown
5. Funciones Python implementadas
6. Tests existentes

Uso:
    python scripts/validate_integration.py --node-id 1.6.1.1.3
"""

import json
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional


class IntegrationValidator:
    """Validador de integración de nodos de documentación."""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.project_root = Path(__file__).parent.parent
        self.catalog_path = self.project_root / "config" / "temario_catalogado.json"
        self.docs_root = self.project_root / "docs" / "temario"
        self.core_root = self.project_root / "core"
        self.tests_root = self.project_root / "tests"
        
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate(self) -> bool:
        """Ejecuta todas las validaciones."""
        print(f"\n{'='*70}")
        print(f"🔍 VALIDANDO INTEGRACIÓN DEL NODO: {self.node_id}")
        print(f"{'='*70}\n")
        
        # 1. Validar catálogo
        catalog_node = self._validate_catalog()
        if not catalog_node:
            return False
        
        # 2. Validar referencias Python
        self._validate_python_refs(catalog_node)
        
        # 3. Validar metadatos
        self._validate_metadata(catalog_node)
        
        # 4. Validar archivo markdown
        self._validate_markdown(catalog_node)
        
        # 5. Validar funciones Python
        self._validate_python_functions(catalog_node)
        
        # 6. Validar tests
        self._validate_tests(catalog_node)
        
        # Mostrar resultados
        self._print_results()
        
        return len(self.errors) == 0
    
    def _validate_catalog(self) -> Optional[Dict]:
        """Valida la presencia en temario_catalogado.json."""
        print("📋 Validando catálogo...")
        
        if not self.catalog_path.exists():
            self.errors.append(f"❌ No se encuentra el catálogo: {self.catalog_path}")
            return None
        
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        # Buscar nodo
        node = None
        for item in catalog.get("temario_fe", {}).get("items", []):
            if item.get("id") == self.node_id:
                node = item
                break
        
        if not node:
            self.errors.append(f"❌ Nodo {self.node_id} no encontrado en el catálogo")
            return None
        
        self.info.append(f"✅ Nodo encontrado en catálogo: {node.get('titulo')}")
        
        # Verificar campos básicos
        required_fields = ["id", "titulo", "nivel", "parent_id", "md_path", "status"]
        for field in required_fields:
            if field not in node:
                self.warnings.append(f"⚠️  Campo '{field}' faltante en nodo")
        
        # Verificar estado
        if node.get("status") == "completed":
            self.info.append("✅ Estado: completed")
        elif node.get("status") == "pending":
            self.warnings.append("⚠️  Estado: pending (debería ser 'completed')")
        
        return node
    
    def _validate_python_refs(self, node: Dict):
        """Valida referencias Python."""
        print("\n🐍 Validando referencias Python...")
        
        python_refs = node.get("python_refs", [])
        
        if not python_refs:
            self.warnings.append("⚠️  No hay referencias Python en el nodo")
            return
        
        self.info.append(f"✅ {len(python_refs)} referencia(s) Python encontrada(s)")
        
        for ref in python_refs:
            module = ref.get("module", "")
            function = ref.get("function", "")
            implemented = ref.get("implemented", False)
            
            if implemented:
                self.info.append(f"  ✅ {module}.{function} - Implementada")
            else:
                self.warnings.append(f"  ⚠️  {module}.{function} - No implementada")
    
    def _validate_metadata(self, node: Dict):
        """Valida archivo metadata.json."""
        print("\n📄 Validando metadatos...")
        
        md_path = node.get("md_path", "")
        if not md_path:
            self.errors.append("❌ md_path no especificado en el nodo")
            return
        
        # Obtener directorio del archivo
        md_file_path = self.docs_root / md_path
        metadata_path = md_file_path.parent / "metadata.json"
        
        if not metadata_path.exists():
            self.warnings.append(f"⚠️  No se encuentra metadata.json: {metadata_path}")
            return
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Buscar nodo en metadatos
        node_meta = None
        for item in metadata.get("nodes", []):
            if item.get("id") == self.node_id:
                node_meta = item
                break
        
        if not node_meta:
            self.errors.append(f"❌ Nodo {self.node_id} no encontrado en metadata.json")
            return
        
        self.info.append("✅ Nodo encontrado en metadata.json")
        
        # Verificar sincronización con catálogo
        if node_meta.get("python_refs") != node.get("python_refs"):
            self.warnings.append("⚠️  Referencias Python no sincronizadas entre catálogo y metadatos")
        
        if node_meta.get("status") != node.get("status"):
            self.warnings.append("⚠️  Estado no sincronizado entre catálogo y metadatos")
    
    def _validate_markdown(self, node: Dict):
        """Valida archivo markdown."""
        print("\n📝 Validando archivo markdown...")
        
        md_path = node.get("md_path", "")
        md_file_path = self.docs_root / md_path
        
        if not md_file_path.exists():
            self.errors.append(f"❌ Archivo markdown no encontrado: {md_file_path}")
            return
        
        self.info.append(f"✅ Archivo markdown encontrado")
        
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar navegación
        if "**Ruta:**" in content or "[📚 Fundamentos" in content:
            self.info.append("✅ Breadcrumb de navegación presente")
        else:
            self.warnings.append("⚠️  Falta breadcrumb de navegación")
        
        if "[⬅️ Anterior]" in content:
            self.info.append("✅ Enlace al documento anterior presente")
        else:
            self.warnings.append("⚠️  Falta enlace al documento anterior")
        
        # Verificar sección de funciones Python
        if "🔧 Funciones Python Asociadas" in content:
            self.info.append("✅ Sección de funciones Python presente")
        else:
            self.warnings.append("⚠️  Falta sección de funciones Python")
        
        # Verificar ID del nodo
        if f"**ID:** `{self.node_id}`" in content:
            self.info.append(f"✅ ID del nodo presente: {self.node_id}")
        else:
            self.warnings.append(f"⚠️  ID del nodo no encontrado en el markdown")
    
    def _validate_python_functions(self, node: Dict):
        """Valida que las funciones Python existan."""
        print("\n⚙️  Validando funciones Python...")
        
        python_refs = node.get("python_refs", [])
        
        for ref in python_refs:
            module = ref.get("module", "")
            function = ref.get("function", "")
            
            if not module or not function:
                continue
            
            # Convertir module path a file path
            module_parts = module.split(".")
            module_file = self.core_root / ("/".join(module_parts[1:]) + ".py")
            
            if not module_file.exists():
                self.warnings.append(f"⚠️  Archivo no encontrado: {module_file}")
                continue
            
            # Verificar que la función existe
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar definición de función
            pattern = rf"^def {function}\("
            if re.search(pattern, content, re.MULTILINE):
                self.info.append(f"  ✅ Función {function} encontrada en {module_file.name}")
            else:
                self.warnings.append(f"  ⚠️  Función {function} no encontrada en {module_file.name}")
    
    def _validate_tests(self, node: Dict):
        """Valida existencia de tests."""
        print("\n🧪 Validando tests...")
        
        python_refs = node.get("python_refs", [])
        
        if not python_refs:
            return
        
        # Buscar archivos de test relacionados
        test_files = list(self.tests_root.glob("test_*.py"))
        
        found_tests = False
        for ref in python_refs:
            function = ref.get("function", "")
            
            for test_file in test_files:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if function in content:
                    self.info.append(f"  ✅ Tests encontrados para {function} en {test_file.name}")
                    found_tests = True
        
        if not found_tests:
            self.warnings.append("⚠️  No se encontraron tests para las funciones")
    
    def _print_results(self):
        """Imprime resultados de la validación."""
        print(f"\n{'='*70}")
        print("📊 RESULTADOS DE LA VALIDACIÓN")
        print(f"{'='*70}\n")
        
        if self.info:
            print("✅ INFORMACIÓN:")
            for msg in self.info:
                print(f"  {msg}")
            print()
        
        if self.warnings:
            print("⚠️  ADVERTENCIAS:")
            for msg in self.warnings:
                print(f"  {msg}")
            print()
        
        if self.errors:
            print("❌ ERRORES:")
            for msg in self.errors:
                print(f"  {msg}")
            print()
        
        # Resumen
        print(f"{'='*70}")
        if self.errors:
            print("❌ VALIDACIÓN FALLIDA")
        elif self.warnings:
            print("⚠️  VALIDACIÓN COMPLETADA CON ADVERTENCIAS")
        else:
            print("✅ VALIDACIÓN EXITOSA")
        print(f"{'='*70}\n")


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Valida la integración de un nodo con el sistema de documentación"
    )
    parser.add_argument(
        "--node-id",
        required=True,
        help="ID del nodo a validar (ej: 1.6.1.1.3)"
    )
    
    args = parser.parse_args()
    
    validator = IntegrationValidator(args.node_id)
    success = validator.validate()
    
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
