import time
import random

def mergeSort(inicio: int, fim: int, v: list[int], tam: int):
    if(inicio < fim):
        meio = (inicio+fim)//2
        mergeSort(inicio, meio, v, tam)
        mergeSort(meio+1, fim, v, tam)
        intercala(inicio, meio, fim, v, tam)

def intercala(inicio: int, meio:int, fim: int, v:list[int], tam: int):
    inicio_v1 = inicio
    inicio_v2 = meio+1
    pos_livre = 0
    aux = [0] * tam

    while(inicio_v1 <= meio and inicio_v2 <= fim):
        if(v[inicio_v1] <= v[inicio_v2]):
            aux[pos_livre] = v[inicio_v1]
            pos_livre+=1
            inicio_v1+=1
        else:
            aux[pos_livre] = v[inicio_v2]
            inicio_v2+=1
            pos_livre+=1
    
    while(inicio_v1 <= meio):
        aux[pos_livre] = v[inicio_v1]
        inicio_v1+=1
        pos_livre+=1
    
    while(inicio_v2 <= fim):
        aux[pos_livre] = v[inicio_v2]
        inicio_v2 +=1
        pos_livre+=1
    
    for i in range(pos_livre):
        v[inicio + i] = aux[i]


v = [random.randint(1,100000) for _ in range(10000)]

tam = len(v)

tempo_inicial = time.time()
mergeSort(0,tam-1,v,tam)
tempo_final = time.time()

print("O tempo do merge sort foi de: ", tempo_final - tempo_inicial)
