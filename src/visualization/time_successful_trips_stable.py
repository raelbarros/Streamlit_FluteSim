from src.utils.graph_plotly import plot_histogram
import pandas as pd
import plotly.express as px


#ARQUIVO: generalDroneData


def calculate_time_successful_trips_stable(df):
    """
    Processes the DataFrame to filter outliers in the total travel time of drones during the stable period.

    Args:
        df (DataFrame): DataFrame containing drone data.

    Returns:
        Series: Filtered Series of travel times without outliers.
    """
    df.columns = df.columns.str.strip()

    # Select the relevant column
    travel_times = df['tempo de viagem total dos drones no tempo estavel'].dropna()

    # Calculate Interquartile Range (IQR)
    Q1 = travel_times.quantile(0.25)
    Q3 = travel_times.quantile(0.75)
    IQR = Q3 - Q1

    # Define the limits to identify outliers
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Filter the data to remove outliers
    filtered_travel_times = travel_times[(travel_times >= lower_limit) & (travel_times <= upper_limit)]

    return filtered_travel_times


def plot_time_successful_trips_stable(data_list, labels=None):
    """
    Generates a histogram of travel times without outliers for one or multiple simulations.

    Args:
        data_list (list): List of Series returned by calculate_time_successful_trips_stable.
        labels (list, optional): List of simulation names.

    Returns:
        Figure: Plotly Figure object with the histogram.
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
        df = pd.DataFrame({
            'time': data,
            'Simulacao': sim_name
        })
        data_frames.append(df)

    df_all = pd.concat(data_frames, ignore_index=True)

    # Create the histogram
    labels={'Tempo de Viagem': 'Tempo (s)'}

    fig = plot_histogram(
        df_all, 
        title='Histograma do Tempo de Viagem',
        x='time',
        color='Simulacao',
        labels=labels
    )

    return fig