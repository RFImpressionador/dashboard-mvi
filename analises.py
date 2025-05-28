import streamlit as st
import pandas as pd
from datetime import datetime
from feriados import carregar_feriados_personalizados


def mostrar_dias_sem_morte(df, cidades):
    df_cvli = df[df["CATEGORIA"] == "CVLI"]
    df_cvli_geral = df_cvli[df_cvli["CIDADE FATO"].isin(cidades)]

    ultimas_mortes = df_cvli_geral.groupby("CIDADE FATO")["DATA FATO"].max().reindex(cidades)

    dias_sem_morte = ultimas_mortes.reset_index().rename(columns={"DATA FATO": "Ultima_Morte"})
    dias_sem_morte["Dias_Sem_Mortes"] = (
        pd.to_datetime(datetime.now().date()) - dias_sem_morte["Ultima_Morte"]
    ).dt.days

    dias_sem_morte["Ultima_Morte"] = dias_sem_morte["Ultima_Morte"].dt.strftime("%d/%m/%Y %H:%M")
    dias_sem_morte["Dias_Sem_Mortes"] = dias_sem_morte["Dias_Sem_Mortes"].fillna("Sem registro")
    dias_sem_morte.loc[dias_sem_morte["Dias_Sem_Mortes"] != "Sem registro", "Dias_Sem_Mortes"] = dias_sem_morte.loc[dias_sem_morte["Dias_Sem_Mortes"] != "Sem registro", "Dias_Sem_Mortes"].astype(int)

    st.markdown("### ⏳ Dias sem Mortes por Cidade")
    st.markdown(
        dias_sem_morte
        .style.set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )


def mostrar_total_por_cidade(df_filtrado, cidades):
    tabela_total = (
        df_filtrado
        .groupby(["CIDADE FATO", "CATEGORIA"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=cidades, fill_value=0)
        .stack()
        .reset_index(name="Total")
    )

    st.markdown("### 🔢 Total por Cidade e Categoria")
    st.markdown(
        tabela_total
        .style.set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )


def mostrar_comparativo_ano(df_filtrado, cidades):
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
    col_anos = [col for col in cvli_pivot.columns if isinstance(col, int)]
    col_var = [col for col in cvli_pivot.columns if isinstance(col, str) and "Variação" in col]

    st.markdown("### 📈 Comparativo CVLI Ano a Ano")
    st.markdown(
        cvli_pivot
        .style.format({**{col: "{:.0f}" for col in col_anos + col_var}})
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )


def mostrar_comparativo_mes(df_filtrado, cidades, anos, meses):
    if len(anos) <= 1:
        return

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
    df_cvli["Hora_Fato"] = df_cvli["DATA FATO"].dt.strftime("%H:%M")

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

    st.markdown("### 📊 Comparativo CVLI Mês a Mês")
    st.markdown(
        cvli_mes_pivot
        .style.format({col: "{:.0f}" for col in cvli_mes_pivot.columns if isinstance(col, int) or "% Variação" in str(col)})
        .set_properties(**{'text-align': 'center'})
        .hide(axis='index')
        .to_html(),
        unsafe_allow_html=True
    )

    st.markdown("### 📅 Datas e Dias da Semana por Cidade")
    tabela_detalhes = df_cvli[["CIDADE FATO", "DATA FATO", "Dia_Semana", "Hora_Fato"]]
    tabela_detalhes = tabela_detalhes[df_cvli["Ano"].isin(anos) & df_cvli["Mes"].isin(meses_filtrados)]
    tabela_detalhes = tabela_detalhes.sort_values(by=["CIDADE FATO", "DATA FATO"])
    st.dataframe(tabela_detalhes.reset_index(drop=True))
