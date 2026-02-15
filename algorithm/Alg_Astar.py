import heapq
import time
from algorithm.algorithm import BaseAlgorithm
from algorithm.node import Node
from games.base_state import BaseState
from games.base_game import BaseGame

class Alg_Astar(BaseAlgorithm):
    """
    Implementación del algoritmo de búsqueda A* para problemas de estado.
    Utiliza una cola de prioridad para la lista abierta y maneja la re-exploración
    de nodos para asegurar la optimalidad (costo más bajo).
    """

    def __init__(self):
        super().__init__()
        self.nombre_algoritmo = "A*"


    def calcularAlgoritmo(self, inicio: BaseState, game: BaseGame, heuristica=None):
        """
        Ejecuta A* y calcula las métricas.
        :param inicio: Estado inicial (BaseState).
        :param game: Instancia de BaseGame para las reglas y transiciones.
        :param heuristica: Objeto de heurística con método calculate(state).
        :return: Lista del camino de estados desde el inicio hasta el objetivo, o lista vacía.
        """
        self._start_time = time.time()
        
        # --- Configuración de la Heurística ---
        def h(state):
            # Usar la heurística inyectada si existe, sino 0
            return heuristica.calculate(state) if heuristica else 0

        # --- Inicialización de Estructuras ---
        h_inicio = h(inicio)
        root = Node(state=inicio, cost=0, depth=0, heuristic=h_inicio)

        # open_list: Cola de Prioridad (f_cost, id_unico, nodo)
        # Usamos id_unico para evitar comparaciones de nodos en caso de f_cost iguales
        open_list = [(root.total, 0, root)] 
        
        # best_nodes: Diccionario {estado (hashable): Nodo} para rastrear el mejor camino (menor g)
        best_nodes = {inicio: root}

        # closed_nodes: Conjunto para rastrear los nodos cerrados
        closed_nodes = set()
        
        node_id_counter = 1  # Contador para IDs únicos en el heap
        nodos_totales_creados = 1 # Incluye el nodo raíz
        self.nodos_memoria = len(open_list)

        while open_list:
            # 1. Extraer el nodo con menor f_cost
            f_cost, _, current_node = heapq.heappop(open_list)
            current_state = current_node.state

            if current_state in closed_nodes:
                continue

            # Actualizar memoria actual (open + best)
            memoria_actual = len(open_list) + len(best_nodes)
            self.actualizar_memoria(memoria_actual)
            
            # --- Poda y Control de Optimalidad ---
            # Si el f_cost extraído no coincide con el mejor f_cost conocido (el nodo fue 'superado' antes), ignorar.
            if f_cost > current_node.total:
                 continue

            
            # 2. Comprobar si es la meta
            if game.is_goal_state(current_state):
                self.tiempo = time.time() - self._start_time
                
                path_nodes = current_node.get_path()
                # Reconstruir camino y actualizar métricas finales
                self.camino = [node for node in path_nodes]
                self.nodos_cerrados = len(closed_nodes)
                self.nodos_abiertos = len(open_list)
                self.nodos_totales = nodos_totales_creados
                self.coste = current_node.cost
                self.profundidad = current_node.depth 
                
                return self.camino
            
            # 3. Actualizar métricas
            self.nodos_expandidos += 1

            # 4. Generar sucesores
            for action in game.get_valid_moves(current_state):
                # Calcular el nuevo estado y costos
                nuevo_estado = game.apply(current_state, action)
                g_nuevo = current_node.cost + action.cost()

                # Comprobar si el estado es nuevo o se ha encontrado un camino mejor (menor g)
                is_better = True
                if nuevo_estado in best_nodes:
                    existing_node = best_nodes[nuevo_estado]
                    if g_nuevo >= existing_node.cost:
                        is_better = False # El camino existente es mejor o igual

                if is_better:
                    h_nuevo = h(nuevo_estado)
                    child_node = Node(
                        state=nuevo_estado,
                        parent=current_node,
                        action=action,
                        cost=g_nuevo,
                        depth=current_node.depth + 1,
                        heuristic=h_nuevo
                    )
                    
                    # Almacenar el mejor nodo encontrado para este estado
                    best_nodes[nuevo_estado] = child_node
                    
                    # Añadir a la lista abierta
                    
                    heapq.heappush(open_list, (child_node.total, node_id_counter, child_node))
                    node_id_counter += 1
                    nodos_totales_creados += 1

            closed_nodes.add(current_state)


        # --- No se encontró solución ---
        self.tiempo = time.time() - self.tiempo
        self.nodos_abiertos = 0
        self.nodos_cerrados = len(best_nodes)
        self.nodos_totales = nodos_totales_creados
        self.camino = []
        self.error = "Si"
        print("No se encontró solución.")
        return []