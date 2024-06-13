from flask import Flask, jsonify, request
from contextlib import closing
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
def get_base():
    data = {
        'Overview': '/',
        'Get Harvested Area': '/harvested_area?neighborhood_id={id}&year={year}',
        'Get Productivity': '/productivity?year={year}&state={state1},{state2}',
        'Get Produced Quantity': '/produced_quantity?neighborhood_id={id1},{id2}&year={year1},{year2}'
    }
    return jsonify(success=True, data=data, message='Data retrieved successfully')

@app.route('/harvested_area', methods=['GET'])
def get_harvested_area():
    year = request.args.get('year', type=int)
    neighborhood_id = request.args.get('neighborhood_id', type=int)
    if not year or not neighborhood_id:
        return jsonify(success=False, message='One `year` and one `neighborhood_id` are required'), 400
    
    query = 'SELECT * FROM colheita WHERE municipio_codigo = ? AND ano_codigo = ?'
    with closing(get_db_connection()) as conn:
        data = conn.execute(query, (neighborhood_id, year)).fetchone()

    if data:
        return jsonify(success=True, data=dict(data), message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


@app.route('/productivity', methods=['GET'])
def get_productivity():
    year = request.args.get('year', type=int)
    states = request.args.getlist('state')
    if not year or not states:
        return jsonify(success=False, message='One `year` and one or more `state` are required'), 400
    
    query = 'SELECT * FROM produtividade WHERE ano = ? AND estado IN ({seq1})'.format(
        seq1=','.join(['?']*len(states))
    )
    with closing(get_db_connection()) as conn:
        data = conn.execute(query, [year] + states).fetchall()

    data = [dict(row) for row in data]
    if data:
        return jsonify(success=True, data=data, message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


@app.route('/produced_quantity', methods=['GET'])
def get_produced_quantity():
    years = request.args.getlist('year', type=int)
    neighborhoods = request.args.getlist('neighborhood_id', type=int)
    if not neighborhoods or not years:
        return jsonify(success=False, message='One or more `year` and one or more `neighborhood_id` are required.'), 400
    
    if len(neighborhoods) * len(years) > 100:
        return jsonify(success=False, data=None, message='Request exceeds 100 data points limit'), 400

    query = 'SELECT * FROM producao WHERE municipio_codigo IN ({seq1}) AND ano IN ({seq2})'.format(
        seq1=','.join(['?']*len(neighborhoods)),
        seq2=','.join(['?']*len(years))
    )
    with closing(get_db_connection()) as conn:
        data = conn.execute(query, neighborhoods + years).fetchall()
        
    data = [dict(row) for row in data]
    if data:
        return jsonify(success=True, data=data, message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


if __name__ == '__main__':
    app.run(debug=True)
