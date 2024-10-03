import streamlit as st
import pandas as pd

from src.exposition.simple.collision_rate_per_execution import collision_rate_per_execution
from src.exposition.simple.collision_rate import collision_rate_geral
from src.exposition.simple.time_successful_trips_stable import time_successful_trips_stable
from src.exposition.simple.flight_height import boxsplot_flight_height
from src.exposition.simple.collisions_per_situation import collisions_per_situation
from src.exposition.simple.duration_successful_trips import duration_successful_trips
from src.exposition.simple.drone_density_per_execution import drone_density_per_execution


# Mapeamento dos nomes de arquivos com as funções correspondentes
_MAP_SIMPLE_FUNCTIONS = {
    'droneCollisionData': [collisions_per_situation],
    'generalSimulationData': [collision_rate_per_execution, collision_rate_geral, drone_density_per_execution],
    'generalDroneData': [time_successful_trips_stable, duration_successful_trips, boxsplot_flight_height],
}


# Função para exibir os gráficos
def _display_plot(csv_file, functions, tab):
    try:
        # Carrega o CSV no pandas
        df = pd.read_csv(csv_file)

        # Para cada função, exibe o gráfico com titulo
        for func in functions:
            with tab:
                st.subheader(f"Análise: {func.__name__.replace('_', ' ').capitalize()}")
                #st.write(f"Gráfico gerado para o arquivo **{csv_file.name}**")
                # Exibir gráfico
                st.plotly_chart(func(df))

    except Exception as e:
        st.error(f"Erro ao gerar o gráfico: {str(e)}")


def simple_process(uploaded_files):
    # Verifica se há arquivos enviados
    if uploaded_files:
        # Organiza os gráficos em abas
        tabs = st.tabs([f"Arquivo: {file.name}" for file in uploaded_files])

        # Loop através dos arquivos enviados
        for i, file in enumerate(uploaded_files):
            for key, funcs in _MAP_SIMPLE_FUNCTIONS.items():
                if key in file.name:
                    # Cada aba exibe os gráficos correspondentes a um arquivo
                    _display_plot(file, funcs, tabs[i])
    else:
        st.write("Por favor, faça o upload dos arquivos CSV para gerar os gráficos.")
