
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# 🔐 Tela de login com sessão persistente
def autenticar():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔐 Painel Protegido")
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha == "pmal2025":
            st.session_state.autenticado = True
            st.success("✅ Acesso liberado!")
            st.experimental_rerun()
        elif senha:
            st.error("❌ Senha incorreta.")
        return False
    return True

# Bloqueia o acesso se não estiver autenticado
if not autenticar():
    st.stop()
    
#Conterudo após o login 
st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")

st.markdown("## 📊 Análise MVI 10º BPM")
st.markdown("Visualização interativa de Mortes Violentas Intencionais (CVLI) e outras categorias, com filtros e gráficos atualizados.")

@st.cache_data
#Carrega os dados e Elimina Duplicidade da Tabela
def carregar_dados():
    df = pd.read_excel("Tabela_de_MVI_2023_2025.xlsx")
    df.columns = [
        "Index", "ID", "Data_Fato", "Nome_Vitima", "Sexo", "Mae_Vitima", "Cidade", 
        "Bairro", "Categoria", "Subcategoria", "BO_PC", "BO_SISGOU", "CAD"
    ]
    df["Data_Fato"] = pd.to_datetime(df["Data_Fato"], errors='coerce')
    df["Ano"] = df["Data_Fato"].dt.year
    df["Mes"] = df["Data_Fato"].dt.month
    df["Mes_Nome"] = df["Data_Fato"].dt.strftime('%B')
    
    # 🔁 Remover linhas duplicadas com base em colunas principais
    df = df.drop_duplicates(subset=["Data_Fato", "Nome_Vitima", "Cidade", "Categoria"])
    
    return df

df = carregar_dados()

# Filtros
cidades = st.multiselect("Selecionar Cidades", sorted(df["Cidade"].unique()), default=sorted(df["Cidade"].unique()))
anos = st.multiselect("Selecionar Anos", sorted(df["Ano"].dropna().unique()), default=sorted(df["Ano"].dropna().unique()))
categorias = st.multiselect("Selecionar Categorias", sorted(df["Categoria"].unique()), default=sorted(df["Categoria"].unique()))

df_filtrado = df[df["Cidade"].isin(cidades) & df["Ano"].isin(anos) & df["Categoria"].isin(categorias)]

# Tabela 1: Total por cidade e categoria
tabela_total = df_filtrado.groupby(["Cidade", "Categoria"]).size().reset_index(name="Total")

# Tabela 2: Comparativo CVLI ano a ano
df_cvli = df[df["Categoria"] == "CVLI"]
cvli_por_ano = df_cvli.groupby(["Cidade", "Ano"]).size().reset_index(name="Total")
cvli_pivot = cvli_por_ano.pivot(index="Cidade", columns="Ano", values="Total").fillna(0)
anos_disp = sorted(cvli_pivot.columns.tolist())
for i in range(1, len(anos_disp)):
    ant, atual = anos_disp[i-1], anos_disp[i]
    cvli_pivot[f"% Variação {ant}-{atual}"] = (
    ((cvli_pivot[atual] - cvli_pivot[ant]) / cvli_pivot[ant].replace(0, 1)) * 100
).round(2)
cvli_pivot = cvli_pivot.reset_index()

# Tabela 3: Dias sem mortes
hoje = pd.to_datetime(datetime.now().date())
ultimas_mortes = df.groupby("Cidade")["Data_Fato"].max().reset_index()
ultimas_mortes["Dias_Sem_Mortes"] = (hoje - ultimas_mortes["Data_Fato"]).dt.days
quantitativo = df.groupby("Cidade").size().reset_index(name="Total_Ocorrencias")
dias_sem_morte = pd.merge(quantitativo, ultimas_mortes, on="Cidade").rename(columns={"Data_Fato": "Ultima_Morte"})

# Exibição alterada para centralizar 
st.markdown("### 🔢 Total por Cidade e Categoria")
st.markdown(
    tabela_total.style
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
    unsafe_allow_html=True
)

st.markdown("### 📈 Comparativo CVLI Ano a Ano")
st.markdown(
    cvli_pivot.style
        .format("{:.2f}", subset=[col for col in cvli_pivot.columns if "Variação" in col])
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(), 
    unsafe_allow_html=True

st.markdown("### ⏳ Dias sem Mortes por Cidade")
st.markdown(
    dias_sem_morte.style
        .format({"Dias_Sem_Mortes": "{:.0f}"})
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
    unsafe_allow_html=True
)

# Botão para exportar todas as tabelas
def to_excel(dfs: dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    output.seek(0)
    return output

st.download_button(
    label="📥 Baixar Todas as Tabelas em Excel",
    data=to_excel({
        "Total_Cidade_Categoria": tabela_total,
        "Comparativo_CVLI": cvli_pivot,
        "Dias_Sem_Mortes": dias_sem_morte
    }),
    file_name="Dash_MVI_Tabelas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
