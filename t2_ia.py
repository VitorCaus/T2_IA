import tkinter as tk
import random

# Função Minimax para calcular a melhor jogada
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Função para escolher a melhor jogada usando Minimax
def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Função para verificar se há um vencedor
def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or \
           all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or \
       board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Função para verificar se o tabuleiro está cheio
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

# Função para a jogada do computador considerando o nível de dificuldade
def computer_move():
    if difficulty == 'fácil':
        use_minimax = random.random() < 0.25  # 25% de chance
    elif difficulty == 'médio':
        use_minimax = random.random() < 0.5   # 50% de chance
    elif difficulty == 'difícil':
        use_minimax = True                    # 100% de chance

    if use_minimax:
        move = best_move(board)
    else:
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        move = random.choice(empty_cells)

    if move:
        board[move[0]][move[1]] = 'O'
        buttons[move[0]][move[1]].config(text='O', state='disabled')

        if check_winner(board, 'O'):
            result_label.config(text="O computador venceu!")
            disable_buttons()
        elif is_full(board):
            result_label.config(text="Empate!")
            disable_buttons()

# Função para desabilitar todos os botões
def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state='disabled')

# Função para quando o jogador clica em um botão
def player_click(i, j):
    if board[i][j] == ' ':
        board[i][j] = 'X'
        buttons[i][j].config(text='X', state='disabled')

        if check_winner(board, 'X'):
            result_label.config(text="Parabéns! Você venceu!")
            disable_buttons()
        elif is_full(board):
            result_label.config(text="Empate!")
            disable_buttons()
        else:
            computer_move()

# Função para iniciar o jogo após a seleção de dificuldade
def start_game():
    global board, buttons, result_label

    # Cria o tabuleiro vazio
    board = [[' ' for _ in range(3)] for _ in range(3)]

    # Limpa a janela para exibir o tabuleiro
    for widget in root.winfo_children():
        widget.destroy()

    # Cria os botões do tabuleiro
    buttons = []
    for i in range(3):
        row_buttons = []
        for j in range(3):
            button = tk.Button(root, text=' ', width=10, height=3,
                               command=lambda i=i, j=j: player_click(i, j))
            button.grid(row=i+1, column=j)
            row_buttons.append(button)
        buttons.append(row_buttons)

    # Label para exibir o resultado do jogo
    result_label = tk.Label(root, text="")
    result_label.grid(row=5, column=0, columnspan=3)

    # Botão para reiniciar o jogo
    restart_button = tk.Button(root, text="Reiniciar", command=choose_difficulty)
    restart_button.grid(row=6, column=0, columnspan=3)

# Função para escolher a dificuldade antes do jogo começar
def choose_difficulty():
    global difficulty

    # Limpa a janela
    for widget in root.winfo_children():
        widget.destroy()

    # Label de seleção de dificuldade
    difficulty_label = tk.Label(root, text="Selecione a dificuldade:")
    difficulty_label.grid(row=0, column=0, columnspan=3)

    # Variável de controle para a dificuldade
    difficulty = tk.StringVar(value='médio')

    # Botões de opção de dificuldade
    tk.Radiobutton(root, text="Fácil", variable=difficulty, value='fácil').grid(row=1, column=0)
    tk.Radiobutton(root, text="Médio", variable=difficulty, value='médio').grid(row=1, column=1)
    tk.Radiobutton(root, text="Difícil", variable=difficulty, value='difícil').grid(row=1, column=2)

    # Botão para iniciar o jogo com a dificuldade escolhida
    start_button = tk.Button(root, text="Iniciar Jogo", command=lambda: set_difficulty(difficulty.get()))
    start_button.grid(row=2, column=0, columnspan=3)

# Função para definir a dificuldade e iniciar o jogo
def set_difficulty(selected_difficulty):
    global difficulty
    difficulty = selected_difficulty
    start_game()

# Configuração da janela principal
root = tk.Tk()
root.title("Tic Tac Toe - Jogo da Velha")

# Exibe a tela de seleção de dificuldade
choose_difficulty()

# Executa a interface
root.mainloop()
