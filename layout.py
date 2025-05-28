# layout.py
import streamlit as st

def montar_sidebar():
    with st.sidebar:
        st.image("logo_p2_10bpm.png", width=80)
        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)

        # Filtros serão renderizados por filtros.py
        st.markdown("<h4 style='color:#dc3545;'>🔎 Filtros</h4>", unsafe_allow_html=True)

        # Navegação
        st.markdown("### 🧽 Navegação")
        st.markdown("""
            <ul style='list-style:none; padding-left:0;'>
                <li>⏳ <span style='color:#ccc;'>Dias sem Mortes</span></li>
                <li>🕢 <span style='color:#ccc;'>Total por Cidade</span></li>
                <li>📈 <span style='color:#ccc;'>Comparativo Ano</span></li>
                <li>📊 <span style='color:#ccc;'>Comparativo Mês</span></li>
                <li>🗕️ <span style='color:#ccc;'>Datas Detalhadas</span></li>
            </ul>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
        st.markdown("<small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>", unsafe_allow_html=True)
