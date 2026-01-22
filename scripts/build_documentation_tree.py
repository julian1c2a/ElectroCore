#!/usr/bin/env python3
"""
build_documentation_tree.py

Sistema integrado para construir la estructura completa de documentación desde CONTENIDOS_FE.md.

Funcionalidades:
1. Parsea el archivo markdown de contenidos
2. Genera estructura de directorios y archivos markdown interconectados
3. Crea metadatos JSON para cada nodo (con referencias cruzadas)
4. Vincula con funciones Python en core/ mediante sintaxis especial
5. Actualiza temario_catalogado.json con las referencias

Uso:
    python scripts/build_documentation_tree.py [--dry-run] [--force]
"""

import os
import re
import json
import shutil
import unicodedata
from collections import deque
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class Config:
    """Configuración global del script."""
    SOURCE_MD = "docs/CONTENIDOS_FE.md"
    TARGET_DIR = "docs/temario"
    CATALOG_JSON = "config/temario_catalogado.json"
    METADATA_FILENAME = "metadata.json"
    
    # Sintaxis para vincular con funciones Python
    PYTHON_LINK_PATTERN = r'\{@python:\s*([^}]+)\}'
    # Ejemplo: {@python: core.sistemas_numeracion_basicos.conversion_base_b}
    
    # Plantillas de contenido
    STUB_CONTENT = """
## 📝 Contenido Teórico

*Pendiente de desarrollar*

## 🔧 Funciones Python Asociadas

{python_functions}

## 📚 Recursos Adicionales

- Pendiente de añadir referencias

## ✅ Estado de Desarrollo

- [ ] Teoría documentada
- [ ] Ejemplos añadidos
- [ ] Funciones Python implementadas
- [ ] Tests unitarios creados
"""


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

@dataclass
class PythonReference:
    """Representa una referencia a código Python."""
    module: str
    function: str
    description: str = ""
    implemented: bool = False
    
    @property
    def full_path(self) -> str:
        return f"{self.module}.{self.function}"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NodeMetadata:
    """Metadatos completos de un nodo del árbol de documentación."""
    id: str
    title: str
    level: int
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # Rutas y ubicaciones
    md_path: str = ""
    relative_path: str = ""
    
    # Referencias a código Python
    python_refs: List[Dict[str, Any]] = field(default_factory=list)
    
    # Estado de desarrollo
    status: str = "pending"  # pending, in_progress, completed
    has_exercises: bool = False
    has_examples: bool = False
    
    # Navegación
    prev_id: Optional[str] = None
    next_id: Optional[str] = None
    breadcrumb: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentNode:
    """Nodo en el árbol de documentación."""
    original_name: str
    sanitized_name: str
    level: int
    node_id: str = ""
    
    parent: Optional['DocumentNode'] = None
    children: List['DocumentNode'] = field(default_factory=list)
    
    # Rutas del sistema de archivos
    path: str = ""
    is_directory: bool = False
    
    # Metadatos enriquecidos
    metadata: Optional[NodeMetadata] = None
    python_functions: List[PythonReference] = field(default_factory=list)
    
    def add_child(self, node: 'DocumentNode'):
        """Añade un hijo a este nodo."""
        self.children.append(node)
        node.parent = self
    
    def get_ancestors(self) -> List['DocumentNode']:
        """Retorna lista de ancestros desde la raíz hasta el padre."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors
    
    def get_siblings(self) -> List['DocumentNode']:
        """Retorna lista de hermanos (incluyendo este nodo)."""
        if not self.parent:
            return [self]
        return self.parent.children


# ============================================================================
# UTILIDADES
# ============================================================================

class TextUtils:
    """Utilidades para procesamiento de texto."""
    
    @staticmethod
    def clean_name(name: str) -> str:
        """Limpia el nombre eliminando marcadores markdown."""
        cleaned = re.sub(r'^\s*#+\s*|\s*-\s*', '', name).strip()
        cleaned = cleaned.replace('**', '')
        # Eliminar numeración al inicio (ej: "6.1.2.1.1")
        cleaned = re.sub(r'^\d+(\.\d+)*\s*', '', cleaned)
        return cleaned.strip()
    
    @staticmethod
    def sanitize_name(name: str) -> str:
        """Convierte nombre a formato seguro para nombres de archivo."""
        if not name:
            return "unnamed"
        
        # Normalizar unicode
        s = ''.join(c for c in unicodedata.normalize('NFD', name)
                   if unicodedata.category(c) != 'Mn')
        s = s.lower()
        
        # Reemplazar espacios y caracteres especiales
        s = re.sub(r'[\s./:()]+', '_', s)
        s = re.sub(r'[^a-z0-9_]', '', s)
        
        # Eliminar numeración inicial
        s = re.sub(r'^\d+(_\d+)*_?', '', s).strip('_')
        
        # Limpiar underscores múltiples
        s = re.sub(r'_+', '_', s)
        
        return s.strip('_') or "unnamed"
    
    @staticmethod
    def generate_id(node: DocumentNode) -> str:
        """Genera un ID único para un nodo basado en su posición en el árbol."""
        if not node.parent:
            return "root"
        
        ancestors = node.get_ancestors()
        siblings = node.get_siblings()
        
        # Construir ID jerárquico: 1.2.3.1
        parts = []
        for ancestor in ancestors:
            if ancestor.parent:  # Saltar root
                ancestor_siblings = ancestor.get_siblings()
                idx = ancestor_siblings.index(ancestor) + 1
                parts.append(str(idx))
        
        # Añadir índice propio
        idx = siblings.index(node) + 1
        parts.append(str(idx))
        
        return ".".join(parts)


# ============================================================================
# PARSER DE MARKDOWN
# ============================================================================

class MarkdownParser:
    """Parser del archivo CONTENIDOS_FE.md para construir el árbol."""
    
    def __init__(self, source_file: str):
        self.source_file = source_file
    
    def parse(self) -> DocumentNode:
        """Parsea el markdown y retorna el nodo raíz del árbol."""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f if line.strip()]
        
        root = DocumentNode(
            original_name="Fundamentos de Electrónica",
            sanitized_name="fundamentos_electronica",
            level=-1,
            node_id="root"
        )
        
        parent_stack = [root]
        level_stack = [{'type': 'root', 'level': -1}]
        last_header_level = 0
        
        for line in lines:
            stripped_line = line.strip()
            
            # Ignorar líneas vacías y separadores
            if not stripped_line or stripped_line.startswith('---'):
                continue
            
            # Ignorar líneas que son solo metadatos
            if stripped_line.startswith('*') and 'actualización' in stripped_line.lower():
                continue
            
            level_info = {}
            
            # Determinar tipo y nivel
            if stripped_line.startswith('#'):
                level_info['type'] = 'header'
                level_info['level'] = stripped_line.count('#')
                last_header_level = level_info['level']
            elif stripped_line.startswith('-'):
                level_info['type'] = 'list'
                level_info['level'] = last_header_level + 1
            else:
                continue
            
            # Crear nodo
            original_name = TextUtils.clean_name(stripped_line)
            sanitized_name = TextUtils.sanitize_name(original_name)
            
            node = DocumentNode(
                original_name=original_name,
                sanitized_name=sanitized_name,
                level=level_info['level']
            )
            
            # Encontrar padre correcto en la pila
            while level_info['level'] <= level_stack[-1]['level']:
                parent_stack.pop()
                level_stack.pop()
            
            # Añadir como hijo del padre actual
            parent_stack[-1].add_child(node)
            parent_stack.append(node)
            level_stack.append(level_info)
        
        # Post-procesamiento: marcar directorios y generar IDs
        self._post_process(root)
        
        return root
    
    def _post_process(self, root: DocumentNode):
        """Post-procesa el árbol para establecer flags y generar IDs."""
        def process_node(node: DocumentNode):
            # Marcar como directorio si tiene hijos
            if node.children:
                node.is_directory = True
            
            # Generar ID
            node.node_id = TextUtils.generate_id(node)
            
            # Procesar hijos recursivamente
            for child in node.children:
                process_node(child)
        
        process_node(root)


# ============================================================================
# GENERADOR DE ESTRUCTURA
# ============================================================================

class DocumentationBuilder:
    """Construye la estructura completa de documentación."""
    
    def __init__(self, root_node: DocumentNode, target_dir: str):
        self.root = root_node
        self.target_dir = target_dir
        self.all_nodes: Dict[str, DocumentNode] = {}
        
    def build(self, force: bool = False):
        """Construye toda la estructura de documentación."""
        # Limpiar directorio si existe y force=True
        if os.path.exists(self.target_dir):
            if force:
                print(f"🗑️  Eliminando directorio existente: {self.target_dir}")
                shutil.rmtree(self.target_dir)
            else:
                print(f"⚠️  El directorio {self.target_dir} ya existe. Usa --force para sobrescribir.")
                return
        
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Paso 1: Establecer rutas de archivos
        print("📁 Estableciendo rutas...")
        self._set_paths()
        
        # Paso 2: Crear metadatos para todos los nodos
        print("📊 Generando metadatos...")
        self._create_metadata()
        
        # Paso 3: Generar archivos markdown
        print("📝 Generando archivos markdown...")
        self._generate_markdown_files()
        
        # Paso 4: Generar archivos JSON de metadatos
        print("🗂️  Generando metadatos JSON...")
        self._generate_metadata_files()
        
        # Paso 5: Generar índice general
        print("📚 Generando índice general...")
        self._generate_main_index()
        
        print(f"\n✅ Documentación generada en: {self.target_dir}")
        print(f"   Total de nodos: {len(self.all_nodes)}")
    
    def _set_paths(self):
        """Establece las rutas de archivos para todos los nodos."""
        self.root.path = os.path.join(self.target_dir, 'index.md')
        
        for module in self.root.children:
            self._set_node_paths(module, self.target_dir)
    
    def _set_node_paths(self, node: DocumentNode, parent_dir: str):
        """Establece rutas recursivamente."""
        node_dir = parent_dir
        
        if node.is_directory:
            node_dir = os.path.join(parent_dir, node.sanitized_name)
            node.path = os.path.join(node_dir, 'index.md')
        else:
            node.path = os.path.join(parent_dir, f"{node.sanitized_name}.md")
        
        # Guardar nodo en el índice global
        self.all_nodes[node.node_id] = node
        
        # Procesar hijos
        for child in node.children:
            self._set_node_paths(child, node_dir)
    
    def _create_metadata(self):
        """Crea objetos de metadatos para todos los nodos."""
        for node_id, node in self.all_nodes.items():
            # Obtener IDs de hijos
            children_ids = [child.node_id for child in node.children]
            
            # Obtener IDs de navegación (prev/next)
            siblings = node.get_siblings()
            idx = siblings.index(node)
            prev_id = siblings[idx - 1].node_id if idx > 0 else None
            next_id = siblings[idx + 1].node_id if idx < len(siblings) - 1 else None
            
            # Construir breadcrumb
            ancestors = node.get_ancestors()
            breadcrumb = [
                {"id": anc.node_id, "title": anc.original_name}
                for anc in ancestors
            ]
            breadcrumb.append({"id": node.node_id, "title": node.original_name})
            
            # Crear metadatos
            metadata = NodeMetadata(
                id=node.node_id,
                title=node.original_name,
                level=node.level,
                parent_id=node.parent.node_id if node.parent else None,
                children_ids=children_ids,
                md_path=node.path,
                relative_path=os.path.relpath(node.path, self.target_dir),
                python_refs=[ref.to_dict() for ref in node.python_functions],
                prev_id=prev_id,
                next_id=next_id,
                breadcrumb=breadcrumb
            )
            
            node.metadata = metadata
    
    def generate_preview(self) -> Dict[str, Any]:
        """Genera una vista previa JSON de lo que se creará (sin crear archivos)."""
        # Preparar nodos
        self._set_node_paths(self.root, self.target_dir)
        self._create_metadata()
        
        preview = {
            "metadata": {
                "source": Config.SOURCE_MD,
                "target_dir": Config.TARGET_DIR,
                "catalog_path": Config.CATALOG_JSON,
                "timestamp": "2026-01-22"
            },
            "summary": {
                "total_directories": 0,
                "total_markdown_files": 0,
                "total_metadata_files": 0,
                "total_python_refs": 0
            },
            "structure": []
        }
        
        # Contar y construir estructura
        def build_node_preview(node: DocumentNode) -> Dict[str, Any]:
            """Construye vista previa recursiva de un nodo."""
            node_preview = {
                "id": node.node_id,
                "title": node.original_name,
                "level": node.level,
                "type": "directory" if node.is_directory else "file"
            }
            
            # Información de rutas
            if node.metadata:
                node_preview["paths"] = {
                    "markdown": node.path,
                    "metadata": os.path.join(os.path.dirname(node.path), Config.METADATA_FILENAME),
                    "relative": node.metadata.relative_path
                }
                
                # Navegación
                node_preview["navigation"] = {
                    "parent_id": node.metadata.parent_id,
                    "prev_id": node.metadata.prev_id,
                    "next_id": node.metadata.next_id,
                    "breadcrumb": node.metadata.breadcrumb
                }
                
                # Referencias Python
                if node.python_functions:
                    node_preview["python_refs"] = [ref.to_dict() for ref in node.python_functions]
                    preview["summary"]["total_python_refs"] += len(node.python_functions)
            
            # Actualizar contadores
            if node.is_directory:
                preview["summary"]["total_directories"] += 1
            else:
                preview["summary"]["total_markdown_files"] += 1
                preview["summary"]["total_metadata_files"] += 1  # Un metadata.json por directorio
            
            # Procesar hijos
            if node.children:
                node_preview["children"] = [build_node_preview(child) for child in node.children]
            
            return node_preview
        
        # Construir estructura desde la raíz
        preview["structure"] = [build_node_preview(child) for child in self.root.children]
        
        return preview
    
    def _generate_markdown_files(self):
        """Genera todos los archivos markdown."""
        # BFS para generar por niveles
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            # Crear directorio si es necesario
            file_dir = os.path.dirname(node.path)
            os.makedirs(file_dir, exist_ok=True)
            
            # Generar contenido
            content = self._generate_node_content(node)
            
            # Escribir archivo
            with open(node.path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ {node.path}")
            
            # Añadir hijos a la cola
            for child in node.children:
                queue.append(child)
    
    def _generate_node_content(self, node: DocumentNode) -> str:
        """Genera el contenido markdown para un nodo."""
        lines = []
        
        # Título
        lines.append(f"# {node.original_name}\n")
        
        # Breadcrumb y navegación
        nav_links = self._generate_navigation_links(node)
        if nav_links:
            lines.append(nav_links)
            lines.append("\n---\n")
        
        # ID del nodo
        lines.append(f"**ID:** `{node.node_id}`\n")
        
        # Contenido principal
        if node.is_directory and node.children:
            lines.append("## 📑 Contenido\n")
            for child in node.children:
                rel_link = self._get_relative_link(child.path, os.path.dirname(node.path))
                icon = "📁" if child.is_directory else "📄"
                lines.append(f"- {icon} [{child.original_name}]({rel_link})")
            lines.append("")
        else:
            # Nodo hoja: añadir stub de contenido
            python_funcs_md = self._generate_python_functions_md(node)
            stub = Config.STUB_CONTENT.format(python_functions=python_funcs_md)
            lines.append(stub)
        
        return "\n".join(lines)
    
    def _generate_navigation_links(self, node: DocumentNode) -> str:
        """Genera los enlaces de navegación para un nodo."""
        if not node.metadata:
            return ""
        
        links = []
        file_dir = os.path.dirname(node.path)
        
        # Breadcrumb
        breadcrumb_parts = []
        for item in node.metadata.breadcrumb[:-1]:  # Excluir el nodo actual
            target_node = self.all_nodes.get(item['id'])
            if target_node:
                rel_link = self._get_relative_link(target_node.path, file_dir)
                breadcrumb_parts.append(f"[{item['title']}]({rel_link})")
        
        if breadcrumb_parts:
            links.append("**Ruta:** " + " > ".join(breadcrumb_parts))
        
        # Navegación anterior/siguiente
        nav_parts = []
        if node.metadata.prev_id:
            prev_node = self.all_nodes.get(node.metadata.prev_id)
            if prev_node:
                rel_link = self._get_relative_link(prev_node.path, file_dir)
                nav_parts.append(f"[⬅️ Anterior]({rel_link})")
        
        if node.metadata.next_id:
            next_node = self.all_nodes.get(node.metadata.next_id)
            if next_node:
                rel_link = self._get_relative_link(next_node.path, file_dir)
                nav_parts.append(f"[Siguiente ➡️]({rel_link})")
        
        if nav_parts:
            links.append(" | ".join(nav_parts))
        
        return "\n".join(links) if links else ""
    
    def _generate_python_functions_md(self, node: DocumentNode) -> str:
        """Genera el markdown de las funciones Python asociadas."""
        if not node.python_functions:
            return "*No hay funciones Python asociadas aún*"
        
        lines = []
        for func in node.python_functions:
            status_icon = "✅" if func.implemented else "⚠️"
            lines.append(f"- {status_icon} `{func.full_path}`")
            if func.description:
                lines.append(f"  - {func.description}")
        
        return "\n".join(lines)
    
    def _generate_metadata_files(self):
        """Genera archivos JSON de metadatos para cada directorio."""
        # Agrupar nodos por directorio
        directories = {}
        for node in self.all_nodes.values():
            dir_path = os.path.dirname(node.path)
            if dir_path not in directories:
                directories[dir_path] = []
            directories[dir_path].append(node)
        
        # Generar metadata.json para cada directorio
        for dir_path, nodes in directories.items():
            metadata_path = os.path.join(dir_path, Config.METADATA_FILENAME)
            
            metadata_content = {
                "directory": os.path.relpath(dir_path, self.target_dir),
                "nodes": [node.metadata.to_dict() for node in nodes if node.metadata]
            }
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_content, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ {metadata_path}")
    
    def _generate_main_index(self):
        """Genera el índice principal en la raíz."""
        index_path = os.path.join(self.target_dir, 'index.md')
        
        lines = [
            f"# {self.root.original_name}\n",
            "*Documentación generada automáticamente*\n",
            "---\n",
            "## 📚 Módulos Principales\n"
        ]
        
        for module in self.root.children:
            rel_link = self._get_relative_link(module.path, self.target_dir)
            icon = "📦"
            lines.append(f"- {icon} [{module.original_name}]({rel_link})")
        
        lines.append("\n---")
        lines.append(f"\n*Total de temas: {len(self.all_nodes)}*")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
    
    @staticmethod
    def _get_relative_link(target_path: str, from_dir: str) -> str:
        """Calcula el enlace relativo desde from_dir hasta target_path."""
        return os.path.relpath(target_path, from_dir).replace(os.sep, '/')


# ============================================================================
# ACTUALIZADOR DE CATÁLOGO
# ============================================================================

class CatalogUpdater:
    """Actualiza el archivo temario_catalogado.json con las referencias generadas."""
    
    def __init__(self, catalog_path: str, all_nodes: Dict[str, DocumentNode]):
        self.catalog_path = catalog_path
        self.all_nodes = all_nodes
    
    def update(self):
        """Actualiza el catálogo con la información de los nodos."""
        # Cargar catálogo existente si existe
        if os.path.exists(self.catalog_path):
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
        else:
            catalog = {
                "temario_fe": {
                    "titulo": "Fundamentos de Electrónica - Catálogo de Temas",
                    "version": "4.0",
                    "fecha_actualización": "2026-01-22",
                    "items": []
                }
            }
        
        # Actualizar items
        items = []
        for node_id, node in sorted(self.all_nodes.items(), key=lambda x: x[0]):
            if node.node_id == "root":
                continue
            
            item = {
                "id": node.node_id,
                "titulo": node.original_name,
                "nivel": node.level,
                "parent_id": node.parent.node_id if node.parent and node.parent.node_id != "root" else None,
                "md_path": node.metadata.relative_path if node.metadata else "",
                "python_refs": [ref.to_dict() for ref in node.python_functions],
                "status": node.metadata.status if node.metadata else "pending"
            }
            items.append(item)
        
        catalog["temario_fe"]["items"] = items
        catalog["temario_fe"]["estadísticas"] = {
            "total_items": len(items)
        }
        
        # Guardar catálogo actualizado
        os.makedirs(os.path.dirname(self.catalog_path), exist_ok=True)
        with open(self.catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Catálogo actualizado: {self.catalog_path}")
        print(f"   Total de items: {len(items)}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Construye la estructura de documentación desde CONTENIDOS_FE.md"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Muestra lo que se haría sin ejecutar"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Sobrescribe el directorio de destino si existe"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚀 ElectroCore - Generador de Documentación")
    print("=" * 70)
    
    # Verificar que el archivo fuente existe
    if not os.path.exists(Config.SOURCE_MD):
        print(f"❌ Error: No se encuentra el archivo {Config.SOURCE_MD}")
        return 1
    
    # Parsear el markdown
    print(f"\n📖 Parseando: {Config.SOURCE_MD}")
    parser = MarkdownParser(Config.SOURCE_MD)
    root_node = parser.parse()
    print(f"✓ Árbol parseado: {len(root_node.children)} módulos principales")
    
    if args.dry_run:
        print("\n⚠️  Modo DRY-RUN: No se crearán archivos")
        print(f"   Se generarían archivos en: {Config.TARGET_DIR}")
        
        # Generar vista previa JSON detallada
        builder = DocumentationBuilder(root_node, Config.TARGET_DIR)
        preview = builder.generate_preview()
        
        output_file = "docs/build_preview.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(preview, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Vista previa generada: {output_file}")
        print(f"\n📊 Resumen:")
        print(f"   - Directorios: {preview['summary']['total_directories']}")
        print(f"   - Archivos markdown: {preview['summary']['total_markdown_files']}")
        print(f"   - Archivos metadata: {preview['summary']['total_metadata_files']}")
        print(f"   - Referencias Python: {preview['summary']['total_python_refs']}")
        
        return 0
    
    # Construir documentación
    builder = DocumentationBuilder(root_node, Config.TARGET_DIR)
    builder.build(force=args.force)
    
    # Actualizar catálogo
    print(f"\n📊 Actualizando catálogo...")
    updater = CatalogUpdater(Config.CATALOG_JSON, builder.all_nodes)
    updater.update()
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"\n📂 Explora la documentación en: {Config.TARGET_DIR}")
    print(f"📄 Revisa el catálogo en: {Config.CATALOG_JSON}")
    
    return 0


if __name__ == '__main__':
    exit(main())
