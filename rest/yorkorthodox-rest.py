from flask import Flask, render_template, jsonify
import sqlite3
from sqlite3 import Connection, Cursor
from typing import List


def __get_table_columns(conn: Connection, table_name: str) -> List[str]:
    cursor = conn.cursor()
    query = f"PRAGMA table_info({table_name})"
    cursor.execute(query)
    result = cursor.fetchall()
    return [row[1] for row in result]


with sqlite3.connect('db/lectionary_2021_2031.db') as conn:
    table_columns = __get_table_columns(conn, 'main')

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/lectionary/<date>', methods=['GET'])
def get_date(date):
    with sqlite3.connect('db/lectionary_2021_2031.db') as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM main WHERE date_code = '{date}'"
        cursor.execute(query)
        result = cursor.fetchone()

    if result:
        return jsonify(dict(zip(table_columns, result)))
    else:
        return jsonify({'error': 'Data not found'}), 404
