# layout.py
import streamlit as st
from filtros import aplicar_filtros_sidebar

def exibir_sidebar(df):
    with st.sidebar:
        st.image("logo_p2_10bpm.png", width=80)
        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#dc3545;'>🔎 Filtros</h4>", unsafe_allow_html=True)
        cidades, categorias, anos, meses = aplicar_filtros_sidebar(df)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("### 🧭 Navegação")
        st.markdown("""
            <ul style='list-style:none; padding-left:0;'>
                <li>⏳ <span style='color:#444;'>Dias sem Mortes</span></li>
                <li>🔢 <span style='color:#444;'>Total por Cidade</span></li>
                <li>📈 <span style='color:#444;'>Comparativo Ano</span></li>
                <li>📊 <span style='color:#444;'>Comparativo Mês</span></li>
                <li>📅 <span style='color:#444;'>Datas Detalhadas</span></li>
            </ul>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("<small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>", unsafe_allow_html=True)

    return cidades, categorias, anos, meses
