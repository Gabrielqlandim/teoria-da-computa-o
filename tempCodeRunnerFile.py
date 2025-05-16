import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para calcular a complexidade teórica O(n log n) normalizada
def calc_complexidade_teorica(tamanhos):
    n_log_n = [n * np.log2(n) for n in tamanhos]
    n_log_n_norm = np.array(n_log_n) / max(n_log_n)
    return n_log_n_norm

# Função para gerar os gráficos
def plotar_por_linguagem(df, linguagem_nome, tamanhos=[100, 1000, 10000], casos=["Melhor", "Caso medio", "Pior"]):
    complexidade_norm = calc_complexidade_teorica(tamanhos)
    max_tempo = df['Tempo Médio'].max()
    complexidade_teorica = complexidade_norm * max_tempo
    x = np.arange(len(tamanhos))

    for caso in casos:
        plt.figure(figsize=(10, 6))
        df_caso = df[df['Caso'] == caso]

        tempos = [df_caso[df_caso['Tamanho'] == tam]['Tempo Médio'].values[0] 
                  if not df_caso[df_caso['Tamanho'] == tam].empty else 0 
                  for tam in tamanhos]

        erros = [df_caso[df_caso['Tamanho'] == tam]['Desvio Padrão'].values[0] 
                 if not df_caso[df_caso['Tamanho'] == tam].empty else 0 
                 for tam in tamanhos]

        bars = plt.bar(x, tempos, yerr=erros, capsize=6, width=0.5, label=f'{linguagem_nome}', color='skyblue')
        plt.plot(x, complexidade_teorica, 'r--', label='Complexidade Teórica O(n log n)', linewidth=2)

        # Escreve o desvio padrão acima das barras com destaque
        for i, bar in enumerate(bars):
            altura = bar.get_height()
            dp = erros[i]
            texto = f'DP = {dp:.2e}' if dp > 0 else 'DP = 0'
            plt.text(bar.get_x() + bar.get_width() / 2, altura + max(erros) * 0.2, 
                     texto, ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

        plt.xticks(x, tamanhos)
        plt.xlabel('Tamanho do vetor')
        plt.ylabel('Tempo médio (segundos)')
        plt.title(f'{linguagem_nome} - {caso}\n*DP = Desvio padrão das execuções*', fontsize=13)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # Carrega os arquivos de estatísticas gerados anteriormente
    df_c = pd.read_csv('estatisticas_c.csv')
    df_py = pd.read_csv('estatisticas_python.csv')

    # Gera os gráficos
    plotar_por_linguagem(df_c, 'C')
    plotar_por_linguagem(df_py, 'Python')
