import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar e preparar os dados
def carregar_dados(arquivo_csv, linguagem_nome):
    df = pd.read_csv(arquivo_csv)
    df['Linguagem'] = linguagem_nome
    return df

# Função para calcular média dos tempos por Caso e Tamanho
def calcular_medias(df):
    return df.groupby(['Caso', 'Tamanho'])['Tempo'].mean().reset_index()

# Função para calcular O(n log n) normalizado
def calc_complexidade_teorica(tamanhos):
    n_log_n = [n * np.log2(n) for n in tamanhos]
    n_log_n_norm = np.array(n_log_n) / max(n_log_n)
    return n_log_n_norm

# Função para gerar gráficos por linguagem
def plotar_por_linguagem(df_medias, linguagem_nome, tamanhos=[100, 1000, 10000], casos=["Melhor", "Caso medio", "Pior"]):
    complexidade_norm = calc_complexidade_teorica(tamanhos)
    max_tempo = df_medias['Tempo'].max()
    complexidade_teorica = complexidade_norm * max_tempo
    x = np.arange(len(tamanhos))

    for caso in casos:
        plt.figure(figsize=(10, 6))
        df_caso = df_medias[df_medias['Caso'] == caso]

        tempos = [df_caso[df_caso['Tamanho'] == tam]['Tempo'].values[0] 
                  if not df_caso[df_caso['Tamanho'] == tam].empty else 0 
                  for tam in tamanhos]

        plt.bar(x, tempos, width=0.4, label=f'{linguagem_nome}')
        plt.plot(x, complexidade_teorica, 'r--', label='Complexidade Teórica O(n log n)', linewidth=2)

        plt.xticks(x, tamanhos)
        plt.xlabel('Tamanho do vetor')
        plt.ylabel('Tempo médio (segundos)')
        plt.title(f'{linguagem_nome} - Comparação por caso: {caso}')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

# Carregar os arquivos CSV
df_c = carregar_dados('tempos_c.csv', 'C')
df_py = carregar_dados('tempos_python.csv', 'Python')

# Calcular as médias por linguagem
df_c_medias = calcular_medias(df_c)
df_py_medias = calcular_medias(df_py)

# Gerar os gráficos separados
plotar_por_linguagem(df_c_medias, 'C')
plotar_por_linguagem(df_py_medias, 'Python')
