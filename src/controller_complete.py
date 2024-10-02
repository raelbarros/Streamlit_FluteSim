import streamlit as st
import pandas as pd
import plotly.express as px

# COMPLETA
from lib.exposition.complete.collision_rate import collision_rate_geral

# Mapeamento dos nomes de arquivos com as funções correspondentes
_MAP_COMPLETE_FUNCTIONS = {
    'droneCollisionData': [],
    'generalSimulationData': [collision_rate_geral],
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
