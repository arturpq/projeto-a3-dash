# tab_tec.py - MODIFICADO para análise geral (univariada)

import streamlit as st
import plotly.express as px

from chart_helpers import get_percent_data, get_standardized_interest_data, plot_styled_bar
from constants import DEFAULT_PLOT_LAYOUT, YES_NO
from data_preparation import df_final as d

def render_tab_rec(): # Agora aceita o DataFrame completo (df)
    rec_cols_map = {
        'has_console': 'Tem Videogame (Console)?',
        'has_pc': 'Tem Computador?',
        'has_smartphone': 'Tem Celular?',
        'has_home_wifi': 'Tem Internet Residencial (Wi-Fi)?',
        'has_mobile_data': 'Tem Internet no Celular?'
    }
    
    cols_to_plot = list(rec_cols_map.keys())

    dist_data = get_standardized_interest_data(d, col, YES_NO)

    c1, c2, c3 = st.columns(3)
    c4, c5 = st.columns(2)
    containers = [c1, c2, c3]

    for i, col in enumerate(cols_to_plot):
        with containers[i]:
            title = rec_cols_map[col]
            st.subheader(title)
            fig = px.bar(
                d,
                x=col,
                y="count",
                color=col,
                color_discrete_map=YES_NO, 
                labels={
                    col: "Nível de Interesse",
                    "count": "Participantes"
                },
                custom_data=["percentage"]
            )
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
