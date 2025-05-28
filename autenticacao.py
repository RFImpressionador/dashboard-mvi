import streamlit as st

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
