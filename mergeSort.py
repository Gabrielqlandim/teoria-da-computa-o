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

tempos_execucao1 = []
tempos_execucao2 = []
tempos_execucao3 = []

for i in range(1000):
    v = [random.randint(1,100000) for _ in range(1000)]

    tam = len(v)

    tempo_inicial = time.time()
    mergeSort(0,tam-1,v,tam)
    tempo_final = time.time()

    tempo_execucao1 = tempo_final - tempo_inicial

    tempos_execucao1.append(tempo_execucao1)

for i in range(1000):
    v2 = [random.randint(1,100000) for _ in range(100)]

    tam = len(v2)

    tempo_inicial = time.time()
    mergeSort(0,tam-1,v2,tam)
    tempo_final = time.time()

    tempo_execucao2 = tempo_final - tempo_inicial

    tempos_execucao2.append(tempo_execucao2)

for i in range(1000):
    v3 = [random.randint(1,100000) for _ in range(10000)]

    tam = len(v3)

    tempo_inicial = time.time()
    mergeSort(0,tam-1,v3,tam)
    tempo_final = time.time()

    tempo_execucao3 = tempo_final - tempo_inicial

    tempos_execucao3.append(tempo_execucao3)


print("A média do tempo de execução do vetor com 1000 foi de: ", sum(tempos_execucao1)/1000)
print("A média do tempo de execução do vetor com 100 foi de: ", sum(tempos_execucao2)/1000)
print("A média do tempo de execução do vetor com 10000 foi de: ", sum(tempos_execucao3)/1000)
