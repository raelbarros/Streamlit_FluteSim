from src.utils.graph_plotly import plot_boxsplot
import pandas as pd

# ARQUIVO: generalDroneData

def calculate_flight_height(df):
    """
    Extracts the maximum and minimum flight altitudes from the DataFrame.

    Args:
        df (DataFrame): DataFrame containing drone flight data.

    Returns:
        dict: Dictionary containing 'max_altitude' and 'min_altitude' Series.
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
    Generates a box plot of flight heights for one or multiple simulations.

    Args:
        data_list (list): List of dictionaries returned by calculate_flight_height.
        labels (list, optional): List of simulation names.

    Returns:
        Figure: Plotly Figure object with the box plot.
    """

    if not isinstance(data_list, list):
        data_list = [data_list]
        if labels is None:
            labels = [""]
    if labels is None:
        labels = [f"Simulacao {i+1}" for i in range(len(data_list))]

    # Prepare the data for plotting
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
            'Tipo': 'Mínima',
            'Simulacao': sim_name
        })

        df_combined = pd.concat([df_max, df_min], ignore_index=True)
        data_frames.append(df_combined)

    df_all = pd.concat(data_frames, ignore_index=True)

    labels={'Tipo': 'Tipo de Altitude', 'Altitude': 'Altitude (m)'}
    fig = plot_boxsplot(
        df_all,
        x='Tipo',
        y='Altitude',
        color='Simulacao',
        title='Altura de Voo Máxima e Mínima',
        labels=labels
    )

    return fig

