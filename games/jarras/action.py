from games.base_action import BaseAction
from .state import JarrasState
from dataclasses import dataclass
from enum import Enum, auto

# Clase para representar las 6 posibles transiciones
class Move(Enum):
    # 1. Llenar / Vaciar
    LLENAR_G = auto()       # 5, jp
    LLENAR_P = auto()       # jg, 2
    VACIAR_G = auto()       # 0, jp
    VACIAR_P = auto()       # jg, 0
    # 2. Trasvasar
    TRASVASAR_G_A_P = auto() # Trasvasar de la Grande a la Pequeña
    TRASVASAR_P_A_G = auto() # Trasvasar de la Pequeña a la Grande

@dataclass(frozen=True)
class JarrasAction(BaseAction):
    move: Move

    def __hash__(self):
        return hash(self.move)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JarrasAction):
            return NotImplemented
        return self.move == other.move

    def __str__(self) -> str:
        return self.move.name

    def apply(self, state: JarrasState) -> JarrasState:
        """
        Aplica la acción y devuelve el nuevo estado resultante.
        """
        jg, jp = state.jg, state.jp
        MAXG, MAXP = state.MAXG, state.MAXP
        
        new_jg, new_jp = jg, jp

        if self.move == Move.LLENAR_G:
            new_jg, new_jp = MAXG, jp
        
        elif self.move == Move.LLENAR_P:
            new_jg, new_jp = jg, MAXP
        
        elif self.move == Move.VACIAR_G:
            new_jg, new_jp = 0, jp
        
        elif self.move == Move.VACIAR_P:
            new_jg, new_jp = jg, 0
        
        elif self.move == Move.TRASVASAR_G_A_P:
            # Trasvasar de la Grande a la Pequeña
            space_in_p = MAXP - jp
            pour_amount = min(jg, space_in_p)
            
            new_jg = jg - pour_amount
            new_jp = jp + pour_amount
        
        elif self.move == Move.TRASVASAR_P_A_G:
            # Trasvasar de la Pequeña a la Grande
            space_in_g = MAXG - jg
            pour_amount = min(jp, space_in_g)
            
            new_jg = jg + pour_amount
            new_jp = jp - pour_amount


        return JarrasState(jg=new_jg, jp=new_jp)