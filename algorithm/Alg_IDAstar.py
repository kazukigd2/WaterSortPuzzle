import time
from algorithm.algorithm import BaseAlgorithm
from algorithm.node import Node
from games.base_state import BaseState
from games.base_game import BaseGame

class Alg_IDAstar(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.nombre_algoritmo = "IDA*"

    def calcularAlgoritmo(self, inicio: BaseState, game: BaseGame, heuristica=None):
        self._start_time = time.time()
        self.nodos_totales = 1
        self.nodos_expandidos = 0

        # --- Inicialización de Estructuras ---
        h_inicio = (heuristica.calculate(inicio) if heuristica else 0)
        root = Node(state=inicio, cost=0, depth=0, heuristic=h_inicio)

        f_root = root.cost + h_inicio
        bound = f_root

        while True:
            t = self.IDA_recursive(root, bound, game, heuristica)
            if isinstance(t, list):  # encontró solución
                self.tiempo = time.time() - self._start_time
                return t
            if t == float('inf'):  # no hay solución
                self.tiempo = time.time() - self._start_time
                self.error = "Si"
                print("No se encontró solución.")
                return []
            bound = t  # aumentar límite al mínimo f que excedió el límite

    def IDA_recursive(self, node, bound, game, heuristica=None): 
        self.actualizar_memoria(node.depth + 1)
        h_value = node.heuristic if node.heuristic is not None else 0
        f = node.cost + h_value
        if f > bound:
            return f  # devuelve f que excedió el límite
        if game.is_goal_state(node.state):
            path_nodes = node.get_path()
            self.camino = [n for n in path_nodes]
            self.nodos_cerrados = self.nodos_expandidos
            self.coste = node.cost
            self.profundidad = node.depth
            return self.camino

        min_bound = float('inf')
        self.nodos_expandidos += 1

        for action in game.get_valid_moves(node.state):
            new_state = game.apply(node.state, action=action)
            # Evita ciclos (volver a estados anteriores del camino)
            ancestor = node
            repeated = False
            while ancestor is not None:
                if new_state == ancestor.state:
                    repeated = True
                    break
                ancestor = ancestor.parent
            if repeated:
                continue
            
            h_child = (heuristica.calculate(new_state) if heuristica else 0)

            child_node = Node(
                state=new_state,
                parent=node,
                cost=node.cost + action.cost(), 
                depth=node.depth + 1,
                heuristic=h_child,
                action=action
            )
            self.nodos_totales += 1

            t = self.IDA_recursive(child_node, bound, game, heuristica)
            if isinstance(t, list):
                return t
            if t < min_bound:
                min_bound = t

        return min_bound