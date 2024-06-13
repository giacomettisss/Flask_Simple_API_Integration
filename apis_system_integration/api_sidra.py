from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/harvested_area/<int:neighborhood_id>/<int:year>', methods=['GET'])
def get_harvested_area(neighborhood_id, year):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM colheita WHERE municipio_codigo = ? AND ano_codigo = ?', (neighborhood_id, year)).fetchone()
    conn.close()
    if data:
        return jsonify(success=True, data=dict(data), message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


@app.route('/productivity/<int:year>', methods=['GET'])
def get_productivity(year):
    states  = request.args.getlist('estados')
    conn = get_db_connection()
    query = 'SELECT * FROM produtividade WHERE ano = ? AND estado IN ({seq})'.format(seq=','.join(['?']*len(states )))
    data = conn.execute(query, [year] + states ).fetchall()
    conn.close()
    data = [dict(row) for row in data]
    if data:
        return jsonify(success=True, data=data, message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


@app.route('/produced_quantity', methods=['GET'])
def get_produced_quantity():
    neighborhoods = request.args.getlist('neighborhoods')
    years = request.args.getlist('anos')
    if len(neighborhoods) * len(years) > 100:
        return jsonify(success=False, data=None, message='Request exceeds 100 data points limit')

    conn = get_db_connection()
    query = 'SELECT * FROM producao WHERE municipio_codigo IN ({seq1}) AND ano_codigo IN ({seq2})'.format(seq1=','.join(['?']*len(neighborhoods)), seq2=','.join(['?']*len(years)))
    data = conn.execute(query, neighborhoods + years).fetchall()
    conn.close()
    data = [dict(row) for row in data]
    if data:
        return jsonify(success=True, data=data, message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')


if __name__ == '__main__':
    app.run(debug=True)
