import os
import re
import unicodedata
import shutil
from collections import deque

class Node:
    """Represents a node in the documentation tree."""
    def __init__(self, name, level, parent=None):
        self.original_name = self._clean_name(name)
        self.sanitized_name = self._sanitize(self.original_name)
        self.level = level
        self.parent = parent
        self.children = []
        self.path = ""
        self.is_directory = False
        self.status = 'pending'

    def _clean_name(self, name):
        return re.sub(r'^\s*#+\s*|\s*-\s*', '', name).strip()

    def _sanitize(self, name):
        if not name: return "unnamed"
        s = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
        s = s.lower()
        s = re.sub(r'[\s./:()]+', '_', s)
        s = re.sub(r'[^a-z0-9_]', '', s)
        s = re.sub(r'^\d+(_\d+)*_?', '', s).strip('_')
        s = re.sub(r'_+', '_', s)
        return s.strip('_') or "unnamed"

def parse_markdown_to_tree(source_file):
    """Parses a markdown file and builds a hierarchical tree of Nodes."""
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f if line.strip()]

    root = Node("Temario Principal", -1)
    parent_stack = [root]
    level_stack = [{'type': 'root', 'level': -1}] 

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line: continue

        level_info = {}
        if stripped_line.startswith('#'):
            level_info['type'] = 'header'
            level_info['level'] = stripped_line.count('#')
        elif stripped_line.startswith('-'):
            level_info['type'] = 'list'
            level_info['level'] = len(line) - len(line.lstrip(' ')) # Assuming 4 spaces for indentation level
        else:
            continue

        node = Node(stripped_line, level_info['level'])
        
        # Find correct parent in stack
        while level_info['level'] <= level_stack[-1]['level']:
            # Exception for list items under headers
            if level_info['type'] == 'list' and level_stack[-1]['type'] == 'header':
                 if level_info['level'] > level_stack[-1]['level']: # list is child of header
                    break
            parent_stack.pop()
            level_stack.pop()

        parent_stack[-1].add_child(node)
        node.parent = parent_stack[-1]
        parent_stack.append(node)
        level_stack.append(level_info)

    # Post-process to set is_directory flag
    def set_directory_flag(node):
        if node.children: node.is_directory = True
        for child in node.children:
            set_directory_flag(child)
    
    set_directory_flag(root)
    return root

def set_node_paths(node, parent_dir):
    """Recursively traverses the tree to set the .path attribute for every node."""
    if node.is_directory:
        node_dir = os.path.join(parent_dir, node.sanitized_name)
        node.path = os.path.join(node_dir, 'index.md')
        for child in node.children:
            set_node_paths(child, node_dir)
    else:
        node.path = os.path.join(parent_dir, f"{node.sanitized_name}.md")
        # Leaf node, no children to recurse into

def generate_docs_from_tree(base_dir, root_node):
    """
    Generates documentation by first setting all paths, then writing all files.
    """
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # 1. First Pass: Set all node paths
    root_node.path = os.path.join(base_dir, 'index.md')
    for module in root_node.children:
        set_node_paths(module, base_dir)

    # 2. Second Pass: Generate all files
    def get_relative_link(target_path, from_dir):
        return os.path.relpath(target_path, from_dir).replace(os.sep, '/')

    def generate_files_recursively(node):
        # Create directory for the file if it doesn't exist
        file_dir = os.path.dirname(node.path)
        os.makedirs(file_dir, exist_ok=True)
        
        # --- Generate Content ---
        content = [f"# {node.original_name}\n"]
        
        # Nav links
        links = []
        if node.parent and node.parent.path:
            links.append(f"[Volver a {node.parent.original_name}]({get_relative_link(node.parent.path, file_dir)})")
        if node.parent:
            siblings = node.parent.children
            try:
                idx = siblings.index(node)
                if idx > 0:
                    prev_s = siblings[idx - 1]
                    links.append(f"[< Anterior: {prev_s.original_name}]({get_relative_link(prev_s.path, file_dir)})")
                if idx < len(siblings) - 1:
                    next_s = siblings[idx + 1]
                    links.append(f"[Siguiente: {next_s.original_name} >]({get_relative_link(next_s.path, file_dir)})")
            except ValueError: pass
        
        if links:
            content.append(" | ".join(links) + "\n\n---")

        # Child links (Table of Contents)
        if node.is_directory and node.children:
            content.append("\n## Contenido\n")
            for child in node.children:
                content.append(f"- [{child.original_name}]({get_relative_link(child.path, file_dir)})")
        
        # --- Write File ---
        with open(node.path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        node.status = 'written'

        # Recurse
        for child in node.children:
            generate_files_recursively(child)
    
    # Generate root index.md, then kick off recursion for the rest
    with open(root_node.path, 'w', encoding='utf-8') as f:
        f.write(f"# {root_node.original_name}\n\n## Módulos\n")
        for module in root_node.children:
            link = get_relative_link(module.path, base_dir)
            f.write(f"- [{module.original_name}]({link})\n")
    root_node.status = 'written'


    for module in root_node.children:
        generate_files_recursively(module)


if __name__ == '__main__':
    SOURCE_MD = 'docs/CONTENIDOS_FE.md'
    TARGET_DIR = 'docs/temario'
    
    print(f"Iniciando la re-generación de la estructura desde '{SOURCE_MD}' en '{TARGET_DIR}'...")
    doc_tree = parse_markdown_to_tree(SOURCE_MD)
    generate_docs_from_tree(TARGET_DIR, doc_tree)
    print(f"Proceso completado. Revisa la carpeta '{TARGET_DIR}'.")