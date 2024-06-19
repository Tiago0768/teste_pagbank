import os, warnings, time
import sqlite3 as sql
from tabulate import tabulate

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

    #execução tabela students
    cursor_sd.execute(drop_table_students)
    cursor_sd.execute(create_students)
    cursor_sd.executemany(insert_students, valores_tabela_students)

    con_sd.commit()

    #trazendo a coluna dia (ainda sem formatacao)
    cursor_sd.execute("""
    ALTER TABLE ANALITICO_PAGSHOW
    ADD COLUMN dia INTEGER;
    """)
    con_sd.commit()

    #update com o tratamento do campo dia
    cursor_sd.execute("""
    UPDATE ANALITICO_PAGSHOW
        SET dia = CAST((CAST(substr(evento_inicio, 1, 10) AS INTEGER) - 1) % 7 AS INTEGER)
    """)
    con_sd.commit()

    query_analitica = """select * from ANALITICO_PAGSHOW"""

    cursor_sd.execute(query_analitica)
    resultado_analitica = cursor_sd.fetchall()

    return resultado_analitica

def desafio_3():

    ordenacao_entrada = '>'
    
    resposta_letra_a = f"""
    SELECT 
    evento_nome, 
    COUNT(*) as total_pos_horario
    FROM 
        ANALITICO_PAGSHOW
    WHERE 
        cliente_entrada {ordenacao_entrada} evento_inicio
    GROUP BY 
        evento_nome
    """

    dia_evento = 6

    resposta_letra_b = f"""
    SELECT 
    COUNT(DISTINCT evento_nome) as eventos,
    CASE dia
        WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
                WHEN 2 THEN 'Terça-feira'
                    WHEN 3 THEN 'Quarta-feira'
                        WHEN 4 THEN 'Quinta-feira'
                            WHEN 5 THEN 'Sexta-feira'
                                WHEN 6 THEN 'Sábado'
    END as dia_semana
    FROM 
        ANALITICO_PAGSHOW
    WHERE 
        dia = {dia_evento}"""

    # letra a
    cursor_sd.execute(resposta_letra_a)
    resultado_letra_a = cursor_sd.fetchall()
    headers_letra_a = [description[0] for description in cursor_sd.description]

    # letra b
    # cursor.description acessa informações das colunas da consulta.
    cursor_sd.execute(resposta_letra_b)
    resultado_letra_b = cursor_sd.fetchall()
    headers_letra_b = [description[0] for description in cursor_sd.description]

    print("")
    print("resposta opção a")
    resposta_a = print(tabulate(resultado_letra_a, headers=headers_letra_a, tablefmt="grid"))
    print("")
    print("resposta opção b")
    resposta_b = print(tabulate(resultado_letra_b, headers=headers_letra_b, tablefmt="grid"))

    return resposta_a, resposta_b

analitico_pagshow()
