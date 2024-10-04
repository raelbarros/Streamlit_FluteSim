import streamlit as st
from src.processing.simple_process import simple_process
from src.processing.complete_process import complete_process


# Constantes e Variaveis Globais
_VALID_FILES = ['droneCollisionData.csv', 'generalDroneData.csv', 'generalSimulationData.csv']
_ERROR_INVALID_FILES = "Arquivos invalidos, verifique se os nomes dos arquivos estão corretos"
_INFO_FILL_SIMULATION = "Preencha todas as informaçoes das Simulaçoes"
_SUCCESS_MESSAGE = "Graficos gerados com sucesso!"


def configure_page():
    st.set_page_config(
        page_title="Drone Simulation Dashboard",
        page_icon="🛸",
        layout="wide"
    )
    st.title("Drone Simulation Dashboard")
    st.markdown("""
        Bem-vindo ao dashboard de simulação de drones! 
        Aqui voce pode enviar os dados da sua simulação, e gerar graficos analiticos para entender o desempenho dos seus drones.
        **Siga os passos abaixo**:
        1. Escolha o tipo de analise que deseja realizar.
        2. Faça o upload dos arquivos CSV no menu lateral.
        3. Veja os graficos gerados na tela principal.
    """)


def sidebar_menu():
    with st.sidebar:
        st.header("Upload dos arquivos CSV 📂")
        st.markdown("""
            **Arquivos validos**:
            - `droneCollisionData.csv`
            - `generalDroneData.csv`
            - `generalSimulationData.csv`
        """)
        option = st.selectbox(
            "Que tipo de analise você deseja?",
            ("Simples", "Completa"),
            index=None,
            placeholder="Selecione o método...",
        )

        if option == "Simples":
            # Upload dos arquivos para a analise simples
            uploaded_files = st.file_uploader(
                "Upload dos dados da Simulação", type="csv", accept_multiple_files=True
            )
            return option, uploaded_files, None

        elif option == "Completa":
            # Configuraçoes para a analise completa
            qtd_exec = st.number_input(
                "Quantidade de Simulaçoes", min_value=2, max_value=5, step=1
            )
            list_simulation = []
            for i in range(int(qtd_exec)):
                st.divider()
                st.subheader(f"Informaçoes da Simulação {i+1} 👇")
                name = st.text_input(
                    f"Titulo da Simulação {i+1}, ex: 12/60", 
                    key=f"name_{i}", 
                    placeholder="Digite um titulo para a simulação"
                )
                files = st.file_uploader(
                    f"Upload dos dados da Simulação {i+1}", type="csv", accept_multiple_files=True, key=f"uploader_{i}"
                )
                list_simulation.append({'name': name, 'files': files})
            return option, None, list_simulation

    # Retorno padrão caso nada seja selecionado
    return option, None, None


def validate_uploaded_files(uploaded_files):
    invalid_files = [file.name for file in uploaded_files if file.name not in _VALID_FILES]
    if invalid_files:
        st.error(f"Arquivos invalidos encontrados: {', '.join(invalid_files)}")
        st.stop()
    for file in uploaded_files:
        if file.size == 0:
            st.error(f"O arquivo {file.name} esta vazio.")
            st.stop()


def process_simple_simulation(uploaded_files):
    try:
        with st.spinner('Processando arquivos e gerando graficos...'):
            simple_process(uploaded_files)
        st.success(_SUCCESS_MESSAGE)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os arquivos: {e}")


def process_complete_simulation(list_simulation):
    try:
        with st.spinner('Processando arquivos e gerando graficos...'):
            complete_process(list_simulation)
        st.success(_SUCCESS_MESSAGE)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar as simulaçoes: {e}")


def main():
    configure_page()
    option, uploaded_files, list_simulation = sidebar_menu()

    if option == "Simples":
        if uploaded_files:
            validate_uploaded_files(uploaded_files)
            process_simple_simulation(uploaded_files)
        else:
            st.info('Por favor, faça o upload dos arquivos da simulação.', icon="ℹ️")

    elif option == "Completa":
        # Verifica se todas as informaçoes foram preenchidas
        if list_simulation and all(sim['name'] and sim['files'] for sim in list_simulation):
            # Valida os arquivos de cada simulação
            for sim in list_simulation:
                validate_uploaded_files(sim['files'])

            process_complete_simulation(list_simulation)
        else:
            st.info(_INFO_FILL_SIMULATION, icon="ℹ️")


if __name__ == "__main__":
    main()
