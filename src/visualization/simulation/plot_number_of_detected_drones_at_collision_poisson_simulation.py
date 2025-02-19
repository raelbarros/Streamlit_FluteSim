import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: droneCollisionData

def calculate_detected_drones_simulation(df):
    """
    Calcula a quantidade media de drones detectados no momento de colisão por execução e a media geral da simulação.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulação.

    Returns:
        dict: Dicionário com 'media', 'desvio_padrao' e 'intervalo' da taxa de colisão.
    """
    
    # Agrupa por nnum de execução e calcula a media para cada execução
    grouped_means = df.groupby('Numero da execucao')['numero de drones detectados na colisao'].mean()

    # Calcula a media geral das medias por execução
    media = grouped_means.mean()
    desvio_padrao = grouped_means.std()

    n = len(grouped_means)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0  # Evitar divisão por zero

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
        x_label="Arrival rate (drones/min)",
        y_label='',
        title='Number of drones detected at the time of the collision',
    )
