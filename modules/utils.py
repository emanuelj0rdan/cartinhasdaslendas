import time
import streamlit as st
import numpy as np
# Todas as funções do projeto.

# ------------------------------- página Home -------------------------------
def melhores_notas(df_data):
    notas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 'Wiki', 'Country', 'Country flag',
        'Photo']).columns.tolist()
    posicoes = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
    id_nota_maxima = []
    ultima_coluna = df_data[notas].columns[-1]
    penultima_coluna = df_data[notas].columns[-2]
    for x in posicoes:
        id_nota_maxima.append(df_data[df_data['Role'] == x][ultima_coluna].idxmax())

    colunas = st.columns(5)
    for i in range(5):
        coluna_atual = df_data.iloc[id_nota_maxima[i]]
        colunas[i].image(f"{coluna_atual['Photo']}", width=100)
        colunas[i].metric(
            label=coluna_atual['ID'],
            value=coluna_atual[ultima_coluna],
            delta=f'{coluna_atual[ultima_coluna] - coluna_atual[penultima_coluna]}'
        )

def all_notes(df_data, role):
    notas = df_data.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 'Wiki', 'Country', 'Country flag',
        'Photo']).columns.tolist()
    lane_notas = df_data[df_data['Role'] == role][notas]
    lane_notas.set_index('ID', inplace=True)
    coluna_notas = lane_notas.sort_values(by=[lane_notas.columns[-1]], ascending = False).iloc[:, -1]
    return coluna_notas.iloc[1:]

# ------------------------------- página Player -------------------------------
#Função pra pegar a última nota do player
def ultima_nota(registro):
    for i in reversed(range(len(registro))):
        if registro.iloc[i] != 0:
            return registro.iloc[i]
    return "Sem nota"


def media_posicao(df, role):
    notas = df.drop(columns=['Team', 'Name', 'Current Team', 'Role', 'Birthday', 'Age', 'Sigla', 'Logo Role', 'Logo Team', 'Wiki', 'Country', 'Country flag', 
                                  'Photo']).columns.tolist()
    dfnotas = df[df['Role'] == role][notas].set_index("ID")
    media = dfnotas.replace(0, np.nan).mean().mean()
    return media
    

#Função pra calcular a média do player
def media_do_player(tabela):
    # Substitui as notas ZERO por NaN
    tabela = tabela.replace(0, np.nan)
    # Calcula a média ignorando os valores NaN
    media = tabela.mean()
    return media

#------------------------------- página Players e Teams -------------------------------
#Função pra calcular a média do time
def media_do_time(tabela):
    media = tabela.replace(0, np.nan).mean().mean()
    return media



def line_chart(df_notas):
    chart = st.line_chart()
    for coluna, valor in df_notas.items():
        chart.add_rows({coluna: valor})
        time.sleep(0.05)


#------------------------------- página Teams e Compare -------------------------------

def create_stdataframe(df, colunas):
    # dicionário para mapear as colunas das respectivas rodadas
    rodadas = {
        "S1": "Rodada 1-2", "S2": "Rodada 3-4", "S3": "Rodada 5-6", "S4": "Rodada 7-8", "S5": "Rodada 9-10",
        "S6": "Rodada 11-12", "S7": "Rodada 13-14", "S8": "Rodada 15-16", "S9": "Rodada 17-18",
        "Playoff 1": "Playoff 1", "Playoff 2": "Playoff 2", "Playoff 3": "Playoff 3", "Final": "Final"
        }

    # dicionário para as colunas fixas
    fixed_columns = {
        "Photo": st.column_config.ImageColumn("Jogador"),
        "Logo Role": st.column_config.ImageColumn("Rota"),
        "Country flag": st.column_config.ImageColumn("Nacionalidade"),
        }

    # dicionário para as colunas dinâmicas(rodadas que ocorrem ao longo do tempo)
    dynamic_columns = {}
    for col in colunas:
        if col not in fixed_columns:
            # Verifica se todos os valores na coluna são zero
            if not df[col].eq(0).all():
                dynamic_columns[col] = st.column_config.ProgressColumn(rodadas[col], format="%d", max_value=int(df[col].max()))

    # Combine os dois dicionários
    column_config = {**fixed_columns, **dynamic_columns}
    # Use o dicionário de configurações de colunas ao criar o dataframe
    st.dataframe(df[colunas].set_index('Photo'), use_container_width=True, hide_index=True, column_order=column_config, column_config=column_config)
