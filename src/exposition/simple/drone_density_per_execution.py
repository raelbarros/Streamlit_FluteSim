import pandas as pd
import numpy as np
from lib.utils.utils import plot_bar_simple

# ARQUIVO: generalSimulationData

def drone_density_per_execution(df):
    df.columns = df.columns.str.strip()

    df = df.sort_values(by="Numero da execucao")

    num_drones = np.array(df["numero total de drones lancados"].values)
    label = np.array(df["Numero da execucao"].values)
    
    n = len(df["Numero da execucao"])
    list_intervalo = np.zeros(n)
    
    return plot_bar_simple(
        labels=label,
        values=num_drones,
        intervalos=list_intervalo,
        title="Densidade de Drones por execução",
        x_label="Simulação",
        y_label="Quantidade",
    )


# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
# https://www.significados.com.br/intervalo-de-confianca/
