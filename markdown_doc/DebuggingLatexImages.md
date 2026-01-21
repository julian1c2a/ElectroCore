# Guía de Depuración de Imágenes LaTeX (Flujo Mejorado)

Este proyecto utiliza un sistema de **Gestión de Recursos (Asset Manager)** que permite separar la generación automática de diagramas de su corrección manual.

## 🔄 Flujo de Trabajo de Depuración

Si un diagrama generado automáticamente (ej: un circuito o cronograma) no se ve bien en el PDF final:

1.  **Localizar el Borrador**:
    *   Ve a `build/latex/components/`.
    *   Encuentra el archivo problemático (ej: `ej5_seq_timing.tex`).
    *   Copia su contenido.

2.  **Preparar el Candidato**:
    *   Ve a `resources/latex/debugging/`.
    *   Abre (o crea) el archivo `candidate.tex`.
    *   Pega el contenido del borrador allí.

3.  **Visualizar y Corregir**:
    *   Abre y compila `resources/latex/debugging/test_component.tex`.
    *   Verás el diagrama renderizado en un entorno aislado.
    *   Edita `candidate.tex` y recompila `test_component.tex` hasta que el diagrama esté perfecto.

4.  **Promover a Producción**:
    *   Una vez corregido, guarda el contenido de `candidate.tex` en un nuevo archivo en la carpeta superior: `resources/latex/`.
    *   **Importante:** El nombre del archivo debe coincidir con el ID que espera el generador (ej: `ej5_seq_timing.tex`). Puedes ver este nombre en la cabecera del archivo generado original.

5.  **Verificar**:
    *   Ejecuta `python main_v2.py`.
    *   El sistema detectará tu archivo en `resources/latex/` y lo usará automáticamente.

## 📂 Estructura de Carpetas

*   `build/latex/components/`: **Borradores** generados por Python.
*   `resources/latex/debugging/`: **Laboratorio**.
    *   `test_component.tex`: El archivo que compilas para ver los cambios.
    *   `candidate.tex`: El archivo sucio donde editas el código.
*   `resources/latex/`: **Producción**. Archivos `.tex` finales y corregidos.
