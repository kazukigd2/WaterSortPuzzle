import pygame
import numpy as np
import time
import results.Results as rs
import os

from games.water_sort_puzzle.game import WaterSortGame
from games.water_sort_puzzle.action import WaterSortAction
from games.water_sort_puzzle.state import WaterSortState
from algorithm.Alg_Astar import Alg_Astar
from algorithm.Alg_BactrackingCot import Alg_BacktrakingCot
from algorithm.Alg_BFS import Alg_BFS 
from algorithm.Alg_DFS import Alg_DFS
from algorithm.Alg_DFSlimited import Alg_DFSlimited
from algorithm.Alg_IDAstar import Alg_IDAstar
from games.water_sort_puzzle.heuristic import Heuristic_1, Heuristic_2, Heuristic_3

# --- Configuración y Constantes ---

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (65, 105, 225)
ORANGE = (255, 165, 0)
RED = (200, 50, 50)
GREEN = (50, 205, 50)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Mapeo de colores del juego (Color numérico: RGB)
COLOR_MAPPING_RGB = {
    1: (200, 50, 50),    # RED
    2: (65, 105, 225),   # BLUE
    3: (50, 205, 50),    # GREEN
    4: (255, 255, 0),    # YELLOW
    5: (255, 165, 0),    # ORANGE
    6: (128, 0, 128),    # PURPLE
    7: (0, 255, 255),    # CYAN
    8: (255, 192, 203),  # PINK
    9: (128, 128, 128),  # GRAY
    10: (0, 0, 0),       # BLACK
    0: (200, 200, 200)   # Empty
}

# Configuración de botones de la barra lateral
SIDEBAR_X = WIDTH - 260
SIDEBAR_WIDTH = 240
BUTTON_HEIGHT = 40
BUTTON_SPACING = 10

ALGORITHMS = {
    "A*": (Alg_Astar, BLUE),
    "BFS": (Alg_BFS, GREEN),
    "DFS": (Alg_DFS, PURPLE),
    "DFS Limited": (Alg_DFSlimited, (180, 120, 0)),
    "IDA*": (Alg_IDAstar, (100, 149, 237)),
    "Backtrack": (Alg_BacktrakingCot, RED),
}

HEURISTICS_CLASSES = {
    "1": Heuristic_1,
    "2": Heuristic_2,
    "3": Heuristic_3,
}
ALGORITHMS_AVAILABLE = True

class WaterSortGUI:
    def __init__(self, game: WaterSortGame):
        pygame.init()
        self.game = game
        self.config = {
            'num_tubes': game.num_tubes,
            'num_colors': game.num_colors,
            'capacity': game.capacity,
            'seed': game.seed
        }
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Water Sort Puzzle")
        self.font_small = pygame.font.Font(None, 22)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Estado del juego
        self.current_state: WaterSortState = game._initial_state
        self.selected_tube_index = -1
        self.solution_path = None
        self.solution_step = 0
        self.solution_running = False
        self.game_over = False
        self.solver_name = ""
        self.solver_instance = None

        # --- POP-UP ---
        self.show_report_warning = False
        self.report_warning_rects = {}

        # Control de Heurísticas
        self.HEURISTICS = {"No": None, **{k: k for k in HEURISTICS_CLASSES.keys()}}
        self.selected_heuristic = "No"

        # Parámetros de Diseño de tubos
        self.TUBE_WIDTH = 50
        self.TUBE_HEIGHT = 220
        self.TUBE_CAPACITY = game.capacity
        # Ancho disponible para los tubos
        available_width = WIDTH - SIDEBAR_WIDTH - 40  # 40 px de margen

        # Calculamos ancho máximo por tubo para que quepan
        max_tube_width = 60  # opcional, ancho máximo que queremos
        tube_width = min(self.TUBE_WIDTH, available_width // game.num_tubes)

        # Recalcular spacing según ancho real
        tube_spacing = (available_width - tube_width * game.num_tubes) // (game.num_tubes + 1)

        # Guardar valores ajustados
        self.TUBE_WIDTH = tube_width
        self.tube_spacing = tube_spacing
        self.TUBE_Y_START = HEIGHT - self.TUBE_HEIGHT - 50

        # Inicialización de Rects de botones
        y = BUTTON_SPACING
        self.BUTTONS_RECTS = {}
        for i, name in enumerate(ALGORITHMS.keys()):
            self.BUTTONS_RECTS[name] = pygame.Rect(
                SIDEBAR_X, y + i * (BUTTON_HEIGHT + BUTTON_SPACING), SIDEBAR_WIDTH, BUTTON_HEIGHT
            )

        # Posiciones de Radio Buttons
        self.RADIO_BUTTON_POS = (
            SIDEBAR_X + 10, 
            y + len(ALGORITHMS) * (BUTTON_HEIGHT + BUTTON_SPACING) + 30
        )
        self.RADIO_BUTTON_SIZE = 12
        self.RADIO_TEXT_OFFSET = 30
        self.RADIO_SPACING = 40
        self._heuristic_rects = self._setup_heuristic_rects()
        
        # Campos de entrada
        base_y_inputs = self.RADIO_BUTTON_POS[1] + (len(self.HEURISTICS) // 2 + 1) * self.RADIO_SPACING + 20
        self.COTA_INPUT_BOX = pygame.Rect(SIDEBAR_X, base_y_inputs, 100, 30)
        self.SEED_INPUT_BOX = pygame.Rect(SIDEBAR_X + 130, base_y_inputs, 100, 30)
        self.cota_value = 30
        self.input_active_cota = False
        self.seed_value = self.config['seed']
        self.input_active_seed = False


        # Botón Reset
        self.RESET_BUTTON_RECT = pygame.Rect(SIDEBAR_X, base_y_inputs + 50, SIDEBAR_WIDTH, 40)
        self.RESET_BUTTON_TEXT = "Resetear Juego"

        # Botón Generar Reportes
        self.REPORT_BUTTON_WIDTH = 220
        self.REPORT_BUTTON_HEIGHT = 40
        self.REPORT_BUTTON_RECT = pygame.Rect(
            (WIDTH - SIDEBAR_WIDTH -300 - self.REPORT_BUTTON_WIDTH) // 2,
            self.TUBE_Y_START - 70,
            self.REPORT_BUTTON_WIDTH,
            self.REPORT_BUTTON_HEIGHT
        )
        self.REPORT_BUTTON_TEXT = "Generar Informes"

        # Desplegable
        self.dropdowns = []
        self.dropdown_active = None

        base_x = self.REPORT_BUTTON_RECT.right + 30
        base_y = self.REPORT_BUTTON_RECT.y + 10
        spacing = 130

        self.add_dropdown("Nº Tubos", (base_x, base_y), list(range(5, 13)), self.config['num_tubes'])
        self.add_dropdown("Nº Colores", (base_x + spacing, base_y), list(range(3, self.config['num_tubes'] - 1)), self.config['num_colors'])



    # --- Métodos de Setup ---
    def _setup_heuristic_rects(self):
        """Calcula y devuelve los rectángulos de colisión para los radio buttons."""
        rects = {}
        start_x, start_y = self.RADIO_BUTTON_POS
        current_x = start_x + 10
        current_y = start_y + 30
        for name in self.HEURISTICS.keys():
            rects[name] = pygame.Rect(
                current_x, current_y, self.RADIO_SPACING, self.RADIO_BUTTON_SIZE
            )
            current_x += self.RADIO_SPACING
        return rects

    def _show_report_warning_popup(self):
        """Activa el estado de visualización de la advertencia antes de generar el reporte."""
        self.show_report_warning = True

    def _draw_report_warning_popup(self, screen):
        if not self.show_report_warning:
            return

        # Dimensiones y posición del pop-up
        POPUP_WIDTH, POPUP_HEIGHT = 650, 350
        POPUP_X = (WIDTH - POPUP_WIDTH) // 2
        POPUP_Y = (HEIGHT - POPUP_HEIGHT) // 2
        POPUP_RECT = pygame.Rect(POPUP_X, POPUP_Y, POPUP_WIDTH, POPUP_HEIGHT)

        # Fondo semi-transparente para oscurecer el juego
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Dibujar caja del pop-up
        pygame.draw.rect(screen, WHITE, POPUP_RECT, border_radius=10)
        pygame.draw.rect(screen, BLACK, POPUP_RECT, 3, border_radius=10)
        
        # Título
        title_surface = self.font_large.render("¡ADVERTENCIA DE EJECUCIÓN!", True, RED)
        screen.blit(title_surface, title_surface.get_rect(midtop=(POPUP_RECT.centerx, POPUP_Y + 20)))

        # Mensajes de advertencia
        messages = [
            f"Heurística Seleccionada: {self.selected_heuristic}",
            f"Número de Tubos: {self.config['num_tubes']}",
            f"Número de Colores: {self.config['num_colors']}",
            "",
            "Sin Heurística o con el número de tubos es muy grande,",
            "esta operación **podría durar varias horas**.",
            "¿Está seguro que desea continuar?"
        ]

        text_y = POPUP_Y + 70
        for i, msg in enumerate(messages):
            color = RED if i > 3 else BLACK
            font = self.font_medium if i > 3 else self.font_small
            
            # Formato especial para destacar el tiempo (lógica de renderizado simple)
            if "**podría durar varias horas**" in msg:
                parts = msg.split('**')
                total_width = font.size(parts[0])[0] + self.font_medium.size(parts[1])[0] + font.size(parts[2])[0]
                current_x = POPUP_RECT.centerx - total_width // 2 
                
                # Parte 1
                part1_surface = font.render(parts[0], True, color)
                screen.blit(part1_surface, (current_x, text_y))
                current_x += part1_surface.get_width()
                
                # Parte Bold
                bold_surface = self.font_medium.render(parts[1], True, color)
                screen.blit(bold_surface, (current_x, text_y - 2)) 
                current_x += bold_surface.get_width()
                
                # Parte 2
                part2_surface = font.render(parts[2], True, color)
                screen.blit(part2_surface, (current_x, text_y))
            else:
                text_surface = font.render(msg, True, color)
                screen.blit(text_surface, text_surface.get_rect(midtop=(POPUP_RECT.centerx, text_y)))

            text_y += font.get_linesize() + 5

        # Botones (Cancel, Continue)
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 40
        BUTTON_Y = POPUP_Y + POPUP_HEIGHT - BUTTON_HEIGHT - 20
        
        # Botón Cancelar
        cancel_rect = pygame.Rect(POPUP_X + 50, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, cancel_rect, 0, 5)
        cancel_text = self.font_medium.render("Cancelar", True, BLACK)
        screen.blit(cancel_text, cancel_text.get_rect(center=cancel_rect.center))

        # Botón Continuar
        continue_rect = pygame.Rect(POPUP_X + POPUP_WIDTH - BUTTON_WIDTH - 50, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, RED, continue_rect, 0, 5)
        continue_text = self.font_medium.render("Continuar", True, WHITE)
        screen.blit(continue_text, continue_text.get_rect(center=continue_rect.center))
        
        # Guardar rectángulos para manejo de clic
        self.report_warning_rects = {
            "cancel": cancel_rect,
            "continue": continue_rect
        }

    # --- Métodos de Dibujo ---

    def draw_tube(self, screen, tube_data: np.ndarray, index: int):
        x = self.tube_spacing * (index + 1) + self.TUBE_WIDTH * index
        tube_rect = pygame.Rect(x, self.TUBE_Y_START, self.TUBE_WIDTH, self.TUBE_HEIGHT)
        pygame.draw.rect(screen, BLACK, tube_rect, 2)

        if index == self.selected_tube_index:
            pygame.draw.rect(screen, ORANGE, tube_rect, 4)

        liquid_layers = [c for c in tube_data if c != 0]
        layer_height = self.TUBE_HEIGHT / self.TUBE_CAPACITY
        
        # Dibujo de las capas: iteramos al revés para ir de abajo hacia arriba
        for i, color_num in enumerate(reversed(liquid_layers)):
            y = self.TUBE_Y_START + self.TUBE_HEIGHT - (i + 1) * layer_height
            color_rgb = COLOR_MAPPING_RGB.get(color_num, BLACK)
            layer_rect = pygame.Rect(x + 1, y + 1, self.TUBE_WIDTH - 2, layer_height - 1)
            pygame.draw.rect(screen, color_rgb, layer_rect)
            
        max_text_width = self.TUBE_WIDTH
        font_size = 22
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(f"Tubo {index}", True, BLACK)

        # Reducir tamaño si no cabe
        while text_surface.get_width() > max_text_width and font_size > 8:
            font_size -= 1
            font = pygame.font.Font(None, font_size)
            text_surface = font.render(f"Tubo {index+1}", True, BLACK)

        # Dibujar texto centrado debajo del tubo
        text_rect = text_surface.get_rect(center=(x + self.TUBE_WIDTH / 2, self.TUBE_Y_START + self.TUBE_HEIGHT + 10))
        screen.blit(text_surface, text_rect)
        
    def draw_heuristic_selector(self, screen):
        title_surface = self.font_medium.render("Heurísticas: (A*, IDA*)", True, BLACK)
        screen.blit(title_surface, self.RADIO_BUTTON_POS)
        
        for name, rect in self._heuristic_rects.items():
            
            center_x = rect.x + self.RADIO_BUTTON_SIZE // 2
            center_y = rect.y + self.RADIO_BUTTON_SIZE // 2
            
            center = (center_x, center_y)
            
            pygame.draw.circle(screen, BLACK, center, self.RADIO_BUTTON_SIZE // 2 + 1, 1)
            
            if name == self.selected_heuristic:
                pygame.draw.circle(screen, BLUE, center, self.RADIO_BUTTON_SIZE // 2 - 3)
            
            text_surface = self.font_small.render(name, True, BLACK)
            
            text_rect = text_surface.get_rect(centerx=center_x)
            text_rect.top = rect.y + self.RADIO_BUTTON_SIZE + 5 
            
            screen.blit(text_surface, text_rect)

    def add_dropdown(self, label, pos, options, default):
        """Crea un nuevo menú desplegable."""
        rect = pygame.Rect(pos[0], pos[1], 100, 30)
        dropdown = {
            "label": label,
            "rect": rect,
            "options": options,
            "selected": default,
        }
        self.dropdowns.append(dropdown)

    def draw_dropdowns(self, screen):
        """Dibuja todos los desplegables creados."""
        font_label = self.font_small
        font_value = self.font_medium

        for i, d in enumerate(self.dropdowns):
            rect = d["rect"]

            # Etiqueta
            label_surface = font_label.render(d["label"], True, BLACK)
            label_x = rect.centerx - label_surface.get_width() // 2
            screen.blit(label_surface, (label_x, rect.y - 22))

            # Caja principal
            border_color = BLUE if self.dropdown_active == i else BLACK
            pygame.draw.rect(screen, WHITE, d["rect"])
            pygame.draw.rect(screen, border_color, d["rect"], 2)

            # Texto seleccionado
            value_surface = font_value.render(str(d["selected"]), True, BLACK)
            value_x = rect.centerx - value_surface.get_width() // 2
            value_y = rect.centery - value_surface.get_height() // 2
            screen.blit(value_surface, (value_x, value_y))

            # Opciones si está abierto
            if self.dropdown_active == i:
                for j, opt in enumerate(d["options"]):
                    option_rect = pygame.Rect(rect.x, rect.bottom + j * 30, rect.width, 30)
                    pygame.draw.rect(screen, WHITE, option_rect)
                    pygame.draw.rect(screen, BLACK, option_rect, 1)

                    # Texto de opción centrado
                    opt_surface = font_label.render(str(opt), True, BLACK)
                    opt_x = option_rect.centerx - opt_surface.get_width() // 2
                    opt_y = option_rect.centery - opt_surface.get_height() // 2
                    screen.blit(opt_surface, (opt_x, opt_y))

    def draw_algorithm_buttons(self, screen):
        if not ALGORITHMS_AVAILABLE: return

        for name, rect in self.BUTTONS_RECTS.items():
            _, color = ALGORITHMS[name]
            pygame.draw.rect(screen, color, rect, 0, 5)
            text_surface = self.font_medium.render(f"Resolver {name}", True, WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def draw_input_boxes(self, screen):
        self._draw_single_input(screen, "Cota: (DFS lim, Backtrack)", self.COTA_INPUT_BOX, self.cota_value, self.input_active_cota)
        self._draw_single_input(screen, "Seed:", self.SEED_INPUT_BOX, self.seed_value, self.input_active_seed)
        
    def _draw_single_input(self, screen, label_text, rect, value, is_active):
        if '(' in label_text:
            main_label = label_text.split('(')[0].strip()
            aux_text = '(' + label_text.split('(')[1].strip()
        else:
            main_label = label_text
            aux_text = ""

        line_height = self.font_medium.get_linesize()

        main_surface = self.font_medium.render(main_label, True, BLACK)
        main_rect = main_surface.get_rect(midbottom=(rect.centerx, rect.top - 5 - line_height))
        screen.blit(main_surface, main_rect)

        if aux_text:
            aux_surface = self.font_small.render(aux_text, True, BLACK)
            aux_rect = aux_surface.get_rect(midbottom=(rect.centerx, rect.top - 5))
            screen.blit(aux_surface, aux_rect)

        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLUE if is_active else BLACK, rect, 2)

        text_to_draw = str(value) if value != "" else ""
        text_surface = self.font_medium.render(text_to_draw, True, BLACK)

        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw_reset_button(self, screen):
        pygame.draw.rect(screen, ORANGE, self.RESET_BUTTON_RECT, 0, 5)
        text_surface = self.font_medium.render(self.RESET_BUTTON_TEXT, True, BLACK)
        text_rect = text_surface.get_rect(center=self.RESET_BUTTON_RECT.center)
        screen.blit(text_surface, text_rect)

    def draw_report_button(self, screen):
        pygame.draw.rect(screen, (170, 0, 255), self.REPORT_BUTTON_RECT, border_radius=8)
        text_surface = self.font_medium.render(self.REPORT_BUTTON_TEXT, True, WHITE)
        text_rect = text_surface.get_rect(center=self.REPORT_BUTTON_RECT.center)
        screen.blit(text_surface, text_rect)

    # --- Lógica de Solución (Centralizada) ---

    def _execute_solver(self, name: str, solver_class, heuristic_instance=None, bound=None):
        """Método unificado para ejecutar cualquier algoritmo de búsqueda."""
        if not ALGORITHMS_AVAILABLE:
            print(f"Error: El módulo {name} no está disponible.")
            return
        
        if self.solution_running or self.game_over:
            print("El juego ya terminó o ya está resolviendo.")
            return

        print(f"Iniciando búsqueda {name}...")
        start_time = time.time()
        
        solver = solver_class()
        self.solver_instance = solver
        
        # Prepara los argumentos para calcularAlgoritmo
        kwargs = {
            'inicio': self.game.current_state(),
            'game': self.game,
        }
        if heuristic_instance is not None:
            kwargs['heuristica'] = heuristic_instance
        if bound is not None:
            kwargs['bound'] = bound

        try:
            solver.calcularAlgoritmo(**kwargs)
            self.solution_path = getattr(solver, 'camino', None) # Asume que guarda el path en 'acciones'
        except Exception as e:
            print(f"Error ejecutando {name}: {e}")
            self.solution_path = None
            
        end_time = time.time()

        if self.solution_path:
            print(f"Solución {name} encontrada en {len(self.solution_path)-1} pasos. Tiempo: {end_time - start_time:.2f}s")
            self.solution_step = 0
            self.solution_running = True
            self.solver_name = name
            # Asegurar que el estado inicial para la reproducción es el estado actual
            self.current_state = self.game.current_state() 
        else:
            self.solver_name = ""
            print(f"No se encontró solución con {name}. Tiempo: {end_time - start_time:.2f}s")
            self.solution_path = None
            self.solution_running = False

    def generate_report(self):
        print("Generando informe...")

        ## Si no se hace reset del juego se ejecuta mal las variables del juego 
        self.handle_reset()


        # Rutas de los algoritmos y resultados
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        base_dir = os.path.abspath(base_dir)
        carpeta_algoritmos = os.path.join(base_dir, 'algorithm')
        carpeta_reporte = os.path.join(base_dir, f"results_t{self.config['num_tubes']}_c{self.config['num_colors']}")

        # Argumentos comunes en los algoritmos
        inicio_estado = self.game.current_state()
        juego = self.game
        cota = self.cota_value if isinstance(self.cota_value, int) and self.cota_value > 0 else 30
        
        heuristic_class = HEURISTICS_CLASSES.get(self.selected_heuristic)
        heuristic_instance = heuristic_class() if heuristic_class else None

        config_args = {
            "Alg_Astar": {
                "inicio": inicio_estado,
                "game": juego,
                "heuristica": heuristic_instance
            },
            "Alg_BFS": {
                "inicio": inicio_estado,
                "game": juego
            },
            "Alg_DFS": {
                "inicio": inicio_estado,
                "game": juego
            },
            "Alg_DFSlimited": {
                "inicio": inicio_estado,
                "game": juego,
                "bound": cota
            },
            "Alg_BacktrakingCot": {
                "inicio": inicio_estado,
                "game": juego,
                "bound": cota
            },
            "Alg_IDAstar": {
                "inicio": inicio_estado,
                "game": juego,
                "heuristica": heuristic_instance
            }
        }

        heuristic_class = HEURISTICS_CLASSES.get(self.selected_heuristic)
        try:
            rs.report(
                carpeta_algoritmos=carpeta_algoritmos,
                carpeta_reporte=carpeta_reporte,
                metodo="calcularAlgoritmo",
                metodo_resultados="obtener_resultados",
                num_tubos=self.game.num_tubes,
                num_colores=self.game.num_colors,
                config_args=config_args,
                heuristico=self.selected_heuristic,
                cota=self.cota_value,
                semilla=self.seed_value,
            )
            print("Informe generado.")
        except Exception as e:
            print(f"Error al generar el informe: {e}")


        
        

    # Métodos de Solución Públicos
    def solve_with_astar(self):
        heuristic_class = HEURISTICS_CLASSES.get(self.selected_heuristic)
        heuristic_instance = heuristic_class() if heuristic_class else None
        self._execute_solver("A*", ALGORITHMS["A*"][0], heuristic_instance=heuristic_instance)
        
    def solve_with_backtrack(self):
        cota = self.cota_value if isinstance(self.cota_value, int) and self.cota_value > 0 else 30
        self._execute_solver("Backtrack", ALGORITHMS["Backtrack"][0], bound=cota)

    def solve_with_bfs(self):
        self._execute_solver("BFS", ALGORITHMS["BFS"][0])

    def solve_with_dfs(self):
        self._execute_solver("DFS", ALGORITHMS["DFS"][0])

    def solve_with_dfslimited(self):
        cota = self.cota_value if isinstance(self.cota_value, int) and self.cota_value > 0 else 30
        self._execute_solver("DFS Limited", ALGORITHMS["DFS Limited"][0], bound=cota)

    def solve_with_ida(self):
        heuristic_class = HEURISTICS_CLASSES.get(self.selected_heuristic)
        heuristic_instance = heuristic_class() if heuristic_class else None
        self._execute_solver("IDA*", ALGORITHMS["IDA*"][0], heuristic_instance=heuristic_instance)
    
    def apply_next_solution_step(self):
        """Aplica el siguiente movimiento de la solución para los algoritmos."""
        if not self.solution_path or self.solution_step >= len(self.solution_path)-1:
            self.solution_running = False
            return

        if(self.solution_step == 0):
            print("\n" + "="*50)
            print(f" Paso {self.solution_step} / {len(self.solution_path)-1} ".center(50, "="))
            print(f"{self.solution_path[self.solution_step].cost} + {self.solution_path[self.solution_step].heuristic} = {self.solution_path[self.solution_step].total}")
            print(" Estado Inicial ".center(50, "-"))
            print(self.current_state)  
            print("-"*50 + "\n")

        self.solution_step += 1

        action: WaterSortAction = self.solution_path[self.solution_step].action
        print("="*50)
        print(f"Acción aplicada: {action}")
        print("="*50)

        print("\n" + "="*50)
        print(f" Paso {self.solution_step} / {len(self.solution_path)-1} ".center(50, "="))
        print(f"{self.solution_path[self.solution_step].cost} + {self.solution_path[self.solution_step].heuristic} = {self.solution_path[self.solution_step].total}")

        # Aplicar la acción
        new_state = action.apply(self.current_state)
        print(" Estado ".center(50, "-"))
        print(new_state)  
        print("-"*50 + "\n")
      
        # Actualizar el estado
        self.game.set_current_state(new_state)
        self.current_state = new_state

        if self.solution_step >= len(self.solution_path)-1:
            print(f"¡Solución {self.solver_name} completada!")
            self.solution_running = False
            
            # Verificar el estado meta
            if self.game.rules.is_goal_state(self.current_state):
                self.game_over = True
                print("¡Juego Ganado mediante algoritmo!")
            
            if hasattr(self, 'solver_instance'):
                self.solver_instance.imprimirEstadisticas()
            
            self.solution_path = None # Limpiar la ruta después de terminar

    # --- Manejo de Eventos ---

    def handle_reset(self):
        print("Creando nueva instancia del juego...")
        self.input_active_cota = False
        self.input_active_seed = False

        heuristic_class = HEURISTICS_CLASSES.get(self.selected_heuristic)
        heuristic_instance = heuristic_class() if heuristic_class else None

        new_game = WaterSortGame(
            num_tubes=self.config['num_tubes'],
            num_colors=self.config['num_colors'],
            capacity=self.config['capacity'],
            seed=self.seed_value,
            heuristic_func=heuristic_instance
        )
        
        self.game = new_game
        self.current_state = self.game.current_state()
        self.selected_tube_index = -1
        self.solution_path = None
        self.solution_step = 0
        self.solution_running = False
        self.solving = False
        self.game_over = False
        self.show_report_warning = False

        self.solver_instance = None

        self._update_layout()

        print("Juego reseteado. Nueva instancia creada. Listo para jugar.")
    
    # --- Manejo de Clics de raton ---
    def handle_mouse_click(self, pos):
        if self.show_report_warning:
            if self.report_warning_rects.get("cancel", pygame.Rect(0,0,0,0)).collidepoint(pos):
                self.show_report_warning = False # Cancela y cierra el pop-up
                print("Generación de informe cancelada por el usuario.")
                return True
            elif self.report_warning_rects.get("continue", pygame.Rect(0,0,0,0)).collidepoint(pos):
                self.show_report_warning = False # Cierra el pop-up
                self.generate_report() # Procede con la generación
                return True
            # Si se clica en cualquier otro sitio mientras el pop-up está activo
            return True

        if self.RESET_BUTTON_RECT.collidepoint(pos):
            self.game_over = False
            self.handle_reset()
            return

        if self.solution_running:
            return

        if self.REPORT_BUTTON_RECT.collidepoint(pos):
            self._show_report_warning_popup()
            return

        if self.handle_dropdown_click(pos):
            return

        if self.game_over:
            return

        # 1. Chequeo de Input Boxes
        if self._check_input_box_click(pos, self.COTA_INPUT_BOX, 'cota'): return
        if self._check_input_box_click(pos, self.SEED_INPUT_BOX, 'seed'): return

        # Si se hizo clic fuera, asegurar que las inactividades se manejen
        if self.input_active_cota:
            self.input_active_cota = False
            cota_old = 30 
            if hasattr(self, 'config') and 'cota' in self.config:
                cota_old = self.config['cota']
    
            current_input_str = str(self.cota_value)
    
            if current_input_str.isdigit() and current_input_str != "":
                new_cota_val = int(current_input_str)
                new_cota_val = min(new_cota_val, 99) 
            else:
                new_cota_val = cota_old 

            self.cota_value = new_cota_val
            self.config['cota'] = new_cota_val

        if self.input_active_seed:
            self.input_active_seed = False
            config_seed_old = self.config['seed'] 
            current_input_str = str(self.seed_value)
            if current_input_str.isdigit():
                new_seed_val = int(current_input_str)
            else:
                new_seed_val = self.config['seed'] 

            self.seed_value = new_seed_val
            if new_seed_val != config_seed_old:
                self.handle_reset()
            

        # 2. Chequeo de Radio Buttons
        for name, rect in self._heuristic_rects.items():
            if rect.collidepoint(pos):
                self.selected_heuristic = name
                print(f"Heurística seleccionada: {name}")
                return

        # 3. Chequeo de Botones de Algoritmos
        BUTTON_SOLVERS = {
            "A*": self.solve_with_astar,
            "BFS": self.solve_with_bfs,
            "DFS": self.solve_with_dfs,
            "DFS Limited": self.solve_with_dfslimited,
            "IDA*": self.solve_with_ida,
            "Backtrack": self.solve_with_backtrack,
        }
        for name, rect in self.BUTTONS_RECTS.items():
            if rect.collidepoint(pos):
                if name in BUTTON_SOLVERS:
                    BUTTON_SOLVERS[name]()
                    return
        
        # 4. Lógica de Clic en Tubo
        self._handle_tube_click_area(pos)
    
    # --- Lógica de Input Boxes ---
    def _check_input_box_click(self, pos, rect, type_str):
        """Función auxiliar para manejar el clic en cajas de texto."""
        is_cota = (type_str == 'cota')
        
        if rect.collidepoint(pos):
            # Desactivar el otro input box
            if is_cota:
                self.input_active_seed = False
            else:
                self.input_active_cota = False
                
            # Determinar si la caja *actual* se está activando
            is_currently_inactive = (is_cota and not self.input_active_cota) or (not is_cota and not self.input_active_seed)
            
            # --- Lógica de borrado ---
            if is_currently_inactive:
                current_value = self.cota_value if is_cota else self.seed_value
                
                # Si el valor no es cero, lo establecemos como string vacío
                if current_value != 0:
                    new_value = "" 
                else:
                    new_value = "0" # Si es 0, lo mantenemos como "0" o ""

                if is_cota:
                    self.cota_value = new_value
                    self.input_active_cota = True
                else:
                    self.seed_value = new_value
                    self.input_active_seed = True
            return True
        return False

    # --- Lógica de Dropdowns ---
    def handle_dropdown_click(self, pos):
        """Gestiona los clics de los menús desplegables y actualiza el juego si cambian los valores."""
        # Si hay uno activo, primero ver si clicó dentro de sus opciones
        if self.dropdown_active is not None:
            d = self.dropdowns[self.dropdown_active]
            for j, opt in enumerate(d["options"]):
                option_rect = pygame.Rect(d["rect"].x, d["rect"].bottom + j * 30, d["rect"].width, 30)
                if option_rect.collidepoint(pos):
                    # --- Valor cambiado ---
                    old_value = d["selected"]
                    d["selected"] = opt
                    self.dropdown_active = None

                    # Si realmente cambió el valor
                    if opt != old_value:
                        self._on_dropdown_changed(d["label"], opt)

                    return True

        # Clic en caja principal
        for i, d in enumerate(self.dropdowns):
            if d["rect"].collidepoint(pos):
                self.dropdown_active = None if self.dropdown_active == i else i
                return True

        # Clic fuera: cerrar todo
        self.dropdown_active = None
        return False

        # Clic en caja principal
        for i, d in enumerate(self.dropdowns):
            if d["rect"].collidepoint(pos):
                self.dropdown_active = None if self.dropdown_active == i else i
                return True

        # Clic fuera: cerrar todo
        self.dropdown_active = None
        return False

    # --- Lógica de Cambio en Dropdowns ---
    def _on_dropdown_changed(self, label, new_value):
        """Se llama cuando cambia el valor de un dropdown."""
        # Buscar los valores actuales
        tubes_dropdown = next((d for d in self.dropdowns if d["label"] == "Nº Tubos"), None)
        colors_dropdown = next((d for d in self.dropdowns if d["label"] == "Nº Colores"), None)

        if not tubes_dropdown or not colors_dropdown:
            return

        # --- Si se cambia el número de tubos ---
        if label == "Nº Tubos":
            tubes_val = new_value
            # Actualizar opciones del dropdown de colores
            colors_dropdown["options"] = list(range(3, tubes_val - 1))
            colors_dropdown["selected"] = max(3, tubes_val - 2)
            num_colors = colors_dropdown["selected"]

            # Actualizar config
            self.config['num_tubes'] = tubes_val
            self.config['num_colors'] = num_colors

            # Regenerar el juego usando tu reset
            self.handle_reset()

        # --- Si se cambia el número de colores ---
        elif label == "Nº Colores":
            num_colors = new_value
            tubes_val = tubes_dropdown["selected"]

            self.config['num_tubes'] = tubes_val
            self.config['num_colors'] = num_colors

            self.handle_reset()
    
    # --- Lógica de Clic en Tubos ---
    def _handle_tube_click_area(self, pos):
        mouse_x, mouse_y = pos
        num_tubes = self.current_state.get_num_tubes()
        
        for i in range(num_tubes):
            x_start = self.tube_spacing * (i + 1) + self.TUBE_WIDTH * i
            x_end = x_start + self.TUBE_WIDTH
            
            if (x_start <= mouse_x <= x_end and 
                self.TUBE_Y_START <= mouse_y <= self.TUBE_Y_START + self.TUBE_HEIGHT):
                self.process_tube_click(i)
                return
    
    # --- Lógica de Clic en Tubos ---
    def process_tube_click(self, clicked_tube_index: int):
        # 1. Si no hay tubo seleccionado (Primer clic: Origen)
        if self.selected_tube_index == -1:
            if self.game.current_state().height(clicked_tube_index) > 0:
                self.selected_tube_index = clicked_tube_index
            return

        # 2. Si hay un tubo seleccionado (Segundo clic: Destino)
        else:
            source = self.selected_tube_index
            target = clicked_tube_index

            if source == target:
                self.selected_tube_index = -1
                return

            action = WaterSortAction(source=source, target=target, amount=1) # El amount real se ajusta internamente

            valid_moves = self.game.rules.get_valid_moves(self.current_state)
            
            # Buscamos si existe una acción válida de (source, target)
            actual_action = next((a for a in valid_moves if a.source == source and a.target == target), None)
            
            if actual_action:
                print(f"Aplicando acción manual: {actual_action}")
                new_state = actual_action.apply(self.current_state)
                
                self.game.set_current_state(new_state)
                self.current_state = new_state
                
                if self.game.rules.is_goal_state(self.current_state):
                    self.game_over = True
                    print("¡Juego Ganado!")
            else:
                print(f"Movimiento manual no válido.")
            
            self.selected_tube_index = -1

    # --- Manejador de inputs ---
    def handle_key_down(self, event):
        """Maneja los eventos de teclado para las cajas de entrada."""
        # Determina si estamos editando Cota o Seed
        is_cota = self.input_active_cota
        is_seed = self.input_active_seed

        if is_cota or is_seed:
            active_var_name = 'cota_value' if is_cota else 'seed_value'
            current_value = getattr(self, active_var_name)
            
            if event.key == pygame.K_RETURN:
                setattr(self, 'input_active_cota' if is_cota else 'input_active_seed', False)
                # Asegura que si está vacío, sea 0
                if str(current_value) == "":
                    setattr(self, active_var_name, 0)
                return

            current_str = str(current_value)
            
            if event.key == pygame.K_BACKSPACE:
                new_str = current_str[:-1]
            elif event.unicode.isdigit():
                # Concatenar dígito
                new_str = event.unicode if current_str in ("0", "") else current_str + event.unicode
            else:
                return
                
            setattr(self, active_var_name, new_str)
            
            # Conversión y límite (después de la edición como string)
            if new_str != "":
                int_value = int(new_str)
                limit = 99 if is_cota else 999
                if int_value > limit:
                    int_value = limit
                setattr(self, active_var_name, int_value)
            
    # --- Método de Dibujo Principal ---
    def draw(self):
        self.screen.fill(WHITE)

        for i, tube in enumerate(self.current_state.tubes):
            self.draw_tube(self.screen, tube, i)
            
        self.draw_heuristic_selector(self.screen)
        self.draw_algorithm_buttons(self.screen)
        self.draw_input_boxes(self.screen)
        self.draw_report_button(self.screen)
        self.draw_reset_button(self.screen)
        self.draw_dropdowns(self.screen)
        self._draw_report_warning_popup(self.screen)
        
        # Dibujar mensaje de estado
        if self.game_over:
            status_text = "¡JUEGO COMPLETADO! Resetea el juego."
        elif self.solution_running:
            total_steps = len(self.solution_path)-1 if self.solution_path else 0
            status_text = f"REPRODUCIENDO SOLUCIÓN {self.solver_name}... Paso {self.solution_step}/{total_steps}"
        elif self.selected_tube_index != -1:
            status_text = f"Tubo seleccionado: {self.selected_tube_index}. Haz clic en el destino."
        else:
            status_text = "Selecciona un tubo origen"


        # Dibujar mensaje de estado
        font_status = self.font_medium
        main_surface = font_status.render(status_text, True, BLACK)
        main_rect = main_surface.get_rect(topleft=(20, 20))  # ponerlo cerca de la parte superior
        self.screen.blit(main_surface, main_rect)

        # --- DIBUJAR ESTADÍSTICAS DEL ALGORITMO ---
        if hasattr(self, 'solver_instance') and self.solver_instance and not self.solution_running:
            alg = self.solver_instance
            stats_lines = [
                f"Estadísticas del algoritmo {alg.nombre_algoritmo}:",
                f"Nodos expandidos: {alg.nodos_expandidos}",
                f"Nodos abiertos: {alg.nodos_abiertos}",
                f"Nodos cerrados: {alg.nodos_cerrados}",
                f"Nodos totales: {alg.nodos_totales}",
                f"Coste total: {alg.coste}",
                f"Nodos max en memoria: {alg.nodos_memoria}",
                f"Profundidad: {alg.profundidad}",
                f"Tiempo: {alg.tiempo:.4f} s"
            ]

            font_stats = self.font_small
            y = main_rect.bottom + 5  # justo debajo del mensaje principal
            for line in stats_lines:
                line_surface = font_stats.render(line, True, (40, 40, 40))
                line_rect = line_surface.get_rect(topleft=(20, y))
                self.screen.blit(line_surface, line_rect)
                y += font_stats.get_linesize()
        
        pygame.display.flip()

    # --- Actualización de Layout ---
    def _update_layout(self):
        """Recalcula TUBE_WIDTH, tube_spacing y posiciones dependientes del número de tubos."""
        num_tubes = int(self.config.get('num_tubes', len(self.current_state.tubes) if hasattr(self, 'current_state') else 6))

        available_width = WIDTH - SIDEBAR_WIDTH - 40  # 40 px de margen

        max_tube_width = 60
        tube_width = min(self.TUBE_WIDTH if hasattr(self, 'TUBE_WIDTH') else 50, available_width // max(1, num_tubes))
        tube_width = min(tube_width, max_tube_width)
        # En caso de que sea muy estrecho, limitar un mínimo razonable
        tube_width = max(30, tube_width)

        total_tubes_width = tube_width * num_tubes
        leftover = max(0, available_width - total_tubes_width)
        tube_spacing = leftover // (num_tubes + 1)

        # Guardar en la instancia
        self.TUBE_WIDTH = tube_width
        self.TUBE_CAPACITY = self.config.get('capacity', getattr(self, 'TUBE_CAPACITY', self.TUBE_CAPACITY))
        self.tube_spacing = tube_spacing
        self.TUBE_Y_START = HEIGHT - self.TUBE_HEIGHT - 50

    # --- Bucle Principal ---
    def run(self):
        SOLUTION_SPEED_MS = 500
        last_step_time = pygame.time.get_ticks()

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)

            # Lógica de reproducción automática de la solución
            current_time = pygame.time.get_ticks()
            if self.solution_running and current_time - last_step_time > SOLUTION_SPEED_MS:
                self.apply_next_solution_step()
                last_step_time = current_time

            self.draw()
            self.clock.tick(30)

        pygame.quit()