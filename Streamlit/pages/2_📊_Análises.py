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

# Widget de input de arquivo Excel na barra lateral
uploaded_file = st.sidebar.file_uploader(
    label="Faça upload do arquivo CSV",
    type=["csv"]
)

# Carregar dados do arquivo Excel em um DataFrame pandas
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Transformando a variável 'data_ref' em mes/ano para legenda
    df["data_ref"] = pd.to_datetime(df["data_ref"])
    tick_labs = df['data_ref'].map(lambda ts: ts.strftime("%m-%Y")).unique()
else:
    st.warning("Por favor, faça upload de um arquivo .CSV para continuar.")

# Adicionar opções de seleção na barra lateral
selecao_opcoes = st.sidebar.selectbox(
    "Selecione uma opção",
    ("Data Frame", "Matriz de Correlação", "Renda ao longo do tempo", "Renda x Variáveis")
)

# Widget de exibição do DataFrame
if selecao_opcoes == "Data Frame":
    if 'df' not in locals():
        df = None
    # Widget de slider para ajustar o número de linhas exibidas
    if df is not None:
        num_rows = st.sidebar.slider(
            "Selecione o número de linhas a serem exibidas",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1
        )
        st.write(df.head(num_rows))

# Widget de exibição da matriz de correlação
if selecao_opcoes == "Matriz de Correlação":
    if 'df' not in locals():
        st.warning("Por favor, faça upload de um arquivo para continuar.")
    else:
        sns.clustermap(
            data=df.corr(),
            figsize=(10, 10),
            center=0,
            cmap=sns.diverging_palette(h_neg=350, h_pos=125, as_cmap=True, sep=1, center='light')
        )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        plt.close()

# Widget de exibição da renda ao longo do tempo por variável
if selecao_opcoes == "Renda ao longo do tempo":
    if 'df' not in locals():
        st.warning("Por favor, faça upload de um arquivo para continuar.")
    else:
        # Adicionar widget de seleção para escolher variáveis
        variaveis_selecionadas = st.sidebar.multiselect(
            "Selecione as variáveis para visualizar",
            ('sexo', 'posse_de_veiculo', 'posse_de_imovel', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia')
        )

        # Loop para plotagem das figuras
        for var in variaveis_selecionadas:
            plt.figure(figsize=(10, 6))
            sns.pointplot(x="data_ref", y="renda", hue=var, data=df, dodge=True, ci=95)
            plt.xticks(list(range(df['data_ref'].nunique())), tick_labs, rotation=90)
            #plt.legend(loc='lower center', bbox_to_anchor=(0.5, -.50), ncol=3)
            plt.title(f'Média da renda ao longo do tempo por {var}')
            plt.subplots_adjust(hspace=0.7)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            plt.close()

# Widget de exibição da renda ao longo do tempo por variável
if selecao_opcoes == "Renda x Variáveis":
    if 'df' not in locals():
        st.warning("Por favor, faça upload de um arquivo para continuar.")
    else:
        # Widget para escolher entre variáveis numéricas e categóricas
        tipo_variavel = st.sidebar.selectbox("Selecione o tipo de variável", ["Categóricas", "Numéricas"])

        # Filtrando as variáveis categóricas e numéricas
        var_cat = ['sexo', 'posse_de_veiculo', 'posse_de_imovel', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia']
        var_num = ['idade', 'tempo_emprego']

        # Widget para selecionar as variáveis
        if tipo_variavel == "Categóricas":
            var_selecionadas = st.sidebar.multiselect("Selecione as variáveis categóricas", var_cat)
            # Gráfico de média de renda para cada categoria das variáveis categóricas
            for var in var_selecionadas:
                    df_cat = df.groupby(var, as_index=False)['renda'].mean()
                    plt.figure(figsize=(10,6))
                    ax = sns.barplot(x=var, y='renda', data=df_cat)
                    ax.set_title(f'{var.capitalize()} x Renda Média')
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    st.pyplot()
                    plt.close()

        else:
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


