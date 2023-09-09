#!/usr/bin/env python3

import json
import os
from pathlib import Path
import sqlite3

from util import build_date_str, build_designation, get_data_dict


cwd = Path(os.path.realpath(os.path.dirname(__file__)))

lectionary_db_path = cwd / '..' / 'app' / 'db' / 'YOCal_master.db'
output_path = cwd / '..' / 'app' / 'db' / 'services.db'
if os.path.exists(output_path):
    os.remove(output_path)
assert os.path.exists(output_path.parent), "lectionary database is needed"


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
        lectionary_data = get_data_dict(service["date"])
        date_str = build_date_str(lectionary_data)
        designation = build_designation(lectionary_data)

        service_cur.execute('INSERT INTO services (timestamp, date_str, commemoration)'
                    'VALUES (?, ?, ?)',
                    (f'{service["date"]} {service["time"]}', date_str, designation))
        service_id = service_cur.lastrowid

        for description in service['description']:
            service_cur.execute('INSERT INTO descriptions (service_id, text)'
                           'VALUES (?, ?)',
                           (service_id, description))
