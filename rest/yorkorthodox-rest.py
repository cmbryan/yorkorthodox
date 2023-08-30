from flask import Flask, render_template, jsonify
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
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/lectionary_raw/<date>', methods=['GET'])
def get_raw_date(date):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM main WHERE date_code = '{date}'"
        cursor.execute(query)
        result = cursor.fetchone()

    if result:
        return jsonify(dict(zip(table_columns, result)))
    else:
        return jsonify({'error': 'Data not found'}), 404


@app.route('/lectionary/<date>', methods=['GET'])
@cross_origin()
def get_date(date):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM main WHERE date_code = '{date}'"
        cursor.execute(query)
        result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'Data not found'}), 404
    
    data_dict = dict(zip(table_columns, result))

    # format designations
    data_dict['desig'] = ', '.join([d for d in [data_dict['desig_a'], data_dict['desig_g']] if d])
    data_dict.pop('desig_a')
    data_dict.pop('desig_g')

    # 

    return jsonify(data_dict)
