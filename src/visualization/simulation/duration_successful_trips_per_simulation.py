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
    Calculates the average duration of successful trips for the simulation.

    Args:
        df (DataFrame): DataFrame containing drone data.

    Returns:
        dict: Dictionary containing 'media', 'desvio_padrao', and 'intervalo'.
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
    Generates a bar chart of the average duration of successful trips per simulation.

    Args:
        data_list (list): List of dictionaries calculated by the calculate_duration_successful_trips function.
        labels (list, optional): List of labels for the simulations.

    Returns:
        Figure: Plotly figure object.
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

    # Call the plot_bar function
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
