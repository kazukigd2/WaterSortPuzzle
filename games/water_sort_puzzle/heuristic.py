import numpy as np
from collections import defaultdict

class Heuristic:
    def __init__(self):
        pass

    def calculate(self,state: np.ndarray):
        pass

class Heuristic_1(Heuristic):
    def __init__(self):
        super().__init__()

    def calculate(self,state: np.ndarray):

        heuristic = 0

        num_colour_tube = defaultdict(list)
        for indx,tube in enumerate(state.tubes):
            colours_in_tube = set(tube) # unique colours in tube
            colours_in_tube.discard(0)
            for colour in colours_in_tube:
                num_colour_tube[colour].append(indx) # apppend the index 
        
        
        for colour,tubes_index in num_colour_tube.items():
            count = {i: list(state.tubes[i]).count(colour) for i in tubes_index}  
            max_colour = max(count.values())  
            dispersion_weight = sum(count.values()) - max_colour
            heuristic += (len(tubes_index) - 1) * dispersion_weight

        return heuristic

class Heuristic_2(Heuristic):
    def __init__(self):
        super().__init__()

    def calculate(self,state):

        size_tube = state.tubes.shape[1]
        incomplete_tubes = 0
        correct_pos_colour = 0

        for indx, tube in enumerate(state.tubes):
            colours_in_tube = set(x for x in tube if x != 0)
            if(len(colours_in_tube) != 1):
                incomplete_tubes+=1

            bottom_idx = next((i for i in reversed(range(size_tube)) if tube[i] != 0), None)
            if bottom_idx is not None:
                bottom_colour = tube[bottom_idx]
                for i in reversed(range(bottom_idx+1)):
                    if tube[i] == bottom_colour:
                        correct_pos_colour += 1
                    else:
                        break

            # print(f"Los datos de cada iteracion {incomplete_tubes} y  {correct_pos_colour}")
            
        return (incomplete_tubes * 4) - correct_pos_colour


class Heuristic_3(Heuristic):
    def __init__(self):
        super().__init__()

    def calculate(self,state: np.ndarray):
        total_unidades_mezcladas = 0
        unidades_bloqueadas = 0

        for tube in state.tubes:
            colores = tube[tube != 0]

            # --- Unidades mezcladas ---
            if len(np.unique(colores)) > 1:
                total_unidades_mezcladas += len(colores)

            # --- Unidades bloqueadas ---
            for i in range(len(colores)-1, -1, -1):  # de arriba (último índice) a abajo (0)
                color_actual = colores[i]
                colores_debajo = colores[:i]         # todo lo que está debajo

                # Contar cuántas unidades debajo son de color distinto
                unidades_bloqueadas += np.sum(colores_debajo != color_actual)

        return total_unidades_mezcladas  + (2 * unidades_bloqueadas)



