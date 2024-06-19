import os, warnings, time
import sqlite3 as sql
from tabulate import tabulate

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def desafio_3():

    ordenacao_entrada = '>'
    dia_evento = '6'

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

    resposta_letra_b = f"""
    SELECT 
    COUNT(DISTINCT evento_nome) as eventos
    FROM 
        ANALITICO_PAGSHOW
    WHERE 
        strftime('%w', evento_inicio) = {dia_evento}"""

    #letra a
    cursor_sd.execute(resposta_letra_a)
    resultado_letra_a = cursor_sd.fetchall()

    #letra b
    cursor_sd.execute(resposta_letra_b)
    resultado_letra_b = cursor_sd.fetchall()

    print(resultado_letra_a)
    print(resultado_letra_b)

desafio_3()