from dataclasses import dataclass
from typing import Any, Optional
import numpy as np
from games.base_state import BaseState

@dataclass(frozen=True)
class WaterSortState(BaseState):
    """
    Representa un estado del juego Water Sort Puzzle.
    Cada tubo es un array numpy de enteros:
    0 = vacío, 1..n = colores
    El estado completo es una matriz (num_tubes x capacity)
    """

    tubes: np.ndarray
    colormap: Optional[object] = None  # <-- añadimos colormap opcional

    #Esta opcion hace que una vez inicializado el array este no sea mutable para evitar errores
    def __post_init__(self):
        self.tubes.flags.writeable = False

    def __hash__(self) -> int:
        return hash(self.tubes.tobytes())

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, WaterSortState) and np.array_equal(self.tubes, other.tubes)

    def __str__(self) -> str:
        s_lines = []
        for i in range(self.tubes.shape[0]):
            tube = self.tubes[i]
            if self.colormap:
                colors = [self.colormap.decode(n) for n in tube]
            else:
                colors = tube.tolist()
            s_lines.append(f"Tubo {i}: {colors}")
        return "Estado actual:\n" + "\n".join(s_lines)

    def get_num_tubes(self):
        return self.tubes.shape[0]

    def get_capacity(self):
        return self.tubes.shape[1]

    def get_num_colors(self):
        # Contar todos los colores distintos distintos de 0
        return len(np.unique(self.tubes[self.tubes != 0]))

    def get_empty_space(self, tube):
        return np.count_nonzero(tube == 0)

    def top_color(self, tube):
        # Encuentra la primera posición no vacía desde el principio
        nonzeros = np.nonzero(tube)[0]
        if len(nonzeros) == 0:
            return 0, 0  # tubo vacío

        top_idx = nonzeros[0]  # top está al principio
        color = tube[top_idx]

        # contar cuántos del mismo color hay consecutivos desde el top
        amount = 1
        for i in range(top_idx + 1, len(tube)):
            if tube[i] == color:
                amount += 1
            else:
                break

        return color, amount


    def height(self, tube_index: int) -> int:
        """Devuelve cuántos líquidos hay en un tubo (no vacíos)."""
        return np.count_nonzero(self.tubes[tube_index])


