#!/usr/bin/env python3
"""
sync_python_refs.py

Parser automático que extrae referencias Python desde los archivos Markdown
usando la sintaxis [[módulo.función]] y las sincroniza con el catálogo JSON.

Sintaxis en Markdown:
    [[core.formal_languages.alfabeto_definicion]]
    [[core.ieee754.convertir_decimal_ieee754]]
    
El script:
1. Escanea todos los .md en docs/temario/
2. Extrae referencias [[...]]
3. Actualiza config/temario_catalogado.json
4. Actualiza metadata.json de cada nodo
5. (Opcional) Genera stubs en core/

Uso:
    python scripts/sync_python_refs.py                    # Escanear y reportar
    python scripts/sync_python_refs.py --update           # Actualizar catálogo
    python scripts/sync_python_refs.py --generate-stubs   # Generar stubs en core/
    python scripts/sync_python_refs.py --verbose          # Modo detallado
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import argparse


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class Config:
    TARGET_DIR = "docs/temario"
    CATALOG_JSON = "config/temario_catalogado.json"
    CORE_DIR = "core"
    
    # Patrón para detectar referencias Python en Markdown
    # Formato: [[core.modulo.funcion]] o [[modulo.funcion]]
    PYTHON_REF_PATTERN = r'\[\[([a-zA-Z_][a-zA-Z0-9_\.]*)\]\]'


# ============================================================================
# EXTRACTOR DE REFERENCIAS
# ============================================================================

class ReferenceExtractor:
    """Extrae referencias Python desde archivos Markdown."""
    
    def __init__(self, target_dir: str, pattern: str):
        self.target_dir = Path(target_dir)
        self.pattern = re.compile(pattern)
        self.references: Dict[str, List[Dict]] = defaultdict(list)
    
    def scan_all_markdown_files(self) -> Dict[str, List[Dict]]:
        """Escanea todos los archivos .md y extrae referencias."""
        print(f"🔍 Escaneando archivos Markdown en: {self.target_dir}")
        
        count = 0
        for md_file in self.target_dir.rglob("*.md"):
            refs = self.extract_from_file(md_file)
            if refs:
                count += len(refs)
        
        print(f"✅ Se encontraron {count} referencias en {len(self.references)} nodos")
        return dict(self.references)
    
    def extract_from_file(self, filepath: Path) -> List[Dict]:
        """Extrae referencias de un archivo específico."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Error leyendo {filepath}: {e}")
            return []
        
        # Buscar el ID del nodo en el archivo
        node_id = self._extract_node_id(content)
        if not node_id:
            return []
        
        # Extraer todas las referencias [[...]]
        matches = self.pattern.findall(content)
        if not matches:
            return []
        
        refs = []
        for match in matches:
            ref_info = self._parse_reference(match, filepath, content)
            if ref_info:
                refs.append(ref_info)
        
        if refs:
            self.references[node_id] = refs
        
        return refs
    
    def _extract_node_id(self, content: str) -> Optional[str]:
        """Extrae el ID del nodo desde el contenido Markdown."""
        # Buscar patrón: **ID:** `X.X.X.X`
        match = re.search(r'\*\*ID:\*\*\s*`([^`]+)`', content)
        return match.group(1) if match else None
    
    def _parse_reference(self, ref_string: str, filepath: Path, 
                         content: str) -> Optional[Dict]:
        """Parsea una referencia individual y extrae metadatos."""
        parts = ref_string.split('.')
        
        # Determinar módulo y función/clase/método
        # Formato esperado: modulo.Clase.metodo o modulo.funcion
        if parts[0] == 'core':
            # Si empieza con 'core', el módulo es parts[1]
            module = parts[1]
            # Todo lo demás después del módulo es la función/clase/método
            function = '.'.join(parts[2:]) if len(parts) > 2 else ''
        else:
            # Si no empieza con 'core', el módulo es el primer elemento
            module = parts[0]
            # Todo lo demás es la función/clase/método
            function = '.'.join(parts[1:]) if len(parts) > 1 else ''
        
        # Intentar extraer descripción (buscar cerca de la referencia)
        description = self._extract_description(ref_string, content)
        
        # Verificar si está implementada
        implemented = self._check_if_implemented(module, function)
        
        return {
            "module": module,
            "function": function,
            "description": description,
            "implemented": implemented,
            "source_file": str(filepath.relative_to(self.target_dir.parent))
        }
    
    def _extract_description(self, ref_string: str, content: str) -> str:
        """Intenta extraer la descripción asociada a la referencia."""
        # Buscar el contexto alrededor de la referencia
        pattern = rf'\[\[{re.escape(ref_string)}\]\].*?[-:]?\s*\*\*Descripción[:\*]+\s*([^\n]+)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Intentar buscar en la misma línea o línea siguiente
        pattern2 = rf'\[\[{re.escape(ref_string)}\]\][^\n]*\n[^\n]*?:\s*([^\n]+)'
        match2 = re.search(pattern2, content)
        
        if match2:
            return match2.group(1).strip()
        
        return ""
    
    def _check_if_implemented(self, module: str, function: str) -> bool:
        """
        Verifica si la función/clase/método existe en core/.
        
        Soporta:
        - Funciones: nombre_funcion
        - Clases: NombreClase
        - Métodos: NombreClase.metodo
        - Atributos estáticos: NombreClase.atributo
        """
        module_path = Path(Config.CORE_DIR) / f"{module.replace('.', '/')}.py"
        
        if not module_path.exists():
            return False
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            # Si contiene punto, es un método o atributo de clase
            if '.' in function:
                parts = function.split('.')
                class_name = parts[0]
                member_name = parts[1]  # Solo el primer nivel después del punto
                
                # Buscar la clase a nivel de módulo
                for node in tree.body:
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        # Buscar el método dentro del body de la clase
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef) and item.name == member_name:
                                return True
                        # No encontrado en esta clase
                        return False
                
                # Clase no encontrada
                return False
            
            # Si no contiene punto, buscar función o clase a nivel de módulo
            for node in tree.body:
                # Buscar funciones
                if isinstance(node, ast.FunctionDef) and node.name == function:
                    return True
                # Buscar clases
                if isinstance(node, ast.ClassDef) and node.name == function:
                    return True
        except Exception as e:
            # Opcional: descomentar para debug
            # print(f"Error checking {module}.{function}: {e}")
            pass
        
        return False


# ============================================================================
# ACTUALIZADOR DE CATÁLOGO
# ============================================================================

class CatalogUpdater:
    """Actualiza el catálogo JSON con las referencias extraídas."""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict:
        """Carga el catálogo desde JSON."""
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"Catálogo no encontrado: {self.catalog_path}")
        
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self):
        """Guarda el catálogo actualizado."""
        with open(self.catalog_path, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=2, ensure_ascii=False)
        print(f"💾 Catálogo guardado: {self.catalog_path}")
    
    def update_references(self, references: Dict[str, List[Dict]]) -> int:
        """Actualiza las referencias Python en el catálogo."""
        updated_count = 0
        items = self.catalog.get("temario_fe", {}).get("items", [])
        
        for item in items:
            node_id = item.get("id")
            if node_id in references:
                # Actualizar python_refs
                new_refs = references[node_id]
                
                # Mantener referencias existentes que no estén en el nuevo escaneo
                existing_refs = item.get("python_refs", [])
                merged_refs = self._merge_references(existing_refs, new_refs)
                
                item["python_refs"] = merged_refs
                updated_count += 1
        
        return updated_count
    
    def _merge_references(self, existing: List[Dict], new: List[Dict]) -> List[Dict]:
        """Combina referencias existentes con nuevas, evitando duplicados."""
        merged = {}
        
        # Añadir existentes
        for ref in existing:
            key = f"{ref['module']}.{ref['function']}"
            merged[key] = ref
        
        # Actualizar/añadir nuevas
        for ref in new:
            key = f"{ref['module']}.{ref['function']}"
            if key in merged:
                # Actualizar descripción si la nueva es más completa
                if ref.get('description') and len(ref['description']) > len(merged[key].get('description', '')):
                    merged[key]['description'] = ref['description']
                # Actualizar estado de implementación
                merged[key]['implemented'] = ref['implemented']
            else:
                merged[key] = ref
        
        return list(merged.values())


# ============================================================================
# GENERADOR DE STUBS
# ============================================================================

class StubGenerator:
    """Genera stubs de funciones Python en core/."""
    
    def __init__(self, core_dir: str):
        self.core_dir = Path(core_dir)
    
    def generate_stubs(self, references: Dict[str, List[Dict]]) -> int:
        """Genera stubs para funciones no implementadas."""
        generated_count = 0
        
        # Agrupar por módulo
        by_module = defaultdict(list)
        for node_id, refs in references.items():
            for ref in refs:
                if not ref['implemented']:
                    by_module[ref['module']].append(ref)
        
        # Generar stub por cada módulo
        for module, funcs in by_module.items():
            if self._generate_module_stub(module, funcs):
                generated_count += len(funcs)
        
        return generated_count
    
    def _generate_module_stub(self, module: str, functions: List[Dict]) -> bool:
        """Genera o actualiza un módulo con stubs de funciones."""
        module_path = self.core_dir / f"{module.replace('.', '/')}.py"
        
        # Crear directorios si no existen
        module_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Si el archivo existe, leer contenido existente
        existing_code = ""
        if module_path.exists():
            with open(module_path, 'r', encoding='utf-8') as f:
                existing_code = f.read()
        
        # Generar stubs solo para funciones que no existen
        new_stubs = []
        for func in functions:
            if not self._function_exists(existing_code, func['function']):
                stub = self._generate_function_stub(func)
                new_stubs.append(stub)
        
        if not new_stubs:
            return False
        
        # Añadir stubs al final del archivo
        with open(module_path, 'a', encoding='utf-8') as f:
            if existing_code and not existing_code.endswith('\n\n'):
                f.write('\n\n')
            f.write('\n\n'.join(new_stubs))
            f.write('\n')
        
        print(f"📝 Generados {len(new_stubs)} stubs en: {module_path}")
        return True
    
    def _function_exists(self, code: str, function_name: str) -> bool:
        """Verifica si una función ya existe en el código."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return True
        except:
            pass
        return False
    
    def _generate_function_stub(self, func: Dict) -> str:
        """Genera el código stub de una función."""
        desc = func.get('description', 'TODO: Añadir descripción')
        
        stub = f'''def {func['function']}(*args, **kwargs):
    """
    {desc}
    
    TODO: Implementar esta función
    
    Args:
        *args: Parámetros por definir
        **kwargs: Parámetros opcionales por definir
    
    Returns:
        TODO: Definir tipo de retorno
    
    Raises:
        NotImplementedError: Función pendiente de implementar
    """
    raise NotImplementedError(f"{func['function']} aún no está implementada")'''
        
        return stub


# ============================================================================
# REPORTE
# ============================================================================

class Reporter:
    """Genera reportes del escaneo de referencias."""
    
    @staticmethod
    def print_summary(references: Dict[str, List[Dict]]):
        """Imprime un resumen de las referencias encontradas."""
        total_refs = sum(len(refs) for refs in references.values())
        implemented = sum(
            1 for refs in references.values() 
            for ref in refs if ref['implemented']
        )
        
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE REFERENCIAS PYTHON")
        print("=" * 70)
        print(f"Total de nodos con referencias: {len(references)}")
        print(f"Total de referencias encontradas: {total_refs}")
        print(f"Implementadas: {implemented} ({implemented/total_refs*100:.1f}%)")
        print(f"Pendientes: {total_refs - implemented} ({(total_refs-implemented)/total_refs*100:.1f}%)")
        print("=" * 70)
    
    @staticmethod
    def print_detailed(references: Dict[str, List[Dict]], verbose: bool = False):
        """Imprime reporte detallado."""
        print("\n📋 DETALLE POR NODO:\n")
        
        for node_id, refs in sorted(references.items()):
            status_icon = "✅" if all(r['implemented'] for r in refs) else "⚠️"
            print(f"{status_icon} Nodo {node_id}: {len(refs)} referencia(s)")
            
            if verbose:
                for ref in refs:
                    impl = "✅" if ref['implemented'] else "❌"
                    print(f"   {impl} {ref['module']}.{ref['function']}")
                    if ref.get('description'):
                        print(f"      → {ref['description'][:60]}...")
                print()


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza referencias Python desde Markdown al catálogo"
    )
    parser.add_argument(
        '--update', 
        action='store_true',
        help='Actualizar el catálogo JSON con las referencias encontradas'
    )
    parser.add_argument(
        '--generate-stubs', 
        action='store_true',
        help='Generar stubs de funciones en core/ para referencias no implementadas'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    print("🚀 Sync Python References - Extracción automática desde Markdown")
    print("=" * 70)
    
    # 1. Extraer referencias
    extractor = ReferenceExtractor(Config.TARGET_DIR, Config.PYTHON_REF_PATTERN)
    references = extractor.scan_all_markdown_files()
    
    if not references:
        print("\n⚠️  No se encontraron referencias [[...]] en los archivos Markdown")
        return
    
    # 2. Mostrar reporte
    Reporter.print_summary(references)
    Reporter.print_detailed(references, args.verbose)
    
    # 3. Actualizar catálogo si se solicita
    if args.update:
        print("\n🔄 Actualizando catálogo...")
        updater = CatalogUpdater(Config.CATALOG_JSON)
        updated = updater.update_references(references)
        updater.save()
        print(f"✅ {updated} nodos actualizados en el catálogo")
    
    # 4. Generar stubs si se solicita
    if args.generate_stubs:
        print("\n📝 Generando stubs en core/...")
        generator = StubGenerator(Config.CORE_DIR)
        generated = generator.generate_stubs(references)
        print(f"✅ {generated} funciones stub generadas")
    
    # 5. Mensaje final
    if not args.update and not args.generate_stubs:
        print("\n💡 Usa --update para actualizar el catálogo")
        print("💡 Usa --generate-stubs para generar funciones stub en core/")
    
    print("\n" + "=" * 70)
    print("✅ Proceso completado")
    print("=" * 70)


if __name__ == "__main__":
    main()
