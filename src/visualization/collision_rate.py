import numpy as np
from src.utils.graph_plotly import plot_bar_simple


def calculate_collision_rate(df):
    """
    Calcula a taxa de colisão com base no DataFrame fornecido.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulação.

    Returns:
        dict: Dicionário com 'media', 'desvio_padrao' e 'intervalo' da taxa de colisão.
    """
    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero de drones lancados no tempo estavel"].values

    # Evitar divisão por zero
    with np.errstate(divide='ignore', invalid='ignore'):
        taxa_colisoes = np.where(num_drones != 0, (num_colisoes / num_drones) * 100, 0)

    media = np.mean(taxa_colisoes)
    desvio_padrao = np.std(taxa_colisoes)

    n = len(taxa_colisoes)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0  # Evitar divisão por zero

    return {
        "media": media,
        "desvio_padrao": desvio_padrao,
        "intervalo": intervalo
    }


def plot_collision_rate(data, labels=None):
    """
    Gera o gráfico da taxa de colisão.

    Args:
        data (list or dict): Dados da taxa de colisão.
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
        labels = labels or [f"Simulação {i+1}" for i in range(len(data))]
    
    else:
        raise ValueError("O parâmetro 'data' deve ser um dicionário ou uma lista de dicionários.")

    return plot_bar_simple(
        values=media,
        intervalos=intervalo,
        labels=labels,
        title="Taxa de Colisão Geral",
        x_label="Simulação",
        y_label="Collision rate (%)",
    )
