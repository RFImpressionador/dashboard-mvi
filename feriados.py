import pandas as pd
import requests
from io import BytesIO

def carregar_feriados_personalizados():
    url = "https://drive.google.com/uc?export=download&id=1Nh3R5Ni6F7NEoj3ECLRo4vNEWIo38FWV"
    resposta = requests.get(url)
    arquivo = BytesIO(resposta.content)

    df = pd.read_excel(arquivo, engine="openpyxl")
    df.columns = [col.lower().strip() for col in df.columns]

    # Converte a coluna 'data' para datetime (pt-BR)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

    # Gera dicionário agrupado por cidade
    feriados_dict = {}
    for _, linha in df.iterrows():
        cidade = linha["cidade"]
        tipo = linha["tipo"]
        data = linha["data"].date()

        if cidade not in feriados_dict:
            feriados_dict[cidade] = {"municipal": set(), "estadual": set()}

        feriados_dict[cidade][tipo].add(data)

    return feriados_dict
