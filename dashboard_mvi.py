# ✅ Importações
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from pathlib import Path

# ⚠️ DEVE vir antes de qualquer outro comando do Streamlit
st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")

# ✅ Carrega e aplica o CSS customizado
def aplicar_css_personalizado():
    caminho_css = "style.css"
    if Path(caminho_css).exists():
        with open(caminho_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

aplicar_css_personalizado()

# 🛡️ LOGIN
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

    
# ✅ Carrega e aplica o CSS customizado
def aplicar_css_personalizado():
    caminho_css = "style.css"
    if Path(caminho_css).exists():
        with open(caminho_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

aplicar_css_personalizado()



# 📅 Data da última modificação da planilha
caminho_arquivo = Path("Tabela_de_MVI_2024_2025.xlsx")
data_modificacao = datetime.fromtimestamp(caminho_arquivo.stat().st_mtime).strftime("%d/%m/%Y")

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
    RELATÓRIO DE INTELIGÊNCIA
</div>
<div style="text-align: center; font-size: 14px;">
    Última atualização da planilha: <strong>{data_modificacao}</strong>
</div>
""", unsafe_allow_html=True)

# 📊 Carregamento e preparo dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Tabela_de_MVI_2024_2025.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["DATA FATO"] = pd.to_datetime(df["DATA FATO"], dayfirst=True, errors="coerce")
    df["Ano"] = df["DATA FATO"].dt.year
    df["Mes"] = df["DATA FATO"].dt.month
    df["Mes_Nome"] = df["DATA FATO"].dt.strftime('%B')
    df = df.drop_duplicates(subset=["DATA FATO", "NOME VITIMA", "CIDADE FATO", "CATEGORIA"])
    return df

df = carregar_dados()

# 🎯 Filtros
cidades_10bpm = [
    "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
    "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
    "Belém", "Tanque d Arca", "Maribondo"
]
cidades = st.multiselect("Selecionar Cidades", sorted(df["CIDADE FATO"].unique()), default=[c for c in cidades_10bpm if c in df["CIDADE FATO"].unique()])
categorias = st.multiselect("Selecionar Categorias", sorted(df["CATEGORIA"].unique()), default=sorted(df["CATEGORIA"].unique()))
anos = st.multiselect("Selecionar Anos", options=sorted(df["Ano"].dropna().unique().tolist()), default=sorted(df["Ano"].dropna().unique().tolist()))

nomes_meses_ptbr = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
meses = st.multiselect("Selecionar Mês (opcional)", options=sorted(df["Mes"].dropna().unique().tolist()), format_func=lambda x: nomes_meses_ptbr[x - 1], default=[])

df_filtrado = df[df["CIDADE FATO"].isin(cidades) & df["Ano"].isin(anos) & df["CATEGORIA"].isin(categorias)]
if meses:
    df_filtrado = df_filtrado[df_filtrado["Mes"].isin(meses)]

# 📌 Tabela 2:Tabela Total
tabela_total = df_filtrado.groupby(["CIDADE FATO", "CATEGORIA"]).size().reset_index(name="Total")
st.markdown("### 🔢 Total por Cidade e Categoria")
st.markdown(tabela_total.style.set_properties(**{'text-align': 'center'}).hide(axis='index').to_html(), unsafe_allow_html=True)

# 📆 Dias sem Mortes
hoje = pd.to_datetime(datetime.now().date())
ultimas_mortes = df_filtrado.groupby("CIDADE FATO")["DATA FATO"].max().reset_index()
ultimas_mortes["Dias_Sem_Mortes"] = (hoje - ultimas_mortes["DATA FATO"]).dt.days
quantitativo = df_filtrado.groupby("CIDADE FATO").size().reset_index(name="Total_Ocorrencias")
dias_sem_morte = pd.merge(quantitativo, ultimas_mortes, on="CIDADE FATO").rename(columns={"DATA FATO": "Ultima_Morte"})
st.markdown("### ⏳ Dias sem Mortes por Cidade")
st.markdown(dias_sem_morte.style.format({"Dias_Sem_Mortes": "{:.0f}"}).set_properties(**{'text-align': 'center'}).hide(axis='index').to_html(), unsafe_allow_html=True)

# Tabela 3: Comparativo CVLI Ano a Ano
df_cvli = df_filtrado[df_filtrado["CATEGORIA"] == "CVLI"]
cvli_por_ano = df_cvli.groupby(["CIDADE FATO", "Ano"]).size().reset_index(name="Total")
cvli_pivot = cvli_por_ano.pivot(index="CIDADE FATO", columns="Ano", values="Total").fillna(0).astype(int)

anos_disp = sorted(cvli_pivot.columns.tolist())
for i in range(1, len(anos_disp)):
    ant, atual = anos_disp[i - 1], anos_disp[i]
    col_var = f"% Variação {ant}-{atual}"
    cvli_pivot[col_var] = ((cvli_pivot[atual] - cvli_pivot[ant]) / cvli_pivot[ant].replace(0, 1)) * 100
    cvli_pivot[col_var] = cvli_pivot[col_var].round(0).astype(int)

cvli_pivot = cvli_pivot.reset_index()

st.markdown("### 📈 Comparativo CVLI Ano a Ano")
col_anos = [col for col in cvli_pivot.columns if isinstance(col, int)]
col_var = [col for col in cvli_pivot.columns if isinstance(col, str) and "Variação" in col]

st.markdown(
    cvli_pivot.style
    .format({**{col: "{:.0f}" for col in col_anos + col_var}})
    .set_properties(**{'text-align': 'center'})
    .hide(axis='index')
    .to_html(),
    unsafe_allow_html=True
)

# 📊 Comparativo CVLI Mês a Mês
# Tabela 4: Comparativo CVLI Mês a Mês
if len(anos) > 1:
    cvli_mes = df_cvli.groupby(["CIDADE FATO", "Ano", "Mes"]).size().reset_index(name="Total")
    cvli_mes_pivot = cvli_mes.pivot(index=["CIDADE FATO", "Mes"], columns="Ano", values="Total").fillna(0).astype(int)

    anos_mes = sorted([col for col in cvli_mes_pivot.columns if isinstance(col, int)])
    for i in range(1, len(anos_mes)):
        ant, atual = anos_mes[i - 1], anos_mes[i]
        col_var = f"% Variação {ant}-{atual}"
        cvli_mes_pivot[col_var] = ((cvli_mes_pivot[atual] - cvli_mes_pivot[ant]) / cvli_mes_pivot[ant].replace(0, 1)) * 100
        cvli_mes_pivot[col_var] = cvli_mes_pivot[col_var].round(0).astype(int)

    cvli_mes_pivot = cvli_mes_pivot.reset_index()

    st.markdown("### 📊 Comparativo CVLI Mês a Mês")
    col_anos_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, int)]
    col_var_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, str) and "Variação" in col]

    st.markdown(
        cvli_mes_pivot.style
        .format({**{col: "{:.0f}" for col in col_anos_mes + col_var_mes}})
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
