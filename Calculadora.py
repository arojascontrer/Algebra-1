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

def limpiapantallas():
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
    """
    Convierte un string de polinomio en un array de coeficientes.
    
    Args:
        polinomio: String del polinomio (ej: "x^2 + 1")
        
    Returns:
        numpy.ndarray: Array de coeficientes
    """
    # Eliminamos los espacios en blanco y verificamos que no esté vacío
    polinomio = polinomio.replace(' ', '')
    if not polinomio:
        raise ValueError("El polinomio no puede estar vacío")
    
    # Encontramos todos los términos válidos del polinomio
    terminos = re.findall(r'[+-]?(?:\d*\.?\d*)?x?\^?\d*', polinomio)
    
    # Filtramos términos vacíos o inválidos
    terminos = [t for t in terminos if t and t not in ['+', '-']]
    
    if not terminos:
        raise ValueError("No se encontraron términos válidos en el polinomio")

    # Creamos un diccionario para almacenar los coeficientes
    coeficientes = {}

    for termino in terminos:
        try:
            if 'x' in termino:
                if '^' in termino:
                    # Término con x elevado a una potencia (ej: 2x^3)
                    coef_str, exp_str = termino.split('x^')
                    exponente = int(exp_str) if exp_str else 1
                else:
                    # Término con x sin potencia (ej: 2x)
                    coef_str = termino.replace('x', '')
                    exponente = 1

                # Procesamos el coeficiente
                if coef_str in ['', '+']:
                    coeficiente = 1
                elif coef_str == '-':
                    coeficiente = -1
                else:
                    coeficiente = float(coef_str)
            else:
                # Término constante
                exponente = 0
                coeficiente = float(termino)

            # Sumamos el coeficiente si ya existe un término con ese exponente
            coeficientes[exponente] = coeficientes.get(exponente, 0) + coeficiente

        except ValueError as e:
            raise ValueError(f"Término inválido encontrado: {termino}")

    if not coeficientes:
        raise ValueError("No se pudo extraer ningún coeficiente válido")

    # Creamos el array de coeficientes
    grado_maximo = max(coeficientes.keys())
    arreglo_coeficientes = np.zeros(grado_maximo + 1)

    for exponente, coef in coeficientes.items():
        arreglo_coeficientes[exponente] = coef

    return arreglo_coeficientes

def encontrar_raices(coeficientes: np.ndarray) -> List[complex]:
    """
    Encuentra las raíces de un polinomio usando numpy.
    
    Args:
        coeficientes: Array de coeficientes del polinomio en orden ascendente de grado
        
    Returns:
        Lista de raíces complejas
    """
    # Invertimos el orden de los coeficientes para numpy.roots
    return np.roots(coeficientes[::-1])

def formatear_numero_complejo(num: complex, precision: int = 3) -> str:
    """
    Formatea un número complejo para mostrarlo de forma legible.
    
    Args:
        num: Número complejo
        precision: Número de decimales a mostrar
        
    Returns:
        String formateado del número complejo
    """
    real = round(num.real, precision)
    imag = round(num.imag, precision)
    
    if abs(imag) < 1e-10:  # Si la parte imaginaria es prácticamente cero
        return f"{real}"
    elif abs(real) < 1e-10:  # Si la parte real es prácticamente cero
        if abs(imag - 1) < 1e-10:
            return "i"
        elif abs(imag + 1) < 1e-10:
            return "-i"
        else:
            return f"{imag}i"
    else:
        signo = "+" if imag >= 0 else "-"
        if abs(abs(imag) - 1) < 1e-10:
            return f"{real} {signo} i"
        else:
            return f"{real} {signo} {abs(imag)}i"

def factorizar_polinomio(coeficientes: np.ndarray) -> str:
    """
    Factoriza un polinomio y retorna una representación en string de la factorización.
    
    Args:
        coeficientes: Array de coeficientes del polinomio en orden ascendente de grado
        
    Returns:
        String con la factorización del polinomio
    """
    # Encontrar las raíces
    raices = encontrar_raices(coeficientes)
    
    # Si el polinomio es de grado 0 o 1
    if len(coeficientes) <= 2:
        return "El polinomio no se puede factorizar más"
    
    # Construir la factorización
    factores = []
    coef_principal = coeficientes[-1]  # Coeficiente principal
    
    if abs(coef_principal - 1) > 1e-10:  # Si el coeficiente principal no es 1
        factores.append(str(coef_principal))
    
    for raiz in raices:
        factor = f"(x - ({formatear_numero_complejo(raiz)}))"
        factores.append(factor)
    
    return " × ".join(factores)

def Entrada():
    print("Función de entrada de datos ejecutada.")

def Divsint():
    """
    Función principal para la factorización de polinomios.
    """
    print("\n Factorización de Polinomios")
    print("="*26)
    print("Ingrese el polinomio en formato: ax^n + bx^(n-1) + ... + cx + d")
    print("Ejemplo: x^3 - 6x^2 + 11x - 6")
    
    while True:
        try:
            polinomio = input("Ingrese el polinomio: ")
            coeficientes = obtener_coeficientes(polinomio)
            print(f"Coeficientes: {coeficientes}")
            
            factorizacion = factorizar_polinomio(coeficientes)
            print("\nFactorización:")
            print(factorizacion)
            
            # Preguntamos si desea continuar
            continuar = input("\n¿Desea factorizar otro polinomio? (s/n): ").lower()
            if continuar != 's':
                break
            
        except Exception as e:
            print(f"\nError: Hubo un problema al procesar el polinomio: {str(e)}")
            print("Por favor, verifique el formato e intente nuevamente.")
            
            # Preguntamos si desea intentar de nuevo
            continuar = input("\n¿Desea intentar de nuevo? (s/n): ").lower()
            if continuar != 's':
                break

def GaussJordan():
    print("Función de sistema de ecuaciones por Gauss-Jordan ejecutada.")

def Opmat():
    print("Función de operaciones con matrices ejecutada.")

def main():

    while True:
        limpiapantallas()
        mostrar_titulo()  # Llamamos a la función para mostrar el título
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            Entrada()
        elif opcion == '2':
            limpiapantallas()
            Divsint()
            
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