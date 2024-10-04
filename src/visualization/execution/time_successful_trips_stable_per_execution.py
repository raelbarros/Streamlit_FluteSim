from src.utils.graph_plotly import plot_histogram
import pandas as pd
import plotly.express as px


#ARQUIVO: generalDroneData


def calculate_time_successful_trips_stable_per_execution(df):
    """
    Processa dataframe e filtra outliers de tempo de viagem total no tempo estavel

    Args:
        df (DataFrame): DF contendo os dados

    Returns:
        Series: Dados filtrados sem os outliers.
    """
    df.columns = df.columns.str.strip()

    # Seleciona coluna relevante
    travel_times = df['tempo de viagem total dos drones no tempo estavel'].dropna()

    # Calcula Interquartile Range (IQR)
    Q1 = travel_times.quantile(0.25)
    Q3 = travel_times.quantile(0.75)
    IQR = Q3 - Q1

    # Define os limites de outliers
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Filtra os dados pelo limites
    filtered_travel_times = travel_times[(travel_times >= lower_limit) & (travel_times <= upper_limit)]

    return filtered_travel_times


def plot_time_successful_trips_stable_per_execution(data_list, labels=None):
    """
    Gera histograma de tempo de viagem para as simulaçoes.

    Args:
        data_list (list): Lista de dados calculados por calculate_time_successful_trips_stable
        labels (list, optional): Listas de nomes da simulaçao.

    Returns:
        Figure: Objeto de figura Plotly
    """


    if not isinstance(data_list, list):
        data_list = [data_list]

    if labels is None:
        labels = [f"Simulacao {i+1}" for i in range(len(data_list))]

    # Prepara df para plot
    data_frames = []
    for data, sim_name in zip(data_list, labels):
        df = pd.DataFrame({
            'time': data,
            'Simulacao': sim_name
        })
        data_frames.append(df)

    df_all = pd.concat(data_frames, ignore_index=True)

    # Criacaçao do grafico
    labels={'Tempo de Viagem': 'Tempo (s)'}

    fig = plot_histogram(
        df_all, 
        title='Histograma do Tempo de Viagem',
        x='time',
        color='Simulacao',
        labels=labels
    )

    return fig