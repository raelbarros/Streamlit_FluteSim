import numpy as np
from src.utils.graph_plotly import plot_bar_simple


def calculate_collision_rate_per_execution(df):
    """
    Calcula a taxa de colisão por execução.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulação.

    Returns:
        dict: Dicionário contendo as execuçoes, taxas de colisão e intervalos (zeros neste caso).
    """
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero de drones lancados no tempo estavel"].values
    execucoes = df["Numero da execucao"].values

    # Evitar divisão por zero
    with np.errstate(divide='ignore', invalid='ignore'):
        taxa_colisao = np.where(num_drones != 0, (num_colisoes / num_drones) * 100, 0)

    n = len(execucoes)
    intervalos = np.zeros(n)  # Intervalos são zeros neste caso

    return {
        "execucoes": execucoes,
        "taxa_colisao": taxa_colisao,
        "intervalos": intervalos
    }


def plot_collision_rate_per_execution(data_list, labels=None):
    """
    Gera o gráfico da taxa de colisão por execução usando plot_bar_simple.

    Args:
        data_list (list): Lista de dicionários, cada um contendo 'execucoes' e 'taxa_colisao' para uma simulação.
        labels (list, optional): Lista de nomes das simulações correspondentes aos dados em data_list.

    Retorna:
        fig (go.Figure): Figura plotly com o gráfico de barras.
    """
    if not isinstance(data_list, list):
        data_list = [data_list]
        if labels is None:
            labels = ["Simulação"]
    
    if labels is None:
        labels = [f"Simulação {i+1}" for i in range(len(data_list))]

    # Obter todas as execuções únicas
    all_execucoes = sorted(set(exec_num for data in data_list for exec_num in data['execucoes']))
    list_exec = [str(exec_num) for exec_num in all_execucoes]

    # Preparar os valores e intervalos para cada simulação
    values_list = []
    intervalos_list = []
    for data in data_list:
        # Criar um dicionário para mapear execuções para taxas de colisão
        exec_taxa_dict = dict(zip(data['execucoes'], data['taxa_colisao']))
        # Obter os valores na ordem de all_execucoes
        series_values = [exec_taxa_dict.get(exec_num, 0) for exec_num in all_execucoes]
        values_list.append(series_values)
        # Intervalos são zeros
        series_intervalos = [0] * len(all_execucoes)
        intervalos_list.append(series_intervalos)

    # Chamar a função plot_bar_simple
    fig = plot_bar_simple(
        values=values_list,
        intervalos=intervalos_list,
        labels=list_exec,
        x_label='Execução',
        y_label='Collision Rate (%)',
        title='Taxa de Colisão por Execução',
        show_interval=False
    )
    # Atualizar os nomes das séries
    for i, sim_name in enumerate(labels):
        fig.data[i].name = sim_name

    return fig