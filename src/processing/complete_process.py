import streamlit as st
import pandas as pd

# Importando as funçoes de cada grafico
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

def process_simulation_files(simulation):
    """
    Processa os arquivos de uma simulação individual.

    Args:
        simulation (dict): Dicionario contendo o nome da simulação e os arquivos.
    Returns:
        list: Lista de dicionarios com os resultados.
    """
    results = []
    sim_name = simulation['name']
    list_files = simulation['files']

    for file in list_files:
        file_processed = False
        
        for key, funcs in MAP_FUNCTIONS.items():
            if key in file.name:
                
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()
                df = df.sort_values(by="Numero da execucao")

                for func_dict in funcs:
                    calc_func = func_dict['function_name']
                    plot_func = func_dict['plot']
                    
                    func_name = calc_func.__name__
                    plot_func_name = plot_func.__name__
                    
                    try:
                        value = calc_func(df)
                        result = {
                            'simulation_name': sim_name,
                            'file_name': file.name,
                            'function_name': func_name,
                            'value': value,
                            'plot_function': plot_func_name
                        }
                        results.append(result)
                    
                    except Exception as e:
                        st.error(f"Erro ao processar {func_name} no arquivo {file.name}: {e}")
                
                file_processed = True
                break  # Sai do loop depois processar o arquivo
        
        if not file_processed:
            st.warning(f"O arquivo {file.name} não tem funçoes associadas.")
    
    return results


def aggregate_results(all_results):
    """
    Agrega os resultados de todas as simulações e exibe os gráficos.

    Args:
        all_results (list): Lista de resultados de todas as simulações.
    """
    if not all_results:
        st.warning("Nenhum resultado foi gerado.")
        return

    results_df = pd.DataFrame(all_results)

    # Cria abas por nome do arquivo
    files_name = results_df['file_name'].unique()
    tabs = st.tabs([f"Arquivo: {file}" for file in files_name])

    for tab, file_name in zip(tabs, files_name):
        with tab:

            # Filtra os resultados para este arquivo
            df_file = results_df[results_df['file_name'] == file_name]

            # Obter todos os nomes de funções para este arquivo
            function_names = df_file['function_name'].unique()

            for func_name in function_names:
                df_func = df_file[df_file['function_name'] == func_name]

                if not df_func.empty:
                    st.subheader(f"Análise: {func_name.replace('_', ' ').capitalize()}")

                    # Extrair os valores
                    data = df_func['value'].tolist()
                    labels = df_func['simulation_name'].tolist()
                    plot_func_name = df_func['plot_function'].iloc[0]

                    # Gerar e exibir o gráfico
                    plot_func = globals()[plot_func_name]
                    
                    fig = plot_func(data, labels=labels)
                    # Gerar e exibir o grafico
                    if fig:
                        st.plotly_chart(fig)
                        st.divider()
                    else:
                        st.warning(f"A função {func_name} não retornou um grafico.")
                else:
                    st.write(f"Nenhum dado disponível para a análise {func_name}.")


def complete_process(list_simulation):
    """
    Processa todas as simulaçoes para a analise completa.

    Args:
        list_simulation (list): Lista de simulaçoes com seus respectivos arquivos.
    """
    all_results = []

    for simulation in list_simulation:
        results = process_simulation_files(simulation)
        all_results.extend(results)

    aggregate_results(all_results)