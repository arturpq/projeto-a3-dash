import streamlit as st
import plotly.express as px
import pandas as pd

from chart_helpers import AREA_COLORS, get_percent_data, get_standardized_interest_data, map_to_area, normalize_subject, plot_styled_bar
from constants import DEFAULT_PLOT_LAYOUT, INTEREST_SCALE_COLORS, INTEREST_SCALE_ORDER, UNIVERSITY_TIME
from data_preparation import df_final as d_clean
from data_preparation import df as d

def render_tab_inter(use_removed_data):
    
    df = d if use_removed_data else d_clean
    
    st.metric("Participantes da Amostra", len(df))

    st.header("Distribuição do Nível de Interesse")
    st.markdown(
        "Gráficos mostram a distribuição dos participantes pela escala de interesse, **padronizada** de Nenhum (vermelho) a Muito (verde)."
    )

    

    interest_cols_map = {
        "interest_math": "Matemática",
        "interest_portuguese": "Português",
        "interest_logic_math": "Lógica e Matemática", 
        "interest_tech_innovation": "Tecnologia e Inovação"
    }

    cols_to_plot = list(interest_cols_map.keys())

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

            dist_data = get_standardized_interest_data(df, col, INTEREST_SCALE_ORDER)

            fig = px.bar(
                dist_data,
                x=col,
                y="count",
                color=col,
                color_discrete_map=INTEREST_SCALE_COLORS, 
                labels={
                    col: "Nível de Interesse",
                    "count": "Participantes"
                },
                custom_data=["percentage"]
                
            )

            fig.update_xaxes(categoryorder="array", categoryarray=INTEREST_SCALE_ORDER)

            fig.update_traces(
                hovertemplate=(
                    f"<b>{title}:</b> %{{x}}<br>"
                    "<b>Participantes:</b> %{y}<br>"
                    "<b>Percentual:</b> %{customdata[0]:.2f}%<extra></extra>"
                )
            )
            fig.update_layout(
                **DEFAULT_PLOT_LAYOUT,
                showlegend=False, 
                title_text=""
            )

            st.plotly_chart(fig, width='stretch')
    st.subheader("Turno Preferido")
    
    preferred_shift_data = get_percent_data(d, "preferred_shift")
    fig = plot_styled_bar(
        df=preferred_shift_data,
        x_col="preferred_shift",
        y_col="count",
        x_title="Turno Preferido",
        y_title="Participantes",
        orientation="h",
        color_discrete_map=UNIVERSITY_TIME
    )
    st.plotly_chart(fig, width='stretch')    
    




    st.header("Matérias Preferidas")
    df_viz = df[df['subject_normalized'].map(lambda df: len(df)) > 0].copy()

    st.subheader("Todas as Respostas (Combinações)")

    df_viz['combined_str'] = df_viz['subject_normalized'].apply(
        lambda x: ', '.join(sorted(x))
    )

    v_combined = df_viz['combined_str'].value_counts().reset_index()
    v_combined.columns = ['Mencao Combinada', 'count']

    total_combined = v_combined['count'].sum()
    v_combined['percentage'] = (v_combined['count'] / total_combined * 100).round(2)
    
    fig_combined = plot_styled_bar(
        df=v_combined.head(15), 
        x_col='Mencao Combinada',
        y_col='count',
        x_title='Participantes',
        y_title='Combinação de Matérias',
        orientation="h",
        color_discrete_map=None
    )
    st.plotly_chart(fig_combined, use_container_width=True, key="combined_mentions_normalized")


    st.subheader("Menção Individual de Matérias")

    df_exploded_subj = df_viz.explode('subject_normalized')

    v_individual = df_exploded_subj['subject_normalized'].value_counts().reset_index()
    v_individual.columns = ['Mencao Individual', 'count']

    mask_exclude = v_individual['Mencao Individual'].isin(['Sem Resposta', ''])
    v_individual = v_individual[~mask_exclude]

    total_individual = v_individual['count'].sum()
    v_individual['percentage'] = (v_individual['count'] / total_individual * 100).round(2)

    fig_individual = plot_styled_bar(
        df=v_individual.head(15),
        x_col='Mencao Individual',
        y_col='count',
        x_title='Vez(es) Mencionada',
        y_title='Matérias',
        orientation="h",
        color_discrete_map=None 
    )
    st.plotly_chart(fig_individual, use_container_width=True, key="total_mentions_normalized")

    st.markdown("---")
    st.header("Distribuição de Menções por Área de Conhecimento")

    df_exploded_area = df_viz.explode('knowledge_areas')

    v_areas = df_exploded_area['knowledge_areas'].value_counts().reset_index()
    v_areas.columns = ['Area de Conhecimento', 'count']

    mask_exclude_area = v_areas['Area de Conhecimento'].isin(['Não Classificado', 'Outros/Geral', '', None])
    v_areas = v_areas[~mask_exclude_area]

    total_areas = v_areas['count'].sum()
    v_areas['percentage'] = (v_areas['count'] / total_areas * 100).round(2)

    fig_area = plot_styled_bar(
        df=v_areas,
        x_col='Area de Conhecimento',
        y_col='count',
        x_title='Vezes Mencionada',
        y_title='Área de Conhecimento',
        orientation="h",
        color_discrete_map=AREA_COLORS
    )
    st.plotly_chart(fig_area, use_container_width=True, key="area_distribution")

    st.markdown("---")
    st.header("Avaliação da Experiência do Evento")

    LIKERT_ORDER = [
        "Discordo totalmente",
        "Discordo parcialmente",
        "Nem concordo nem discordo",
        "Concordo parcialmente",
        "Concordo totalmente"
    ]

    LIKERT_COLORS = {
        "Discordo totalmente": "#d9534f", 
        "Discordo parcialmente": "#f0ad4e",     
        "Nem concordo nem discordo": "#f7f7f7", 
        "Concordo parcialmente": "#5bc0de",     
        "Concordo totalmente": "#5cb85c"        
    }

    
    event_cols_map = {
        'q_overall_experience_positive': 'Experiência Geral Positiva',
        'q_explanations_clear': 'Explicações Claras',
        'q_apps_interesting': 'Aplicações Interessantes',
        'q_tech_use_good': 'Uso Adequado de Tecnologia',
        'q_helped_understand_cs': 'Ajudou a Entender Computação'
    }

    
    
    cols_list = list(event_cols_map.keys())

    
    c1, c2 = None, None

    for i, col in enumerate(cols_list):
        if col not in df.columns:
            continue

        
        counts = df[col].value_counts()
                
        
        counts = counts.reindex(LIKERT_ORDER, fill_value=0)
                
        
        likert_data = counts.reset_index()
        likert_data.columns = [col, 'count'] 
                
        
        total = likert_data['count'].sum()
        if total > 0:
            likert_data['percentage'] = (likert_data['count'] / total * 100).round(2)
        else:
            likert_data['percentage'] = 0.0

        
        fig = plot_styled_bar(
            df=likert_data,
            x_col=col,       
            y_col="count",
            x_title="Resposta",
            y_title="Participantes",
            orientation="v", 
            color_discrete_map=LIKERT_COLORS 
        )
        
        
        fig.update_xaxes(
            categoryorder="array", 
            categoryarray=LIKERT_ORDER,
            fixedrange=True
        )

        if i == 0:
            title = event_cols_map[col]
            st.subheader(title)
            st.plotly_chart(fig, use_container_width=True, key=f"likert_{col}")
            
            st.markdown("---") 
            c1, c2 = st.columns(2)

        else:
            if c1 is None or c2 is None:
                c1, c2 = st.columns(2)

            container = c1 if i % 2 != 0 else c2

            with container:
                title = event_cols_map[col]
                st.subheader(title)
                st.plotly_chart(fig, use_container_width=True, key=f"likert_{col}")
    st.text("A experiência de todos em relação ao evento foi muito positiva. Por conta dessa uniformidade, não é viável realizar uma análise aprofundada, pois a falta de variação nas respostas.")
    