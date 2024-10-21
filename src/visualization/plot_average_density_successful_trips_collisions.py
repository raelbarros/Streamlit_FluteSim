import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
    Arquivo não contemplado no streamlit
    É necessario passar o caminho da pasta para resgatar os arquivos numberOfCollisionsPerInterval, numberOfSuccessfulTripsPerInterval e Summary
"""

# Função para ler e processar múltiplos arquivos summary
def process_summary_file(pasta_simulacoes, num_exec):
    lista_drones = []

    # Iterar sobre todos os arquivos de summary
    for i in range(0, num_exec):
        arquivo_summary = os.path.join(pasta_simulacoes, f'Summary-{i}.txt')
        
        # Ler o arquivo summary
        summary_df = pd.read_csv(arquivo_summary, header=None, names=['Tempo', 'Drones'])

        # Agrupar os dados por intervalos de 10 segundos (20ms * 500 = 10000ms = 10s)
        summary_df['Intervalos_60s'] = summary_df.index // 500  # Agrupa cada 500 linhas
        summary_agrupado = summary_df.groupby('Intervalos_60s').mean()

        # Adicionar os dados processados à lista
        lista_drones.append(summary_agrupado['Drones'])

    # Calcular a média geral da quantidade de drones por intervalo de 60 segundos
    matriz_drones = np.array([drones.to_numpy() for drones in lista_drones])
    media_drones = np.mean(matriz_drones, axis=0)

    return summary_agrupado['Tempo'], media_drones


def read_simulation_file(pasta_simulacoes, prefixo_arquivo, num_exec):
    lista_simulacoes = []
    
    # Ler arquivos de simulação
    for i in range(0, num_exec):
        arquivo = os.path.join(pasta_simulacoes, f"{prefixo_arquivo}-{i}.txt")
        
        # Carregar o arquivo como DataFrame
        df = pd.read_csv(arquivo, delimiter=',', header=None) 
        
        # Adicionar os dados
        lista_simulacoes.append(df)
    
    # Verifica shape do DF
    shapes = [df.shape for df in lista_simulacoes]
    print(f"Shape DataFrames: {shapes}")
    
    # Encontrar o número máximo de linhas e colunas
    max_rows = max(df.shape[0] for df in lista_simulacoes)
    max_cols = max(df.shape[1] for df in lista_simulacoes)
    
    # Padronizar os DataFrames
    lista_simulacoes_padded = []
    for df in lista_simulacoes:
        # Preencher com NaN para linhas e colunas faltantes
        df_padded = df.reindex(index=range(max_rows), columns=range(max_cols))
        lista_simulacoes_padded.append(df_padded)
    
    # Converter em arrays numpy
    matriz_simulacoes = np.array([df.to_numpy() for df in lista_simulacoes_padded])
    
    # Calcular a média, ignorando NaN
    media_simulacoes = np.nanmean(matriz_simulacoes, axis=0)
    
    return media_simulacoes

# Função para plotar grafico
def plotar_grafico_serie_temporal(media_viagens_sucesso, media_colisoes, intervalos_tempo, media_drones_summary, tempo_summary):
    media_colisoes = media_colisoes.flatten()
    media_viagens_sucesso = media_viagens_sucesso.flatten()

    plt.figure(figsize=(10, 6))

    # Plotar a média de viagens bem-sucedidas por intervalo
    plt.plot(intervalos_tempo, media_viagens_sucesso, label='Viagens com Sucesso', color='green', linestyle='-')

    # Plotar a média de colisões por intervalo
    plt.plot(intervalos_tempo, media_colisoes, label='Colisões', color='red', linestyle='-')

    # Plotar a média de drones na simulação por intervalo
    plt.plot(tempo_summary, media_drones_summary, label='Drones', color='orange', linestyle='-')

    # Adicionar títulos e rótulos
    plt.title('')
    plt.xlabel('Intervalos')
    plt.ylabel('Média por Intervalo')

    # Adicionar grade e legenda
    plt.grid(True)
    plt.legend()

    # Exibir o gráfico
    plt.show()


# FIXME: Trocar caminho do arquivo e verificar o valor de 4000 etc.. e num de exec
pasta_simulacoes = r'D:\RESULTS\exec_04 (com esfera)\4_60_30x_model_10\2000-0' 
num_exec = 29

# Processa arquivos com janela temporal de 10s
media_viagens_sucesso = read_simulation_file(pasta_simulacoes, 'numberOfSuccessfulTripsPerInterval', num_exec)
media_colisoes = read_simulation_file(pasta_simulacoes, 'numberOfCollisionsPerInterval', num_exec)

# Processar os dados do summary
tempo_summary, media_drones_summary = process_summary_file(pasta_simulacoes, num_exec)

# Intervalo de tempo de 10s
intervalos_tempo = [i * 10 for i in range(1, media_viagens_sucesso.shape[1] + 1)]

plotar_grafico_serie_temporal(media_viagens_sucesso, media_colisoes, intervalos_tempo, media_drones_summary, tempo_summary)