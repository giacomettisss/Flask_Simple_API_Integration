import sqlite3
import csv
import logging
from functools import wraps


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def logging_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Function Started: {func.__name__}')
        if args:            
            logging.info(f' > Args: {args}')
        if kwargs:
            logging.info(f' > Kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logging.info(f'Function Completed: {func.__name__}')
        return result
    return wrapper


@logging_function
def create_tables():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS state_municipality (
            id INTEGER PRIMARY KEY,
            state_ibge_id INTEGER,
            state_uf TEXT,
            municipality_ibge_id INTEGER,
            municipality_name TEXT
        )
    ''')
    conn.commit()
    conn.close()


@logging_function
def populate_estado_municipio():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()

    csv_file = './data/process_state_neighborhood/dct_municipio_uf.csv'
    
    with open(csv_file, 'r', encoding='latin1') as file:
        reader = csv.DictReader(file, delimiter=';')
        columns = reader.fieldnames
        cursor.execute('BEGIN TRANSACTION')
        for row in reader:
            cursor.execute('''
                INSERT OR REPLACE INTO estado_municipio (
                    state_ibge_id, state_uf, municipality_ibge_id, municipality_name
                ) VALUES (?, ?, ?, ?)
            ''', (row['id_uf_ibge'], row['sg_uf'], row['id_municipio_ibge'], row['nm_municipio']))
        cursor.execute('COMMIT')
    
    conn.close()


if __name__ == '__main__':
    create_tables()
    populate_estado_municipio()
