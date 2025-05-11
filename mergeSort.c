#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void intercala(int inicio, int meio, int fim, int v[], int tam){
    int inicio_v1 = inicio;
    int inicio_v2 = meio+1;
    int pos_livre = 0;
    int aux[tam];

    while(inicio_v1<=meio && inicio_v2<=fim){
        if(v[inicio_v1] <= v[inicio_v2])
            aux[pos_livre++] = v[inicio_v1++];
        else
            aux[pos_livre++] = v[inicio_v2++];
    }

    while(inicio_v1 <= meio)
        aux[pos_livre++] = v[inicio_v1++];

    while(inicio_v2 <= fim)
        aux[pos_livre++] = v[inicio_v2++];

    for(inicio_v1 = inicio; inicio_v1 <= fim; inicio_v1++)
        v[inicio_v1] = aux[inicio_v1-inicio];
}

void mergeSort(int inicio, int fim, int v[], int tam){
    if(inicio<fim){
        int meio = (inicio+fim)/2;
        mergeSort(inicio, meio,v, tam);
        mergeSort(meio+1, fim, v, tam);
        intercala(inicio, meio, fim, v, tam);
    }
}


void executar(int tam, int caso){

    double tempos_execucao[1000];

    //Laço de reetição para realizar a ordenação 1000 vezes para calcular a média
    for(int j=0; j<1000; j++){

        int v[tam];
        clock_t inicio, fim;
        double tempo;

        //Laço de repetição para inicializar o vetor
        for(int i=0; i<tam; i++){

            //MELHOR CASO - inicia o vetor ordenado
            if (caso == 1){
                v[i] = i;
            }
            //CASO MÉDIO - inicia o vetor com números aleatórios
            else if (caso == 2){
                v[i] = rand();
            }
            //PIOR CASO - cria o vetor ordenado descrescente
            else if (caso == 3){
                v[i] = tam - i;
            }
        }

        //Roda o merge sort e salva os tempos de inicio e fim da execução
        inicio = clock();
        mergeSort(0, tam-1, v, tam);
        fim = clock();

        //Calcula o tempo de execução do código e adiciona na lista de tempos
        tempo = ((double)(fim - inicio)) / CLOCKS_PER_SEC;
        tempos_execucao[j] = tempo;
        
    }

    //Calcula a média de tempo de execução
    double soma = 0.0;
    double media;

    for (int i = 0; i < 1000; i++){
        soma += tempos_execucao[i];
    }

    media = soma/1000;

    if (caso == 1){
        printf("Melhor caso\n");
    }
    else if (caso == 2){
        printf("Caso medio\n");
    }
    else if (caso == 3){
        printf("Pior caso\n");
    }

    printf("Vetor de tamanho %d\n", tam);
    printf("Media de tempo: %f segundos\n", media);
    printf("\n");

}

int main(void){

    executar(100, 1);
    executar(100, 2);
    executar(100, 3);

    executar(1000, 1);
    executar(1000, 2);
    executar(1000, 3);

    executar(10000, 1);
    executar(10000, 2);
    executar(10000, 3);

    return 0;
    
}