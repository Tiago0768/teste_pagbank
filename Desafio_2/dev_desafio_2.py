import os, warnings, time
import sqlite3 as sql
from tabulate import tabulate

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def desafio_2():

    #TABELA students
    drop_table_students = """DROP TABLE IF EXISTS students"""

    create_students = """CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    college_name TEXT
    )
    """

    valores_tabela_students = [
        (1352, 'Howard Fields','University of California, Davis'),
        (1801, 'Tyrone Doyle', 'Santa Clara University'),
        (2079, 'Albert Burgess', 'Yale University'),
        (2616, 'Patrick Hum', 'Bryn Mawr College'),
        (3920, 'Diana Hum', 'Yale University'),
        (4226, 'Eugene Rogers', 'Dartmouth College')
    ]

    insert_students = f"""INSERT INTO students (id, name, college_name) VALUES (?, ?, ?)
    """

    #execução tabela students
    cursor_sd.execute(drop_table_students)
    cursor_sd.execute(create_students)
    cursor_sd.executemany(insert_students, valores_tabela_students)

    #TABELA participations
    drop_table_participations = """DROP TABLE IF EXISTS participations"""

    create_participations = """CREATE TABLE participations (
    participant_id INTEGER,
    student_id INTEGER,
    category TEXT, 
    score INTEGER
    )
    """

    valores_tabela_participations = [
    (11853, 5746, 'Caribou Contest', 92),
    (12114, 2616, 'Spelling Bee', 38),
    (12267, 2079, 'Debate', 55),
    (14036, 2079, 'Google Science Fair', 33),
    (14149, 1801, 'Google Science Fair', 87),
    (19674, 6698, 'RoboCup', 89),
    (20679, 5746, 'RoboCup', 98),
    (20718, 8721, 'Caribou Contest', 66),
    (20847, 2616, 'Caribou Contest', 64)
    ]

    insert_participations = """INSERT INTO participations (participant_id, student_id, category, score) VALUES (?, ?, ?, ?)"""

    #execução tabela participations
    cursor_sd.execute(drop_table_participations)
    cursor_sd.execute(create_participations)
    cursor_sd.executemany(insert_participations, valores_tabela_participations)

    # variaveis vencedores ordenados
    decrescente = 'DESC'
    ascendente = 'ASC'
    ordenacao_ranking = '<='
    ranking = 3

    # resposta desafio 2
    consulta = f"""
    WITH vencedores_ordenados AS (
        SELECT
        category,
        student_id,
        name AS nome,
        college_name,
        score,
        ROW_NUMBER()
            OVER (
                PARTITION BY 
                category 
                ORDER BY score {decrescente}, 
                college_name {ascendente}) AS ordenacao_ranking
        FROM
            participations p 
            JOIN students s ON p.student_id = s.id
    )
    SELECT
    category,
    student_id,
    nome,
    college_name,
    score
    FROM
        vencedores_ordenados
    WHERE
        ordenacao_ranking {ordenacao_ranking} {ranking}
    ORDER BY
        category {ascendente},
        score {decrescente}
    LIMIT 3
    """

    #execução query resposta desafio 2
    cursor_sd.execute(consulta)
    vencedores = cursor_sd.fetchall()

    if vencedores:
        headers = ["category", "student_id", "Nome", "college_name", "score"]
        tabela_vencedores = tabulate(vencedores, headers=headers, tablefmt="pretty")
        print("O top 3 vencedores são: ")
        print("")
        print(tabela_vencedores)
    else:
        print("Não foram encontrados vencedores.")

    return vencedores