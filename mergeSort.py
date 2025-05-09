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


# para os vetores que tem tamanho 100
tempos_melhor_100 = []
tempos_pior_100 = []
tempos_medio_100 = []

for i in range(1000):
    v1 = list(range(100))                    # melhor caso
    v2 = list(range(100, 0, -1))             # pior caso
    v3 = [random.randint(1,100000) for _ in range(100)]  # caso médio

    for v, lista_tempos in [(v1, tempos_melhor_100), (v2, tempos_pior_100), (v3, tempos_medio_100)]:
        tam = len(v)
        tempo_inicial = time.time()
        mergeSort(0,tam-1,v,tam)
        tempo_final = time.time()
        lista_tempos.append(tempo_final - tempo_inicial)


# para os vetores que têm tamanho 1000
tempos_melhor_1000 = []
tempos_pior_1000 = []
tempos_medio_1000 = []
for i in range(1000):
    v1 = list(range(1000))                    # melhor caso
    v2 = list(range(1000, 0, -1))             # pior caso
    v3 = [random.randint(1,100000) for _ in range(1000)]  # caso médio

    for v, lista_tempos in [(v1, tempos_melhor_1000), (v2, tempos_pior_1000), (v3, tempos_medio_1000)]:
        tam = len(v)
        tempo_inicial = time.time()
        mergeSort(0,tam-1,v,tam)
        tempo_final = time.time()
        lista_tempos.append(tempo_final-tempo_inicial)

# para os vetores que têm tamanho 10000
tempos_melhor_10000 = []
tempos_pior_10000 = []
tempos_medio_10000 = []
for i in range(1000):
    v1 = list(range(10000))                    # melhor caso
    v2 = list(range(10000, 0, -1))             # pior caso
    v3 = [random.randint(1,100000) for _ in range(10000)]  # caso médio

    for v, lista_tempos in [(v1, tempos_melhor_10000), (v2, tempos_pior_10000), (v3, tempos_medio_10000)]:
        tam = len(v)
        tempo_inicial = time.time()
        mergeSort(0,tam-1,v,tam)
        tempo_final = time.time()
        lista_tempos.append(tempo_final - tempo_inicial)


print("\nTAMANHO 100")
print("Média melhor caso:", sum(tempos_melhor_100)/10)
print("Média pior caso:  ", sum(tempos_pior_100)/10)
print("Média caso médio: ", sum(tempos_medio_100)/10)

print("\nTAMANHO 1000")
print("Média melhor caso:", sum(tempos_melhor_1000)/10)
print("Média pior caso:  ", sum(tempos_pior_1000)/10)
print("Média caso médio: ", sum(tempos_medio_1000)/10)

print("\nTAMANHO 10000")
print("Média melhor caso:", sum(tempos_melhor_10000)/10)
print("Média pior caso:  ", sum(tempos_pior_10000)/10)
print("Média caso médio: ", sum(tempos_medio_10000)/10)
