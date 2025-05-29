import streamlit as st

def aplicar_css_personalizado():
    st.markdown("""
        <style>
        /* === Tema Roxo Escuro Elegante === */

        body {
            background-color: #1a092a;
            color: #f5e9ff;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #e0aaff;
            font-weight: bold;
            text-align: center;
        }

        section[data-testid="stSidebar"] {
            background-color: #2c0b47;
            color: white;
            border-right: 2px solid #a64ac9;
        }

        .stSelectbox, .stMultiSelect, .stRadio, .stCheckbox {
            background-color: #2c0b47;
            border: 1px solid #a64ac9;
            color: white;
            border-radius: 6px;
        }

        div[data-baseweb="tag"] {
            background-color: #a64ac9 !important;
            color: #1a092a !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 5px 12px !important;
            margin: 3px 3px 3px 0 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        button[aria-label="remove"] svg {
            fill: #1a092a !important;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            background-color: #2b1544;
            color: #f5e9ff;
        }

        th {
            background-color: #a64ac9;
            color: #1a092a;
        }

        td, th {
            border: 1px solid #4e1b6c;
            padding: 8px;
            text-align: center;
        }

        [data-testid="stMetric"] {
            background-color: #2b1544;
            border: 1px solid #a64ac9;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            margin: 0.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 6px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #a64ac9;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-track {
            background-color: transparent;
        }

        a {
            color: #e0aaff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        label, div[data-testid="stMarkdownContainer"] p {
            color: #e0aaff !important;
            font-size: 14px !important;
        }

        </style>
    """, unsafe_allow_html=True)
