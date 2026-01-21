import os
import pathlib
from typing import Callable

class LatexAssetManager:
    def __init__(self, base_build_path="build/latex"):
        self.base_path = base_build_path
        self.components_path = os.path.join(base_build_path, "components")
        
        # Usar ruta absoluta basada en la ubicación de este archivo
        # Este archivo está en: renderers/latex/utils/asset_manager.py
        # Raíz del proyecto: ../../../
        current_dir = pathlib.Path(__file__).parent.absolute()
        project_root = current_dir.parent.parent.parent
        self.resources_path = project_root / "resources" / "latex"
        
        # Asegurar que existe el directorio de componentes generados
        os.makedirs(self.components_path, exist_ok=True)

    def get_component(self, name_id: str, content_generator_func: Callable[[], str]) -> str:
        r"""
        Gestiona un componente LaTeX (ej: un diagrama TikZ).
        """
        
        # Nombre del archivo esperado
        filename = f"{name_id}.tex"
        
        # 1. Chequear recurso fijo (Fixed)
        fixed_file_path = self.resources_path / filename
        
        # DEBUG
        # print(f"🔍 Buscando: {fixed_file_path}")
        
        if fixed_file_path.exists():
            print(f"✨ Recurso fijo encontrado: {filename}")
            # Ruta relativa para el \input desde el archivo Examen_Final.tex (que está en build/latex/)
            # Necesitamos subir 2 niveles (../../) para salir de build/latex/ y entrar a resources/latex/
            # Usamos forward slashes para LaTeX
            relative_input_path = f"../../resources/latex/{filename}"
            
            return fr"% [RECURSO FIJO DETECTADO: {filename}]" + "\n" + fr"\input{{{relative_input_path}}}" + "\n"

        # 2. Generar borrador (Draft)
        content = content_generator_func()
        
        header = f"% --- COMPONENTE GENERADO: {name_id} ---\n"
        header += f"% ID: {name_id}\n"
        header += f"% Si quieres fijar este diseño, copia este archivo a 'resources/latex/{filename}' y edítalo.\n"
        
        full_content = header + content
        
        draft_path = os.path.join(self.components_path, filename)
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        return fr"\input{{components/{filename}}}" + "\n"
