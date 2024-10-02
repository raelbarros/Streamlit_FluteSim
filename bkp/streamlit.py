# import pandas as pd
# from lib.handler.collision_rate_simple import collision_rate_simple
# from lib.utils import plot_bar_simple, plot_boxsplot
# import streamlit as st

# # Page config
# st.set_page_config(page_title="Dash FluteSim", layout="wide")

# _VALID_FILES = ['droneCollisionData.csv', 'generalDroneData.csv', 'generalSimulationData.csv']

# st.sidebar.title("Análise de Dados de Simulações do FluteSim")

# st.sidebar.subheader("1. Data")
# with st.sidebar:
#     option = st.selectbox(
#         "Que tipo de análise você deseja?",
#         ("Simples", "Completa"),
#         index=None,
#         placeholder="Selecione o método...",
#     )

#     simple = st.file_uploader(
#         "Upload dos dados da Simulação", type="csv", accept_multiple_files=True
#     )

# # Processamento dos arquivos e geração do gráfico
# if option == "Simples" and simple:
#     for i in simple:
#         if i.name not in _VALID_FILES:
#             st.error("Arquivos inválidos, verifique se os nomes dos arquivos estão corretos")
#             st.stop()
        
#         if i.name == 'generalSimulationData.csv':
#             df = pd.read_csv(i)
#             df.columns = df.columns.str.strip()

#             list_media, list_intervalo = collision_rate_simple(df)
            
#             fig = plot_bar_simple(
#                 type='simple',
#                 values=list_media,
#                 intervalos=list_intervalo,
#                 title="Taxa de Colisão por Taxa de Chegada",
#                 x_label="Arrival rate (drones/min)",
#                 y_label="Collision rate (%)",
#                 figsize=(8, 4)
#             )
#             # Renderiza o gráfico na área principal
#             st.pyplot(fig)
        
#         if i.name == 'generalDroneData.csv':
#             df = pd.read_csv(i)
#             df.columns = df.columns.str.strip()

#             fig = plot_boxsplot("Altura", 'Maxima', df["altitude maxima atingida"])

#             st.pyplot(fig)

#     # elif option == "Completa":
#     #     number = st.number_input(
#     #         "Quantidade de Simulações", min_value=2, max_value=5, step=1
#     #     )

#     #     list_files = []
#     #     for i in range(number):
#     #         file = st.file_uploader(
#     #             f"Upload dos dados da Simulação {i+1}", type="csv", accept_multiple_files=True, key=f"uploader_{i}"
#     #         )
#     #         if file is not None:
#     #             list_files.append(file)
