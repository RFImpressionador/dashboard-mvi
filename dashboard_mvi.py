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

if not autenticar():
    st.stop()

df = carregar_dados()
if df.empty:
    st.stop()

# 📊 Filtros
cidades, categorias, anos, meses = aplicar_filtros_sidebar(df)

# 🔎 Aplicando filtros
df_filtrado = df[df["CIDADE FATO"].isin(cidades) & df["Ano"].isin(anos) & df["CATEGORIA"].isin(categorias)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(meses)]

# 📊 Exibição das Tabelas
mostrar_dias_sem_morte(df_filtrado, cidades)
mostrar_total_por_cidade(df_filtrado, cidades)
mostrar_comparativo_ano(df_filtrado, cidades)
mostrar_comparativo_mes(df_filtrado, cidades, anos, meses)

# 📥 Botão exportar
st.download_button("📅 Baixar Tabelas em Excel", data=to_excel({"Dados Filtrados": df_filtrado}), file_name="dados_filtrados.xlsx")
