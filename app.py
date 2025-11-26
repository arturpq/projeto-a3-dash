import streamlit as st
import pandas as pd
import plotly.express as px

from tab_final import render_tab_final
from tab_geral import render_tab_geral
from tab_hs import render_tab_hs
from tab_inter import render_tab_inter

from data_preparation import load_and_prepare_data

st.set_page_config(page_title="Dashboard", layout="wide")


with st.sidebar:
    show_removed_data = st.toggle("Mostrar dados removidos")
    st.title("Sobre o Projeto")
    st.info(
        """
        Análise sobre as respostas da pesquisa de um evento sobre a área de tecnologia
        """
    )

    st.markdown("### Desenvolvido por:")
    st.markdown("**Artur de Lima Bezerra**")
    st.caption("Estudante de Ciência da Computação")
    
    st.markdown("[GitHub](https://github.com/arturpq)")
    
    st.markdown("---")
    st.caption("2025")

st.title("Análise de Respostas do Evento")

df, df_age, df_gender = load_and_prepare_data()

tab_geral, tab_inter, tab_hs, tab_final = st.tabs(["Análise Geral","Análise de Interesses", "Alunos Mais Prováveis", "Perfil do Participante"])

with tab_geral:
    
    render_tab_geral()

with tab_inter:

    render_tab_inter(show_removed_data)

with tab_hs:

    render_tab_hs(show_removed_data)

with tab_final:
    
    render_tab_final(show_removed_data)

