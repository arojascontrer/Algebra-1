import os
import platform
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
    # Detectar el sistema operativo
    sistema = platform.system()
    
    if sistema == "Windows":
        os.system("cls")  # Comando para limpiar la pantalla en Windows
    else:
        os.system("clear")  # Comando para limpiar la pantalla en Linux y otros sistemas Unix


def mostrar_menu():
    print("Menú de opciones:")
    print("1. Entrada de datos")
    print("2. División sintética de polinomios")
    print("3. Sistema de Ecuaciones por Gauss-Jordan")
    print("4. Operaciones con matrices")
    print("5. Salir")

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
            Divsint()
        elif opcion == '3':
            GaussJordan()
        elif opcion == '4':  # Cambiado de '3' a '4'
            Opmat()
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
