import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

arquivos = {
    "PPO (Swish, Clip)": "src/visualization/auxiliar/data/trajectory/Log_Path_drone 0_5.csv",
    "A2C (Swish, Clip)": "src/visualization/auxiliar/data/trajectory/Log_Path_drone 0_7.csv",
    "SingleDrone": "src/visualization/auxiliar/data/trajectory/Log_Path_drone 1_7.csv",
    "SpeedDrone": "src/visualization/auxiliar/data/trajectory/Log_Path_drone 0_4.csv",

}
cores = {
    "A2C (Swish, Clip)": "#9467bd",
    "PPO (Swish, Clip)": "#2CA02C",
    "SingleDrone": "#D62728",
    "SpeedDrone": "#1F77B4",
}

dados = {}

# -----------------------
# DETECÇÃO DA "IDA"
# -----------------------
# Não existe coluna explícita marcando ida/volta, então detectamos o pouso:
# o drone decola (y ultrapassa Y_DECOLAGEM), voa, e ao chegar no destino
# desce perto do chão (y abaixo de Y_POUSO) pela primeira vez após decolar.
# Cortamos a trajetória nesse ponto, descartando a volta.
Y_DECOLAGEM = 5.0
Y_POUSO = 3.0


def apenas_ida(df, y_decolagem=Y_DECOLAGEM, y_pouso=Y_POUSO):
    decolou = False
    for i, y in enumerate(df["y"].values):
        if not decolou and y > y_decolagem:
            decolou = True
        elif decolou and y < y_pouso:
            return df.iloc[: i + 1].reset_index(drop=True)
    return df  # não detectou pouso: mantém tudo


# -----------------------
# LEITURA COM PANDAS
# -----------------------
for nome, caminho in arquivos.items():
    try:
        df = pd.read_csv(caminho)
    except FileNotFoundError:
        print(f"[aviso] arquivo não encontrado, pulando: {caminho}")
        continue

    # garantir ordenação temporal (essencial para trajetória correta)
    if "time" in df.columns:
        df = df.sort_values(by="time")

    df = apenas_ida(df)

    dados[nome] = df

# -----------------------
# FIGURA
# -----------------------
fig = plt.figure(figsize=(14, 6))

# =======================
# 3D
# =======================
ax3d = fig.add_subplot(1, 2, 1, projection="3d")

for nome, df in dados.items():
    cor = cores.get(nome, "black")

    xs = df["x"].values
    ys = df["y"].values
    zs = df["z"].values

    ax3d.plot(xs, ys, zs, label=nome, color=cor, linewidth=1.5)

    if len(df) > 0:
        ax3d.scatter(xs[0], ys[0], zs[0], color=cor, marker="o", s=60, edgecolors="black")


ax3d.set_xlabel("X (m)")
ax3d.set_ylabel("Y (m)")
ax3d.set_zlabel("Z (m)")
ax3d.set_title("3D Flight Path", y=-0.18)
ax3d.legend()

# =======================
# 2D (vista superior)
# =======================
ax2d = fig.add_subplot(1, 2, 2)

for nome, df in dados.items():
    cor = cores.get(nome, "black")

    xs = df["x"].values
    ys = df["y"].values

    ax2d.plot(xs, ys, label=nome, color=cor, linewidth=1.5)

    if len(df) > 0:
        ax2d.scatter(xs[0], ys[0], color=cor, marker="o", s=60, edgecolors="black", zorder=3)

ax2d.set_xlabel("X (m)")
ax2d.set_ylabel("Y (m)")
ax2d.set_title("Altitude Profile (X-Y Plane)", y=-0.18)
ax2d.legend()
ax2d.grid(True, alpha=0.3)
ax2d.set_aspect("auto")

plt.tight_layout()
plt.savefig("trajetorias_drones.png", dpi=150, bbox_inches="tight")
plt.show()

print("Gráfico salvo em trajetorias_drones.png")