import tkinter as tk
from tkinter import messagebox
import heapq
import random

# ======================
# Representação do problema
# ======================

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

ROWS = 3
COLS = 3


def is_solvable(state):
    """
    Verifica se o estado é solucionável.
    Conta inversões (ignora o zero).
    Para o 8-puzzle, número de inversões deve ser par.
    """
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0


def manhattan_distance(state):
    """
    Heurística: distância de Manhattan para o objetivo GOAL_STATE.
    """
    distance = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        goal_index = GOAL_STATE.index(value)
        x1, y1 = divmod(index, COLS)
        x2, y2 = divmod(goal_index, COLS)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def get_neighbors(state):
    """
    Retorna estados vizinhos (movendo o zero).
    """
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, COLS)

    moves = []
    if x > 0:
        moves.append((-1, 0))  # cima
    if x < ROWS - 1:
        moves.append((1, 0))   # baixo
    if y > 0:
        moves.append((0, -1))  # esquerda
    if y < COLS - 1:
        moves.append((0, 1))   # direita

    for dx, dy in moves:
        new_x = x + dx
        new_y = y + dy
        new_index = new_x * COLS + new_y
        new_state = list(state)
        # troca zero com a peça adjacente
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))

    return neighbors


def reconstruct_path(came_from, current):
    """
    Reconstrói o caminho do início até o estado final.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(start_state):
    """
    Algoritmo A* para resolver o 8-puzzle.
    Retorna a lista de estados do caminho (incluindo início e fim).
    Se não achar solução, retorna None.
    """
    if not is_solvable(start_state):
        return None

    open_set = []
    heapq.heappush(open_set, (0, start_state))

    came_from = {}
    g_score = {start_state: 0}
    f_score = {start_state: manhattan_distance(start_state)}

    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == GOAL_STATE:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score_neighbor = tentative_g + manhattan_distance(neighbor)
                f_score[neighbor] = f_score_neighbor
                heapq.heappush(open_set, (f_score_neighbor, neighbor))

    return None


def generate_random_state():
    """
    Gera um estado aleatório solucionável.
    """
    state = list(GOAL_STATE)
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return tuple(state)


# ======================
# Interface gráfica (Tkinter)
# ======================

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8 Puzzle - A* Solver")

        self.current_state = GOAL_STATE
        self.solution_path = None
        self.step_index = 0

        self.buttons = []
        self.create_board()
        self.create_controls()
        self.update_board()

    def create_board(self):
        frame_board = tk.Frame(self.master)
        frame_board.pack(pady=10)

        for i in range(ROWS):
            row = []
            for j in range(COLS):
                btn = tk.Button(frame_board, text="", width=4, height=2,
                                font=("Helvetica", 24))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def create_controls(self):
        frame_controls = tk.Frame(self.master)
        frame_controls.pack(pady=10)

        btn_random = tk.Button(frame_controls, text="Estado Aleatório",
                               command=self.set_random_state)
        btn_random.grid(row=0, column=0, padx=5)

        btn_solve = tk.Button(frame_controls, text="Resolver (A*)",
                              command=self.solve_puzzle)
        btn_solve.grid(row=0, column=1, padx=5)

        btn_next = tk.Button(frame_controls, text="Próximo passo",
                             command=self.next_step)
        btn_next.grid(row=0, column=2, padx=5)

        btn_reset = tk.Button(frame_controls, text="Resetar",
                              command=self.reset_to_goal)
        btn_reset.grid(row=0, column=3, padx=5)

        self.label_info = tk.Label(self.master, text="Estado atual / passos: 0")
        self.label_info.pack(pady=5)

    def update_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                value = self.current_state[i * COLS + j]
                text = "" if value == 0 else str(value)
                self.buttons[i][j]["text"] = text

    def set_random_state(self):
        self.current_state = generate_random_state()
        self.solution_path = None
        self.step_index = 0
        self.label_info.config(text="Estado aleatório gerado. Passos: 0")
        self.update_board()

    def solve_puzzle(self):
        self.solution_path = a_star(self.current_state)
        if self.solution_path is None:
            messagebox.showerror("Erro", "Este estado não é solucionável.")
            return

        self.step_index = 0
        total_steps = len(self.solution_path) - 1
        self.label_info.config(text=f"Solução encontrada! Total de passos: {total_steps}")

    def next_step(self):
        if not self.solution_path:
            messagebox.showinfo("Info", "Primeiro clique em 'Resolver (A*)'.")
            return

        if self.step_index < len(self.solution_path) - 1:
            self.step_index += 1
            self.current_state = self.solution_path[self.step_index]
            self.update_board()
            self.label_info.config(
                text=f"Mostrando passo {self.step_index} de {len(self.solution_path) - 1}"
            )
        else:
            messagebox.showinfo("Info", "Já está no estado final!")

    def reset_to_goal(self):
        self.current_state = GOAL_STATE
        self.solution_path = None
        self.step_index = 0
        self.label_info.config(text="Resetado para o estado final. Passos: 0")
        self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleGUI(root)
    root.mainloop()