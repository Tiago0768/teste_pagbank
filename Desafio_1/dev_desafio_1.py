import os, warnings, time
import sqlite3 as sql

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def desafio_1():

    #TABELA CANDIDATES
    drop_table_candidates = """drop table candidates"""

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
        (3, 'M', 49, 'Democratic'),
        (4, 'M', 60, 'Republic'),
        (5, 'M', 61, 'Republic'),
        (6, 'M', 48, 'Republic')
    ]

    insert_candidates = f"""INSERT INTO candidates (id, gender, age, party) VALUES (?, ?, ?, ?)
    """

    #TABELA RESULTS
    drop_table_results = """drop table results"""

    create_results = """CREATE TABLE results (
    constituency_id INTEGER PRIMARY KEY,
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

    #execução tabela candidates
    cursor_sd.execute(drop_table_candidates)
    cursor_sd.execute(create_candidates)
    cursor_sd.execute(insert_candidates, valores_tabela_candidates)
    cursor_sd.execute("SELECT * FROM candidates")
    candidatos = cursor_sd.fetchall()

    #execução tabela results
    cursor_sd.execute(drop_table_results)
    cursor_sd.execute(create_results)
    cursor_sd.execute(insert_results, valores_tabela_results)
    cursor_sd.execute("SELECT * FROM results")
    resultados = cursor_sd.fetchall()

    con_sd.commit()

    print(candidatos)
    print(resultados)

desafio_1()