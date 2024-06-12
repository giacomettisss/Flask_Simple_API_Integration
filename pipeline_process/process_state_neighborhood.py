import sqlite3
import csv
import logging
from functools import wraps


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Iniciando a função {func.__name__}')
        logging.info(f'Args: {args}, Kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logging.info(f'Função {func.__name__} concluída')
        return result
    return wrapper


@log_function_call
def create_tables():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS municipio_estado (
            id INTEGER
            id_uf_ibge INTEGER,
            sg_uf TEXT,
            id_municipio_ibge INTEGER,
            nm_municipio TEXT,
            PRIMARY KEY (id)
        )
    ''')
    conn.commit()
    conn.close()


@log_function_call
def populate_municipio_estado():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()

    csv_file = './data/process_state_neighborhood/dct_municipio_uf.csv'
    
    with open(csv_file, 'r', encoding='latin1') as file:
        reader = csv.DictReader(file, delimiter=';')
        columns = reader.fieldnames
        print(columns)
        cursor.execute('BEGIN TRANSACTION')
        for row in reader:
            print(row)
            cursor.execute('''
                INSERT OR REPLACE INTO municipio_estado (
                    id_uf_ibge, sg_uf, id_municipio_ibge, nm_municipio
                ) VALUES (?, ?, ?, ?)
            ''', (row['id_uf_ibge'], row['sg_uf'], row['id_municipio_ibge'], row['nm_municipio']))
        cursor.execute('COMMIT')
    
    conn.close()


if __name__ == '__main__':
    create_tables()
    populate_municipio_estado()
