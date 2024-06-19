import os, warnings, time
import sqlite3 as sql

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def desafio_1():

    #TABELA CANDIDATES
    drop_table_candidates = """DROP TABLE IF EXISTS candidates"""

    create_candidates = """CREATE TABLE candidates (
    id INTEGER PRIMARY KEY,
    gender TEXT,
    age INTEGER,
    party TEXT
    )
    """

    valores_tabela_candidates = [
        (1, 'M', 55, 'Democratic'),
        (2, 'M', 51, 'Democratic'),
        (3, 'F', 49, 'Democratic'),
        (4, 'M', 60, 'Republic'),
        (5, 'F', 61, 'Republic'),
        (6, 'F', 48, 'Republic')
    ]

    insert_candidates = f"""INSERT INTO candidates (id, gender, age, party) VALUES (?, ?, ?, ?)
    """

    #execução tabela candidates
    cursor_sd.execute(drop_table_candidates)
    cursor_sd.execute(create_candidates)
    cursor_sd.executemany(insert_candidates, valores_tabela_candidates)

    #TABELA RESULTS
    drop_table_results = """DROP TABLE IF EXISTS results"""

    create_results = """CREATE TABLE results (
    constituency_id INTEGER,
    candidate_id INTEGER,
    votes INTEGER
    )
    """

    valores_tabela_results = [
        (1, 1, 847529),
        (1, 4, 283409),
        (2, 2, 293841),
        (2, 5, 394385),
        (3, 3, 429084),
        (3, 6, 303890)
    ]

    insert_results = """INSERT INTO results (constituency_id, candidate_id, votes) VALUES (?, ?, ?)"""

    #execução tabela results
    cursor_sd.execute(drop_table_results)
    cursor_sd.execute(create_results)
    cursor_sd.executemany(insert_results, valores_tabela_results)

    #execução do resultado
    genero = "F"
    filtro_data = '<'
    valor_idade = '50'

    #query gerando a resposta do desafio
    query_desafio_1 = f"""
    SELECT 
        c.gender, 
        SUM(r.votes) AS votos_ganhos_f
    FROM 
        candidates c
    JOIN 
        results r ON c.id = r.candidate_id
    WHERE 
        c.gender = '{genero}' 
        AND c.age {filtro_data} {valor_idade}
    """
    cursor_sd.execute(query_desafio_1)
    resultado_desafio_1 = cursor_sd.fetchall()

    # genero formatado
    if genero == "F":
        genero_formatado = "feminino"
    else:
        genero_formatado = "masculino"

    # filtro de data formatado 
    if filtro_data == "<":
        filtro_data_formatado = "inferior"
    elif filtro_data == ">":
        filtro_data_formatado = "maior"
    elif filtro_data == "=":
        filtro_data_formatado = "igual"
    elif filtro_data == ">=":
        filtro_data_formatado = " maior igual"
    elif filtro_data == "<=":
        filtro_data_formatado = "menor igual"
    elif filtro_data == "<>":
        filtro_data_formatado = "diferente"

    # votos formatados
    votos_ganhos = resultado_desafio_1[0][1]
    votos_formatados = "{:,}".format(votos_ganhos)

    con_sd.commit()

    #resposta da questão, deixei dinamico caso queiram analisar outros resultados de forma facilitada. 
    resposta_1 = print(f'O número de votos ganhos por candidatas do sexo {genero_formatado} cuja idade é {filtro_data_formatado} a {valor_idade} anos é de {votos_formatados} mil votos contabilizados.')

    return resposta_1