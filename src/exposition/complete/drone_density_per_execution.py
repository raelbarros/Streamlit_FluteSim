import numpy as np

# ARQUIVO: generalSimulationData

def drone_density_per_execution(df):
    df.columns = df.columns.str.strip()

    df = df.sort_values(by="Numero da execucao")

    num_drones = np.array(df["numero total de drones lancados"].values)
    label = np.array(df["Numero da execucao"].values)
    
    return {"num_drones": num_drones, "label": label}


# https://www.lampada.uerj.br/arquivosdb/_book/intervaloconfianca.html
# https://www.significados.com.br/intervalo-de-confianca/
