from abc import ABC, abstractmethod
from typing import List

class BaseRules(ABC):
    """
    Define la interfaz mínima que deben cumplir las reglas de cualquier juego.
    """

    @abstractmethod
    def is_valid_state(self, state) -> bool:
        pass

    @abstractmethod
    def is_goal_state(self, state) -> bool:
        pass

    @abstractmethod
    def get_valid_moves(self, state) -> List:
        pass
