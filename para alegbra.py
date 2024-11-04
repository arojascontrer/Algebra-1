import numpy as np
from fractions import Fraction

# Preguntar al usuario si desea usar números imaginarios
usar_imaginarios = input("¿Desea trabajar con números imaginarios? (s/n): ").lower() == 's'

# Función para crear una matriz con elementos ingresados por el usuario
def input_matriz(filas, columnas, usar_imaginarios):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            entrada = input(f"Ingrese el valor de la posición ({i+1},{j+1}): ")
            entrada = entrada.replace(" ", "").replace("i", "j")  # Reemplaza "i" con "j" si se usan imaginarios
            try:
                if "/" in entrada:
                    fila.append(Fraction(entrada))
                elif "j" in entrada and usar_imaginarios:
                    fila.append(complex(entrada))
                else:
                    fila.append(float(entrada) if "." in entrada else int(entrada))
            except ValueError:
                print("Entrada inválida, por favor ingrese un número entero, fracción o complejo.")
                return None
        matriz.append(fila)
    # Define el tipo de datos de la matriz según si se usan imaginarios o no
    return np.array(matriz, dtype=complex if usar_imaginarios else float)

# Funciones para operaciones específicas
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

# Menu de opciones
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
    opcion = int(input("Ingrese el número de la operación que desea realizar: "))
    return opcion

# Ingreso de dimensiones para las matrices
filas_A = int(input("Ingrese el número de filas para la matriz A: "))
columnas_A = int(input("Ingrese el número de columnas para la matriz A: "))

# Obtener opción seleccionada
opcion = menu()

# Verificación y ejecución de la opción
if opcion in [1, 2, 3]:
    # Operaciones básicas requieren dos matrices de mismas dimensiones
    filas_B = int(input("Ingrese el número de filas para la matriz B: "))
    columnas_B = int(input("Ingrese el número de columnas para la matriz B: "))
    if filas_A != filas_B or columnas_A != columnas_B:
        print("Error: Las matrices deben tener las mismas dimensiones.")
    else:
        print("Ingrese los valores para la matriz A:")
        A = input_matriz(filas_A, columnas_A, usar_imaginarios)
        print("\nIngrese los valores para la matriz B:")
        B = input_matriz(filas_B, columnas_B, usar_imaginarios)
        if opcion == 1:
            resultado = A + B
            print("\nResultado de A + B:")
        elif opcion == 2:
            resultado = A - B
            print("\nResultado de A - B:")
        elif opcion == 3:
            resultado = A @ B
            print("\nResultado de A x B:")
elif opcion == 4:
    # Matriz triangular
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    tipo = input("¿Desea matriz triangular superior o inferior? (superior/inferior): ")
    resultado = matriz_triangular(A, tipo)
    print(f"\nMatriz triangular {tipo}:")
elif opcion == 5:
    # Matriz diagonal
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    resultado = matriz_diagonal(A)
    print("\nMatriz diagonal:")
elif opcion == 6:
    # Verificar matriz escalar
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    es_escalar, resultado = matriz_escalar(A)
    print("\nEs matriz escalar:" if es_escalar else "No es matriz escalar.")
elif opcion == 7:
    # Traza
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    resultado = traza(A)
    print("\nTraza de la matriz A:", resultado)
elif opcion == 8:
    # Transposición
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    resultado = transposicion(A)
    print("\nTransposición de la matriz A:")
elif opcion == 9:
    # Conjugado
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    resultado = conjugado(A)
    print("\nConjugado de la matriz A:")
elif opcion == 10:
    # Conjugado transpuesto
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    resultado = conjugado_transpuesto(A)
    print("\nConjugado transpuesto de la matriz A:")
elif opcion == 11:
    # Potencia n-ésima
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    n = int(input("Ingrese el valor de n para la potencia: "))
    resultado = potencia(A, n)
    print(f"\nMatriz A elevada a la potencia {n}:")
elif opcion == 12:
    # Resolver ecuación Ax = B
    filas_B = int(input("Ingrese el número de filas para la matriz B: "))
    print("Ingrese los valores para la matriz A:")
    A = input_matriz(filas_A, columnas_A, usar_imaginarios)
    print("\nIngrese los valores para la matriz B:")
    B = input_matriz(filas_B, 1, usar_imaginarios)  # Matriz B es vector columna
    resultado = resolver_ecuacion(A, B)
    print("\nSolución de Ax = B:" if isinstance(resultado, np.ndarray) else resultado)
else:
    print("Opción no válida")

print(resultado)

