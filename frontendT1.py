import joblib
import os
import random
from sklearn.metrics import accuracy_score

modelo_mlp = joblib.load('./modelo_mlp.pkl')



VITORIA_X = "X ganhou"
VITORIA_O = "O ganhou"
EMPATE = "Empate"
JOGO = "Tem jogo" 

def verificar_estado(tabuleiro):
  # vitoria para X
  for i in range(0, 9, 3):
    if tabuleiro[i] == tabuleiro[i+1] == tabuleiro[i+2] == 1:
      return VITORIA_X 
  
  for i in range(3):
    if tabuleiro[i] == tabuleiro[i+3] == tabuleiro[i+6] == 1:
      return VITORIA_X

  if tabuleiro[0] == tabuleiro[4] == tabuleiro[8] == 1 or tabuleiro[2] == tabuleiro[4] == tabuleiro[6] == 1:
    return VITORIA_X
  
  # vitoria para O
  for i in range(0, 9, 3):
    if tabuleiro[i] == tabuleiro[i+1] == tabuleiro[i+2] == -1:
      return VITORIA_O 
  
  for i in range(3):
    if tabuleiro[i] == tabuleiro[i+3] == tabuleiro[i+6] == -1:
      return VITORIA_O

  if tabuleiro[0] == tabuleiro[4] == tabuleiro[8] == -1 or tabuleiro[2] == tabuleiro[4] == tabuleiro[6] == -1:
    return VITORIA_O
  

  # Tem jogo ou empate 
  if 0 in tabuleiro:
    return JOGO
  else:
    return EMPATE
  
def print_tabuleiro(tabuleiro):
  tabuleiro_mapeado = tabuleiro.copy()
  print (tabuleiro_mapeado)

  for i in range (0, 9, 1):
    if(tabuleiro_mapeado[i] == 1): 
      tabuleiro_mapeado[i] = 'X'
    elif(tabuleiro_mapeado[i] == -1): 
      tabuleiro_mapeado[i] = "O"
    else: 
      tabuleiro_mapeado[i] = "_"
  
  for i in range(0, 9, 3):
        print(f"{tabuleiro_mapeado[i]}  {tabuleiro_mapeado[i+1]}  {tabuleiro_mapeado[i+2]}")

def jogada_cpu(tabuleiro):
  posicoes_livres = [i for i, valor in enumerate(tabuleiro) if valor == 0]
  if posicoes_livres:
    escolha = random.choice(posicoes_livres)
    tabuleiro[escolha] = -1
  return tabuleiro

def limpar_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux e macOS
        os.system('clear')

def main():
  predicoes_ia = []
  estados_jogo = []
  tabuleiro_atual = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  restart = False
  game_loop = True

  while game_loop:

    print_tabuleiro(tabuleiro_atual)
    posicao = input("Insira uma posição: ")

    if posicao == "-1": break

    tabuleiro_atual[int(posicao)] = 1

    resultado = verificar_estado(tabuleiro_atual)
    estados_jogo.append(resultado)
    print(f"Estado do jogo: {resultado}")

    predicao = modelo_mlp.predict([tabuleiro_atual])
    predicoes_ia.append(predicao)
    print(f"Previsão do modelo MLP: {predicao}")

    print("Acuracia: ", accuracy_score(estados_jogo, predicoes_ia))


    if resultado == JOGO:
      print("Jogada do computador...")
      tabuleiro_atual = jogada_cpu(tabuleiro_atual)
      print_tabuleiro(tabuleiro_atual)

      resultado = verificar_estado(tabuleiro_atual)
      estados_jogo.append(resultado)
      print(f"Estado do jogo: {resultado}")

      predicao = modelo_mlp.predict([tabuleiro_atual])
      predicoes_ia.append(predicao)
      print(f"Previsão do modelo MLP: {predicao}")

      print("Acuracia: ", accuracy_score(estados_jogo, predicoes_ia))



    if predicao != JOGO:
      print("\nIA detectou encerramento do jogo")
      while(True):
        reiniciar = input("Deseja reiniciar (Y/N)?  ")

        if reiniciar == "Y" or reiniciar == "y":
          restart = True
          game_loop = False
          break
        elif reiniciar == "N" or reiniciar == "n":
          game_loop = False
          break
        else: continue

  if restart:
    limpar_terminal() 
    main()

if __name__ == "__main__":
    main()