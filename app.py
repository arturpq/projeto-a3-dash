import streamlit as st
import pandas as pd
import plotly.express as px

from tab_geral import render_tab_geral
from tab_inter import render_tab_inter
from tab_rec import render_tab_rec
from tab_gender import render_tab_gender

from data_preparation import load_and_prepare_data
from constants import GENDER_COLORS, GENDER_HOVER_TEMPLATE

# Config
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Análise de Respostas do Evento")

# Dados
df, df_age, df_gender = load_and_prepare_data()

# Abas
tab_geral, tab_inter,  tab_rec, tab_gender, tab_age, tab_atributos = st.tabs(["Análise Geral","Análise de Interesses", "Análise de Recursos", "Análise de Gênero", "Análise de Idade", "Visão Geral"])

# ============================================================
# 1 — GERAL
# ============================================================
with tab_geral:
    
    render_tab_geral()
# ============================================================
# ABA 2 — IDADE
# ============================================================
with tab_inter:

    render_tab_inter()

with tab_rec:

    render_tab_rec()


with tab_gender:
    
    render_tab_gender()

with tab_age:
    st.header("Análise por Gênero")
    st.dataframe(df_gender)

    st.header("Análise Cruzada por Gênero")

with tab_atributos:

    st.header("Atributos Gerais da Base Completa")
