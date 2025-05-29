# layout.py
import streamlit as st
from filtros import aplicar_filtros_sidebar

def exibir_sidebar(df):
    with st.sidebar:
        st.markdown("""
            <style>
            div[data-baseweb="tag"] {
                background-color: #00c8c8 !important;
                color: #1e1e2f !important;
                font-weight: bold;
                border-radius: 6px;
                padding: 4px 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.image("logo_p2_10bpm.png", width=80)
        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#dc3545;'>🔎 Filtros</h4>", unsafe_allow_html=True)

        cidades, categorias, anos, meses = aplicar_filtros_sidebar(df)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("### 🧭 Navegação")
        st.markdown(\"\"\"<ul style='list-style:none; padding-left:0;'>...\"\"\", unsafe_allow_html=True)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("<small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>", unsafe_allow_html=True)

    return cidades, categorias, anos, meses
