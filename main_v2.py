import os
import argparse
from core.exam_builder import ExamBuilder
from renderers.latex.main_renderer import LatexExamRenderer

def main():
    # Configuración por defecto para pruebas
    default_config = os.path.join("config", "test_exam.json")
    
    print("🚀 Iniciando Generador de Exámenes V2...")
    
    # 1. Construcción
    try:
        builder = ExamBuilder(default_config)
        exercises = builder.build()
    except Exception as e:
        print(f"❌ Error al construir el examen: {e}")
        return
    
    if not exercises:
        print("❌ No se generaron ejercicios. Revisa la configuración.")
        return

    output_dir = os.path.join("build", "latex")
    os.makedirs(output_dir, exist_ok=True)

    # 2. Renderizado EXAMEN (Enunciado)
    print("🎨 Renderizando Examen (Enunciado)...")
    try:
        renderer_exam = LatexExamRenderer(is_solution=False)
        latex_code = renderer_exam.render(exercises)
        
        output_file = os.path.join(output_dir, "Examen_V2.tex")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(latex_code)
        print(f"✅ Examen generado: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"❌ Error al renderizar examen: {e}")
        import traceback
        traceback.print_exc()

    # 3. Renderizado SOLUCIÓN
    print("🎨 Renderizando Solución...")
    try:
        renderer_sol = LatexExamRenderer(is_solution=True)
        latex_code_sol = renderer_sol.render(exercises)
        
        output_file_sol = os.path.join(output_dir, "Solucion_V2.tex")
        with open(output_file_sol, "w", encoding="utf-8") as f:
            f.write(latex_code_sol)
        print(f"✅ Solución generada: {os.path.abspath(output_file_sol)}")
        
    except Exception as e:
        print(f"❌ Error al renderizar solución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()