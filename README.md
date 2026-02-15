## Hub de Juegos

Este proyecto está diseñado como un **hub central de juegos**, permitiendo ejecutar diferentes juegos que heredan de `BaseGame`.  
Actualmente incluye:

- **Water Sort Puzzle** (con interfaz gráfica o ejecución en consola)
- **Juego de las Jarras**

La arquitectura del hub está implementada de forma **modular y escalable**, de manera que **agregar nuevos juegos es sencillo**: basta con añadir la clase del juego y registrar sus parámetros.  

---

# 🧩 Water Sort Puzzle Solver

Este proyecto implementa un **solucionador del juego Water Sort Puzzle** con interfaz gráfica desarrollada en **Pygame** y soporte para distintos algoritmos de búsqueda como **A\***, **BFS**, **DFS**, **DFS con cota**, **Backtracking con cota** e **IDA\***.  

Incluye además herramientas para generar reportes y análisis del rendimiento mediante **pandas** y **openpyxl**.

---

## 🖥️ Ejecutable para Windows

Este repositorio incluye un ejecutable para Windows que permite ejecutar el programa sin necesidad de instalar Python ni dependencias.

📁 Ubicación:

```bash
bin/water_sort_solver.exe
```

Solo necesitas descargar el repositorio y ejecutar el archivo .exe.

⚠️ Nota: El ejecutable está compilado para Windows 64-bit.

---

## 🚀 Requisitos previos

Asegúrate de tener instalado **Python 3.9 o superior**.  
Puedes verificarlo ejecutando:

```bash
python --version
```
---

## 📦 Instalación de dependencias

El proyecto utiliza varias librerías de Python.  
Las **librerías principales** son:

- `numpy` → manejo de colecciones y estructuras numéricas.  
- `pygame` → interfaz gráfica del juego.  
- `pandas` → generación de reportes en formato DataFrame.
- `matplotlib` → generación de gráficos comparativos.
- `openpyxl` → exportación de resultados a Excel.

Puedes instalar las dependencias de dos maneras:

### 🔹 Opción 1: Instalar dependencias principales manualmente

```bash
pip install numpy matplotlib pygame pandas openpyxl
```

### 🔹 Opción 2: Instalar todas las dependencias del proyecto

Para instalar todas las librerías exactas con sus versiones especificadas en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Recomendación:** crea un entorno virtual para mantener el proyecto aislado del sistema:

```bash
python -m venv venv
source venv/bin/activate # En Linux/Mac
venv\Scripts\activate # En Windows
pip install -r requirements.txt
```

---

## 🕹️ Ejecución del juego

Una vez instaladas las dependencias, puedes ejecutar el juego con interfaz gráfica:

```bash
python main.py
```

Esto abrirá la ventana del juego en Pygame y permitirá jugar o visualizar cómo el algoritmo resuelve el puzzle automáticamente.

---

## ⚙️ Ejecución sin interfaz (modo consola)

Si prefieres ejecutar el juego sin interfaz gráfica, utiliza el archivo:

```bash
python mainNoGUI.py
```

En `mainNoGUI.py` puedes modificar la configuración inicial directamente en la variable `CONFIG`.  
Este ejemplo sirve tanto para **Water Sort Puzzle** como para **Jarras**, y permite seleccionar el juego, el algoritmo, la heurística (solo para WaterSort + AStar/IDAstar) y los parámetros específicos de cada juego:

```python
# ===============================================
# Configuración de Juegos y Algoritmos
# ===============================================
CONFIG  = {
    # --- Configuración General ---
    "juego_str": "WaterSort",            # "WaterSort" o "Jarras"
    "algoritmo_str": "Astar",            # Elegir entre Astar, BFS, DFS, DFS_Cota, Backtracking_Cota o IDAstar
    "cota": 10,                          # Solo para DFS_Cota y Backtracking_Cota las demas las ignora (entre 0 y 99 el resto se autoajusta)

    # --- WaterSort ---
    "num_tubes": 5,                     # Max 12, se autoajusta a mas y Min 5, se autoajusta a menos
    "num_colors": 3,                    # Max num_tubes-2, Min 3 se autoajusta
    "heuristica_str": "H1",             # Elegir entre H1, H2, H3 o No, (Solo para AStar e IDAstar las demas las ignora)
    "seed": 42,                         # Semilla para generar el juego entre 0 y 999, se autoajusta si insertas un valor no valido

    # --- Jarras ---
    "initial_jg": 0,                    # Estado inicial Jarra grande
    "initial_jp": 0,                    # Estado inicial Jarra pequeña
    "goalP": 1,                         # Estado final deseado Jarra pequeña
    "goalG": 0                          # Estado final deseado Jarra grande
}
# ===============================================
```

Este modo es ideal para probar diferentes configuraciones de algoritmos y heurísticas sin necesidad de la interfaz gráfica.

## 📊 Reportes y resultados

Los resultados de ejecución y rendimiento pueden exportarse a hojas de cálculo Excel y csv utilizando pandas y openpyxl, también se podrá generar gráficos comparativos entre los algoritmos ejecutados en formato ".png".
Esto permite analizar el comportamiento de cada algoritmo, los tiempos de ejecución y el número de pasos necesarios para resolver cada instancia del puzzle.

---

## 📊 Créditos

Desarrollado por:
  - Juan Miguel Sarria Orozco
  - Daniela Suárez Morales
  - María Paulina Ordóñez Walkowiak
