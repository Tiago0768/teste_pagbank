import os, warnings, time
import sqlite3 as sql

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def analitico_pagshow():

    #TABELA bruta para etl da pagshow
    drop_table_students = """DROP TABLE IF EXISTS ANALITICO_PAGSHOW"""

    create_students = """CREATE TABLE ANALITICO_PAGSHOW (
    evento_nome TEXT,
    evento_inicio TIMESTAMP,
    artista_nome TEXT,
    cliente_nome TEXT,
    cliente_cpf TEXT,
    cliente_telefone TEXT,
    cliente_entrada TIMESTAMP
    )
    """

    valores_tabela_students = [
        ('Funn Festival', '01/04/2023 22:00', 'Bruno & Mamone', 'Lucas', '111.111.111-11', '5513992123212', '01/04/2023 22:43'),
        ('Fuzuê', '02/04/2023 22:00', 'Michel Teló', 'Pedro', '222.222.222-22', '5511982332556', '02/04/2023 22:31'),
        ('Comédia Stand Up', '03/04/2023 22:00', 'Fábio Rabin', 'Leonardo', '333.333.333-33', '5513991857732', '03/04/2023 22:12'),
        ('Fuzuê', '04/04/2023 22:00', 'Michel Teló', 'Vivian', '444.444.444-44', '5521997889889', '04/04/2023 22:01'),
        ('2 Minutes To Midnight', '05/04/2023 22:00', 'Iron Maiden', 'Anne', '555.555.555-55', '5511988272121', '05/04/2023 22:21'),
        ('Comédia Stand Up', '03/04/2023 22:00', 'Fábio Rabin', 'Lucas', '111.111.111-11', '5513992123212', '03/04/2023 22:04'),
        ('2 Minutes To Midnight', '07/04/2023 22:00', 'Iron Maiden', 'Rodrigo', '666.666.666-66', '5511945311288', '07/04/2023 22:06'),
        ('Funn Festival', '01/04/2023 22:00', 'Bruno & Marrone', 'Pedro', '222.222.222-22', '5511982332556', '01/04/2023 22:40'),
        ('Oceano', '09/04/2023 22:00', 'Djavan', 'Suellen', '777.777.777-77', '5521991012434', '09/04/2023 23:06')
    ]


    insert_students = f"""INSERT INTO ANALITICO_PAGSHOW (evento_nome, evento_inicio, artista_nome, cliente_nome, cliente_cpf, cliente_telefone, cliente_entrada) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    query_analitica = """select * from ANALITICO_PAGSHOW"""

    #execução tabela students
    cursor_sd.execute(drop_table_students)
    cursor_sd.execute(create_students)
    cursor_sd.executemany(insert_students, valores_tabela_students)

    cursor_sd.execute(query_analitica)
    resultado_analitica = cursor_sd.fetchall()

    con_sd.commit()

    return resultado_analitica