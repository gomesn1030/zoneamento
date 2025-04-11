import sqlite3

def popular_banco():
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()

    # Inserir cidade Joinville
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, estado) VALUES (1, 'Joinville', 'SC')")

    cursor.executescript("""
        -- Macrozona
        INSERT OR IGNORE INTO macrozona (codigo, descricao, cidade_id) VALUES
            ('ARPA', 'Área Rural de Proteção Ambiental', 1),
            ('ARUC', 'Área Rural de Utilização Controlada', 1),
            ('AUAP', 'Área Urbana de Adensamento Prioritário', 1),
            ('AUAS', 'Área Urbana de Adensamento Secundário', 1),
            ('AUAC', 'Área Urbana de Adensamento Controlado', 1),
            ('AUAE', 'Área Urbana de Adensamento Especial', 1),
            ('AUPA', 'Área Urbana de Proteção Ambiental', 1);

        -- Zona
        INSERT OR IGNORE INTO zona (codigo, nome, macrozona_codigo, cidade_id) VALUES
            ('SA-01', 'Setor de Adensamento Prioritário 01 (Centro)', 'AUAP', 1),
            ('SA-02', 'Setor de Adensamento Prioritário 02 (Norte/Sul)', 'AUAP', 1),
            ('SA-03', 'Setor de Adensamento Secundário', 'AUAS', 1),
            ('SA-04', 'Setor de Adensamento Controlado', 'AUAC', 1),
            ('SA-05', 'Setor de Adensamento Especial', 'AUAE', 1),
            ('SE-01', 'Setor Especial de Interesse Cultural', 'AUAP', 1),
            ('SE-02', 'Setor Especial de Interesse Público', 'AUAP', 1),
            ('SE-03', 'Setor Especial de Interesse Educacional', 'AUAS', 1),
            ('SE-04', 'Setor Especial de Conservação de Morros', NULL, 1),
            ('SE-05', 'Setor Especial de Conservação de Várzeas', NULL, 1),
            ('SE-06', 'Setor Especial de Interesse Industrial', 'AUAC', 1),
            ('SE-06A','Setor Especial de Interesse Industrial Misto', 'AUAC', 1),
            ('SE-07', 'Setor Especial 07 (índices definidos por lei específica)', NULL, 1),
            ('SE-08', 'Setor Especial de Centralidade Urbana', NULL, 1),
            ('SE-09', 'Setor Especial de Interesse de Segurança Pública', 'AUAS', 1);

        -- Parametros urbanisticos (exemplos resumidos)
        INSERT OR IGNORE INTO parametros_urbanisticos (macrozona_codigo, zona_codigo, coeficiente_aprov, gabarito_maximo, area_minima_lote, taxa_ocupacao_max, cidade_id) VALUES
            ('AUAP','SA-01', 4.0, 45, 240, 0.60, 1),
            ('AUAP','SA-02', 3.0, 25, 240, 0.60, 1),
            ('AUAS','SA-03', 2.0, 15, 240, 0.60, 1),
            ('AUAC','SA-04', 1.5, 9,  240, 0.60, 1),
            ('AUAE','SA-05', 1.0, 9,  450, 0.60, 1),
            ('AUPA',NULL,   0.1, 9,  5000, 0.10, 1),
            ('ARPA',NULL,   0.1, 9, 20000, 0.05, 1),
            ('ARUC',NULL,   0.1, 9, 20000, 0.10, 1);

        -- Usos permitidos
        INSERT OR IGNORE INTO usos_permitidos (macrozona_codigo, zona_codigo, tipo_uso, porte, cnae, permissao, cidade_id) VALUES
            ('AUAP', 'SA-01', 'Residencial Unifamiliar', NULL, NULL, 'Permitido', 1),
            ('AUAP', 'SA-01', 'Residencial Multifamiliar', NULL, NULL, 'Permitido', 1),
            ('AUPA', NULL, 'Residencial Multifamiliar', NULL, NULL, 'Proibido', 1),
            ('ARPA', NULL, 'Residencial Unifamiliar', NULL, NULL, 'Permitido', 1),
            ('AUAP', 'SA-02', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Permitido', 1),
            ('AUAS', 'SA-03', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Condicionado', 1),
            ('AUAC', 'SA-04', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Proibido', 1);

        -- Faixa especial
        INSERT OR IGNORE INTO faixa_especial (codigo, descricao, cidade_id) VALUES
            ('FV', 'Faixa Viária', 1),
            ('FR', 'Faixa Rodoviária', 1);

        -- Zona-faixa especial
        INSERT OR IGNORE INTO zona_faixa_especial (zona_codigo, faixa_codigo, cidade_id) VALUES
            ('SA-01', 'FV', 1),
            ('SA-02', 'FV', 1),
            ('SA-02', 'FR', 1),
            ('SA-03', 'FV', 1),
            ('SA-03', 'FR', 1),
            ('SA-04', 'FR', 1),
            ('SA-05', 'FV', 1);
    """)

    conn.commit()
    conn.close()
