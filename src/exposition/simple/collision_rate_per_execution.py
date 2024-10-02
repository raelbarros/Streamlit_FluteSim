import pandas as pd
import numpy as np
from lib.utils.utils import plot_bar_simple

# ARQUIVO: generalSimulationData

# def _calculate(df):
#     num_colisoes = df["numero total de drones colidentes"].values
#     num_drones = df["numero de drones lancados no tempo estavel"].values

#     taxa_colisoes = (num_colisoes / num_drones) * 100

#     media = np.mean(taxa_colisoes)
#     desvio_padrao = np.std(taxa_colisoes)

#     n = len(taxa_colisoes)
#     intervalo = 1.96 * (desvio_padrao / np.sqrt(n))

#     return media, desvio_padrao, intervalo


def collision_rate_per_execution(df):
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    df["taxa_colisao"] = (
        (df["numero total de drones colidentes"] / df["numero de drones lancados no tempo estavel"]) * 100
    )
    
    taxa = np.array(df["taxa_colisao"].values)
    label = np.array(df["Numero da execucao"].values)

    n = len(df["Numero da execucao"])
    list_intervalo = np.zeros(n)


    return plot_bar_simple(
        labels=label,
        values=taxa,
        intervalos=list_intervalo,
        title="Taxa de Colisão por Execução",
        x_label="Simulação",
        y_label="Collision rate (%)",
    )


# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
# https://www.significados.com.br/intervalo-de-confianca/
