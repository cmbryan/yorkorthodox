#!/usr/bin/env python3

import json
import os
from pathlib import Path
import sqlite3


cwd = Path(os.path.realpath(os.path.dirname(__file__)))

lectionary_db_path = cwd / '..' / 'db' / 'lectionary_2021_2031.db'
output_path = cwd / '..' / 'db' / 'services.db'
if os.path.exists(output_path):
    os.remove(output_path)

with sqlite3.connect(output_path) as service_conn, \
     sqlite3.connect(lectionary_db_path) as lectionary_conn:
    service_cur = service_conn.cursor()
    lectionary_cur = lectionary_conn.cursor()

    service_cur.execute('CREATE TABLE services (id INTEGER PRIMARY KEY, timestamp, date_str, commemoration)')
    service_cur.execute('CREATE TABLE descriptions (service_id, text,'
                        ' FOREIGN KEY (service_id) REFERENCES services (id))')
    service_cur.execute('PRAGMA foreign_keys = ON;')

    with open(cwd / '..' / 'data' / 'services.json') as input_fh:
        services = json.load(input_fh)

    for service in services:
        # Get relevant information from the lectionary
        lectionary_cur.execute('SELECT date_str, major_commem'
                               ' FROM main WHERE date_code=?',
                               (service['date'],))
        lectionary_data = lectionary_cur.fetchone()

        service_cur.execute('INSERT INTO services (timestamp, date_str, commemoration)'
                    'VALUES (?, ?, ?)',
                    (f'{service["date"]} {service["time"]}', *lectionary_data))
        service_id = service_cur.lastrowid

        for description in service['description']:
            service_cur.execute('INSERT INTO descriptions (service_id, text)'
                           'VALUES (?, ?)',
                           (service_id, description))
