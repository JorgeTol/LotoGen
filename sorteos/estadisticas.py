#! /usr/bin/env python3

""""
    Generar estadísticas de los distintos sortéos, perfiles y figuras de las combinaciones
"""
import sorteos.resultados as resultados

# Estraer la combinación principal dependiendo del tipo de sorteo. Se eliminan complementarios, reintegros, etc.
# Return string
def extraer_combinacion(combinacion_completa, nombre_juego):
    if nombre_juego in ["Primitiva", "Bonoloto"]:
        combinacion = combinacion_completa.split(' - ', 5) # Pasar los números a una lista
        # complementario = combinacion[5][5:7] # Incluir el complementario al perfil de la combinación  NOTA: Descomentar para habilitar
        combinacion[5] = combinacion[5][0:2] # El último de la lista incluye complementario, reintegro, etc. Se eliminan.
        # combinacion.append(complementario) NOTA: Descomentar para habilitar

    if nombre_juego == "Euromillones":
        combinacion = combinacion_completa.split(' - ', 6) # Pasar los números a una lista
        combinacion = combinacion[0:5] # Los dos últimos números son las estrellas. Se eliminan. 
    
    if nombre_juego == "El Gordo de la Primitiva":
        combinacion = combinacion_completa.split(' - ', 4) # Pasar los números a una lista
        combinacion[4] = combinacion[4][0:2] # El último de la lista incluye complementario, reintegro, etc. Se eliminan.
    
    return combinacion    
        

# Devolver un perfil de la combinación con la cantidad de números menor o igual a 25 y mayores a 25
# Combinacion: str. Numeros de la combinacion (incluye complementarios, reintegros, etc)
# Nombre_juego: str. Identificador del juego, hay que diferenciar el número de números que tiene cada juego.
# Return String
def menor_mayor_25(combinacion_completa, nombre_juego):
    menor_igual = 0
    mayor = 0             
    
    combinacion = extraer_combinacion(combinacion_completa, nombre_juego)

    for num in combinacion:
        num = int(num)
        if num <= 25:
            menor_igual += 1
        else:
            mayor += 1        

    return str(menor_igual) + " / " + str(mayor)

# Devolver un perfil de la combinación con la cantidad de números pares e impares
# Combinacion: str. Numeros de la combinacion (incluye complementarios, reintegros, etc)
# Nombre_juego: str. Identificador del juego, hay que diferenciar el número de números que tiene cada juego.
# Return String
def pares_impares(combinacion_completa, nombre_juego):
    par = 0
    impar = 0
   
    combinacion = extraer_combinacion(combinacion_completa, nombre_juego)

    for num in combinacion:
        num = int(num)
        if num % 2 == 0:
            par += 1
        else:
            impar += 1
    
    return str(par) + " / " + str(impar)

# Mostrar el número de apariciones en el periodo de tiempo configurado
def num_apariciones(sorteo_elegido):
    resultados_sorteos = resultados.sorteos_json(sorteo_elegido)
    combinaciones_ganadoras = []
    for combinacion in resultados_sorteos:
        combinaciones_ganadoras.append(extraer_combinacion(combinacion["combinacion"],sorteo_elegido[0]))
    
    # Crear listado de bolas, tienen que ser str y con dos dígitos
    bolas = []
    for bola in range(1, 47):
        bola = str(bola)
        if len(bola) == 1:
            bola = "0" + bola
        bolas.append(bola)
        
    apariciones = {} # Almacenar Bola: numero de apariciones
    for bola in bolas:
        num_apariciones = 0
        for conbinacion in combinaciones_ganadoras:
            if bola in conbinacion:                
                num_apariciones += 1
        apariciones[bola] = num_apariciones
    
    apariciones_ord = dict(sorted(apariciones.items(), key=lambda x: x[1], reverse=True))
    
    for bola, apariciones in apariciones_ord.items():
        print(bola, "*" * apariciones)
    
    # df = pd.DataFrame({
    #     "Número" : bolas,
    #     "Apariciones" : apariciones
    # })
    # df.sort_values(by=['Apariciones'], inplace=True, ascending=False)
    # print(df)
    
    




if __name__ == "__main__":
    num_apariciones(["El Gordo de la Primitiva","https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=ELGR&celebrados=true&fechaInicioInclusiva=20220117&fechaFinInclusiva=20230217"] )