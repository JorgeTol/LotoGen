import urllib.request
import json
from datetime import datetime
from prettytable import PrettyTable, DOUBLE_BORDER
import locale

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

class Sorteo:
    def __init__(self, sorteo_elegido):
        self.__fuente_datos_sorteo = sorteo_elegido[1]    # Url que contiene los datos a descargar
        self.__nombre_sorteo = sorteo_elegido[0]    # Nombre del sorteo.
        self.__numero_bolas = sorteo_elegido[3]    # Número de bolas que entran en juego en la combinación principal.  
        
        # Almacenar todos los datos en json
        with  urllib.request.urlopen(self.__fuente_datos_sorteo) as f:
            lectura_datos = f.read().decode('utf-8')
            self.__tabla_json = json.loads(lectura_datos)
        
        self.__fecha_sorteo = []
        self.__combinaciones = []    # Números de la combinación principal
        self.__num_adicionales = []   # Complementarios, reintegros, estrellas. 
        self.__numeros_bajos_altos = []
        self.__pares_impares = []        
        
        # Extraer los datos para rellenar los atributos
        for datos_sorteo in self.__tabla_json:
            fecha = datetime.fromisoformat(datos_sorteo["fecha_sorteo"])
            fecha_formateada = f"{fecha.strftime('%A ').title():<10}" + fecha.strftime("%d/%m/%Y") # Lunes[margen]01/12/2000
            self.__fecha_sorteo.append(fecha_formateada)
            if self.__nombre_sorteo in ["Primitiva", "Bonoloto"]:                
                combinacion_separada = datos_sorteo["combinacion"].rsplit(" ", maxsplit=2) # Pasar a un array [combinacion, complementario reintegro]
                self.__combinaciones.append(combinacion_separada[0])
                self.__num_adicionales.append(combinacion_separada[1] + ' ' + combinacion_separada[2])                
            
            if self.__nombre_sorteo == "El Gordo de la Primitiva":
                combinacion_separada = datos_sorteo["combinacion"].rsplit(" ", maxsplit=1) # Pasar a un array [combinacion, complementario reintegro]
                self.__combinaciones.append(combinacion_separada[0])
                self.__num_adicionales.append(combinacion_separada[1] )
            
            if self.__nombre_sorteo == "Euromillones":
                combinacion_separada = datos_sorteo["combinacion"].rsplit(" - ", maxsplit=2) # Pasar a un array [combinacion, estrellas]
                self.__combinaciones.append(combinacion_separada[0]) 
                self.__num_adicionales.append(combinacion_separada[1]  + ' - ' + combinacion_separada[2]) 
        
        for combinacion in self.__combinaciones:
            combinacion = combinacion.split(" - ")
            numeros_bajos = len(list(filter(lambda x: int(x) < 26, combinacion)))
            numeros_altos = len(combinacion) - numeros_bajos            
            self.__numeros_bajos_altos.append(f"{numeros_bajos} / {numeros_altos}")
            
            pares = len(list(filter(lambda x: int(x) % 2 == 0, combinacion)))
            impares = len(combinacion) - pares
            self.__pares_impares.append(f"{pares} / {impares}")  
              
    
    # Generar listado de los últimos sorteos. Columnas fecha, combinación, sorteo secundario (si lo hay) y perfil de la combinación
    # Return string
    def ultimas_combinaciones(self):        
        tabla = PrettyTable()
        
        tabla.add_column("Fecha sorteo", self.__fecha_sorteo)
        tabla.add_column("Combinacion ganadora", self.__combinaciones)
        if self.__nombre_sorteo in ["Primitiva", "Bonoloto"]:
            titulo_cabecera = "C y R"
        elif self.__nombre_sorteo == "El Gordo de la Primitiva":
            titulo_cabecera = "Nº clave"
        elif self.__nombre_sorteo == "Euromillones":
            titulo_cabecera = "Estrellas"
        tabla.add_column(titulo_cabecera, self.__num_adicionales)
        
        tabla.add_column("Bajos / Altos", self.__numeros_bajos_altos)
        tabla.add_column("Pares / Impares", self.__pares_impares)
        tabla.set_style(DOUBLE_BORDER)
        print(tabla)
        print("Mostrando los últimos ", len(self.__combinaciones), " resultados")

    def apariciones_ausencias(self, total_bolas, sorteos):
        tabla = PrettyTable()
        tabla.field_names = ["Bola", "Apariciones", "Sorteos ausente"]
        # Creamos el listado de todas las bolas
        n_bolas = [x for x in range(1, total_bolas + 1)] 
        list_numeros_aparecidos = [int(x) for y in sorteos for x in y.split(" - ")] # Pasar de un array con combinaciones a un array con números.

        for bola in n_bolas:
            apariciones = list_numeros_aparecidos.count(bola)
            # Calcular días sin aparecer
            sorteos_ausente = 0
            for sorteo in sorteos:
                combinacion = list(map(int,sorteo.split(" - "))) # Convertir los dígitos (string) a enteros
                if bola not in combinacion:
                    sorteos_ausente += 1                               
                else:
                    break
            salida_apariciones = str(apariciones).ljust(3, " ") + "*" * apariciones
            salida_sorteos_ausente = str(sorteos_ausente).ljust(3, " ") + "*" * sorteos_ausente

            tabla.add_row([bola, salida_apariciones, salida_sorteos_ausente])
        tabla.set_style(DOUBLE_BORDER)
        tabla.align["Apariciones"] = "l"
        tabla.align["Sorteos ausente"] = "l"
        # Descomentar y/o modificar las siguientes líneas para establecer un orden por columnas.
        # tabla_apariciones.sortby = "Bola"
        # tabla_apariciones.reversesort = True

        print(tabla)
    
    
    # Generar tablas con distintas estadísticas: 
    # - Primera tabla: Apariciones por figuras (nº bajos y altos, pares e impares) 
    # - Segunda tabla: Nº de apariciones por bola y días ausentes.
    # - Tercera tabla (Euromillones): Igual que la segunda tabla pero para las estrellas.
    # 
    def estadisticas(self):
        # ############
        # Primera tabla: 
        #     Número de veces que ha aparicido una figura (nºbajo/alto y par/impar)
        # ############
        bajo_alto = {}        
        par_impar = {}        
        
        # Obtener la cantidad de números que tiene la combinación para obtener todas las posible figuras
        longitud_combinacion = len(self.__combinaciones[1].split(" - "))
        for num in range(longitud_combinacion + 1 ): 
            figura_key = str(num) + " / " + str((longitud_combinacion) - num)
            bajo_alto[figura_key] = 0
            par_impar[figura_key] = 0  
        
        for figura in self.__numeros_bajos_altos:            
            bajo_alto[figura] += 1
        
        for figura in self.__pares_impares:
            par_impar[figura] += 1       
        
        tabla_figuras = PrettyTable()
        # Primera fila, cabecera
        titulo_columna = ["Figuras"]
        for head in bajo_alto.keys():
            titulo_columna.append(head)
        tabla_figuras.field_names = titulo_columna
        # Segunda fila, estadísticas nº bajos y altos
        n_bajos_altos = ["Bajos / Altos"]
        for value in bajo_alto.values():
            n_bajos_altos.append(value)
        tabla_figuras.add_row(n_bajos_altos)
        # Tercera fila, estadísticas pares impares
        n_pares_impares = ["Pares / Impares"]
        for value in par_impar.values():
            n_pares_impares.append(value)
        tabla_figuras.add_row(n_pares_impares)
        tabla_figuras.set_style(DOUBLE_BORDER)
        print(tabla_figuras)
        # ############
        # Segunda tabla:
        #     Nº de veces que ha aparecido un número.
        #     Nº de sorteos que lleva sin aparecer un número.
        # ############
        
        self.apariciones_ausencias(self.__numero_bolas, self.__combinaciones) 

        ##############
        # Tercera tabla:
        #     Estrellas en Euromillones
        #     Nº de veces que ha aparecido un número.
        #     Nº de sorteos que lleva sin aparecer un número.
        ##############
        if self.__nombre_sorteo == "Euromillones":
            bolas_estrellas = 12
            print("")
            print("Estrellas")
            print("")
            self.apariciones_ausencias(bolas_estrellas, self.__num_adicionales) 

        print("Mostrando estadísticas de los últimos ", len(self.__combinaciones), " resultados")
    

if __name__ == "__main__":
    #sorteo_elegido = Sorteo(["Euromillones","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva=20220717&fechaFinInclusiva=20230327", 5, 50])
    #sorteo_elegido = Sorteo(["El Gordo de la Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=20221206&fechaFinInclusiva=20230308"])
    #sorteo_elegido = Sorteo(["Bonoloto","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&fechaInicioInclusiva=20220205&fechaFinInclusiva=20230308", 6, 49])
    sorteo_elegido = Sorteo(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206", 6, 49])

    #Primitiva.historial_combinaciones(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206"])
    
    sorteo_elegido.estadisticas()
    #sorteo_elegido.ultimas_combinaciones()
    
    #print(list(sorteo_elegido._Sorteo__combinaciones))
    # print(list(sorteo_elegido._Sorteo__numeros_bajos_altos))
    #sorteo_elegido._Sorteo__numeros_bajos_altos