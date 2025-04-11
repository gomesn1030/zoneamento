import streamlit as st
import sqlite3
import pandas as pd

# Funções auxiliares

def conectar():
    return sqlite3.connect('zoneamento.db')

def listar_tabelas():
    return ["macrozona", "zona", "parametros_urbanisticos", "usos_permitidos", "faixa_especial", "zona_faixa_especial"]

def carregar_dados(tabela):
    conn = conectar()
    df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
    conn.close()
    return df

def salvar_dados(tabela, df):
    conn = conectar()
    df.to_sql(tabela, conn, if_exists='replace', index=False)
    conn.close()

def deletar_registro(tabela, condicao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE {condicao}")
    conn.commit()
    conn.close()

def adicionar_registro(tabela, novos_dados):
    conn = conectar()
    cursor = conn.cursor()
    colunas = ', '.join(novos_dados.keys())
    valores = tuple(novos_dados.values())
    placeholders = ', '.join(['?'] * len(novos_dados))
    cursor.execute(f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})", valores)
    conn.commit()
    conn.close()

# --- Streamlit App ---

st.title("Gerenciamento de Dados do Zoneamento (CRUD)")

# Escolher a tabela
tabela = st.selectbox("Escolha a tabela para gerenciar:", listar_tabelas())

if tabela:
    st.subheader(f"Dados da tabela {tabela}")
    df = carregar_dados(tabela)

    # Exibir dados
    st.dataframe(df)

    st.write("---")
    st.subheader("Editar dados")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Salvar Alterações"):
        salvar_dados(tabela, edited_df)
        st.success("Alterações salvas com sucesso!")

    st.write("---")
    st.subheader("Excluir registro")
    if len(df) > 0:
        coluna_chave = st.selectbox("Escolha a coluna de identificação para exclusão:", df.columns)
        valor_chave = st.text_input(f"Digite o valor de {coluna_chave} a ser excluído:")

        if st.button("Excluir Registro"):
            if valor_chave:
                condicao = f"{coluna_chave} = '{valor_chave}'"
                deletar_registro(tabela, condicao)
                st.success(f"Registro onde {coluna_chave} = {valor_chave} excluído com sucesso!")
            else:
                st.warning("Digite um valor para exclusão.")

    st.write("---")
    st.subheader("Adicionar novo registro")
    novos_dados = {}
    for coluna in df.columns:
        novos_dados[coluna] = st.text_input(f"{coluna}", key=f"new_{coluna}")

    if st.button("Adicionar Novo Registro"):
        if all(novos_dados.values()):
            adicionar_registro(tabela, novos_dados)
            st.success("Novo registro adicionado com sucesso!")
        else:
            st.warning("Preencha todos os campos para adicionar um novo registro.")
