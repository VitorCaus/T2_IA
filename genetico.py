import random
import sys
import numpy as np
from outraRede.RedeNeural import RedeNeural



TAM_CROMOSSOMO = 180

REDE_GANHOU = 1000
MINIMAX_GANHOU = -50
EMPATE = 0
POSICAO_INVALIDA_REDE = -1000

tam_populacao = None
populacao = None 
intermediaria = None

#dificuldade para minimax
dificuldade = ""

tabuleiro = []

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

            #atualiza tabuleiro minimax
            # tabuleiro_letras = convert_board_letters(tabuleiroRede)
            # tabuleiro = [tabuleiro_letras[i:i + 3] for i in range(0, 9, 3)]

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
    ind1, ind2 = random.sample(range(0, tam_populacao), 2)
    return ind1 if populacao[ind1][TAM_CROMOSSOMO] > populacao[ind2][TAM_CROMOSSOMO] else ind2


def crossover():
    # Cruzamento media
    for j in range(1, tam_populacao, 2):
        ind1 = torneio()
        ind2 = torneio()

        cromossomo1 = np.array(populacao[ind1])
        cromossomo2 = np.array(populacao[ind2])

        intermediaria[j] = (cromossomo1 + cromossomo2)/2


def mutacao():
    quant = random.randint(1, 3)
    for i in range(quant):
        individuo = random.randint(1, tam_populacao-1)
        posicao = random.randint(0, TAM_CROMOSSOMO-1)
        print(f"Cromossomo {individuo} sofreu mutação no peso {posicao}")
        populacao[individuo][posicao] = random.uniform(-1, 1)   


def achou_solucao(melhor):
    # if populacao[melhor][TAM_CROMOSSOMO] == 0:
    #     print(f"\nAchou a solução ótima. Ela corresponde ao cromossomo: {melhor}")
    #     print("Solução Decodificada:")
    #     for pessoa in range(2):
    #         soma = 0
    #         print(f"Pessoa {pessoa}: ", end="")
    #         for i in range(TAM_CROMOSSOMO):
    #             if populacao[melhor][i] == pessoa:
    #                 print(TAM_CROMOSSOMO, end=" ")
    #                 # soma += cargas[i]
    #         print(f"- Total: {soma}")
    #     return True
    return False

# ---------------------------------------------------------------------------------------------------------
def minimax(tabuleiro, depth, is_maximizing):
    if check_winner(tabuleiro, -1):
        return 1
    if check_winner(tabuleiro, 1):
        return -1
    if is_full(tabuleiro):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            # for j in range(3):
                if tabuleiro[i] == 0:
                    tabuleiro[i] = -1
                    score = minimax(tabuleiro, depth + 1, False)
                    tabuleiro[i] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            # for j in range(3):
                if tabuleiro[i] == 0:
                    tabuleiro[i] = 1
                    score = minimax(tabuleiro, depth + 1, True)
                    tabuleiro[i] = 0
                    best_score = min(score, best_score)
        return best_score

# Função para escolher a melhor jogada usando Minimax
def best_move(tabuleiro):
    best_score = -float('inf')
    move = None
    for i in range(9):
        # for j in range(3):
            if tabuleiro[i] == 0:
                tabuleiro[i] = -1
                score = minimax(tabuleiro, 0, False)
                tabuleiro[i] = 0
                if score > best_score:
                    best_score = score
                    move = i
    return move

def check_winner(tabuleiro, player):
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
        if all(tabuleiro[i] == player for i in linha):
            return True

    return False


# Função para verificar se o tabuleiro está cheio
def is_full(tabuleiro):
    return all(tabuleiro[i] != 0 for i in range(9))

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

    if use_minimax:
        move = best_move(tabuleiro)
    else:
        empty_cells = [i for i in range(9) if tabuleiro[i] == 0]
        move = random.choice(empty_cells)

    if move:
        tabuleiro[move] = -1


def random_difficulty():
    return random.choice(['facil','medio','dificil'])

def convert_board_numbers(board):
    converted = board.copy()
    for i in range (0, 9, 1):
        if(converted[i] == 'X'): 
            converted[i] = 1
        elif(converted[i] == 'O'): 
            converted[i] = -1
        else: 
            converted[i] = 0
    return converted

def convert_board_letters(board):
    converted = board.copy()
    for i in range (0, 9, 1):
        if(converted[i] == 1): 
            converted[i] = 'X'
        elif(converted[i] == -1): 
            converted[i] = 'O'
        else: 
            converted[i] = '_'
    return converted

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
    
    random.seed()

    tam_populacao = int(sys.argv[1])

    populacao = init_populacao()

    intermediaria = init_populacao()
    
    tabuleiro = init_tabuleiro()

    init()
    for g in range(1):
        print(f"Geração: {g}")
        dificuldade = random_difficulty()
        print(f"Dificuldade para Minimax = {dificuldade.capitalize()}")
        calcula_aptidao()
        print_matriz()
        melhor = get_mais_apto()
        print(f"Melhor Rede Elitismo = {melhor} - (APT = {populacao[melhor][TAM_CROMOSSOMO]})")
        # if achou_solucao(melhor):
        #     break
        crossover()
        # global populacao
        populacao = [row[:] for row in intermediaria]
        if random.randint(0, 4) == 0:
            print("Mutação")
            mutacao()
    # print_matriz()
    

    melhor = populacao[0]

    print(f"\n\n-- MAIS APTO (APTIDÃO = {melhor[TAM_CROMOSSOMO]})--\n\n")
    melhor = melhor[:-1]

    backup_melhor = open("bestMLP.txt", "w")
    for peso in melhor:
        backup_melhor.write(f"{peso}\n")
    backup_melhor.close()
    print(melhor)


if __name__ == "__main__":
    main()

# TODO 
# adicionar verificação de convergencia
# <<<<transformar mais apta em MLP -> só usar nosso MLP direto>>>>>
# verificar aprendizado, talvez intensificar mutação