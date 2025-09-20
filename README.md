# AFD-simulator
# Simulador Interactivo de Autómatas Finitos Deterministas (AFD)

Este proyecto implementa un **simulador interactivo de Autómatas Finitos Deterministas (AFD)** con interfaz gráfica desarrollada en **Python y PyQt6**.  
El objetivo principal es proporcionar una herramienta educativa que permita a los estudiantes comprender y practicar el funcionamiento de los AFD, fundamentales en la teoría de la computación y lenguajes formales.

---

## 📖 Descripción de la aplicación

El simulador permite:

- **Definir un AFD** a partir de sus cinco componentes:
  - Conjunto de estados
  - Alfabeto
  - Estado inicial
  - Estados de aceptación
  - Función de transición
- **Evaluar cadenas de entrada**, mostrando paso a paso el recorrido por los estados y el resultado (aceptada o rechazada).
- **Generar automáticamente las primeras 10 cadenas aceptadas** por el autómata (ordenadas por longitud).
- **Guardar y cargar autómatas en formato JSON**, para reutilizarlos fácilmente.
- **Usar ejemplos predefinidos** (paridad de 1s, terminan en 01, etc.) para practicar.

La interfaz es sencilla e intuitiva, diseñada para estudiantes que estén cursando asignaturas de **Lenguajes Formales y Autómatas** o áreas relacionadas.

---

## ⚙️ Requisitos

- **Python 3.10+** (recomendado Python 3.13).
- **PyQt6** para la interfaz gráfica.

Instalar dependencias:
```bash
py -m pip install PyQt6
```
▶️ Compilación y ejecución

Clona el repositorio o descarga los archivos del proyecto.

Abre una terminal (PowerShell o CMD) en la carpeta del proyecto.

Ejecuta el simulador con:
```bash
py AFD_PyQt6_Simulator.py
```
O abre el ejecutable.

Esto abrirá la ventana principal del simulador.

🖱️ Uso básico
🔹 Definir un AFD

Ingresa los estados, alfabeto, estado inicial, estados de aceptación y transiciones en el formulario de la izquierda.

Pulsa Aplicar definición para que el autómata quede registrado.

🔹 Evaluar cadenas

Escribe una cadena en el campo de texto superior derecho.

Pulsa Evaluar y revisa el paso a paso del recorrido.

🔹 Generar cadenas aceptadas

Pulsa el botón Generar en la sección inferior derecha.

Se mostrarán las primeras 10 cadenas válidas que acepta el AFD.

🔹 Guardar y cargar autómatas

Usa Guardar AFD (JSON) para almacenar tu definición en un archivo.

Con Cargar AFD (JSON) puedes volver a utilizar un autómata previamente guardado.

🔹 Ejemplos incluidos

Haz clic en los ejemplos de la lista derecha (paridad de 1s, terminan en 01, etc.) para cargar rápidamente un autómata ya definido.
