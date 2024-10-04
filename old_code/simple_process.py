import streamlit as st
import pandas as pd

from src.exposition.simple.collision_rate_per_execution import collision_rate_per_execution
from src.exposition.simple.time_successful_trips_stable import time_successful_trips_stable
from src.exposition.simple.flight_height import boxsplot_flight_height
from src.exposition.simple.collisions_per_situation import collisions_per_situation
from src.exposition.simple.duration_successful_trips import duration_successful_trips
from src.exposition.simple.drone_density_per_execution import drone_density_per_execution

#MIGRANDO
from src.visualization.collision_rate import calculate_collision_rate, plot_collision_rate




# Mapeamento dos nomes de arquivos com as funções correspondentes
MAP_FUNCTIONS = {
    # 'droneCollisionData': [collisions_per_situation],
    'generalSimulationData': [
        {
            'function_name': calculate_collision_rate,
            'plot': plot_collision_rate,
        }
    ],
    # 'generalDroneData': [time_successful_trips_stable, duration_successful_trips, boxsplot_flight_height],
}


def _display_plots(file, functions):
    """
    Carrega o arquivo CSV e exibe os gráficos correspondentes.

    Args:
        file (UploadedFile): O arquivo CSV enviado pelo usuário.
        functions (list): Lista de funções para gerar os gráficos.
    """
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df = df.sort_values(by="Numero da execucao")

        for func_dict in functions:
            calc_func = func_dict['function_name']
            plot_func = func_dict['plot']
            func_name = calc_func.__name__
            
            st.subheader(f"Análise: {func_name.replace('_', ' ').capitalize()}")
            
            value = calc_func(df)

            fig = plot_func(value)

            # Gerar e exibir o gráfico
            if fig:
                st.plotly_chart(fig)
            else:
                st.warning(f"A função {func_name} não retornou um gráfico.")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo {file.name}: {str(e)}")


# def simple_process(uploaded_files):
#     """
#     Processa os arquivos enviados para a análise simples.

#     Args:
#         uploaded_files (list): Lista de arquivos enviados pelo usuário.
#     """
#     if not uploaded_files:
#         st.info("Por favor, faça o upload dos arquivos CSV para gerar os gráficos.")
#         return

#     # Organiza os gráficos em abas
#     tabs = st.tabs([f"Arquivo: {file.name}" for file in uploaded_files])

#     for i, file in enumerate(uploaded_files):
#         file_processed = False
#         for key, funcs in MAP_FUNCTIONS.items():
#             if key in file.name:
#                 with tabs[i]:
#                     _display_plots(file, funcs)
#                 file_processed = True
#                 break  # Encerra o loop após encontrar o arquivo correspondente
#         if not file_processed:
#             st.warning(f"O arquivo {file.name} não tem funções associadas.")



def simple_process(uploaded_files):
    """
    Processa os arquivos enviados para a análise simples.

    Args:
        uploaded_files (list): Lista de arquivos enviados pelo usuário.
    """
    if not uploaded_files:
        st.info("Por favor, faça o upload dos arquivos CSV para gerar os gráficos.")
        return

    # Organiza os gráficos em abas
    tabs = st.tabs([f"Arquivo: {file.name}" for file in uploaded_files])

    for i, file in enumerate(uploaded_files):
        file_processed = False
        for key, funcs in MAP_FUNCTIONS.items():
            if key in file.name:
                with tabs[i]:
                    _display_plots(file, funcs)
                file_processed = True
                break  # Encerra o loop após encontrar o arquivo correspondente
        if not file_processed:
            st.warning(f"O arquivo {file.name} não tem funções associadas.")


