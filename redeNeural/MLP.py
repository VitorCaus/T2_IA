import numpy as np
import random

class Neuronio:
    def __init__(self, pesos):
        self.pesos = np.array(pesos)

    def propagacao(self, x):
        x_novo = [1] + list(x)
        saida = 0
        for i in range(0, 10, 1):
            saida += x_novo[i] * self.pesos[i]
        return tanh(saida)


class MLP:
    def __init__(self, camadas):
        self.camadas = camadas

    def start(self, entrada):
        saida_camada = entrada
        for camada in self.camadas:
            y_gerados = []
            for neuronio in camada:
                y_gerados.append(neuronio.propagacao(saida_camada))
            saida_camada = y_gerados
        return saida_camada

def tanh(x):
    return np.tanh(x)


# ------------------------------------------------------------------------------------------------------

def main(tabuleiro, pesos):
    # pesos aleatorios (alterar para receber do genetico)
    pesosAux = [random.uniform(-1, 1) for i in range(180)]
    camada_oculta = [];
    camada_saida = [];

    #inicializacao dos neuronios nas camadas (e os seus pesos)
    contador = 0
    while(contador < 180):
        if contador < 90:
            camada_oculta.append(Neuronio(pesos=pesosAux[contador:contador+10]))
        else:
            camada_saida.append(Neuronio(pesos=pesosAux[contador:contador+10]))
        contador += 10

    mlp = MLP(camadas=[camada_oculta, camada_saida])

    saida = mlp.start(tabuleiro)
    print("saida da rede:", saida)

    pos_maior = np.argmax(saida)
    print("Posicao maior valor: ", pos_maior)
    print("Maior valor: ", saida[pos_maior])

if __name__ == "__main__":
    entrada = np.array([1, 0, 0, -1, -1, 0, 0, 0, 1])
    main(tabuleiro=entrada, pesos=[])