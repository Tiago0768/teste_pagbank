import os, warnings, time
import sqlite3 as sql
from dev_pagshow_analitico import analitico_pagshow

user_system = os.getlogin()

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
start_diario = time.time()

con_sd = sql.connect('TIAGOFERREIRA.DB')
cursor_sd = con_sd.cursor()

def desafio_3():

    #TABELA bruta para etl da pagshow
    analitico_pagshow_desenv = analitico_pagshow()

    print(analitico_pagshow_desenv)

    return analitico_pagshow_desenv