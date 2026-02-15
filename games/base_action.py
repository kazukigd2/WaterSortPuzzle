from abc import ABC, abstractmethod
from typing import Any

class BaseAction(ABC):
    """
    Clase base abstracta para las acciones de los juegos.
    Obliga a que todas las acciones sean hashables y comparables.
    """

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __str__(self) -> str:
        return str(self)

    @abstractmethod
    def apply(self, state: Any) -> Any:
        """Aplica la acción al estado y devuelve el nuevo estado resultante."""
        pass

    def cost(self) -> float:
        """Devuelve el coste asociado a realizar la acción (por defecto 1)."""
        return 1.0

