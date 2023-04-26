<p align="left">
   <img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green?style=plastic&logo=appveyor">
   <img src="https://img.shields.io/badge/PYTHON-3.10-blue?style=plastic&logo=appveyor">
   <img src="https://img.shields.io/badge/Platform-win | ios | linux-grey?style=plastic&logo=appveyor">
</p>

# Loterias y apuestas

## Introducción
Este repositorio está desarrollado integramente en Python y utiliza algunas dependencias como Numpy. El proyecto siguen desarrollo, se irán implementando más funciones y mejorando las que ya tiene.
Siéntete libre de sugerir nuevas funcionalidades, mejoras de código o cualquier otra idea o error que puedas encontrar.

## ¿Qué hace esta aplicación?
Realiza consultas y análisis sobre los últimos sorteos, creando estadísticas y generando combinaciones. Todo desde la terminal de Linux o Mac y terminal CMD de Windows.

Actualmente están disponibles los siguienes sorteos:
- Primitiva.
- Bonoloto.
- Euromillones.
- El Gordo de la Primitiva.

Con cada sorteo hay varias operaciones que se pueden realizar:
- Visualización de los últimos sorteos.
- Estadísticas:
    * Apariciones por figura *numeros altos / numeros bajos, pares / impares*.
    * Nº de veces que ha salido un número.
    * Porcentaje de apariciones.
    * Nº de sorteos que lleva sin aparecer.
- Generador de combinaciones:
    * En base a las estadísticas.
    * Utilizando un modelo de aprendizaje automático. *Proximamente*
    * Backtest. Consulta los premios que se hubieran obtenido con la configuración elegida en el último sorteo. *Proximamente*

<table>
  <thead>
    <tr>
      <td align="left">
        :information_source: Aviso
      </td>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        <p>Los juego de azar son eso, azar. No es posible predecir o adivinar una combinación de números y más cuando las posibilidades son elevadísimas.
        Este repositorio está creado con fines de aprendizaje, poder visualizar las combinaciones de los sorteos realizados, consultar estadísticas y generar <b>posibles</b> combinaciones. <b>No utilizar para hacer un número de apuestas que no te puedas permitir. Juega con moderación.</b>
    </tr>
  </tbody>
</table>

## Instalación
El repositorio puede ejecutarse en cualquier computadora que tenga Python instalado, recomendable la versión 3.10, no se han realizado test en versiones anteriores.

Para comprobar la version, en Windows ejecutar CMD, en IOs y Linux ejercutar la terminal.

```python3 --version```. Debería de mostrar algo así ```Python 3.10.x```

Plataformas:
- Linux. Viene instalado por defecto en todas las distribuciones. En caso de no tener la versión correcta

```sudo apt update```

```sudo apt install python3.10```

- Windows y macOS. Descargar el instalador desde la página de Python https://www.python.org/downloads/ y seguir las instrucciones.

Descargar el repositorio directamente desde la opción de descargas o utilizando Git.

```git clone https://github.com/JorgeTol/LotoGen.git```

Una vez descargado nos ubicamos en la carpeta e instalamos las dependencias necesarias con el siguiente comando.

```pip install -r requirements.txt```

En el caso de tener que instalar pip (gestor de paquetes), en el siguiente enlace tienes los pasos https://pip.pypa.io/en/stable/installation/

Si no ha ocurrido ningún error ya se puede ejecutar el repositorio.

## Comenzando

Ejecutar ```python generador_inter.py```.
> Si hay varias versiones de python en el sistema y no está por defecto activada la version 3 ```python3 generador_inter.py```

Elegir el número correspondiente al sorteo. 

<img alt="Menú con un listado para elegir la Loteria." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Select_loterias.png">

Aparecerá un submenú con opciones a realizar.

<img alt="Opciones a realizar con el sorteo elegido." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Select_options.png">

## Ultimos sorteos.

En la tabla se muestran los últimos 80 sorteos realizados, incluye la fecha, combinación, números adicionales (reintegro, complementarios, estrellas, etc) y las figuras de la combinación. Los datos se actualizan automáticamente al último sorteo elegido.

<img alt="Tabla con los resultados de la lotería." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Ejemplo_tabla_sorteos.png">

## Estadísticas.

Genera dos tablas con las estadísticas de los últimos sorteos:

- 1ª tabla. Estadísticas de las figuras de la combinación. Números bajos (<26) / números altos (>25), números pares / números impares.
- 2ª tabla. Estadísticas de las bolas que entran en juego, número de apariciones, porcentaje de apariciones y sorteos ausentes.

En el sorteo de Euromillones también mostrará las estadísticas de las estrellas.

<img alt="Tabla con las estadísticas de los últimos sorteos." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Ejemplo_tabla_estadisticas.png">

## Generar combinaciones.

Dos métodos de generarlas, utilizando las estadísticas y usando un modelo de aprendizaje automático (en desarrollo).

<img alt="Menú con opciones para generar combinaciones." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Select_option_pronosticos.png">

### Crear combinaciones en base a las estadísticas.

Partiendo de la teoría de que todas las bolas tienen las mismas posibilidades de salir, a lo largo de los sorteos, estas tienden a aparecer un número de veces lo más parecido posible. 

> Entonces, las que han salido muy pocas veces o llevan varios sorteos sin salir tienen mas probabilidades de aparecer.

Las figuras de las combinaciones indican la relación de las bolas que la forman y siempre hay unas figuras que se repiten más que otras.

> Entonces, las combinaciones con las figuras mas repetidas tienen mas probabilidades de aparecer.

El generador utiliza los siguientes filtros:
 - Ausencias. Excluye las bolas que han aparecido en los últimos sorteos. Por defecto está seleccionado 1. 
 - Porcentaje de apariciones. Excluye las bolas que están por encima de la media.
 - Figuras. Las combinaciones que genera tienen las figuras que más se han repedido en los últimos sorteos.
 - Número de apariciones. Hace una ponderación para que tengan más probabilidades de aparecer las bolas que menos porcentaje tengan.  
 
 > Los anteriores parámetros son modificables. Durante el proceso se pedirá si se dedice modificar, dejar en blanco para mantener los valores por defecto. 

 
 Por defecto genera un máximo de 1000 combinaciones, depende de los filtros y valores aplicados. Se puede elegir que filtros quitar o añadir editando directamente el código en el archivo *sorteos/sorteo.py* , cambiando ```True``` por ```False```.
 
 ``` 
AUSENCIAS = True   # Incluir los números que llevan X sorteos sin salir.
PORCENTAJE = True  # Incluir los números que tienen una media de apariciones por debajo de la media.
FIGURAS = True     # Aplicar el filtro de figuras que mas se repiten. Nº bajo / Nº alto, pares / impares
POPULATION = False # Dar más probabilidades de aparición a los números que tienen un menor porcentaje de apariciones.
 ```
 
 En la consola se mostrará una tabla con la configuración y las primeras combinaciones generadas. En la carpeta raiz *pronosticos* se guardará un archivo de texto con todas las combinaciones, el nombre del archivo es el nombre del sorteo mas la fecha de generación de dicho archivo.

<img alt="Tablas con los pronósticos y los parámetros de configuración." src="https://github.com/JorgeTol/LotoGen/blob/develop/img/Ejemplo_tabla_pronosticos.png">

<hr \>
Se agradece que se reporte cualquier error.

Si quieres apoyar o agradecer este proyecto y que siga creciendo se admiten donaciones
<p>
  <a href="https://www.paypal.com/webapps/mpp/paypal-popup" title="Donación en Paypal"> <img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo"></a>
</p>
