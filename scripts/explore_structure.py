#!/usr/bin/env python3
"""
Script para explorar la estructura de directorios generada por build_documentation_tree.py
"""
import os
from pathlib import Path


def main():
    base = Path("docs/temario")
    
    if not base.exists():
        print(f"❌ El directorio {base} no existe")
        print("   Ejecuta primero: python scripts/build_documentation_tree.py")
        return
    
    print("=" * 70)
    print("📂 Estructura de Documentación Generada")
    print("=" * 70)
    print()
    
    total_dirs = 0
    total_files = 0
    
    for root, dirs, files in os.walk(base):
        level = root.replace(str(base), '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        
        if level == 0:
            print(f"{indent}📁 {folder_name}/")
        else:
            print(f"{indent}├─ 📁 {folder_name}/")
        
        total_dirs += 1
        
        subindent = '  ' * (level + 1)
        
        # Mostrar archivos
        md_files = [f for f in files if f.endswith('.md')]
        json_files = [f for f in files if f.endswith('.json')]
        
        for i, file in enumerate(sorted(md_files)[:2]):  # Primeros 2 MD
            total_files += 1
            print(f"{subindent}│  📄 {file}")
        
        if len(md_files) > 2:
            print(f"{subindent}│  ... y {len(md_files)-2} archivos .md más")
            total_files += len(md_files) - 2
        
        for i, file in enumerate(sorted(json_files)[:1]):  # Primer JSON
            total_files += 1
            print(f"{subindent}│  🗂️  {file}")
        
        if len(json_files) > 1:
            print(f"{subindent}│  ... y {len(json_files)-1} archivos .json más")
            total_files += len(json_files) - 1
        
        # Límite de profundidad para visualización
        if level >= 3:
            # No mostrar subdirectorios profundos
            dirs.clear()
    
    print()
    print("=" * 70)
    print(f"📊 Resumen:")
    print(f"   - Total directorios: {total_dirs}")
    print(f"   - Total archivos: {total_files}")
    print("=" * 70)


if __name__ == "__main__":
    main()
