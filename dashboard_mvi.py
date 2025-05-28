# ✅ Importações
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
import requests
import plotly.express as px
import plotly.graph_objects as go

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
        
        # Mapeamento manual para nomes dos meses em português
        mapa_meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        df["Mes_Nome"] = df["Mes"].map(mapa_meses)
        
        # Garantir que a coluna CATEGORIA existe
        if "CATEGORIA" not in df.columns:
            st.warning("Coluna 'CATEGORIA' não encontrada. Verificando se existe 'SUBJETIVIDADE' ou similar...")
            # Tentar encontrar colunas alternativas
            for col_alternativa in ["SUBJETIVIDADE", "TIPO", "CLASSIFICACAO"]:
                if col_alternativa in df.columns:
                    df["CATEGORIA"] = df[col_alternativa]
                    st.info(f"Usando coluna '{col_alternativa}' como 'CATEGORIA'")
                    break
            else:
                # Se nenhuma coluna alternativa for encontrada, criar uma padrão
                st.error("Nenhuma coluna de categoria encontrada. Criando coluna padrão 'CVLI'")
                df["CATEGORIA"] = "CVLI"
        
        # Remover duplicatas
        df = df.drop_duplicates(subset=["DATA FATO", "NOME VITIMA", "CIDADE FATO", "CATEGORIA"])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Criar um DataFrame mínimo para evitar erros
        return pd.DataFrame({
            "DATA FATO": [datetime.now()],
            "NOME VITIMA": ["ERRO DE CARREGAMENTO"],
            "CIDADE FATO": ["ERRO"],
            "CATEGORIA": ["ERRO"],
            "Ano": [datetime.now().year],
            "Mes": [datetime.now().month],
            "Mes_Nome": ["Erro"]
        })

# 🔄 Botão de recarregamento manual
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🔄 Atualizar dados da planilha"):
        st.cache_data.clear()
        st.success("Dados atualizados com sucesso!")

df = carregar_dados()

# 📊 Filtros interativos
st.sidebar.header("Filtros")

# Filtro de anos
anos_disponiveis = sorted(df["Ano"].dropna().unique(), reverse=True)
if not anos_disponiveis:
    anos_disponiveis = [datetime.now().year]
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos:",
    options=anos_disponiveis,
    default=anos_disponiveis
)

# Filtro de cidades
cidades_disponiveis = sorted(df["CIDADE FATO"].dropna().unique())
if not cidades_disponiveis:
    cidades_disponiveis = ["Todas"]
cidades_selecionadas = st.sidebar.multiselect(
    "Selecione as cidades:",
    options=cidades_disponiveis,
    default=cidades_disponiveis
)

# Filtro de categorias
categorias_disponiveis = sorted(df["CATEGORIA"].dropna().unique())
if not categorias_disponiveis:
    categorias_disponiveis = ["CVLI"]
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias:",
    options=categorias_disponiveis,
    default=["CVLI"] if "CVLI" in categorias_disponiveis else categorias_disponiveis[:1]
)

# Aplicar filtros
df_filtrado = df.copy()
if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Ano"].isin(anos_selecionados)]
if cidades_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["CIDADE FATO"].isin(cidades_selecionadas)]
if categorias_selecionadas:
    df_filtrado = df_filtrado[df_filtrado["CATEGORIA"].isin(categorias_selecionadas)]

# Verificar se há dados após filtros
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# 📊 Tabela 1: Total por Cidade e Categoria
st.markdown("### 📊 Total por Cidade e Categoria")

# Criar tabela de totais
tabela_total = df_filtrado.groupby(["CIDADE FATO", "CATEGORIA"]).size().reset_index(name="Total")
tabela_total = tabela_total.pivot_table(
    index="CIDADE FATO", 
    columns="CATEGORIA", 
    values="Total", 
    aggfunc="sum",
    fill_value=0
).reset_index()

# Adicionar coluna de total geral
categorias = tabela_total.columns.tolist()[1:]  # Excluir a coluna 'CIDADE FATO'
tabela_total["Total Geral"] = tabela_total[categorias].sum(axis=1)

# Adicionar linha de totais
totais_por_categoria = tabela_total[categorias + ["Total Geral"]].sum().to_frame().T
totais_por_categoria.insert(0, "CIDADE FATO", "TOTAL")
tabela_total = pd.concat([tabela_total, totais_por_categoria], ignore_index=True)

# Exibir tabela formatada
st.dataframe(
    tabela_total.style.background_gradient(cmap="Blues", subset=categorias + ["Total Geral"])
    .format("{:.0f}", subset=categorias + ["Total Geral"])
    .set_properties(**{"text-align": "center"}),
    use_container_width=True
)

# 📊 Tabela 2: Comparativo CVLI Anual
st.markdown("### 📊 Comparativo CVLI Anual")

# Filtrar apenas CVLI
df_cvli = df_filtrado[df_filtrado["CATEGORIA"] == "CVLI"] if "CVLI" in categorias_selecionadas else df_filtrado

# Criar tabela de comparativo anual
cvli_pivot = df_cvli.groupby(["CIDADE FATO", "Ano"]).size().reset_index(name="Total")
cvli_pivot = cvli_pivot.pivot_table(
    index="CIDADE FATO", 
    columns="Ano", 
    values="Total", 
    aggfunc="sum",
    fill_value=0
).reset_index()

# Calcular variações percentuais entre anos
anos_pivot = [col for col in cvli_pivot.columns if isinstance(col, (int, float))]
for i in range(1, len(anos_pivot)):
    ano_atual = anos_pivot[i]
    ano_anterior = anos_pivot[i-1]
    col_var = f"Var % {ano_anterior}-{ano_atual}"
    cvli_pivot[col_var] = cvli_pivot.apply(
        lambda x: ((x[ano_atual] - x[ano_anterior]) / x[ano_anterior] * 100) if x[ano_anterior] > 0 else (
            float('inf') if x[ano_atual] > 0 else 0
        ),
        axis=1
    )
    # Formatar infinito
    cvli_pivot[col_var] = cvli_pivot[col_var].replace([float('inf')], 999)

# Adicionar linha de totais
totais_por_ano = cvli_pivot.drop("CIDADE FATO", axis=1).sum().to_frame().T
totais_por_ano.insert(0, "CIDADE FATO", "TOTAL")
cvli_pivot = pd.concat([cvli_pivot, totais_por_ano], ignore_index=True)

# Colunas de anos e variações
cols_anos = [col for col in cvli_pivot.columns if isinstance(col, (int, float))]
cols_var = [col for col in cvli_pivot.columns if isinstance(col, str) and "Var %" in col]

# Exibir tabela formatada
st.dataframe(
    cvli_pivot.style
    .background_gradient(cmap="Blues", subset=cols_anos)
    .background_gradient(cmap="RdYlGn_r", subset=cols_var)
    .format("{:.0f}", subset=cols_anos)
    .format("{:.1f}%", subset=cols_var)
    .set_properties(**{"text-align": "center"}),
    use_container_width=True
)

# 📊 Tabela 3: Dias Sem Mortes
st.markdown("### 📊 Dias Sem Mortes por Cidade")

# Calcular dias sem mortes
hoje = datetime.now().date()
ultima_data_por_cidade = df_cvli.groupby("CIDADE FATO")["DATA FATO"].max()
dias_sem_morte = pd.DataFrame({
    "CIDADE FATO": ultima_data_por_cidade.index,
    "Última Ocorrência": ultima_data_por_cidade.dt.date,
    "Dias Sem Mortes": [(hoje - data).days for data in ultima_data_por_cidade.dt.date]
})

# Ordenar por dias sem mortes (decrescente)
dias_sem_morte = dias_sem_morte.sort_values("Dias Sem Mortes", ascending=False)

# Exibir tabela formatada
st.dataframe(
    dias_sem_morte.style
    .background_gradient(cmap="Greens", subset=["Dias Sem Mortes"])
    .format({"Última Ocorrência": "{:%d/%m/%Y}", "Dias Sem Mortes": "{:.0f}"})
    .set_properties(**{"text-align": "center"}),
    use_container_width=True
)

# 📊 Tabela 4: Comparativo CVLI Mês a Mês (BLOCO CORRIGIDO)
st.markdown("### 📊 Comparativo CVLI Mês a Mês")

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
    cvli_mes_pivot = cvli_mes_pivot.sort_values(["CIDADE FATO", "Mes"])

    # Substituir números dos meses por nomes
    mapa_meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    cvli_mes_pivot["Mês"] = cvli_mes_pivot["Mes"].map(mapa_meses)
    cvli_mes_pivot = cvli_mes_pivot.drop("Mes", axis=1)
    
    col_anos_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, int)]
    col_var_mes = [col for col in cvli_mes_pivot.columns if isinstance(col, str) and "Variação" in col]

    # Exibir tabela formatada
    st.dataframe(
        cvli_mes_pivot.style
        .background_gradient(cmap="Blues", subset=col_anos_mes)
        .background_gradient(cmap="RdYlGn_r", subset=col_var_mes)
        .format({**{col: "{:.0f}" for col in col_anos_mes}, **{col: "{:.0f}%" for col in col_var_mes}})
        .set_properties(**{"text-align": "center"}),
        use_container_width=True
    )
else:
    st.info("É necessário ter dados de pelo menos dois anos para gerar o comparativo mês a mês.")

# 📊 Visualização Gráfica: Evolução Mensal de CVLI
st.markdown("### 📈 Evolução Mensal de CVLI")

# Preparar dados para o gráfico
df_grafico = df_cvli.copy()
df_grafico["Ano-Mês"] = df_grafico["Ano"].astype(str) + "-" + df_grafico["Mes"].astype(str).str.zfill(2)
df_grafico["Data"] = pd.to_datetime(df_grafico["Ano-Mês"] + "-01")
evolucao_mensal = df_grafico.groupby(["Data", "CIDADE FATO"]).size().reset_index(name="Total")

# Criar gráfico
fig = px.line(
    evolucao_mensal, 
    x="Data", 
    y="Total", 
    color="CIDADE FATO",
    markers=True,
    title="Evolução Mensal de CVLI por Cidade",
    labels={"Total": "Número de Casos", "Data": "Mês/Ano", "CIDADE FATO": "Cidade"}
)
fig.update_layout(
    xaxis_title="Mês/Ano",
    yaxis_title="Número de Casos",
    legend_title="Cidade",
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# 📥 Exportação
def to_excel(dfs: dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    output.seek(0)
    return output

# Botão para download
st.download_button(
    "📥 Baixar Todas as Tabelas em Excel", 
    data=to_excel({
        "Total_Cidade_Categoria": tabela_total,
        "Comparativo_CVLI": cvli_pivot,
        "Dias_Sem_Mortes": dias_sem_morte,
        "CVLI_Mes_a_Mes": cvli_mes_pivot if 'cvli_mes_pivot' in locals() else pd.DataFrame()
    }), 
    file_name=f"Dash_MVI_Tabelas_{datetime.now().strftime('%Y%m%d')}.xlsx", 
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px;">
    Dashboard desenvolvido pela P2 do 10º BPM - PMAL<br>
    Para suporte técnico: p2.10bpm@pm.al.gov.br
</div>
""", unsafe_allow_html=True)
