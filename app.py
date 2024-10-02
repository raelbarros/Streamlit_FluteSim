import streamlit as st
from lib.controller_simple import simple_process
from lib.controller_complete import complete_process

# Nome dos arquivos validos
_VALID_FILES = ['droneCollisionData.csv', 'generalDroneData.csv', 'generalSimulationData.csv']


# Configuracao da Pagina
st.set_page_config(
    page_title="Drone Simulation Dashboard",
    page_icon="🛸",
    layout="wide"  # Isso ativa a tela larga
)
st.title("Drone Simulation Dashboard")
st.markdown("""
    Bem-vindo ao dashboard de simulação de drones! 
    Aqui você pode enviar os dados da sua simulação, e gerar gráficos analíticos para entender o desempenho dos seus drones.
    **Siga os passos abaixo**:
    1. Escolha o tipo de análise que deseja realizar.
    2. Faça o upload dos arquivos CSV no menu lateral.
    3. Veja os gráficos gerados na tela principal.
""")

# Menu lateral para upload dos arquivos CSV
with st.sidebar:
    st.header("Upload dos arquivos CSV 📂")
    st.markdown("""
        **Arquivos válidos**:
        - `droneCollisionData.csv`
        - `generalDroneData.csv`
        - `generalSimulationData.csv`
    """)

    option = st.selectbox(
        "Que tipo de análise você deseja?",
        ("Simples", "Completa"),
        index=None,
        placeholder="Selecione o método...",
    )

# Processamento dos arquivos e geração do gráfico
    if option == "Simples":

        uploaded_files = st.file_uploader(
            "Upload dos dados da Simulação", type="csv", accept_multiple_files=True
        )
        for i in uploaded_files:
            if i.name not in _VALID_FILES:
                st.error("Arquivos inválidos, verifique se os nomes dos arquivos estão corretos")
                st.stop()
            

    elif option == "Completa":
        qtd_exec = st.number_input(
            "Quantidade de Simulações", min_value=2, max_value=5, step=1
        )

        list_simulation = []
        for i in range(qtd_exec):
            st.divider()
            st.subheader(f"Informações da Simulação {i+1} 👇")

            name = st.text_input("Titulo da Simulação, ex: 12/60", key=f"name_{i}")
            file = st.file_uploader(
                f"Upload dos dados da Simulação {i+1}", type="csv", accept_multiple_files=True, key=f"uploader_{i}"
            )

            # Armazena as informações em um dicionário
            list_simulation.append({'name': name, 'files': file})



if option == 'Simples' and uploaded_files:
    with st.spinner('Processando arquivos e gerando gráficos...'):
        simple_process(uploaded_files)

    st.success('Gráficos gerados com sucesso!')


if option == "Completa":
    # Verifica se tem itens nulos nas listas de arquivos e nomes
    missing_data = any(not sim['name'] or not sim['files'] for sim in list_simulation)

    if missing_data:
        st.info('Preencha as informações das Simulações', icon="ℹ️")

    else:
        with st.spinner('Processando arquivos e gerando gráficos...'):
            # # Processamento das simulações
            # for sim in list_simulation:
            #     name = sim['name']
            #     files = sim['files']

            complete_process(list_simulation)
                
        st.success('Gráficos gerados com sucesso!')
    