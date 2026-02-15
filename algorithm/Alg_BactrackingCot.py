import time
from algorithm.algorithm import BaseAlgorithm 
from algorithm.node import Node
from games.base_state import BaseState
from games.base_game import BaseGame

class Alg_BacktrakingCot(BaseAlgorithm):

    def __init__(self):
        super().__init__()
        self.nombre_algoritmo = "Backtracking Acotado"

    def calcularAlgoritmo(self, inicio: BaseState,game: BaseGame, bound= 0, depth = 0, current_node: Node= None):
        """
        Ejecuta Backtrack-Acotado y calcula las métricas.
        :param inicio: Estado inicial (BaseState).
        :param game: Instancia de BaseGame para las reglas y transiciones.
        :param bound: Cota máxima de profundidad.
        :return: Lista del camino de estados desde el inicio hasta el objetivo, o lista vacía.
        """

        # Inicialización en la primera llamada
        if depth == 0:
            self._start_time = time.time()
            self.nodos_expandidos = 0
            self.nodos_totales = 1
            self.camino = []
            current_node = Node(state=inicio, depth=0, cost=0)

        self.actualizar_memoria(depth + 1)
       
        # Si supera la cota devuelve FRACASO(lista vacía)
        if depth > bound:
            return []

        # Si es estado meta
        if game.is_goal_state(current_node.state):
            path_nodes = current_node.get_path()
            self.camino = [node for node in path_nodes]
            self.coste = current_node.cost
            self.profundidad = depth
            self.tiempo = time.time() - self._start_time
            return self.camino

        # Expandimos el nodo
        self.nodos_expandidos += 1

        
        # Obtener los estados en el camino actual para evitar ciclos
        path_states = set(node.state for node in current_node.get_path())

        # Explorar sucesores
        for action in game.get_valid_moves(current_node.state):
            new_state = game.apply(current_node.state, action)
            
            if new_state in path_states:
                continue

            self.nodos_totales +=1

            new_node = Node(state=new_state, parent=current_node, action=action, depth=depth+1, cost=current_node.cost + action.cost())
            solution = self.calcularAlgoritmo(new_state, game, bound, depth+1, new_node)
            
            if solution:  # Devuelve la primera solución encontrada
                if depth == 0:
                    self.tiempo = time.time() - self._start_time
                return solution

        # Si no se encontró solución
        if depth == 0:
            self.error = "Si" if not self.camino else "No"
            self.tiempo = time.time() - self._start_time
        return []

