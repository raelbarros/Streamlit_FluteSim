from utils.graph_plotly import plot_bar_simple
import numpy as np


# ARQUIVO: droneCollisionData


# fmt: off
# Definicao do mapeamento de situacoes usando dicionário
MAPPING_SITUATIONS = {
    (5, 0): 0, (0, 5): 0, # 5 com 0 ou 0 com 5 (pouso com decolagem ou decolagem com pouso) - Posicao 1 (índice 0)
    (1, 1): 1, # 1 com 1 (ida com ida) - Posicao 2 (índice 1)
    (4, 4): 2, # 4 com 4 (volta com volta) - Posicao 3 (índice 2)
    (4, 0): 3, (0, 4): 3, # 4 com 0 ou 0 com 4 (volta com decolagem ou decolagem com volta) - Posicao 4 (índice 3)
    (4, 3): 4, (3, 4): 4, # 4 com 3 ou 3 com 4 (volta com decolagem da entrega ou decolagem da entrega com volta) - Posicao 5 (índice 4)
    (3, 1): 5, (1, 3): 5, # 3 com 1 ou 1 com 3 (decolagem da entrega com ida ou ida com decolagem da entrega) - Posicao 6 (índice 5)
    (1, 2): 6, (2, 1): 6, # 1 com 2 ou 2 com 1 (ida com pouso da entrega ou pouso da entrega com ida) - Posicao 7 (índice 6)
    (0, 0): 7, # 0 com 0 (decolagem com decolagem) - Posicao 8 (índice 7)
    (5, 1): 8, (1, 5): 8, # 5 com 1 ou 1 com 5 (pouso com ida ou ida com pouso) - Posicao 9 (índice 8)
    (2, 5): 9, (5, 2): 9, # 2 com 5 ou 5 com 2 (pouso da entrega com pouso ou pouso com pouso da entrega) - Posicao 10 (índice 9)
    (3, 0): 10, (0, 3): 10, # 3 com 0 ou 0 com 3 (decolagem da entrega com decolagem ou decolagem com decolagem da entrega) - Posicao 11 (índice 10)
    (5, 4): 11, (4, 5): 11, # 5 com 4 ou 4 com 5 (pouso com volta ou volta com pouso) - Posicao 12 (índice 11)
    (5, 5): 12, # 5 com 5 (pouso com pouso) - Posicao 13 (índice 12)
    (2, 2): 13, # 2 com 2 (pouso da entrega com pouso da entrega) - Posicao 14 (índice 13)
    (0, 1): 14, (1, 0): 14, # 0 com 1 ou 1 com 0 (decolagem com ida ou ida com decolagem) - Posicao 15 (índice 14)
    (0, 2): 15, (2, 0): 15, # 0 com 2 ou 2 com 0 (decolagem com pouso da entrega ou pouso da entrega com decolagem) - Posicao 16 (índice 15)
    (2, 3): 16, (3, 2): 16, # 2 com 3 ou 3 com 2 (pouso da entrega com decolagem da entrega ou decolagem da entrega com pouso da entrega) - Posicao 17 (índice 16)
    (2, 4): 17, (4, 2): 17, # 2 com 4 ou 4 com 2 (pouso da entrega com volta ou volta com pouso da entrega) - Posicao 18 (índice 17)
    (3, 3): 18, # 3 com 3 (decolagem da entrega com decolagem da entrega) - Posicao 19 (índice 18)
    (3, 5): 19, (5, 3): 19, # 3 com 5 ou 5 com 3 (decolagem da entrega com pouso ou pouso com decolagem da entrega) - Posicao 20 (índice 19)
    (4, 1): 20, (1, 4): 20 # 4 com 1 ou 1 com 4 (volta com ida ou ida com volta) - Posicao 21 (índice 20)
}
# fmt: on


# Definicao das categorias e os índices correspondentes
CATEGORIAS = {
    "Takeoff": [3, 4, 5, 14],
    "Landing": [6, 8, 11, 17],
    "Landing and take-off": [0, 7, 9, 10, 12, 13, 15, 16, 18, 19],
    "Cruise": [20, 1, 2],
}


def _map_situation(etapa1, etapa2):
    """
    Mapeia pares de etapas de viagem para uma situacao de colisao específica.

    Args:
        etapa1 (int): Etapa da viagem do primeiro drone.
        etapa2 (int): Etapa da viagem do segundo drone.

    Returns:
        int: Índice da situacao de colisao (0 a 19). Retorna np.nan se nao corresponder a nenhuma situacao.
    """
    return MAPPING_SITUATIONS.get((etapa1, etapa2), np.nan)


def _summarize_situation(
    media_situacoes, desvio_padrao_situacoes, intervalo_confianca_situacoes
):
    """
    Agrupa as situacoes de colisao em categorias maiores.

    Args:
        media_situacoes (np.array): Medias das situacoes de colisao.
        desvio_padrao_situacoes (np.array): Desvios padrao das situacoes de colisao.
        intervalo_confianca_situacoes (np.array): Intervalos de confianca das situacoes de colisao.

    Returns:
        tuple: Medias, desvios padrao e intervalos de confianca das categorias sintetizadas.
    """
    media_categorias = []
    desvio_padrao_categorias = []
    intervalo_confianca_categorias = []

    for _, indices in CATEGORIAS.items():
        media = np.nansum(media_situacoes[indices])
        desvio_padrao = np.nansum(desvio_padrao_situacoes[indices])
        intervalo_confianca = np.nansum(intervalo_confianca_situacoes[indices])

        media_categorias.append(media)
        desvio_padrao_categorias.append(desvio_padrao)
        intervalo_confianca_categorias.append(intervalo_confianca)

    return (
        np.array(media_categorias),
        np.array(desvio_padrao_categorias),
        np.array(intervalo_confianca_categorias),
    )


def collisions_per_situation(df):

    df.columns = df.columns.str.strip()

    # Aplicar a funcao de mapeamento para cada linha
    df["situacao"] = df.apply(
        lambda row: _map_situation(
            row["etapa da viagem dos pares que colidiram1"],
            row["etapa da viagem dos pares que colidiram2"],
        ),
        axis=1,
    )

    # Agrupar por execucao e situacao, contando ocorrencias
    df_grouped = (
        df.groupby(["Numero da execucao", "situacao"]).size().unstack(fill_value=0)
    )

    # Preencher colunas ausentes com zero (caso algumas situacoes nao ocorram em certas execucoes)
    df_grouped = df_grouped.reindex(columns=range(21), fill_value=0)

    # Calcular medias e desvios padrao por situacao
    vetor_medias = df_grouped.mean(axis=0).values  # Media por situacao
    vetor_desvio_padrao = df_grouped.std(axis=0).values  # Desvio padrao por situacao
    num_execucoes = df_grouped.shape[0]

    # Calcular intervalos de confianca (95%)
    intervalo_confianca = 1.96 * vetor_desvio_padrao / np.sqrt(num_execucoes)

    # Sintetizar situacoes em categorias maiores
    media_categorias, _, intervalo_confianca_categorias = (
        _summarize_situation(vetor_medias, vetor_desvio_padrao, intervalo_confianca)
    )

    labels = np.array(list(CATEGORIAS.keys()))
    return plot_bar_simple(
        labels=labels,
        values=media_categorias,
        intervalos=intervalo_confianca_categorias,
        title="Número Medio de Colisões por Situação",
        x_label="Situação",
        y_label="Número de Colisões",
    )
