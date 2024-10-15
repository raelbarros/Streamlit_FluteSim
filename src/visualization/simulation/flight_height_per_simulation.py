from src.utils.graph_plotly import plot_boxsplot
import pandas as pd

# ARQUIVO: generalDroneData

def calculate_flight_height(df):
    """
    Coleta altitude maxima e minima o DF

    Args:
        df (DataFrame): DF com os dados de voou.

    Returns:
        dict: Dict contendo 'max_altitude' e 'min_altitude'
    """
    df.columns = df.columns.str.strip()

    # Remove rows with missing altitude data
    df = df.dropna(subset=["altitude maxima atingida", "altitude minima atingida"])

    max_altitude = df["altitude maxima atingida"]
    min_altitude = df["altitude minima atingida"]

    return {
        "max_altitude": max_altitude,
        "min_altitude": min_altitude
    }


def plot_flight_height(data_list, labels=None):
    """
    Gera boxsplot de altura de voo 
    
    Args:
        data_list (list): Lista de valores calculados por calculate_flight_height.
        labels (list, optional): Listas de nomes da simulaçao.

    Returns:
        Figure: Objeto de figura Plotly
    """

    if not isinstance(data_list, list):
        data_list = [data_list]
        if labels is None:
            labels = [""]
    if labels is None:
        labels = [f"Simulacao {i+1}" for i in range(len(data_list))]

    # Prepara df para plot
    data_frames = []
    for data, sim_name in zip(data_list, labels):
        df_max = data['max_altitude']
        df_min = data['min_altitude']

        df_max = pd.DataFrame({
            'Altitude': df_max,
            'Tipo': 'Máxima',
            'Simulacao': sim_name
        })
        df_min = pd.DataFrame({
            'Altitude': df_min,
            'Tipo': 'Minima',
            'Simulacao': sim_name
        })

        df_combined = pd.concat([df_max, df_min], ignore_index=True)
        data_frames.append(df_combined)

    df_all = pd.concat(data_frames, ignore_index=True)

    # Criacaçao do grafico
    labels={'Tipo': 'Tipo de Altitude', 'Altitude': 'Altitude (m)'}
    fig = plot_boxsplot(
        df_all,
        x='Tipo',
        y='Altitude',
        color='Simulacao',
        title='Altura de Voo Mxima e Minima',
        labels=labels
    )

    return fig

