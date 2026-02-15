from collections import deque
import time
from algorithm.algorithm import BaseAlgorithm
from algorithm.node import Node
from games.base_state import BaseState
from games.base_game import BaseGame

class Alg_BFS(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.nombre_algoritmo = "BFS"

    def calcularAlgoritmo(self, inicio: BaseState, game: BaseGame):
        self._start_time = time.time()

        # Inicialización de estructuras
        root = Node(state=inicio,cost=0,depth=0)

        # Lista de abiertos
        open_list = deque([root])

        # Lista de cerrados
        close_list = []

        visited = set()
        visited.add(inicio)

        node_id_counter = 1
        nodos_totales_creados = 1
        self.nodos_memoria = len(open_list)

        while open_list:
            current_node = open_list.popleft()
            current_state = current_node.state
            
            close_list.append(current_node)

            actual_memoria = len(open_list) + len(close_list)
            self.actualizar_memoria(actual_memoria)
            

            if game.is_goal_state(current_node.state):
                self.tiempo = time.time() - self._start_time
                
                path_nodes = current_node.get_path()
                # Reconstruir camino y actualizar métricas finales
                self.camino = [node for node in path_nodes]

                self.nodos_abiertos = len(open_list)
                self.nodos_cerrados = self.nodos_expandidos
                self.nodos_totales = nodos_totales_creados
                self.coste = current_node.cost
                self.profundidad = current_node.depth 
                
                return self.camino
            self.nodos_expandidos +=1
            
            for action in game.get_valid_moves(current_state):

                new_state = game.apply(current_state,action=action)

                if new_state not in visited:
                    visited.add(new_state)
                    child_node = Node(
                        state=new_state,
                        parent=current_node,
                        cost=current_node.cost + action.cost(),
                        depth= current_node.depth + 1,
                        action=action,
                    )
                    open_list.append(child_node)
                    nodos_totales_creados+=1
        

        self.tiempo = time.time() - self._start_time
        self.nodos_expandidos = self.nodos_expandidos
        self.nodos_abiertos = 0
        self.nodos_cerrados = len(close_list)
        self.nodos_totales = nodos_totales_creados
        self.camino = []
        self.error = "Si"
        print("No se encontró solución.")
        return []




        
