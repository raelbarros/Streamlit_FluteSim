import streamlit as st
import pandas as pd

#MIGRANDO
from src.visualization.collision_rate import calculate_collision_rate, plot_collision_rate
from src.visualization.collision_rate_per_execution import calculate_collision_rate_per_execution, plot_collision_rate_per_execution
from src.visualization.collisions_per_situation import calculate_collisions_per_situation, plot_collisions_per_situation
from src.visualization.drone_density_per_execution import calculate_drone_density_per_execution, plot_drone_density_per_execution
from src.visualization.duration_successful_trips import calculate_duration_successful_trips, plot_duration_successful_trips
from src.visualization.flight_height import calculate_flight_height, plot_flight_height
from src.visualization.time_successful_trips_stable import calculate_time_successful_trips_stable, plot_time_successful_trips_stable


# Mapeamento dos nomes de arquivos com as funçoes correspondentes
MAP_FUNCTIONS = {
    'droneCollisionData': [
        {
            'function_name': calculate_collisions_per_situation,
            'plot': plot_collisions_per_situation,
        },
    ],
    'generalSimulationData': [
        {
            'function_name': calculate_collision_rate,
            'plot': plot_collision_rate,
        },
        {
            'function_name': calculate_collision_rate_per_execution,
            'plot': plot_collision_rate_per_execution,
        },
        {
            'function_name': calculate_drone_density_per_execution,
            'plot': plot_drone_density_per_execution,
        },
    ],
    'generalDroneData': [
        {
            'function_name': calculate_duration_successful_trips,
            'plot': plot_duration_successful_trips,
        },
        {
            'function_name': calculate_flight_height,
            'plot': plot_flight_height,
        },
        {
            'function_name': calculate_time_successful_trips_stable,
            'plot': plot_time_successful_trips_stable,
        },
    ],
}


def _display_plots(file, functions):
    """
    Carrega o arquivo CSV e exibe os graficos correspondentes.

    Args:
        file (UploadedFile): O arquivo CSV enviado pelo usuario.
        functions (list): Lista de funçoes para gerar os graficos.
    """
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df = df.sort_values(by="Numero da execucao")

        for func_dict in functions:
            calc_func = func_dict['function_name']
            plot_func = func_dict['plot']
            func_name = calc_func.__name__
            
            st.subheader(f"Analise: {func_name.replace('_', ' ').capitalize()}")
            
            value = calc_func(df)
            fig = plot_func(value)

            # Gerar e exibir o grafico
            if fig:
                st.plotly_chart(fig)
                st.divider()
            else:
                st.warning(f"A função {func_name} não retornou um grafico.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo {file.name}: {str(e)}")


def simple_process(uploaded_files):
    """
    Processa os arquivos enviados para a analise simples.

    Args:
        uploaded_files (list): Lista de arquivos enviados pelo usuario.
    """
    if not uploaded_files:
        st.info("Por favor, faça o upload dos arquivos CSV para gerar os graficos.")
        return

    # Organiza os graficos em abas
    tabs = st.tabs([f"Arquivo: {file.name}" for file in uploaded_files])

    for i, file in enumerate(uploaded_files):
        file_processed = False
        
        for key, funcs in MAP_FUNCTIONS.items():
            if key in file.name:
                
                with tabs[i]:
                    _display_plots(file, funcs)
                
                file_processed = True
                break
        
        if not file_processed:
            st.warning(f"O arquivo {file.name} não tem funçoes associadas.")


