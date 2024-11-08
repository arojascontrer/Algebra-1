import os
import platform
import re
import numpy as np
import cmath
from typing import List, Tuple, Union
from fractions import Fraction
from sympy import Matrix, pretty

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
    print("1. Operaciones con matrices")
    print("2. División sintética de polinomios")
    print("3. Sistema de Ecuaciones por Gauss-Jordan")
    print("4. Créditos")
    print("5. Salir")

def mostrar_credits():
    print("\n=== Créditos ===")
    print("Hecho por:")
    print("Rojas Contreras Aarón")
    print("Fuentes Llantada Marco Antonio")
    print("Valle Alvarez Carlos David")
    print("Versión 1.0.0")
    input("\nPresione Enter para continuar...")

# Función para detectar el tipo de número y convertirlo
def convertir_entrada(entrada):
    entrada = entrada.replace(" ", "").replace("i", "j")  # Reemplaza "i" con "j" para números complejos en Python
    try:
        if "/" in entrada:
            return Fraction(entrada)  # Convierte a fracción si contiene "/"
        elif "j" in entrada:
            return complex(entrada)   # Convierte a número complejo si contiene "j"
        else:
            return float(entrada) if "." in entrada else int(entrada)  # Float o int según corresponda
    except ValueError:
        print("Entrada inválida. Intente de nuevo.")
        return None

# Función para crear una matriz a partir de entradas del usuario
def input_matriz(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            while True:
                entrada = input(f"Ingrese el valor de la posición ({i+1},{j+1}): ")
                valor = convertir_entrada(entrada)
                if valor is not None:
                    fila.append(valor)
                    break
                else:
                    print("Por favor, ingrese un número válido.")
        matriz.append(fila)
    return np.array(matriz)

# Función para imprimir la matriz en formato ordenado
def mostrar_matriz(matriz):
    # Convertir la matriz de numpy a una matriz de SymPy para una mejor visualización
    matriz_sympy = Matrix(matriz.tolist())
    print(pretty(matriz_sympy))

# Funciones para operaciones específicas
def matriz_inversa(A):
    if np.linalg.det(A) == 0:
        return "La matriz no tiene inversa (determinante es cero)."
    else:
        return np.linalg.inv(A)

def matriz_triangular(A, tipo="superior"):
    return np.triu(A) if tipo == "superior" else np.tril(A)

def matriz_diagonal(A):
    return np.diag(np.diag(A))

def matriz_escalar(A):
    if np.allclose(np.diag(A), A[0, 0] * np.eye(A.shape[0])):
        return True, A[0, 0] * np.eye(A.shape[0])
    return False, None

def traza(A):
    return np.trace(A)

def transposicion(A):
    return A.T

def conjugado(A):
    return np.conj(A)

def conjugado_transpuesto(A):
    return A.T.conj()

def potencia(A, n):
    return np.linalg.matrix_power(A, n)

def resolver_ecuacion(A, B):
    if A.shape[0] == A.shape[1] and A.shape[0] == B.shape[0]:
        return np.linalg.solve(A, B)
    else:
        return "No se puede resolver; la matriz A debe ser cuadrada y B debe tener dimensiones compatibles."

def menu():
    print("\nSeleccione la operación:")
    print("1: Sumar matrices")
    print("2: Restar matrices")
    print("3: Multiplicar matrices")
    print("4: Matriz triangular (superior o inferior)")
    print("5: Matriz diagonal")
    print("6: Verificar matriz escalar")
    print("7: Traza de una matriz")
    print("8: Transposición de una matriz")
    print("9: Conjugado de una matriz")
    print("10: Conjugado transpuesto")
    print("11: Potencia n-ésima de una matriz")
    print("12: Resolver ecuación matricial (Ax = B)")
    print("13: Inversa de una matriz")
    opcion = int(input("Ingrese el número de la operación que desea realizar: "))
    return opcion

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

def mostrar_galera_ruffini(coeficientes: list, divisor: float, resultados: list, residuo: float):
    """
    Muestra la división sintética en formato visual de galera.
    """
    # Primera línea: coeficientes originales
    print("\n" + "="*50)
    coef_str = "    "
    for c in coeficientes:
        coef_str += f"{c:4d}  "
    print(coef_str)
    
    # Segunda línea: números que se bajan
    div_str = f"{divisor:2d} │"
    for i in range(len(resultados)):
        div_str += "    "  # Espacios para alinear
        div_str += f"↓"
    print(div_str)
    
    # Tercera línea: resultados de multiplicación
    mul_str = "   "
    for r in resultados:
        mul_str += f"{r:4d}  "
    print(mul_str)
    
    # Línea final: resultados
    print("   " + "-"*(len(coef_str)-3))
    res_str = "    "
    for r in resultados:
        res_str += f"{r:4d}  "
    res_str += f"{int(residuo):4d}"
    print(res_str + "\n")

def ruffini_visual(coeficientes: list, divisor: float, mostrar: bool = False) -> tuple:
    """
    Realiza la división sintética mostrando el proceso visual solo si mostrar=True.
    """
    n = len(coeficientes)
    resultados = [coeficientes[0]]
    
    for i in range(1, n):
        valor = coeficientes[i] + (divisor * resultados[i-1])
        resultados.append(valor)
    
    residuo = resultados.pop()
    
    if mostrar:
        mostrar_galera_ruffini(coeficientes, divisor, resultados, residuo)
        
    return resultados, residuo

def probar_raices_ruffini(coeficientes: list) -> list:
    """
    Prueba sistemáticamente números enteros para encontrar raíces,
    mostrando solo los intentos exitosos.
    """
    raices = []
    coef_actual = coeficientes.copy()
    
    while len(coef_actual) > 1:
        raiz_encontrada = False
        # Probar números del 1 al 100 y sus negativos alternadamente
        for i in range(1, 101):
            for divisor in [i, -i]:
                cociente, residuo = ruffini_visual(coef_actual, divisor, mostrar=False)
                
                if abs(residuo) < 1e-10:
                    print(f"\n¡Raíz encontrada!: {divisor}")
                    # Mostrar el proceso visual solo cuando encontramos una raíz
                    ruffini_visual(coef_actual, divisor, mostrar=True)
                    raices.append(divisor)
                    coef_actual = cociente
                    raiz_encontrada = True
                    break
            if raiz_encontrada:
                break
                
        if not raiz_encontrada:
            print("\nNo se encontraron más raíces racionales por Ruffini")
            break
            
    return raices

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
            polinomio = input("\nIngrese el polinomio: ")
            coeficientes = obtener_coeficientes(polinomio)
            coef_list = [int(c) if c.is_integer() else c for c in coeficientes[::-1]]
            
            print("\nBuscando raíces por el método de Ruffini:")
            raices_ruffini = probar_raices_ruffini(coef_list)
            
            if raices_ruffini:
                print("\nRaíces encontradas por Ruffini:", raices_ruffini)
                
                print("\nComprobando todas las raíces con numpy.roots:")
                raices_np = encontrar_raices(coeficientes)
                print("Todas las raíces (incluyendo complejas):")
                for i, raiz in enumerate(raices_np, 1):
                    print(f"Raíz {i}: {formatear_numero_complejo(raiz)}")
                
                print("\nFactorización completa:")
                print(factorizar_polinomio(coeficientes))
            else:
                print("\nImposible encontrar raíces con Ruffini")
                print("Encontrando raíces por factorización...")
                raices_np = encontrar_raices(coeficientes)
                print("\nRaíces encontradas:")
                for i, raiz in enumerate(raices_np, 1):
                    print(f"Raíz {i}: {formatear_numero_complejo(raiz)}")
                
                print("\nFactorización completa:")
                print(factorizar_polinomio(coeficientes))
            
            continuar = input("\n¿Desea factorizar otro polinomio? (s/n): ").lower()
            if continuar != 's':
                break
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Por favor, verifique el formato e intente nuevamente.")
            continuar = input("\n¿Desea intentar de nuevo? (s/n): ").lower()
            if continuar != 's':
                break

def GaussJordan():
    while True:
        n = int(input("Introduce el número de ecuaciones (n): "))  # Número de filas
        m = int(input("Introduce el número de variables (m): "))   # Número de columnas
        # Solicitar los coeficientes de la matriz A 
        print("Introduce los coeficientes de las ecuaciones (filas de la matriz A):")
        A = np.zeros((n, m))  # Crear una matriz de ceros de tamaño n x m
        for i in range(n):
            A[i, :] = list(map(float, input(f"Coeficientes de la ecuación {i+1}: ").split()))

        # Solicitar los términos independientes (columna B)
        print("Introduce los términos independientes (B):")
        B = np.zeros((n, 1))  # Crear un vector columna de ceros
        for i in range(n):
            B[i, 0] = float(input(f"Término independiente de la ecuación {i+1}: "))

        # Crear la matriz aumentada [A | B]
        AB = np.concatenate((A, B), axis=1)
        ABO = np.copy(AB)

        # Mostrar la matriz aumentada inicial
        print("\nMatriz aumentada inicial:")
        print(ABO)

        # Pivoteo parcial por filas
        for i in range(0, n-1):
            columna = abs(AB[i:, i])
            dondemax = np.argmax(columna)
            
            if dondemax != 0:
                # Intercambia las filas
                temporal = np.copy(AB[i, :])
                AB[i, :] = AB[dondemax + i, :]
                AB[dondemax + i, :] = temporal

            # Imprimir la matriz después del pivoteo
            print(f"\nDespués del pivoteo en la fila {i+1}:")
            print(AB)

        AB1 = np.copy(AB)

        # Eliminación hacia adelante
        for i in range(0, n-1):
            pivote = AB[i, i]
            adelante = i + 1
            for k in range(adelante, n):
                factor = AB[k, i] / pivote
                AB[k, :] = AB[k, :] - AB[i, :] * factor

            # Imprimir la matriz después de cada paso de eliminación hacia adelante
            print(f"\nDespués de la eliminación hacia adelante en la fila {i+1}:")
            print(AB)

        AB2 = np.copy(AB)

        # Eliminación hacia atrás
        for i in range(n-1, -1, -1):
            pivote = AB[i, i]
            AB[i, :] = AB[i, :] / pivote  # Normalizar la fila para que el pivote sea 1
            for k in range(i-1, -1, -1):  # Eliminar los elementos por encima del pivote
                factor = AB[k, i]
                AB[k, :] = AB[k, :] - AB[i, :] * factor

            # Imprimir la matriz después de cada paso de eliminación hacia atrás
            print(f"\nDespués de la eliminación hacia atrás en la fila {i+1}:")
            print(AB)

        # La solución está en la última columna de AB
        X = np.copy(AB[:, -1])

        print("\nLa solución es:")
        print(X)

        continuar = input("\n¿Desea realizar otra operación? (s/n): ").lower()
        if continuar != 's':
            break

        

def Opmat():
    while True:
        limpiapantallas()
        opcion = menu()
        
        if opcion in range(1, 14):  # Opciones válidas del 1 al 13
            # Primero solicitamos las dimensiones de la matriz A
            filas_A = int(input("Ingrese el número de filas para la matriz A: "))
            columnas_A = int(input("Ingrese el número de columnas para la matriz A: "))
            
            # Para las operaciones que requieren dos matrices
            if opcion in [1, 2, 3]:
                filas_B = int(input("Ingrese el número de filas para la matriz B: "))
                columnas_B = int(input("Ingrese el número de columnas para la matriz B: "))
                
                if opcion in [1, 2] and (filas_A != filas_B or columnas_A != columnas_B):
                    print("Error: Las matrices deben tener las mismas dimensiones para suma y resta.")
                    input("\nPresione Enter para continuar...")
                    continue
                elif opcion == 3 and columnas_A != filas_B:
                    print("Error: El número de columnas de A debe ser igual al número de filas de B para multiplicación.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                print("\nIngrese los valores para la matriz A:")
                A = input_matriz(filas_A, columnas_A)
                print("\nIngrese los valores para la matriz B:")
                B = input_matriz(filas_B, columnas_B)
                
                if opcion == 1:
                    resultado = A + B
                    print("\nResultado de A + B:")
                elif opcion == 2:
                    resultado = A - B
                    print("\nResultado de A - B:")
                elif opcion == 3:
                    resultado = A @ B
                    print("\nResultado de A × B:")
                
                mostrar_matriz(resultado)
            
            # Para operaciones que requieren una sola matriz
            else:
                print("\nIngrese los valores para la matriz A:")
                A = input_matriz(filas_A, columnas_A)
                
                if opcion == 4:
                    tipo = input("¿Desea matriz triangular superior o inferior? (superior/inferior): ").lower()
                    resultado = matriz_triangular(A, tipo)
                    print(f"\nMatriz triangular {tipo}:")
                    mostrar_matriz(resultado)
                
                elif opcion == 5:
                    resultado = matriz_diagonal(A)
                    print("\nMatriz diagonal:")
                    mostrar_matriz(resultado)
                
                elif opcion == 6:
                    es_escalar, resultado = matriz_escalar(A)
                    if es_escalar:
                        print("\nEs matriz escalar:")
                        mostrar_matriz(resultado)
                    else:
                        print("No es matriz escalar.")
                
                elif opcion == 7:
                    resultado = traza(A)
                    print("\nTraza de la matriz A:", resultado)
                
                elif opcion == 8:
                    resultado = transposicion(A)
                    print("\nTransposición de la matriz A:")
                    mostrar_matriz(resultado)
                
                elif opcion == 9:
                    resultado = conjugado(A)
                    print("\nConjugado de la matriz A:")
                    mostrar_matriz(resultado)
                
                elif opcion == 10:
                    resultado = conjugado_transpuesto(A)
                    print("\nConjugado transpuesto de la matriz A:")
                    mostrar_matriz(resultado)
                
                elif opcion == 11:
                    n = int(input("Ingrese el valor de n para la potencia: "))
                    resultado = potencia(A, n)
                    print(f"\nMatriz A elevada a la potencia {n}:")
                    mostrar_matriz(resultado)
                
                elif opcion == 12:
                    if filas_A != columnas_A:
                        print("Error: La matriz A debe ser cuadrada para resolver Ax = B")
                        input("\nPresione Enter para continuar...")
                        continue
                    
                    print("\nIngrese los valores para el vector B:")
                    B = input_matriz(filas_A, 1)  # B debe ser un vector columna
                    resultado = resolver_ecuacion(A, B)
                    
                    if isinstance(resultado, str):
                        print(resultado)
                    else:
                        print("\nSolución de Ax = B:")
                        mostrar_matriz(resultado)
                
                elif opcion == 13:
                    if filas_A != columnas_A:
                        print("Error: La matriz debe ser cuadrada para calcular su inversa")
                        input("\nPresione Enter para continuar...")
                        continue
                    
                    resultado = matriz_inversa(A)
                    if isinstance(resultado, str):
                        print(resultado)
                    else:
                        print("\nInversa de la matriz A:")
                        mostrar_matriz(resultado)
            
            # Preguntar si desea realizar otra operación
            continuar = input("\n¿Desea realizar otra operación? (s/n): ").lower()
            if continuar != 's':
                break
        else:
            print("Opción no válida")
            input("\nPresione Enter para continuar...")

def main():

    while True:
        limpiapantallas()
        mostrar_titulo()  # Llamamos a la función para mostrar el título
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == '1':
            Opmat()
        elif opcion == '2':
            limpiapantallas()
            Divsint()
        elif opcion == '3':
            GaussJordan()
        elif opcion == '4':
            limpiapantallas()
            mostrar_titulo()
            mostrar_credits()
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()