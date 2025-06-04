import pandas as pd
from io import BytesIO
from unittest.mock import patch, MagicMock

import dados


def test_carregar_dados():
    df_mock = pd.DataFrame({
        "DATA FATO": ["01/01/2023"],
        "NOME VITIMA": ["A"],
        "CIDADE FATO": ["Cidade"],
        "CATEGORIA": ["Cat"]
    })

    mock_response = MagicMock()
    mock_response.content = b""
    mock_response.raise_for_status = lambda: None

    with patch('dados.requests.get', return_value=mock_response), \
         patch('dados.pd.read_excel', return_value=df_mock):
        df = dados.carregar_dados()

    expected_cols = {"DATA FATO", "NOME VITIMA", "CIDADE FATO", "CATEGORIA", "Ano", "Mes", "Mes_Nome"}
    assert expected_cols.issubset(df.columns)
    assert len(df) == 1
