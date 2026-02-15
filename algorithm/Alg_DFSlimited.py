import time
from algorithm.node import Node
from games.base_state import BaseState
from games.base_game import BaseGame
from algorithm.algorithm import BaseAlgorithm

class Alg_DFSlimited(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.nombre_algoritmo = "DFS limitado"

    def calcularAlgoritmo(self, inicio: BaseState, game: BaseGame, bound: int):
        self._start_time = time.time()

        # Nodo raíz
        root = Node(state=inicio, cost=0, depth=0)

        # Lista de abiertos (pila)
        open_list = [root]

        # Lista de cerrados
        close_list = []

        visited = set()
        visited.add(inicio)

        nodos_totales_creados = 1
        self.nodos_memoria = len(open_list)

        while open_list:
            current_node = open_list.pop()  # LIFO en lugar de FIFO
            current_state = current_node.state
            
            close_list.append(current_node)

            actual_memoria = len(open_list) + len(close_list)
            self.actualizar_memoria(actual_memoria)
            

            if game.is_goal_state(current_node.state):
                self.tiempo = time.time() - self._start_time
                
                path_nodes = current_node.get_path()
                self.camino = [node for node in path_nodes]

                self.nodos_abiertos = len(open_list)
                self.nodos_cerrados = self.nodos_expandidos
                self.nodos_totales = nodos_totales_creados
                self.coste = current_node.cost
                self.profundidad = current_node.depth 
                
                return self.camino
            self.nodos_expandidos += 1

            # Generar sucesores
            if(current_node.depth < bound):
                for action in game.get_valid_moves(current_state):
                    new_state = game.apply(current_state, action=action)

                    if new_state not in visited:
                        visited.add(new_state)
                        child_node = Node(
                            state=new_state,
                            parent=current_node,
                            cost=current_node.cost + action.cost(),
                            depth=current_node.depth + 1,
                            action=action,
                        )
                        open_list.append(child_node)  # Añadir al final para explorarlo pronto
                        nodos_totales_creados += 1

        # Si no se encontró solución
        self.tiempo = time.time() - self._start_time
        self.nodos_abiertos = 0
        self.nodos_cerrados = len(close_list)
        self.nodos_totales = nodos_totales_creados
        self.camino = []
        self.error = "Si"
        print("No se encontró solución.")
        return []
