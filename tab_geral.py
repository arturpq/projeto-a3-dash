import pandas as pd
from datetime import datetime
import streamlit as st
from data_preparation import load_and_prepare_data
from chart_helpers import get_percent_data, plot_styled_bar, plot_styled_pie
from constants import HIGHSCHOOL_YEAR, GENDER_COLORS, GENDER_HOVER_TEMPLATE, YES_NO, UNIVERSITY_COLORS


def render_tab_geral():
    df, df_age, df_gender = load_and_prepare_data()
    col1, col2 = st.columns(2)

    # KPIs
    with col1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(df))
        c2.metric("Idades inválidas", (df["age"] == 0).sum())
        c3.metric("Gênero não informado", (df["gender"] == "Prefiro não dizer").sum())

    with col2:
        _, cm, _ = st.columns([1, 1, 1])
        cm.metric("Idade média", f"{df_age['age'].mean():.1f}")

    st.markdown("---")
    st.header("Gênero e Idade")

    col_g1, col_g2 = st.columns(2)

    # -------- Pizza gênero --------
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

    # ------- Barra idade --------
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
    st.write("A análise dos dados revelou a ausência dos valores de idade para 7 participantes da pesquisa e a não resposta sobre o gênero por 1 participante.")
    st.write("Devido à semelhança entre as idades registradas, optou-se por manter os registros com idade ausente, excluindo a variável idade da análise aprofundada. O registro com informação de gênero ausente foi removido do dataset para garantir a integridade da análise dessa variável.")
    st.markdown("---")
    st.header("Ensino Médio e Universidade")

    col_hs, col_uni ,col_uni2 = st.columns(3)

    # -------- Ensino médio --------
    with col_hs:
        st.subheader("Ano do Ensino Médio")
        hs = get_percent_data(df_gender, "high_school_year")
        fig = plot_styled_bar(
            df=hs,
            x_col="high_school_year",
            y_col="count",
            x_title="Ano",
            y_title="Participantes",
            color_discrete_map=HIGHSCHOOL_YEAR
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------- Universidade --------
    with col_uni:
        st.subheader("Planeja Fazer Faculdade?")
        plans_uni_data = get_percent_data(df_gender, "plans_university")
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
        uni = get_percent_data(df_gender, "university_choice")
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
    st.write("Por não refletir o público-alvo da pesquisa, sendo um outlier e um valor indesejado, este registro foi removido do dataset.")