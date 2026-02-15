from abc import ABC, abstractmethod

class BaseState(ABC):
    """
    Clase base abstracta para todos los estados de juegos.
    Garantiza que todos los estados sean comparables y hashables.
    """

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Debe definir la igualdad entre estados."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Debe definir el hash para poder usar el estado en sets o diccionarios."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Representación legible del estado (para debugging o impresión)."""
        pass