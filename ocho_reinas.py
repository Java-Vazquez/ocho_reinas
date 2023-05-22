import heapq

class State:
    def __init__(self, board, row, col, cost, heuristic):
        self.board = board
        self.row = row
        self.col = col
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

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

def solve_n_queens_a_star(N):
    board = [[0 for _ in range(N)] for _ in range(N)]
    initial_state = State(board, 0, 0, 0, calculate_heuristic(board, N))
    heap = []
    heapq.heappush(heap, initial_state)

    while heap:
        current_state = heapq.heappop(heap)

        if current_state.row >= N:
            return current_state.board

        for col in range(N):
            if is_safe(current_state.board, current_state.row, col, N):
                new_board = [row[:] for row in current_state.board]
                new_board[current_state.row][col] = 1
                new_cost = current_state.cost + 1
                new_heuristic = calculate_heuristic(new_board, N)
                new_state = State(new_board, current_state.row + 1, col, new_cost, new_heuristic)
                heapq.heappush(heap, new_state)

    return None

def print_board(board):
    for row in board:
        print(row)

# Ejemplo de uso: resolver el problema de las 4 reinas
N = 8
solution = solve_n_queens_a_star(N)

if solution is None:
    print("No existe una solución para el problema de las %d reinas." % N)
else:
    print_board(solution)
