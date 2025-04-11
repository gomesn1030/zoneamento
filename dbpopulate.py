import streamlit as st
import sqlite3

# Função para criar o banco de dados e tabelas
def criar_banco():
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()

    # Cria as tabelas
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS cidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS macrozona (
            codigo       VARCHAR(4) PRIMARY KEY,
            descricao    TEXT NOT NULL,
            cidade_id    INTEGER NOT NULL,
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );

        CREATE TABLE IF NOT EXISTS zona (
            codigo            VARCHAR(10) PRIMARY KEY,
            nome              TEXT NOT NULL,
            macrozona_codigo  VARCHAR(4),
            cidade_id         INTEGER NOT NULL,
            CONSTRAINT fk_zona_macrozona FOREIGN KEY (macrozona_codigo) REFERENCES macrozona(codigo),
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );

        CREATE TABLE IF NOT EXISTS parametros_urbanisticos (
            macrozona_codigo   VARCHAR(4) NOT NULL,
            zona_codigo        VARCHAR(10),
            coeficiente_aprov  NUMERIC(3,1) NOT NULL,
            gabarito_maximo    INTEGER NOT NULL,
            area_minima_lote   INTEGER NOT NULL,
            taxa_ocupacao_max  NUMERIC(5,2) NOT NULL,
            cidade_id          INTEGER NOT NULL,
            PRIMARY KEY (macrozona_codigo, zona_codigo, cidade_id),
            CONSTRAINT fk_param_macrozona FOREIGN KEY (macrozona_codigo) REFERENCES macrozona(codigo),
            CONSTRAINT fk_param_zona FOREIGN KEY (zona_codigo) REFERENCES zona(codigo),
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );

        CREATE TABLE IF NOT EXISTS usos_permitidos (
            macrozona_codigo   VARCHAR(4) NOT NULL,
            zona_codigo        VARCHAR(10),
            tipo_uso           VARCHAR(100) NOT NULL,
            porte              VARCHAR(20),
            cnae               VARCHAR(50),
            permissao          VARCHAR(20) NOT NULL,
            cidade_id          INTEGER NOT NULL,
            PRIMARY KEY (macrozona_codigo, zona_codigo, tipo_uso, porte, cidade_id),
            CONSTRAINT fk_uso_macrozona FOREIGN KEY (macrozona_codigo) REFERENCES macrozona(codigo),
            CONSTRAINT fk_uso_zona FOREIGN KEY (zona_codigo) REFERENCES zona(codigo),
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );

        CREATE TABLE IF NOT EXISTS faixa_especial (
            codigo       VARCHAR(10) PRIMARY KEY,
            descricao    TEXT NOT NULL,
            cidade_id    INTEGER NOT NULL,
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );

        CREATE TABLE IF NOT EXISTS zona_faixa_especial (
            zona_codigo   VARCHAR(10) NOT NULL,
            faixa_codigo  VARCHAR(10) NOT NULL,
            cidade_id     INTEGER NOT NULL,
            PRIMARY KEY (zona_codigo, faixa_codigo, cidade_id),
            CONSTRAINT fk_zona_faixa_zona FOREIGN KEY (zona_codigo) REFERENCES zona(codigo),
            CONSTRAINT fk_zona_faixa_faixa FOREIGN KEY (faixa_codigo) REFERENCES faixa_especial(codigo),
            FOREIGN KEY (cidade_id) REFERENCES cidade(id)
        );
    ''')

    conn.commit()
    conn.close()

# --- Streamlit App ---

st.title("Criar Banco de Dados de Zoneamento")

st.write("Este app cria o banco de dados com as tabelas necessárias para o gerenciamento de zoneamento.")

if st.button("Criar Banco de Dados"):
    criar_banco()
    st.success("Banco de dados 'zoneamento.db' criado com sucesso!")
