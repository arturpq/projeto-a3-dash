# tab_edu.py

import streamlit as st
import plotly.express as px

from chart_helpers import get_percent_data, get_standardized_interest_data, plot_styled_bar
from constants import DEFAULT_PLOT_LAYOUT, INTEREST_SCALE_COLORS, INTEREST_SCALE_ORDER
from data_preparation import df


def render_tab_inter():
    st.header("Distribuição do Nível de Interesse")
    st.markdown(
        "Gráficos mostram a distribuição dos participantes pela escala de interesse, **padronizada** de Nenhum (vermelho) a Muito (verde)."
    )

    interest_cols_map = {
        "interest_math": "Matemática",
        "interest_portuguese": "Português",
        "interest_logic_math": "Lógica e Matemática", # Usando a coluna existente
        "interest_tech_innovation": "Tecnologia e Inovação"
    }
    
    # Lista de colunas para garantir a ordem
    cols_to_plot = list(interest_cols_map.keys())

    # Usamos colunas para posicionar os gráficos
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    containers = [c1, c2, c3, c4]


    for i, col in enumerate(cols_to_plot):
        if col not in df.columns:
            containers[i].warning(f"Coluna '{col}' não encontrada.")
            continue

        with containers[i]:
            title = interest_cols_map[col]
            st.subheader(title)

            # 1. Padroniza os dados
            dist_data = get_standardized_interest_data(df, col, INTEREST_SCALE_ORDER)

            # 2. Cria o gráfico de barras vertical
            fig = px.bar(
                dist_data,
                x=col,
                y="count",
                # Cor por categoria
                color=col,
                color_discrete_map=INTEREST_SCALE_COLORS, 
                labels={
                    col: "Nível de Interesse",
                    "count": "Participantes"
                },
                custom_data=["percentage"],
                orientation="v"
            )

            # Define a ordem correta no eixo X
            fig.update_xaxes(categoryorder="array", categoryarray=INTEREST_SCALE_ORDER)

            # Aplica o estilo de hover e layout padrão
            fig.update_traces(
                hovertemplate=(
                    f"<b>{title}:</b> %{{x}}<br>"
                    "<b>Participantes:</b> %{y}<br>"
                    "<b>Percentual:</b> %{customdata[0]:.2f}%<extra></extra>"
                )
            )
            fig.update_layout(
                **DEFAULT_PLOT_LAYOUT,
                showlegend=False, # Oculta a legenda pois a cor é a própria categoria no eixo X
                title_text=""
            )

            st.plotly_chart(fig, use_container_width=True)