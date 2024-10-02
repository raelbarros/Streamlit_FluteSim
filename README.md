
# Simulação de Flauta com Streamlit


## Instalação

Para instalar as dependências necessárias, certifique-se de ter o Python, depois siga estes passos:

1. Clone o repositório:

```bash
git clone https://github.com/raelbarros/streamlitFluteSim.git
cd streamlitFluteSim
```

2. Instale as dependências usando o `Poetry`:

```bash
pip install -r requirements.txt
```

3. Para executar a aplicação:

```bash
streamlit run app.py
```

Isso iniciará a aplicação localmente e fornecerá um link para abri-la no seu navegador.

## Como Usar

1. **Envie Arquivos**: Use o menu lateral para enviar um ou mais arquivos CSV contendo os dados da simulação.
2. **Veja os Resultados**: A área principal exibirá uma variedade de gráficos, mostrando distribuições de dados, métricas agregadas (média, desvio padrão e intervalos de confiança) e outras visualizações úteis.
3. **Explore os Dados**: Interaja com os gráficos para dar zoom, mover e obter visualizações detalhadas dos resultados da simulação.

## Exemplo

Aqui está um exemplo de como usar o aplicativo:

1. Inicie o aplicativo usando `streamlit run app.py`.
2. Envie seus arquivos CSV através do menu lateral.
3. A visualização principal será atualizada com gráficos baseados nos dados enviados.

## Requisitos

- Python 3.9+
