from modules.utils import ultima_nota, media_posicao, media_do_player, media_do_time
from modules.session_state import init_session_state
import streamlit as st
import webbrowser
import time
import numpy as np
import pandas as pd
import plotly.express as px

##################### Configuração inicial #####################
st.set_page_config(
    page_title="Players",
    page_icon="🎮",
    layout="wide"
)

##################### Prepara os dados #####################
init_session_state()
df_data = st.session_state["data"]

teams = df_data["Team"].value_counts().index
team = st.sidebar.selectbox("Team", teams)

df_players = df_data[df_data["Team"] == team]
players = df_players["ID"].value_counts().index
player = st.sidebar.selectbox("ID", players)

notas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 
                         'Wiki', 'Country', 'Country flag', 'Photo']).columns.tolist()

player_stats = df_data[df_data["ID"] == player].iloc[0]
player_stats_notes = player_stats[notas]
df_players_notes = df_players[notas[1:]]

##################### Informações do jogador #####################
st.image(f"{player_stats['Photo']}", width=150)
st.title(f"{player_stats['ID']}")

#pega o link da imagem da logo do time
logoteam_url = player_stats['Logo Team']
logorole_url = player_stats['Logo Role']
largura = 25
st.markdown(f"**Time:** {player_stats['Team']}  <img src='{logoteam_url}' width='{largura}'>", unsafe_allow_html=True)
st.markdown(f"**Posição:** {player_stats['Role']} <img src='{logorole_url}' width='{largura}'>", unsafe_allow_html=True)
 
col1, col2, col3 = st.columns(3)
if player_stats['Age'] > 100:
    col1.markdown(f"**Idade:** Sem informação")
else:
    col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Nome:** {player_stats['Name']}")
# pega o link da imagem do país pra usar na coluna
flag_url = player_stats['Country flag']
col3.markdown(f"**Nacionalidade:** <img src='{flag_url}' width='{largura}'>", unsafe_allow_html=True)


st.divider()
##################### Notas do jogador #####################
#AQUI É A MÉDIA DAS NOTAS
media_player = media_do_player(player_stats_notes[1:])


if media_player > 0:
    st.subheader(f"Média geral do player {media_player:.0f}")
    progress_bar = st.progress(0)
    for porcentagem in range(int(media_player)):
        time.sleep(0.01)
        progress_bar.progress(porcentagem + 1)

    #media do time
    ultimanota = ultima_nota(player_stats_notes[1:])
    pnotes_sem_id = player_stats_notes[notas[1:]]
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Média do time", value=f"{media_do_time(df_players_notes):.0f}")
    col2.metric(label="Média da posição", value=f"{media_posicao(df_data, player_stats['Role']):.0f}")
    col3.metric(label="Última nota", value=f"{ultimanota:.0f}")

    # Cria o gráfico
    pnotes_no_zero = player_stats_notes[player_stats_notes != 0]
    fig = px.line(pnotes_no_zero, x=pnotes_no_zero[1:].index, y=pnotes_no_zero[1:].values, markers=True, 
                  text=pnotes_no_zero[1:].values, title='Progresso de notas do jogador')
    fig.update_traces(textposition="bottom center")
    fig.update_xaxes(title_text='Rodada')
    fig.update_yaxes(title_text='Nota')
    fig.update_layout(modebar_remove = ["pan", "lasso", "select"])
    st.plotly_chart(fig, use_container_width=True)
        
else:
    st.subheader(f"Média geral inexistente")
    progress_text = "Jogador sem nota no campeonato"
    st.progress(int(player_stats['S1']), text=progress_text)


btn = st.button("Acesse a Wiki do jogador")
if btn:
    webbrowser.open_new_tab(f"{player_stats['Wiki']}")

link = player_stats['Wiki']