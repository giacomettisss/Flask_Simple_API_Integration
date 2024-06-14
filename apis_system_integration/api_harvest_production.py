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
        'Get Harvested Area': '/harvested_area?year={year}&municipality_id={id}',
        'Get Productivity': '/productivity?year={year}&state_uf={state}',
        'Get Produced Quantity': '/produced_quantity?year={year}&municipality_id={id}'
    }
    return jsonify(success=True, data=data, message='Data retrieved successfully')

@app.route('/harvested_area', methods=['GET'])
def get_harvested_area():
    year = request.args.get('year', type=int)
    municipality_id = request.args.get('municipality_id', type=int)
    if not year or not municipality_id:
        return jsonify(success=False, message='One `year` and one `municipality_id` are required'), 400
    
    query = 'SELECT * FROM harvest WHERE municipality_code = ? AND year_codigo = ?'
    with closing(get_db_connection()) as conn:
        data = conn.execute(query, (municipality_id, year)).fetchone()

    if data:
        return jsonify(success=True, data=dict(data), message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


@app.route('/productivity', methods=['GET'])
def get_productivity():
    year = request.args.get('year', type=int)
    states = request.args.getlist('state_uf')
    if not year or not states:
        return jsonify(success=False, message='One `year` and one or more `state` are required'), 400
    
    query = 'SELECT * FROM productivity WHERE year = ? AND state_uf IN ({seq1})'.format(
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
    neighborhoods = request.args.getlist('municipality_id', type=int)
    if not neighborhoods or not years:
        return jsonify(success=False, message='One or more `year` and one or more `municipality_id` are required.'), 400
    
    if len(neighborhoods) * len(years) > 100:
        return jsonify(success=False, data=None, message='Request exceeds 100 data points limit'), 400

    query = 'SELECT * FROM production WHERE municipality_code IN ({seq1}) AND year IN ({seq2})'.format(
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
