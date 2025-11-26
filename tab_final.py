import streamlit as st
import pandas as pd
from data_preparation import df_final as d_clean
from data_preparation import df as d
from constants import UNIVERSITY_COLORS, GENDER_COLORS
def render_white_svg(file_path):
    """
    Lê um arquivo SVG, força a cor branca e exibe ocupando 100% da largura da coluna.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        # 1. Substitui cores comuns por BRANCO
        svg_content = svg_content.replace('fill="currentColor"', 'fill="#FFFFFF"')
        svg_content = svg_content.replace('fill="black"', 'fill="#FFFFFF"')
        svg_content = svg_content.replace('fill="#000000"', 'fill="#FFFFFF"')
        
        # 2. Força o SVG a ser responsivo (width=100%)
        # Injetamos um style diretamente na tag <svg> se ela não tiver, 
        # ou apenas garantimos que ele esteja dentro de uma div elástica.
        # O jeito mais seguro é substituir a abertura da tag:
        svg_content = svg_content.replace('<svg', '<svg style="width: 100%; height: auto;"')

        # 3. Renderiza
        st.markdown(
            f"""
            <div style="width: 100%; display: flex; justify-content: center; align-items: center;">
                {svg_content}
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {file_path}")
def render_tab_final(use_removed_data):
    # ==============================================================================
    # 1. PREPARAÇÃO GLOBAL DOS DADOS
    # ==============================================================================
    d_work = d if use_removed_data else d_clean
    
    # Limpeza e Padronização
    cols_text = ['university_choice', 'high_school_year', 'gender', 'preferred_shift', 'programming_experience']
    for c in cols_text:
        if c in d_work.columns:
            d_work[c] = d_work[c].astype(str).str.strip()

    d_work['university_choice'] = d_work['university_choice'].replace({
        'Pública': 'Universidade Pública',
        'Privada': 'Universidade Privada'
    })

    # --- NOVA FUNÇÃO: CALCULAR MATÉRIA PREFERIDA (COM ARRAY) ---
    def get_top_subject(subset_df):
        """
        Explode a coluna de arrays 'subject_normalized' e retorna a(s) matéria(s) mais frequente(s).
        """
        if subset_df.empty: return "N/A"
        
        # Explode o array para contar cada menção individualmente
        exploded = subset_df.explode('subject_normalized')
        
        # Se só tiver NaNs ou listas vazias
        if exploded['subject_normalized'].dropna().empty:
            return "N/A"

        # Conta frequências
        counts = exploded['subject_normalized'].value_counts()
        if counts.empty: return "N/A"
        
        max_freq = counts.iloc[0]
        # Pega todos que têm a mesma contagem máxima (empate)
        top_subjects = counts[counts == max_freq].index.tolist()
        
        if len(top_subjects) == 1:
            return top_subjects[0]
        elif len(top_subjects) == 2:
            return f"{top_subjects[0]} e {top_subjects[1]}"
        else:
            return "Variado/Indefinido"

    # Função Auxiliar de Perfil (Atualizada)
    def get_profile_text(subset, is_female_focus=False):
        if subset.empty: return "Sem dados suficientes."
        try:
            # Idade
            ages = subset[subset['age'] > 0]['age']
            p_age = int(ages.mode()[0]) if not ages.empty else "?"
            
            # Outros atributos
            p_shift = subset['preferred_shift'].mode()[0]
            
            # Matéria Preferida (Usando a nova lógica)
            p_subj = get_top_subject(subset)
            
            gender_str = "Mulher" if is_female_focus else subset['gender'].mode()[0]

            return (
                f"Perfil: {gender_str}, {p_age} anos.<br>"
                f"Prefere turno da {p_shift}.<br>"
                f"Gosta de {p_subj}."
            )
        except: return "Dados variados demais."

    # ==============================================================================
    # 2. PARTE A: PERSONA GERAL
    # ==============================================================================
    st.header("Perfil Médio do Participante")
    st.markdown("Perfil predominante calculado com base na frequência (moda) de **todas as respostas**.")

    # Cálculo das Modas Gerais
    try:
        age_valid = d_work[d_work['age'] > 0]['age']
        g_age = int(age_valid.mode()[0]) if not age_valid.empty else "N/A"
        g_gender = d_work['gender'].mode()[0]
        g_year = d_work['high_school_year'].mode()[0]
        g_uni = d_work['university_choice'].mode()[0]
        
        # Usa a função correta para matéria geral
        g_subj = get_top_subject(d_work)
        
    except: g_age, g_gender, g_year, g_uni, g_subj = "N/A", "N/A", "N/A", "N/A", "N/A"

    # Layout Geral
    c_img, c_metrics = st.columns([1, 3])
    with c_img:
        render_white_svg("gender-male.svg")
    
    with c_metrics:
        m1, m2, m3 = st.columns(3)
        m1.metric("Idade Típica", f"{g_age} Anos")
        m2.metric("Gênero", g_gender)
        m3.metric("Ano Escolar", g_year)
        
        m4, m5 = st.columns(2) # Mantendo grid de 3 para alinhar
        m4.metric("Objetivo", g_uni)
        m5.metric("Matéria Favorita", g_subj)
        
        st.info(f"💡 **Resumo:** A maioria do público é do **{g_year}**, gênero **{g_gender}**, com **{g_age} anos** e foco em **{g_uni}**.")


    st.markdown
    st.header("Consideração")
    st.text("Com base nas análises feitas, o evento teve resultado muito positivo, e maior parte do publico apresenta uma considerável afinidade com a área, a análise de perfil considera que todos são possiveis estudantes da área da tecnologia")
    st.markdown("---")
    st.subheader("Arquétipos de Alunos (Geral)")
    st.text("Separar os alunos pela maior probabilidade da sua entrada na faculdade")
    
    gen_archetypes = [
        {"name": "🎯 Alunos Mais Prováveis", "rule": "3º Ano ➝ Univ. Privada", "mask": (d_work['high_school_year'] == '3º ano') & (d_work['university_choice'] == 'Universidade Privada'), "color": "#5cb85c"},
        {"name": "🏫 Alunos Menos Prováveis", "rule": "3º Ano ➝ Univ. Pública", "mask": (d_work['high_school_year'] == '3º ano') & (d_work['university_choice'] == 'Universidade Pública'), "color": "#f0ad4e"},
        {"name": "🌱 Futuros Mais Prováveis", "rule": "2º Ano ➝ Univ. Privada", "mask": (d_work['high_school_year'] == '2º ano') & (d_work['university_choice'] == 'Universidade Privada'), "color": "#5bc0de"},
        {"name": "📚 Futuros Menos Prováveis", "rule": "2º Ano ➝ Univ. Pública", "mask": (d_work['high_school_year'] == '2º ano') & (d_work['university_choice'] == 'Universidade Pública'), "color": "#d9534f"}
    ]

    c1, c2 = st.columns(2)
    for i, arc in enumerate(gen_archetypes):
        with (c1 if i % 2 == 0 else c2):
            subset = d_work[arc['mask']]
            count = len(subset)
            total = len(d_work)
            pct = int(count / total * 100) if total > 0 else 0
            
            st.markdown(f"### {arc['name']}")
            st.caption(f"Critério: {arc['rule']}")
            st.markdown(f"""<div style="background-color: #f0f2f6; border-radius: 8px; margin-bottom: 10px;"><div style="width: {pct if pct > 5 else 5}%; background-color: {arc['color']}; padding: 8px; border-radius: 8px; text-align: right; color: white; font-weight: bold;">{count}</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="border-left: 5px solid {arc['color']}; padding: 10px; border-radius: 5px; background-color: rgba(255,255,255,0.5); font-size: 0.95em;">{get_profile_text(subset)}</div><br>""", unsafe_allow_html=True)

    # ==============================================================================
    # 3. PARTE B: PERSONA FEMININA (3º ANO)
    # ==============================================================================
    st.markdown("---")
    st.header("Perfil Médio Feminino (3º Ano)")
    st.markdown("Recorte específico para **Mulheres do 3º Ano**, identificando características para campanhas focadas.")

    # Filtro Específico
    d_fem = d_work[(d_work['gender'] == 'Mulher') & (d_work['high_school_year'] == '3º ano')].copy()

    if d_fem.empty:
        st.error("Não há dados suficientes para Mulheres do 3º Ano.")
    else:
        # Cálculo Modas Femininas
        try:
            age_valid_f = d_fem[d_fem['age'] > 0]['age']
            f_age = int(age_valid_f.mode()[0]) if not age_valid_f.empty else "?"
            f_uni = d_fem['university_choice'].mode()[0]
            f_shift = d_fem['preferred_shift'].mode()[0]
            f_raw_prog = d_fem['programming_experience'].mode()[0]
            f_prog = "Iniciante" if "não" in f_raw_prog.lower() else "Já praticou"
            
            # Matéria (Usando a nova lógica)
            f_subj = get_top_subject(d_fem)
            
        except: f_age, f_uni, f_shift, f_prog, f_subj = "?", "?", "?", "?", "?"

        # Layout Feminino (Idêntico ao Geral)
        cf_img, cf_metrics = st.columns([1, 3])
        with cf_img:
            render_white_svg("gender-female.svg")            
        
        with cf_metrics:
            fm1, fm2, fm3 = st.columns(3)
            fm1.metric("Idade Típica", f"{f_age} Anos")
            fm2.metric("Gênero", "Mulher")
            fm3.metric("Ano Escolar", "3º ano")
            
            fm4, fm5 = st.columns(2) # Grid 3 para alinhar
            fm4.metric("Objetivo Principal", f_uni)
            fm5.metric("Matéria Favorita", f_subj)
            
            st.info(f"👩‍🎓 **Resumo:** A aluna típica do 3º ano tem **{f_age} anos**, prefere estudar no turno da **{f_shift}** e seu foco principal é a **{f_uni}**.")

        # --- ARQUÉTIPOS FEMININOS ---
        st.subheader("Comparativo de Perfis (Feminino)")
        st.markdown("Diferenças entre quem busca o ensino privado vs. público dentro deste recorte.")

        fem_archetypes = [
            {"name": "🎯 As Mais Prováveis (Privada)", "rule": "Mulheres | 3º Ano ➝ Privada", "mask": (d_fem['university_choice'] == 'Universidade Privada'), "color": "#5bc0de"}, # Azul Claro
            {"name": "🏫 As Menos Prováveis (Pública)", "rule": "Mulheres | 3º Ano ➝ Pública", "mask": (d_fem['university_choice'] == 'Universidade Pública'), "color": "#f0ad4e"}  # Laranja
        ]

        c_f1, c_f2 = st.columns(2)
        for i, arc in enumerate(fem_archetypes):
            # Alterna colunas (0 -> esq, 1 -> dir)
            col_target = c_f1 if i == 0 else c_f2
            
            with col_target:
                subset = d_fem[arc['mask']]
                count = len(subset)
                total = len(d_fem)
                pct = int(count / total * 100) if total > 0 else 0
                
                st.markdown(f"### {arc['name']}")
                st.caption(f"Critério: {arc['rule']}")
                st.markdown(f"""<div style="background-color: #f0f2f6; border-radius: 8px; margin-bottom: 10px;"><div style="width: {pct if pct > 5 else 5}%; background-color: {arc['color']}; padding: 8px; border-radius: 8px; text-align: right; color: white; font-weight: bold;">{count} ({pct}%)</div></div>""", unsafe_allow_html=True)
                st.markdown(f"""<div style="border-left: 5px solid {arc['color']}; padding: 15px; border-radius: 5px; background-color: rgba(255,255,255,0.5); font-size: 0.95em;">{get_profile_text(subset, is_female_focus=True)}</div>""", unsafe_allow_html=True)