from dataclasses import dataclass
from games.base_action import BaseAction
from games.water_sort_puzzle.state import WaterSortState
import numpy as np

@dataclass(frozen=True)
class WaterSortAction(BaseAction):
    """
    Representa una acción de verter líquido desde un tubo origen a uno destino.
    """
    source: int
    target: int
    amount: int

    def __str__(self):
        return f"Vertir desde tubo {self.source} a tubo {self.target} la cantidad {self.amount}"

    def __eq__(self, other):
        return isinstance(other, WaterSortAction) and self.source == other.source and self.target == other.target


    def __hash__(self):
        return hash((self.source, self.target))

    # --- Aplicación de movimiento ---
    def apply(self, state: WaterSortState) -> WaterSortState:
        # 1. Copiar el estado (necesario ya que el estado es inmutable)
        new_tubes = state.tubes.copy()
        from_tube = new_tubes[self.source]
        to_tube = new_tubes[self.target]

        # # 2. Calcular la cantidad a verter (basado en el estado ORIGINAL)
        color, amount = state.top_color(from_tube)
        # empty_space = state.get_empty_space(to_tube)
        # pour_amount = min(amount, empty_space)
        
        # # Si pour_amount es 0 (no debería ocurrir si get_valid_moves es correcto), retornar el mismo estado.
        # if pour_amount == 0:
        #     return state

        # 3. VACIADO (Quitar del origen)
        # Bajo la convención [0, 1, 2, 3], el top son los índices MÁS BAJOS con líquido.
        # np.where(from_tube != 0)[0] devuelve los índices del líquido ordenados (ej: [1, 2, 3]).
        # [:pour_amount] selecciona los índices a vaciar desde el top.
        
        indices_to_clear = np.where(from_tube != 0)[0][:self.amount] 
        from_tube[indices_to_clear] = 0

        # 4. LLENADO (Poner en destino)
        # Los vacíos están en los índices más bajos (ej: [0, 1]). 
        # Para verter, se debe rellenar el hueco MÁS CERCANO al líquido (el índice vacío más ALTO).
        
        empty_indices = np.where(to_tube == 0)[0]
        # El índice vacío más alto está al final de la lista empty_indices.
        fill_indices = empty_indices[-self.amount:] 
        to_tube[fill_indices] = color

        # 5. Devolver el nuevo estado
        return WaterSortState(tubes=new_tubes, colormap=state.colormap)