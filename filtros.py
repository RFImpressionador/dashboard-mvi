import streamlit as st

def aplicar_filtros_sidebar(df):
    cidades_10bpm = [
        "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
        "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
        "Belém", "Tanque d Arca", "Maribondo"
    ]

    cidades = st.multiselect(
        "Selecionar Cidades",
        sorted(df["CIDADE FATO"].dropna().unique()),
        default=[c for c in cidades_10bpm if c in df["CIDADE FATO"].unique()]
    )

    categorias = st.multiselect(
        "Selecionar Categorias",
        sorted(df["CATEGORIA"].dropna().unique()),
        default=sorted(df["CATEGORIA"].dropna().unique())
    )

    anos = st.multiselect(
        "Selecionar Anos",
        options=sorted(df["Ano"].dropna().unique().tolist()),
        default=sorted(df["Ano"].dropna().unique().tolist())
    )

    nomes_meses_ptbr = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    meses = st.multiselect(
        "Selecionar Mês (opcional)",
        options=sorted(df["Mes"].dropna().unique().tolist()),
        format_func=lambda x: nomes_meses_ptbr[int(x) - 1],
        default=[]
    )

    return cidades, categorias, anos, meses
