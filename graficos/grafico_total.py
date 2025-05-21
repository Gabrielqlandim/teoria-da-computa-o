import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar e preparar os dados
def carregar_dados(arquivo_csv, linguagem_nome):
    df = pd.read_csv(arquivo_csv)
    df['Linguagem'] = linguagem_nome
    return df

# Calcular média dos tempos por Caso e Tamanho
def calcular_medias(df):
    return df.groupby(['Caso', 'Tamanho'])['Tempo'].mean().reset_index()

# Calcular O(n log n) normalizado
def calc_complexidade_teorica(tamanhos):
    n_log_n = [n * np.log2(n) for n in tamanhos]
    n_log_n_norm = np.array(n_log_n) / max(n_log_n)
    return n_log_n_norm

# Gerar gráfico agrupado para Melhor, Caso médio e Pior
def plotar_casos_juntos(df_medias, linguagem_nome, tamanhos=[100, 1000, 10000], casos=["Melhor", "Caso medio", "Pior"]):
    x = np.arange(len(tamanhos))
    n_casos = len(casos)
    largura = 0.8 / n_casos  # dividir o espaço das barras igualmente

    plt.figure(figsize=(12, 7))

    # Para posicionar as barras corretamente
    offsets = np.linspace(-0.4 + largura/2, 0.4 - largura/2, n_casos)

    for i, caso in enumerate(casos):
        tempos = [
            df_medias[(df_medias['Caso'] == caso) & (df_medias['Tamanho'] == tam)]['Tempo'].values[0]
            if not df_medias[(df_medias['Caso'] == caso) & (df_medias['Tamanho'] == tam)].empty else 0
            for tam in tamanhos
        ]
        plt.bar(x + offsets[i], tempos, width=largura, label=caso)

    complexidade_norm = calc_complexidade_teorica(tamanhos)
    max_tempo = df_medias['Tempo'].max()
    complexidade_teorica = complexidade_norm * max_tempo
    plt.plot(x, complexidade_teorica, 'r--', label='Complexidade Teórica O(n log n)', linewidth=2)

    plt.xticks(x, tamanhos)
    plt.xlabel('Tamanho do vetor')
    plt.ylabel('Tempo médio (segundos)')
    plt.title(f'{linguagem_nome} - Comparação dos Casos por Tamanho')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# Carregar os arquivos CSV
df_c = carregar_dados('tempos_c.csv', 'C')
df_py = carregar_dados('tempos_python.csv', 'Python')

# Calcular médias
df_c_medias = calcular_medias(df_c)
df_py_medias = calcular_medias(df_py)

# Plotar gráfico para C e Python
plotar_casos_juntos(df_c_medias, 'C')
plotar_casos_juntos(df_py_medias, 'Python')

print(df_c_medias)
print(df_py_medias)
