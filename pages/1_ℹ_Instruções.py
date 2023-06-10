import pandas as pd
import pandas as pd
import numpy as np
import streamlit as st
import base64
import requests

# Definir o template
st.set_page_config(page_title='Previsão de Renda',
                page_icon='💰',
                layout='wide')

# Título centralizado
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<h1 style="font-size:4.5rem;">Instruções</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Divisão
st.write("---")

# Adicionando texto antes do vídeo
st.write("Este é um tutorial em vídeo sobre como usar a aplicação")

# Adicionando vídeo
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<iframe width="800" height="500" src="https://www.youtube.com/embed/UQvP8m5AGdU" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
    '</div>',
    unsafe_allow_html=True
)

# Arquivo csv modelo 
st.write('# Modelo do arquivo CSV')
st.write('O arquivo a ser usado deve ter o nome e ordem das colunas identicos a do modelo')
url = "https://raw.githubusercontent.com/Caiodrp/previsao-renda-streamlit/main/CSV/previsao_de_renda.csv" 

# Função para baixar o arquivo
@st.cache_data(ttl=86400)
def download_file(url):
    response = requests.get(url)
    b64 = base64.b64encode(response.content).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="previsao_de_renda.csv">Baixar arquivo</a>'

# Adicionando botão para download
st.markdown(download_file(url), unsafe_allow_html=True)

# Imagem do dicionário de dados
st.image("https://raw.githubusercontent.com/Caiodrp/previsao-renda-streamlit/main/CSV/Dicion%C3%A1rio%20de%20Dados.png")

# Adicionando texto
st.write(
    """
    # Análises

    Na página "Análises", você pode visualizar diferentes gráficos e informações sobre o seu conjunto de dados. 

    ### Data Frame

    A primeira opção de gráficos disponíveis é a "Data Frame", que exibe as primeiras linhas do seu conjunto de dados. Você pode escolher o número de linhas a serem exibidas com o slider na barra lateral.

    ### Matriz de Correlação

    A segunda opção de gráficos é a "Matriz de Correlação", que exibe a relação entre todas as variáveis do seu conjunto de dados. 

    ### Renda ao longo do tempo

    A terceira opção de gráficos é a "Renda ao longo do tempo", que exibe a média da renda ao longo do tempo para diferentes variáveis. Você pode escolher as variáveis a serem exibidas na barra lateral.

    ### Renda x Variáveis

    A quarta opção de gráficos disponíveis é a "Renda x Variáveis", que exibe a relação entre a renda e outras variáveis. Você pode escolher o tipo de variáveis a serem exibidas na barra lateral.

    # Prever Renda

    Na página "Prever Renda", você pode fazer previsões de renda para novos dados. Para isso, você precisa preencher os campos na barra lateral ou carregar um arquivo CSV com novos dados(no modelo do arquivo de exemplo a cima), e clicar em "Prever Renda".  

    __*As variáveis de tempo(idade e tempo de emprego), devem ser preenchidas em anos.__

    """
)