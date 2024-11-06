import random
import math

class Neuronio:
    def __init__(self, pesos):
        self.pesos = pesos

    def propagacao(self, entradas):
        x_linha = [1] + list(entradas)
        soma = 0
        soma = sum(e * p for e, p in zip(x_linha, self.pesos))

        # for i in range(len(entradas)):
        #     soma += x_linha[i] * self.pesos[i]

        # return 1 / (1 + math.exp (-soma)) # sigmoid
        return math.tanh(soma) # tangente hiperbolica

class RedeNeural:
    def __init__(self, camadas, neuronios, saidas):
        self.camadas = camadas
        self.neuronios = neuronios
        self.saidas = saidas
        self.pesos = self.inicializaPesos() # substituir por algoritmo genetico para gerar os pesos
        self.neuronios_camadas = self.cria_neuronio()

    def inicializaPesos(self):
        pesos = []
        topologia = (self.neuronios * self.camadas) * (self.neuronios + 1)
        for i in range(topologia):
            pesos.append(random.uniform(-1,1))
        return pesos
    
    def get_pesos(self):
        return self.pesos
    
    def cria_neuronio(self):
        neuronios = []
        peso_index = 0
    
        for camada in range(self.camadas):
            camada_neuronios = []
            for _ in range(self.neuronios):
                neuronio_pesos = self.pesos[peso_index:peso_index+self.neuronios+1]
                camada_neuronios.append(Neuronio(neuronio_pesos))
                peso_index += self.neuronios + 1
            neuronios.append(camada_neuronios)
        
        return neuronios
    
    def propagacao(self, entradas):
        neuronios = self.neuronios_camadas
        for camada in neuronios:
            saidas = []
            for neuronio in camada:
                saidas.append(neuronio.propagacao(entradas))
            entradas = saidas
        print("Valores neuronios de saida:", saidas)
        # encontrando o maior valor dos neuronios de saida. isso representa a posicao a ser jogada
        max_index = saidas.index(max(saidas))
        return max_index

    
