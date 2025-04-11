import streamlit as st
import sqlite3

# Funções auxiliares
def conectar():
    return sqlite3.connect('zoneamento.db')

def buscar_usos(tipo_uso, cidade_id):
    conn = conectar()
    cursor = conn.cursor()

    query = '''
        SELECT DISTINCT macrozona_codigo, zona_codigo
        FROM usos_permitidos
        WHERE tipo_uso LIKE ? AND permissao = 'Permitido' AND cidade_id = ?
    '''
    cursor.execute(query, (f"%{tipo_uso}%", cidade_id))
    resultados = cursor.fetchall()

    conn.close()
    return resultados

def pesquisar_uso():
    st.header("Pesquisar Uso Permitido")

    conn = conectar()
    cidades = conn.execute("SELECT * FROM cidade").fetchall()
    conn.close()

    cidade_nome = st.selectbox("Escolha a cidade:", [c[1] for c in cidades])
    cidade_id = [c[0] for c in cidades if c[1] == cidade_nome][0]

    tipo_uso_input = st.text_input("Digite o tipo de uso para pesquisar:")

    if st.button("Buscar"):
        if tipo_uso_input:
            resultados = buscar_usos(tipo_uso_input, cidade_id)
            if resultados:
                st.success(f"Encontramos {len(resultados)} resultado(s):")
                for macrozona, zona in resultados:
                    st.write(f"Macrozona: {macrozona} | Zona: {zona if zona else 'Geral da Macrozona'}")
            else:
                st.warning("Nenhum uso permitido encontrado para essa busca.")
        else:
            st.error("Digite um termo para buscar.")
