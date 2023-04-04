#! /usr/bin/env python3

""""
    Clase para mostrar últimas combinaciones con sus estadísticas
"""
import urllib.request
import json
from datetime import datetime
import numpy as np
from prettytable import PrettyTable, DOUBLE_BORDER
import locale

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

class Sorteo:
    def __init__(self, sorteo_elegido):
        self.__nombre_sorteo = sorteo_elegido[0]    # Nombre del sorteo.
        self.__cantidad_bolas_combinacion = sorteo_elegido[2]    # Cantidad de números que componen la combinación.
        self.__cantidad_numeros_adicionales = sorteo_elegido[3]    # Cantidad de números que componen los números adicionales, complementario y reintegro, estrellas, etc..
        self.__numero_bolas = sorteo_elegido[4]    # Número de bolas que entran en juego en la combinación principal.  
        
        # Almacenar todos los datos en json
        with  urllib.request.urlopen(sorteo_elegido[1]) as f:
            lectura_datos = f.read().decode('utf-8')
            self.__tabla_json = json.loads(lectura_datos)
        
        self.__fecha_sorteo = []
        self.__combinaciones = []
        self.__joker = []
        self.__numeros_adicionales = []
        # Extraer los datos para rellenar los atributos
        for datos_sorteo in self.__tabla_json:
            fecha = datetime.fromisoformat(datos_sorteo["fecha_sorteo"])
            fecha_formateada = f"{fecha.strftime('%A ').title():<10}" + fecha.strftime("%d/%m/%Y") # Lunes[margen]01/12/2000
            
            # Crear un array con la combinacion principal
            if  self.__nombre_sorteo == "Euromillones":
                split = " - "
            elif self.__nombre_sorteo in ["Primitiva", "Bonoloto", "El Gordo de la Primitiva"]:
                split = " "
            combinacion = datos_sorteo["combinacion"].rsplit(split, maxsplit=sorteo_elegido[3]) 
            combinacion_prin = np.array([int(x) for x in combinacion[0].rsplit(" - ")]) 
            if self.__nombre_sorteo == "Primitiva":
                    self.__joker.append(datos_sorteo["joker"]["combinacion"])
            
            # Crear array con los números adicionales.            
            num_adicionales = ""
            for i in range(1,self.__cantidad_numeros_adicionales + 1):
                num_adicionales += combinacion[i] + " "
            
            self.__fecha_sorteo.append(fecha_formateada)
            self.__combinaciones.append(combinacion_prin)
            self.__numeros_adicionales.append(num_adicionales.strip())

        self.__combinaciones = np.array(self.__combinaciones)
        
    
    # Generar listado de los últimos sorteos. Columnas fecha, combinación, sorteo secundario (si lo hay) y perfil de la combinación
    # Return string
    def ultimas_combinaciones(self):        
        tabla = PrettyTable()
        if self.__nombre_sorteo in ["Primitiva", "Bonoloto"]:
            titulo_cabecera = "Comp. y Reint."
        elif self.__nombre_sorteo == "El Gordo de la Primitiva":
            titulo_cabecera = "Nº clave"
        elif self.__nombre_sorteo == "Euromillones":
            titulo_cabecera = "Estrellas"
        tabla.field_names = ["Fecha sorteo", "Combinacion", titulo_cabecera, "Bajos / Altos", "Pares / Impares"]
        
        for i in range(len(self.__combinaciones)):
          tabla.add_row(
              [self.__fecha_sorteo[i],
              ' - '.join(map(lambda s :f"{str(s):>2s}", self.__combinaciones[i])),     # En la combinación se pasa el array a string y se formatéa y espacia cada digito
               self.__numeros_adicionales[i],
               str(len(self.__combinaciones[i][self.__combinaciones[i] < 26])) + " / " + str(len(self.__combinaciones[i][self.__combinaciones[i] > 25])),
               str(len(self.__combinaciones[i][self.__combinaciones[i] % 2 == 0])) + " / " + str(len(self.__combinaciones[i][self.__combinaciones[i] % 2 !=0]))
              ]
            )
        if self.__nombre_sorteo == "Primitiva":
            tabla.add_column("Joker", self.__joker)
        tabla.set_style(DOUBLE_BORDER)  
        print(tabla)
        print("Mostrando los últimos ", len(self.__combinaciones), " resultados")
    
    # Muestra el número de apariciones de una bola y los sorteos que lleva sin aparecer.
    # Return string, tabla.
    def apariciones_ausencias(self, total_bolas, sorteos):
        tabla = PrettyTable()
        tabla.field_names = ["Bola", "Apariciones", "Sorteos ausente"]
        # Creamos el listado de todas las bolas
        n_bolas = [x for x in range(1, total_bolas + 1)] 
        
        for bola in n_bolas:
            apariciones = len(sorteos[sorteos == bola])
            # Calcular días sin aparecer
            sorteos_ausente = 0
            for sorteo in  sorteos:
                if bola not in sorteo:
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
        tabla.set_style(DOUBLE_BORDER)
        print(tabla)

    # Muestra una tabla con las estadísticas por figuras, nº bajo / alto y par / impar
    # Return string, tabla.
    def figuras_combinaciones(self):
        bajo_alto = {}        
        par_impar = {}        
        
        # Crear las posibles figuras dependiendo del número de bolas de la combinación
        for num in range(self.__cantidad_bolas_combinacion + 1 ): 
            figura_key = str(num) + " / " + str((self.__cantidad_bolas_combinacion) - num)
            bajo_alto[figura_key] = 0
            par_impar[figura_key] = 0  
        
        # Conteo de figuras.
        for sorteo in self.__combinaciones:
            figura_bajo_alto = str(len(sorteo[sorteo < 26])) + " / " + str(len(sorteo[sorteo > 25]))
            figura_par_impar = str(len(sorteo[sorteo %2 == 0])) +  " / " + str(len(sorteo[sorteo %2 != 0]))

            bajo_alto[figura_bajo_alto] += 1
            par_impar[figura_par_impar] += 1               
        
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
        self.figuras_combinaciones()

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
            titulo = "Estrellas"
            print("*" * len(titulo))
            print(titulo)
            print("*" * len(titulo))
            estrellas = []
            for e in range(len(self.__numeros_adicionales)):
                estrellas.append([int(x) for x in self.__numeros_adicionales[e].split(" ")])               
            estrellas = np.array(estrellas)
            self.apariciones_ausencias(bolas_estrellas, estrellas) 

        print("Mostrando estadísticas de los últimos ", len(self.__combinaciones), " resultados")
    

if __name__ == "__main__":
    #sorteo_elegido = Sorteo(["Euromillones","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva=20220717&fechaFinInclusiva=20230327", 5, 2, 50])
    #sorteo_elegido = Sorteo(["El Gordo de la Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=20220506&fechaFinInclusiva=20230308", 5, 1, 54])
    #sorteo_elegido = Sorteo(["Bonoloto","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&fechaInicioInclusiva=20220205&fechaFinInclusiva=20230308", 6, 2, 49])
    sorteo_elegido = Sorteo(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206", 6, 2, 49])

    #Primitiva.historial_combinaciones(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206"])
    #sorteo_elegido.estadisticas()
    #sorteo_elegido._Sorteo__combinaciones
    sorteo_elegido.ultimas_combinaciones()
    print(list(sorteo_elegido._Sorteo__joker))
    # print(list(sorteo_elegido._Sorteo__numeros_bajos_altos))
    #sorteo_elegido._Sorteo__numeros_bajos_altos