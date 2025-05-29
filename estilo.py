import streamlit as st

def aplicar_css_personalizado():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
