from src.utils.graph_plotly import plot_histogram, plot_boxsplot

# ARQUIVO: generalDroneData_12

def boxsplot_flight_height(df):
    df.columns = df.columns.str.strip()

    df_max = df["altitude maxima atingida"]
    df_min = df["altitude minima atingida"]

    labels = ["Maxima", "Minima"]
    return plot_boxsplot("Altura", labels, df_max, df_min)


# def histogram_flight_height(df):
#     df.columns = df.columns.str.strip()

#     df_max = df["altitude maxima atingida"]
#     df_min = df["altitude minima atingida"]

#     df_altura = pd.concat([df_max, df_min])

#     return plot_histogram(df_altura, 'Altura', 'Quantidade', 'Altura de voo')
    