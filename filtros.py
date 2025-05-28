import streamlit as st

def aplicar_filtros_sidebar(df):
    cidades_10bpm = [
        "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
        "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
        "Belém", "Tanque d Arca", "Maribondo"
    ]

    with st.sidebar:
        st.image("logo_p2_10bpm.png", width=150)
        st.markdown("---")
        st.markdown("### 🧭 Navegação")
        st.markdown("[⏳ Dias sem Mortes](#dias_sem_mortes)", unsafe_allow_html=True)
        st.markdown("[🔢 Total por Cidade](#total_cidade)", unsafe_allow_html=True)
        st.markdown("[📈 Comparativo Ano](#comparativo_ano)", unsafe_allow_html=True)
        st.markdown("[📊 Comparativo Mês](#comparativo_mes)", unsafe_allow_html=True)
        st.markdown("[📅 Datas Detalhadas](#datas_detalhes)", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### 🔍 Filtros")
        usar_cidades_10bpm = st.checkbox("Usar cidades do 10º BPM", value=True)

        cidades = sorted(df["CIDADE FATO"].dropna().unique())
        cidades_selecionadas = cidades_10bpm if usar_cidades_10bpm else cidades
        cidades = st.multiselect("Selecionar Cidades", cidades, default=[c for c in cidades_10bpm if c in cidades])

        categorias = st.multiselect("Selecionar Categorias", sorted(df["CATEGORIA"].dropna().unique()), default=sorted(df["CATEGORIA"].dropna().unique()))
        anos = st.multiselect("Selecionar Anos", options=sorted(df["Ano"].dropna().unique().tolist()), default=sorted(df["Ano"].dropna().unique().tolist()))

        nomes_meses_ptbr = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        meses = st.multiselect("Selecionar Mês (opcional)", options=sorted(df["Mes"].dropna().unique().tolist()), format_func=lambda x: nomes_meses_ptbr[x - 1], default=[])

        if st.button("🧹 Limpar Filtros"):
            st.experimental_rerun()

        st.markdown("---")
        st.markdown("<p style='font-size:10px; text-align:center;'>Criado por Analista de Campo - codinome <b>Falcão</b></p>", unsafe_allow_html=True)

    return cidades, categorias, anos, meses
