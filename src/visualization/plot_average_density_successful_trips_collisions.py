import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
    Arquivo não contemplado no streamlit
    É necessario passar o caminho da pasta para resgatar os arquivos numberOfCollisionsPerInterval, numberOfSuccessfulTripsPerInterval e Summary
"""


# Função para ler e processar arquivos summary
def process_summary_file(pasta_simulacoes, num_exec):
    lista_drones = []
    all_indices = set()

    for i in range(0, num_exec):
        arquivo_summary = os.path.join(pasta_simulacoes, f'Summary-{i}.txt')

        summary_df = pd.read_csv(arquivo_summary, header=None, names=['Tempo', 'Drones'])

        summary_df['Tempo'] = summary_df.index * 0.02

        summary_df['Intervalos_10s'] = (summary_df.index // 500) * 10 
        summary_agrupado = summary_df.groupby('Intervalos_10s').mean()

        all_indices.update(summary_agrupado.index.tolist())
        lista_drones.append(summary_agrupado['Drones'])

    full_index = sorted(all_indices)

    lista_drones_reindexed = [drones.reindex(full_index, fill_value=np.nan) for drones in lista_drones]

    combined_df = pd.concat(lista_drones_reindexed, axis=1)
    media_drones = combined_df.mean(axis=1)

    return combined_df.index, media_drones


def read_and_process_file(pasta_simulacoes, prefixo_arquivo, num_exec):
    lista_colisoes = []
    
    for i in range(0, num_exec):
        arquivo = os.path.join(pasta_simulacoes, f"{prefixo_arquivo}-{i}.txt")
        
        if not os.path.exists(arquivo):
            print(f"Arquivo não encontrado: {arquivo}")
            continue
        
        df = pd.read_csv(arquivo, delimiter=',', header=None)
        df = df.dropna()
        data = df.to_numpy().flatten()
        lista_colisoes.append(data)
    
    max_length = max(len(data) for data in lista_colisoes)
    lista_colisoes_padded = [np.pad(data, (0, max_length - len(data)), 'constant') for data in lista_colisoes]
    matriz_colisoes = np.array(lista_colisoes_padded)
    
    numero_de_colisoes_por_minuto = []
    for execucao in matriz_colisoes:
        colisoes_por_minuto = [np.sum(execucao[i:i+6]) for i in range(0, len(execucao), 6)]
        numero_de_colisoes_por_minuto.append(colisoes_por_minuto)
    
    numero_de_colisoes_por_minuto = np.array(numero_de_colisoes_por_minuto)
    media_colisoes_por_minuto = np.mean(numero_de_colisoes_por_minuto, axis=0)
    
    return media_colisoes_por_minuto



def plotar_grafico(media_viagens_por_minuto, media_colisoes_por_minuto, media_drones, tempo_drones):
    tempo_minutos = np.arange(1, len(media_viagens_por_minuto) + 1) * 60  # Cada ponto representa 60 segundos
    
    plt.figure(figsize=(12, 8))
    
    # Plotar numero de viagens bem-sucedidas
    plt.plot(tempo_minutos, media_viagens_por_minuto, label='Successful trips', color='green')
    
    # Plotar numero de colisões
    plt.plot(tempo_minutos, media_colisoes_por_minuto, label='Collisions', color='red')
    
    # Plotar numero de drones
    plt.plot(tempo_drones, media_drones, label='Drones', color='orange', linestyle='-')
    
    plt.title('')
    plt.xlabel('Time (s)', fontsize=20)
    plt.ylabel('Number of drones', fontsize=20)
    plt.legend(fontsize=15, loc='center')
    plt.grid(False)
    plt.show()


#FIXME: alterar caminho e qtd de execuções, ***COM A PASTA 8000-0 (ou equivalente)***
# Definir parametros
pasta_simulacoes = r'D:\RESULTS\Exec_07\192_60_30x_model_10\10000-0'
num_exec = 29

# Processar dados de viagens com sucesso
media_viagens_por_minuto = read_and_process_file(pasta_simulacoes, 'numberOfSuccessfulTripsPerInterval', num_exec)

# Processar dados de colisões
media_colisoes_por_minuto = read_and_process_file(pasta_simulacoes, 'numberOfCollisionsPerInterval', num_exec)

# Processar dados do summary
tempo_drones, media_drones = process_summary_file(pasta_simulacoes, num_exec)

# Plotar os dados
plotar_grafico(media_viagens_por_minuto, media_colisoes_por_minuto, media_drones, tempo_drones)
