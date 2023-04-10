from sorteos import sorteo
from datetime import date, timedelta
from os import strerror

# Se listarán los sorteos celebrados dentro del siguiente rango de fechas. NOTA. Actualmente se cargan los últimos 80 sorteos.
hoy = date.today()
fecha_inicio = hoy - timedelta(days=365)  # 1 año (365 días) Formato:AAAAMMDD
fecha_inicio = fecha_inicio.strftime("%Y%m%d")
fecha_fin = hoy.strftime("%Y%m%d")

# Listado de juegos.
# id : [Nombre sorteo,
#       url json,
#       número de bolas,
#       número bolas adicionales (reintegro, complementario, estrellas, etc),
#       total números que entran en juego]
list_lottery = {
    0: ["Salir", ""],
    1: ["Primitiva",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=" + fecha_inicio + "&fechaFinInclusiva=" + fecha_fin,
        6,
        2,
        49],
    2: ["Bonoloto",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&fechaInicioInclusiva=" + fecha_inicio + "&fechaFinInclusiva=" + fecha_fin,
        6,
        2,
        49],
    3: ["Euromillones",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva=" + fecha_inicio + "&fechaFinInclusiva=" + fecha_fin,
        5,
        2,
        50],
    4: ["El Gordo de la Primitiva",
        "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=" + fecha_inicio + "&fechaFinInclusiva=" + fecha_fin,
        5,
        1,
        54]
    }

options_lottery = {0: "Volver al menú principal",  1: "Ver ultimos sorteos", 2: "Estadísticas", 3: "Generar combinaciones"} # Opciones por juego
options_generator = {0: "Volver al menú principal", 1: "Basado en las estadísticas", 2: "Utilizando un modelo de Aprendizaje Automático"}
# Imprimir listado con opciones para los menús
# Return str
def print_menu(items, incluye_list = False): 
    for key in items.keys():
        # Diferenciar si los item del dict incluyen array o no
        if incluye_list: 
            opcion = items[key][0]
        else:
            opcion = items[key]
        print(" " * 10, str(key) + ".", opcion)   
 
# Menú opciones para la opción generar combinaciones
def menu_generador(num_loteria):
    #sorteo_generar = sorteo.GeneradorComBinaciones(list_lottery[num_loteria])
    while True:
        try:
            print("""
            El generador tiene 2 modos para crear las distintas combinaciones:
                - Basado en las estadísticas. Figuras de las combinaciones (nº bajos / nº altos, pares / impares), apariciones y sorteos ausentes.
                  Usa las estadísticas de los últimos 80 sorteos, se actualiza automáticamente. Crea una combinación con las siguientes reglas:
                      * Figuras. Crea las que mas aparecen.
                      * Apariciones. Utiliza una ponderación mayor con los números que menos han aparecido.
                      * Sorteos. Utiliza una ponderación mayor con los números que llevan mas tiempo sin aparecen.
                - Utilizando un modelo de Aprendizaje Automático, con los registros de los últimos sorteos crea posibles combinaciones.
            """)
            print_menu(options_generator)
            modo_generador = int(input(
                "[ " + list_lottery[num_loteria][0].upper() + " ]"+ 
                " Elije una opción  (" + str(min(options_generator.keys())) + "-" +  str(max(options_generator.keys())) + "): ")
                )
            print(modo_generador)
            if modo_generador not in options_generator.keys():
                print("*" * 20)
                print("ERROR. El número", modo_generador, "no es una opción correcta.")
                print("*" * 20)                
            else:
                if modo_generador == 0:
                    break
                else:
                    print(modo_generador)
        except ValueError:
            print("*" * 20)
            print("ERROR. Sólo números. ")
            print("*" * 20)     
        except Exception as ex:
            print("Ocurrio un error.", ex.args )


# Generar un menú con opciones a realizar con el sorteo elegido
# Return int
def lottery_menu(num_loteria): 
    sorteo_elegido = sorteo.Sorteo(list_lottery[num_loteria])      
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
                print("*" * 20)
                print("ERROR. El número", user_select_options, "no es una opción correcta.")
                print("*" * 20)                
            else:
                if user_select_options == 0:
                    break
                else:                    
                    if user_select_options == 1:                        
                        sorteo_elegido.ultimas_combinaciones()
                    if user_select_options == 2:
                        sorteo_elegido.estadisticas()
                    if user_select_options == 3:
                        menu_generador(num_loteria)            
        except ValueError:
            print("*" * 20)
            print("ERROR. Sólo números. ")
            print("*" * 20)     
        except Exception as ex:
            print("Ocurrio un error.", ex.args )
    main_menu()
    
# Menú principal, mostrar listados de sortéos y selección.
# Return int
def main_menu():
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
                print("*" * 20)
                print("ERROR. El número", user_select_lottery, "no es una opción correcta.") 
                print("*" * 20)
            elif user_select_lottery == 0:
                quit() 
            else:
                break                     
        except ValueError:
            print("*" * 20)
            print("ERROR. Sólo números. ") 
            print("*" * 20)
        except Exception as ex:
            print("*" * 20)
            print("ERROR: ", ex.args)
            print("*" * 20)                 
    lottery_menu(user_select_lottery)

main_menu()



