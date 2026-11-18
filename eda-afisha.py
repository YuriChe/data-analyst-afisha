import os
import pandas as pd
from dotenv import load_dotenv
from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.engine import URL     

load_dotenv()

def get_engine():
    # пароль: из .env, а нет файла — спросят интерактивно
    password = os.getenv('DB_PWD') or getpass('Пароль: ')

    return create_engine(
        URL.create(
            'postgresql+psycopg2',
            username=os.getenv('DB_USER', 'praktikum_student'),
            password=password,
            host=os.getenv('DB_HOST', 'rc1e-oa2gp4mf9egcsq5k.mdb.yandexcloud.net'),
            port=int(os.getenv('DB_PORT', '6432')),
            database=os.getenv('DB_NAME', 'data-analyst-afisha'),
        ),
        connect_args={'sslmode': 'require'},
    )

engine = get_engine()


