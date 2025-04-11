import streamlit as st
import sqlite3
import dbcreate
import dbpopulate
import localizar
import crud
import os

st.set_page_config(page_title="Zoneamento Urbano", layout="wide")

st.title("Sistema de Zoneamento Urbano")

# --- Funções auxiliares ---
def listar_cidades():
    conn = sqlite3.connect('zoneamento.db')
    cidades = conn.execute("SELECT id, nome FROM cidade").fetchall()
    conn.close()
    return cidades

def cadastrar_cidade(nome, estado):
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cidade (nome, estado) VALUES (?, ?)", (nome, estado))
    conn.commit()
    conn.close()

# --- Sidebar ---
st.sidebar.header("Gerenciamento de Cidades")
cidades = listar_cidades()
cidade_nome = st.sidebar.selectbox("Escolha uma cidade:", [c[1] for c in cidades])
cidade_id = [c[0] for c in cidades if c[1] == cidade_nome][0]

st.sidebar.subheader("Cadastrar Nova Cidade")
nome_nova_cidade = st.sidebar.text_input("Nome da nova cidade")
estado_nova_cidade = st.sidebar.text_input("Estado da nova cidade")
if st.sidebar.button("Cadastrar Cidade"):
    if nome_nova_cidade and estado_nova_cidade:
        cadastrar_cidade(nome_nova_cidade, estado_nova_cidade)
        st.experimental_rerun()
    else:
        st.sidebar.error("Preencha todos os campos para cadastrar uma cidade.")

menu = st.sidebar.selectbox(
    "Escolha uma opção:", 
    ["Início", "Criar Banco de Dados", "Popular Banco de Dados", "Pesquisar Uso Permitido", "Cadastros"]
)

# --- Menu Principal ---
if menu == "Início":
    st.write("Bem-vindo ao sistema de gerenciamento de zoneamento urbano.")

elif menu == "Criar Banco de Dados":
    if st.button("Criar Banco"):
        dbcreate.criar_banco()
        st.success("Banco de dados criado com sucesso!")

elif menu == "Popular Banco de Dados":
    if st.button("Popular Banco"):
        dbpopulate.popular_banco()
        st.success("Banco de dados populado com sucesso!")

elif menu == "Pesquisar Uso Permitido":
    localizar.pesquisar_uso()

elif menu == "Cadastros":
    crud.crud_app()