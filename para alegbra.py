import numpy as np
from fractions import Fraction
from sympy import Matrix, pretty

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

# Menú de opciones
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

# Ingreso de dimensiones para las matrices
filas_A = int(input("Ingrese el número de filas para la matriz A: "))
columnas_A = int(input("Ingrese el número de columnas para la matriz A: "))

# Obtener opción seleccionada
opcion = menu()

# Verificación y ejecución de la opción
if opcion in [1, 2, 3]:
    filas_B = int(input("Ingrese el número de filas para la matriz B: "))
    columnas_B = int(input("Ingrese el número de columnas para la matriz B: "))
    if filas_A != filas_B or columnas_A != columnas_B:
        print("Error: Las matrices deben tener las mismas dimensiones.")
    else:
        print("Ingrese los valores para la matriz A:")
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
            print("\nResultado de A x B:")
        mostrar_matriz(resultado)
elif opcion == 4:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    tipo = input("¿Desea matriz triangular superior o inferior? (superior/inferior): ")
    resultado = matriz_triangular(A, tipo)
    print(f"\nMatriz triangular {tipo}:")
    mostrar_matriz(resultado)
elif opcion == 5:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = matriz_diagonal(A)
    print("\nMatriz diagonal:")
    mostrar_matriz(resultado)
elif opcion == 6:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    es_escalar, resultado = matriz_escalar(A)
    if es_escalar:
        print("\nEs matriz escalar:")
        mostrar_matriz(resultado)
    else:
        print("No es matriz escalar.")
elif opcion == 7:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = traza(A)
    print("\nTraza de la matriz A:", resultado)
elif opcion == 8:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = transposicion(A)
    print("\nTransposición de la matriz A:")
    mostrar_matriz(resultado)
elif opcion == 9:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = conjugado(A)
    print("\nConjugado de la matriz A:")
    mostrar_matriz(resultado)
elif opcion == 10:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = conjugado_transpuesto(A)
    print("\nConjugado transpuesto de la matriz A:")
    mostrar_matriz(resultado)
elif opcion == 11:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    n = int(input("Ingrese el valor de n para la potencia: "))
    resultado = potencia(A, n)
    print(f"\nMatriz A elevada a la potencia {n}:")
    mostrar_matriz(resultado)
elif opcion == 12:
    filas_B = int(input("Ingrese el número de filas para la matriz B: "))
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    print("\nIngrese los valores para la matriz B:")
    B = input_matriz(filas_B, 1)
    resultado = resolver_ecuacion(A, B)
    if isinstance(resultado, np.ndarray):
        print("\nSolución de Ax = B:")
        mostrar_matriz(resultado)
    else:
        print(resultado)
elif opcion == 13:
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A)
    resultado = matriz_inversa(A)
    if isinstance(resultado, np.ndarray):
        print("\nInversa de la matriz A:")
        mostrar_matriz(resultado)
    else:
        print(resultado)
else:
    print("Opción no válida")


