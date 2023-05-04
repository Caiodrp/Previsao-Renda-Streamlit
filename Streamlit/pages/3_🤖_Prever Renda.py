import pandas as pd
import seaborn as sn
import numpy as np
import streamlit as st
import joblib

from joblib import load
from sklearn.tree import DecisionTreeRegressor

# Definir o template
st.set_page_config(page_title='Previsão de Renda',
                page_icon='💰',
                layout='wide')

# Título centralizado
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<h1 style="font-size:4.5rem;">Prever Renda</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Divisão
st.write("---")

#Carregando o modelo treinado da árvore de regressão
model = joblib.load('tree_reg.pkl')

# Opções na sidebar
st.sidebar.subheader("Opções")
opcao = st.sidebar.selectbox("Escolha como inserir os dados", ["Carregar CSV", "Inserir manualmente"])

if opcao == "Carregar CSV":
    # Função para carregar um CSV
    @st.cache
    def carregar_CSV():  
        # Widget para upload do arquivo CSV
        file = st.sidebar.file_uploader("Carregue um arquivo CSV", type=["csv"])
        if file is not None:
            # Lendo o arquivo CSV
            df_csv = pd.read_csv(file)
            # Exibindo o DataFrame carregado
            st.write("Dados carregados do arquivo CSV:")
            st.dataframe(df_csv)
            #Criando o botão para prever a renda
            if st.button("PREVER RENDA"):
                # Realizando as previsões para os dados carregados do CSV
                y_pred = model.predict(df_csv)
                # Exibindo as previsões
                st.write("Previsões de renda:")
                st.write(y_pred)
        else:
            st.warning("Por favor, carregue um arquivo CSV.")

else:
    # Define as opções para inserção manual de dados
    options = {
        'sexo': ['F', 'M'],
        'posse de veiculo': ['Não', 'Sim'],
        'posse de imovel': ['Não', 'Sim'],
        'tipo de renda': ['Assalariado', 'Empresário', 'Pensionista', 'Servidor público'],
        'educacao': ['Primário', 'Secundário', 'Superior completo', 'Superior incompleto'],
        'estado civil': ['Casado', 'Separado', 'Solteiro', 'União', 'Viúvo'],
        'tipo de residencia': ['Aluguel', 'Casa', 'Com os pais', 'Comunitário', 'Governamental']
    }

    # widgets para os usuários iserirem os dados
    idade = st.sidebar.number_input('Idade:', step=1)
    tempo_emprego = st.sidebar.number_input('Tempo de emprego:', step=1)
    qt_pessoas_residencia = st.sidebar.number_input('Quantidade de pessoas na residência:', step=1)
    qtd_filhos = st.sidebar.number_input('Quantidade de filhos:', step=1)
    values = {key: st.sidebar.selectbox(key, val) for key, val in options.items()}

    # Cria o DataFrame com as respostas do usuário
    binary_map = {'Não': 0, 'Sim': 1}
    df_manual = pd.DataFrame({
    'posse_de_veiculo': [binary_map[values['posse de veiculo']]],
    'posse_de_imovel': [binary_map[values['posse de imovel']]],
    'qtd_filhos': [qtd_filhos],
    'idade': [idade],
    'tempo_emprego': [tempo_emprego],
    'qt_pessoas_residencia': [qt_pessoas_residencia],
    'sexo_F': [1 if values['sexo'] == 'F' else 0],
    'sexo_M': [1 if values['sexo'] == 'M' else 0],
    'tipo_renda_Assalariado': [1 if values['tipo de renda'] == 'Assalariado' else 0],
    'tipo_renda_Empresário': [1 if values['tipo de renda'] == 'Empresário' else 0],
    'tipo_renda_Pensionista': [1 if values['tipo de renda'] == 'Pensionista' else 0],
    'tipo_renda_Servidor_público': [1 if values['tipo de renda'] == 'Servidor público' else 0],
    'educacao_Primário': [1 if values['educacao'] == 'Primário' else 0],
    'educacao_Secundário': [1 if values['educacao'] == 'Secundário' else 0],
    'educacao_Superior_completo': [1 if values['educacao'] == 'Superior completo' else 0],
    'educacao_Superior incompleto': [1 if values['educacao'] == 'Superior incompleto' else 0],
    'estado_civil_Casado': [1 if values['estado civil'] == 'Casado' else 0],
    'estado_civil_Separado': [1 if values['estado civil'] == 'Separado' else 0],
    'estado_civil_Solteiro': [1 if values['estado civil'] == 'Solteiro' else 0],
    'estado_civil_União': [1 if values['estado civil'] == 'União' else 0],
    'estado_civil_Viúvo': [1 if values['estado civil'] == 'Viúvo' else 0],
    'tipo_residencia_Aluguel': [1 if values['tipo de residencia'] == 'Aluguel' else 0],
    'tipo_residencia_Casa': [1 if values['tipo de residencia'] == 'Casa' else 0],
    'tipo_residencia_Com os pais': [1 if values['tipo de residencia'] == 'Com os pais' else 0],
    'tipo_residencia_Comunitário': [1 if values['tipo de residencia'] == 'Comunitário' else 0],
    'tipo_residencia_Governamental': [1 if values['tipo de residencia'] == 'Governamental' else 0]
    })

    # Criando o botão para prever a renda
    if st.button("PREVER RENDA"):
        # Realizando as previsões para os dados do usuário
        renda_prevista = model.predict(df_manual)
        # Exibindo as previsões
        st.write("Previsão de renda:", "{:.2f}".format(float(np.ravel(renda_prevista)[0])).replace('.', ','))
