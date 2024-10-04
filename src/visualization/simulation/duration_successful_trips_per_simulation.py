import numpy as np
from src.utils.graph_plotly import plot_bar

#ARQUIVO: generalDroneData

def calculate_confidence_interval(series):
    mean = series.mean()
    std = series.std()
    n = series.count()
    
    if n > 0:
        interval = 1.96 * (std / np.sqrt(n))
    else:
        interval = 0

    return interval

def calculate_duration_successful_trips_per_simulation(df):
    """
    Calcula a media de duraçao das viagem 

    Args:
        df (DataFrame): DF contendo os dados

    Returns:
        dict: Dict contendo 'media', 'desvio_padrao', and 'intervalo'.
    """
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["drone ID", "tempo de viagem total dos drones no tempo estavel"])

    travel_times = df["tempo de viagem total dos drones no tempo estavel"]

    mean = travel_times.mean()
    std = travel_times.std()
    
    interval = calculate_confidence_interval(travel_times)

    return {
        "media": mean,
        "desvio_padrao": std,
        "intervalo": interval
    }

def plot_duration_successful_trips_per_simulation(data, labels=None):
    """
    Gera grafico de barras com a duração media das viagens

    Args:
        data_list (list): Lista de valores calculados por calculate_duration_successful_trips function.
        labels (list, optional): Listas de nomes da simulaçao.

    Returns:
        Figure: Objeto de figura Plotly
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

    # Chama funcao de plot
    fig = plot_bar(
        values=media,
        intervalos=intervalo,
        labels=labels,
        x_label='Simulação',
        y_label='Tempo (s)',
        title='Duração Média das Viagens com Sucesso por Simulação',
        show_interval=True
    )

    return fig
