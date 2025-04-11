import streamlit as st
import sqlite3
import pandas as pd

def crud_app(cidade_id):
    st.header("Gerenciamento de Macrozona")

    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()

    # Exibir as macrozonas da cidade selecionada
    macrozonas = pd.read_sql_query(
        "SELECT * FROM macrozona WHERE cidade_id = ?", conn, params=(cidade_id,)
    )

    st.dataframe(macrozonas)

    st.subheader("Cadastrar Nova Macrozona")
    codigo = st.text_input("Código da Macrozona")
    descricao = st.text_input("Descrição da Macrozona")

    if st.button("Salvar Macrozona"):
        if codigo and descricao:
            try:
                cursor.execute(
                    "INSERT INTO macrozona (codigo, descricao, cidade_id) VALUES (?, ?, ?)",
                    (codigo, descricao, cidade_id)
                )
                conn.commit()
                st.success("Macrozona cadastrada com sucesso!")
                st.experimental_rerun()
            except sqlite3.IntegrityError:
                st.error("Erro: Código já cadastrado.")
        else:
            st.warning("Preencha todos os campos.")

    conn.close()
