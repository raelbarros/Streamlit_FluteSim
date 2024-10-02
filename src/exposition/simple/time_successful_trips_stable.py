import numpy as np
import pandas as pd
from lib.utils.utils import plot_histogram


#ARQUIVO: generalDroneData

def time_successful_trips_stable(df):
    df.columns = df.columns.str.strip()

    df = df['tempo de viagem total dos drones no tempo estavel']

    # Interquartile Range (IQR)
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    # Definindo os limites para identificar outliers
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Filtrando os dados para remover outliers
    df_filtrado = df[(df >= limite_inferior) & (df <= limite_superior)]


    return plot_histogram(df_filtrado, 'Tempo (s)', 'Numero de Drones', "Tempo de Viagem")
