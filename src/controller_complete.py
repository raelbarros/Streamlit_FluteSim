import streamlit as st
import pandas as pd
import ast
import re
import matplotlib.pyplot as plt
import numpy as np

# COMPLETA
from src.exposition.complete.collision_rate import collision_rate_geral
from src.exposition.complete.collision_rate_per_execution import collision_rate_per_execution
from src.exposition.complete.drone_density_per_execution import drone_density_per_execution

# Mapeamento dos nomes de arquivos com as funções correspondentes
_MAP_COMPLETE_FUNCTIONS = {
    'droneCollisionData': [],
    'generalSimulationData': [collision_rate_geral, collision_rate_per_execution, drone_density_per_execution],
    'generalDroneData': [],
}

def _process_data(csv_file, functions):
    results = []
    try:
        # Carrega o CSV no pandas
        df = pd.read_csv(csv_file)
        # Para cada função, exibe o gráfico com título
        for func in functions:
            # Processa os dados
            func(df)
            result = {
                'value': func(df),
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
                    results = _process_data(file, funcs)
                    for result in results:
                        # Adiciona informações adicionais ao resultado
                        result.update({
                            'simulation_name': sim_name,
                            'file_name': file.name
                        })
                        all_results.append(result)
                    break  # Sai do loop após processar result
            else:
                st.warning(f"O arquivo {file.name} não tem funções associadas.")

    # Após processar todos os arquivos, cria o DataFrame
    if all_results:
        results_df = pd.DataFrame(all_results)
        st.write("### Resultados Agregados")

        # Cria abas por nome de arquivo
        file_tabs = st.tabs([f"Arquivo: {file_name}" for file_name in file_names])
        for tab, file_name in zip(file_tabs, file_names):
            with tab:
                st.header(f"Análises para {file_name}")
                
                # Filtra os resultados para este arquivo
                df_file = results_df[results_df['file_name'] == file_name]
                if not df_file.empty:
                    # Gera os gráficos para este arquivo
                    # COLOCAR GRAFICO AQUI
                    teste(df_file)
                else:
                    st.write("Nenhum dado disponível para este arquivo.")
    else:
        st.warning("Nenhum resultado foi gerado.")


def teste(df):
    for key, funcs in _MAP_COMPLETE_FUNCTIONS.items():
        for func in funcs:
            func_name = func.__name__  # Obtém o nome da função como string
            df_grouped = df[
                    (df["file_name"] == f"{key}.csv")
                    & (df["function_name"] == func_name)
                ]
            plot_graph(df_grouped, func_name)


from utils.graph_plotly import plot_bar_simple
def plot_graph(df, func):
    if func == "collision_rate_geral":
        # Extrai o valor de 'media' dos dicionários
        df['media'] = df['value'].apply(lambda x: x['media'] if x else None)
        df['desvio_padrao'] = df['value'].apply(lambda x: x['desvio_padrao'] if x else None)
        df['intervalo'] = df['value'].apply(lambda x: x['intervalo'] if x else None)
        
        media = df['media'].values
        intervalo = df['intervalo'].values
        labels = df['simulation_name'].tolist()

        st.plotly_chart(plot_bar_simple(
            values=media,
            intervalos=intervalo,
            labels=labels,
            title="Taxa de Colisão Geral",
            x_label="Simulação",
            y_label="Collision rate (%)",
            )
        )