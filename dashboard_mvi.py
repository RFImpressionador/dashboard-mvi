# ✅ Importações
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from pathlib import Path
import requests

# ⚠️ Configura a página antes de qualquer outro comando do Streamlit
st.set_page_config(page_title="Análise MVI 10º BPM", layout="wide")

# ✅ Aplica o CSS customizado, se existir
def aplicar_css_personalizado():
    caminho_css = "style.css"
    if Path(caminho_css).exists():
        with open(caminho_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

aplicar_css_personalizado()

# 🔐 Função de login simples
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

# 📅 Texto fixo indicando atualização da planilha
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

# 📊 Carrega os dados da planilha do Google Drive em tempo real
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

# 🔄 Botão de recarregamento manual
if st.button("🔄 Atualizar dados da planilha"):
    st.cache_data.clear()

df = carregar_dados()
if df.empty:
    st.stop()

# 📊 Tabela 4: Comparativo CVLI Mês a Mês (BLOCO CORRIGIDO)
if len(df["Ano"].dropna().unique()) > 1:
    cidades = sorted(df["CIDADE FATO"].dropna().unique())
    anos = sorted(df["Ano"].dropna().unique())
    meses = sorted(df["Mes"].dropna().unique())

    meses_filtrados = meses if meses else list(range(1, 13))

    todas_combinacoes = pd.MultiIndex.from_product(
        [cidades, anos, meses_filtrados],
        names=["CIDADE FATO", "Ano", "Mes"]
    )

    df_cvli = df[df["CATEGORIA"] == "CVLI"]
    cvli_mes = df_cvli.groupby(["CIDADE FATO", "Ano", "Mes"]).size().reset_index(name="Total")

    cvli_mes = cvli_mes.set_index(["CIDADE FATO", "Ano", "Mes"]).reindex(todas_combinacoes, fill_value=0).reset_index()
    cvli_mes_pivot = cvli_mes.pivot(index=["CIDADE FATO", "Mes"], columns="Ano", values="Total").fillna(0).astype(int)

    anos_mes = sorted([col for col in cvli_mes_pivot.columns if isinstance(col, int)])
    for i in range(1, len(anos_mes)):
        ant, atual = anos_mes[i - 1], anos_mes[i]
        col_var = f"% Variação {ant}-{atual}"
        cvli_mes_pivot[col_var] = ((cvli_mes_pivot[atual] - cvli_mes_pivot[ant]) / cvli_mes_pivot[ant].replace(0, 1)) * 100
        cvli_mes_pivot[col_var] = cvli_mes_pivot[col_var].round(0).astype(int)

    cvli_mes_pivot = cvli_mes_pivot.reset_index()
    cvli_mes_pivot = cvli_mes_pivot.sort_values("CIDADE FATO")

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
