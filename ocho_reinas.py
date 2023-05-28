"""
Problema de las 8 reinas
Universidad Panamericana
Inteligencia Artificial
Francisco Anaya Viveros
Joel Vázquez Anaya
Javier Vázquez Gurrola
Generación del archivo: 22/05/2023
Fecha de entrega: 01/06/2023
Versión 1.3
El código aquí presentado busca resolver de manera eficiente el problema de las 8 reinas con una implementación del algoritmo A* (A estrella)
Intrucciones: 

"""
"""Dependencia"""
import heapq
import random
import time

"""CLASES Y FUNCIONES DE APOYO"""

""" La función menu busca implementar un menú para facilitar el uso del programa, dando opciones variadas  que el usuario puede elegir """
def menu():
    while True:
        print("\nMenú:")
        print("1. Ejecutar código")
        print("2. Ejecutar código con información adicional")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            n = int(input("Ingresa el valor de N: "))
            initial_board = input("¿Deseas ingresar un estado inicial? (S/N): ")

            # Verificar si el usuario desea ingresar un estado inicial
            if initial_board.upper() == "S":
                print("Ingrese el estado inicial de las reinas:")
                board = []
                for _ in range(n):
                    row = input().split()
                    board.append([int(val) for val in row])
            else:
                board = None

            # Resolver el problema de las reinas utilizando el estado inicial proporcionado
            start_time = time.time()
            solution = solve_n_queens_a_star(n, board)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if solution is None:
                print("No existe una solución para el problema de las %d reinas." % n)
            else:
                print("\nEstado final del tablero (solución):\n")
                print_board(solution)
                
            print("\nTiempo de ejecución:", elapsed_time, "segundos\n")

        elif opcion == "2": #Opción con información adicional
            n = int(input("Ingresa el valor de N: "))
            initial_board = input("¿Deseas ingresar un estado inicial? (S/N): ")

            # Verificar si el usuario desea ingresar un estado inicial
            if initial_board.upper() == "S":
                print("Ingrese el estado inicial de las reinas:")
                board = []
                for _ in range(n):
                    row = input().split()
                    board.append([int(val) for val in row])
            else:
                board = None

            # Resolver el problema de las reinas utilizando el estado inicial proporcionado
            start_time = time.time()
            solution = solve_n_queens_a_star(n, board)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if solution is None:
                print("No existe una solución para el problema de las %d reinas." % n)
            else:
                print("Estado final del tablero (solución):")
                print_board(solution)

            print("\nTiempo de ejecución:", elapsed_time, "segundos\n")

        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")


"""La función print_board imprime el tablero en la consola."""
def print_board(board):
    for row in board:
        print(row)

"""El objetivo de la clase State es representar un estado del problema en el contexto del algoritmo A*. 
Cada objeto de la clase State almacena información sobre el tablero, la posición actual de la reina, 
el costo acumulado hasta ese estado y el valor heurístico asociado.
La clase State tiene los siguientes atributos:
board: una matriz que representa el tablero con las reinas colocadas.
row y col: las coordenadas de la próxima casilla a explorar.
cost: el costo acumulado para llegar al estado actual.
heuristic: la heurística estimada para el estado actual."""
class State:
    def __init__(self, board, row, col, cost, heuristic):
        self.board = board
        self.row = row
        self.col = col
        self.cost = cost
        self.heuristic = heuristic

#La clase State también define el método especial __lt__ que compara dos objetos State en función de la suma del costo y la heurística. 
#Esto permite utilizar la clase en una cola de prioridad para garantizar que los estados se expandan en el orden adecuado durante la búsqueda A*.
    def __lt__(self, other):
        # Método para comparar dos estados basado en la suma del costo y la heurística
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

"""La función get_random_initial_state(N) se utiliza para obtener un estado inicial aleatorio en el problema de las reinas. 
Esta función crea un tablero vacío de tamaño NxN y luego coloca N reinas de forma aleatoria en el tablero. 
Las reinas se colocan en filas diferentes y en columnas seleccionadas al azar, asegurando que no haya dos reinas en la misma columna. 
El resultado es un tablero que representa un estado inicial aleatorio para resolver el problema de las reinas, 
donde cada casilla con el valor 1 indica la presencia de una reina en esa posición del tablero."""
# Función para obtener un estado inicial aleatorio
def get_random_initial_state(N):
    board = [[0] * N for _ in range(N)]
    queens = random.sample(range(N), N)
    for row, col in enumerate(queens):
        board[row][col] = 1
    return board

"""FUNCIONES PRINCIPALES"""

""" La función calculate_heuristic calcula la heurística para un tablero dado. 
Recorre todas las posiciones del tablero y suma puntos por cada reina que esté en la misma fila, columna o diagonal. 
También suma puntos por cada reina en las diagonales secundarias.
La heurística se calcula contando el número de reinas que amenazan a otras reinas en el tablero:
Se inicializa la variable heuristic en 0.
Se recorre cada celda del tablero utilizando dos bucles for anidados, donde i representa la fila y j representa la columna.
Si la celda (i, j) contiene una reina (valor 1), se procede a verificar si hay otras reinas en la misma fila, misma columna o en las diagonales.
Para verificar si hay una reina en la misma fila, se utiliza otro bucle for desde 0 hasta N, donde k representa la columna. 
Si se encuentra una reina en la misma fila (en la posición (i, k) con k != j), se incrementa la heurística en 1.
Para verificar si hay una reina en la misma columna, se utiliza otro bucle for desde 0 hasta N, donde k representa la fila. 
Si se encuentra una reina en la misma columna (en la posición (k, j) con k != i), se incrementa la heurística en 1.
Para verificar las diagonales, se utilizan cuatro bucles for anidados con diferentes rangos y condiciones. 
Se recorren las diagonales principales y secundarias a partir de la posición de la reina en (i, j).
Para las diagonales principales, se verifica si hay una reina en las posiciones (i+k, j+k), (i-k, j-k), (i+k, j-k), (i-k, j+k) con k desde 1 hasta N-1. 
Si se encuentra una reina en cualquiera de estas posiciones, se incrementa la heurística en 1.
Para las diagonales secundarias, se verifica si hay una reina en las posiciones (i+k, j-k), (i-k, j+k), (i+k, j+k), (i-k, j-k) con k desde 1 hasta N-1. 
Si se encuentra una reina en cualquiera de estas posiciones, se incrementa la heurística en 1.
Al finalizar los bucles, se retorna el valor de la heurística, que representa el número de reinas que se amenazan mutuamente en el tablero.
"""
def calculate_heuristic(board, N):
    heuristic = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                # Verificar si hay una reina en la misma fila o diagonal
                for k in range(N):
                    if board[i][k] == 1 and k != j:
                        heuristic += 1
                    if board[k][j] == 1 and k != i:
                        heuristic += 1
                # Verificar si hay una reina en las diagonales secundarias
                for k in range(1, N):
                    if i + k < N and j + k < N and board[i + k][j + k] == 1:
                        heuristic += 1
                    if i - k >= 0 and j - k >= 0 and board[i - k][j - k] == 1:
                        heuristic += 1
                    if i + k < N and j - k >= 0 and board[i + k][j - k] == 1:
                        heuristic += 1
                    if i - k >= 0 and j + k < N and board[i - k][j + k] == 1:
                        heuristic += 1
    return heuristic


"""La función is_safe verifica si es seguro colocar una reina en una posición determinada del tablero. 
Comprueba si hay reinas en la misma fila, diagonal superior izquierda y diagonal inferior izquierda.
La función is_safe se encarga de verificar si es seguro colocar una reina en una determinada posición del tablero. 

Verificación de la misma fila:
Se recorre la fila desde la columna 0 hasta la columna anterior a la posición actual (col).
Si se encuentra una reina en alguna de las celdas de la misma fila (board[row][i] == 1), significa que ya hay una reina en esa fila y, por lo tanto, 
no es seguro colocar una reina en la posición actual.
En este caso, se retorna False indicando que no es seguro.

Verificación de la misma diagonal superior izquierda:
Se utilizan los bucles zip para iterar simultáneamente en dos rangos: desde la fila actual (row) hacia arriba y desde la columna actual (col) hacia la izquierda.
Se compara si hay una reina en cada celda correspondiente a la diagonal superior izquierda (board[i][j] == 1).
Si se encuentra una reina en alguna de las celdas de la misma diagonal, indica que ya hay una reina en esa diagonal y, 
por lo tanto, no es seguro colocar una reina en la posición actual.
En este caso, se retorna False indicando que no es seguro.

Verificación de la misma diagonal inferior izquierda:
Se utilizan los bucles zip para iterar simultáneamente en dos rangos: desde la fila actual (row) hacia abajo y desde la columna actual (col) hacia la izquierda.
Se compara si hay una reina en cada celda correspondiente a la diagonal inferior izquierda (board[i][j] == 1).
Si se encuentra una reina en alguna de las celdas de la misma diagonal, indica que ya hay una reina en esa diagonal y, 
por lo tanto, no es seguro colocar una reina en la posición actual.
En este caso, se retorna False indicando que no es seguro.
Si ninguna de las verificaciones anteriores detecta una amenaza de otras reinas en la misma fila o en las diagonales, 
se asume que es seguro colocar una reina en la posición actual y se retorna True. 
Esto indica que la posición actual es válida y no hay reinas que se amenacen directamente desde esa posición.
"""
def is_safe(board, row, col, N):
    # Verificar si hay una reina en la misma fila
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Verificar si hay una reina en la misma diagonal superior izquierda
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Verificar si hay una reina en la misma diagonal inferior izquierda
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

"""Función principal que resuelve el problema de las N reinas utilizando A*
La función solve_n_queens_a_star resuelve el problema de las N reinas utilizando el algoritmo A*. 
Comienza con un tablero vacío y crea un estado inicial con costo cero y la heurística calculada para ese tablero. 
Luego, se crea una cola de prioridad (heap) y se inserta el estado inicial en ella.
El bucle principal sigue extrayendo el estado con menor costo de la cola de prioridad. 
Si se alcanza la última fila del tablero, se ha encontrado una solución y se devuelve el tablero. 
Si no, se generan los sucesores del estado actual colocando una reina en cada columna segura. 
Cada sucesor tiene un nuevo tablero, un costo incrementado en 1 y una nueva heurística calculada para el nuevo tablero. 
Estos sucesores se agregan a la cola de prioridad.
El bucle continúa hasta que se encuentre una solución o no haya más estados por explorar."""
def solve_n_queens_a_star(N, initial_board):
    # Crear un tablero vacío de tamaño NxN, creando una matriz bidimensional de tamaño NxN y la inicializa con ceros.
    board = [[0 for _ in range(N)] for _ in range(N)]
    empty_board = [[0 for _ in range(N)] for _ in range(N)]

    if initial_board is not  None:
        # Copiar el estado inicial proporcionado por el usuario al tablero
        for i in range(N):
            for j in range(N):
                board[i][j] = initial_board[i][j]
    else: 
      board = get_random_initial_state(N)


    print("\nEstado inicial del tablero: \n")
    print_board(board)
    print("\n......................\n")


    # Crear el estado inicial con el tablero vacío y la heurística inicial
    initial_state = State(empty_board, 0, 0, 0, calculate_heuristic(empty_board, N))

    # Crear una cola de prioridad (heap) para almacenar los estados
    heap = []
    heapq.heappush(heap, initial_state)

    while heap:
        # Obtener el estado actual de la cola de prioridad (el estado con menor costo + heurística)
        current_state = heapq.heappop(heap)

        # Verificar si se han colocado todas las reinas (se ha alcanzado la última fila)
        if current_state.row >= N:
            return current_state.board

        # Probar todas las columnas en la fila actual para colocar una reina
        for col in range(N):
            # Verificar si es seguro colocar una reina en la posición actual
            if is_safe(current_state.board, current_state.row, col, N):
                # Crear una copia del tablero actual y colocar una reina en la posición actual
                new_board = [row[:] for row in current_state.board]
                new_board[current_state.row][col] = 1

                # Calcular el nuevo costo y la nueva heurística para el estado actualizado
                new_cost = current_state.cost + 1
                new_heuristic = calculate_heuristic(new_board, N)

                # Crear un nuevo estado con el tablero actualizado y la nueva información
                new_state = State(new_board, current_state.row + 1, col, new_cost, new_heuristic)

                # Agregar el nuevo estado a la cola de prioridad
                heapq.heappush(heap, new_state)

    # Si no se encontró ninguna solución, retornar None
    return None

#Llamada a la función menu para ejecutar el menú y empezar el programa.
menu()
