import pandas as pd
from io import BytesIO
from unittest.mock import patch

import exportacao


def test_to_excel_returns_bytesio():
    df = pd.DataFrame({'A': [1], 'B': [2]})

    class DummyWriter:
        def __init__(self, buffer, engine=None):
            self.buffer = buffer
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass
        def write(self, data):
            self.buffer.write(data)

    def fake_to_excel(self, writer, sheet_name='Sheet1', index=False, **kwargs):
        writer.write(self.to_csv(index=index).encode())

    with patch('exportacao.pd.ExcelWriter', DummyWriter), \
         patch.object(pd.DataFrame, 'to_excel', fake_to_excel):
        output = exportacao.to_excel({'Sheet': df})

    assert isinstance(output, BytesIO)
    assert len(output.getvalue()) > 0
