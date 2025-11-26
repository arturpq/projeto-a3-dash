
import streamlit as st
import plotly.express as px
import pandas as pd 

from chart_helpers import get_percent_data
from constants import DEFAULT_PLOT_LAYOUT, YES_NO 

from data_preparation import df_final as d_clean
from data_preparation import df as d
YES_NO_ORDER = list(YES_NO.keys()) 


def render_rec(): 
    st.header("Análise de Recursos")
    
    use_clean_data = st.checkbox(
        "Usar todos os dados", 
        value=False
    )
    
    df = d if use_clean_data else d_clean

    rec_cols_map = {
        'has_console': 'Tem Videogame (Console)?',
        'has_pc': 'Tem Computador?',
        'has_smartphone': 'Tem Celular?',
        'has_home_wifi': 'Tem Internet Residencial (Wi-Fi)?',
        'has_mobile_data': 'Tem Internet no Celular?'
    }
    
    cols_to_plot = list(rec_cols_map.keys())

    c1, c2, c3 = st.columns(3)
    c4, c5 = st.columns(2)
    containers = [c1, c2, c3, c4, c5]

    col_index = 0 
    
    for col in cols_to_plot:
        
        container = containers[col_index]

        with container:
            dist_data = get_percent_data(df, col)

            dist_data[col] = pd.Categorical(dist_data[col], categories=YES_NO_ORDER, ordered=True)
            dist_data = dist_data.sort_values(col)
            
            title = rec_cols_map[col]
            st.subheader(title)

            fig = px.bar(
                dist_data, 
                x=col, 
                y="count", 
                color=col, 
                color_discrete_map=YES_NO, 
                labels={
                    col: title, 
                    "count": "Participantes"
                },
                custom_data=["percentage"],
                orientation="v"
            )

            fig.update_traces(
                hovertemplate=(
                    f"<b>{title}:</b> %{{x}}<br>" 
                    f"<b>Participantes:</b> %{{y}}<br>"
                    "<b>Percentual:</b> %{customdata[0]:.2f}%<extra></extra>"
                )
            )

            fig.update_layout(
                **DEFAULT_PLOT_LAYOUT,
                showlegend=False, 
                title_text=""
            )

            st.plotly_chart(fig, width='stretch', key=f"rec_bar_{col}")
            
        col_index += 1
    
    st.markdown("---")
    st.header("Jogos e Programação")
    st.markdown("Análise rápida sobre o perfil dos participantes em relação a jogos e contato prévio com programação.")

    col_prog, col_games = st.columns(2)

    with col_prog:
        st.subheader("Conhecimento em Programação")
        
        prog_col = 'programming_experience'
        
        if prog_col in df.columns:
            prog_data = get_percent_data(df, prog_col)

            PROG_ORDER = [
                "Sim, já pratiquei", 
                "Já vi, mas nunca pratiquei", 
                "Ainda não"
            ]
            
            PROG_COLORS = {
                "Sim, já pratiquei": "#5cb85c",       
                "Já vi, mas nunca pratiquei": "#f0ad4e", 
                "Ainda não": "#d9534f"               
            }

            fig_prog = px.bar(
                prog_data,
                x=prog_col,
                y="count",
                color=prog_col,
                color_discrete_map=PROG_COLORS,
                labels={
                    prog_col: "Nível de Experiência",
                    "count": "Participantes"
                },
                custom_data=["percentage"]
            )
            
            fig_prog.update_xaxes(categoryorder="array", categoryarray=PROG_ORDER)
            
            fig_prog.update_traces(
                hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<br>Porcentagem: %{customdata[0]}%<extra></extra>"
            )
            fig_prog.update_layout(
                **DEFAULT_PLOT_LAYOUT, 
                showlegend=False, 
                title_text=""
            )
            
            st.plotly_chart(fig_prog, use_container_width=True)
        else:
            st.warning(f"Coluna '{prog_col}' não encontrada.")


    with col_games:
        st.subheader("Gosta de Jogos Eletrônicos?")
        
        games_col = 'likes_games'
        
        if games_col in df.columns:
            games_data = get_percent_data(df, games_col)
            
            YES_NO_LOCAL = {
                "Sim": "#5cb85c",
                "Não": "#d9534f"
            }

            fig_games = px.bar(
                games_data,
                x=games_col,
                y="count",
                color=games_col,
                color_discrete_map=YES_NO_LOCAL,
                labels={
                    games_col: "Resposta",
                    "count": "Participantes"
                },
                custom_data=["percentage"]
            )
            
            fig_games.update_xaxes(categoryorder="array", categoryarray=["Sim", "Não"])

            fig_games.update_traces(
                hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<br>Porcentagem: %{customdata[0]}%<extra></extra>"
            )
            fig_games.update_layout(
                **DEFAULT_PLOT_LAYOUT, 
                showlegend=False, 
                title_text=""
            )
            
            st.plotly_chart(fig_games, use_container_width=True)
        else:
            st.warning(f"Coluna '{games_col}' não encontrada.")
    
    
    
    