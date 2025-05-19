import pandas as pd

def calcular_estatisticas(arquivo_csv, linguagem_nome, saida_csv):
    # Carrega o CSV
    df = pd.read_csv(arquivo_csv)

    # Calcula média e desvio padrão por Caso e Tamanho
    estatisticas = df.groupby(['Caso', 'Tamanho'])['Tempo'].agg(['mean', 'std']).reset_index()

    # Renomeia as colunas
    estatisticas.rename(columns={'mean': 'Tempo Médio', 'std': 'Desvio Padrão'}, inplace=True)

    # Adiciona nome da linguagem
    estatisticas['Linguagem'] = linguagem_nome

    # Salva em novo CSV
    estatisticas.to_csv(saida_csv, index=False)
    print(f'Estatísticas salvas em: {saida_csv}')

if __name__ == '__main__':
    # Executa para os dois arquivos
    calcular_estatisticas('csv/tempos_c.csv', 'C', 'csv/estatisticas_c.csv')
    calcular_estatisticas('csv/tempos_python.csv', 'Python', 'csv/estatisticas_python.csv')
