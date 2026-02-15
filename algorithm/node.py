from typing import Optional, Any

class Node:
    """
    Nodo para los algoritmos de búsqueda.
    Guarda el estado, acción que lo generó, padre, coste, profundidad, heurística y otros.
    """

    def __init__(
        self,
        state: Any,
        parent: Optional["Node"] = None,
        action: Optional[Any] = None,
        cost: float = 0.0,
        depth: int = 0,
        heuristic: float = 0.0
    ):
        self.state = state          # Estado del juego (BaseState o concreto)
        self.parent = parent        # Nodo padre
        self.action = action        # Acción que llevó a este estado (BaseAction)
        self.cost = cost            # Coste acumulado desde el nodo inicial
        self.depth = depth          # Profundidad en el árbol
        self.heuristic = heuristic  # Heurística para A*
        self.total = cost + heuristic  # f(n) = g(n) + h(n)

    # ----------------------
    # Para comparaciones en estructuras de prioridad (heapq, etc.)
    # ----------------------
    def __lt__(self, other: "Node"):
        return self.total < other.total

    def __eq__(self, other: Any):
        if not isinstance(other, Node):
            return False
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    # ----------------------
    # Método para reconstruir el camino desde la raíz
    # ----------------------
    def get_path(self) -> list:
        """
        Devuelve la secuencia de nodos desde la raíz hasta este nodo.
        """
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent
        return list(reversed(path))

    def get_actions(self) -> list:
        """
        Devuelve la secuencia de acciones desde la raíz hasta este nodo.
        """
        return [node.action for node in self.get_path()[1:]]  # excluir el nodo inicial