import random
import sys
import numpy as np
from outraRede.RedeNeural import RedeNeural




TAM_CROMOSSOMO = 180

REDE_GANHOU = 1000
MINIMAX_GANHOU = -50
EMPATE = 0
POSICAO_INVALIDA_REDE = -1000


def init():
    for i in range(tam_populacao):
        populacao[i][:180] = [random.uniform(-1, 1) for i in range(180)]


def print_matriz():
    for i in range(tam_populacao):
        print(f"C: {i} - {' '.join(map(str, populacao[i][:-1]))} F: {populacao[i][TAM_CROMOSSOMO]}\n")

def convert_board_value(char):
    if char == 1:
        return 'X'
    elif char == -1:
        return 'O'
    else:
        return '_'

def aptidao(individuo):
    pesos = populacao[individuo][:180]
    rede = RedeNeural(2, 9, 9, pesos)

    global tabuleiro

    aptidao = 0

    print("\n--------------------------------------------------------")
    print(f"CALCULANDO APTIDAO PARA INDIVÍDUO {individuo}:")
    for i in range(0, 9, 1):
        print(f"---| RODADA {i} |--- ")
        if not(i % 2):#rede - jogando como X
            print(f"Rede {individuo} joga\n")
            melhor_posicao = rede.propagacao(tabuleiro)
            
            if(tabuleiro[melhor_posicao] != 0):
                aptidao = POSICAO_INVALIDA_REDE
                print(f"TABULEIRO (POS. INVÁLIDA) -> {melhor_posicao} = {convert_board_value(tabuleiro[melhor_posicao])}:\n")
                print_board()
                break
            
            tabuleiro[melhor_posicao] = 1

            if(check_winner(tabuleiro, 1)):
                print(f"TABULEIRO (REDE {individuo} VENCE):\n")
                print_board()
                aptidao = REDE_GANHOU
                break
        else:#minimax - jogando como O
            print("Minimax joga")
            computer_move()#tabuleiro tambem atualizado nessa funcao

            if(check_winner(tabuleiro, -1)):
                aptidao = MINIMAX_GANHOU
                print("TABULEIRO (MINIMAX VENCE):\n")
                print_board()
                break
        print(f"TABULEIRO (RODADA {i}):\n")
        print_board()
    if aptidao == 0 and is_full(tabuleiro):
        aptidao = EMPATE
        print("TABULEIRO (EMPATE):\n")
        print_board()

    
    quantidade_vazios = tabuleiro.count(0)

    resultante = aptidao * quantidade_vazios

    print(f"APTIDÃO RESULTANTE = {resultante}\n")
    return resultante



def calcula_aptidao():
    for i in range(tam_populacao):
        populacao[i][TAM_CROMOSSOMO] = aptidao(i)
        global tabuleiro
        tabuleiro = init_tabuleiro()


def get_mais_apto():
    linha = max(range(0, tam_populacao), key=lambda x: populacao[x][TAM_CROMOSSOMO])
    intermediaria[0] = populacao[linha].copy()
    return linha


def torneio():
    ind1 = random.randint(0, tam_populacao-1)
    ind2 = random.randint(0, tam_populacao-1)
    return ind1 if populacao[ind1][TAM_CROMOSSOMO] > populacao[ind2][TAM_CROMOSSOMO] else ind2


def crossover():
    # Cruzamento media
    for j in range(1, tam_populacao):
        ind1 = 0 if populacao[0][TAM_CROMOSSOMO] >= 1000 else torneio()
        ind2 = torneio()

        cromossomo1 = np.array(populacao[ind1])
        cromossomo2 = np.array(populacao[ind2])

        intermediaria[j] = (cromossomo1 + cromossomo2)/2

# def mutacao():
#     quant = random.randint(1, 5)
#     for i in range(quant):
#         individuo = random.randint(1, tam_populacao-1)

#         num_mudancas = random.randint(1, 10)
#         for j in range(num_mudancas):
#             posicao = random.randint(0, TAM_CROMOSSOMO-1)
#             print(f"Cromossomo {individuo} sofreu mutação no peso {posicao}")
#             populacao[individuo][posicao] = random.uniform(-1, 1)   

# def mutacao():
#     taxa_mutacao = 0.02
#     for individuo in range(1, tam_populacao):  
#         for posicao in range(TAM_CROMOSSOMO):
#             if random.random() < taxa_mutacao:
#                 print(f"Cromossomo {individuo} sofreu mutação no peso {posicao}")
#                 populacao[individuo][posicao] = random.uniform(-1, 1)

def mutacao():
    individuo = random.randint(1, tam_populacao-1)
    # peso = random.randint(0, TAM_CROMOSSOMO-1)
    print(f"Individuo {individuo} sofreu mutação em todos os pesos")
    # print(f"Individuo {individuo} sofreu mutação no peso {peso}")
    populacao[individuo][:180] = [random.uniform(-1, 1) for i in range(180)]

# def mutacao():
#     individuo = random.randint(1, tam_populacao-1)
#     num_neuronios = random.randint(1, 3)
#     for _ in range(num_neuronios):
#         neuronio = random.randint(0, 17)
#         inicio = neuronio * 10
#         populacao[individuo][inicio:inicio+10] = [random.uniform(-1, 1) for i in range(10)]
#         print(f"Indivíduo {individuo} sofreu mutação no neurônio {neuronio}")

# def mutacao():
#     individuo = random.randint(1, tam_populacao-1)
#     for i in range (0, TAM_CROMOSSOMO, 10):
#         peso = random.randint(0,9)
#         # populacao[individuo][peso+i] = random.uniform(-1, 1)
#         populacao[individuo][peso+i] *= -1
#         print(f"Individuo {individuo} teve mutação do peso {peso+i}")


def convergencia(aptidao_minima, porcentagem_minima):
    count = sum(1 for ind in populacao if ind[TAM_CROMOSSOMO] >= aptidao_minima)
    proporcao = count / tam_populacao
    print(f"Indivíduos aptos (>= {aptidao_minima}): {count}/{tam_populacao} ({proporcao*100:.2f}%)")
    with open("convergencias.txt", "a") as file:
        file.write(f"Individuos aptos (>= {aptidao_minima}): {count}/{tam_populacao} ({proporcao*100:.2f}%) | {proporcao >= porcentagem_minima}\n")
    return proporcao >= porcentagem_minima


# ---------------------------------------------------------------------------------------------------------
def minimax(board, depth, is_maximizing):
    if check_winner(board, -1):
        return 1
    if check_winner(board, 1):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
                if board[i] == 0:
                    board[i] = -1
                    score = minimax(board, depth + 1, False)
                    board[i] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
                if board[i] == 0:
                    board[i] = 1
                    score = minimax(board, depth + 1, True)
                    board[i] = 0
                    best_score = min(score, best_score)
        return best_score

# Função para escolher a melhor jogada usando Minimax
def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = minimax(board, 0, False)
                board[i] = 0
                if score > best_score:
                    best_score = score
                    move = i
    return move

def check_winner(board, player):
    posicoes_vitoria = [
        [0, 1, 2],  #linha1
        [3, 4, 5],  #linha2
        [6, 7, 8],  #linha3
        [0, 3, 6],  #coluna1
        [1, 4, 7],  #coluna2
        [2, 5, 8],  #coluna3
        [0, 4, 8],  #diagonal principal
        [2, 4, 6],  #diagonal secundaria
    ]

    for linha in posicoes_vitoria:
        if all(board[i] == player for i in linha):
            return True

    return False


# Função para verificar se o tabuleiro está cheio
def is_full(board):
    return all(board[i] != 0 for i in range(9))

def computer_move():
    use_minimax = 0
    if dificuldade == 'facil':
        #25% de chance
        use_minimax = random.random() < 0.25
    elif dificuldade == 'medio':
        #50% de chance
        use_minimax = random.random() < 0.5
    elif dificuldade == 'dificil':
        #100% de chance
        use_minimax = True

    move = None

    if use_minimax:
        move = best_move(tabuleiro)

    if move is None:
        empty_cells = [i for i in range(9) if tabuleiro[i] == 0]
        move = random.choice(empty_cells)
        
    tabuleiro[move] = -1


def random_difficulty():
    return random.choice(['facil','medio','dificil'])

def print_board():
    converted = tabuleiro.copy()
    for i in range (0, 9, 1):
        if(converted[i] == 1): 
            converted[i] = 'X'
        elif(converted[i] == -1): 
            converted[i] = 'O'
        else: 
            converted[i] = '_'
    for i in range(0, 9, 3):
        print(' '.join([converted[i], converted[i+1], converted[i+2], "\n"]))

def init_tabuleiro():
    return [0 for i in range(9)]

def init_populacao():
    return [[0] * (TAM_CROMOSSOMO+1) for i in range(tam_populacao)]
# ---------------------------------------------------------------------------------------------------------

def main():
    global tam_populacao, populacao, intermediaria, tabuleiro, dificuldade
    if len(sys.argv) < 2:
        print("ERRO: uso = python ./genetico.py <tam_populacao>")
        return
    
    # random.seed()

    tam_populacao = int(sys.argv[1])

    populacao = init_populacao()

    intermediaria = init_populacao()
    
    tabuleiro = init_tabuleiro()

    init()
    for g in range(100):
        print(f"\n -==<| Geração: {g} |>==-")
        dificuldade = random_difficulty()
        print(f"Dificuldade para Minimax = {dificuldade.capitalize()}")
        calcula_aptidao()
        # print_matriz()
        melhor = get_mais_apto()
        print(f"Melhor Rede Elitismo = {melhor} - (APT = {populacao[melhor][TAM_CROMOSSOMO]})")
        
        aptidoes = open("aptidoes.txt", "a")
        aptidoes.write(f"{melhor} -> APT = {populacao[melhor][TAM_CROMOSSOMO]} DIF = {dificuldade}\n")
        aptidoes.close()

        if(convergencia(1000, 0.7)):
            print("\n-+++<| CONVERGENCIA |>+++-\n")
            break;
        crossover()
        populacao = [row[:] for row in intermediaria]
        taxa_mutacao = random.random()
        if taxa_mutacao <= 0.2:
            print("\n===< MUTAÇÃO >===")
            mutacao()
    # print_matriz()
    

    melhor = populacao[0]

    print(f"\n\n-- MAIS APTO (APTIDÃO = {melhor[TAM_CROMOSSOMO]})--\n\n")
    melhor = melhor[:-1]

    backup_melhor = open("bestMLP1.txt", "w")
    for peso in melhor:
        backup_melhor.write(f"{peso}\n")
    backup_melhor.close()
    print(melhor)


if __name__ == "__main__":
    main()