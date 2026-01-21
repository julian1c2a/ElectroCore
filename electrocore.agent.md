# QUÉ SE PRETENDE EN ESTE PROYECTO.

## OBJETIVO GENERAL

Esto ha de ser un proyecto de documentación-libro/manual/software-de-ayuda/guía-práctica/tutorial/demo-sobre-explicación que sirva para aprender la asignatura Fundamentos de Electrónica, que constituye una materia troncal en los Grados de Ingenierías Industriales, al menos en la Unión Europea.

El anterior objetivo general no limita el alcance del proyecto, que puede excederse en el temario al antiguo temario de las asignaturas Electrónica Básica, Electrónica Digital y Electrónica Analógica.

De esta forma el proyecto se enfoca a una especie de base de conocimientos en electrónica, desde el que podemos extraer ejercicios, exámenes, un software de prácticas sobre una página web, un sistema de ejercicios a cumplimentar y corregir, una extracción de manual o de examen sobre lenguaje latex o usando formato docx.

## FORMA DE TRABAJO

Iré desarrollando el archivo CONTENT_FE.md, que contiene actualmente el temario de la asignatura, y a medida que vaya escribiendo el desarrollo de ese temario se irán creando nuevas funciones del project_root/core/. en python, totalmente desconectadas de las otras partes del proyecto, y cada nuevo desrrollo se irá añadiendo a project_root/config/temario_catalogado.json, que contendrá el temario catalogado y la referencia a los archivos de desarrollo en core/ y a los archivos de desarrollo en docs/, a la vez que en project_root/core/catalog.py se irán creando las funciones de consulta y extracción de información de project_root/config/temario_catalogado.json.

## ARQUITECTURA DEL PROYECTO

El proyecto tendrá la siguiente arquitectura:
```
project_root/
│├── core/
│   ├── __init__.py
│   ├── catalog.py
│   ├── electronics_fundamentals.py # desrrollo de funciones python que desarrollan el temario
│   ├── ...py
│
│├── config/
│   ├── temario_catalogado.json # temario catalogado y referencia a archivos de desarrollo
│   ├── ...json
│
│├── docs/
│   ├── CONTENT_FE.md # desarrollo del temario en markdown
│   ├── ...md
|
|├── models/
|
|
|├── modules/
|
|
|├── resources/
|
|
|├── resources/
|
|├── web/
|
│├── electrocore.agent.md # este archivo de agente personalizado

```
