from modules.gsheets_connection import extract_data
import streamlit as st
import pandas as pd

planilha = st.secrets["planilhas"]["2024 1° Split"]

id_planilha = planilha['id_planilha']
sheet_name = planilha['sheet_name']

# Define e inicializa o st.session_state
def init_session_state():
    if "data" not in st.session_state:
        df_data = extract_data(id_planilha, sheet_name)
        st.session_state["data"] = df_data