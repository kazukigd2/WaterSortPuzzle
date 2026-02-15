import random
import numpy as np
from games.base_game import BaseGame
from .state import WaterSortState
from .rules import WaterSortRules
from .colorMap import ColorMap  # opcional para nombres de colores

# Definimos el colormap global (opcional)
default_colormap = ColorMap(["R", "B", "G", "Y", "O", "P", "C", "Pi", "Gr", "Bk"]) 

class WaterSortGame(BaseGame):
    def __init__(
        self,
        num_tubes: int,
        num_colors: int,
        capacity: int = 4,
        seed: int = None,
        heuristic_func=None,
        colormap: ColorMap = default_colormap
    ):
        
        if num_tubes > 12:
            num_tubes = 12
        elif num_tubes < 5:
            num_tubes = 5

        max_colors = num_tubes - 2
        if num_colors > max_colors:
            num_colors = max_colors
        elif num_colors < 3:
            num_colors = 3

        self.num_tubes = num_tubes
        self.num_colors = num_colors
        self.capacity = capacity
        self.seed = seed

        # 1️ Creamos las reglas
        self.rules = WaterSortRules(num_tubes=num_tubes, num_colors=num_colors, seed=seed)
        
        # 2️ Generamos el estado inicial
        initial_tubes = self._generate_initial_state(num_tubes, num_colors, capacity, seed)
        initial_state = WaterSortState(tubes = initial_tubes, colormap=colormap)
        

        # 3️ Llamamos al constructor de BaseGame
        super().__init__(rules=self.rules, initial_state=initial_state, heuristic_func=heuristic_func)
        super().set_current_state(initial_state)

    # -------------------------------
    # Generador de estado inicial
    # -------------------------------
    def _generate_initial_state(self, num_tubes: int, num_colors: int, capacity: int, seed: int = None) -> np.ndarray:
#         tubes = np.array([
#         [1, 1, 2, 3],  # Tubo 0: [R, R, A, V]
#         [2, 3, 3, 1],  # Tubo 1: [A, V, V, R]
#         [2, 1, 2, 3],  # Tubo 2: [A, R, A, V]
#         [0, 0, 0, 0],  # Tubo 3: vacío
#         [0, 0, 0, 0]   # Tubo 4: vacío
# ])
        
        
        tubes = np.zeros((num_tubes, capacity), dtype=int)
        random.seed(seed)

        for i in range(num_colors):  
            tubes[i] = (i+1)

        stateTemp = WaterSortState(tubes = tubes, colormap=default_colormap)

        for i in range(30):
            moves = self.rules.get_mix_moves(stateTemp)
            if not moves:
                break
            move = random.choice(moves)
            stateTemp = move.apply(stateTemp)

        return stateTemp.tubes

    # -------------------------------
    # Método para mostrar el estado
    # -------------------------------
    def show_state(self):
        """Imprime el estado actual usando la representación de WaterSortState"""
        print(str(self._initial_state))
