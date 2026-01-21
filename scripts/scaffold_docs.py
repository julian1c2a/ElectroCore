import os
import re
import unicodedata
from collections import OrderedDict

def sanitize_name(name):
    """Sanitizes a string to be used as a file or directory name and gets the original name."""
    original_name = re.sub(r'^\s*#+\s*|\s*-\s*(\[.*?\]\s*)?|\s*\*\s*', '', name).strip()
    original_name = re.sub(r'\*\*(.*?)\*\*', r'\1', original_name)

    sanitized = ''.join(c for c in unicodedata.normalize('NFD', original_name) if unicodedata.category(c) != 'Mn')
    sanitized = sanitized.lower()
    sanitized = re.sub(r'[\s./-]+', '_', sanitized)
    sanitized = re.sub(r'[^a-z0-9_]', '', sanitized)
    sanitized = re.sub(r'^\d+(_\d+)*_?', '', sanitized).strip('_')
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_'), original_name

def create_structure_with_links(source_file, base_dir):
    """Creates a linked directory and file structure from a markdown file."""
    if os.path.exists(base_dir):
        # A more targeted clean could be implemented if needed
        # For now, let's start fresh to ensure link integrity
        pass # Not cleaning for now, just creating missing files.
    os.makedirs(base_dir, exist_ok=True)
    print(f"Directorio base '{base_dir}' asegurado.")

    with open(source_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]

    # --- Pass 1: Build a complete map of the structure ---
    structure_map = OrderedDict()
    path_stack = []
    indent_stack = [-1]
    all_nodes = []

    # Add root node
    root_sanitized, root_original = sanitize_name(lines[0])
    root_path = root_sanitized
    structure_map[root_path] = {'original_name': root_original, 'children': [], 'parent': None, 'level': 0}
    path_stack.append(root_path)
    all_nodes.append(root_path)


    for i, line in enumerate(lines[1:]): # Skip H1 title
        stripped_line = line.strip()
        indent = len(line) - len(line.lstrip(' '))
        
        if stripped_line.startswith('#'): # Headers reset the path
            level = stripped_line.count('#')
            path_stack = path_stack[:level]
            indent_stack = [-1]
            continue

        if stripped_line.startswith('-'):
            name, original_name = sanitize_name(stripped_line)
            if not name:
                continue

            while indent <= indent_stack[-1]:
                path_stack.pop()
                indent_stack.pop()
            
            parent_path = "/".join(path_stack)
            current_path = f"{parent_path}/{name}"

            # Determine if it's a directory (has children)
            is_directory = False
            if (i + 2) < len(lines):
                next_line = lines[i+2]
                if next_line.strip().startswith('-'):
                    next_indent = len(next_line) - len(next_line.lstrip(' '))
                    if next_indent > indent:
                        is_directory = True

            structure_map[parent_path]['children'].append({
                'path': current_path, 'original_name': original_name, 'is_directory': is_directory
            })

            if is_directory:
                structure_map[current_path] = {'original_name': original_name, 'children': [], 'parent': parent_path, 'level': len(path_stack)}
                path_stack.append(name)
                indent_stack.append(indent)
            
            all_nodes.append(current_path)

    # --- Pass 2: Generate files and inject links ---
    for i, path in enumerate(all_nodes):
        node = structure_map.get(path)
        is_directory = node is not None

        # Determine siblings
        parent_node = structure_map.get(node['parent']) if node else None
        siblings = parent_node['children'] if parent_node else structure_map[root_path]['children']
        
        sibling_paths = [s['path'] for s in siblings]
        try:
            current_index_in_siblings = sibling_paths.index(path)
            prev_sibling_path = sibling_paths[current_index_in_siblings - 1] if current_index_in_siblings > 0 else None
            next_sibling_path = sibling_paths[current_index_in_siblings + 1] if current_index_in_siblings < len(siblings) - 1 else None
        except ValueError: # path is not in siblings list (it's the root or an error)
            current_index_in_siblings = -1
            prev_sibling_path = None
            next_sibling_path = None

        # Create path on filesystem
        fs_path = os.path.join(base_dir, *path.split('/'))
        
        content = []
        if is_directory:
            os.makedirs(fs_path, exist_ok=True)
            file_path = os.path.join(fs_path, 'index.md')
            original_name = node['original_name']
            children = node['children']
            parent_path = node['parent']
        else: # It's a file from the perspective of the parent
            file_path = f"{fs_path}.md"
            # Get info from parent
            parent_path_str = "/".join(path.split('/')[:-1])
            parent_node = structure_map[parent_path_str]
            child_info = next(c for c in parent_node['children'] if c['path'] == path)
            original_name = child_info['original_name']
            children = [] # Files have no children
            parent_path = parent_path_str
        
        # Build Content
        content.append(f"# {original_name}\n")

        # Navigation
        nav_links = []
        if parent_path:
            # Relative path from current file to parent's index.md
            relative_parent_path = os.path.join('..', 'index.md')
            nav_links.append(f"[Subir a {structure_map[parent_path]['original_name']}]({relative_parent_path})")

        if prev_sibling_path:
            # Relative path to previous sibling
            is_dir = structure_map.get(prev_sibling_path) is not None
            rel_path = os.path.join('..', os.path.basename(prev_sibling_path), 'index.md' if is_dir else '')
            if not is_dir:
                rel_path = f"../{os.path.basename(prev_sibling_path)}.md"

            nav_links.append(f"[< Anterior: {structure_map.get(prev_sibling_path, {}).get('original_name', os.path.basename(prev_sibling_path))}]({rel_path})")

        if next_sibling_path:
            is_dir = structure_map.get(next_sibling_path) is not None
            rel_path = os.path.join('..', os.path.basename(next_sibling_path), 'index.md' if is_dir else '')
            if not is_dir:
                rel_path = f"../{os.path.basename(next_sibling_path)}.md"

            nav_links.append(f"[Siguiente: {structure_map.get(next_sibling_path, {}).get('original_name', os.path.basename(next_sibling_path))} >]({rel_path})")
            
        if nav_links:
            content.append(" | ".join(nav_links))
            content.append("\n---")

        # Children / Table of Contents
        if children:
            content.append("\n## Contenido\n")
            for child in children:
                child_name = os.path.basename(child['path'])
                link_path = f"./{child_name}/index.md" if child['is_directory'] else f"./{child_name}.md"
                content.append(f"- [{child['original_name']}]({link_path})")
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))


if __name__ == '__main__':
    SOURCE_MD = 'docs/CONTENIDOS_FE.md'
    TARGET_DIR = 'docs/temario'
    print(f"Iniciando la creación de la estructura desde '{SOURCE_MD}' en '{TARGET_DIR}'...")
    # For safety, remove old dir. A more robust merge could be implemented.
    # import shutil
    # if os.path.exists(TARGET_DIR):
    #     shutil.rmtree(TARGET_DIR)
    create_structure_with_links(SOURCE_MD, TARGET_DIR)
    print("Proceso completado con hipervínculos. Revisa la carpeta 'docs/temario'.")
