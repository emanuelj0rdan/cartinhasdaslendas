import gspread
import pandas as pd
import streamlit as st
import json

# Acessando a variável de ambiente
credentials = json.loads(st.secrets["google_sheets"]["credentials"])

def extract_data(key, sheet_name):
    #gc = gspread.service_account(filename='cartinhasdaslendas.json')
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_key(key)
    ws = sh.worksheet(sheet_name)
    dados = ws.get_all_records()
    df = pd.DataFrame(dados)
    df = df.iloc[:, 1:]  # Exclui a primeira coluna
    return df
