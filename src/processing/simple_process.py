import streamlit as st
import pandas as pd

# Importando as funçoes de cada grafico
from src.visualization.execution.collision_rate_per_execution import calculate_collision_rate_per_execution, plot_collision_rate_per_execution
from src.visualization.simulation.collision_rate_per_simulation import calculate_collision_rate_per_simulation, plot_collision_rate_per_simulation
from src.visualization.simulation.collisions_per_situation import calculate_collisions_per_situation, plot_collisions_per_situation
from src.visualization.execution.drone_density_per_execution import calculate_drone_density_per_execution, plot_drone_density_per_execution
from src.visualization.simulation.drone_density_per_simulation import calculate_drone_density_per_simulation, plot_drone_density_per_simulation
from src.visualization.execution.duration_successful_trips_per_execution import calculate_duration_successful_trips_per_execution, plot_duration_successful_trips_per_execution
from src.visualization.simulation.duration_successful_trips_per_simulation import calculate_duration_successful_trips_per_simulation, plot_duration_successful_trips_per_simulation
from src.visualization.simulation.flight_height_per_simulation import calculate_flight_height, plot_flight_height
from src.visualization.execution.time_successful_trips_stable_per_execution import calculate_time_successful_trips_stable_per_execution, plot_time_successful_trips_stable_per_execution


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
            'function_name': calculate_collision_rate_per_execution,
            'plot': plot_collision_rate_per_execution,
        },
        {
            'function_name': calculate_collision_rate_per_simulation,
            'plot': plot_collision_rate_per_simulation,
        },
        {
            'function_name': calculate_drone_density_per_execution,
            'plot': plot_drone_density_per_execution,
        },
        {
            'function_name': calculate_drone_density_per_simulation,
            'plot': plot_drone_density_per_simulation,
        },
    ],
    'generalDroneData': [
        {
            'function_name': calculate_duration_successful_trips_per_execution,
            'plot': plot_duration_successful_trips_per_execution,
        },
        {
            'function_name': calculate_duration_successful_trips_per_simulation,
            'plot': plot_duration_successful_trips_per_simulation,
        },
        {
            'function_name': calculate_flight_height,
            'plot': plot_flight_height,
        },
        {
            'function_name': calculate_time_successful_trips_stable_per_execution,
            'plot': plot_time_successful_trips_stable_per_execution,
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


