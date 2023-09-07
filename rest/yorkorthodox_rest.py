from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import List

cwd = os.path.dirname(os.path.realpath(__file__))
lectionary_db_path = f'{cwd}/db/YOCal_Master.db'
services_db_path = f'{cwd}/db/services.db'


class NoDataException(Exception):
    pass


def __query(query, args=tuple(), fetchall=False):
    with sqlite3.connect(lectionary_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall if fetchall else cursor.fetchone()

    if not result:
        raise NoDataException()

    return result


def __get_table_columns(table_name: str) -> List[str]:
    with sqlite3.connect(lectionary_db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in result]


main_columns = __get_table_columns('yocal_main')
lect_columns = __get_table_columns('yocal_lectionary')

app = Flask(__name__)

@app.route('/')
@cross_origin()
def hello():
    return render_template('hello.html')


@app.route('/lectionary', methods=['GET'])
@cross_origin()
def get_date():
    try:
        date = request.args.get('date')
        query_result = __query('SELECT * FROM yocal_main WHERE date = ?', (date,))
        if not isinstance(query_result, tuple):
            raise NoDataException()
        main_data = dict(zip(main_columns, query_result))

        # Pass-through
        result = {k:main_data[k] for k in ['fast', 'basil']}

        result['date_str'] = f'{main_data["day_name"]}, {main_data["ord"]}' \
                             f' {main_data["month"]} {main_data["year"]}'
        result['tone'] = f'{main_data["tone"]} - {main_data["eothinon"]}'
        
        result['desig'] = ', '.join(filter(lambda d:d, [
            main_data['desig_a'],
            main_data['desig_g'],
            main_data['major_commem'],
            main_data['fore_after']
        ]))

        result['general_saints'] = main_data['class_5']
        result['british_saints'] = main_data['british']

        return jsonify(result)

    except NoDataException:
        return jsonify({'error': 'Data not found'}), 404


@app.route('/services', methods=['GET'])
@cross_origin()
def get_services():
    date = request.args.get('date')
    num_services = request.args.get('num_services')

    # Connect to the SQLite database
    with sqlite3.connect(services_db_path) as conn:
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
