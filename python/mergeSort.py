import csv
import time
import random

def intercala(inicio, meio, fim, v, tam):
    inicio_v1 = inicio
    inicio_v2 = meio + 1
    pos_livre = 0
    aux = [0] * tam

    while inicio_v1 <= meio and inicio_v2 <= fim:
        if v[inicio_v1] <= v[inicio_v2]:
            aux[pos_livre] = v[inicio_v1]
            inicio_v1 += 1
        else:
            aux[pos_livre] = v[inicio_v2]
            inicio_v2 += 1
        pos_livre += 1

    while inicio_v1 <= meio:
        aux[pos_livre] = v[inicio_v1]
        inicio_v1 += 1
        pos_livre += 1

    while inicio_v2 <= fim:
        aux[pos_livre] = v[inicio_v2]
        inicio_v2 += 1
        pos_livre += 1

    for i in range(pos_livre):
        v[inicio + i] = aux[i]

def mergeSort(inicio, fim, v, tam):
    if inicio < fim:
        meio = (inicio + fim) // 2
        mergeSort(inicio, meio, v, tam)
        mergeSort(meio + 1, fim, v, tam)
        intercala(inicio, meio, fim, v, tam)

def gerar_e_salvar_csv(nome_arquivo):
    casos = {
        "Melhor": lambda tam: list(range(tam)),
        "Caso medio": lambda tam: [random.randint(1, tam) for _ in range(tam)],
        "Pior": lambda tam: list(range(tam, 0, -1))
    }

    tamanhos = [100, 1000, 10000]

    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["Caso", "Tamanho", "Execucao", "Tempo"])

        for tam in tamanhos:
            for caso_nome, func in casos.items():
                for execucao in range(1, 1001):
                    v = func(tam)
                    inicio = time.time()
                    mergeSort(0, tam - 1, v, tam)
                    fim = time.time()
                    tempo = fim - inicio
                    escritor.writerow([caso_nome, tam, execucao, tempo])

if __name__ == "__main__":
    gerar_e_salvar_csv("tempos_python.csv")
