import sqlite3
import requests
import datetime
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
        CREATE TABLE IF NOT EXISTS harvest (
            id INTEGER PRIMARY KEY,
            territorial_level_code INTEGER,
            territorial_level TEXT,
            measure_unit_code INTEGER,
            measure_unit TEXT,
            value INTEGER,
            municipality_code INTEGER,
            municipality TEXT,
            variable_code INTEGER,
            variable TEXT,
            year_code INTEGER,
            year INTEGER,
            product_code INTEGER,
            product TEXT,
            UNIQUE(
                territorial_level_code,
                measure_unit_code,
                municipality_code,
                variable_code,
                year_code,
                product_code
            )
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS production (
            id INTEGER PRIMARY KEY,
            territorial_level_code INTEGER,
            territorial_level TEXT,
            measure_unit_code INTEGER,
            measure_unit TEXT,
            value INTEGER,
            municipality_code TEXT,
            municipality TEXT,
            variable_code INTEGER,
            variable TEXT,
            year_code INTEGER,
            year INTEGER,
            product_code INTEGER,
            product TEXT,
            UNIQUE(
                territorial_level_code,
                measure_unit_code,
                municipality_code,
                variable_code,
                year_code,
                product_code
            )
        )
    ''')
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS productivity AS
        SELECT
            me.state_uf,
            h.year,
            SUM(p.value) / SUM(h.value) AS productivity
        FROM
            harvest h
        JOIN
            production p ON h.municipality_code = p.municipality_code AND h.year = p.year
        JOIN
            state_municipality me ON h.municipality_code = me.municipality_id_ibge
        GROUP BY
            me.state_code, h.year
    ''')
    conn.commit()
    conn.close()


@logging_function
def insert_or_update(year):
    def clean_value(value):
        return None if value == '-' else value
    
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    url_area = f'https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216/p/{year}/c782/40124?formato=json'
    url_producao = f'https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/214/p/{year}/c782/40124?formato=json'
    
    response_area = requests.get(url_area).json()
    response_producao = requests.get(url_producao).json()
    
    for item in response_area[1:]:
        item['V'] = clean_value(item['V'])
        cursor.execute('''
            INSERT OR REPLACE INTO colheita (
                nivel_territorial_codigo, nivel_territorial, unidade_medida_codigo, unidade_medida, valor, municipio_codigo, municipio, variavel_codigo, variavel, ano_codigo, ano, produto_codigo, produto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['NC'], item['NN'], item['MC'], item['MN'], item['V'], item['D1C'], item['D1N'], item['D2C'], item['D2N'], item['D3C'], item['D3N'], item['D4C'], item['D4N']
        ))
        
    for item in response_producao[1:]:
        item['V'] = clean_value(item['V'])
        cursor.execute('''
            INSERT OR REPLACE INTO producao (
                nivel_territorial_codigo, nivel_territorial, unidade_medida_codigo, unidade_medida, valor, municipio_codigo, municipio, variavel_codigo, variavel, ano_codigo, ano, produto_codigo, produto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['NC'], item['NN'], item['MC'], item['MN'], item['V'], item['D1C'], item['D1N'], item['D2C'], item['D2N'], item['D3C'], item['D3N'], item['D4C'], item['D4N']
        ))
        
    conn.commit()
    conn.close()


@logging_function
def delete(year):
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM colheita WHERE ano_codigo = ?', (year,))
    cursor.execute('DELETE FROM producao WHERE ano_codigo = ?', (year,))
    conn.commit()
    conn.close()


@logging_function
def insert_or_update_till_current_year():
    start_year = 2018
    current_year = datetime.datetime.now().year
    for year in range(start_year, current_year + 1):
        insert_or_update(year=year)


if __name__ == '__main__':
    create_tables()
    insert_or_update_till_current_year()
