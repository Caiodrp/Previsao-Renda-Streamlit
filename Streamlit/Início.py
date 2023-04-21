import pandas as pd
import pandas as pd
import numpy as np
import streamlit as st

# Definir o template
st.set_page_config(page_title='Previsão de Renda',
                page_icon='💰',
                layout='wide')

# Título centralizado
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<h1 style="font-size:4.5rem;">PREVISÃO DE RENDA</h1>'
    '</div>',
    unsafe_allow_html=True
)

# Subtítulo
st.write(
    '<div style="display:flex; align-items:center; justify-content:center;">'
    '<h2 style="font-size:2.5rem;">Um modelo de Machine Learning para prever renda</h2>'
    '</div>',
    unsafe_allow_html=True
)

# Divisão
st.write("---")

# Imagem do lado da explicação
st.write(
    '<div style="display:flex; align-items:center; justify-content:space-between;">'
    "<p style='font-size:1.5rem;'> Esse aplicativo é uma ferramenta de IA que, "
    "utilizando análises de dados, automatiza o entendimento de o quão a renda de uma pessoa está associada a "
    "características pessoais. Através de um modelo de "
    "<strong>Machine Learning</strong>, ele utiliza técnicas de "
    "<strong>regressão</strong> para prever a renda de um novo usuário com "
    "novos dados apresentados.</p>"
    '<img src="https://media.tenor.com/aIvGbxyqS4AAAAAd/bender-money.gif" width="400" animated>'
    '</div>',
    unsafe_allow_html=True
)

# Divisão
st.write("---")

st.write(
    '<h3 style="text-align:left;">Autor</h3>'
    '<ul style="list-style-type: disc; margin-left: 20px;">'
    '<li>Caio Douglas Rodrigues de Paula</li>'
    '<li><a href="https://github.com/Caiodrp/previsao-renda-streamlit">GitHub</a></li>'
    '</ul>',
    unsafe_allow_html=True
)

