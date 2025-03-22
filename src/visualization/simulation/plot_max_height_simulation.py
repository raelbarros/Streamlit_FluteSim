import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: generalDroneData

def calculate_max_height_simulation(df):
    """
    Calcula a taxa de colisao com base no DataFrame fornecido.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulaçao.

    Returns:
        dict: Dicionrio com 'media', 'desvio_padrao' e 'intervalo' da taxa de colisao.
    """
    height = df["altitude maxima atingida"].values

    height = height[~np.isnan(height)]

    media = np.mean(height)
    desvio_padrao = np.std(height)

    n = len(height)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0  # Evitar divisao por zero

    return {
        "media": media,
        "desvio_padrao": desvio_padrao,
        "intervalo": intervalo
    }


def plot_max_height_simulation(data, labels=None):
    """
    Gera o grafico de altitude maxima de voo.

    Args:
        data (list or dict): Dados da simulação.
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
        x_label="Arrival rate (drones/min)",
        y_label='Height (m)',
        title='Maximum altitude (m)',
    )
