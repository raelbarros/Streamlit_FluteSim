import numpy as np

# ARQUIVO: generalSimulationData

def collision_rate_per_execution(df):
    df.columns = df.columns.str.strip()

    df = df.sort_values(by="Numero da execucao")

    df["taxa_colisao"] = (
        (df["numero total de drones colidentes"] / df["numero de drones lancados no tempo estavel"]) * 100
    )
    
    taxa = np.array(df["taxa_colisao"].values)
    label = np.array(df["Numero da execucao"].values)

    return {"taxa": taxa, "label": label}

# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
# https://www.significados.com.br/intervalo-de-confianca/
