import os
import platform
import re
import numpy as np
import cmath
from typing import List, Tuple, Union


def mostrar_titulo():
    titulo = r"""
   _____      _            _           _                   _____                  _            _               
  / ____|    | |          | |         | |                 |  __ \           /\   | |          | |              
 | |     __ _| | ___ _   _| | __ _  __| | ___  _ __ __ _  | |  | | ___     /  \  | | __ _  ___| |__  _ __ __ _ 
 | |    / _` | |/ __| | | | |/ _` |/ _` |/ _ \| '__/ _` | | |  | |/ _ \   / /\ \ | |/ _` |/ _ \ '_ \| '__/ _` |
 | |___| (_| | | (__| |_| | | (_| | (_| | (_) | | | (_| | | |__| |  __/  / ____ \| | (_| |  __/ |_) | | | (_| |
  \_____\__,_|_|\___|\__,_|_|\__,_|\__,_|\___/|_|  \__,_| |_____/ \___| /_/    \_\_|\__, |\___|_.__/|_|  \__,_|
                                                                                     __/ |                     
                                                                     |___/        
    """
    
    # Centrar el título
    lineas = titulo.splitlines()
    max_length = max(len(linea) for linea in lineas)  # Longitud de la línea más larga
    centered_title = "\n".join(linea.center(max_length) for linea in lineas)  # Centrar cada línea
    print(centered_title)
def limpiapantallas(): #función para clrscr dependiendo de el SO
    """Limpia la pantalla de la terminal."""
    
    sistema = platform.system()
    
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_menu():
    print("Menú de opciones:")
    print("1. Entrada de datos")
    print("2. División sintética de polinomios")
    print("3. Sistema de Ecuaciones por Gauss-Jordan")
    print("4. Operaciones con matrices")
    print("5. Créditos")
    print("6. Salir")

def obtener_coeficientes(polinomio):
    # Eliminamos los espacios en blanco del polinomio
    polinomio = polinomio.replace(' ', '')
    
    # Encontramos todos los términos del polinomio usando una expresión regular
    # La expresión regular busca términos que pueden incluir coeficientes y variables
    terminos = re.findall(r'[+-]?\d*\.?\d*x?\^?\d*', polinomio)

    # Creamos un diccionario para almacenar los coeficientes
    coeficientes = {}

    for termino in terminos:
        if 'x' in termino:
            if '^' in termino:
                # Si el término tiene una potencia
                parte_coef, parte_exp = termino.split('x^')
                exponente = int(parte_exp)
            else:
                # Si el término no tiene una potencia explícita
                parte_coef = termino[:-1]
                exponente = 1
            
            # Determinamos el coeficiente
            if parte_coef == '' or parte_coef == '+':
                coeficiente = 1
            elif parte_coef == '-':
                coeficiente = -1
            else:
                coeficiente = float(parte_coef)
        else:
            # Si el término es un número constante
            exponente = 0
            coeficiente = float(termino)

        # Almacenamos el coeficiente en el diccionario
        coeficientes[exponente] = coeficientes.get(exponente, 0) + coeficiente

    # Creamos un arreglo unidimensional con los coeficientes
    grado_maximo = max(coeficientes.keys())
    arreglo_coeficientes = np.zeros(grado_maximo + 1)

    for exponente, coef in coeficientes.items():
        arreglo_coeficientes[exponente] = coef

    return arreglo_coeficientes

def Entrada():
    print("Función de entrada de datos ejecutada.")

def Divsint():
    print("Función de división sintética de polinomios ejecutada.")

def GaussJordan():
    print("Función de sistema de ecuaciones por Gauss-Jordan ejecutada.")

def Opmat():
    print("Función de operaciones con matrices ejecutada.")

def main():
    limpiapantallas()
    mostrar_titulo()  # Llamamos a la función para mostrar el título
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == '1':
            Entrada()
        elif opcion == '2':
            polinomio = input("Introduce un polinomio:")
            coeficientes = obtener_coeficientes(polinomio)
            print(coeficientes)
        elif opcion == '3':
            GaussJordan()
        elif opcion == '4':
            Opmat()
        elif opcion == '5':
            limpiapantallas()
            mostrar_titulo()
            print("Hecho por:")
            print("Rojas Contreras Aarón")
            print("Fuentes Llantada Marco Antonio")
            print("")
            print("Versión 0.1.1")
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
