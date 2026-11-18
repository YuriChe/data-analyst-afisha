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

query = '''
        SELECT
            user_id,
        device_type_canonical,
        order_id,
        created_dt_msk AS order_dt,
        created_ts_msk AS order_ts,
        currency_code,
        revenue,
        tickets_count,
        created_dt_msk::date - LAG(created_dt_msk::date) OVER (PARTITION BY user_id
        ORDER BY
            created_dt_msk) AS days_since_prev,
        event_id,
        event_name_code AS event_name,
        event_type_main,
        service_name,
        region_name,
        city_name
        FROM afisha.purchases p
        JOIN afisha.events e
                USING (event_id)
        JOIN afisha.city c
                USING (city_id)
        JOIN afisha.regions r
                USING (region_id)
        WHERE
            p.device_type_canonical IN ('mobile', 'desktop') AND event_type_main != 'фильм'
'''

df = pd.read_sql_query(query, con=engine)


