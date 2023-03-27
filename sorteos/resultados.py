#! /usr/bin/env python3

""""
    Módulo para mostrar últimas combinaciones con sus perfiles de número (pares/impares, menor/mayor 25)
"""
import urllib.request
import json
from datetime import datetime
import locale
import sorteos.estadisticas as estadisticas
from prettytable import PrettyTable

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

resultados_sorteos = ""    # Donde de almacenará los datos de los sorteos en json

# Descargar en formato json listado de sorteos
def sorteos_json(sorteo_elegido):
    with  urllib.request.urlopen(sorteo_elegido[1]) as f:
        resultados_sorteos = f.read().decode('utf-8')
        resultados_sorteos = json.loads(resultados_sorteos)
    
    return resultados_sorteos


# Generar listado de los últimos sorteos. Columnas fecha, combinación, sorteo secundario (si lo hay) y perfil de la combinación
# Return string
def ultimas_combinaciones(sorteo_elegido):
    # Inicializar los arrays que contendrán los datos de las columnas
   

    resultados_sorteos = sorteos_json(sorteo_elegido)
   
   
    
    tabla = PrettyTable()
    columnas = ["Fecha sorteo", "Combinacion ganadora", "<= 25 / > 25", "Par / Impar"]
    if sorteo_elegido[0] == "Primitiva":
        columnas.append("joker")
    tabla.field_names = columnas
    
    
    
    for datos_sorteo in resultados_sorteos:
        filas = []
        fecha = datetime.fromisoformat(datos_sorteo["fecha_sorteo"])
        filas.append(fecha.strftime("%d/%m/%Y"), )
        if sorteo_elegido[0] in ["Primitiva", "Bonoloto", "El Gordo de la Primitiva"]: 
            filas.append(datos_sorteo["combinacion"])
            
        if sorteo_elegido[0]  == "Euromillones":
            numeros_principales = datos_sorteo["combinacion"].rsplit(" - ", maxsplit=2)[0] # Obtiene la combinación
            estrellas = datos_sorteo["combinacion"].rsplit(" - ", maxsplit=2)[1] + " - " + datos_sorteo["combinacion"].rsplit(" - ", maxsplit=2)[2]   # Obtiene las estrellas
            filas.append(numeros_principales +"  E: " + estrellas)
            
        filas.append(estadisticas.menor_mayor_25(datos_sorteo["combinacion"], sorteo_elegido[0]))
        filas.append(estadisticas.pares_impares(datos_sorteo["combinacion"], sorteo_elegido[0]).center(11))
            
        if sorteo_elegido[0] == "Primitiva":
            filas.append(datos_sorteo["joker"]["combinacion"])
        
        tabla.add_row(filas) 
              
    print(tabla)

    



if __name__ == "__main__":
    #print(menor_mayor_25("06 - 16 - 24 - 28 - 32 - 46 C(17) R(9)", "Primitiva"))
    ultimas_combinaciones(["Euromillones","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva=20221117&fechaFinInclusiva=20230217"] )
    