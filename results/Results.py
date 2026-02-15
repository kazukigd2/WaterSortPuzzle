import pandas as pd 
import inspect
from datetime import datetime
import os
import matplotlib.pyplot as plt
import importlib.util
from algorithm.algorithm import BaseAlgorithm
from typing import Optional



def generar_graficos(df: pd.DataFrame, output_dir):
    """
    Genera y guarda gráficos comparativos de rendimiento entre algoritmos.

    Crea una carpeta con la fecha actual (YYYY_MM_DD) dentro del directorio 'results'
    y guarda los gráficos como archivos .png en su interior.

    Args:
        df (pd.DataFrame): DataFrame con los resultados de los algoritmos.
                           Debe contener las columnas 'algoritmo', 'tiempo' y 'nodos_expandidos'.
    
    Returns:
        list: Una lista de cadenas de texto con las rutas a los gráficos generados.
    """
    date_time_obj = datetime.now().strftime('%Y_%m_%d') 
    hour_time_obj = datetime.now().strftime('%H_%M_%S') 
    # output_dir = os.path.join(os.path.dirname(__file__), date_time_obj)
    os.makedirs(output_dir, exist_ok=True)

    rutas = []

    # Tiempo promedio por algoritmo
    if "tiempo" in df.columns:
        tiempo_prom = df.groupby("algoritmo")["tiempo"].mean().sort_values()
        plt.figure()
        tiempo_prom.plot(kind="bar", title="Tiempo promedio por algoritmo")
        plt.xlabel("Algoritmo")
        plt.ylabel("Tiempo (s)")
        ruta_tiempo = os.path.join(output_dir, "tiempo_promedio.png")
        plt.savefig(ruta_tiempo)
        rutas.append(ruta_tiempo)

    # Nodos expandidos promedio
    if "nodos_expandidos" in df.columns:
        nodos_prom = df.groupby("algoritmo")["nodos_expandidos"].mean().sort_values()
        plt.figure()
        nodos_prom.plot(kind="bar", title="Nodos expandidos promedio")
        plt.xlabel("Algoritmo")
        plt.ylabel("Nodos expandidos")
        ruta_nodos = os.path.join(output_dir, "nodos_expandidos.png")
        plt.savefig(ruta_nodos)
        rutas.append(ruta_nodos)

    return rutas

def export (data:pd.DataFrame, output_dir, num_tubos: int = 0, num_colores: int = 0, heuristico: str = None,
           cota: Optional[float] = None,
           semilla: Optional[int] = None):
    """
    Exporta un DataFrame de resultados a archivos CSV y Excel.

    Crea un directorio con la fecha actual (YYYY_MM_DD) dentro de la carpeta 'results'.
    Dentro de ese directorio, guarda los datos en un archivo .csv y un .xlsx,
    nombrados con la hora y minuto actuales (resultados_HH_MM).

    Args:
        data (pd.DataFrame): El DataFrame que contiene los datos a exportar.
    """
    date_time_obj = datetime.now().strftime('%Y_%m_%d') 
    hour_time_obj = datetime.now().strftime('%H_%M') 
    # output_dir = os.path.join(os.path.dirname(__file__), date_time_obj)

    os.makedirs(output_dir,exist_ok=True)
    file_path_csv = os.path.join(output_dir, f"resultados_{hour_time_obj}.csv")
    file_path_excel = os.path.join(output_dir, f"resultados_{hour_time_obj}.xlsx")



    data.to_csv(file_path_csv, index=False)
    
    # --- Guardar Excel con cabecera personalizada ---
    with pd.ExcelWriter(file_path_excel, engine='openpyxl') as writer:
        fila_inicial = 0

        # Información general
        info = []
        if num_tubos:
            info.append(['Número de tubos', num_tubos])
        if num_colores:
            info.append(['Número de colores', num_colores])
        if heuristico is not None:
            info.append(['Heurístico', heuristico])
        if cota is not None:
            info.append(['Cota', cota])
        if semilla is not None:
            info.append(['Semilla', semilla])

        if info:
            info_df = pd.DataFrame(info, columns=['Descripción', 'Valor'])
            info_df.to_excel(writer, index=False, header=False, startrow=fila_inicial)
            fila_inicial += len(info_df) + 2  # deja un par de filas en blanco

        # Escribir los resultados
        data.to_excel(writer, index=False, startrow=fila_inicial)


def report (carpeta_algoritmos:str, carpeta_reporte: str, 
            metodo:str= "calcularAlgoritmo", 
            metodo_resultados: str = "obtener_resultados",
            config_args: Optional[dict] = None,
            heuristico: str = None,
            cota: Optional[float] = None,
            semilla: Optional[int] = None,
            num_tubos: int = 0, num_colores: int = 0,
            clase_Base:type = BaseAlgorithm)-> str:
    
    """
    Ejecuta los métodos de las clases de la carpeta seleccionada, permitiendo pasar argumentos a 
    los métodos y genera un informe consolidado junto archivos csv, excel e imágenes. Posteriormente 
    abre la carpeta donde se encuentra el informe.

    Args:
        carpeta_algoritmos (str): ruta de los algoritmos.
        carpeta_reporte (str): ruta del informe resultante generado.
        metodo (str): metodo a ejecutar de las clases.
        config_args (dict | None): configuracion con argumentos por clases/módulo.

    Returns:
        str: ruta completa del informe y archivos adicionales
    """
    
    resultados = []

    if not os.path.isdir(carpeta_algoritmos):
        raise FileNotFoundError(f"La carpeta {carpeta_algoritmos} no existe")
    
    date_time_obj = datetime.now().strftime('%Y_%m_%d') 

    # Verifica si existe carpeta si no existe la crea
    os.makedirs(carpeta_reporte, exist_ok=True)

    path_reporte = os.path.join(carpeta_reporte,f"informe_{date_time_obj}")

    os.makedirs(path_reporte, exist_ok=True)



    for archivo in os.listdir(carpeta_algoritmos):
        if archivo.endswith(".py") and not archivo.startswith("__") and archivo.startswith("Alg"):
            nombre_modulo = os.path.splitext(archivo)[0]
            ruta_script = os.path.join(carpeta_algoritmos,archivo)

            print(f"Ejecutando {nombre_modulo}")

            try:
                spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_script)
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)

                clases = [
                    cls for _, cls in inspect.getmembers(modulo,inspect.isclass)
                    if (clase_Base is None or issubclass(cls, clase_Base)) and cls.__module__ == nombre_modulo
                ]

                if not clases:
                    print(f"[AVISO] No se encontraron clases en el {archivo}\n")
                    continue

                for clase in clases:
                    nombre_clase = clase.__name__
                    instancia = clase()

                    if nombre_clase in config_args:
                        args = config_args[nombre_clase]

                        if hasattr(instancia, metodo):
                            metodo_func = getattr(instancia,metodo)

                            try:
                                metodo_func(**args)
                                print("Algoritmo ejecutado")
                                if hasattr(instancia,metodo_resultados):
                                    metodo_func_res = getattr(instancia,metodo_resultados)
                                    try:
                                        data = metodo_func_res()
                                        print([data])
                                        resultados.append(data)
                                    except Exception as e:
                                        print(f"[ERROR] Falló la ejecución de {metodo_func_res}: {e}")
                                else:
                                    print(f"[ERROR] {nombre_clase} no implementa {metodo_resultados}")
                            except Exception as e:
                                print(f"[ERROR] Falló la ejecución de {nombre_clase}: {e}")
                        else:
                            print(f"[ERROR] Falló la ejecución de {nombre_clase}: {e}")
                    else:
                        print(f"[ERROR] {nombre_clase} no implementa {metodo}")                       


            except Exception as e :
                print(f"[ERROR] No se pudo procesar {archivo}: {e}\n")
            

    # Abrir la carpeta donde se encuentra el reporte
    df = pd.DataFrame(resultados)

    export(df, path_reporte,
           num_tubos=num_tubos,
           num_colores=num_colores,
           heuristico=heuristico,
           cota=cota,
           semilla=semilla)
    generar_graficos(df, path_reporte)

    os.startfile(path_reporte)
    




