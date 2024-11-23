//Dojo feito em aula pela turma de 2021/02
//Comentado

//Objetivo: Distribuição de tarefas entre duas pessoas, considerando o tempo estimado em horas para cada tarefa. A meta é
//          não sobrecarregar nenhuma das pessoas, ou seja, a carga em horas recebida pelas pessoas deve ser igual ou muito
//          próxima.


import java.util.Random;

class Main {

//20 Tarefas e suas respectivas horas estimadas para que sejam concluídas
private static int[] cargas = {27, 7, 6, 5, 4, 6, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1,27, 7, 6, 5, 4, 6, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};

//Tamanho da população atual -> número de cromossomos, ou seja, soluções candidatas.
private static final int TAM = 11;

//Populacao Atual
private static int[][] populacao;

//Populacao Intermediaria
private static int[][] intermediaria;

//Ciclo do algoritmo no método main

  public static void main(String[] args) {
    Random rand = new Random();
    populacao = new int[TAM][cargas.length+1];
    intermediaria = new int[TAM][cargas.length+1];
    int melhor;

    //cria a população inicial
    init();    //gera população inicial aleatoriamente
    
    for (int g=0; g<300; g++){
    	System.out.println("Geração: " + g);
    	calculaAptidao();   //calcula a aptidão (função heurística) dos cronomossomos
    	printMatriz();      //escreva a população atual na tela
    	melhor = getBest(); //aplica elitismo
    	System.out.println( "Metodo Elitismo = " + melhor);
    	if(achouSolucao(melhor)) break;  //verifica se achou a solução
    	crossover();	    //realiza torneio e cruzamento - taxa de 100%
    	populacao = intermediaria;  //concluida a populacao intermediária, ela se torna a nova população atual
    	if(rand.nextInt(5)==0) {    //aplica mutação (chance)
    		System.out.println("Mutação");
    		mutacao();
    	}	
    }
  }


  //Gera aleatoriamente as distribuições de cargas, inicializa a população inicial.  
  public static void  init() {
    Random rand = new Random();

    for (int i=0; i < TAM; i++) {
      for (int j=0; j < cargas.length; j++) {
        populacao[i][j] = rand.nextInt(2);
      }
    }
  }

  //Escreve a população inicial e as aptidões dos cronomossos
  public static void printMatriz() {
    int j = 0;
    for (int i=0; i < TAM; i++) {
      System.out.print("C: " + i + " - ");
      for (j=0; j < cargas.length; j++) {
        System.out.print(populacao[i][j] + " ");
      }
      System.out.println("F: " + populacao[i][j]);
    }
  }
  
  //Calcula a aptidão - Função heurística dos cromossomos
  public static int aptidao(int individuo){
   int somaZero = 0;
   int somaUm = 0;
    for(int j = 0; j < cargas.length; j++){
      if(populacao[individuo][j] == 0 ){
        somaZero += cargas[j];
      } else {
        somaUm += cargas[j];
      }
    }
    return Math.abs(somaZero - somaUm);

  }

  //Atribui aptidão a ultima coluna da população
  public static void calculaAptidao(){
  for(int i = 0; i < TAM; i++){
    populacao[i][cargas.length] = aptidao(i);
  }
}

  //Elitismo - encontra o melhor cromossomo da população atual e copia para primeira linha da população intermediária
  public static int getBest(){
    int min = populacao[0][cargas.length];
    int linha = 0;
    for(int i = 1; i < TAM; i++){
      if(populacao[i][cargas.length] < min){
        min = populacao[i][cargas.length];
        linha = i;
      }
    }

    for(int i = 0; i < cargas.length; i++)
      intermediaria[0][i] = populacao[linha][i];

  return linha;
  }

  //Seleção por torneio : escolhe os cromossomos que serão cruzados
  public static int torneio(){
    Random rand = new Random();
    int individuo1 ,individuo2;

    individuo1 = rand.nextInt(TAM);
    individuo2 = rand.nextInt(TAM);

  if(populacao[individuo1][cargas.length] < populacao[individuo2][cargas.length])
    return individuo1;
  else
    return individuo2;
  }

  //Cruzamento uniponto
  public static void crossover(){
     
      for (int j=1; j<TAM; j=j+2){
         int ind1 = torneio();
         int ind2 = torneio();
        for (int k=0; k<cargas.length/2; k++){
        	intermediaria [j][k]= populacao [ind1][k];
        	intermediaria [j+1][k]= populacao [ind2][k];
        }
        for (int k=cargas.length/2; k<cargas.length; k++){
        	intermediaria [j][k]= populacao [ind2][k];
        	intermediaria [j+1][k]= populacao [ind1][k];
        }
      }
    
  }
  
  //Mutação
  public static void mutacao(){
       Random rand = new Random();
       int quant = rand.nextInt(3)+1;
       for(int i = 0; i<quant; i++){
       	int individuo = rand.nextInt(TAM);
       	int posicao = rand.nextInt(cargas.length);
       
       	System.out.println("Cromossomo " + individuo + " sofreu mutação na carga de indice " + posicao);
      	 	if(populacao[individuo][posicao]==0) populacao[individuo][posicao]=1;
       	else populacao[individuo][posicao]=0;
       }
      
  }
  
  //Verifica se a solução foi encontrada
  public static boolean achouSolucao(int melhor){
  	if(populacao[melhor][cargas.length]==0){
  		int soma = 0;
  		System.out.println("\nAchou a solução ótima. Ela corresponde ao cromossomo :"+ melhor);
  		System.out.println("Solução Decodificada: ");
  		System.out.println("Pessoa 0: ");
  		for(int i=0; i<cargas.length; i++) 
  			if(populacao[melhor][i]==0) {
  				System.out.print(cargas[i]+ " ");
  				soma = soma + cargas[i];
  		        }
  		System.out.println(" - Total: " + soma);
  		
  		soma = 0;
  		System.out.println("Pessoa 1: ");
  		for(int i=0; i<cargas.length; i++) 
  			if(populacao[melhor][i]==1) {
  				System.out.print(cargas[i]+ " ");
  				soma = soma + cargas[i];
  		        }
  		System.out.println(" - Total: " + soma);
  		return true;		
  	}
  	return false;
  }
}

