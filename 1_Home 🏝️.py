from modules.utils import melhores_notas, all_notes
import streamlit as st
import pandas as pd
from modules.gsheets_connection import extract_data

st.set_page_config(
    page_icon = 'https://pbs.twimg.com/profile_images/1745280145433182208/WtAIAMnV_400x400.png',
    page_title='Cartinha das Lendas',
    layout="wide",
    menu_items={
        'About': "### Isso é apenas *entretenimento*, *divirta-se*!"
    }
)

planilha = st.secrets["planilhas"]["2024 1° Split"]

id_planilha = planilha['id_planilha']
sheet_name = planilha['sheet_name']


if "data" not in st.session_state:
    df_data = extract_data(id_planilha, sheet_name)
    st.session_state["data"] = df_data


st.write("# CARTINHAS DAS LENDAS 🏝️")

periodo_selecionado = st.selectbox('Selecione o split:', list(st.secrets["planilhas"].keys()),
                                   index=None, placeholder="Por padrão, as notas carregadas serão as do split em andamento")

if periodo_selecionado in st.secrets["planilhas"]:
    info_planilha = st.secrets["planilhas"][periodo_selecionado]
    with st.spinner("Carregando notas..."):
        df_data = extract_data(info_planilha['id_planilha'], info_planilha['sheet_name'])

    # Atualizar os dados no session state
    st.session_state["data"] = df_data

    st.write('Split carregado:', periodo_selecionado)
    st.toast(f'Notas de {periodo_selecionado} carregadas!', icon='🎉')


    st.subheader('MAIORES NOTAS DA ÚLTIMA RODADA :sunglasses: :crown:', divider='green')
    melhores_notas(df_data)

    # Criar cinco colunas
    col1, col2, col3, col4, col5 = st.columns(5)

    # Exibir um DataFrame em cada coluna
    col1.dataframe(all_notes(df_data, "Top"), column_config={"ID": "Jogador"}, use_container_width = True)
    col2.dataframe(all_notes(df_data, "Jungle"), column_config={"ID": "Jogador"}, use_container_width = True)
    col3.dataframe(all_notes(df_data, "Mid"), column_config={"ID": "Jogador"}, use_container_width = True)
    col4.dataframe(all_notes(df_data, "Bot"), column_config={"ID": "Jogador"}, use_container_width = True)
    col5.dataframe(all_notes(df_data, "Support"), column_config={"ID": "Jogador"}, use_container_width = True)


st.sidebar.caption("Da comunidade para a comunidade!")


# btn = st.button("Acesse os dados no Kaggle")
# if btn:
#    webbrowser.open_new_tab("https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data")

"---"
st.markdown(''' Um dashboard simples apenas pra registro das notas das Cartinhas das Lendas. 🃏 ''')
st.caption('Todos dados utilizados foram obtidos da [Wiki do CBLOL](https://lol.fandom.com/wiki/Circuit_Brazilian_League_of_Legends) e das redes sociais do grupo [Ilha das Lendas](https://twitter.com/ilhadaslendas)')