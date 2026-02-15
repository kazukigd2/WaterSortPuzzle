from .state import WaterSortState
from .action import WaterSortAction
from games.base_rules import BaseRules
import numpy as np

class WaterSortRules(BaseRules):
    def __init__(self, num_tubes, num_colors, seed=None):
        self.__num_tubes = num_tubes
        self.__num_colors = num_colors
        self.__seed = seed
        self.__capacity = 4
        self.__tubes = np.full((self.__num_tubes, self.__capacity), 0)

    # --- Validaciones básicas ---
    def is_valid_state(self, state: WaterSortState) -> bool:
        """Verifica que todos los colores sean válidos y que ningún tubo tenga más colores de la capacidad."""
        for tube in state.tubes:
            # Verificar colores válidos (ignora 0)
            if any(color != 0 and color not in self.valid_colors for color in tube):
                return False
            # Verificar altura: cantidad de elementos distintos de 0 no excede capacidad
            if np.count_nonzero(tube) > self.__capacity:
                return False
        return True

    def is_goal_state(self, state):
        capacity = state.get_capacity() # Obtener capacidad del estado

        for tube in state.tubes:
            num_liquid = np.count_nonzero(tube)
            
            # 1. Tubo vacío: Siempre es una meta válida.
            if num_liquid == 0:
                continue

            # 2. Tubo con líquido:
            
            # 2a. Debe estar completamente lleno.
            # (En puzzles solubles, los tubos de color deben estar llenos a capacidad total).
            if num_liquid != capacity:
                return False 
                
            # 2b. Todos los colores deben ser iguales (consolidación).
            nonzeros = tube[tube != 0]
            if not np.all(nonzeros == nonzeros[0]):
                return False
                
        return True

    # --- Movimientos ---
    def get_valid_moves(self, state): 
        valid_moves = []
    
        for i in range(state.get_num_tubes()):
            from_tube = state.tubes[i]

            # Si el tubo está vacío pasamos al siguiente
            if state.get_empty_space(from_tube) == self.__capacity:
                continue
        
            # Guardamos el color de arriba y cantidad
            color_origin, amount_color_origin = state.top_color(from_tube)

            for j in range(self.__num_tubes):
                # No se puede verter en el mismo tubo
                if i == j:
                    continue

                to_tube = state.tubes[j]

                # Si el tubo está lleno, no podemos verter ahí
                empty_space = state.get_empty_space(to_tube)
                if empty_space == 0:
                    continue
            
                # Color del top del tubo destino
                color_dest, _ = state.top_color(to_tube)

                # Permitimos verter si el tubo destino está vacío o el top coincide
                if color_dest == 0 or color_origin == color_dest:
                    # Movemos la cantidad posible entre origen y espacio libre
                    pour_amount = min(amount_color_origin, empty_space)
                    # Guardamos la acción
                    valid_moves.append(WaterSortAction(source=i, target=j, amount = pour_amount))

        return valid_moves
    
    #Reglas para conseguir un estado inicial valido
    def get_mix_moves(self, state):
        mix_moves = []

        for i in range(self.__num_tubes):
            from_tube = state.tubes[i]

            # Si está vacío, saltar
            if state.get_empty_space(from_tube) == self.__capacity:
                continue

            color_origin, amount_color_origin = state.top_color(from_tube)
            nonzeros = np.nonzero(from_tube)[0]
            top_idx = nonzeros[-1]

            # Para mezclar debe haber una pieza debajo del misma color
            if amount_color_origin==1:
                continue

            # Recorremos posibles destinos
            for j in range(self.__num_tubes):
                if i == j:
                    continue

                to_tube = state.tubes[j]
                #Debe haber hueco en el tubo
                empty_space = state.get_empty_space(to_tube)
                if empty_space == 0:
                    continue

                color_dest = state.top_color(to_tube)[0]

                # Solo si está vacío o no coincide el color superior
                if color_dest != color_origin:
                    # Puedes mover desde la cantidad completa - 1 hasta 1 solo bloque
                    for amount in range(amount_color_origin - 1, 0, -1):
                        pour_amount = min(amount, empty_space)
                        mix_moves.append(WaterSortAction(source=i, target=j, amount=pour_amount))
        return mix_moves
    


