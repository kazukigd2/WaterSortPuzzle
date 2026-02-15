from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    """
    Clase base abstracta que define la estructura común de los algoritmos de búsqueda.
    Todas las implementaciones (BFS, DFS, A*, IDA*, etc.) heredan de esta clase.
    """

    def __init__(self):
        # Inicialización de las estadísticas del algoritmo, estas metricas serán actualizadas durante la ejecución del algoritmo.
        self.nombre_algoritmo = ""
        self.nodos_expandidos = 0
        self.nodos_abiertos = 0
        self.nodos_cerrados = 0
        self.nodos_totales = 0
        self.nodos_memoria = 0
        self.profundidad = 0
        self.coste = 0
        self.camino = []
        self.tiempo = 0
        self.error = "No"
        
    @abstractmethod
    def calcularAlgoritmo(self, inicio=None, meta=None, heuristica=None):
        """
        Simula el cálculo del algoritmo, método abstracto que debe implementar cada algoritmo concreto.
        """

    def imprimirEstadisticas(self, caminos=False):
        """
        Imprime en consola las estadísticas generales del algoritmo.
        Si 'caminos=True', también muestra el camino completo de estados y acciones. esto sirve cuando no se tiene GUI
        """
        if caminos:
            print("\nCamino encontrado (acciones):")
            for i, camino in enumerate(self.camino):
                
                print(f"Paso {i}:")
                print(f"{camino.cost} + {camino.heuristic} = {camino.total}")
                print(f"Estado   => {camino.state}")
            
                # Solo imprimimos una acción si no es el último estado
                if i < len(self.camino) - 1:
                    print(f"Acción   => {self.camino[i+1].action}") # Llama a BaseAction.__str__()
                else: print("Estado final")
      
                # Separador
                print("-" * 30)

        print(f"\nEstadísticas del algoritmo {self.nombre_algoritmo}:")
        print(f"Nodos expandidos: {self.nodos_expandidos}")
        print(f"Nodos abiertos: {self.nodos_abiertos}")
        print(f"Nodos cerrados: {self.nodos_cerrados}")
        print(f"Nodos totales: {self.nodos_totales}")
        print(f"Coste total: {self.coste}")
        print(f"Nodos en memoria: {self.nodos_memoria}")
        print(f"Profundidad: {self.profundidad}")
        print(f"Tiempo: {self.tiempo:.4f} s")

    def obtener_resultados (self) :
        """
        Devuelve las métricas principales del algoritmo en forma de diccionario.
        Esto permite exportar o registrar fácilmente los resultados en formato JSON o CSV.
        """

        return {
        "algoritmo": self.nombre_algoritmo,
        "nodos_expandidos": self.nodos_expandidos,
        "nodos_abiertos": self.nodos_abiertos,
        "nodos_cerrados": self.nodos_cerrados,
        "nodos_totales": self.nodos_totales,
        "profundidad": self.profundidad,
        "coste": self.coste,
        "nodos_memoria": self.nodos_memoria,
        "tiempo": self.tiempo,
        "error": self.error
        }

    def actualizar_memoria(self, actual_memoria: int):
        """Actualiza el máximo de nodos en memoria si el valor actual es mayor.
        Este método se invoca durante la ejecución del algoritmo cuando cambia la frontera.
        """
        if actual_memoria > self.nodos_memoria:
            self.nodos_memoria = actual_memoria







