# 📊 Painel Analítico MVI 10º BPM

Este projeto é um painel interativo desenvolvido com Streamlit para análise de dados de violência letal no âmbito do 10º Batalhão da Polícia Militar de Alagoas (10º BPM).

## 🗂️ Estrutura Modular

```
├── dashboard_mvi.py       <- Arquivo principal da aplicação
├── autenticacao.py       <- Função de autenticação por senha
├── dados.py              <- Carregamento e tratamento de dados
├── estilo.py             <- Aplicação de CSS customizado
├── exportacao.py         <- Exportação de tabelas em Excel
├── filtros.py            <- Lógica de filtros reutilizável
└── style.css             <- Arquivo CSS com estilos visuais (opcional)
```

## ▶️ Como Executar

1. Instale as dependências:

```bash
pip install streamlit pandas openpyxl xlsxwriter requests
```

2. Execute o aplicativo:

```bash
streamlit run dashboard_mvi.py
```

## 🔐 Autenticação

O painel é protegido por senha, definida no arquivo `autenticacao.py`. Por padrão:

```python
senha == "pmal2025"
```

## 🔎 Funcionalidades

* Filtros por cidade, categoria, ano e mês
* Análise CVLI mês a mês e ano a ano
* Dias sem registro de mortes por cidade
* Exportação de todas as tabelas em Excel

## 📥 Fonte dos Dados

Os dados são baixados automaticamente via planilha pública do Google Drive, cujo ID está no arquivo `dados.py`.

## 📄 Licença

Projeto institucional. Uso interno restrito à PMAL.
