import numpy as np
from src.utils.graph_plotly import plot_bar_simple

# ARQUIVO: generalSimulationData

def calculate_collision_rate_per_execution(df):
    """
    Calcula a taxa de colisao por execuçao.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulaçao.

    Returns:
        dict: Dicionario contendo as execuçoes, taxas de colisao e intervalos (zeros neste caso).
    """
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero de drones lancados no tempo estavel"].values
    execucoes = df["Numero da execucao"].values

    # Evitar divisao por zero
    with np.errstate(divide='ignore', invalid='ignore'):
        taxa_colisao = np.where(num_drones != 0, (num_colisoes / num_drones) * 100, 0)

    n = len(execucoes)
    intervalos = np.zeros(n)  # Intervalos sao zeros neste caso

    return {
        "execucoes": execucoes,
        "taxa_colisao": taxa_colisao,
        "intervalos": intervalos
    }


def plot_collision_rate_per_execution(data_list, labels=None):
    """
    Gera o grafico da taxa de colisao por execuçao usando plot_bar_simple.

    Args:
        data_list (list): Lista de dicionarios, cada um contendo 'execucoes' e 'taxa_colisao' para uma simulaçao.
        labels (list, optional): Lista de nomes das simulaçoes correspondentes aos dados em data_list.

    Retorna:
        fig (go.Figure): Figura plotly com o grafico de barras.
    """
    if not isinstance(data_list, list):
        data_list = [data_list]
        if labels is None:
            labels = ["Simulaçao"]
    
    if labels is None:
        labels = [f"Simulaçao {i+1}" for i in range(len(data_list))]

    # Obter todas as execuçoes unicas
    all_execucoes = sorted(set(exec_num for data in data_list for exec_num in data['execucoes']))
    list_exec = [str(exec_num) for exec_num in all_execucoes]

    # Preparar os valores e intervalos para cada simulaçao
    values_list = []
    intervalos_list = []
    for data in data_list:
        # Criar um dicionario para mapear execuçoes para taxas de colisao
        exec_taxa_dict = dict(zip(data['execucoes'], data['taxa_colisao']))
        # Obter os valores na ordem de all_execucoes
        series_values = [exec_taxa_dict.get(exec_num, 0) for exec_num in all_execucoes]
        values_list.append(series_values)
        # Intervalos sao zeros
        series_intervalos = [0] * len(all_execucoes)
        intervalos_list.append(series_intervalos)

    # Chamar a funçao plot_bar_simple
    fig = plot_bar_simple(
        values=values_list,
        intervalos=intervalos_list,
        labels=list_exec,
        x_label='Execuçao',
        y_label='Collision Rate (%)',
        title='Taxa de Colisao por Execuçao',
        show_interval=False
    )
    # Atualizar os nomes das séries
    for i, sim_name in enumerate(labels):
        fig.data[i].name = sim_name

    return fig