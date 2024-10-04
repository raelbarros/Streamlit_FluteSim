import pandas as pd
import numpy as np
from src.utils.graph_plotly import plot_bar_group

# ARQUIVO: generalSimulationData

def calculate_collision_rate(df):
    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero de drones lancados no tempo estavel"].values

    taxa_colisoes = (num_colisoes / num_drones) * 100

    media = np.mean(taxa_colisoes)
    desvio_padrao = np.std(taxa_colisoes)

    n = len(df)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n))

    return media, desvio_padrao, intervalo


if __name__ == "__main__":
    # Adaptar os dfs de acordo com a quantidade de dados necessarios.
    # Adequar as labeis da chamada da função tbm.

    # Load Dados
    df_6 = pd.read_csv("data/generalSimulationData_6.csv")
    df_6.columns = df_6.columns.str.strip()

    df_12 = pd.read_csv("data/generalSimulationData_12.csv")
    df_12.columns = df_12.columns.str.strip()

    media__6, _, intervalo__6 = calculate_collision_rate(df_6)
    media__12, _, intervalo__12 = calculate_collision_rate(df_12)

    list_media = np.array([[media__6], [media__12]])
    list_intervalo = np.array([[intervalo__6], [intervalo__12]])
    
    legends = np.array(["teste1", "teste2"])
    labels = np.array(['6', '12'])

    plot_bar_group(
        labels=labels,
        values=list_media,
        intervalos=list_intervalo,
        legends=legends,
        title="Taxa de Colisão por Taxa de Chegada"
    )


# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
