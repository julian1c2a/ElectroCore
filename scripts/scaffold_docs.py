import os
import re
import shutil
import unicodedata

def sanitize_name(name):
    """Sanitizes a string to be used as a file or directory name."""
    # Get the original name for use in the file's H1 title
    original_name = re.sub(r'^\s*#+\s*|\s*-\s*(\[.*?\]\s*)?|\s*\*\s*', '', name).strip()
    original_name = re.sub(r'\*\*(.*?)\*\*', r'\1', original_name)

    # --- Sanitization for filesystem path ---
    sanitized = original_name
    sanitized = ''.join(c for c in unicodedata.normalize('NFD', sanitized) if unicodedata.category(c) != 'Mn')
    sanitized = sanitized.lower()
    sanitized = re.sub(r'[\s./-]+', '_', sanitized)
    sanitized = re.sub(r'[^a-z0-9_]', '', sanitized)
    # Remove leading numbering from the outline
    sanitized = re.sub(r'^\d+(_\d+)*_?', '', sanitized).strip('_')
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    return sanitized, original_name

def create_structure_from_markdown(source_file, base_dir):
    """Creates or updates a directory and file structure from a markdown file non-destructively."""
    # Ensure the base directory exists, but do not clean it.
    os.makedirs(base_dir, exist_ok=True)
    print(f"Directorio base '{base_dir}' asegurado. Se crearán solo archivos y directorios faltantes.")

    with open(source_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]

    header_path_stack = [base_dir]
    list_path_stack = []
    list_indent_stack = [-1]
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith('#'):
            header_level = stripped_line.count('#')
            name, _ = sanitize_name(stripped_line)
            if not name:
                continue

            while len(header_path_stack) > header_level:
                header_path_stack.pop()
            
            parent_dir = os.path.join(*header_path_stack)
            current_path = os.path.join(parent_dir, name)
            os.makedirs(current_path, exist_ok=True)
            
            # THE FIX IS HERE: Append only the name component, not the full path
            header_path_stack.append(name)

            list_path_stack = []
            list_indent_stack = [-1]
            continue

        if stripped_line.startswith('-'):
            indent = len(line) - len(line.lstrip(' '))
            name, original_name = sanitize_name(stripped_line)
            if not name:
                continue
            
            while indent <= list_indent_stack[-1]:
                if list_path_stack:
                    list_path_stack.pop()
                list_indent_stack.pop()

            # Unify path construction to avoid joining already joined paths
            parent_path = os.path.join(*header_path_stack, *list_path_stack)

            is_directory = False
            if i + 1 < len(lines):
                next_line = lines[i+1]
                if next_line.strip().startswith('-'):
                    next_indent = len(next_line) - len(next_line.lstrip(' '))
                    if next_indent > indent:
                        is_directory = True
            
            if is_directory:
                new_dir_path = os.path.join(parent_path, name)
                os.makedirs(new_dir_path, exist_ok=True)
                list_path_stack.append(name)
                list_indent_stack.append(indent)
            else:
                md_file_path = os.path.join(parent_path, f"{name}.md")
                if not os.path.exists(md_file_path):
                    with open(md_file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {original_name}\n\n")

if __name__ == '__main__':
    SOURCE_MD = 'docs/CONTENIDOS_FE.md'
    TARGET_DIR = 'docs/temario'
    print(f"Iniciando la creación de la estructura desde '{SOURCE_MD}' en '{TARGET_DIR}'...")
    create_structure_from_markdown(SOURCE_MD, TARGET_DIR)
    print("Proceso completado. Revisa la carpeta 'docs/temario'.")