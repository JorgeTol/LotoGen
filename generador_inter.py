from sorteos import sorteo
from os import strerror

banner = """
                       .____             __                  .__                                        
  /\|\/\   /\|\/\      |    |     ____ _/  |_   ____ _______ |__|_____     ______     /\|\/\   /\|\/\   
 _)    (___)    (__    |    |    /  _ \\\   __\_/ __ \\\_  __ \|  |\__  \   /  ___/    _)    (___)    (__ 
 \_     _/\_     _/    |    |___(  <_> )|  |  \  ___/ |  | \/|  | / __ \_ \___ \     \_     _/\_     _/ 
   )    \   )    \     |_______ \\\____/ |__|   \___  >|__|   |__|(____  //____  >      )    \   )    \  
   \/\|\/   \/\|\/             \/                  \/                 \/      \/       \/\|\/   \/\|\/  
                                                                                                        
"""

# Listado de juegos.
# id : [Nombre sorteo,
#       url json,
#       número de bolas que se extraen,
#       número bolas adicionales que se extraen(reintegro, complementario, estrellas, etc),
#       total números que entran en juego]
list_lottery = {
    0: ["Salir", ""],
    1: ["Primitiva",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&",
        6,
        2,
        49],
    2: ["Bonoloto",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&",
        6,
        2,
        49],
    3: ["Euromillones",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&",
        5,
        2,
        50,
        12], # Número de estrellas que entran en juego
    4: ["El Gordo de la Primitiva",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&",
        5,
        1,
        54]
    }

options_lottery = {0: "Volver al menú principal",  1: "Ver ultimos sorteos", 2: "Estadísticas", 3: "Generar combinaciones", 4: "Backtest"} # Opciones por juego
options_generator = {0: "Volver al menú principal", 1: "Basado en las estadísticas", 2: "Utilizando un modelo de Aprendizaje Automático (Próximamente)"}

# Formatea la salida de los mensajes en Exceptions:
# Return str
def mensaje_error(args):
    print("\n" + "*" * 20 + " ERROR " + "*" * 20)
    if len(args) > 0:
        for error in args:
            print("\t" + error)
    print("*" * 47 + "\n")

# Imprimir listado con opciones para los menús
# Return str
def print_menu(items, incluye_list = False): 
    for key in items.keys():
        # Diferenciar si los item del dict incluyen array o no
        if incluye_list: 
            opcion = items[key][0]
        else:
            opcion = items[key]
        print("\t" + str(key), opcion)
# Menú opciones para la función generar combinaciones
# Return int
def menu_generador(num_loteria):
    while True:
        try:
            print("""
    El generador tiene 2 modos para crear las distintas combinaciones:
        - Basado en las estadísticas.Se actualiza automáticamente. Crea combinaciones con las siguientes reglas:
              * Figuras. Las combinaciones generadas tendrán las que más se repitan. Nº bajo / Nº alto, par / impar
              * Ausencias. Genera las combinaciones con los números que llevan ausentes X sorteos.
              * Media aparaciones. Excluye los números que están por encima de la media.
              * Apariciones. Utiliza una ponderación mayor con los números que llevan mas tiempo sin aparecer.
        - Utilizando un modelo de Aprendizaje Automático, con los registros de los últimos sorteos crea posibles combinaciones.
            """)
            print_menu(options_generator)
            generador_elegido = int(input(
                "[ " + list_lottery[num_loteria][0].upper() + " ]"+ 
                " Elije una opción  (" + str(min(options_generator.keys())) + "-" +  str(max(options_generator.keys())) + "): ")
                )
            if generador_elegido not in options_generator.keys():
                raise Exception(f"El número {generador_elegido}, no es una opción correcta.")           
            
        except ValueError:
            errores = ("Sólo se admiten números",)
            mensaje_error(errores)     
        except Exception as ex:
            mensaje_error(ex.args)
    
        else:
            return generador_elegido

# Genera un menú con opciones a realizar con el sorteo elegido
def lottery_menu(num_loteria): 
    sorteo_elegido = sorteo.Sorteo(list_lottery[num_loteria]) 
    pronosticos = sorteo.Pronosticos(list_lottery[num_loteria])         
    while True:          
        try:
            print("")
            print("-" * len(list_lottery[num_loteria][0]), " " * len(list_lottery[num_loteria][0]), "-" * len(list_lottery[num_loteria][0]))
            print(" " * len(list_lottery[num_loteria][0]), list_lottery[num_loteria][0].upper())
            print("-" * len(list_lottery[num_loteria][0]), " " * len(list_lottery[num_loteria][0]), "-" * len(list_lottery[num_loteria][0]))
            print("")
            print("Opciones: ")
            print_menu(options_lottery)
            user_select_options = int(input(
                "[ " + list_lottery[num_loteria][0].upper() + " ]"+ 
                " Elije una opción  (" + str(min(options_lottery.keys())) + "-" +  str(max(options_lottery.keys())) + "): ")
                )
            
            if user_select_options not in options_lottery.keys():
                raise Exception(f"El número {user_select_options} no es una opción correcta.")
            else:
                if user_select_options == 0:
                    break
                else:                    
                    if user_select_options == 1:                        
                        sorteo_elegido.ultimas_combinaciones()
                    if user_select_options == 2:
                        sorteo_elegido.estadisticas()
                    if user_select_options == 3:
                        if user_select_options == 0:
                            break
                        if menu_generador(num_loteria) == 1:
                            pronosticos.imprimir_pronosticos()
                    if user_select_options == 4:
                        pronosticos.backtest()                       
        except ValueError:
            errores = ("Sólo se admiten números",)
            mensaje_error(errores)     
        except Exception as ex:
            mensaje_error(ex.args)
    main_menu()
    
# Menú principal, mostrar listados de sortéos y selección.
# Return int
def main_menu():
    print(banner)
    print("""
        Consulta estadísticas, últimos sorteos y pronostica resultados a partir de las estadísticas o utilizando el aprendizaje automático.
        Los juegos de azar son eso, azar. Los pronósticos que genera este script no asegurán una mayor probabilidad de aciertos.

        Elija el sorteo:
        """)
    print_menu(list_lottery, incluye_list=True)
    
    while True: 
        try:
            user_select_lottery = int(input("Elige un número (" + str(min(list_lottery.keys())) + "-" +  str(max(list_lottery.keys())) + "): ")) 
            if user_select_lottery not in list_lottery.keys():
                raise Exception(f"El número {user_select_lottery} no es una opción correcta.") 
            elif user_select_lottery == 0:
                quit() 
            else:
                break                     
        except ValueError:
            errores = ("Sólo se admiten números",)
            mensaje_error(errores)
        except Exception as ex:
            mensaje_error(ex.args)                 
    lottery_menu(user_select_lottery)

main_menu()



