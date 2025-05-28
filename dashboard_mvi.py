# 📁 Estrutura modular proposta
# ├── app.py                <- Arquivo principal (interface)
# ├── filtros.py            <- Filtros e lógica de seleção
# ├── dados.py              <- Funções de carregamento e transformação de dados
# ├── autenticacao.py       <- Controle de acesso
# ├── estilo.py             <- CSS customizado
# ├── exportacao.py         <- Exportação de dados para Excel
# └── analises.py           <- Exibição de tabelas e comparativos

# ===========================================
# dashboard_mvi.py (Arquivo principal)
# ===========================================
import streamlit as st
from dados import carregar_dados
from filtros import aplicar_filtros_sidebar
from autenticacao import autenticar
from estilo import aplicar_css_personalizado
from exportacao import to_excel
from analises import (
    mostrar_dias_sem_morte,
    mostrar_total_por_cidade,
    mostrar_comparativo_ano,
    mostrar_comparativo_mes
)
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")
aplicar_css_personalizado()

# 🔐 Autenticação
if not autenticar():
    st.stop()

# 📊 Carregamento de dados
df = carregar_dados()
if df.empty:
    st.stop()

# 📊 Filtros
cidades, categorias, anos, meses = aplicar_filtros_sidebar(df)

# ✅ Menu lateral com logo e navegação
with st.sidebar:
    st.image("logo_p2_10bpm.png", width=90)
    st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#dc3545;'>🧭 Navegação</h4>", unsafe_allow_html=True)
    st.markdown("<ul style='list-style:none; padding-left:0'>" +
        "<li><a href='#dias_sem_mortes'>⏳ Dias sem Mortes</a></li>" +
        "<li><a href='#total_cidade'>🔢 Total por Cidade</a></li>" +
        "<li><a href='#comparativo_ano'>📈 Comparativo Ano</a></li>" +
        "<li><a href='#comparativo_mes'>📊 Comparativo Mês</a></li>" +
        "<li><a href='#datas_detalhadas'>📅 Datas Detalhadas</a></li>" +
        "</ul>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
    st.markdown("<small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>", unsafe_allow_html=True)

# 🔎 Aplicando filtros
df_filtrado = df[df["CIDADE FATO"].isin(cidades) & df["Ano"].isin(anos) & df["CATEGORIA"].isin(categorias)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(meses)]

# 📊 Exibição das Tabelas
st.markdown("<div id='dias_sem_mortes'></div>", unsafe_allow_html=True)
mostrar_dias_sem_morte(df, cidades)

st.markdown("<div id='total_cidade'></div>", unsafe_allow_html=True)
mostrar_total_por_cidade(df_filtrado, cidades)

st.markdown("<div id='comparativo_ano'></div>", unsafe_allow_html=True)
mostrar_comparativo_ano(df_filtrado, cidades)

st.markdown("<div id='comparativo_mes'></div>", unsafe_allow_html=True)
mostrar_comparativo_mes(df_filtrado, cidades, anos, meses)

# 📥 Botão exportar
st.download_button("📅 Baixar Tabelas em Excel", data=to_excel({"Dados Filtrados": df_filtrado}), file_name="dados_filtrados.xlsx")

st.markdown("<div id='datas_detalhadas'></div>", unsafe_allow_html=True)
