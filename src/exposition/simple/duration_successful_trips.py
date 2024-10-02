import numpy as np
import pandas as pd
from lib.utils.utils import plot_bar_simple


#ARQUIVO: generalDroneData

# def _calculate(df):
#     df_grouped = (
#         df.groupby("Numero da execucao")
#         .agg(
#             {
#                 "tempo de viagem total dos drones no tempo estavel": ["sum", "count"],
#             }
#         )
#         .reset_index()
#     )

#     df_grouped = df_grouped[
#                     df_grouped[("tempo de viagem total dos drones no tempo estavel", "sum")] != 0
#                 ]
    
#     vetor_medias = df_grouped[("tempo de viagem total dos drones no tempo estavel", "sum")] / df_grouped[("tempo de viagem total dos drones no tempo estavel", "count")]

#     media = np.mean(vetor_medias)
#     desvio_padrao = np.std(vetor_medias)

#     n = df_grouped['Numero da execucao'].count()
#     intervalo = 1.96 * (desvio_padrao / np.sqrt(n))

#     return media, desvio_padrao, intervalo

# Função para calcular o intervalo de confiança
def confidence_interval(series):
    mean = series.mean()
    std = series.std()
    n = series.count()
    interval = 1.96 * (std / np.sqrt(n))
    return interval

def _calculate(df):
    # Limpa coluna lixo
    df = df.dropna(subset=["drone ID"])

    # Agrupa coluna por Numero de execução e agrega valos de media,
    # desvio padrão e intervalo de confiaça da coluna tempo de viagem total dos drones no tempo estavel
    df_grouped = (
        df.groupby("Numero da execucao")
        .agg(
            {
                "tempo de viagem total dos drones no tempo estavel": ["mean", "std", confidence_interval],
            }
        )
        .dropna()
        .reset_index()
    )

    media = df_grouped[("tempo de viagem total dos drones no tempo estavel", "mean")].values
    desvio_padrao = df_grouped[("tempo de viagem total dos drones no tempo estavel", "std")].values
    intervalo = df_grouped[("tempo de viagem total dos drones no tempo estavel", "confidence_interval")].values
    label = df_grouped["Numero da execucao"].values

    return media, desvio_padrao, intervalo, label

def duration_successful_trips(df):
    df.columns = df.columns.str.strip()

    media, _, intervalo, label = _calculate(df)

    list_media = np.array(media)
    list_intervalo = np.array(intervalo)
    label = np.array(label)

    
    return plot_bar_simple(
        labels=label,
        values=list_media,
        intervalos=list_intervalo,
        title="Duração de Viagens com Sucesso",
        x_label="Simulação",
        y_label="Time (s)",
    )

