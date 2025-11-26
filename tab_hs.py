import streamlit as st
import plotly.express as px
import pandas as pd

from data_preparation import df
from constants import DEFAULT_PLOT_LAYOUT, GENDER_COLORS, UNIVERSITY_COLORS, YES_NO

def render_tab_hs():
    
    df_clean = df.copy()
    df_clean = df_clean[df_clean['plans_university'] != 'Não']
    df_clean = df_clean[df_clean['gender'] != 'Prefiro não dizer']

    col_toggle, _ = st.columns([1, 3])
    with col_toggle:
        include_missing = st.toggle("Incluir dados desconsiderados", value=False)
    
    if include_missing:
        st.info("Exibindo dados brutos (inclui quem não quer faculdade ou não informou gênero, se houver resposta de universidade).")
        d_base = df.copy() 
    else:
        d_base = df_clean.copy() 
    st.metric("Tamanho da Amostra",len(d_base))
    st.subheader("Intenção de Universidade (Pública vs. Privada)")
    st.markdown("Comparativo entre alunos do 3º e 2º ano em relação ao tipo de universidade pretendida.")

    d_filtered = d_base.copy()

    cols_to_clean = ['plans_university', 'gender', 'university_choice', 'high_school_year', 'has_pc', 'programming_experience']
    for col in cols_to_clean:
        if col in d_filtered.columns:
            d_filtered[col] = d_filtered[col].astype(str).str.strip()

    target_years = ['2º ano', '3º ano']
    target_unis = list(UNIVERSITY_COLORS.keys()) 
    
    d_filtered = d_filtered[
        d_filtered['high_school_year'].isin(target_years) & 
        d_filtered['university_choice'].isin(target_unis)
    ]
    
    grouped_data = d_filtered.groupby(['high_school_year', 'university_choice']).size().reset_index(name='count')
    total = grouped_data['count'].sum()
    grouped_data['percentage'] = (grouped_data['count'] / total * 100).round(1) if total > 0 else 0

    if not grouped_data.empty:
        fig = px.bar(
            grouped_data,
            x='high_school_year',       
            y='count',                  
            color='university_choice',  
            barmode='group',            
            color_discrete_map=UNIVERSITY_COLORS,
            labels={
                'high_school_year': 'Ano Escolar',
                'count': 'Quantidade de Alunos',
                'university_choice': 'Tipo de Universidade'
            },
            custom_data=['percentage']
        )
        fig.update_xaxes(categoryorder='array', categoryarray=['3º ano', '2º ano'])
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Tipo: %{data.name}<br>Participantes: %{y}<br>Global: %{customdata[0]}%<extra></extra>"
        )
        fig.update_layout(**DEFAULT_PLOT_LAYOUT, title_text="", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True, key="hs_uni_comparison")
    else:
        st.warning("Não há dados suficientes com os filtros atuais.")

    st.markdown("---")

    st.subheader("Detalhamento por Gênero: Escolha da Faculdade")
    
    c1, c2 = st.columns(2)

    def plot_gender_stack(year_label, title_text):
        df_year = d_filtered[d_filtered['high_school_year'] == year_label].copy()
        if df_year.empty: return None

        grouped = df_year.groupby(['university_choice', 'gender']).size().reset_index(name='count')
        grouped['total_uni'] = grouped.groupby('university_choice')['count'].transform('sum')
        grouped['percentage'] = (grouped['count'] / grouped['total_uni'] * 100).round(1)

        fig = px.bar(
            grouped,
            x='university_choice',
            y='count',
            color='gender',
            barmode='stack',
            color_discrete_map=GENDER_COLORS, 
            labels={'university_choice': 'Universidade', 'count': 'Qtd', 'gender': 'Gênero'},
            custom_data=['percentage']
        )
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Gênero: <b>%{data.name}</b><br>Qtd: %{y}<br>Pct: %{customdata[0]}%<extra></extra>"
        )
        fig.update_layout(**DEFAULT_PLOT_LAYOUT, title_text="", legend_title_text="")
        st.subheader(title_text)
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{year_label}_gender")

    with c1: plot_gender_stack('3º ano', "3º Ano - Faculdade")
    with c2: plot_gender_stack('2º ano', "2º Ano - Faculdade")

    st.markdown("---")

    st.subheader("Infraestrutura: Acesso a Computador")
    st.markdown("Comparativo de posse de computador para cada Ano Escolar, subdividido pelo Tipo de Universidade desejada.")

    col_3ano, col_2ano = st.columns(2)

    def plot_pc_specific(year_label, uni_type, title_text):
        subset = d_filtered[
            (d_filtered['high_school_year'] == year_label) & 
            (d_filtered['university_choice'] == uni_type)
        ].copy()

        if subset.empty:
            st.info(f"Sem dados: {uni_type}")
            return None

        grouped = subset.groupby(['has_pc', 'gender']).size()
        
        present_genders = subset['gender'].unique()
        
        all_combinations = pd.MultiIndex.from_product([['Sim', 'Não'], present_genders], names=['has_pc', 'gender'])
        grouped = grouped.reindex(all_combinations, fill_value=0).reset_index(name='count')
        
        grouped['total_pc'] = grouped.groupby('has_pc')['count'].transform('sum')
        grouped['percentage'] = 0.0
        mask = grouped['total_pc'] > 0
        grouped.loc[mask, 'percentage'] = (grouped.loc[mask, 'count'] / grouped.loc[mask, 'total_pc'] * 100).round(1)

        fig = px.bar(
            grouped,
            x='has_pc',             
            y='count',
            color='gender',         
            barmode='stack',
            color_discrete_map=GENDER_COLORS, 
            labels={'gender': 'Gênero', 'count': 'Qtd', 'has_pc': 'Tem PC?'},
            custom_data=['percentage']
        )
        fig.update_xaxes(categoryorder='array', categoryarray=['Sim', 'Não'])
        fig.update_traces(
            hovertemplate="<b>Tem PC? %{x}</b><br>Gênero: <b>%{data.name}</b><br>Qtd: %{y}<br>Pct na Categoria: %{customdata[0]}%<extra></extra>"
        )
        fig.update_layout(**DEFAULT_PLOT_LAYOUT, title_text="", legend_title_text="Gênero")
        st.caption(title_text) 
        st.plotly_chart(fig, use_container_width=True, key=f"pc_{year_label}_{uni_type}")

    with col_3ano:
        st.subheader("3º Ano")
        plot_pc_specific('3º ano', 'Privada', "Pretende: Privada")
        st.markdown("") 
        plot_pc_specific('3º ano', 'Pública', "Pretende: Pública")

    with col_2ano:
        st.subheader("2º Ano")
        plot_pc_specific('2º ano', 'Privada', "Pretende: Privada")
        st.markdown("") 
        plot_pc_specific('2º ano', 'Pública', "Pretende: Pública")

    st.markdown("---")

    st.subheader("Conhecimento em Programação")
    st.markdown("Nível de experiência prévia com programação.")

    c5, c6 = st.columns(2)
    PROG_ORDER = ["Sim, já pratiquei", "Já vi, mas nunca pratiquei", "Ainda não"]
    
    UNI_COLORS_SHORT = {
        'Pública': UNIVERSITY_COLORS.get('Universidade Pública', '#F57C2A'),
        'Privada': UNIVERSITY_COLORS.get('Universidade Privada', '#2AEAF5')
    }

    def plot_prog_experience(year_label, title_text):
        df_year = d_filtered[d_filtered['high_school_year'] == year_label].copy()

        if df_year.empty:
            st.warning(f"Sem dados para {year_label}.")
            return None

        grouped = df_year.groupby(['programming_experience', 'university_choice']).size().reset_index(name='count')
        grouped['total_xp'] = grouped.groupby('programming_experience')['count'].transform('sum')
        grouped['percentage'] = (grouped['count'] / grouped['total_xp'] * 100).round(1)

        fig = px.bar(
            grouped,
            x='programming_experience', 
            y='count',
            color='university_choice',  
            barmode='stack',            
            color_discrete_map=UNI_COLORS_SHORT, 
            labels={'university_choice': 'Universidade', 'count': 'Participantes', 'programming_experience': 'Experiência'},
            custom_data=['percentage']
        )
        fig.update_xaxes(categoryorder='array', categoryarray=PROG_ORDER)
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Destino: <b>%{data.name}</b><br>Qtd: %{y}<br>Pct na Categoria: %{customdata[0]}%<extra></extra>"
        )
        fig.update_layout(**DEFAULT_PLOT_LAYOUT, title_text="", legend_title_text="")
        st.subheader(title_text)
        st.plotly_chart(fig, use_container_width=True, key=f"prog_{year_label}")

    with c5:
        plot_prog_experience('3º ano', "3º Ano - Programação")

    with c6:
        plot_prog_experience('2º ano', "2º Ano - Programação")