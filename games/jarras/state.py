from dataclasses import dataclass
from games.base_state import BaseState
from typing import Tuple

@dataclass(frozen=True)
class JarrasState(BaseState):
    """
    Representa el estado actual del problema de las Jarras.
    jg: Contenido de la jarra grande (Capacidad MAXG=5)
    jp: Contenido de la jarra pequeña (Capacidad MAXP=2)
    """
    jg: int
    jp: int
    
    # Definiciones de capacidad
    MAXG: int = 5
    MAXP: int = 2

    def __hash__(self) -> int:
        """
        Calcula el hash basado en el contenido de ambas jarras.
        """
        # Usamos una tupla (jg, jp) para asegurar un hash fiable
        return hash((self.jg, self.jp))

    def __eq__(self, other: object) -> bool:
        """
        Compara dos estados para ver si tienen el mismo contenido.
        """
        if not isinstance(other, JarrasState):
            return NotImplemented
        return self.jg == other.jg and self.jp == other.jp

    def __str__(self) -> str:
        """
        Representación legible del estado: (Contenido Grande, Contenido Pequeña)
        """
        return f"({self.jg},{self.jp})"