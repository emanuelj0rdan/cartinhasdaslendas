import streamlit as st
from modules.session_state import init_session_state
from modules.utils import create_stdataframe, media_do_time, line_chart
import plotly.express as px
import time

st.set_page_config(
    page_title="Times",
    page_icon="🏆",
    layout="wide"
)

init_session_state()

df_data = st.session_state["data"]

teams = df_data["Team"].value_counts().index
team = st.sidebar.selectbox("Time", teams)

df_filtered = df_data[df_data["Team"] == team].set_index("ID")

st.image(df_filtered.iloc[0]["Logo Team"], width=60)
st.markdown(f"## {team}")
st.markdown(f"**Sigla:** {df_filtered.iloc[0]['Sigla']}")


colunas = df_data.drop(columns=['ID', 'Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Team', 
                         'Wiki', 'Country']).columns.tolist()
notas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 
                         'Wiki', 'Country', 'Country flag', 'Photo']).columns.tolist()

# Prepara os dados pra plotar o gráfico com as notas do time.
data_notes = df_data[df_data["Team"] == team][notas].melt(id_vars='ID', var_name='Rodada', value_name='Nota')
media_team = media_do_time(df_filtered[notas[1:]])

st.subheader(f"Média geral do time {media_team:.0f}")
progress_bar = st.progress(0)
for porcentagem in range(int(media_team)):
    time.sleep(0.01)
    progress_bar.progress(porcentagem + 1)

create_stdataframe(df_filtered[colunas], colunas)

fig = px.line(data_notes[data_notes['Nota'] != 0], x='Rodada', y='Nota', color='ID', symbol="ID",
              title='Notas dos Jogadores ao longo das semanas')
fig.update_layout(height=500, legend_title_text='Jogador / Coach')
fig.update_layout(modebar_remove = ["pan", "lasso", "select"])
st.plotly_chart(fig, use_container_width=True)

st.caption('O gráfico é interativo:', help= 'Teste')
st.caption('Clique :blue[1x] no nome do jogador/coach na legenda para excluir/adicionar as notas dele')
st.caption('Clique :blue[2x] no nome do jogador/coach na legenda para isolar as notas(e vice-versa)')
st.caption('No gráfico, clique :blue[e arraste] pra dar zoom. Clique :blue[2x] no gráfico pra sair do zoom')


