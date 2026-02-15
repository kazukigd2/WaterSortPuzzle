from games.base_rules import BaseRules
from .state import JarrasState
from .action import JarrasAction, Move
from typing import List, Iterable

class JarrasRules(BaseRules):
    """
    Define las reglas de las Jarras.
    """
    def __init__(self, goalG: int = 0, goalP: int = 1):
        self.goalG = goalG # Contenido objetivo para la jarra grande (jg)
        self.goalP = goalP # Contenido objetivo para la jarra pequeña (jp)

    def is_valid_state(self, state: JarrasState) -> bool:
        """Un estado siempre es válido si los contenidos no exceden la capacidad."""
        MAXG, MAXP = state.MAXG, state.MAXP
        return (0 <= state.jg <= MAXG and 0 <= state.jp <= MAXP)

    def is_goal_state(self, state: JarrasState) -> bool:
        """Comprueba si el estado es un estado objetivo (jp tiene el valor goal)."""
        # Adaptación del esFinal(Jarras e) de tu código Java
        return (state.jp == self.goalP) and (state.jg == self.goalG)

    def get_valid_moves(self, state: JarrasState) -> Iterable[JarrasAction]:
        """
        Devuelve todas las acciones válidas desde el estado actual.
        """
        jg, jp = state.jg, state.jp
        MAXG, MAXP = state.MAXP, state.MAXP
        valid_actions: List[JarrasAction] = []
        
        # Las 6 posibles acciones:
        
        # 1. Llenar G: solo si no está llena
        if jg < MAXG:
            valid_actions.append(JarrasAction(Move.LLENAR_G))
            
        # 2. Llenar P: solo si no está llena
        if jp < MAXP:
            valid_actions.append(JarrasAction(Move.LLENAR_P))

        # 3. Vaciar G: solo si tiene líquido
        if jg > 0:
            valid_actions.append(JarrasAction(Move.VACIAR_G))
            
        # 4. Vaciar P: solo si tiene líquido
        if jp > 0:
            valid_actions.append(JarrasAction(Move.VACIAR_P))

        # 5. Trasvasar G -> P: solo si G tiene líquido Y P no está llena
        if jg > 0 and jp < MAXP:
            valid_actions.append(JarrasAction(Move.TRASVASAR_G_A_P))

        # 6. Trasvasar P -> G: solo si P tiene líquido Y G no está llena
        if jp > 0 and jg < MAXG:
            valid_actions.append(JarrasAction(Move.TRASVASAR_P_A_G))
            
        return valid_actions