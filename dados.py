import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

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
