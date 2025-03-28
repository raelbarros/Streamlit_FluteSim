import numpy as np
from src.utils.graph_plotly import plot_bar

# ARQUIVO: generalSimulationData

def calculate_drone_density_per_simulation(df):
    """
    Calcula a densidade media de drones para a simulação.

    Args:
        df (DataFrame): DataFrame contendo os dados da simulação.

    Returns:
        dict: Dicionrio contendo 'media', 'desvio_padrao' e 'intervalo'.
    """
    df.columns = df.columns.str.strip()

    # Extrai o numero total de drones lançados em cada execução
    num_drones = df["numero total de drones lancados"].astype(int)

    # Calcula a media, desvio padrão e intervalo de confiança
    media = num_drones.mean()
    desvio_padrao = num_drones.std()
    n = num_drones.count()
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0

    return {
        "media": media,
        "desvio_padrao": desvio_padrao,
        "intervalo": intervalo
    }


def plot_drone_density_per_simulation(data, labels=None):
    """
    Gera um grafico de barras da densidade media de drones por simulação.

    Args:
        data_list (list): Lista de dicionrios retornados pela função calculate_drone_density.
        labels (list, optional): Lista de labels para as simulaçoes.
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

    # Chama a função plot_bar
    fig = plot_bar(
        values=media,
        intervalos=intervalo,
        labels=labels,
        x_label='Arrival rate (drones/min)',
        y_label='Number of drones',
        title='Average Number of Drones',
        show_interval=True
    )

    return fig