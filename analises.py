import streamlit as st
import pandas as pd
from datetime import datetime
from feriados import carregar_feriados_personalizados
import holidays


# CSS Inline
st.markdown("""
    <style>
    div[data-baseweb="tag"] {
        background-color: #00c8c8 !important;
        color: #1e1e2f !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 4px 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ... outras funções omitidas para brevidade ...

def mostrar_comparativo_mes(df_filtrado, cidades, anos, meses):
    meses_filtrados = sorted(meses) if meses else list(range(1, 13))
    todas_combinacoes = pd.MultiIndex.from_product(
        [cidades, anos, meses_filtrados],
        names=["CIDADE FATO", "Ano", "Mes"]
    )

    df_cvli = df_filtrado[df_filtrado["CATEGORIA"] == "CVLI"].copy()
    dias_pt = {
        "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    df_cvli["Dia_Semana"] = df_cvli["DATA FATO"].dt.day_name().map(dias_pt)

    feriados_custom = carregar_feriados_personalizados()
    feriados_nacionais = holidays.Brazil()

    def classificar_tipo_dia(row):
        data = row["DATA FATO"].date()
        cidade = row["CIDADE FATO"]

        if data in feriados_nacionais:
            return "Feriado Nacional"
        elif cidade in feriados_custom:
            if data in feriados_custom[cidade]["municipal"]:
                return "Feriado Municipal"
            elif data in feriados_custom[cidade]["estadual"]:
                return "Feriado Estadual"
        return "Dia comum"

    df_cvli["Tipo_Dia"] = df_cvli.apply(classificar_tipo_dia, axis=1)

    cvli_mes = df_cvli.groupby(["CIDADE FATO", "Ano", "Mes"]).size().reset_index(name="Total")
    cvli_mes = cvli_mes.set_index(["CIDADE FATO", "Ano", "Mes"]).reindex(todas_combinacoes, fill_value=0).reset_index()
    cvli_mes["Mes_Ano"] = cvli_mes["Mes"].apply(lambda x: f"{x:02d}") + "/" + cvli_mes["Ano"].astype(str)

    cvli_mes_pivot = cvli_mes.pivot(index="CIDADE FATO", columns="Mes_Ano", values="Total").fillna(0).astype(int)
    cvli_mes_pivot = cvli_mes_pivot.reset_index()

    # Adiciona colunas de variação ano a ano por mês
    colunas_meses_ano = sorted([col for col in cvli_mes_pivot.columns if col != "CIDADE FATO"])
    for i in range(1, len(anos)):
        for mes in meses_filtrados:
            mes_str = f"{mes:02d}"
            col_ant = f"{mes_str}/{anos[i-1]}"
            col_atual = f"{mes_str}/{anos[i]}"
            if col_ant in cvli_mes_pivot.columns and col_atual in cvli_mes_pivot.columns:
                col_var = f"% Variação {col_ant}-{col_atual}"
                cvli_mes_pivot[col_var] = ((cvli_mes_pivot[col_atual] - cvli_mes_pivot[col_ant]) / cvli_mes_pivot[col_ant].replace(0, 1)) * 100
                cvli_mes_pivot[col_var] = cvli_mes_pivot[col_var].round(0).astype(int)

    # Formata nomes dos meses
    nomes_meses_ptbr = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    def nome_mes(col):
        if "/" in col:
            mes, ano = col.split("/")
            return f"{nomes_meses_ptbr[int(mes)-1]}/{ano}"
        return col

    cvli_mes_pivot.columns = ["CIDADE FATO"] + [nome_mes(c) for c in cvli_mes_pivot.columns[1:]]

    col_format = {col: "{:.0f}" for col in cvli_mes_pivot.columns if col != "CIDADE FATO"}

    st.markdown("### 📊 Comparativo CVLI Mês a Mês")
    st.markdown(
        cvli_mes_pivot
        .style.format(col_format)
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )

    st.markdown("### 📅 Datas e Dias da Semana por Cidade")
    df_cvli["DATA FATO"] = pd.to_datetime(df_cvli["DATA FATO"])
    df_cvli["DATA FATO"] = df_cvli["DATA FATO"].dt.strftime("%d/%m/%Y %H:%M")

    tabela_detalhes = df_cvli[["CIDADE FATO", "DATA FATO", "Dia_Semana", "Tipo_Dia"]]
    tabela_detalhes = tabela_detalhes[df_cvli["Ano"].isin(anos) & df_cvli["Mes"].isin(meses_filtrados)]
    tabela_detalhes = tabela_detalhes.sort_values(by=["CIDADE FATO", "DATA FATO"])

    st.markdown(
        tabela_detalhes
        .style.set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )
