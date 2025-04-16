import streamlit as st
import sqlite3
import pandas as pd

def cadastro_macrozona(cidade_id):
    st.header("Zonas cadastradas para a cidade")  # Exibe um cabeçalho na interface do Streamlit.

    # Conecta ao banco de dados SQLite chamado 'zoneamento.db'.
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL.

    # Consulta as macrozonas do banco de dados para a cidade especificada.
    macrozonas = pd.read_sql_query(
        "SELECT codigo as Macrozona, descricao as 'Descrição' FROM macrozona WHERE cidade_id = ?", conn, params=(cidade_id,)
    )

    # Exibe os dados das macrozonas em um dataframe na interface do Streamlit.
    st.dataframe(macrozonas)

    # Adiciona um subtítulo para a seção de cadastro de nova macrozona.
    st.subheader("Cadastrar nova macrozona")

    # Campo de entrada para o código da macrozona.
    codigo = st.text_input("Código da macrozona")

    # Campo de entrada para a descrição da macrozona.
    descricao = st.text_input("Descrição do Zoneamento")

    # Botão para salvar a nova macrozona.
    if st.button("Salvar"):
        # Verifica se os campos de código e descrição foram preenchidos.
        if codigo and descricao:
            try:
                # Insere a nova macrozona no banco de dados.
                cursor.execute(
                    "INSERT INTO macrozona (codigo, descricao, cidade_id) values (?, ?, ?)",
                    (codigo, descricao, cidade_id)
                )
                # Confirma as alterações no banco de dados.
                conn.commit()
                # Exibe uma mensagem de sucesso.
                st.success("Macrozona cadastrada") 
                # Recarrega a aplicação para atualizar os dados exibidos.
            except sqlite3.IntegrityError:
                # Exibe uma mensagem de erro caso o código já esteja cadastrado.
                st.error("Erro: Código já cadastrado.")
        else:
            # Exibe um aviso caso algum campo não tenha sido preenchido.
            st.warning("Preencha todos os campos.")

    # Fecha a conexão com o banco de dados.
    st.rerun()
    conn.close()