import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit as st
from data_preparation import load_and_prepare_data
from chart_helpers import get_percent_data, normalize_subject, plot_styled_bar, plot_styled_pie
from constants import DEFAULT_PLOT_LAYOUT, HIGHSCHOOL_YEAR, GENDER_COLORS, GENDER_HOVER_TEMPLATE, YES_NO, UNIVERSITY_COLORS
from resources import render_rec


def render_tab_geral():
    df, df_age, df_gender = load_and_prepare_data()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(df))
    c2.metric("Idades inválidas", (df["age"] == 0).sum())
    c3.metric("Gênero não informado", (df["gender"] == "Prefiro não dizer").sum())

    

    st.markdown("---")
    st.header("Gênero e Idade")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Distribuição por gênero")

        include_missing = st.toggle("Incluir 'Prefiro não dizer'")
        d = df if include_missing else df_gender

        g_data = d["gender"].value_counts().reset_index()
        g_data.columns = ["gender", "count"]


        fig = plot_styled_pie(
            df=g_data,
            names_col="gender",
            values_col="count",
            colors_map=GENDER_COLORS,
            hover_template=GENDER_HOVER_TEMPLATE
        )
        st.plotly_chart(fig, use_container_width=True)
        c1g, c2g, c3g = st.columns(3)
        c1g.metric("Homens", len(d[d["gender"] == "Homem"] =="Homem"))
        c2g.metric("Mulheres", len(d[d["gender"] == "Mulher"] == "Mulher"))
        c3g.metric("Não Binário", len(d[d["gender"] == "Não binário"] == "Não binário"))
        c4g, c5g, c6g = st.columns(3)
        c5g.metric("Não Respondeu", len(d[d["gender"] == "Prefiro não dizer"] == "Prefiro não dizer"))

    with col_g2:
        st.subheader("Distribuição por Idade")

        include_invalid = st.toggle("Incluir idades inválidas")
        d = df if include_invalid else df_age

        age_data = get_percent_data(d, "age").sort_values("age")

        fig = plot_styled_bar(
            df=age_data,
            x_col="age",
            y_col="count",
            x_title="Participantes",
            y_title="Idade",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        c1i, c2i, c3i = st.columns(3)
        c4i, c5i = st.columns(2)
        mean_age = d['age'].mean()
        median_age = d['age'].median()
        mode_age = d['age'].mode().iloc[0] if not df_age['age'].mode().empty else None
        variance_age = d['age'].var()
        std_dev_age = d['age'].std()
        
        c1i.metric(
            label="Média", 
            value=f"{mean_age:.2f} anos"
        )
        
        c2i.metric(
            label="Mediana", 
            value=f"{median_age:.1f} anos"
        )
        
        c3i.metric(
            label="Moda", 
            value=f"{mode_age:.0f} anos" if mode_age is not None else "N/A"
        )
        c4i.metric(
            label="Variância", 
            value=f"{variance_age:.2f}"
        )
        
        c5i.metric(
            label="Desvio Padrão", 
            value=f"{std_dev_age:.2f}"
        )

    st.write("A análise dos dados revelou a ausência dos valores de idade para 7 participantes da pesquisa e a não resposta sobre o gênero por 1 participante.")
    st.write("Devido à semelhança entre as idades registradas e 7 valores invalidos, optou-se por não fazer uma analise aprofundada utilizando a idade como base.")
    st.markdown("---")
    st.header("Ensino Médio e Universidade")

    col_hs, col_uni ,col_uni2 = st.columns(3)

    with col_hs:
        st.subheader("Ano do Ensino Médio")
        hs = get_percent_data(df, "high_school_year")
        fig = plot_styled_bar(
            df=hs,
            x_col="high_school_year",
            y_col="count",
            x_title="Ano",
            y_title="Participantes",
            color_discrete_map=HIGHSCHOOL_YEAR
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_uni:
        st.subheader("Planeja Fazer Faculdade?")
        plans_uni_data = get_percent_data(df, "plans_university")
        fig = plot_styled_bar(
            df=plans_uni_data,
            x_col="plans_university",
            y_col="count",
            x_title="Resposta",
            y_title="Participantes",
            color_discrete_map=YES_NO
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_uni2:
        st.subheader("Tipo de Faculdade")
        uni = get_percent_data(df, "university_choice")
        fig = plot_styled_bar(
            df=uni,
            x_col="university_choice",
            y_col="count",
            x_title="Quantidade",
            y_title="Faculdade",
            color_discrete_map=UNIVERSITY_COLORS
        )
        st.plotly_chart(fig, use_container_width=True)
    st.write("A análise da intenção de cursar faculdade revelou a existência de apenas um participante que não planeja ingressar no ensino superior")
    st.write("Por não refletir o público-alvo da pesquisa, sendo um outlier e um valor indesejado, este registro foi removido de futuras análises")
    
    render_rec()

