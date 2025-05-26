import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar dados de estatísticas
def carregar_estatisticas(arquivo_csv):
    try:
        df = pd.read_csv(arquivo_csv)
        cols_necessarias = ['Caso', 'Tamanho', 'Tempo Médio', 'Desvio Padrão', 'Linguagem']
        for col in cols_necessarias:
            if col not in df.columns:
                # Se a coluna 'Linguagem' não existir, tenta adicionar com base no nome do arquivo
                if col == 'Linguagem' and 'estatisticas_c' in arquivo_csv:
                    df['Linguagem'] = 'C'
                elif col == 'Linguagem' and 'estatisticas_python' in arquivo_csv:
                    df['Linguagem'] = 'Python'
                else:
                    raise ValueError(f"Coluna '{col}' não encontrada no arquivo {arquivo_csv}")
        
        df['Tempo Médio'] = pd.to_numeric(df['Tempo Médio'], errors='coerce')
        df['Desvio Padrão'] = pd.to_numeric(df['Desvio Padrão'], errors='coerce')
        df['Tamanho'] = pd.to_numeric(df['Tamanho'], errors='coerce')
        df.dropna(subset=['Tempo Médio', 'Tamanho'], inplace=True)
        df['Desvio Padrão'].fillna(0, inplace=True) # Preenche NaN no Desvio Padrão com 0
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo_csv} não encontrado.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro ao carregar ou processar {arquivo_csv}: {e}")
        return pd.DataFrame()

# Função para plotar gráficos por linguagem e por tamanho
def plotar_casos_por_tamanho_linguagem(df_stats, linguagem_nome, tamanhos_desejados=[1000, 10000, 100000], casos_plot=["Melhor", "Caso medio", "Pior"]):
    if df_stats.empty:
        print(f"Nenhum dado fornecido para {linguagem_nome}.")
        return

    df_lang = df_stats[df_stats['Linguagem'] == linguagem_nome]
    if df_lang.empty:
        print(f"Nenhum dado para a linguagem {linguagem_nome}.")
        return

    for tam in tamanhos_desejados:
        df_tamanho = df_lang[df_lang['Tamanho'] == tam]
        if df_tamanho.empty:
            print(f"Nenhum dado para {linguagem_nome} com tamanho N={tam}.")
            continue

        medias = []
        desvios = []
        casos_encontrados = []

        for caso in casos_plot:
            data_caso = df_tamanho[df_tamanho['Caso'] == caso]
            if not data_caso.empty:
                medias.append(data_caso['Tempo Médio'].iloc[0])
                desvios.append(data_caso['Desvio Padrão'].iloc[0])
                casos_encontrados.append(caso)
            else:
                # Adiciona placeholders se o caso não for encontrado para manter o alinhamento
                medias.append(0)
                desvios.append(0)
                if caso not in casos_encontrados: # Evita adicionar casos placeholder se não houver dados
                     casos_encontrados.append(caso + " (sem dados)")


        if not any(m > 0 for m in medias): # Pula se não houver dados significativos
            print(f"Nenhum dado de tempo médio significativo para {linguagem_nome}, N={tam}.")
            continue
            
        x = np.arange(len(casos_plot)) # Usar casos_plot para o eixo x garante 3 posições

        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        
        bars = ax.bar(x, medias, yerr=desvios, capsize=5, alpha=0.8, color=['#1f77b4', '#ff7f0e', '#2ca02c']) # Cores para Melhor, Médio, Pior
        
        ax.set_xticks(x)
        ax.set_xticklabels(casos_plot) # Rótulos do eixo x são os casos
        ax.set_xlabel('Caso de Teste')
        ax.set_ylabel('Tempo Médio (s) com Desvio Padrão')
        ax.set_title(f'{linguagem_nome} - Desempenho para N={tam}')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Adicionar valores nas barras
        for bar in bars:
            yval = bar.get_height()
            if yval > 0 : # Só anota se a barra tiver altura
                plt.text(bar.get_x() + bar.get_width()/2.0, yval + (max(medias) * 0.01 if medias else 0), f'{yval:.6f}', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.show()

# Função para plotar gráficos comparativos C vs Python
def plotar_comparativo_linguagens(df_c_stats, df_py_stats, tamanhos_desejados=[1000, 10000, 100000], casos_plot=["Melhor", "Caso medio", "Pior"]):
    if df_c_stats.empty or df_py_stats.empty:
        print("Dados de C ou Python Faltando. Gráficos comparativos não serão gerados.")
        return

    df_c_filtrado = df_c_stats[df_c_stats['Tamanho'].isin(tamanhos_desejados)]
    df_py_filtrado = df_py_stats[df_py_stats['Tamanho'].isin(tamanhos_desejados)]

    if df_c_filtrado.empty and df_py_filtrado.empty: # Verifica se ambos estão vazios após o filtro
        print("Nenhum dado para os tamanhos especificados em C ou Python para comparação.")
        return
    
    # Garante que estamos comparando apenas tamanhos presentes em AMBOS os dataframes filtrados
    tamanhos_comuns = sorted(list(set(df_c_filtrado['Tamanho']) & set(df_py_filtrado['Tamanho'])))
    if not tamanhos_comuns:
        print("Nenhum tamanho em comum entre C e Python para os filtros aplicados.")
        return

    n_tamanhos = len(tamanhos_comuns)
    x_indices = np.arange(n_tamanhos) 
    
    for caso_atual in casos_plot:
        medias_c = []
        desvios_c = []
        medias_py = []
        desvios_py = []
        
        # Coleta dados apenas para tamanhos comuns
        for tam_atual in tamanhos_comuns:
            data_c = df_c_filtrado[(df_c_filtrado['Caso'] == caso_atual) & (df_c_filtrado['Tamanho'] == tam_atual)]
            data_py = df_py_filtrado[(df_py_filtrado['Caso'] == caso_atual) & (df_py_filtrado['Tamanho'] == tam_atual)]

            medias_c.append(data_c['Tempo Médio'].iloc[0] if not data_c.empty else 0)
            desvios_c.append(data_c['Desvio Padrão'].iloc[0] if not data_c.empty and pd.notna(data_c['Desvio Padrão'].iloc[0]) else 0)
            
            medias_py.append(data_py['Tempo Médio'].iloc[0] if not data_py.empty else 0)
            desvios_py.append(data_py['Desvio Padrão'].iloc[0] if not data_py.empty and pd.notna(data_py['Desvio Padrão'].iloc[0]) else 0)
        
        if not any(m > 0 for m in medias_c + medias_py): # Pula se não houver dados significativos
            print(f"Nenhum dado de tempo médio significativo para comparação no caso: {caso_atual}.")
            continue

        plt.figure(figsize=(12, 7))
        ax = plt.gca()
        largura_barra = 0.35

        bar1 = ax.bar(x_indices - largura_barra/2, medias_c, width=largura_barra, label='C', yerr=desvios_c, capsize=5, color='blue', alpha=0.8)
        bar2 = ax.bar(x_indices + largura_barra/2, medias_py, width=largura_barra, label='Python', yerr=desvios_py, capsize=5, color='orange', alpha=0.8)

        ax.set_xticks(x_indices)
        ax.set_xticklabels(tamanhos_comuns)
        ax.set_xlabel('Tamanho do vetor (n)')
        ax.set_ylabel('Tempo Médio (s) com Desvio Padrão')
        ax.set_title(f'Comparativo C vs Python - Caso: {caso_atual}')
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Adicionar valores nas barras
        for bar_group in [bar1, bar2]:
            for bar in bar_group:
                yval = bar.get_height()
                if yval > 0:
                     plt.text(bar.get_x() + bar.get_width()/2.0, yval + (max(medias_c + medias_py) * 0.01 if medias_c + medias_py else 0), f'{yval:.6f}', ha='center', va='bottom', fontsize=8)
        
        # Considerar escala logarítmica se os tempos de Python forem muito maiores
        max_py_time = max(medias_py) if medias_py else 0
        min_c_time_non_zero = min(m for m in medias_c if m > 0) if any(m > 0 for m in medias_c) else max_py_time # Evita divisão por zero ou min de lista vazia
        if max_py_time > 0 and min_c_time_non_zero > 0 and max_py_time / min_c_time_non_zero > 50: # Heurística para escala log
            ax.set_yscale('log')
            ax.set_ylabel('Tempo Médio (s) com Desvio Padrão (Escala Log)')
            print(f"Usando escala logarítmica para o gráfico comparativo do caso: {caso_atual}")


        plt.tight_layout()
        plt.show()

# --- Execução Principal ---
if __name__ == '__main__':
    df_c_stats = carregar_estatisticas('estatisticas_c.csv')
    df_py_stats = carregar_estatisticas('estatisticas_python.csv')

    tamanhos_para_plotar = [1000, 10000, 100000]
    casos_para_plotar = ["Melhor", "Caso medio", "Pior"]

    # Gerar gráficos por linguagem e por tamanho
    if not df_c_stats.empty:
        plotar_casos_por_tamanho_linguagem(df_c_stats, 'C', tamanhos_desejados=tamanhos_para_plotar, casos_plot=casos_para_plotar)
    else:
        print("Não foi possível gerar gráficos para C (por tamanho) devido a erro ao carregar dados.")
        
    if not df_py_stats.empty:
        plotar_casos_por_tamanho_linguagem(df_py_stats, 'Python', tamanhos_desejados=tamanhos_para_plotar, casos_plot=casos_para_plotar)
    else:
        print("Não foi possível gerar gráficos para Python (por tamanho) devido a erro ao carregar dados.")

    # Gerar gráficos comparativos C vs Python
    if not df_c_stats.empty and not df_py_stats.empty:
        plotar_comparativo_linguagens(df_c_stats, df_py_stats, tamanhos_desejados=tamanhos_para_plotar, casos_plot=casos_para_plotar)
    else:
        print("Não foi possível gerar gráficos comparativos C vs Python devido a erro ao carregar dados de uma ou ambas as linguagens.")
