#!/usr/bin/env python3
"""
Script para ver ejemplos de metadata JSON generados
"""
import json
from pathlib import Path


def print_metadata(filepath: Path, title: str):
    """Imprime metadata de forma formateada"""
    print(f"\n📍 {title}")
    print(f"   Archivo: {filepath}")
    print("-" * 70)
    
    if not filepath.exists():
        print(f"❌ El archivo no existe")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print("-" * 70)


def main():
    print("=" * 70)
    print("🗂️  Ejemplos de Metadata JSON")
    print("=" * 70)
    
    # Ejemplo 1: Metadata de un nodo raíz
    root_metadata = Path("docs/temario/fundamentos_de_electronica/metadata.json")
    print_metadata(root_metadata, "1. Metadata de Nodo Raíz (Fundamentos de Electrónica)")
    
    # Ejemplo 2: Metadata de un módulo
    module_metadata = Path(
        "docs/temario/fundamentos_de_electronica/"
        "modulo_6_fundamentos_de_electronica_digital/"
        "metadata.json"
    )
    print_metadata(module_metadata, "2. Metadata de Módulo (Electrónica Digital)")
    
    # Ejemplo 3: Metadata de una sección
    section_metadata = Path(
        "docs/temario/fundamentos_de_electronica/"
        "modulo_6_fundamentos_de_electronica_digital/"
        "sistemas_de_representacion_de_la_informacion/"
        "sistemas_de_numeracion/"
        "conversion_entre_sistemas_de_numeracion_numeros_naturales/"
        "metadata.json"
    )
    print_metadata(section_metadata, "3. Metadata de Sección (Conversión entre sistemas)")
    
    print("\n" + "=" * 70)
    print("✅ Ejemplos completados")
    print("=" * 70)


if __name__ == "__main__":
    main()
