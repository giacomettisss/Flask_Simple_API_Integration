import sqlite3
import requests
import datetime
import logging
from functools import wraps


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def logging_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Iniciando a função {func.__name__}')
        if args:            
            logging.info(f' - Args: {args}')
        if kwargs:
            logging.info(f' -  Kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logging.info(f'Função {func.__name__} concluída')
        return result
    return wrapper


@logging_function
def create_tables():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS colheita (
            id INTEGER PRIMARY KEY,
            nivel_territorial_codigo TEXT,
            nivel_territorial TEXT,
            unidade_medida_codigo TEXT,
            unidade_medida TEXT,
            valor INTEGER,
            municipio_codigo TEXT,
            municipio TEXT,
            variavel_codigo TEXT,
            variavel TEXT,
            ano_codigo INTEGER,
            ano TEXT,
            produto_codigo TEXT,
            produto TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producao (
            id INTEGER PRIMARY KEY,
            nivel_territorial_codigo TEXT,
            nivel_territorial TEXT,
            unidade_medida_codigo TEXT,
            unidade_medida TEXT,
            valor INTEGER,
            municipio_codigo TEXT,
            municipio TEXT,
            variavel_codigo TEXT,
            variavel TEXT,
            ano_codigo INTEGER,
            ano TEXT,
            produto_codigo TEXT,
            produto TEXT
        )
    ''')
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS produtividade AS
        SELECT
            me.sg_uf AS estado,
            c.ano,
            SUM(p.valor) / SUM(c.valor) AS produtividade
        FROM
            colheita c
        JOIN
            producao p ON c.municipio_codigo = p.municipio_codigo AND c.ano = p.ano
        JOIN
            municipio_estado me ON c.municipio_codigo = me.id_municipio_ibge
        GROUP BY
            me.sg_uf, c.ano
    ''')
    conn.commit()
    conn.close()


@logging_function
def insert_or_update(year):
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    url_area = f'https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/216/p/{year}/c782/40124?formato=json'
    url_producao = f'https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/214/p/{year}/c782/40124?formato=json'
    
    response_area = requests.get(url_area).json()
    response_producao = requests.get(url_producao).json()
    
    for item in response_area:
        cursor.execute('''
            INSERT OR REPLACE INTO colheita (
                nivel_territorial_codigo, nivel_territorial, unidade_medida_codigo, unidade_medida, valor, municipio_codigo, municipio, variavel_codigo, variavel, ano_codigo, ano, produto_codigo, produto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['NC'], item['NN'], item['MC'], item['MN'], item['V'], item['D1C'], item['D1N'], item['D2C'], item['D2N'], item['D3C'], item['D3N'], item['D4C'], item['D4N']
        ))
        
    for item in response_producao:
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
    start_year = 2023
    current_year = datetime.datetime.now().year
    for year in range(start_year, current_year + 1):
        insert_or_update(year=year)


if __name__ == '__main__':
    create_tables()
    insert_or_update_till_current_year()
