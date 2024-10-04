import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px


pio.templates.default = 'gridon'


def plot_boxsplot(df, title, x, y, color, labels):
    """
    Cria um boxplot usando plotly.

    Args:
        title (str): Titulo do grafico.
        labels (list): Lista de rótulos para cada conjunto de dados.
        args: Conjuntos de dados para plotar.

    Retorna:
        fig (go.Figure): Figura plotly com o boxplot.
    """

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels
    )

    return fig



def plot_histogram(df, title, x, color, labels):
    """
    Cria um histograma com contagens
    """

    fig = px.histogram(
        df,
        x=x,
        color=color,
        title=title,
        labels=labels,
        barmode='overlay',
        nbins=50,
        opacity=0.75
    )

    return fig


def plot_bar(values, intervalos=None, labels=None, x_label="Eixo X", y_label="Eixo Y", title="grafico de Barras", show_num=False, show_interval=True):
    """
    Cria um grafico de barras (simples ou agrupado) com intervalos de confiança.

    Args:
        values (np.ndarray or list of np.ndarray): Valores das barras. Pode ser um array para barras simples ou uma lista de arrays para barras agrupadas.
        intervalos (np.ndarray or list of np.ndarray): Intervalos de confiança para cada barra ou grupo de barras.
        labels (np.ndarray): Rótulos das barras (para o eixo X).
        x_label (str): Legenda do eixo X.
        y_label (str): Legenda do eixo Y.
        title (str): Titulo do grafico.
        show_num (bool): Se True, exibe os valores acima das barras.

    Retorna:
        fig (go.Figure): Figura plotly com o grafico de barras.
    """
    # Verifica se values e uma lista (barras agrupadas) ou um array (barras simples)
    if isinstance(values, list):
        num_series = len(values)
        if labels is None:
            raise ValueError("Para barras agrupadas, 'labels' deve ser fornecido.")

        fig = go.Figure()
        for i in range(num_series):
            series_values = values[i]
            series_intervalos = intervalos[i] if isinstance(intervalos, list) else intervalos
            series_name = f"Serie {i+1}"

            error_y = dict(type='data', array=series_intervalos, visible=True) if show_interval and series_intervalos is not None else None

            fig.add_trace(go.Bar(
                x=labels,
                y=series_values,
                name=series_name,
                error_y=error_y,
                text=series_values if show_num else None,
                textposition='outside' if show_num else None
            ))
        fig.update_layout(barmode='group')
    else:
        # grafico de barras simples
        fig = go.Figure(go.Bar(
            x=labels,
            y=values,
            error_y=dict(type='data', array=intervalos, visible=True),
            text=values if show_num else None,
            textposition='outside' if show_num else None
        ))

    ymax = (np.array(values).max() + np.array(intervalos).max()) * 1.2

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        yaxis=dict(range=[0, ymax]),
    )

    return fig