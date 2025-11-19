# tab_tec.py - MODIFICADO para análise geral (univariada)

import streamlit as st
from chart_helpers import get_percent_data, plot_styled_bar
from data_preparation import df as d
def render_tab_tec(): # Agora aceita o DataFrame completo (df)
    """
    Renderiza os gráficos relacionados a tecnologia, dispositivos e avaliação do evento
    de forma geral (univariada).
    """
    st.title("Análise de Tecnologia e Avaliação do Evento")
    st.markdown(
        "Esta seção apresenta a distribuição geral de respostas para variáveis de tecnologia, acesso e feedback do evento."
    )

    # ============================================================
    # 1 — ACESSO E INTERESSE EM TECNOLOGIA
    # ============================================================
    st.markdown("---")
    st.header("Acesso à Tecnologia e Experiência")

    tech_interest_cols = ["interest_tech_innovation", "interest_logic_math", "programming_experience"]
    
    for col in tech_interest_cols:
        if col not in d.columns:
            continue

        title_map = {
            "interest_tech_innovation": "Interesse em Tecnologia e Inovação",
            "interest_logic_math": "Interesse em Desafios Lógicos/Matemáticos",
            "programming_experience": "Experiência com Programação"
        }
        title = title_map.get(col, col.replace('_', ' ').title())

        st.subheader(title)
        dist_data = get_percent_data(d, col) # Dados de distribuição
        
        # Gráfico de barras simples
        fig = plot_styled_bar(
            df=dist_data,
            x_col=col,
            y_col="count",
            x_title=title,
            y_title="Participantes",
            orientation="h" # Horizontal para categorias
        )
        st.plotly_chart(fig, use_container_width=True)


    # ============================================================
    # 2 — POSSE DE DISPOSITIVOS
    # ============================================================
    st.markdown("---")
    st.header("Posse de Dispositivos (Hardwares)")

    device_cols = ["has_pc", "has_home_wifi", "has_console", "likes_games"]

    c1, c2 = st.columns(2)
    
    for i, col in enumerate(device_cols):
        if col not in d.columns:
            continue
        
        container = c1 if i % 2 == 0 else c2

        with container:
            title_map = {
                "has_pc": "Possui Computador",
                "has_home_wifi": "Possui Wi-Fi Residencial",
                "has_console": "Possui Videogame/Console",
                "likes_games": "Gosta de Jogos Eletrônicos"
            }
            title = title_map.get(col, col.replace('_', ' ').title())

            st.markdown(f"**{title}**")
            dist_data = get_percent_data(d, col) # Dados de distribuição

            # Gráfico de barras simples
            fig = plot_styled_bar(
                df=dist_data,
                x_col=col,
                y_col="count",
                x_title=title,
                y_title="Participantes",
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)


    # ============================================================
    # 3 — AVALIAÇÃO DO EVENTO (LIKERT)
    # ============================================================
    st.markdown("---")
    st.header("Avaliação do Evento")
    st.markdown("As perguntas de avaliação mostram o nível de concordância geral.")
    
    evaluation_cols = [
        "q_explanations_clear", "q_apps_interesting",
        "q_tech_use_good", "q_helped_understand_cs",
        "q_overall_experience_positive"
    ]
    
    for col in evaluation_cols:
        if col not in d.columns:
            continue
        
        title_map = {
            "q_explanations_clear": "Explicações Claras",
            "q_apps_interesting": "Aplicações Despertaram Interesse",
            "q_tech_use_good": "Uso de Tecnologia Adequado",
            "q_helped_understand_cs": "Ajudou a Entender Ciência da Computação",
            "q_overall_experience_positive": "Experiência Geral Positiva"
        }
        title = title_map.get(col, col.replace('q_', '').replace('_', ' ').title())

        st.subheader(title)
        
        dist_data = get_percent_data(d, col) # Dados de distribuição

        # Gráfico de barras simples
        fig = plot_styled_bar(
            df=dist_data,
            x_col=col,
            y_col="count",
            x_title="Nível de Concordância",
            y_title="Participantes",
            orientation="v" # Vertical é melhor para escalas Likert
        )
        st.plotly_chart(fig, use_container_width=True)