#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h> // Necessário para QueryPerformanceCounter

// A função intercala permanece a mesma
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

// A função mergeSort permanece a mesma
void mergeSort(int inicio, int fim, int v[], int tam){
    if(inicio<fim){
        int meio = (inicio+fim)/2;
        mergeSort(inicio, meio,v, tam);
        mergeSort(meio+1, fim, v, tam);
        intercala(inicio, meio, fim, v, tam);
    }
}

void executar(int tam, int caso, FILE *f){
    double tempos_execucao[15];
    LARGE_INTEGER frequency;        // Para a frequência do contador de performance
    LARGE_INTEGER inicio_pc, fim_pc; // Para os timestamps do contador de performance
    double tempo;

    // Pega a frequência do contador. Isso só precisa ser feito uma vez,
    // mas pode ser feito aqui para manter a lógica de tempo dentro da função.
    QueryPerformanceFrequency(&frequency);

    for(int j=0; j<15; j++){
        int v[tam]; // Considere alocação dinâmica para 'tam' muito grande (malloc)

        // Preenche o vetor v
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

        QueryPerformanceCounter(&inicio_pc); // Captura o timestamp de início
        mergeSort(0, tam-1, v, tam);
        QueryPerformanceCounter(&fim_pc);   // Captura o timestamp de fim

        // Calcula o tempo decorrido em segundos
        tempo = (double)(fim_pc.QuadPart - inicio_pc.QuadPart) / frequency.QuadPart;
        tempos_execucao[j] = tempo;
    }

    const char *nome_caso;
    if (caso == 1) nome_caso = "Melhor";
    else if (caso == 2) nome_caso = "Caso medio";
    else nome_caso = "Pior";

    for(int i=0; i<15; i++){
        fprintf(f, "%s,%d,%d,%.9f\n", nome_caso, tam, i+1, tempos_execucao[i]);
    }
}

int main(void){
    // Inicializa o gerador de números aleatórios para que 'rand()'
    // produza sequências diferentes a cada execução do programa.
    srand(time(NULL));

    FILE *f = fopen("tempos_c.csv", "w");
    if(f == NULL){
        printf("Erro ao abrir arquivo para escrita\n");
        return 1;
    }

    fprintf(f, "Caso,Tamanho,Execucao,Tempo\n");

    executar(1000, 1, f);
    executar(1000, 2, f);
    executar(1000, 3, f);

    executar(10000, 1, f);
    executar(10000, 2, f);
    executar(10000, 3, f);

    executar(100000, 1, f);
    executar(100000, 2, f);
    executar(100000, 3, f);

    fclose(f);
    return 0;
}