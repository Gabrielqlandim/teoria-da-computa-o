import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotar_desvio_padrao(df, linguagem_nome, tamanhos=[100, 10000, 100000], casos=["Melhor", "Caso medio", "Pior"]):
    x = np.arange(len(tamanhos))
    plt.figure(figsize=(12, 7))

    largura_barra = 0.25
    deslocamento = [-largura_barra, 0, largura_barra]

    for idx, caso in enumerate(casos):
        df_caso = df[df['Caso'] == caso]

        desvios = [df_caso[df_caso['Tamanho'] == tam]['Desvio Padrão'].values[0]
                   if not df_caso[df_caso['Tamanho'] == tam].empty else 0
                   for tam in tamanhos]

        posicoes = x + deslocamento[idx]
        bars = plt.bar(posicoes, desvios, width=largura_barra, label=f'{caso}', alpha=0.8)

        for i, bar in enumerate(bars):
            altura = bar.get_height()
            texto = f'{altura:.5f}' if altura > 0 else '0'
            plt.text(bar.get_x() + bar.get_width()/2, altura + 0.0005,
                     texto, ha='center', va='bottom', fontsize=9, color='black')

    plt.xticks(x, tamanhos)
    plt.xlabel('Tamanho do vetor')
    plt.ylabel('Desvio padrão (segundos)')
    plt.title(f'{linguagem_nome} - Comparação do Desvio Padrão entre Casos')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    df_c = pd.read_csv('estatisticas_c.csv')
    df_py = pd.read_csv('estatisticas_python.csv')

    plotar_desvio_padrao(df_c, 'C')
    plotar_desvio_padrao(df_py, 'Python')
