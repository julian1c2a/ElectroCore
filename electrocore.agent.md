# QUÉ SE PRETENDE EN ESTE PROYECTO.

## OBJETIVO GENERAL

Esto ha de ser un proyecto de documentación-libro/manual/software-de-ayuda/guía-práctica/tutorial/demo-sobre-explicación que sirva para aprender la asignatura Fundamentos de Electrónica, que constituye una materia troncal en los Grados de Ingenierías Industriales, al menos en la Unión Europea.

El anterior objetivo general no limita el alcance del proyecto, que puede excederse en el temario al antiguo temario de las asignaturas Electrónica Básica, Electrónica Digital y Electrónica Analógica.

De esta forma el proyecto se enfoca a una especie de base de conocimientos en electrónica, desde el que podemos extraer ejercicios, exámenes, un software de prácticas sobre una página web, un sistema de ejercicios a cumplimentar y corregir, una extracción de manual o de examen sobre lenguaje latex o usando formato docx.

## FORMA DE TRABAJO

Iré desarrollando el archivo CONTENT_FE.md, que contiene actualmente el temario de la asignatura, y a medida que vaya escribiendo el desarrollo de ese temario se irán creando nuevas funciones del project_root/core/. en python, totalmente desconectadas de las otras partes del proyecto, y cada nuevo desrrollo se irá añadiendo a project_root/config/temario_catalogado.json, que contendrá el temario catalogado y la referencia a los archivos de desarrollo en core/ y a los archivos de desarrollo en docs/, a la vez que en project_root/core/catalog.py se irán creando las funciones de consulta y extracción de información de project_root/config/temario_catalogado.json.

## Flujo de Trabajo y Arquitectura Detallada

La arquitectura del proyecto está diseñada para ser modular y escalable, permitiendo un flujo de trabajo claro desde la solicitud del usuario hasta la generación del producto final (ej. un examen en PDF).

A continuación se detalla el flujo y los componentes principales:

### 1. Interfaz de Usuario (`cli`)
El proceso comienza aquí. El usuario interactúa con la aplicación a través de la línea de comandos para solicitar la generación de problemas o exámenes.

-   **Punto de entrada:** `cli/__main__.py` es el ejecutable principal que parsea los argumentos del usuario (qué temas, cuántas preguntas, qué formato de salida, etc.).
-   **Lógica de comandos:** `cli/problems.py` contiene la lógica específica para los subcomandos, coordinando la creación de los artefactos solicitados.

### 2. Orquestación y Lógica Principal (`core`)
El `cli` invoca al `core` para que ensamble y gestione la creación del examen.

-   **Orquestador:** `core/exam_builder.py` actúa como el director de orquesta. Recibe la petición desde el `cli`.
-   **Catálogo de Contenidos:** Para saber qué generador usar, `core/catalog.py` consulta el archivo `config/temario_catalogado.json`. Este JSON mapea los temas de la asignatura con los módulos de generación de problemas correspondientes.
-   **Fábrica de Generadores:** `core/generator_factory.py` recibe el tema y crea una instancia del generador de problemas específico que se encuentra en el directorio `modules`.

### 3. Generación de Problemas (`modules`)
Aquí reside la "magia" de la creación de ejercicios. Cada subdirectorio es una unidad autónoma de conocimiento.

-   **Estructura:** Cada subdirectorio (ej. `modules/numeracion/`) corresponde a un área temática.
-   **Lógica del Generador:** Dentro de un módulo, archivos como `generators.py` contienen las clases y funciones que crean los datos del problema (enunciado, opciones, pasos de la solución).

### 4. Estructura de Datos (`models`)
Los generadores no devuelven texto plano; devuelven objetos fuertemente tipados definidos en este directorio. Esto desacopla la lógica de la presentación.

-   **Modelo Principal:** `models/problem.py` define la clase `Problem`, una estructura de datos que contiene el enunciado, la solución, el tipo de problema y metadatos adicionales.
-   **Tipos y Soluciones:** Otros archivos definen entidades relacionadas como `ProblemType` o modelos para las soluciones.

### 5. Renderizado de Salida (`renderers`)
Una vez que el `exam_builder` tiene una lista de objetos `Problem`, se la entrega al renderizador adecuado para crear el archivo final.

-   **Lógica de renderizado:** Los subdirectorios `renderers/html/`, `renderers/latex/`, etc., contienen la lógica para convertir la lista de objetos `Problem` en un formato específico (HTML, .tex, etc.).
-   **Recursos Adicionales:** El directorio `resources/` (ej. `resources/latex/`) almacena plantillas y activos estáticos que los renderizadores utilizan para dar formato al documento final (ej. una plantilla de examen en LaTeX).

### 6. Persistencia de Datos (`database`)
Si se desea guardar un examen generado para su posterior uso o análisis, se utiliza la capa de persistencia.

-   **Patrón de Repositorio:** La arquitectura se abstrae del motor de almacenamiento mediante una interfaz en `database/repository.py`.
-   **Implementaciones:**
    -   `database/file_repo.py`: Guarda los exámenes como archivos locales (normalmente en formato JSON).
    -   `database/sqlite_repo.py`: Guarda los exámenes en una base de datos SQLite, permitiendo consultas más complejas.


## REGLAS

1. Cada nueva funcionalidad se desarrolla en un archivo python independiente en core/.
2. Cada nueva funcionalidad se documenta en docs/ con referencias cruzadas.
3. El temario_catalogado.json se actualiza con cada nueva funcionalidad.
4. El archivo catalog.py se actualiza para incluir funciones de consulta para cada nueva funcionalidad.
5. Se mantiene una estructura modular y clara para facilitar el mantenimiento y la escalabilidad del proyecto.
6. No se desrrollan archivos en project_root/ directamente, salvo este archivo electrocore.agent.md.
7. El archivo electrocore.agent.md define las reglas y la arquitectura del proyecto.
8. El desarrollo se realiza de forma iterativa, añadiendo nuevas funcionalidades y documentándolas progresivamente.
9. Se va desarrollando a la vez la aplicáción web en web/ para exponer las funcionalidades de forma interactiva.
10. Se implementan tests en tests/ para asegurar la calidad del código y la corrección de las funcionalidades. No se dejará ninguna funcionalidad sin testear profundamente.

## DESARROLLO ITERATIVO
