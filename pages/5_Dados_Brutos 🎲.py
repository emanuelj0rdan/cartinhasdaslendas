import streamlit as st
import numpy as np


st.set_page_config(
    page_title="Dados Brutos ",
    page_icon="🎲",
    layout="wide"
)

st.title("Todas as notas do Split")
st.caption('Cada coluna é uma semana')

if "data" in st.session_state:
     df_data = st.session_state["data"]
     notas = df_data.drop(columns=['Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 'Wiki', 'Country', 'Country flag', 
                                  'Photo']).columns.tolist()
     st.dataframe(df_data[notas].set_index("ID"), use_container_width = True)

else:
      st.write("Nenhum dado foi encontrado. Por favor, selecione as notas na página principal")