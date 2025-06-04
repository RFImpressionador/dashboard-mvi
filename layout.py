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
       # st.markdown(\"\"\"<ul style='list-style:none; padding-left:0;'>...\"\"\", unsafe_allow_html=True)
st.markdown("""
            <ul style='list-style:none; padding-left:0;'>
                <li>⏳ <a href="#dias-sem-mortes-por-cidade" style="text-decoration: none; color: white;">Dias sem Mortes</a></li>
                <li>🔢 <a href="#total-por-cidade-e-categoria" style="text-decoration: none; color: white;">Total por Cidade</a></li>
                <li>📈 <a href="#comparativo-cvli-ano-a-ano" style="text-decoration: none; color: white;">Comparativo Ano</a></li>
                <li>📊 <a href="#comparativo-cvli-mes-a-mes" style="text-decoration: none; color: white;">Comparativo Mês</a></li>
                <li>🗕️ <a href="#datas-e-dias-da-semana-por-cidade" style="text-decoration: none; color: white;">Datas Detalhadas</a></li>
            </ul>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("<small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>", unsafe_allow_html=True)

    return cidades, categorias, anos, meses
