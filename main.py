import streamlit as st
import sqlite3
import os
import dbcreate
import dbpopulate
import localizar
import crud
import cadastros

# Verificar e criar estrutura do banco de dados se necessário
def verifica_cria_banco():
    if not os.path.exists('zoneamento.db'):
        dbcreate.criar_banco()
    else:
        conn = sqlite3.connect('zoneamento.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM cidade LIMIT 1")
        except sqlite3.OperationalError:
            dbcreate.criar_banco()
        conn.close()

# Chamar a verificação no início do app
verifica_cria_banco()

# --- Interface do App ---

st.set_page_config(page_title="Zoneamento Urbano", layout="wide")

st.sidebar.header("Gerenciamento de Cidades")

# Cadastrar nova cidade
def cadastrar_cidade():
    with st.sidebar.expander("Cadastrar Nova Cidade"):
        nome = st.text_input("Nome da Cidade")
        estado = st.text_input("Estado (UF)")
        if st.button("Cadastrar Cidade"):
            if nome and estado:
                conn = sqlite3.connect('zoneamento.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cidade (nome, estado) VALUES (?, ?)", (nome, estado))
                conn.commit()
                conn.close()
                st.success(f"Cidade '{nome} - {estado}' cadastrada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha todos os campos.")

# Listar cidades cadastradas
def listar_cidades():
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM cidade")
    cidades = cursor.fetchall()
    conn.close()
    return cidades

# --- Fluxo principal ---

cadastrar_cidade()

cidades = listar_cidades()
cidade_id_nome = {cid: nome for cid, nome in cidades}

cidade_selecionada_nome = st.sidebar.selectbox(
    "Escolha a Cidade", list(cidade_id_nome.values())
)

# Encontrar o ID da cidade selecionada
cidade_selecionada_id = None
for cid, nome in cidade_id_nome.items():
    if nome == cidade_selecionada_nome:
        cidade_selecionada_id = cid
        break

# Cabeçalho principal
st.title(f"Sistema de Zoneamento Urbano - {cidade_selecionada_nome}")

menu = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["Início", "Popular Banco de Dados", "Pesquisar Uso Permitido", "Cadastros", "Cadastrar Macrozona"]
)

if menu == "Início":
    st.write("Bem-vindo ao sistema de gerenciamento de zoneamento urbano.")

elif menu == "Popular Banco de Dados":
    if st.button("Popular Banco"):
        dbpopulate.popular_banco()
        st.success("Banco de dados populado com sucesso!")

elif menu == "Pesquisar Uso Permitido":
    localizar.pesquisar_uso(cidade_selecionada_id)

elif menu == "Cadastros":
    crud.crud_app(cidade_selecionada_id)

elif menu == "Cadastrar Macrozona":
    cadastros.cadastro_macrozona(cidade_selecionada_id)
