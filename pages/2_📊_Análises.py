import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import streamlit as st

# Definir o template
st.set_page_config(page_title='Previsão de Renda',
                page_icon='💰',
                layout='wide')

# Título centralizado
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<h1 style="font-size:4.5rem;">Análises</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Divisão
st.write("---")

# carregando o CSV
uploaded_file = st.sidebar.file_uploader(
    label="Faça upload do arquivo CSV",
    type=["csv"]
)

if uploaded_file is not None:
    # Função para transformar em Data Frame
    @st.cache_data 
    def load_data():
        df = pd.read_csv(uploaded_file)
        df["data_ref"] = pd.to_datetime(df["data_ref"])
        return df

    df = load_data()
    st.write("Dados Carregados")

    #Função para gerenciar o Data Frame
    @st.cache_data(experimental_allow_widgets=True)
    def show_data(df):
        # Widget de slider para ajustar o número de linhas exibidas
        num_rows = st.sidebar.slider(
            "Selecione o número de linhas a serem exibidas",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1
        )
        # Exibe o DataFrame com o número de linhas selecionado
        st.write(df.head(num_rows))

    #Função para a opção da Matriz de Correlação
    @st.cache_data
    def exibir_matriz_correlacao(df):
        sns.clustermap(
        data=df.corr(),
        figsize=(10, 10),
        center=0,
        cmap=sns.diverging_palette(h_neg=350, h_pos=125, as_cmap=True, sep=1, center='light')
        )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        plt.close()

    #Função para a opção Renda ao longo do tempo
    @st.cache_data(experimental_allow_widgets=True)
    def exibir_renda_ao_longo_tempo(df):
        # Adicionar widget de seleção para escolher variáveis
        variaveis_selecionadas = st.sidebar.multiselect(
        "Selecione as variáveis para visualizar",
        ('sexo', 'posse_de_veiculo', 'posse_de_imovel', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia')
    )
        #Função lambda que transforma as datas para mês e ano apenas
        tick_labs = df['data_ref'].map(lambda ts: ts.strftime("%m-%Y")).unique()

        # Loop para plotagem das figuras
        for var in variaveis_selecionadas:
            plt.figure(figsize=(10, 6))
            sns.pointplot(x="data_ref", y="renda", hue=var, data=df, dodge=True, ci=95)
            plt.xticks(list(range(df['data_ref'].nunique())), tick_labs, rotation=90)
            plt.title(f'Média da renda ao longo do tempo por {var}')
            plt.subplots_adjust(hspace=0.7)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            plt.close()

    #Função para a opção Renda x Variável
    @st.cache_data(experimental_allow_widgets=True)
    def exibir_renda_x_variaveis(df):
        # Widget para escolher entre variáveis numéricas e categóricas
        tipo_variavel = st.sidebar.selectbox("Selecione o tipo de variável", ["Categóricas", "Numéricas"])

        # Widget para selecionar as variáveis
        if tipo_variavel == "Categóricas":
            # Filtrando as variáveis categóricas e numéricas
            var_cat = ['sexo', 'posse_de_veiculo', 'posse_de_imovel', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia']
            var_selecionadas = st.sidebar.multiselect("Selecione as variáveis categóricas", var_cat)
            for var in var_selecionadas:
                df_cat = df.groupby(var, as_index=False)['renda'].mean()
                plt.figure(figsize=(10,6))
                ax = sns.barplot(x=var, y='renda', data=df_cat)
                ax.set_title(f'{var.capitalize()} x Renda Média')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
                plt.close()

        var_num = ['idade', 'tempo_emprego']

        var_selecionadas = st.sidebar.multiselect("Selecione as variáveis numéricas", var_num)
        # Gráfico de média x Renda das variáveis numéricas
        for var in var_selecionadas:
            plt.figure(figsize=(10,6))
            ax = sns.lineplot(x=var, y='renda', data=df, ci=None, estimator='mean')
            ax.set_title(f'{var.capitalize()} x Renda Média')
            plt.ylim(0, 11000)
            plt.yticks(np.arange(0, 11000, step=2500))
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            plt.close()

    # Adicionar opções de seleção na barra lateral
    selecao_opcoes = st.sidebar.selectbox(
        "Selecione uma opção",
        ("Data Frame", "Matriz de Correlação", "Renda ao longo do tempo", "Renda x Variáveis")
        )

    # Verifica se o DataFrame está presente
    if selecao_opcoes == "Data Frame":
            num_rows = st.sidebar.slider(
            "Selecione o número de linhas a serem exibidas",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1
            )
            # Exibe o DataFrame com o número de linhas selecionado
            st.write(df.head(num_rows))

    elif selecao_opcoes == "Matriz de Correlação":
            exibir_matriz_correlacao(df)

    elif selecao_opcoes == "Renda ao longo do tempo":
            exibir_renda_ao_longo_tempo(df)

    else:
            exibir_renda_x_variaveis(df)

#Caso o usuário não carregue o arquivo
else:
    st.warning("Por favor, carregue um arquivo CSV.")





