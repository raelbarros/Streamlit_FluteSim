import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: generalSimulationData

def calculate_drone_density_per_execution(df):
    """
    Calcula a densidade de drones por execuçao.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulaçao.

    Returns:
        dict: Dicionario contendo 'execucoes' e 'num_drones'.
    """
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    execucoes = df["Numero da execucao"].values.astype(int)
    num_drones = df["numero total de drones lancados"].values.astype(int)

    return {
        "execucoes": execucoes,
        "num_drones": num_drones
    }


def plot_drone_density_per_execution(data_list, labels=None):
    """
    Gera o grafico da densidade de drones por execuçao.

    Args:
        data_list (list): Lista de dicionarios retornados por calculate_drone_density_per_execution.
        labels (list, optional): Lista de nomes das simulaçoes correspondentes aos dados em data_list.

    Returns:
        Figure: Objeto de figura Plotly.
    """
    if not isinstance(data_list, list):
        data_list = [data_list]
    
    if labels is None:
        labels = [f"Simulaçao {i+1}" for i in range(len(data_list))]

    # Obter todas as execuçoes unicas
    all_execucoes = sorted(set(exec_num for data in data_list for exec_num in data['execucoes']))
    num_exec = [str(exec_num) for exec_num in all_execucoes]

    # Preparar os valores para cada simulaçao
    values_list = []
    intervalos_list = []
    
    for data in data_list:
        # Criar um dicionario para mapear execuçoes para numero de drones
        exec_num_drones_dict = dict(zip(data['execucoes'], data['num_drones']))
        
        # Obter os valores na ordem de all_execucoes
        series_values = [exec_num_drones_dict.get(exec_num, 0) for exec_num in all_execucoes]
        values_list.append(series_values)
        
        # Intervalos sao zeros
        series_intervalos = [0] * len(all_execucoes)
        intervalos_list.append(series_intervalos)

    # Chama a funçao plot_bar
    fig = plot_bar(
        values=values_list,
        intervalos=intervalos_list,
        labels=num_exec,
        x_label='Execuçao',
        y_label='Quantidade de Drones',
        title='Densidade de Drones por Execuçao',
        show_interval=False
    )
    # Atualizar os nomes das séries
    for i, sim_name in enumerate(labels):
        fig.data[i].name = sim_name

    return fig