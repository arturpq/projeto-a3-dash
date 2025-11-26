import pandas as pd
from datetime import datetime
import streamlit as st

from chart_helpers import normalize_subject

COLUMN_MAP = {
    'ID': 'id',
    'Data de nascimento': 'birth_date',
    'Com qual gênero você se identifica?': 'gender',
    'Em qual ano do ensino médio você está?': 'high_school_year',
    'Você pretende fazer um curso universitário no próximo ano ou quando terminar o 3º ano?': 'plans_university',
    'Em qual universidade?': 'university_choice',
    'Qual o turno de sua preferência?': 'preferred_shift',
    'Tecnologia e inovação': 'interest_tech_innovation',
    'Resolver desafios lógicos e matemáticos': 'interest_logic_math',
    'Matemática': 'interest_math',
    'Português': 'interest_portuguese',
    'Qual a sua matéria preferida na escola? (resposta aberta)': 'favorite_subject',
    'Já teve contato com programação ou desenvolvimento de jogos/aplicações?': 'programming_experience',
    'Você gosta de jogos eletrônicos?': 'likes_games',
    'Videogame': 'has_console',
    'Computador': 'has_pc',
    'Internet residencial (Wi-Fi)': 'has_home_wifi',
    'Celular': 'has_smartphone',
    'Internet no celular': 'has_mobile_data',
    'As explicações dos estudantes foram claras e fáceis de entender.': 'q_explanations_clear',
    'As aplicações apresentadas despertaram meu interesse.': 'q_apps_interesting',
    'O uso das tecnologias nas oficinas foi adequado e interessante': 'q_tech_use_good',
    'A atividade ajudou-me a compreender melhor o que é o curso de Ciência da Computação': 'q_helped_understand_cs',
    'De modo geral, a experiência do evento foi positiva.': 'q_overall_experience_positive'
}
AREA_MAP = {
    # Ciências da Natureza
    "Biologia": "Ciências da Natureza",
    "Química": "Ciências da Natureza",
    
    # Ciências Humanas e Sociais
    "História": "Ciências Humanas",
    "Geografia": "Ciências Humanas",
    "Sociologia": "Ciências Humanas",
    "Filosofia": "Ciências Humanas",
    
    # Matemática e Exatas
    "Matemática": "Ciências Exatas",
    "Informática": "Ciências Exatas",
    
    # Linguagens
    "Português": "Linguagens",
    "Inglês": "Linguagens",
    
    # Outros/Geral (Manter para filtrar ou visualizar ruído)
    "Educação Física": "Outros/Geral",
    "Sem Resposta": "Outros/Geral"
}

DROP_COLS = [
    'Hora de início', 'Hora de conclusão', 'Email', 'Nome', 'Hora da última modificação'
]


def calculate_age(date):
    """Retorna idade inteira ou 0 para inválidos."""
    if pd.isna(date):
        return 0

    today = datetime.now()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return max(age, 0)

def map_to_unique_areas(subject_list):
    if not subject_list: return []
        
    unique_areas = set()
        
    for subject in subject_list:
        area = AREA_MAP.get(subject)
        if area:
            unique_areas.add(area)
        
    return sorted(list(unique_areas))

@st.cache_data
def load_and_prepare_data(file_path="Raw_Data.xlsx"):

    try:
        df = pd.read_excel(file_path)
    except Exception:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df.columns = df.columns.str.strip()

    df = df.drop(columns=DROP_COLS, errors="ignore")
    df = df.rename(columns=COLUMN_MAP)

    df_temp = df[df['favorite_subject'].notna()].copy()
    SPLIT_PATTERN = r',\s*|\s+e\s*|\s+ou\s*|\s*/\s*|\s+\+\s*|;\s*'

    df_temp['subject_array_split'] = (
        df_temp['favorite_subject']
        .astype(str)
        .str.lower()
        .str.split(SPLIT_PATTERN)
    )

    df['subject_normalized'] = df_temp['subject_array_split'].apply(
        lambda subject_list: [normalize_subject(s) for s in subject_list if s.strip()]
    )

    df['knowledge_areas'] = df['subject_normalized'].apply(map_to_unique_areas)

    df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
    df["age"] = df["birth_date"].apply(calculate_age)
    df = df.drop(columns=["birth_date"])

    df_age = df[df["age"] > 0].copy()
    df_gender = df[df["gender"] != "Prefiro não dizer"].copy()

    return df, df_age, df_gender
df, df_age, df_gender = load_and_prepare_data()
df_final = df_gender[df_gender["plans_university"] == "Sim"].copy()