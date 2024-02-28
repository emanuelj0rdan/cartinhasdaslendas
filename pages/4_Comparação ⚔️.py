from modules.session_state import init_session_state
from modules.utils import create_stdataframe
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from urllib.error import URLError

##################### Configuração inicial #####################
st.set_page_config(
    page_title="Comparação",
    page_icon="⚔️",
    layout="wide"
)

init_session_state()

def get_UN_data():
    df_data = st.session_state["data"]
    return df_data.set_index("ID")

st.text('Para uma comparação mais livre, pode selecionar quantos nomes quiser. Mas cria um gráfico bagunçado e confuso.')
st.caption('"Com :blue[grandes poderes] vem :blue[grandes responsabilidades]"')

try:
    df_data = get_UN_data()
    players = st.multiselect(
        "Escolha os jogadores", list(df_data.index), ["Brance", "Netuno", "Route", "TitaN"],
        placeholder = 'Escolha uma opção', help = 'Esses 4 estão escolhidos por padrão',
        label_visibility = "visible" #"hidden", or "collapsed")
    )
    colunas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Team', 
                                    'Wiki', 'Country']).columns.tolist()
    notas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 
                                  'Wiki', 'Country', 'Country flag', 'Photo']).columns.tolist()
    if not players:
        st.error("Por favor, selecione pelo menos um jogador/coach.")
    else:
        data = df_data.loc[players]
        st.write("### Notas das Cartinhas")
        create_stdataframe(data[colunas], colunas)

        data_notes = data[notas]
        data_note = data_notes.T
        fig = px.line(data_note, x=data_note.index, y=data_note.columns, symbol="ID", title='Progresso das notas')
        fig.update_layout(height=500, legend_title_text='Jogador / Coach')
        fig.update_xaxes(title_text='Rodada')
        fig.update_yaxes(title_text='Nota')
        fig.update_layout(modebar_remove = ["pan", "lasso", "select"])
        st.plotly_chart(fig, use_container_width=True)

        st.caption('O gráfico é interativo:', help= 'Teste')
        st.caption('Clique :blue[1x] no nome do jogador/coach na legenda para excluir/adicionar as notas dele')
        st.caption('Clique :blue[2x] no nome do jogador/coach na legenda para isolar as notas dele')
        st.caption('No gráfico, clique :blue[e arraste] pra dar zoom. Clique :blue[2x] no gráfico pra sair do zoom')

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )