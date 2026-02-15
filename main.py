from GUI.WaterSortGUI import WaterSortGUI 
from games.water_sort_puzzle.game import WaterSortGame

def run_gui():
    """
    Función principal para inicializar el juego con la interfaz.
    """
    
    #Configuraciones del juego inicial
    NUM_TUBES = 6 #Max 12, se autoajusta a mas y Min 5, se autoajusta a menos
    NUM_COLORS = 4 #Max num_tubes-2, Min 3 se autoajusta
    SEED = 42

    #Clase del juego
    game = WaterSortGame(
        num_tubes=NUM_TUBES,
        num_colors=NUM_COLORS,
        seed=SEED,
    )

    #Interfaz gráfica
    gui = WaterSortGUI(game)
    gui.run()

if __name__ == "__main__":
    # Ejecutar el codigo con la GUI.
    run_gui()