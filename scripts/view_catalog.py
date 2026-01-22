#!/usr/bin/env python3
"""
Script para explorar el catálogo generado (temario_catalogado.json)
"""
import json
from pathlib import Path
from collections import Counter


def main():
    catalog_file = Path("config/temario_catalogado.json")
    
    print("=" * 70)
    print("📚 Catálogo de Documentación")
    print("=" * 70)
    
    if not catalog_file.exists():
        print(f"\n❌ El archivo no existe: {catalog_file}")
        print("   Ejecuta primero: python scripts/build_documentation_tree.py")
        return
    
    with open(catalog_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extraer la lista de items desde la estructura anidada
    catalog = data.get('temario_fe', {}).get('items', [])
    
    # Estadísticas
    print(f"\n📊 Estadísticas Generales:")
    print(f"   - Total de items: {len(catalog)}")
    
    # Inferir tipo basado en nivel (los items no tienen campo 'tipo')
    def get_tipo(item):
        nivel = item['nivel']
        if nivel == 1:
            return 'root'
        elif nivel == 2:
            return 'module'
        elif nivel == 3:
            return 'section'
        else:
            return 'topic'
    
    # Contar por tipo inferido
    types = Counter(get_tipo(item) for item in catalog)
    print(f"\n📋 Distribución por tipo (inferido del nivel):")
    for tipo, count in types.items():
        print(f"   - {tipo}: {count}")
    
    # Contar por nivel
    levels = Counter(item['nivel'] for item in catalog)
    print(f"\n🏗️  Distribución por nivel:")
    for level in sorted(levels.keys()):
        print(f"   - Nivel {level}: {levels[level]} nodos")
    
    # Mostrar primeros 10 items
    print(f"\n📄 Primeros 10 items del catálogo:")
    print("-" * 70)
    
    for i, item in enumerate(catalog[:10], 1):
        print(f"\n{i}. {item['titulo']}")
        print(f"   ID: {item['id']}")
        print(f"   Nivel: {item['nivel']}")
        print(f"   Markdown: {item['md_path']}")
        if item.get('python_refs') and len(item['python_refs']) > 0:
            print(f"   Funciones Python: {', '.join(item['python_refs'])}")
    
    print("\n" + "-" * 70)
    
    # Buscar items con funciones Python vinculadas
    items_with_functions = [item for item in catalog if item.get('python_refs') and len(item['python_refs']) > 0]
    
    if items_with_functions:
        print(f"\n🔗 Items con funciones Python vinculadas: {len(items_with_functions)}")
        for item in items_with_functions[:5]:
            print(f"   - {item['titulo']}: {', '.join(item['python_refs'])}")
    else:
        print(f"\n⚠️  Ningún item tiene funciones Python vinculadas aún")
        print("   Usa: python scripts/link_python_functions.py")
    
    # Mostrar estructura jerárquica (primeros módulos)
    print(f"\n🌳 Estructura Jerárquica (primeros módulos):")
    print("-" * 70)
    
    def print_tree(items, parent_id=None, level=0, max_level=2, printed_count=[0]):
        if level > max_level or printed_count[0] >= 20:
            return
        
        children = [item for item in items if item.get('parent_id') == parent_id]
        
        for child in children:
            indent = "  " * level
            nivel = child['nivel']
            icon = "📁" if nivel <= 3 else "📄"
            print(f"{indent}{icon} {child['titulo']}")
            printed_count[0] += 1
            
            if printed_count[0] >= 20:
                print(f"{indent}   ... (mostrando solo primeros 20)")
                return
            
            print_tree(items, child['id'], level + 1, max_level, printed_count)
    
    print_tree(catalog)
    
    print("\n" + "=" * 70)
    print("✅ Exploración completada")
    print(f"📂 Catálogo completo en: {catalog_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
