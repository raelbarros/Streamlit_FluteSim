import pandas as pd
import matplotlib.pyplot as plt


"""
    Arquivo não contemplado no streamlit
    É necessario passar o caminho da pasta para ler o arquivo droneCollisionData.csv
"""


#FIXME: alterar caminho e qtd de execuções ***SEM A PASTA 8000-0***
pasta_simulacoes = r'D:\RESULTS\Exec_07\128_60_30x_model_10'


_FILE = 'droneCollisionData.csv'
final_path = f"{pasta_simulacoes}\{_FILE}"

df = pd.read_csv(final_path)
df.columns = df.columns.str.strip()

x = df['posicao da colisao no eixo x']
y = df['posicao da colisao no eixo z']

plt.figure(figsize=(8, 6))

plt.scatter(x, y)

plt.title('Pontos de Colisões do Drone')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Z')
plt.legend()

#plt.grid(True)
plt.show()