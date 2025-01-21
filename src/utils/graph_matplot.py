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

