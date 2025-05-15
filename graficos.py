import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para ler e preparar dados
def carregar_dados(arquivo_csv, linguagem_nome):
    df = pd.read_csv(arquivo_csv)
    df['Linguagem'] = linguagem_nome
    return df

# Função para calcular média dos tempos por Caso e Tamanho e Linguagem
def calcular_medias(df):
    return df.groupby(['Linguagem', 'Caso', 'Tamanho'])['Tempo'].mean().reset_index()

# Função para calcular n log n normalizado para o eixo y (escala semelhante)
def calc_complexidade_teorica(tamanhos):
    n_log_n = [n * np.log2(n) for n in tamanhos]
    # Normaliza para ficar parecido com os tempos médios (dividindo pelo maior valor)
    n_log_n_norm = np.array(n_log_n) / max(n_log_n)
    return n_log_n_norm

def plotar_comparativo(df_medias, tamanhos=[100,1000,10000], casos=["Melhor", "Caso medio", "Pior"]):

    complexidade_norm = calc_complexidade_teorica(tamanhos)
    max_tempo = df_medias['Tempo'].max()

    # Para normalizar a complexidade para a escala de tempos reais:
    complexidade_teorica = complexidade_norm * max_tempo

    # Configura a largura das barras
    largura = 0.35
    x = np.arange(len(tamanhos))  # posições dos grupos no eixo x

    for caso in casos:
        plt.figure(figsize=(10,6))
        df_caso = df_medias[df_medias['Caso'] == caso]

        # Extrair tempos para C e Python
        tempos_c = [df_caso[(df_caso['Linguagem']=='C') & (df_caso['Tamanho']==tam)]['Tempo'].values[0] for tam in tamanhos]
        tempos_py = [df_caso[(df_caso['Linguagem']=='Python') & (df_caso['Tamanho']==tam)]['Tempo'].values[0] for tam in tamanhos]

        plt.bar(x - largura/2, tempos_c, width=largura, label='C')
        plt.bar(x + largura/2, tempos_py, width=largura, label='Python')

        plt.plot(x, complexidade_teorica, 'r--', label='Complexidade Teórica O(n log n) (normalizada)', linewidth=2)

        plt.xticks(x, tamanhos)
        plt.xlabel('Tamanho do vetor')
        plt.ylabel('Tempo médio (segundos)')
        plt.title(f'Comparação de tempos - Caso: {caso}')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

# Carrega os dados
df_c = carregar_dados('tempos_c.csv', 'C')
df_py = carregar_dados('tempos_python.csv', 'Python')

# Junta os dados
df_todos = pd.concat([df_c, df_py])

# Calcula as médias
df_medias = calcular_medias(df_todos)

# Plota os gráficos comparativos
plotar_comparativo(df_medias)
