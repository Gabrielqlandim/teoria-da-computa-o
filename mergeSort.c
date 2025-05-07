#include <stdio.h>

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

int main(void){
    int v[] = {38, 27, 43, 3, 9, 82, 10};

    int tam = sizeof(v)/sizeof(v[0]);

    mergeSort(0, tam-1, v, tam);

    printf("Vetor em ordem: ");

    for(int i=0; i<tam; i++)
        printf("%d ", v[i]);
    
    printf("\n");

    return 0;
}