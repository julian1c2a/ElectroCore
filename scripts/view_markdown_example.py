#!/usr/bin/env python3
"""
Script para ver un ejemplo de archivo markdown generado
"""
from pathlib import Path


def main():
    # Ejemplo: un archivo de hoja (topic)
    example_file = Path(
        "docs/temario/fundamentos_de_electronica/"
        "modulo_6_fundamentos_de_electronica_digital/"
        "sistemas_de_representacion_de_la_informacion/"
        "sistemas_de_numeracion/"
        "conversion_entre_sistemas_de_numeracion_numeros_naturales/"
        "conversion_de_base_10_a_base_b_divisiones_sucesivas.md"
    )
    
    print("=" * 70)
    print("📄 Ejemplo de Archivo Markdown Generado")
    print("=" * 70)
    print(f"\n📍 Archivo: {example_file}\n")
    
    if not example_file.exists():
        print(f"❌ El archivo no existe: {example_file}")
        print("   Ejecuta primero: python scripts/build_documentation_tree.py")
        return
    
    print("-" * 70)
    with open(example_file, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
    print("-" * 70)
    
    # Mostrar también el index del directorio padre
    parent_index = example_file.parent / "index.md"
    
    if parent_index.exists():
        print(f"\n📍 Index del directorio padre: {parent_index}\n")
        print("-" * 70)
        with open(parent_index, "r", encoding="utf-8") as f:
            content = f.read()
            # Mostrar solo las primeras 30 líneas
            lines = content.split('\n')
            for line in lines[:30]:
                print(line)
            if len(lines) > 30:
                print(f"\n... y {len(lines)-30} líneas más")
        print("-" * 70)


if __name__ == "__main__":
    main()
