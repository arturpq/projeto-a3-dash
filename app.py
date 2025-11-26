import streamlit as st
import pandas as pd
import plotly.express as px

from tab_geral import render_tab_geral
from tab_hs import render_tab_hs
from tab_inter import render_tab_inter

from data_preparation import load_and_prepare_data
from constants import GENDER_COLORS, GENDER_HOVER_TEMPLATE

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Análise de Respostas do Evento")

df, df_age, df_gender = load_and_prepare_data()

tab_geral, tab_inter, tab_hs = st.tabs(["Análise Geral","Análise de Interesses", "Alunos Mais Prováveis"])

with tab_geral:
    
    render_tab_geral()

with tab_inter:

    render_tab_inter()

with tab_hs:

    render_tab_hs()
