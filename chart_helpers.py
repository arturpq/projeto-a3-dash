import pandas as pd
import plotly.express as px
from constants import DEFAULT_PLOT_LAYOUT, GENDER_COLORS, INTEREST_SCALE_ORDER
def get_percent_data(df, column):
    """Retorna contagem + porcentagem para uma coluna categórica."""
    if df.empty or column not in df.columns:
        return pd.DataFrame()

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "count"]
    total = counts["count"].sum()
    counts["percentage"] = (counts["count"] / total * 100).round(2)
    return counts


def get_cross_data(df, category_col, gender_col="gender"):
    """
    Retorna contagem e porcentagem de uma coluna categórica
    cruzada com o gênero.
    """
    if df.empty or category_col not in df.columns or gender_col not in df.columns:
        return pd.DataFrame()

    cross_tab = pd.crosstab(df[category_col], df[gender_col])
    cross_df = cross_tab.reset_index().melt(
        id_vars=category_col, var_name=gender_col, value_name="count"
    )

    cross_df["category_total"] = cross_df.groupby(category_col)["count"].transform("sum")
    cross_df["percent_in_category"] = (
        cross_df["count"] / cross_df["category_total"] * 100
    ).round(2)

    return cross_df


def plot_styled_pie(df, names_col, values_col, colors_map, hover_template):
    """Pizza limpa, sem título e sem rótulos internos."""
    if df.empty:
        return None

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=0.35,
        color=names_col,
        color_discrete_map=colors_map
    )

    fig.update_traces(
        hovertemplate=hover_template,
        textinfo="percent"  
    )

    fig.update_layout(
        **DEFAULT_PLOT_LAYOUT,
        showlegend=True,
        title_text=""
    )

    return fig


def plot_styled_bar(df, x_col, y_col, x_title, y_title, orientation="v", color_discrete_map=None):
    if df.empty:
        return None

    
    if "percentage" in df.columns:
        df["percentage"] = df["percentage"].astype(float)

    px_x = x_col if orientation == "v" else y_col
    px_y = y_col if orientation == "v" else x_col
    
    color_col = x_col if color_discrete_map else None

    fig = px.bar(
        df,
        x=px_x,
        y=px_y,
        color=color_col, 
        color_discrete_map=color_discrete_map, 
        labels={
        px_x: x_title,   
        px_y: y_title    
    },
        custom_data=["percentage"],
        orientation=orientation
    )

    hover_template = (
    f"<b>{x_title}:</b> %{{x}}<br>"
    f"<b>{y_title}:</b> %{{y}}<br>"
    "<b>Percentual:</b> %{customdata[0]:.2f}%<extra></extra>"
    )

    fig.update_traces(hovertemplate=hover_template)

    fig.update_layout(
        **DEFAULT_PLOT_LAYOUT,
        showlegend=False
    )

    fig.update_layout(title_text="")

    return fig


def plot_grouped_bar(df, category_col, gender_col, x_title, y_title):
    """
    Gráfico de barras agrupado para análise cruzada (Categoria vs. Gênero).
    Assumimos que o dataframe vem de get_cross_data().
    """
    if df.empty:
        return None

    fig = px.bar(
        df,
        x=category_col,
        y="count",
        color=gender_col,
        barmode="group",
        color_discrete_map=GENDER_COLORS,
        labels={
            category_col: x_title,
            "count": y_title,
            gender_col: "Gênero",
        },
        custom_data=["percent_in_category"],
    )

    fig.update_traces(
        hovertemplate=(
            f"<b>{x_title}:</b> %{{x}}<br>"
            "<b>Gênero:</b> %{customdata[0]}<br>" 
            "<b>Contagem:</b> %{y}<br>"
            "<b>Percentual na Categoria:</b> %{customdata[0]:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(
        **DEFAULT_PLOT_LAYOUT,
        showlegend=True,
        legend_title_text="Gênero",
        title_text=""
    )

    return fig

def get_standardized_interest_data(df, column, interest_order):
    """
    Retorna a contagem e porcentagem para uma coluna de interesse,
    garantindo que todas as categorias (Nenhum a Muito) estejam presentes,
    mesmo que com contagem zero.
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "count"]

    base_df = pd.DataFrame({
        column: interest_order,
        "count": 0
    })

    merged_df = base_df.merge(counts, on=column, how="left", suffixes=('_base', '_real'))
    
    merged_df['count'] = merged_df['count_real'].fillna(merged_df['count_base'])
    merged_df = merged_df.drop(columns=['count_base', 'count_real'])

    total = merged_df["count"].sum()
    merged_df["percentage"] = (merged_df["count"] / total * 100).round(2)
    
    merged_df[column] = pd.Categorical(merged_df[column], categories=interest_order, ordered=True)
    merged_df = merged_df.sort_values(column)

    return merged_df
import pandas as pd


SUBJECT_MAP = {
    "Matemática": [
        "matematica", 
    ],
    "Física": [
        "fisica", 
        "fisic"
    ],
    "Português": [
        "português.", 
    ],
    "História": [
        "historia", 
        "history"
    ],
    "Educação Física": [
        "educação fisica"
    ],
    "Química": [
        "quimica" 
        
    ],
    "Sem Resposta": [
        "eu não sei... kkkk"
    ]
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


AREA_COLORS = {
    "Ciências Exatas": "#1f77b4",          
    "Ciências da Natureza": "#2ca02c",     
    "Ciências Humanas": "#ff7f0e",        
    "Linguagens": "#9467bd",               
    "Outros/Geral": "#7f7f7f"              
}

def map_to_area(subject: str) -> str:
    """Mapeia uma matéria normalizada para uma área de conhecimento."""
    return AREA_MAP.get(subject, "Não Classificado")

def normalize_subject(raw_subject: str) -> str:
    """
    Verifica se uma string bruta está no array de variações
    e a substitui pela chave normalizada correspondente.
    """
    if not isinstance(raw_subject, str):
        return raw_subject  
    
    cleaned_subject = raw_subject.strip().lower()

    for correct_name, variations in SUBJECT_MAP.items():
        if cleaned_subject in variations:
            return correct_name  

    return cleaned_subject.title()