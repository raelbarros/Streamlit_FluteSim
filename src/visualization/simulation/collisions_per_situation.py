from src.utils.graph_plotly import plot_bar
import numpy as np


# ARQUIVO: droneCollisionData


# fmt: off
# Definicao do mapeamento de situacoes usando dicionario
MAPPING_SITUATIONS = {
    (5, 0): 0, (0, 5): 0, # 5 com 0 ou 0 com 5 (pouso com decolagem ou decolagem com pouso) - Posicao 1 (indice 0)
    (1, 1): 1, # 1 com 1 (ida com ida) - Posicao 2 (indice 1)
    (4, 4): 2, # 4 com 4 (volta com volta) - Posicao 3 (indice 2)
    (4, 0): 3, (0, 4): 3, # 4 com 0 ou 0 com 4 (volta com decolagem ou decolagem com volta) - Posicao 4 (indice 3)
    (4, 3): 4, (3, 4): 4, # 4 com 3 ou 3 com 4 (volta com decolagem da entrega ou decolagem da entrega com volta) - Posicao 5 (indice 4)
    (3, 1): 5, (1, 3): 5, # 3 com 1 ou 1 com 3 (decolagem da entrega com ida ou ida com decolagem da entrega) - Posicao 6 (indice 5)
    (1, 2): 6, (2, 1): 6, # 1 com 2 ou 2 com 1 (ida com pouso da entrega ou pouso da entrega com ida) - Posicao 7 (indice 6)
    (0, 0): 7, # 0 com 0 (decolagem com decolagem) - Posicao 8 (indice 7)
    (5, 1): 8, (1, 5): 8, # 5 com 1 ou 1 com 5 (pouso com ida ou ida com pouso) - Posicao 9 (indice 8)
    (2, 5): 9, (5, 2): 9, # 2 com 5 ou 5 com 2 (pouso da entrega com pouso ou pouso com pouso da entrega) - Posicao 10 (indice 9)
    (3, 0): 10, (0, 3): 10, # 3 com 0 ou 0 com 3 (decolagem da entrega com decolagem ou decolagem com decolagem da entrega) - Posicao 11 (indice 10)
    (5, 4): 11, (4, 5): 11, # 5 com 4 ou 4 com 5 (pouso com volta ou volta com pouso) - Posicao 12 (indice 11)
    (5, 5): 12, # 5 com 5 (pouso com pouso) - Posicao 13 (indice 12)
    (2, 2): 13, # 2 com 2 (pouso da entrega com pouso da entrega) - Posicao 14 (indice 13)
    (0, 1): 14, (1, 0): 14, # 0 com 1 ou 1 com 0 (decolagem com ida ou ida com decolagem) - Posicao 15 (indice 14)
    (0, 2): 15, (2, 0): 15, # 0 com 2 ou 2 com 0 (decolagem com pouso da entrega ou pouso da entrega com decolagem) - Posicao 16 (indice 15)
    (2, 3): 16, (3, 2): 16, # 2 com 3 ou 3 com 2 (pouso da entrega com decolagem da entrega ou decolagem da entrega com pouso da entrega) - Posicao 17 (indice 16)
    (2, 4): 17, (4, 2): 17, # 2 com 4 ou 4 com 2 (pouso da entrega com volta ou volta com pouso da entrega) - Posicao 18 (indice 17)
    (3, 3): 18, # 3 com 3 (decolagem da entrega com decolagem da entrega) - Posicao 19 (indice 18)
    (3, 5): 19, (5, 3): 19, # 3 com 5 ou 5 com 3 (decolagem da entrega com pouso ou pouso com decolagem da entrega) - Posicao 20 (indice 19)
    (4, 1): 20, (1, 4): 20 # 4 com 1 ou 1 com 4 (volta com ida ou ida com volta) - Posicao 21 (indice 20)
}
# fmt: on


# Definicao das categorias e os indices correspondentes
CATEGORIAS = {
    "Takeoff": [3, 4, 5, 14],
    "Landing": [6, 8, 11, 17],
    "Landing and take-off": [0, 7, 9, 10, 12, 13, 15, 16, 18, 19],
    "Cruise": [20, 1, 2],
}


def calculate_collisions_per_situation(df):
    """
    Calcula o numero medio de colisoes por situaçao e por categoria.

    Args:
        df (DataFrame): DataFrame contendo os dados de colisoes.

    Returns:
        dict: Dicionario contendo medias, intervalos de confiança e labels das categorias.
    """
    df.columns = df.columns.str.strip()

    # Aplicar a funçao de mapeamento para cada linha
    df["situacao"] = df.apply(
        lambda row: MAPPING_SITUATIONS.get(
            (row["etapa da viagem dos pares que colidiram1"], row["etapa da viagem dos pares que colidiram2"]),
            np.nan
        ),
        axis=1,
    )

    # Remover linhas com situaçao NaN
    df = df.dropna(subset=["situacao"])

    # Agrupar por execuçao e situaçao, contando ocorrencias
    df_grouped = df.groupby(["Numero da execucao", "situacao"]).size().unstack(fill_value=0)

    # Preencher colunas ausentes com zero
    df_grouped = df_grouped.reindex(columns=range(21), fill_value=0)

    # Calcular medias e desvios padrao por situaçao
    vetor_medias = df_grouped.mean(axis=0).values  # Media por situaçao
    vetor_desvio_padrao = df_grouped.std(axis=0).values  # Desvio padrao por situaçao
    num_execucoes = df_grouped.shape[0]

    # Calcular intervalos de confiança (95%)
    intervalo_confianca = 1.96 * vetor_desvio_padrao / np.sqrt(num_execucoes)

    # Agrupar situaçoes em categorias maiores
    media_categorias = []
    intervalo_confianca_categorias = []
    categorias = []

    for categoria, indices in CATEGORIAS.items():
        media = np.nansum(vetor_medias[indices])
        intervalo = np.nansum(intervalo_confianca[indices])

        media_categorias.append(media)
        intervalo_confianca_categorias.append(intervalo)
        categorias.append(categoria)

    return {
        "media_categorias": np.array(media_categorias),
        "intervalo_confianca_categorias": np.array(intervalo_confianca_categorias),
        "categorias": categorias
    }



def plot_collisions_per_situation(data_list, labels=None):
    """
    Gera o grafico do numero medio de colisoes por situaçao.

    Args:
        data_list (list): Lista de dicionarios retornados por calculate_collisions_per_situation.
        simulation_names (list, optional): Lista de nomes das simulaçoes correspondentes aos dados em data_list.

    Returns:
        Figure: Objeto de figura Plotly.
    """
    if not isinstance(data_list, list):
        data_list = [data_list]
    
    if labels is None:
        labels = [f"Simulaçao {i+1}" for i in range(len(data_list))]

    categorias = data_list[0]['categorias'] 

    values_list = [data['media_categorias'] for data in data_list]
    intervalos_list = [data['intervalo_confianca_categorias'] for data in data_list]

    # Chama a funçao plot_bar modificada para suportar multiplas series
    fig = plot_bar(
        values=values_list,
        intervalos=intervalos_list,
        labels=categorias,
        x_label="",
        y_label="Number of collisions",
        title="Numero of collisions per situation"
    )

    # Atualizar os nomes das simulaçao
    for i, sim_name in enumerate(labels):
        fig.data[i].name = sim_name

    return fig
