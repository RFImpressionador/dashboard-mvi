# Importações
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from pathlib import Path
import os

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

# ⚠️ A linha abaixo deve ser a PRIMEIRA após autenticação (ANTES de qualquer markdown ou imagem):
st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")

# 📅 Verifica a data da última atualização da planilha
from pathlib import Path
caminho_arquivo = Path("Tabela_de_MVI_2024_2025.xlsx")
data_modificacao = datetime.fromtimestamp(caminho_arquivo.stat().st_mtime).strftime("%d/%m/%Y")

# 🚨 Cabeçalho institucional completo
st.markdown("""
<div style="text-align: center; color: red; font-weight: bold; border: 2px solid red; padding: 5px;">
CONHECIMENTO PARA ASSESSORAMENTO DO PROCESSO DECISÓRIO, NÃO TENDO FINALIDADE PROBATÓRIA. CONFORME PREVISTO NA DNISP, ESTE DOCUMENTO E SEUS ANEXOS NÃO DEVEM SER INSERIDOS EM PROCEDIMENTOS E/OU PROCESSOS DE QUALQUER NATUREZA.
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
    Última atualização da planilha: <strong>{}</strong>
</div>
""".format(data_modificacao), unsafe_allow_html=True)


# ================= DADOS E DASHBOARD =================

# Carrega os dados e prepara colunas de datas
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Tabela_de_MVI_2024_2025.xlsx")
    df.columns = [
        "Index", "ID", "Data_Fato", "Nome_Vitima", "Sexo", "Mae_Vitima", "Cidade", 
        "Bairro", "Categoria", "Subcategoria", "BO_PC", "BO_SISGOU", "CAD"
    ]

    # ✅ Converte "Data_Fato" para datetime completo (corrige dia/mês/ano e hora)
    df["Data_Fato"] = pd.to_datetime(df["Data_Fato"], dayfirst=True, errors="coerce")

    # ✅ Extrai informações de tempo
    df["Ano"] = df["Data_Fato"].dt.year
    df["Mes"] = df["Data_Fato"].dt.month
    df["Mes_Nome"] = df["Data_Fato"].dt.strftime('%B')  # Nome do mês por extenso

    # ✅ Remove duplicatas baseando-se em múltiplas colunas
    df = df.drop_duplicates(subset=["Data_Fato", "Nome_Vitima", "Cidade", "Categoria"])

    return df


df = carregar_dados()
# ✅ Filtro de cidades com todas disponíveis, mas 10º BPM pré-selecionado
cidades_10bpm = [
    "Palmeira dos Índios", "Igaci", "Estrela de Alagoas", "Minador do Negrão",
    "Cacimbinhas", "Quebrangulo", "Paulo Jacinto", "Mar Vermelho",
    "Belém", "Tanque d Arca", "Maribondo"
]
# ✅ Filtro de cidades com todas disponíveis, mas 10º BPM pré-selecionado
cidades = st.multiselect("Selecionar Cidades", sorted(df["Cidade"].unique()), default=[c for c in cidades_10bpm if c in df["Cidade"].unique()])
# ✅ Filtro de anos com todos disponíveis
anos_disponiveis = sorted(df["Ano"].dropna().unique().tolist())

anos = st.multiselect(
    "Selecionar Anos",
    options=anos_disponiveis,
    default=anos_disponiveis  # pré-seleciona todos os anos realmente presentes
)

# ✅ Filtro de categorias com todos disponíveis
categorias = st.multiselect("Selecionar Categorias", sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))
# ✅ Filtro de meses (exibe nomes, usa números internamente)
meses_disponiveis = sorted(df["Mes"].dropna().unique().tolist())

meses = st.multiselect(
    "Selecionar Mês (opcional)",
    options=meses_disponiveis,
    format_func=lambda x: datetime(2023, x, 1).strftime('%B'),
    default=[]
)


filtros = (
    df["Cidade"].isin(cidades) &
    df["Ano"].isin(anos) &
    df["Categoria"].isin(categorias)
)

if meses:  # Só filtra por mês se meses tiver algo
    filtros = filtros & df["Mes"].isin(meses)

df_filtrado = df[filtros]

# Tabela 1
tabela_total = df_filtrado.groupby(["Cidade", "Categoria"]).size().reset_index(name="Total")

# Tabela 2: Comparativo CVLI
df_cvli = df_filtrado[df_filtrado["Categoria"] == "CVLI"]
cvli_por_ano = df_cvli.groupby(["Cidade", "Ano"]).size().reset_index(name="Total")
cvli_pivot = cvli_por_ano.pivot(index="Cidade", columns="Ano", values="Total").fillna(0)
anos_disp = sorted(cvli_pivot.columns.tolist())
for i in range(1, len(anos_disp)):
    ant, atual = anos_disp[i-1], anos_disp[i]
    cvli_pivot[f"% Variação {ant}-{atual}"] = ((cvli_pivot[atual] - cvli_pivot[ant]) / cvli_pivot[ant].replace(0, 1)) * 100
cvli_pivot = cvli_pivot.round(2).reset_index()

# Tabela 3: Dias sem mortes
hoje = pd.to_datetime(datetime.now().date())
ultimas_mortes = df_filtrado.groupby("Cidade")["Data_Fato"].max().reset_index()
ultimas_mortes["Dias_Sem_Mortes"] = (hoje - ultimas_mortes["Data_Fato"]).dt.days
quantitativo = df_filtrado.groupby("Cidade").size().reset_index(name="Total_Ocorrencias")
dias_sem_morte = pd.merge(quantitativo, ultimas_mortes, on="Cidade").rename(columns={"Data_Fato": "Ultima_Morte"})

# Exibição
st.markdown("### 🔢 Total por Cidade e Categoria")
st.markdown(tabela_total.style.set_properties(**{'text-align': 'center'}).hide(axis='index').to_html(), unsafe_allow_html=True)

st.markdown("### 📈 Comparativo CVLI Ano a Ano")
col_variacoes = [col for col in cvli_pivot.columns if isinstance(col, str) and "Variação" in col]
col_anos = [col for col in cvli_pivot.columns if isinstance(col, int)]
st.markdown(cvli_pivot.style.format({col: "{:.0f}" for col in col_anos} | {col: "{:.2f}" for col in col_variacoes}).set_properties(**{'text-align': 'center'}).hide(axis='index').to_html(), unsafe_allow_html=True)

st.markdown("### ⏳ Dias sem Mortes por Cidade")
st.markdown(dias_sem_morte.style.format({"Dias_Sem_Mortes": "{:.0f}"}).set_properties(**{'text-align': 'center'}).hide(axis='index').to_html(), unsafe_allow_html=True)

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
