import streamlit as st
import pandas as pd

from lib.exposition.simple.collision_rate_per_execution import collision_rate_per_execution
from lib.exposition.simple.collision_rate import collision_rate_geral
from lib.exposition.simple.time_successful_trips_stable import time_successful_trips_stable
from lib.exposition.simple.flight_height import boxsplot_flight_height
from lib.exposition.simple.collisions_per_situation import collisions_per_situation
from lib.exposition.simple.duration_successful_trips import duration_successful_trips
from lib.exposition.simple.drone_density_per_execution import drone_density_per_execution


# Mapeamento dos nomes de arquivos com as funções correspondentes
_MAP_SIMPLE_FUNCTIONS = {
    'droneCollisionData': [collisions_per_situation],
    'generalSimulationData': [collision_rate_per_execution, collision_rate_geral, drone_density_per_execution],
    'generalDroneData': [time_successful_trips_stable, duration_successful_trips, boxsplot_flight_height],
}


# Função para exibir os gráficos
def _display_graph_simple(csv_file, functions, tab):
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
                    _display_graph_simple(file, funcs, tabs[i])
    else:
        st.write("Por favor, faça o upload dos arquivos CSV para gerar os gráficos.")



import streamlit as st
import pandas as pd
import plotly.express as px

# COMPLETA
from lib.exposition.complete.collision_rate import collision_rate_geral as collision_rate_geral_complete

# Mapeamento dos nomes de arquivos com as funções correspondentes
_MAP_COMPLETE_FUNCTIONS = {
    'droneCollisionData': [],
    'generalSimulationData': [collision_rate_geral_complete],
    'generalDroneData': [],
}

def _process_complete_data(csv_file, functions):
    results = []
    try:
        # Carrega o CSV no pandas
        df = pd.read_csv(csv_file)
        # Para cada função, exibe o gráfico com título
        for func in functions:
            # Processa os dados
            media, desvio, intervalo = func(df)
            result = {
                'mean': media,
                'std_dev': desvio,
                'confidence_interval': intervalo,
                'function_name': func.__name__
            }
            # Adiciona o resultado à lista
            results.append(result)
        return results
    except Exception as e:
        st.error(f"Erro ao processar o arquivo {csv_file.name}: {str(e)}")
        return results

def complete_process(list_simulation):
    # Lista para armazenar todos os resultados
    all_results = []
    # Conjunto para coletar nomes únicos de arquivos
    file_names = set()

    # Itera sobre as simulações
    for sim in list_simulation:
        sim_name = sim['name']
        files = sim['files']

        # Itera sobre os arquivos da simulação
        for file in files:
            file_names.add(file.name)
            # Determina o tipo de arquivo com base no nome
            for key, funcs in _MAP_COMPLETE_FUNCTIONS.items():
                if key in file.name:
                    # Processa os dados
                    results = _process_complete_data(file, funcs)
                    for result in results:
                        # Adiciona informações adicionais ao resultado
                        result.update({
                            'simulation_name': sim_name,
                            'file_name': file.name
                        })
                        all_results.append(result)
                    break  # Sai do loop após encontrar a correspondência
            else:
                # Nenhuma correspondência encontrada
                st.warning(f"O arquivo {file.name} não tem funções associadas.")

    # Após processar todos os arquivos, cria o DataFrame
    if all_results:
        results_df = pd.DataFrame(all_results)
        st.write("### Resultados Agregados")
        st.dataframe(results_df)

        # Cria abas por nome de arquivo
        file_tabs = st.tabs([f"Arquivo: {file_name}" for file_name in file_names])
        for tab, file_name in zip(file_tabs, file_names):
            with tab:
                st.header(f"Análises para {file_name}")
                # Filtra os resultados para este arquivo
                df_file = results_df[results_df['file_name'] == file_name]
                if not df_file.empty:
                    # Gera os gráficos para este arquivo
                    fig = px.bar(
                        df_file,
                        x='simulation_name',
                        y='mean',
                        color='function_name',
                        barmode='group',
                        title=f'Média por Simulação e Função para {file_name}'
                    )
                    st.plotly_chart(fig)
                else:
                    st.write("Nenhum dado disponível para este arquivo.")
    else:
        st.warning("Nenhum resultado foi gerado.")
