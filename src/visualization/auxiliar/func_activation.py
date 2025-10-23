import numpy as np
import matplotlib.pyplot as plt

# Intervalo do eixo x
x = np.linspace(-3, 3, 400)

# Funções de ativação
relu = np.maximum(0, x)
swish = x / (1 + np.exp(-x))
tanh = np.tanh(x)
linear_clip = np.clip(x, -1, 1)

# Criação da figura com 2 subplots lado a lado
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ======== Gráfico 1: ReLU e Swish ========
axes[0].plot(x, relu, label='ReLU', linewidth=2)
axes[0].plot(x, swish, label='Swish', linewidth=2)
axes[0].axhline(0, color='black', linewidth=1)
axes[0].axvline(0, color='black', linewidth=1)
# axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].set_title('ReLU e Swish', fontsize=13)
# axes[0].set_xlabel('x', fontsize=11)
# axes[0].set_ylabel('f(x)', fontsize=11)
axes[0].legend()

# ======== Gráfico 2: Tanh e Linear Clipped ========
axes[1].plot(x, tanh, label='Tanh', linewidth=2)
axes[1].plot(x, linear_clip, label='Linear ([-1,1])', linewidth=2)
axes[1].axhline(0, color='black', linewidth=1)
axes[1].axvline(0, color='black', linewidth=1)
# axes[1].grid(True, linestyle='--', alpha=0.6)
axes[1].set_title('Tanh e Linear', fontsize=13)
# axes[1].set_xlabel('x', fontsize=11)
# axes[1].set_ylabel('f(x)', fontsize=11)
axes[1].legend()

# Ajuste de layout
plt.tight_layout()
plt.show()
