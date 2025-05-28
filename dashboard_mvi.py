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

# ✅ Menu lateral (logo, filtros e navegação)
with st.sidebar:
    st.markdown("""
        <div style='text-align: center;'>
            <img src='logo_p2_10bpm.png' width='80' style='border-radius: 50%; display:block; margin:auto;'>
        </div>
        <hr style='border-top: 1px solid #aaa;'>
        <h4 style='color:#dc3545;'>🔎 Filtros</h4>
    """, unsafe_allow_html=True)
    cidades, categorias, anos, meses = aplicar_filtros_sidebar(df)

    st.markdown("""
        <hr style='border-top: 1px solid #aaa;'>
        <h4 style='color:#dc3545;'>🧽 Navegação</h4>
        <ul style='list-style: none; padding-left: 0;'>
            <li>⏳ <a href="#dias-sem-mortes-por-cidade" style="text-decoration: none; color: white;">Dias sem Mortes</a></li>
            <li>🔢 <a href="#total-por-cidade-e-categoria" style="text-decoration: none; color: white;">Total por Cidade</a></li>
            <li>📈 <a href="#comparativo-cvli-ano-a-ano" style="text-decoration: none; color: white;">Comparativo Ano</a></li>
            <li>📊 <a href="#comparativo-cvli-mes-a-mes" style="text-decoration: none; color: white;">Comparativo Mês</a></li>
            <li>🗕️ <a href="#datas-e-dias-da-semana-por-cidade" style="text-decoration: none; color: white;">Datas Detalhadas</a></li>
        </ul>
        <hr style='border-top: 1px solid #aaa;'>
        <small style='color:gray;'>Criado por Analista de Campo — Codinome: <strong>Falcão</strong></small>
    """, unsafe_allow_html=True)

# 🔎 Aplicando filtros
df_filtrado = df[df["CIDADE FATO"].isin(cidades) & df["Ano"].isin(anos) & df["CATEGORIA"].isin(categorias)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(meses)]

# 📊 Exibição das Tabelas
st.markdown("<div style='margin-top: -40px'></div>", unsafe_allow_html=True)
mostrar_dias_sem_morte(df, cidades)
mostrar_total_por_cidade(df_filtrado, cidades)

if len(anos) >= 2:
    mostrar_comparativo_ano(df_filtrado, cidades)
elif len(anos) == 1:
    mostrar_comparativo_mes(df_filtrado, cidades, anos, meses)

# 📅 Botão exportar
st.download_button("🗓️ Baixar Tabelas em Excel", data=to_excel({"Dados Filtrados": df_filtrado}), file_name="dados_filtrados.xlsx")
