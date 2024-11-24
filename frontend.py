import tkinter as tk
import random
from outraRede.RedeNeural import RedeNeural

# opponent = None
neural_network = None


def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or \
           all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or \
       board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def computer_move():

    if opponent == "minimax":
        if difficulty == "facil":
            #25% de chance
            use_minimax = random.random() < 0.25
        elif difficulty == "medio":
            #50% de chance
            use_minimax = random.random() < 0.5
        elif difficulty == "dificil":
            #100% de chance
            use_minimax = True

        move = None
        if use_minimax:
            move = best_move(board)

        if move is None:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
            move = random.choice(empty_cells)

        computer_board_positioning(move)
        # board[move[0]][move[1]] = "O"
        # buttons[move[0]][move[1]].config(text="O", state="disabled")

        # if check_winner(board, "O"):
        #     result_label.config(text="O computador venceu!")
        #     disable_buttons()
        # elif is_full(board):
        #     result_label.config(text="Empate!")
        #     disable_buttons()
    elif opponent == "mlp":
        print(f"Tabuleiro enviado {translate_board(board)}")
        mlp_move = neural_network.propagacao(translate_board(board))
        move = translate_mlp_move(mlp_move)
        print(f"Movimento = {mlp_move} --> {translate_mlp_move(mlp_move)}")

        computer_board_positioning(move)
    else: 
        print("ERRO: oponente inexistente")

def computer_board_positioning(move):
    board[move[0]][move[1]] = "O"
    buttons[move[0]][move[1]].config(text="O", state="disabled")

    if check_winner(board, "O"):
        result_label.config(text="O computador venceu!")
        disable_buttons()
    elif is_full(board):
        result_label.config(text="Empate!")
        disable_buttons()

def translate_board(board):
    mlp_board = [board[i][j] for i in range(3) for j in range(3)]

    for i in range(9):
        if mlp_board[i] == "X":
            mlp_board[i] = 1
        elif mlp_board[i] == "O":
            mlp_board[i] = -1
        else:
            mlp_board[i] = 0
    return mlp_board

def translate_mlp_move(mlp_move):
    board_positions = {
        0: (0,0),
        1: (0,1),
        2: (0,2),
        3: (1,0),
        4: (1,1),
        5: (1,2),
        6: (2,0),
        7: (2,1),
        8: (2,2)
    }

    return board_positions[mlp_move]

def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state="disabled")


def player_click(i, j):
    if board[i][j] == " ":
        board[i][j] = "X"
        buttons[i][j].config(text="X", state="disabled")

        if check_winner(board, "X"):
            result_label.config(text="Parabéns! Você venceu!")
            disable_buttons()
        elif is_full(board):
            result_label.config(text="Empate!")
            disable_buttons()
        else:
            computer_move()

def start_game():
    global board, buttons, result_label

    board = [[" " for _ in range(3)] for _ in range(3)]

    #limpa janela
    for widget in root.winfo_children():
        widget.destroy()

    #cria tabuleiro
    buttons = []
    for i in range(3):
        row_buttons = []
        for j in range(3):
            button = tk.Button(root, text=" ", width=10, height=3,
                               command=lambda i=i, j=j: player_click(i, j))
            button.grid(row=i+1, column=j)
            row_buttons.append(button)
        buttons.append(row_buttons)

    #resultado do jogo
    result_label = tk.Label(root, text="")
    result_label.grid(row=5, column=0, columnspan=3)

    
    restart_button = tk.Button(root, text="Reiniciar", command=choose_opponent)
    restart_button.grid(row=6, column=0, columnspan=3)

def choose_difficulty():
    global difficulty, opponent

    opponent = "minimax"
    #limpa janela
    for widget in root.winfo_children():
        widget.destroy()

    difficulty_label = tk.Label(root, text="Selecione a dificuldade:")
    difficulty_label.grid(row=0, column=0, columnspan=3)

    difficulty = tk.StringVar(value="medio")

    tk.Radiobutton(root, text="facil", variable=difficulty, value="facil").grid(row=1, column=0)
    tk.Radiobutton(root, text="medio", variable=difficulty, value="medio").grid(row=1, column=1)
    tk.Radiobutton(root, text="dificil", variable=difficulty, value="dificil").grid(row=1, column=2)

    start_button = tk.Button(root, text="Iniciar Jogo", command=lambda: set_difficulty(difficulty.get()))
    start_button.grid(row=2, column=0, columnspan=3)

def set_difficulty(selected_difficulty):
    global difficulty
    difficulty = selected_difficulty
    start_game()

def choose_opponent():
    global opponent

    #limpa janela
    for widget in root.winfo_children():
        widget.destroy()

    opponent_label = tk.Label(root, text="Selecione o oponente:")
    opponent_label.grid(row=0, column=0, columnspan=2)

    tk.Button(root, text="Minimax", width=15, command=choose_difficulty).grid(row=1, column=0)
    tk.Button(root, text="Rede Neural", width=15, command=configure_network).grid(row=1, column=1)

def configure_network():
    global neural_network, opponent

    opponent = "mlp"

    weights = []
    with open("bestMLP.txt", "r") as weights_file:
        weights = [float(line.strip()) for line in weights_file] 
        print (f"pesos = {weights}")
    neural_network = RedeNeural(2, 9, 9, weights)

    start_game()

#janela principal
root = tk.Tk()
root.title("Tic Tac Toe - Jogo da Velha")

#selecao de oponente - jogo comeca aqui
choose_opponent()

#inicia interface
root.mainloop()
