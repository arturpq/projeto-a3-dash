import pandas as pd
from datetime import datetime
import streamlit as st
from data_preparation import load_and_prepare_data
from chart_helpers import get_percent_data, plot_styled_bar, plot_styled_pie, plot_grouped_bar, get_cross_data
from constants import GENDER_COLORS, GENDER_HOVER_TEMPLATE

def render_tab_gender():

    df, df_age, df_gender = load_and_prepare_data()
    st.header("Análise por Idade")
    st.dataframe(df_gender)

    st.header("Análise Cruzada - Possíveis Interessados")
    st.markdown(
        "A seguir, gráficos de análise cruzada que detalham as respostas por **Gênero** para diferentes subgrupos (excluindo 'Prefiro não dizer')."
    )

    # DataFrame filtrado para gênero (exclui 'Prefiro não dizer')
    d = df_gender

    # --- 1. Gráfico 3º ano (high_school_year)
    st.subheader("Alunos do 3º Ano")
    col = "high_school_year"
    df_3rd_year = d[d[col] == "3º ano"].copy()
    
    gender_3rd_year_data = get_percent_data(df_3rd_year, "gender")
    pie_hover_template = "<b>Gênero:</b> %{label}<br><b>Participantes:</b> %{value}<br><b>Percentual:</b> %{percent}<extra></extra>"
    
    if not df_3rd_year.empty:
        fig = plot_styled_pie(
            df=gender_3rd_year_data,
            names_col="gender",
            values_col="count",
            colors_map=GENDER_COLORS,
            hover_template=pie_hover_template # Usamos o template personalizado
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma resposta encontrada para alunos do 3º ano (sem gênero não informado).")

    # --- 2. Faculdades (university_choice) - Pública vs. Privada
    st.subheader("Opção por Universidade (Pública/Privada)")
    col = "university_choice"
    # Filtrar apenas as respostas que mencionam 'Universidade Pública' ou 'Universidade Privada'
    df_uni = d[d[col].isin(["Pública", "Privada"])].copy()

    if not df_uni.empty:
        cross_data = get_cross_data(df_uni, category_col=col, gender_col="gender")
        fig = plot_grouped_bar(
            df=cross_data,
            category_col=col,
            gender_col="gender",
            x_title="Opção de Universidade",
            y_title="Participantes"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma resposta válida de 'Universidade Pública' ou 'Privada' (sem gênero não informado).")


    # --- 3. Gosta de jogos (likes_games)
    st.subheader("Gosta de Jogos Eletrônicos")
    col = "likes_games"
    cross_data = get_cross_data(d, category_col=col, gender_col="gender")
    fig = plot_grouped_bar(
        df=cross_data,
        category_col=col,
        gender_col="gender",
        x_title="Gosta de Jogos?",
        y_title="Participantes"
    )
    st.plotly_chart(fig, use_container_width=True)


    # --- 4. Possui Computador (has_pc)
    st.subheader("Possui Computador")
    col = "has_pc"
    cross_data = get_cross_data(d, category_col=col, gender_col="gender")
    fig = plot_grouped_bar(
        df=cross_data,
        category_col=col,
        gender_col="gender",
        x_title="Possui Computador?",
        y_title="Participantes"
    )
    st.plotly_chart(fig, use_container_width=True)


    # --- 5. Possui Celular (has_smartphone) e Dados Móveis (has_mobile_data)
    st.subheader("Possui Celular")
    col = "has_smartphone"
    cross_data = get_cross_data(d, category_col=col, gender_col="gender")
    fig = plot_grouped_bar(
        df=cross_data,
        category_col=col,
        gender_col="gender",
        x_title="Possui Celular?",
        y_title="Participantes"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Possui Dados Móveis")
    col = "has_mobile_data"
    cross_data = get_cross_data(d, category_col=col, gender_col="gender")
    fig = plot_grouped_bar(
        df=cross_data,
        category_col=col,
        gender_col="gender",
        x_title="Possui Dados Móveis?",
        y_title="Participantes"
    )
    st.plotly_chart(fig, use_container_width=True)


    # --- 6. Possui Videogame (has_console)
    st.subheader("Possui Videogame/Console")
    col = "has_console"
    cross_data = get_cross_data(d, category_col=col, gender_col="gender")
    fig = plot_grouped_bar(
        df=cross_data,
        category_col=col,
        gender_col="gender",
        x_title="Possui Videogame?",
        y_title="Participantes"
    )
    st.plotly_chart(fig, use_container_width=True)


    # --- 7. Perguntas sobre Interesse na Faculdade e Evento
    st.subheader("Avaliação e Interesse do Evento")
    interest_cols = [
        "q_explanations_clear", "q_apps_interesting",
        "q_tech_use_good", "q_helped_understand_cs",
        "q_overall_experience_positive"
    ]

    for col in interest_cols:
        if col not in d.columns:
            continue

        # Formatação do título
        title_map = {
            "q_explanations_clear": "Explicações Claras",
            "q_apps_interesting": "Aplicações Despertaram Interesse",
            "q_tech_use_good": "Uso de Tecnologia Adequado",
            "q_helped_understand_cs": "Ajudou a Entender Ciência da Computação",
            "q_overall_experience_positive": "Experiência Geral Positiva"
        }
        title = title_map.get(col, col.replace('q_', '').replace('_', ' ').title())

        st.markdown(f"**{title}**")
        cross_data = get_cross_data(d, category_col=col, gender_col="gender")

        fig = plot_grouped_bar(
            df=cross_data,
            category_col=col,
            gender_col="gender",
            x_title=title,
            y_title="Participantes"
        )
        st.plotly_chart(fig, use_container_width=True)