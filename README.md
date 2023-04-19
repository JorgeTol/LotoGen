<p align="left">
   <img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green?style=plastic&logo=appveyor">
   <img src="https://img.shields.io/badge/PYTHON-3.10-blue?style=plastic&logo=appveyor">
   <img src="https://img.shields.io/badge/Platform-win | ios | linux-grey?style=plastic&logo=appveyor">
</p>

# Loterias y apuestas

## Introducción
Este repositorio desarrollado integramente en Python se creó originalmente como parte de un ejercicio de aprendizaje de dicho lenguaje. Posteriormente se ha ido desarrollando e implementando más funciones, además de las que se irán añadiendo en un futuro.
Siéntete libre de aportar nuevas funcionalidades, sugerencias de mejoras de código o cualquier otra idea.

## ¿Qué hace esta aplicación?
Realiza consultas y análisis sobre los últimos sorteos, creando estadísticas y generando combinaciones.

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
    * Nº de sortéos que un número está ausente.
- Generador de combinaciones:
    * En base a las estadísticas.
    * Utilizando un modelo de aprendizaje automático.
    * Backtest. *Proximamente*

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
        Este repositorio está creado con fines de aprendizaje, poder visualizar las combinaciones de los sorteos realizados, consultar estadísticas y generar **posibles** combinaciones. **No utilizar para hacer un número de apuestas que no te puedes permitir. Juega con moderación.**
    </tr>
  </tbody>
</table>

## Instalación
El repositorio puede ejecutarse en cualquier computadora que tenga Python instalado, recomendable la versión 3.10, no se han realizado test en versiones anteriores.

Para comprobar la version, en windows ejecutar CMD, en IOs y Linux ejercutar la terminal.

```python3 --version```. Debería de mostrar algo así ```Python 3.10.x```

Plataformas:
- Linux. Viene instalado por defecto en todas las distribuciones. En caso de no tener la versión correcta

```sudo apt update```

```sudo apt install python3.10```

- Windows y macOS. Descargar el instalador desde la página de Python https://www.python.org/downloads/ y seguir las instrucciones.

Descargar el repositorio directamente desde la opción de descargas o utilizando Git.

```https://github.com/JorgeTol/LotoGen.git```

Una vez descargado nos ubicamos en la carpeta e instalamos las dependencias necesarias

```pip install -r requirements.txt```

En el caso de tener que instalar pip (Es un gestor de paquetes) en el siguiente enlace tienes los pasos https://pip.pypa.io/en/stable/installation/

Si no ha ocurrido ningún error ya se puede ejecutar el repositorio.


