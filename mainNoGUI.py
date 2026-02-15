from games.water_sort_puzzle.game import WaterSortGame
from games.jarras.game import JarrasGame

from algorithm.Alg_Astar import Alg_Astar
from algorithm.Alg_BactrackingCot import Alg_BacktrakingCot
from algorithm.Alg_BFS import Alg_BFS 
from algorithm.Alg_DFS import Alg_DFS
from algorithm.Alg_DFSlimited import Alg_DFSlimited
from algorithm.Alg_IDAstar import Alg_IDAstar

from games.water_sort_puzzle.heuristic import Heuristic_1, Heuristic_2, Heuristic_3
##Clase principal para ejecutar el juego sin GUI y usar A*

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

# Mapeo de Juegos disponibles
GAMES_MAP = {
    "WaterSort": WaterSortGame,
    "Jarras": JarrasGame
}

# Mapeo de Algoritmos disponibles
ALGORITHMS_MAP = {
    "Astar": Alg_Astar,
    "BFS": Alg_BFS, 
    "DFS": Alg_DFS,
    "DFS_Cota": Alg_DFSlimited,
    "Backtracking_Cota": Alg_BacktrakingCot,
    "IDAstar": Alg_IDAstar,
}

# Mapeo de Heurísticas disponibles (Solo WaterSort)
HEURISTICS_MAP = {
    "H1": Heuristic_1,
    "H2": Heuristic_2, 
    "H3": Heuristic_3,
    "No": None,
}

def run_solver(
    juego_str: str,
    algoritmo_str: str,
    heuristica_str: str,
    cota: int,
    num_tubes: int,
    num_colors: int,
    seed: int,
    initial_jg: int,
    initial_jp: int,
    goalP: int,
    goalG: int,
):
    """
    Ejecuta el juego con el algoritmo y parámetros especificados.
    """
    ALGORITHMS_REQUIRING_HEURISTIC = {"Astar", "IDAstar"}
    ALGORITHMS_REQUIRING_COTA = {"DFS_Cota", "Backtracking_Cota"}

    # -------------------------
    # 1. Inicializar el juego
    # -------------------------
    print(f"\n== Inicializando juego: {juego_str} ==")
    GameClass = GAMES_MAP.get(juego_str)
    if not GameClass:
        print(f"ERROR: Juego '{juego_str}' no encontrado.")
        return

    if juego_str == "WaterSort":
        game = GameClass(num_tubes=num_tubes, num_colors=num_colors, seed=seed)
        inicio = game._initial_state
        print(f"-> Parámetros: {num_tubes} tubos, {num_colors} colores, semilla {seed}")

    elif juego_str == "Jarras":
        game = GameClass(
            initial_jg=initial_jg,
            initial_jp=initial_jp,
            goalP=goalP,
            goalG=goalG,
        )
        inicio = game.initial_state()
        print(f"-> Estado inicial: ({initial_jg}, {initial_jp}) | Objetivo: ({goalG}, {goalP})")

    else:
        print(f"ERROR: Juego '{juego_str}' no implementado.")
        return

    # -------------------------
    # 2. Inicializar algoritmo
    # -------------------------
    AlgoritmoClase = ALGORITHMS_MAP.get(algoritmo_str)
    if not AlgoritmoClase:
        print(f"ERROR: Algoritmo '{algoritmo_str}' no reconocido.")
        return

    solver = AlgoritmoClase()
    print(f"-> Algoritmo seleccionado: {algoritmo_str}")

    # -------------------------
    # 3. Inicializar heurística (solo si aplica)
    # -------------------------
    heuristic_instance = None
    if (
        juego_str == "WaterSort"
        and algoritmo_str in ALGORITHMS_REQUIRING_HEURISTIC
    ):
        HeuristicaClase = HEURISTICS_MAP.get(heuristica_str)
        if HeuristicaClase:
            heuristic_instance = HeuristicaClase()
            print(f"-> Usando Heurística: {heuristica_str}")
        else:
            print("-> No se usará heurística.")
    else:
        print("-> Este juego o algoritmo no usa heurísticas.")

    # -------------------------
    # 4. Calcular la solución
    # -------------------------
    kwargs = {"inicio": inicio, "game": game}
    if heuristic_instance:
        kwargs["heuristica"] = heuristic_instance
    if algoritmo_str in ALGORITHMS_REQUIRING_COTA:
        kwargs["bound"] = cota
        print(f"-> Usando Cota de Profundidad: {cota}")

    print("\n== Ejecutando búsqueda... ==")
    solver.calcularAlgoritmo(**kwargs)

    # -------------------------
    # 5. Resultados
    # -------------------------
    print("\n--- Resultados ---")
    solver.imprimirEstadisticas(True)


if __name__ == "__main__":
    run_solver(**CONFIG)