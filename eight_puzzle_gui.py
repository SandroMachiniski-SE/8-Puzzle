import tkinter as tk
from tkinter import messagebox
import heapq
import random

# ======================
# LÓGICA DO 8-PUZZLE
# ======================

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

ROWS = 3
COLS = 3


def is_solvable(state):
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0


def manhattan_distance(state):
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
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, COLS)

    moves = []
    if x > 0:
        moves.append((-1, 0))
    if x < ROWS - 1:
        moves.append((1, 0))
    if y > 0:
        moves.append((0, -1))
    if y < COLS - 1:
        moves.append((0, 1))

    for dx, dy in moves:
        new_x = x + dx
        new_y = y + dy
        new_index = new_x * COLS + new_y
        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))

    return neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(start_state):
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
    state = list(GOAL_STATE)
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return tuple(state)


# ======================
# INTERFACE GRÁFICA RESPONSIVA
# ======================

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle 3D A* Solver (Responsivo)")

        # permite redimensionar
        self.master.geometry("600x600")
        self.master.minsize(400, 450)

        # Paleta simples
        self.window_bg = "#e5f0fb"
        self.panel_bg = "#d0d8e6"
        self.board_bg = "#f3f4f6"
        self.empty_tile_color = "#cbd5e1"

        self.master.configure(bg=self.window_bg)

        self.tile_colors = {
            1: "#22c55e",
            2: "#3b82f6",
            3: "#22c55e",
            4: "#3b82f6",
            5: "#0ea5e9",
            6: "#3b82f6",
            7: "#f97316",
            8: "#f97316"
        }
        self.text_color = "#ffffff"

        self.current_state = GOAL_STATE
        self.solution_path = None
        self.step_index = 0
        self.manual_moves = 0

        self.buttons = []

        self.build_layout()
        self.update_board()

        # quando a janela redimensionar, ajustar fonte dos tiles
        self.master.bind("<Configure>", self.on_resize)

    def build_layout(self):
        # frame raiz
        root_frame = tk.Frame(self.master, bg=self.panel_bg, bd=4, relief="ridge")
        root_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # deixa root_frame crescer
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # grid no root_frame
        root_frame.rowconfigure(0, weight=0)  # título
        root_frame.rowconfigure(1, weight=3)  # tabuleiro
        root_frame.rowconfigure(2, weight=0)  # controles
        root_frame.rowconfigure(3, weight=0)  # status
        root_frame.columnconfigure(0, weight=1)

        # Título
        title = tk.Label(
            root_frame,
            text="8-PUZZLE 3D A* SOLVER",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_bg,
            fg="#1f2933"
        )
        title.grid(row=0, column=0, pady=(5, 0), sticky="n")

        # Tabuleiro
        board_outer = tk.Frame(root_frame, bg=self.panel_bg)
        board_outer.grid(row=1, column=0, pady=10, sticky="nsew")
        board_outer.rowconfigure(0, weight=1)
        board_outer.columnconfigure(0, weight=1)

        board_inner = tk.Frame(board_outer, bg=self.board_bg, bd=8, relief="ridge")
        board_inner.grid(row=0, column=0, sticky="nsew")

        # permitir expansão do grid interno
        for i in range(ROWS):
            board_inner.rowconfigure(i, weight=1)
            board_inner.columnconfigure(i, weight=1)

        for i in range(ROWS):
            row = []
            for j in range(COLS):
                btn = tk.Button(
                    board_inner,
                    text="",
                    font=("Segoe UI", 24, "bold"),
                    relief="raised",
                    bd=6,
                    activeforeground=self.text_color,
                    cursor="hand2",
                    command=lambda r=i, c=j: self.handle_tile_click(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row.append(btn)
            self.buttons.append(row)

        # Controles
        controls = tk.Frame(root_frame, bg=self.panel_bg)
        controls.grid(row=2, column=0, pady=10, sticky="ew")
        for i in range(3):
            controls.columnconfigure(i, weight=1)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "height": 2,
            "relief": "raised",
            "bd": 4,
            "cursor": "hand2"
        }

        self.btn_random = tk.Button(
            controls,
            text="Estado Aleatório",
            bg="#a855f7",
            fg="#ffffff",
            activebackground="#9333ea",
            activeforeground="#ffffff",
            command=self.set_random_state,
            **btn_style
        )
        self.btn_random.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_solve = tk.Button(
            controls,
            text="Resolver (A*)",
            bg="#22c55e",
            fg="#ffffff",
            activebackground="#16a34a",
            activeforeground="#ffffff",
            command=self.solve_puzzle,
            **btn_style
        )
        self.btn_solve.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_reset = tk.Button(
            controls,
            text="Resetar",
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            command=self.reset_to_goal,
            **btn_style
        )
        self.btn_reset.grid(row=0, column=2, padx=5, sticky="ew")

        # Status
        status_frame = tk.Frame(root_frame, bg=self.panel_bg)
        status_frame.grid(row=3, column=0, pady=(5, 5), padx=5, sticky="ew")
        status_frame.columnconfigure(0, weight=1)

        self.label_steps = tk.Label(
            status_frame,
            text="Passos: 0",
            font=("Segoe UI", 10, "bold"),
            bg=self.panel_bg,
            fg="#111827",
            anchor="w"
        )
        self.label_steps.grid(row=0, column=0, sticky="w")

        self.label_state = tk.Label(
            status_frame,
            text="Estado: objetivo",
            font=("Segoe UI", 9),
            bg=self.panel_bg,
            fg="#374151",
            anchor="w"
        )
        self.label_state.grid(row=1, column=0, sticky="w")

    def on_resize(self, event):
        # Ajusta o tamanho da fonte dos tiles conforme a altura da janela
        # para não quebrar visualmente
        height = self.master.winfo_height()
        # limite simples: entre 14 e 32
        size = max(14, min(32, height // 25))
        for row in self.buttons:
            for btn in row:
                btn.configure(font=("Segoe UI", size, "bold"))

    # --------- ATUALIZAÇÃO VISUAL ---------

    def update_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                value = self.current_state[i * COLS + j]
                btn = self.buttons[i][j]

                if value == 0:
                    btn.configure(
                        text="",
                        bg=self.empty_tile_color,
                        relief="sunken",
                        bd=5
                    )
                else:
                    color = self.tile_colors.get(value, "#3b82f6")
                    btn.configure(
                        text=str(value),
                        fg=self.text_color,
                        bg=color,
                        activebackground=color,
                        relief="raised",
                        bd=6
                    )

        self.label_steps.config(text=f"Passos: {self.manual_moves}")
        if self.current_state == GOAL_STATE:
            self.label_state.config(text="Estado: objetivo")
        else:
            self.label_state.config(text="Estado: em andamento")

    # --------- INTERAÇÃO ---------

    def handle_tile_click(self, row, col):
        index_clicked = row * COLS + col
        zero_index = self.current_state.index(0)

        if self.is_adjacent(index_clicked, zero_index):
            state_list = list(self.current_state)
            state_list[zero_index], state_list[index_clicked] = (
                state_list[index_clicked],
                state_list[zero_index],
            )
            self.current_state = tuple(state_list)

            self.manual_moves += 1
            self.solution_path = None
            self.step_index = 0

            self.update_board()

            if self.current_state == GOAL_STATE:
                messagebox.showinfo(
                    "Parabéns!",
                    f"Você resolveu o puzzle em {self.manual_moves} passos!"
                )

    def is_adjacent(self, idx1, idx2):
        r1, c1 = divmod(idx1, COLS)
        r2, c2 = divmod(idx2, COLS)
        return abs(r1 - r2) + abs(c1 - c2) == 1

    # --------- BOTÕES ---------

    def set_random_state(self):
        self.current_state = generate_random_state()
        self.manual_moves = 0
        self.solution_path = None
        self.step_index = 0
        self.update_board()

    def solve_puzzle(self):
        solution = a_star(self.current_state)
        if solution is None:
            messagebox.showerror("Erro", "Este estado não é solucionável.")
            return

        steps = len(solution) - 1
        self.solution_path = solution
        self.step_index = 0
        messagebox.showinfo(
            "Solução encontrada",
            f"O algoritmo A* encontrou uma solução em {steps} passos.\n"
            f"(Você pode continuar interagindo com o tabuleiro)."
        )

    def reset_to_goal(self):
        self.current_state = GOAL_STATE
        self.manual_moves = 0
        self.solution_path = None
        self.step_index = 0
        self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleGUI(root)
    root.mainloop()