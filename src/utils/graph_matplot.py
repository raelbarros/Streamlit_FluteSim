import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configurando o estilo do grafico
sns.set_theme(style="whitegrid")
sns.set_palette("colorblind")
sns.set_context("paper")


def plot_boxsplot(title, labels, *args):
    fig = plt.figure(figsize=(5, 8))
    sns.boxplot(data=[x for x in args])

    plt.title(title, fontsize=14)
    plt.xticks([0, 1], labels=labels, fontsize=12)

    # Escala do eixo Y
    plt.yticks(fontsize=12)
    plt.grid()

    # Definindo o limite do eixo Y
    # plt.ylim(-10, 200)
    return fig


def plot_histogram(df, x_label, y_label, title):
    # Criando o grafico de distribuição
    fig = plt.figure(figsize=(8, 6))
    sns.histplot(df, kde=True, bins=20, alpha=0.6)

    plt.title(title, fontsize=14)
    plt.ylabel(y_label)
    plt.xlabel(x_label, fontsize=12)
    plt.grid(True)
    
    return fig


def plot_bar_group(**kwargs):
    labels = kwargs.get("labels")
    values = kwargs.get("values")
    intervalos = kwargs.get("intervalos")
    legends = kwargs.get("legends")

    # Verifica tipo das variaveis de input
    if not isinstance(labels, np.ndarray):
        raise ValueError("A variavel `label` deve ser do tipo np.array")
    elif not isinstance(values, np.ndarray):
        raise ValueError("A variavel `values` deve ser do tipo np.array")
    elif not isinstance(intervalos, np.ndarray):
        raise ValueError("A variavel `intervalos` deve ser do tipo np.array")
    elif not isinstance(legends, np.ndarray):
        raise ValueError("A variavel `legend` deve ser do tipo np.array")

    # parametros default
    x_label = kwargs.get("x_label", "Eixo X")
    y_label = kwargs.get("y_label", "Eixo Y")
    title = kwargs.get("title", "Grafico de Barras")
    show_num = kwargs.get("show_num", False)

    figsize = (10, 6)
    width =  0.6
    fontsize = 12

    # Criando o grafico
    fig, ax = plt.subplots(figsize=figsize)

    # Calculando as posiçoes das barras no eixo X
    x = np.arange(len(labels))

    # Plotando as barras para cada subcategoria
    for i, (subcategory, val, err) in enumerate(zip(legends, values, intervalos)):
        ax.bar(x + i * width, val, width, yerr=err, capsize=10, alpha=0.7, label=subcategory)

    # Adicionar rótulos e legendas
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(y_label, fontsize=fontsize)
    ax.set_xlabel(x_label, fontsize=fontsize)
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, (values + intervalos).max() * 1.2)
    ax.legend(title="Legenda")

    # Adicionando valores dentro das barras
    if show_num:
        for i, val in enumerate(values):
            for j, media in enumerate(val):
                bar_x = x[j] + i * width
                ax.annotate(
                    f"{media:.2f}",
                    xy=(bar_x + width / 2 - width / 2, media),
                    xytext=(0, 3),  # 3 pontos acima da barra
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )
    
    # Exibindo o grafico
    plt.tight_layout()
    
    return fig

def plot_bar(**kwargs):
    """ Esta funcao cria um grafico de barras simples. 
        Os parâmetros opcionais permitem personalizar o grafico.

    Args Obrigatorios:
        values (np.ndarray): Array com os valores das barras.
        intervalos (np.ndarray): Array com os intervaloss de confiança para cada barra.

    Args Opcionais:
        labels (np.ndarray): Array com os rotulos das barras.
        x_label (str, opcional): Legenda do eixo X. Padrão e ''.
        y_label (str, opcional): Legenda do eixo Y. Padrão e ''.
        title (str, opcional): Titulo do grafico. Padrão e ''.
        show_num (bool, opcional): Se True, exibe os valores acima das barras. Padrão e False.

    Raises:
        ValueError: Se os valores de `label`, `values` e `intervalos` nao forem np.array

    Return:
        None: A funcao nao retorna nenhum valor, mas exibe o grafico gerado.
    
    Notas:
        - Certifique-se de que `labels`, `values` e `intervalos` sejam arrays NumPy de mesmo comprimento.
        - Se `show_num` for True, os valores das barras serão exibidos acima de cada uma delas.
    """

    # Parametros Obrigatorios
    values = kwargs.get("values")
    intervalos = kwargs.get("intervalos")

    # Verifica tipo das variaveis de input
    if not isinstance(values, np.ndarray):
        raise ValueError("A variavel `values` deve ser do tipo np.array")
    elif not isinstance(intervalos, np.ndarray):
        raise ValueError("A variavel `intervalos` deve ser do tipo np.array")

    # parametros default
    labels = kwargs.get("labels", np.array(['']))
    x_label = kwargs.get("x_label", "Eixo X")
    y_label = kwargs.get("y_label", "Eixo Y")
    title = kwargs.get("title", "Grafico de Barras")
    show_num = kwargs.get("show_num", False)

    figsize = (10, 6)
    width =  0.6
    fontsize = 12

    # Criando o grafico
    fig, ax = plt.subplots(figsize=figsize)

    # Plotar barras
    bars = ax.bar(labels, values, width, yerr=intervalos, capsize=10, alpha=0.7)

    # Add rotulos
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(y_label, fontsize=fontsize)
    ax.set_xlabel(x_label, fontsize=fontsize)
    ax.set_ylim(0, (values + intervalos).max() * 1.2)
    ax.set_xticks(range(len(labels))) 
    ax.set_xticklabels(labels, fontsize=fontsize)


    # Adicionando valores dentro das barras
    if show_num:
        for bar, media in zip(bars, values):
            height = bar.get_height()
            ax.annotate(
                f"{media:.2f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 pontos acima da barra
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
            )

    # Exibindo o grafico
    plt.tight_layout()
    
    return fig



# import plotly.graph_objects as go
# import numpy as np

# import plotly.io as pio


# pio.templates.default = 'presentation'


# def plot_boxsplot(title, labels, *args):
#     """
#     Cria um boxplot usando plotly.

#     Args:
#         title (str): Titulo do grafico.
#         labels (list): Lista de rótulos para cada conjunto de dados.
#         *args: Conjuntos de dados para plotar.

#     Retorna:
#         fig (go.Figure): Figura plotly com o boxplot.
#     """
#     fig = go.Figure()

#     for i, x in enumerate(args):
#         fig.add_trace(go.Box(y=x, name=labels[i]))

#     fig.update_layout(
#         title=title,
#         xaxis_title='',
#         yaxis_title='',
#         yaxis_tickfont_size=12,
#         xaxis_tickfont_size=12,
#         xaxis_tickvals=labels,
#         showlegend=False
#     )

#     return fig

# import numpy as np
# import plotly.graph_objects as go
# from scipy.stats import gaussian_kde
# import numpy as np
# import plotly.graph_objects as go
# from scipy.stats import gaussian_kde

# def plot_histogram(df, x_label, y_label, title):
#     """
#     Cria um histograma com contagens e sobrepoe a curva KDE escalada para as contagens.
#     """
#     # Converter e limpar os dados
#     data = np.asarray(df)
#     data = data[np.isfinite(data)]  # Remove NaNs e Infs

#     if data.size == 0:
#         raise ValueError("O conjunto de dados est vazio após a remoção de valores não finitos.")

#     # Calcular o histograma (com contagens)
#     counts, bins = np.histogram(data, bins=20)
#     bin_centers = (bins[:-1] + bins[1:]) / 2

#     hist = go.Bar(
#         x=bin_centers,
#         y=counts,
#         name='Histograma'
#     )

#     # Calcular a curva de densidade (KDE)
#     kde = gaussian_kde(data)
#     x_vals = np.linspace(data.min(), data.max(), 1000)
#     kde_vals = kde(x_vals)

#     # Escalar a KDE para corresponder às contagens do histograma
#     kde_scaled = kde_vals * data.size * (bins[1] - bins[0])

#     kde_line = go.Scatter(
#         x=x_vals,
#         y=kde_scaled,
#         mode='lines',
#         name='Densidade',
#         line=dict(color='red', width=2)
#     )

#     # Criar a figura e adicionar os traços
#     fig = go.Figure(data=[hist, kde_line])

#     # Atualizar o layout
#     fig.update_layout(
#         title=title,
#         xaxis_title=x_label,
#         yaxis_title=y_label,
#         bargap=0.1,
#         legend=dict(title='Legenda')
#     )

#     return fig

# def plot_bar_group(**kwargs):
#     """
#     Cria um grafico de barras agrupadas com intervalos de confiança.

#     Args Obrigatórios:
#         labels (np.ndarray): Rótulos do eixo X.
#         values (np.ndarray): Valores das barras. Deve ser um array 2D.
#         intervalos (np.ndarray): Intervalos de confiança para as barras. Deve ser um array 2D.
#         legends (np.ndarray): Legendas para cada grupo de barras.

#     Args Opcionais:
#         x_label (str): Legenda do eixo X.
#         y_label (str): Legenda do eixo Y.
#         title (str): Titulo do grafico.
#         show_num (bool): Se True, exibe os valores acima das barras.

#     Retorna:
#         fig (go.Figure): Figura plotly com o grafico de barras.
#     """
#     labels = kwargs.get("labels")
#     values = kwargs.get("values")
#     intervalos = kwargs.get("intervalos")
#     legends = kwargs.get("legends")

#     # Verifica tipo das variveis de input
#     if not isinstance(labels, np.ndarray):
#         raise ValueError("A varivel `labels` deve ser do tipo np.array")
#     elif not isinstance(values, np.ndarray):
#         raise ValueError("A varivel `values` deve ser do tipo np.array")
#     elif not isinstance(intervalos, np.ndarray):
#         raise ValueError("A varivel `intervalos` deve ser do tipo np.array")
#     elif not isinstance(legends, np.ndarray):
#         raise ValueError("A varivel `legends` deve ser do tipo np.array")

#     # Parâmetros default
#     x_label = kwargs.get("x_label", "Eixo X")
#     y_label = kwargs.get("y_label", "Eixo Y")
#     title = kwargs.get("title", "grafico de Barras")
#     show_num = kwargs.get("show_num", False)

#     fig = go.Figure()

#     x = labels
#     ymax = (values + intervalos).max() * 1.2

#     # Plotando as barras para cada subcategoria
#     for i, (subcategory, val, err) in enumerate(zip(legends, values, intervalos)):
#         fig.add_trace(go.Bar(
#             x=x,
#             y=val,
#             name=subcategory,
#             error_y=dict(type='data', array=err, visible=True),
#             offsetgroup=i,
#             text=val if show_num else None,
#             textposition='outside' if show_num else None
#         ))

#     # Atualizar layout
#     fig.update_layout(
#         title=title,
#         xaxis_title=x_label,
#         yaxis_title=y_label,
#         barmode='group',
#         yaxis=dict(range=[0, ymax]),
#         legend_title_text='Legenda'
#     )

#     return fig


# def plot_bar(**kwargs):
#     """
#     Cria um grafico de barras simples com intervalos de confiança.

#     Args Obrigatórios:
#         values (np.ndarray): Valores das barras.
#         intervalos (np.ndarray): Intervalos de confiança para cada barra.

#     Args Opcionais:
#         labels (np.ndarray): Rótulos das barras.
#         x_label (str): Legenda do eixo X.
#         y_label (str): Legenda do eixo Y.
#         title (str): Titulo do grafico.
#         show_num (bool): Se True, exibe os valores acima das barras.

#     Retorna:
#         fig (go.Figure): Figura plotly com o grafico de barras.
#     """
#     # Parâmetros Obrigatórios
#     values = kwargs.get("values")
#     intervalos = kwargs.get("intervalos")

#     # Verifica tipo das variveis de input
#     if not isinstance(values, np.ndarray):
#         raise ValueError("A varivel `values` deve ser do tipo np.array")
#     elif not isinstance(intervalos, np.ndarray):
#         raise ValueError("A varivel `intervalos` deve ser do tipo np.array")

#     # Parâmetros default
#     labels = kwargs.get("labels", np.array(['']))
#     x_label = kwargs.get("x_label", "Eixo X")
#     y_label = kwargs.get("y_label", "Eixo Y")
#     title = kwargs.get("title", "grafico de Barras")
#     show_num = kwargs.get("show_num", False)

#     ymax = (values + intervalos).max() * 1.2

#     fig = go.Figure(go.Bar(
#         x=labels,
#         y=values,
#         error_y=dict(type='data', array=intervalos, visible=True),
#         text=values if show_num else None,
#         textposition='outside' if show_num else None
#     ))

#     fig.update_layout(
#         title=title,
#         xaxis_title=x_label,
#         yaxis_title=y_label,
#         yaxis=dict(range=[0, ymax]),
#     )

#     return fig
