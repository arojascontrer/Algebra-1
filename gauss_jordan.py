import numpy as np

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