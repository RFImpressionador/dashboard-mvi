import streamlit as st

def aplicar_filtros_sidebar(df):
    st.sidebar.header("🔎 Filtros")

    cidades_10bpm = [
        "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
        "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
        "Belém", "Tanque d Arca", "Maribondo"
    ]

    usar_10bpm = st.sidebar.checkbox("Usar cidades do 10º BPM", value=True)
    if usar_10bpm:
        cidades = [c for c in cidades_10bpm if c in df["CIDADE FATO"].unique()]
    else:
        cidades = st.sidebar.multiselect("Selecionar Cidades", sorted(df["CIDADE FATO"].dropna().unique()))

    categorias = st.sidebar.multiselect(
        "Selecionar Categorias",
        sorted(df["CATEGORIA"].dropna().unique()),
        default=sorted(df["CATEGORIA"].dropna().unique())
    )

    anos_disponiveis = df[df["CIDADE FATO"].isin(cidades)]["Ano"].dropna().unique()
    anos = st.sidebar.multiselect(
        "Selecionar Anos",
        sorted(anos_disponiveis),
        default=sorted(anos_disponiveis)
    )

    nomes_meses_ptbr = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    meses = st.sidebar.multiselect(
        "Selecionar Mês (opcional)",
        options=sorted(df["Mes"].dropna().unique().tolist()),
        format_func=lambda x: nomes_meses_ptbr[x - 1],
        default=[]
    )

    if st.sidebar.button("🧹 Limpar Filtros"):
        st.session_state.clear()
        st.rerun()

    return cidades, categorias, anos, meses
