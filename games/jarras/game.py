from games.base_game import BaseGame
from .state import JarrasState
from .rules import JarrasRules
from typing import Callable

class JarrasGame(BaseGame):
    """
    Juego del problema de las Jarras.
    """
    def __init__(
        self,
        initial_jg: int = 0,
        initial_jp: int = 0,
        goalG: int = 0,
        goalP: int = 1,
        heuristic_func: Callable[[JarrasState], float] = None
    ):
        # 1. Creamos las reglas específicas
        rules = JarrasRules(goalG=goalG, goalP=goalP)
        
        # 2. Creamos el estado inicial (JarrasState asume MAXG=5, MAXP=2 por defecto)
        initial_state = JarrasState(jg=initial_jg, jp=initial_jp)
        
        # 3. Llamamos al constructor base
        super().__init__(
            rules=rules,
            initial_state=initial_state,
            heuristic_func=heuristic_func
        )