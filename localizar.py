import streamlit as st
import sqlite3

def pesquisar_uso(cidade_id):
    st.header("Pesquisar Uso Permitido")

    tipo_uso_input = st.text_input("Digite o tipo de uso que deseja pesquisar:")

    if st.button("Buscar"):
        conn = sqlite3.connect('zoneamento.db')
        cursor = conn.cursor()

        query = """
        SELECT u.tipo_uso, z.nome AS zona_nome, m.descricao AS macrozona_descricao
        FROM usos_permitidos u
        LEFT JOIN zona z ON u.zona_codigo = z.codigo AND u.cidade_id = z.cidade_id
        LEFT JOIN macrozona m ON u.macrozona_codigo = m.codigo AND u.cidade_id = m.cidade_id
        WHERE u.tipo_uso LIKE ? 
          AND u.permissao = 'Permitido'
          AND u.cidade_id = ?
        """

        cursor.execute(query, (f"%{tipo_uso_input}%", cidade_id))
        resultados = cursor.fetchall()

        if resultados:
            for tipo_uso, zona_nome, macrozona_desc in resultados:
                st.write(f"**Tipo de Uso:** {tipo_uso}")
                st.write(f"Zona: {zona_nome}")
                st.write(f"Macrozona: {macrozona_desc}")
                st.markdown("---")
        else:
            st.warning("Nenhum uso permitido encontrado para esta pesquisa.")

        conn.close()
