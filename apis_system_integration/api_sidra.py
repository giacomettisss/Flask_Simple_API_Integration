from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/area_colhida/<int:municipio_id>/<int:ano>', methods=['GET'])
def get_area_colhida(municipio_id, ano):
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM colheita WHERE municipio_codigo = ? AND ano_codigo = ?', (municipio_id, ano)).fetchone()
    conn.close()
    if data:
        return jsonify(success=True, data=dict(data), message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')

@app.route('/produtividade/<int:ano>', methods=['GET'])
def get_produtividade(ano):
    estados = request.args.getlist('estados')
    conn = get_db_connection()
    query = 'SELECT * FROM produtividade WHERE ano = ? AND estado IN ({seq})'.format(seq=','.join(['?']*len(estados)))
    data = conn.execute(query, [ano] + estados).fetchall()
    conn.close()
    if data:
        return jsonify(success=True, data=[dict(row) for row in data], message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')

@app.route('/quantidade_produzida', methods=['GET'])
def get_quantidade_produzida():
    municipios = request.args.getlist('municipios')
    anos = request.args.getlist('anos')
    if len(municipios) * len(anos) > 100:
        return jsonify(success=False, data=None, message='Request exceeds 100 data points limit')

    conn = get_db_connection()
    query = 'SELECT * FROM producao WHERE municipio_codigo IN ({seq1}) AND ano_codigo IN ({seq2})'.format(seq1=','.join(['?']*len(municipios)), seq2=','.join(['?']*len(anos)))
    data = conn.execute(query, municipios + anos).fetchall()
    conn.close()
    if data:
        return jsonify(success=True, data=[dict(row) for row in data], message='Data retrieved successfully')
    else:
        return jsonify(success=False, data=None, message='No data found')

if __name__ == '__main__':
    app.run(debug=True)
