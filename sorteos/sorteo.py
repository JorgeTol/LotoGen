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
    
    # Devuelve el número de apariciones de una bola y los sorteos que lleva sin aparecer.
    # Return array [bola, apariciones, sorteos ausentes]
    def apariciones_ausencias(self, total_bolas, sorteos):
        # Crear el listado de todas las bolas
        n_bolas = [x for x in range(1, total_bolas + 1)]        
        resultado = []
        num_sorteos = len(sorteos)
        for bola in n_bolas:
            apariciones = len(sorteos[sorteos == bola])
            porcentaje = int((apariciones / num_sorteos) * 100)
            # Calcular días sin aparecer
            sorteos_ausente = 0
            for sorteo in sorteos:
                if bola not in sorteo:
                    sorteos_ausente += 1
                else:
                    break
            resultado.append([bola, apariciones, porcentaje, sorteos_ausente])
        return np.array(resultado)
        
    # Devuelve las estadísticas por figuras, nº bajo / alto y par / impar
    # Return array [figura, bajos / altos, pares / impares]
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
        figuras = bajo_alto.keys()
        resul_bajo_alto = bajo_alto.values()
        resul_par_impar = par_impar.values()
        
        return np.array([list(figuras), list(resul_bajo_alto), list(resul_par_impar)], dtype=object)
        
    
    # Imprime tablas con distintas estadísticas: 
    # - Primera tabla: Apariciones por figuras (nº bajos y altos, pares e impares) 
    # - Segunda tabla: Nº de apariciones por bola y días ausentes.
    # - Tercera tabla (Euromillones): Igual que la segunda tabla pero para las estrellas.
    # 
    def estadisticas(self):
        # ############
        # Primera tabla: 
        #     Número de veces que ha aparicido una figura (nºbajo/alto y par/impar)
        # ############
        tabla = PrettyTable()
        resultados = self.figuras_combinaciones()
        titulo_columna = ["Figuras"]
        for cabecera in resultados[0]:
            titulo_columna.append(cabecera)
        tabla.field_names = titulo_columna
        fila_bajo_alto = np.insert(resultados[1], 0, "Bajo / Alto")
        fila_par_impar = np.insert(resultados[2], 0, "Par / Impar")
        tabla.add_row(fila_bajo_alto)
        tabla.add_row(fila_par_impar)
        tabla.set_style(DOUBLE_BORDER)
        print(tabla)        

        # ############
        # Segunda tabla:
        #     Nº de veces que ha aparecido un número.
        #     Nº de sorteos que lleva sin aparecer un número.
        # ############
        tabla = PrettyTable()
        tabla.field_names = ["Bola", "Apariciones", "% apariciones", "Sorteos ausente"]
        resultados = self.apariciones_ausencias(self.__numero_bolas, self.__combinaciones) 
        for resultado in resultados:
            tabla.add_row([
                resultado[0],
                f"{str(resultado[1]):<2} " + "*" * resultado[1],
                f"{str(resultado[2]):<2}",
                f"{str(resultado[3]):<2} " + "*" * resultado[3]
            ])
        tabla.align["Apariciones"] = "l"
        tabla.align["Sorteos ausente"] = "l" 
        tabla.set_style(DOUBLE_BORDER)      
        print(tabla)

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
            resultados = self.apariciones_ausencias(bolas_estrellas, estrellas) 
            tabla.clear_rows()
            for resultado in resultados:
                tabla.add_row([
                    resultado[0],
                    f"{str(resultado[1]):<2} " + "*" * resultado[1],
                    f"{str(resultado[2]):<2} ",
                    f"{str(resultado[3]):<2} " + "*" * resultado[3]
                ])            
            print(tabla)
        print("Mostrando estadísticas de los últimos ", len(self.__combinaciones), " resultados")
    
    # Genera combinaciones utilizando las estadísticas, se pueden seleccionar todas (demasiado restrictivo) o sólo algunas comentando código
    # 1- Excluir las bolas que han aparecido en los últimos sorteos, por defecto 1
    # 2- Excluir las bolas que están por encima de la media de porcentaje de apariciones.
    # 3- Al generar las combinaciones, dar mas peso a las bolas con menor porcentaje de apariciones
    def combinaciones_por_estadisticas(self):
        estadisticas = self.apariciones_ausencias(self.__numero_bolas, self.__combinaciones)
        bolas_seleccionadas = estadisticas[:]
        
        # [Activación / Desactivación, valor de los filtros]
        filtros = {
            "Ausencias" : [True, 1],
            "Media porcentaje": [True, round(np.mean(estadisticas[:,2]),2)],
            "peso por porcentaje": True,
            "maximo resultados": 50 # Cantidad máxima de combinaciones a generar
        }       
        # 1- Seleccionar las bolas que cumplen el filtro de en sorteos ausentes.
        if filtros["Ausencias"][0]:
            while True:
                try:
                    input_sorteos_ausentes = input("Excluir las bolas que han aparecido en los últimos sorteos: [Por defecto " + str(filtros["Ausencias"][1]) + "] ")
                    assert input_sorteos_ausentes.isdigit() or input_sorteos_ausentes == "", "Solo números"
                    if input_sorteos_ausentes == "":
                        input_sorteos_ausentes = filtros["Ausencias"][1]
                    break
            
                except Exception as ex:
                    print(ex.args)

            bolas_seleccionadas = bolas_seleccionadas[bolas_seleccionadas[:, 3] > input_sorteos_ausentes]
        
        # 2- Seleccionar las bolas que cumplen el filtro de número de apariciones por debajo de la media en porcentaje.
        if filtros["Media porcentaje"]:            
            while True:   
                try:
                    input_media_porcentaje_apariciones = input("Excluir las bolas que tengan un porcentaje de aparición superior a: [Por defecto " + str(filtros["Media porcentaje"][1]) + "%] ")
                    assert input_media_porcentaje_apariciones.isdigit() or input_media_porcentaje_apariciones == "", "Solo números"
                    if input_media_porcentaje_apariciones == "":
                        input_media_porcentaje_apariciones = filtros["Media porcentaje"][1]               
                    break

                except Exception as ex:
                    print(ex.args)  

            bolas_seleccionadas = bolas_seleccionadas[bolas_seleccionadas[:, 2] < input_media_porcentaje_apariciones]       
        
        # 3- Dar mas probabilidades de aparecer en la combinacion a las bolas con menos apariciones y viceversa.
        if filtros["peso por porcentaje"]:
            ### Asignar a cada porcentaje de aparición de cada bola un valor population
            # Sacar los porcentajes únicos que hay en la tabla
            listado_porcentajes = np.flip(np.unique(bolas_seleccionadas[:, 2])) 
            # Crear la escala de population con tantos niveles como porcenajes existan.
            valores_population = np.linspace(0.00, 0.90, len(listado_porcentajes)) 
                        
            # Asignar los valores population a cada porcentaje {porcentajes : valor_population}
            dictionario = {listado_porcentajes[i]: valores_population[i] for i in range(len(listado_porcentajes))}
            # Asociar los valores population a cada bola según su porcentaje
            # Crear un array con los valores population que coincide en número y orden con las bolas seleccionadas
            valores_population = np.array([dictionario[b[2]] for b in bolas_seleccionadas])
            # Normalizar population (parametro de random.choice) para que la suma total sea 1 aprox.
            valores_population /= valores_population.sum()
        
        numero_resultados = 0
        # Extraer las figuras que mas apariciones tiene, dicha figura se aplicará a generador de combinaciones
        figuras = self.figuras_combinaciones()
        lista_bajos_altos = figuras[1].tolist() 
        index_max_fig_bajo = lista_bajos_altos.index(max(lista_bajos_altos)) # Buscar el índice del mayor valor
        cantidad_numeros_bajos = figuras[0][index_max_fig_bajo][0]
        lista_pares_impares = figuras[2].tolist() 
        index_max_fig_par = lista_pares_impares.index(max(lista_pares_impares)) # Buscar el índice del mayor valor
        cantidad_numeros_pares = figuras[0][index_max_fig_par][0]
        
        resultados = np.empty((0, self.__cantidad_bolas_combinacion), int)
        while numero_resultados < filtros["maximo resultados"]:
            if filtros["peso por porcentaje"]:
                combinacion = np.sort(np.random.choice(bolas_seleccionadas[:,0], self.__cantidad_bolas_combinacion, replace=False, p=valores_population))
            else:
                combinacion = np.sort(np.random.choice(bolas_seleccionadas[:,0], self.__cantidad_bolas_combinacion, replace=False))

            # Filtra las combinaciones que cumplen con las figuras con mas apariciones
            if (len(combinacion[combinacion < 26]) == int(cantidad_numeros_bajos)) and (len(combinacion[combinacion % 2 == 0]) == int(cantidad_numeros_pares)):
                if True:
                    resultados = np.append(resultados, [combinacion], axis=0)
                    numero_resultados += 1  
        
        print(resultados)
        print(f"Total de combinaciones generadas: {numero_resultados:>5}")
        print(f"Figura bajo / alto: {figuras[0][index_max_fig_bajo]:>22}")
        print(f"Figura par / impar: {figuras[0][index_max_fig_par]:>22}")
        
        tabla = PrettyTable()
            


if __name__ == "__main__":
    #sorteo_elegido = Sorteo(["Euromillones","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva=20220517&fechaFinInclusiva=20230427", 5, 2, 50])
    sorteo_elegido = Sorteo(["El Gordo de la Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=20220506&fechaFinInclusiva=20230308", 5, 1, 54])
    #sorteo_elegido = Sorteo(["Bonoloto","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=BONO&celebrados=true&fechaInicioInclusiva=20220205&fechaFinInclusiva=20230308", 6, 2, 49])
    #sorteo_elegido = Sorteo(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206", 6, 2, 49])

    #Primitiva.historial_combinaciones(["Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20221201&fechaFinInclusiva=20230206"])
    sorteo_elegido.combinaciones_por_estadisticas()
    #sorteo_elegido.estadisticas()
    #sorteo_elegido._Sorteo__combinaciones
    #sorteo_elegido.ultimas_combinaciones()
    #print(list(sorteo_elegido._Sorteo__joker))
    # print(list(sorteo_elegido._Sorteo__numeros_bajos_altos))
    #sorteo_elegido._Sorteo__numeros_bajos_altos