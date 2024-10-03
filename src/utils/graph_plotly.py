import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import plotly.io as pio


pio.templates.default = 'gridon'


def plot_boxsplot(title, labels, *args):
    """
    Cria um boxplot usando plotly.

    Args:
        title (str): Título do gráfico.
        labels (list): Lista de rótulos para cada conjunto de dados.
        args: Conjuntos de dados para plotar.

    Retorna:
        fig (go.Figure): Figura plotly com o boxplot.
    """
    fig = go.Figure()

    for i, x in enumerate(args):
        fig.add_trace(go.Box(y=x, name=labels[i]))

    fig.update_layout(
        title=title,
        xaxis_title='',
        yaxis_title='',
        yaxis_tickfont_size=12,
        xaxis_tickfont_size=12,
        xaxis_tickvals=labels,
        showlegend=False
    )

    return fig



def plot_histogram(df, x_label, y_label, title):
    """
    Cria um histograma com contagens e sobrepõe a curva KDE escalada para as contagens.
    """
    # Converter e limpar os dados
    data = np.asarray(df)
    data = data[np.isfinite(data)]  # Remove NaNs e Infs

    if data.size == 0:
        raise ValueError("O conjunto de dados está vazio após a remoção de valores não finitos.")

    # Calcular o histograma (com contagens)
    counts, bins = np.histogram(data, bins=20)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    hist = go.Bar(
        x=bin_centers,
        y=counts,
        name='Dados'
    )

    # Calcular a curva de densidade (KDE)
    kde = gaussian_kde(data)
    x_vals = np.linspace(data.min(), data.max(), 1000)
    kde_vals = kde(x_vals)

    # Escalar a KDE para corresponder às contagens do histograma
    kde_scaled = kde_vals * data.size * (bins[1] - bins[0])

    kde_line = go.Scatter(
        x=x_vals,
        y=kde_scaled,
        mode='lines',
        name='Densidade',
        line=dict(color='red', width=2)
    )

    # Criar a figura e adicionar os traços
    fig = go.Figure(data=[hist, kde_line])

    # Atualizar o layout
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        bargap=0.1
    )

    return fig

def plot_bar_group(**kwargs):
    """
    Cria um gráfico de barras agrupadas com intervalos de confiança.

    Args Obrigatórios:
        labels (np.ndarray): Rótulos do eixo X.
        values (np.ndarray): Valores das barras. Deve ser um array 2D.
        intervalos (np.ndarray): Intervalos de confiança para as barras. Deve ser um array 2D.
        legends (np.ndarray): Legendas para cada grupo de barras.

    Args Opcionais:
        x_label (str): Legenda do eixo X.
        y_label (str): Legenda do eixo Y.
        title (str): Título do gráfico.
        show_num (bool): Se True, exibe os valores acima das barras.

    Retorna:
        fig (go.Figure): Figura plotly com o gráfico de barras.
    """
    labels = kwargs.get("labels")
    values = kwargs.get("values")
    intervalos = kwargs.get("intervalos")
    legends = kwargs.get("legends")

    # Verifica tipo das variáveis de input
    if not isinstance(labels, np.ndarray):
        raise ValueError("A variável `labels` deve ser do tipo np.array")
    elif not isinstance(values, np.ndarray):
        raise ValueError("A variável `values` deve ser do tipo np.array")
    elif not isinstance(intervalos, np.ndarray):
        raise ValueError("A variável `intervalos` deve ser do tipo np.array")
    elif not isinstance(legends, np.ndarray):
        raise ValueError("A variável `legends` deve ser do tipo np.array")

    # Parâmetros default
    x_label = kwargs.get("x_label", "Eixo X")
    y_label = kwargs.get("y_label", "Eixo Y")
    title = kwargs.get("title", "Gráfico de Barras")
    show_num = kwargs.get("show_num", False)

    fig = go.Figure()

    x = labels
    ymax = (values + intervalos).max() * 1.2

    # Plotando as barras para cada subcategoria
    for i, (subcategory, val, err) in enumerate(zip(legends, values, intervalos)):
        fig.add_trace(go.Bar(
            x=x,
            y=val,
            name=subcategory,
            error_y=dict(type='data', array=err, visible=True),
            offsetgroup=i,
            text=val if show_num else None,
            textposition='outside' if show_num else None
        ))

    # Atualizar layout
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        barmode='group',
        yaxis=dict(range=[0, ymax]),
        legend_title_text='Legenda'
    )

    return fig


def plot_bar_simple(**kwargs):
    """
    Cria um gráfico de barras simples com intervalos de confiança.

    Args Obrigatórios:
        values (np.ndarray): Valores das barras.
        intervalos (np.ndarray): Intervalos de confiança para cada barra.

    Args Opcionais:
        labels (np.ndarray): Rótulos das barras.
        x_label (str): Legenda do eixo X.
        y_label (str): Legenda do eixo Y.
        title (str): Título do gráfico.
        show_num (bool): Se True, exibe os valores acima das barras.

    Retorna:
        fig (go.Figure): Figura plotly com o gráfico de barras.
    """
    # Parâmetros Obrigatórios
    values = kwargs.get("values")
    intervalos = kwargs.get("intervalos")

    # Verifica tipo das variáveis de input
    if not isinstance(values, np.ndarray):
        raise ValueError("A variável `values` deve ser do tipo np.array")
    elif not isinstance(intervalos, np.ndarray):
        raise ValueError("A variável `intervalos` deve ser do tipo np.array")

    # Parâmetros default
    labels = kwargs.get("labels", np.array(['']))
    x_label = kwargs.get("x_label", "Eixo X")
    y_label = kwargs.get("y_label", "Eixo Y")
    title = kwargs.get("title", "Gráfico de Barras")
    show_num = kwargs.get("show_num", False)

    ymax = (values + intervalos).max() * 1.2

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        error_y=dict(type='data', array=intervalos, visible=True),
        text=values if show_num else None,
        textposition='outside' if show_num else None
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        yaxis=dict(range=[0, ymax]),
    )

    return fig
