import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: droneCollisionData

def calculate_dected_drones_simulation(df):
    """
    Calcula a quantidade de drones detectados no momento de colisão.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulaçao.

    Returns:
        dict: Dicionrio com 'media', 'desvio_padrao' e 'intervalo' da taxa de colisao.
    """
    num_colisoes = df["numero de drones detectados na colisao"].values

    media = np.mean(num_colisoes)
    desvio_padrao = np.std(num_colisoes)

    n = len(num_colisoes)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0  # Evitar divisao por zero

    return {
        "media": media,
        "desvio_padrao": desvio_padrao,
        "intervalo": intervalo
    }


def plot_dected_drones_per_simulation(data, labels=None):
    """
    Gera o grafico da de quantidade de drones detectados no momento de colisão.

    Args:
        data (list or dict): Dados.
        labels (list, optional): Lista de labels para as barras.

    Returns:
        Figure: Objeto de figura Plotly.
    """
    if isinstance(data, dict):
        media = np.array([data['media']])
        intervalo = np.array([data['intervalo']])
        labels = labels or [""]
    
    elif isinstance(data, list):
        # Caso de multiplas simulaçoes, agregamos os dados
        media = np.array([d['media'] for d in data])
        intervalo = np.array([d['intervalo'] for d in data])
        labels = labels or [f"Simulaçao {i+1}" for i in range(len(data))]
    
    else:
        raise ValueError("O parâmetro 'data' deve ser um dicionrio ou uma lista de dicionrios.")

    return plot_bar(
        values=media,
        intervalos=intervalo,
        labels=labels,
        x_label='Simulação',
        y_label='Quantidade',
        title='Numero de drones detectados no momento da colisão',
    )
