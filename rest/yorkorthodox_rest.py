from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import sqlite3
from sqlite3 import Connection, Cursor
from typing import List


def __get_table_columns(conn: Connection, table_name: str) -> List[str]:
    cursor = conn.cursor()
    query = f"PRAGMA table_info({table_name})"
    cursor.execute(query)
    result = cursor.fetchall()
    return [row[1] for row in result]


db_path = 'db/lectionary_2021_2031.db'

with sqlite3.connect(db_path) as conn:
    table_columns = __get_table_columns(conn, 'main')

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/lectionary', methods=['GET'])
@cross_origin()
def get_date():
    date = request.args.get('date')
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM main WHERE date_code = ?"
        cursor.execute(query, (date,))
        result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Data not found'}), 404
    
    data_dict = dict(zip(table_columns, result))

    # format designations
    data_dict['desig'] = ', '.join([d for d in [data_dict['desig_a'], data_dict['desig_g']] if d])
    data_dict.pop('desig_a')
    data_dict.pop('desig_g')

    return jsonify(data_dict)


@app.route('/services', methods=['GET'])
@cross_origin()
def get_services():
    date = request.args.get('date')
    num_services = request.args.get('num_services')

    # Connect to the SQLite database
    with sqlite3.connect('db/services.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date_str, commemoration, Group_Concat(d.text, ", ")'
                       ' FROM services s JOIN descriptions d ON d.service_id = s.id'
                       ' WHERE timestamp >= ?'
                       ' GROUP BY s.id'
                       ' LIMIT ?',
                       (date, num_services))
        results = cursor.fetchall()

    result = [dict(zip(['date', 'commemoration', 'description'], r)) for r in results]
    return jsonify(result)
