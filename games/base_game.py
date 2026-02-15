from abc import ABC, abstractmethod
from typing import Iterable, Callable
from .base_state import BaseState
from .base_action import BaseAction
from .base_rules import BaseRules

class BaseGame(ABC):
    """
    Clase abstracta que define la estructura mínima de un juego.
    Cada juego debe definir su estado inicial y sus reglas específicas.

    Los algoritmos (A*, BFS, DFS, etc.) trabajarán únicamente con esta interfaz.
    """

    def __init__(
        self,
        rules: BaseRules,
        initial_state: BaseState,
        heuristic_func: Callable[[BaseState], float] = None,
        current_state: BaseState = None
    ):
        self.rules = rules
        self._initial_state = initial_state
        self.heuristic_func = heuristic_func  # heurística opcional

    def initial_state(self) -> BaseState:
        """Devuelve el estado inicial del juego."""
        return self._initial_state

    def current_state(self) -> BaseState:
        """Devuelve el estado actual y jugable del juego."""
        return self._current_state

    def set_current_state(self, new_state: BaseState):
        """Actualiza el estado actual del juego."""
        self._current_state = new_state

    # --- Métodos que delegan en las reglas ---
    def is_valid_state(self, state: BaseState) -> bool:
        """Comprueba si el estado es válido según las reglas del juego."""
        return self.rules.is_valid_state(state)

    def is_goal_state(self, state: BaseState) -> bool:
        """Comprueba si el estado es un estado objetivo."""
        return self.rules.is_goal_state(state)

    def get_valid_moves(self, state: BaseState) -> Iterable[BaseAction]:
        """Devuelve todas las acciones válidas desde el estado actual."""
        return self.rules.get_valid_moves(state)

    def apply(self, state: BaseState, action: BaseAction) -> BaseState:
        """Aplica una acción sobre un estado y devuelve el nuevo estado."""
        return action.apply(state)

    def cost(self, from_state: BaseState, action: BaseAction, to_state: BaseState) -> float:
        if hasattr(self.rules, "cost"):
             return self.rules.cost(from_state, action, to_state)
        elif hasattr(action, "cost"):
            return action.cost()

    def heuristic(self, state: BaseState) -> float:
        """Usa la heurística inyectada si existe, sino devuelve 0."""
        if self.heuristic_func:
            return self.heuristic_func(state)
        return 0.0

    def __str__(self, state: BaseState) -> str:
        """Devuelve una descripción legible del estado (para depuración)."""
        return str(state)