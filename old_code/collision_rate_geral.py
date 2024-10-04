from src.visualization.collision_rate import calculate_collision_rate, plot_collision_rate

def collision_rate_geral(df):
    df.columns = df.columns.str.strip()
    df = df.sort_values(by="Numero da execucao")

    # Calcula os valores
    result = calculate_collision_rate(df)

    # Plota o gráfico
    fig = plot_collision_rate(result)
    return (fig)
