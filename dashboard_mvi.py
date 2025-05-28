# ✅ Importações
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from pathlib import Path
import requests

# ⚠️ Configuração da página
st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")

# ✅ CSS customizado
def aplicar_css_personalizado():
    caminho_css = "style.css"
    if Path(caminho_css).exists():
        with open(caminho_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

aplicar_css_personalizado()

# 🏡 Autenticação simples
def autenticar():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if not st.session_state.autenticado:
        st.title("🔐 Painel Protegido")
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha == "pmal2025":
            st.session_state.autenticado = True
            st.success("✅ Acesso liberado!")
            st.rerun()
        elif senha:
            st.error("❌ Senha incorreta.")
        return False
    return True

if not autenticar():
    st.stop()

# 📅 Data fictícia
data_modificacao = "Atualização automática via Google Sheets"

# 🚨 Cabeçalho institucional
st.markdown(f"""
<div style="text-align: center; color: red; font-weight: bold; border: 2px solid red; padding: 5px;">
CONHECIMENTO PARA ASSESSORAMENTO DO PROCESSO DECISÓRIO, NÃO TENDO FINALIDADE PROBATÓRIA...
</div>
<div style="text-align: center; color: red; font-weight: bold; border: 2px solid red; padding: 5px; margin-top: 5px;">
ACESSO RESTRITO
</div>
<br>
<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/RFImpressionador/dashboard-mvi/main/logo_p2_10bpm.png" width="90">
</div>
<br>
<div style="text-align: center; font-weight: bold;">
    ESTADO DE ALAGOAS<br>
    SECRETARIA DE SEGURANÇA PÚBLICA<br>
    POLÍCIA MILITAR DE ALAGOAS<br>
    COMANDO DE POLICIAMENTO DA REGIÃO DO AGRESTE (CPRA)<br>
    CISP II – 10º BATALHÃO DE POLÍCIA MILITAR (10º BPM)<br>
    <a href="mailto:p2.10bpm@pm.al.gov.br">p2.10bpm@pm.al.gov.br</a>
</div>
<br>
<div style="text-align: center; font-size: 20px; font-weight: bold;">
    RELATÓRIO DE INTELIGÊNCIA - CVLI
</div>
<div style="text-align: center; font-size: 14px;">
    Última atualização da planilha: <strong>{data_modificacao}</strong>
</div>
""", unsafe_allow_html=True)

# 📊 Carregamento de dados
@st.cache_data
def carregar_dados():
    try:
        file_id = "1MNuLlWj6XFHsVgtrp4aUyitApFnFpP5s"
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        resposta = requests.get(url)
        resposta.raise_for_status()
        arquivo = BytesIO(resposta.content)
        df = pd.read_excel(arquivo, engine="openpyxl")
        df.columns = [col.strip() for col in df.columns]
        df["DATA FATO"] = pd.to_datetime(df["DATA FATO"], dayfirst=True, errors="coerce")
        df["Ano"] = df["DATA FATO"].dt.year
        df["Mes"] = df["DATA FATO"].dt.month
        df["Mes_Nome"] = df["DATA FATO"].dt.strftime('%B')
        df = df.drop_duplicates(subset=["DATA FATO", "NOME VITIMA", "CIDADE FATO", "CATEGORIA"])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

if st.button("🔄 Atualizar dados da planilha"):
    st.cache_data.clear()

df = carregar_dados()
if df.empty:
    st.stop()

# Aqui entram os filtros e as três tabelas com merge reindexando as cidades selecionadas,
# como explicado na resposta anterior.


cidades_10bpm = [
    "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
    "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
    "Belém", "Tanque d Arca", "Maribondo"
]
cidades = st.multiselect("Selecionar Cidades", sorted(df["CIDADE FATO"].dropna().unique()), default=[c for c in cidades_10bpm if c in df["CIDADE FATO"].unique()])
categorias = st.multiselect("Selecionar Categorias", sorted(df["CATEGORIA"].dropna().unique()), default=sorted(df["CATEGORIA"].dropna().unique()))
anos = st.multiselect("Selecionar Anos", options=sorted(df["Ano"].dropna().unique().tolist()), default=sorted(df["Ano"].dropna().unique().tolist()))

nomes_meses_ptbr = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
meses = st.multiselect("Selecionar Mês (opcional)", options=sorted(df["Mes"].dropna().unique().tolist()), format_func=lambda x: nomes_meses_ptbr[x - 1], default=[])

df["Dia_Semana"] = df["DATA FATO"].dt.day_name()

dias_semana_disponiveis = df["Dia_Semana"].dropna().unique().tolist()
dias_semana = st.multiselect("Filtrar por Dia da Semana (opcional)", options=sorted(dias_semana_disponiveis), default=[])

if dias_semana:
    df_filtrado = df_filtrado[df_filtrado["Dia_Semana"].isin(dias_semana)]

# 🔎 Aplicando filtros
df_filtrado = df[df["CIDADE FATO"].isin(cidades) & df["Ano"].isin(anos) & df["CATEGORIA"].isin(categorias)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(meses)]

# A partir daqui todo o restante (tabelas, comparativos, exportações) continua funcionando normal ✅

# ⚠️ Lembre-se de instalar o pacote necessário se ainda não tiver:
# pip install openpyxl

# 📆 Tabela 1 Dias sem Mortes — filtrando apenas CVLI e as cidades selecionadas
df_cvli_geral = df[(df["CATEGORIA"] == "CVLI") & (df["CIDADE FATO"].isin(cidades))]

# Última data de morte por cidade (pode estar ausente)
ultimas_mortes = df_cvli_geral.groupby("CIDADE FATO")["DATA FATO"].max()

# Preenche com None para cidades sem mortes registradas
ultimas_mortes = ultimas_mortes.reindex(cidades)

# Cria DataFrame com os cálculos
dias_sem_morte = ultimas_mortes.reset_index().rename(columns={"DATA FATO": "Ultima_Morte"})
dias_sem_morte["Dias_Sem_Mortes"] = dias_sem_morte["Dias_Sem_Mortes"].fillna("Sem registro")
dias_sem_morte = dias_sem_morte.sort_values("CIDADE FATO")  # 🔠 Ordena por cidade

# Formata datas e lida com cidades sem mortes (NaT)
dias_sem_morte["Ultima_Morte"] = dias_sem_morte["Ultima_Morte"].dt.strftime("%d/%m/%Y %H:%M").fillna("Sem registro")
dias_sem_morte["Dias_Sem_Mortes"] = dias_sem_morte["Dias_Sem_Mortes"].fillna("Sem registro")

# 🖼️ Exibe a tabela formatada
st.markdown("### ⏳ Dias sem Mortes por Cidade")
st.markdown(
    dias_sem_morte
    .style.set_properties(**{'text-align': 'center'})
    .hide(axis='index')
    .to_html(),
    unsafe_allow_html=True
)


# 📌 Tabela 2:Tabela Total — mostrando todas as cidades mesmo com 0
tabela_total = (
    df_filtrado
    .groupby(["CIDADE FATO", "CATEGORIA"])
    .size()
    .unstack(fill_value=0)
    .reindex(index=cidades, fill_value=0)
    .stack()
    .reset_index(name="Total")
)

tabela_total = tabela_total.sort_values("CIDADE FATO")  # 🔠 Ordena por cidade

st.markdown("### 🔢 Total por Cidade e Categoria")
st.markdown(
    tabela_total
    .style.set_properties(**{'text-align': 'center'})
    .hide(axis='index')
    .to_html(),
    unsafe_allow_html=True
)

# Tabela 3: Comparativo CVLI Ano a Ano
df_cvli = df_filtrado[df_filtrado["CATEGORIA"] == "CVLI"]
cvli_por_ano = df_cvli.groupby(["CIDADE FATO", "Ano"]).size().unstack(fill_value=0)
cvli_por_ano = cvli_por_ano.reindex(index=cidades, fill_value=0)

anos_disp = sorted(cvli_por_ano.columns.tolist())
for i in range(1, len(anos_disp)):
    ant, atual = anos_disp[i - 1], anos_disp[i]
    col_var = f"% Variação {ant}-{atual}"
    cvli_por_ano[col_var] = ((cvli_por_ano[atual] - cvli_por_ano[ant]) / cvli_por_ano[ant].replace(0, 1)) * 100
    cvli_por_ano[col_var] = cvli_por_ano[col_var].round(0).astype(int)

cvli_pivot = cvli_por_ano.reset_index()
cvli_pivot = cvli_pivot.sort_values("CIDADE FATO")  # 🔠 Ordena por cidade


st.markdown("### 📈 Comparativo CVLI Ano a Ano")
col_anos = [col for col in cvli_pivot.columns if isinstance(col, int)]
col_var = [col for col in cvli_pivot.columns if isinstance(col, str) and "Variação" in col]

st.markdown(
    cvli_pivot
    .style.format({**{col: "{:.0f}" for col in col_anos + col_var}})
    .set_properties(**{'text-align': 'center'})
    .hide(axis='index')
    .to_html(),
    unsafe_allow_html=True
)

# 📊 Tabela 4 Comparativo CVLI Mês a Mês
if len(anos) > 1:
    meses_filtrados = sorted(meses) if meses else list(range(1, 13))

    # Gera todas as combinações possíveis de cidades, anos e meses (de acordo com filtro)
    todas_combinacoes = pd.MultiIndex.from_product(
        [cidades, anos, meses_filtrados],
        names=["CIDADE FATO", "Ano", "Mes"]
    )

    # Filtra os dados
    df_cvli = df_filtrado[df_filtrado["CATEGORIA"] == "CVLI"]
    cvli_mes = df_cvli.groupby(["CIDADE FATO", "Ano", "Mes"]).size().reset_index(name="Total")

    # Reindexa com todas as combinações
    cvli_mes = cvli_mes.set_index(["CIDADE FATO", "Ano", "Mes"]).reindex(todas_combinacoes, fill_value=0).reset_index()

    # Faz pivot para visualização
    cvli_mes_pivot = cvli_mes.pivot(index=["CIDADE FATO", "Mes"], columns="Ano", values="Total").fillna(0).astype(int)

    # Calcula variações percentuais entre os anos selecionados
    anos_mes = sorted([col for col in cvli_mes_pivot.columns if isinstance(col, int)])
    for i in range(1, len(anos_mes)):
        ant, atual = anos_mes[i - 1], anos_mes[i]
        col_var = f"% Variação {ant}-{atual}"
        cvli_mes_pivot[col_var] = ((cvli_mes_pivot[atual] - cvli_mes_pivot[ant]) / cvli_mes_pivot[ant].replace(0, 1)) * 100
        cvli_mes_pivot[col_var] = cvli_mes_pivot[col_var].round(0).astype(int)

    # Exibir tabela
    cvli_mes_pivot = cvli_mes_pivot.reset_index()
cvli_mes_pivot = cvli_mes_pivot.sort_values("CIDADE FATO")  # 🔠 Ordena por cidade

    st.markdown("### 📊 Comparativo CVLI Mês a Mês")
    col_anos_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, int)]
    col_var_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, str) and "Variação" in col]

    st.markdown(
        cvli_mes_pivot
        .style.format({**{col: "{:.0f}" for col in col_anos_mes + col_var_mes}})
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )


# 📥 Exportação
def to_excel(dfs: dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    output.seek(0)
    return output

st.download_button("📥 Baixar Todas as Tabelas em Excel", data=to_excel({
    "Total_Cidade_Categoria": tabela_total,
    "Comparativo_CVLI": cvli_pivot,
    "Dias_Sem_Mortes": dias_sem_morte
}), file_name="Dash_MVI_Tabelas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
