import pandas as pd
import plotly.express as px
import glob
import os

# =========================
# CAMINHO DOS DADOS
# -------------------------
path = "src/visualization/auxiliar/data/rewards/*.csv"

csv_files = glob.glob(path)

dfs = []

colors = [
    # Grupo 1 (tons frios)
    "#1f77b4",  # azul forte
    "#2ca02c",  # verde médio
    "#17becf",  # ciano
    "#9edae5",  # azul claro

    # Grupo 2 (tons quentes)
    "#d62728",  # vermelho
    "#ff7f0e",  # laranja
    "#ffbb78",  # laranja claro
    "#e377c2"   # rosa
]



for file in csv_files:
    df = pd.read_csv(file)
    df["source"] = os.path.basename(file).replace(".csv", "")
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)
ordered_sources = sorted(df_all["source"].unique())

fig = px.line(
    df_all,
    x="Step",
    y="Value",
    color="source",
    category_orders={"source": ordered_sources},
    color_discrete_sequence=colors,
)
fig.update_layout(
    xaxis_title="Episodes",
    yaxis_title="Rewards",
    template="plotly_white",
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
        title_font=dict(size=30),
        tickfont=dict(size=30),
        automargin=True
    ),
    xaxis=dict(
        title_font=dict(size=30),
        tickfont=dict(size=30),
        automargin=True
    ),
)

fig.show()
