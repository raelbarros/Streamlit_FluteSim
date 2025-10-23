import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import Iterable, List
import plotly.express as px

DEFAULT_ROOT = "/Volumes/SSD/Projects/Mestrado/RESULTS/Artigo Final"
DEFAULT_DRONE_CSV = f"{DEFAULT_ROOT}/12_multi_model_ml/droneCollisionData.csv"
DEFAULT_SIMULATION_CSV = f"{DEFAULT_ROOT}/12_multi_model_ml/generalSimulationData.csv"

MODEL_NAME_MAP = {
    "4": "SingleDrone",
    "6": "SpeedDrone",
    "a2c-relu-clip": "A2C (ReLU, Clip)",
    "a2c-relu-tanh": "A2C (ReLU, Tanh)",
    "a2c-swish-clip": "A2C (Swish, Clip)",
    "a2c-swish-tanh": "A2C (Swish, Tanh)",
    "ppo-relu-clip": "PPO (ReLU, Clip)",
    "ppo-relu-tanh": "PPO (ReLU, Tanh)",
    "ppo-swish-clip_(v2_04)": "PPO (Swish, Clip)",
    "ppo-swish-tanh": "PPO (Swish, Tanh)",
}


@dataclass(frozen=True)
class DatasetConfig:
    x_value: str
    drone_csv: str
    simulation_csv: str


def _rename_models(percent_series: pd.Series) -> pd.Series:
    """
    Renomeia os modelos de drones para labels mais amigáveis.
    """
    mapped_index = percent_series.index.map(lambda name: MODEL_NAME_MAP.get(name, name))
    renamed = percent_series.groupby(mapped_index).sum()
    return renamed.sort_values(ascending=False)


def load_collision_summary(drone_csv: str, simulation_csv: str):
    df_drone = pd.read_csv(drone_csv)
    percent_drone = df_drone["modelo"].value_counts(normalize=True) * 100
    percent_drone = _rename_models(percent_drone)

    df_simulation = pd.read_csv(simulation_csv)
    df_simulation.columns = [col.strip() for col in df_simulation.columns]

    num_colisoes = df_simulation["numero total de drones colidentes"].values
    num_drones = df_simulation["numero total de drones lancados"].values

    taxa_colisao = (num_colisoes / num_drones) * 100

    media = np.mean(taxa_colisao)
    desvio_padrao = np.std(taxa_colisao)
    n = len(taxa_colisao)
    intervalo = 1.96 * (desvio_padrao / np.sqrt(n)) if n > 0 else 0

    return media, intervalo, percent_drone


def build_stacked_bar(configs: Iterable[DatasetConfig] = None):

    configs = list(configs)
    if not configs:
        raise ValueError("É necessario fornecer pelo menos um DatasetConfig.")

    summaries = []
    modelo_totais = {}

    for cfg in configs:
        media, intervalo, percent_drone = load_collision_summary(cfg.drone_csv, cfg.simulation_csv)
        stack_values = (percent_drone / 100.0) * media

        summaries.append(
            {
                "x": cfg.x_value,
                "media": media,
                "intervalo": intervalo,
                "percent": percent_drone,
                "stack": stack_values,
            }
        )

        for modelo, percent in percent_drone.items():
            modelo_totais[modelo] = modelo_totais.get(modelo, 0) + percent

    modelos_ordenados: List[str] = sorted(modelo_totais, key=modelo_totais.get, reverse=True)
    categorias = [summary["x"] for summary in summaries]

    fig = go.Figure()

    for modelo in modelos_ordenados:
        y_values = [summary["stack"].get(modelo, 0.0) for summary in summaries]
        porcentagens = [summary["percent"].get(modelo, 0.0) for summary in summaries]
        textos = [f"{p:.1f}%" if p > 1e-6 else "" for p in porcentagens]
        customdata = [[p, modelo] for p in porcentagens]

        fig.add_trace(
            go.Bar(
                x=categorias,
                y=y_values,
                name=modelo,
                # text=textos,
                # textposition="inside",
                # customdata=customdata,
                # hovertemplate=(
                #     "Modelo: %{customdata[1]}"
                #     "<br>Arrival rate: %{x}"
                #     "<br>Percentual: %{customdata[0]:.1f}%"
                #     "<br>Contribuição: %{y:.2f}%"
                #     "<extra></extra>"
                # ),
            )
        )

    ymax = max(summary["media"] + summary["intervalo"] for summary in summaries)
    ymax = ymax * 1.1 if ymax > 0 else 1

    fig.update_layout(
        colorway=px.colors.qualitative.D3,
        template='plotly_white',
        barmode="stack",
        legend=dict(
        title="",
        font=dict(
                size=30  # Define o tamanho do texto da legenda
            ),
            x=0.02,  # Posiçao horizontal dentro do gráfico (0 é a esquerda, 1 é a direita)
            y=0.95,  # Posiçao vertical dentro do gráfico (0 é na base, 1 é no topo)
            xanchor='left',  # Alinha a legenda em relaçao ao ponto definido por x
            yanchor='top',   # Alinha a legenda em relaçao ao ponto definido por y
            bgcolor='rgba(255, 255, 255, 0.7)',  # Fundo da legenda com transparência
            bordercolor='black',  # Cor da borda da legenda
            borderwidth=1         # Largura da borda da legenda
        ),
        yaxis=dict(
                title="Collision rate (%)",
                title_font=dict(size=30),
                tickfont=dict(size=30),
                automargin=True
            ),
        xaxis=dict(
                title="Arrival rate (drones/min)",
                title_font=dict(size=30),
                tickfont=dict(size=30),
                automargin=True
            ),
        title=dict(
                x=0.5,                
                xanchor='center',     
                font=dict(size=40)    
            )
        
    )

    return fig


if __name__ == "__main__":
    example_configs = [
        DatasetConfig(
            x_value="ML",
            drone_csv=DEFAULT_DRONE_CSV,
            simulation_csv=DEFAULT_SIMULATION_CSV,
        ),
        DatasetConfig(
            x_value="ML + Geo",
            drone_csv=f"{DEFAULT_ROOT}/12_multi_model_ml_geo/droneCollisionData.csv",
            simulation_csv=f"{DEFAULT_ROOT}/12_multi_model_ml_geo/generalSimulationData.csv",
        ),
    ]

    figure = build_stacked_bar(example_configs)
    figure.show()
