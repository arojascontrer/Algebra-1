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
    max_length = max(len(linea) for linea in lineas)
    centered_title = "\n".join(linea.center(max_length) for linea in lineas)
    print(centered_title)

def limpiapantallas():
    """Limpia la pantalla de la terminal según el sistema operativo."""
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_menu():
    print("\nMenú de opciones:")
    print("1. Entrada de datos")
    print("2. División sintética de polinomios")
    print("3. Sistema de Ecuaciones por Gauss-Jordan")
    print("4. Operaciones con matrices")
    print("5. Créditos")
    print("6. Salir")

def obtener_coeficientes(polinomio: str) -> np.ndarray:
    """
    Convierte un string de polinomio en un array de coeficientes.
    Ejemplo: "2x^2 - 3x + 1" -> [2, -3, 1]
    """
    # Normalizar el polinomio
    polinomio = polinomio.replace(' ', '').replace('-', '+-').lower()
    if polinomio.startswith('+'):
        polinomio = polinomio[1:]
    
    # Dividir en términos
    terminos = polinomio.split('+')
    coeficientes = {}
    
    for termino in terminos:
        if not termino:
            continue
            
        # Procesar cada término
        if 'x' in termino:
            # Término con variable x
            if '^' in termino:
                # Término con potencia (ej: 2x^3)
                coef_str, exp_str = termino.split('x^')
                exponente = int(exp_str)
            else:
                # Término lineal (ej: 2x)
                coef_str = termino.replace('x', '')
                exponente = 1
                
            # Determinar coeficiente
            if coef_str == '' or coef_str == '+':
                coeficiente = 1
            elif coef_str == '-':
                coeficiente = -1
            else:
                coeficiente = float(coef_str)
        else:
            # Término constante
            exponente = 0
            coeficiente = float(termino)
            
        coeficientes[exponente] = coeficientes.get(exponente, 0) + coeficiente
    
    # Crear array ordenado de coeficientes
    if not coeficientes:
        return np.array([0])
        
    grado = max(coeficientes.keys())
    array_coeficientes = [coeficientes.get(i, 0) for i in range(grado, -1, -1)]
    return np.array(array_coeficientes)

def synthetic_division(coefficients: List[float], divisor: complex) -> Tuple[List[float], complex]:
    """Realiza la división sintética y retorna el cociente y el residuo."""
    n = len(coefficients)
    result = [0] * n
    result[0] = coefficients[0]
    
    for i in range(1, n):
        result[i] = coefficients[i] + result[i-1] * divisor
    
    return result[:-1], result[-1]

def find_roots(coefficients: List[float], tolerance: float = 1e-10) -> List[complex]:
    """Encuentra las raíces del polinomio usando el método de Newton-Raphson."""
    def evaluate(x):
        result = coefficients[0]
        for coef in coefficients[1:]:
            result = result * x + coef
        return result
    
    def derivative(x):
        result = coefficients[0] * (len(coefficients) - 1)
        for i in range(1, len(coefficients) - 1):
            result = result * x + coefficients[i] * (len(coefficients) - i - 1)
        return result
    
    roots = []
    working_coeffs = coefficients.copy()
    
    while len(working_coeffs) > 2:
        x = complex(1, 1)  # Punto inicial
        for _ in range(100):
            fx = evaluate(x)
            if abs(fx) < tolerance:
                break
            dfx = derivative(x)
            if abs(dfx) < tolerance:
                x += complex(0.1, 0.1)
                continue
            x_new = x - fx / dfx
            if abs(x_new - x) < tolerance:
                break
            x = x_new
        
        if abs(x.imag) < tolerance:
            x = complex(x.real, 0)
        
        roots.append(x)
        _, working_coeffs = synthetic_division(working_coeffs, x)
    
    if len(working_coeffs) == 3:
        a, b, c = working_coeffs
        discriminant = complex(b*b - 4*a*c)
        x1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        x2 = (-b - cmath.sqrt(discriminant)) / (2*a)
        roots.extend([x1, x2])
    elif len(working_coeffs) == 2:
        a, b = working_coeffs
        roots.append(-b/a)
    
    return roots

def get_multiplicity(root: complex, all_roots: List[complex], tolerance: float = 1e-10) -> int:
    """Determina la multiplicidad de una raíz."""
    count = 0
    for r in all_roots:
        if abs(r - root) < tolerance:
            count += 1
    return count

def format_linear_factor(root: complex, multiplicity: int) -> str:
    """
    Formatea un factor lineal con su multiplicidad.
    Por ejemplo: (x - 2) o (x - (3 + 2i))
    """
    # Redondear a 4 decimales para mejor presentación
    real_part = round(root.real, 4)
    imag_part = round(root.imag, 4)
    
    if abs(imag_part) < 1e-10:  # Es un número real
        if abs(real_part) < 1e-10:  # Si es prácticamente cero
            factor = "x"
        elif real_part >= 0:
            factor = f"(x - {real_part})"
        else:
            factor = f"(x + {-real_part})"
    else:  # Es un número complejo
        if imag_part >= 0:
            factor = f"(x - ({real_part} + {imag_part}i))"
        else:
            factor = f"(x - ({real_part} - {abs(imag_part)}i))"
    
    if multiplicity > 1:
        factor += f"^{multiplicity}"
    
    return factor

def factorize_polynomial(coefficients: List[float]) -> str:
    """
    Factoriza el polinomio en factores lineales.
    Retorna una cadena con la factorización completa.
    """
    # Encontrar raíces
    roots = find_roots(coefficients)
    
    # Agrupar raíces por multiplicidad
    processed_roots = []
    factors = []
    leading_coef = coefficients[0]
    
    # Formatear el coeficiente principal si no es 1
    result = "" if abs(leading_coef - 1) < 1e-10 else f"{leading_coef}"
    
    for root in roots:
        if any(abs(r - root) < 1e-10 for r in processed_roots):
            continue
            
        multiplicity = get_multiplicity(root, roots)
        factors.append(format_linear_factor(root, multiplicity))
        processed_roots.append(root)
    
    # Si no hay factores, retornar solo el coeficiente principal
    if not factors:
        return str(leading_coef)
    
    # Unir todos los factores
    if result and factors:
        result += " * "
    result += " * ".join(factors)
    
    return result

def format_polynomial(coefficients: np.ndarray) -> str:
    """Formatea un polinomio a partir de sus coeficientes."""
    terms = []
    degree = len(coefficients) - 1
    
    for i, coef in enumerate(coefficients):
        if abs(coef) < 1e-10:
            continue
            
        current_degree = degree - i
        if current_degree == 0:
            terms.append(f"{coef:g}")
        elif current_degree == 1:
            if abs(coef - 1) < 1e-10:
                terms.append("x")
            elif abs(coef + 1) < 1e-10:
                terms.append("-x")
            else:
                terms.append(f"{coef:g}x")
        else:
            if abs(coef - 1) < 1e-10:
                terms.append(f"x^{current_degree}")
            elif abs(coef + 1) < 1e-10:
                terms.append(f"-x^{current_degree}")
            else:
                terms.append(f"{coef:g}x^{current_degree}")
    
    if not terms:
        return "0"
    
    result = terms[0]
    for term in terms[1:]:
        if term[0] == '-':
            result += f" {term}"
        else:
            result += f" + {term}"
    
    return result

def format_complex_number(num: complex, precision: int = 4) -> str:
    """
    Formatea un número complejo de manera legible.
    """
    real = round(num.real, precision)
    imag = round(num.imag, precision)
    
    if abs(imag) < 1e-10:  # Número real
        return f"{real:.{precision}f}"
    elif abs(real) < 1e-10:  # Número imaginario puro
        if abs(imag - 1) < 1e-10:
            return "i"
        elif abs(imag + 1) < 1e-10:
            return "-i"
        else:
            return f"{imag:.{precision}f}i"
    else:  # Número complejo
        if imag > 0:
            return f"{real:.{precision}f} + {imag:.{precision}f}i"
        else:
            return f"{real:.{precision}f} - {abs(imag):.{precision}f}i"

def divsint():
    """Función principal para la división sintética de polinomios."""
    limpiapantallas()
    mostrar_titulo()
    print("\nDivisión Sintética de Polinomios")
    print("================================")
    print("Ingrese el polinomio en formato: ax^n + bx^(n-1) + ... + kx + c")
    print("Ejemplo: 2x^3 - 3x^2 + 4x - 1")
    
    try:
        polinomio = input("\nIngrese el polinomio: ")
        coeficientes = obtener_coeficientes(polinomio)
        
        print(f"\nPolinomio ingresado: {format_polynomial(coeficientes)}")
        print("\nCoeficientes:", coeficientes)
        
        # Encontrar y mostrar todas las raíces
        roots = find_roots(coeficientes.tolist())
        print("\nRaíces encontradas:")
        root_multiplicities = {}
        for i, root in enumerate(roots, 1):
            mult = get_multiplicity(root, roots)
            if mult > 1:
                print(f"r{i} = {format_complex_number(root)} (multiplicidad: {mult})")
            else:
                print(f"r{i} = {format_complex_number(root)}")
        
        # Mostrar la factorización completa
        print("\nFactorización del polinomio:")
        factorizacion = factorize_polynomial(coeficientes.tolist())
        print(factorizacion)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    
    input("\nPresione Enter para continuar...")

def Entrada():
    limpiapantallas()
    mostrar_titulo()
    print("\nEntrada de datos")
    input("\nPresione Enter para continuar...")

def GaussJordan():
    limpiapantallas()
    mostrar_titulo()
    print("\nSistema de Ecuaciones por Gauss-Jordan")
    input("\nPresione Enter para continuar...")

def Opmat():
    limpiapantallas()
    mostrar_titulo()
    print("\nOperaciones con matrices")
    input("\nPresione Enter para continuar...")

def creditos():
    limpiapantallas()
    mostrar_titulo()
    print("\nHecho por:")
    print("Rojas Contreras Aarón")
    print("Fuentes Llantada Marco Antonio")
    print("\nVersión 0.1.1")
    input("\nPresione Enter para continuar...")

def main():
    while True:
        limpiapantallas()
        mostrar_titulo()
        mostrar_menu()
        
        opcion = input("\nSeleccione una opción (1-6): ")
        
        if opcion == '1':
            Entrada()
        elif opcion == '2':
            divsint()
        elif opcion == '3':
            GaussJordan()
        elif opcion == '4':
            Opmat()
        elif opcion == '5':
            creditos()
        elif opcion == '6':
            print("\nSaliendo del programa.")
            break
        else:
            print("\nOpción no válida. Por favor")