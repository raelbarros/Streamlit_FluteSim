import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: generalSimulationData

def calculate_collision_rate_per_simulation(df):
    """
    Calcula a taxa de colisao com base no DataFrame fornecido.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulaçao.

    Returns:
        dict: Dicionrio com 'media', 'desvio_padrao' e 'intervalo' da taxa de colisao.
    """
    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero total de drones lancados"].values

    # Evitar divisao por zero
    with np.errstate(divide='ignore', invalid='ignore'):
        taxa_colisoes = np.where(num_drones != 0, (num_colisoes / num_drones) * 100, 0)

    media = np.mean(taxa_colisoes)
    desvio_padrao = np.std(taxa_colisoes)

    n = len(taxa_colisoes)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0  # Evitar divisao por zero

    return {
        "media": media,
        "desvio_padrao": desvio_padrao,
        "intervalo": intervalo
    }


def plot_collision_rate_per_simulation(data, labels=None):
    """
    Gera o grafico da taxa de colisao.

    Args:
        data (list or dict): Dados da taxa de colisao.
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
        title="Taxa de Colisão (%)",
        x_label="Taxa de Lançamento (drones/min)",
        y_label="Taxa de Colisão (%)",
    )
