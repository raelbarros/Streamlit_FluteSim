import numpy as np
from utils.graph_plotly import plot_bar_simple

# ARQUIVO: generalSimulationData

def _calculate(df):
    num_colisoes = df["numero total de drones colidentes"].values
    num_drones = df["numero de drones lancados no tempo estavel"].values

    taxa_colisoes = (num_colisoes / num_drones) * 100

    media = np.mean(taxa_colisoes)
    desvio_padrao = np.std(taxa_colisoes)

    n = len(taxa_colisoes)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n))

    return media, desvio_padrao, intervalo


def collision_rate_geral(df):
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    media, _, intervalo = _calculate(df)


    return plot_bar_simple(
        values=np.array(media),
        intervalos=np.array(intervalo),
        title="Taxa de Colisão Geral",
        x_label="Simulação",
        y_label="Collision rate (%)",
    )


# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
# https://www.significados.com.br/intervalo-de-confianca/
