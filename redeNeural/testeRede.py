import numpy as np
import random

class Neuronio:
    def __init__(self, pesos, bias, ativacao):
        self.pesos = np.array(pesos)
        self.bias = bias
        self.ativacao = ativacao
    
    def activate(self, x):
        z = np.dot(self.pesos, x) + self.bias
        return self.ativacao(z)

class MLP:
    def __init__(self, camadas):
        self.camadas = camadas

    def propagate(self, x):
        for camada in self.camadas:
            x = np.array([Neuronio.activate(x) for Neuronio in camada])
        return x


def tanh(x):
    return np.tanh(x)

def logistica(x):
    return 1/(1 + np.exp(-x))




pesosAux = [random.uniform(-1, 1) for i in range(180)]
camada_oculta = [];
camada_saida = [];

#inicializacao dos neuronios nas camadas (e os seus pesos)
contador = 0
while(contador < 180):
    if contador < 90:
        camada_oculta.append(Neuronio(pesos=pesosAux[contador+1:contador+10], bias=pesosAux[contador], ativacao=logistica))
    else:
        camada_saida.append(Neuronio(pesos=pesosAux[contador+1:contador+10], bias=pesosAux[contador], ativacao=logistica))
    contador += 10

mlp = MLP(camadas=[camada_oculta, camada_saida])

entrada = np.array([1, 0, 0, -1, -1, 0, 0, 0, 1])
saida = mlp.propagate(entrada)
print("saida da rede:", saida)

pos_maior = saida.argmax()
print("Posicao maior valor: ", pos_maior)
print("Maior valor: ", saida[pos_maior])
