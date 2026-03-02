import numpy as np
import matplotlib.pyplot as plt

# Aumentar tamanho global da fonte
plt.rcParams.update({
    'font.size': 15,       # tamanho do texto geral
    'axes.titlesize': 15,  # tamanho do título
    'axes.labelsize': 15,  # tamanho dos rótulos dos eixos
    'legend.fontsize': 15, # tamanho da legenda
    'xtick.labelsize': 15,
    'ytick.labelsize': 15
})

# Dados de entrada
x = np.linspace(-5, 5, 200)

# ---- Figura 1: ReLU vs Swish ----
relu = np.maximum(0, x)
swish = x / (1 + np.exp(-x))

plt.figure(figsize=(6, 4))
plt.plot(x, relu, label="ReLU", linewidth=2)
plt.plot(x, swish, label="Swish", linewidth=2, color='orange')
plt.legend()
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.title("Funções de Ativação: ReLU e Swish")
plt.xlabel('x', fontsize=15)
plt.ylabel('y', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()

# ---- Figura 2: tanh vs clip ----
tanh = np.tanh(x)
clip = np.clip(x / 2, -1, 1)

plt.figure(figsize=(6, 4))
plt.plot(x, tanh, label="Tanh", linewidth=2)
plt.plot(x, clip, label="Clip [-1, 1]", linewidth=2, color='orange')
plt.legend()
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.title("Funções de Ativação: tanh e clip")
plt.xlabel("x", fontsize=15)
plt.ylabel("y", fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()
