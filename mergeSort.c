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

void executar(int tam, int caso, FILE *f){
    double tempos_execucao[1000];

    for(int j=0; j<1000; j++){
        int v[tam];
        clock_t inicio, fim;
        double tempo;

        for(int i=0; i<tam; i++){
            if (caso == 1){
                v[i] = i;
            }
            else if (caso == 2){
                v[i] = rand();
            }
            else if (caso == 3){
                v[i] = tam - i;
            }
        }

        inicio = clock();
        mergeSort(0, tam-1, v, tam);
        fim = clock();

        tempo = ((double)(fim - inicio)) / CLOCKS_PER_SEC;
        tempos_execucao[j] = tempo;
    }

    const char *nome_caso;
    if (caso == 1) nome_caso = "Melhor";
    else if (caso == 2) nome_caso = "Caso medio";
    else nome_caso = "Pior";

    for(int i=0; i<1000; i++){
        fprintf(f, "%s,%d,%d,%.9f\n", nome_caso, tam, i+1, tempos_execucao[i]);
    }
}

int main(void){
    FILE *f = fopen("tempos_c.csv", "w");
    if(f == NULL){
        printf("Erro ao abrir arquivo para escrita\n");
        return 1;
    }

    fprintf(f, "Caso,Tamanho,Execucao,Tempo\n");

    executar(100, 1, f);
    executar(100, 2, f);
    executar(100, 3, f);

    executar(1000, 1, f);
    executar(1000, 2, f);
    executar(1000, 3, f);

    executar(10000, 1, f);
    executar(10000, 2, f);
    executar(10000, 3, f);

    fclose(f);
    return 0;
}