import random
from RedeNeural import RedeNeural

# 42 para reproduzir os mesmos resultados
random.seed(42)

camadas = 2  # numero de camadas
neuronios_por_camada = 9  # neuronios na camada oculta
saida_neuronios = 9  # neuronios de saida (posicao tabuleiro)

# criando a rede neural
rede = RedeNeural(camadas, neuronios_por_camada, saida_neuronios)

# a entrada representa um estado atual de um tabuleiro de jogo da velha
entradas = [1, 0, 0, 0, 0, 0, 0, 0, 0]

# propagacao da rede
posicao_escolhida = rede.propagacao(entradas)

# posicao tabuleiro escolhida
print("Posicao escolhida para jogada:", posicao_escolhida)