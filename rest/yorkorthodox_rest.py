from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import List, Tuple

cwd = os.path.dirname(os.path.realpath(__file__))
lectionary_db_path = f"{cwd}/db/YOCal_Master.db"
services_db_path = f"{cwd}/db/services.db"


class NoDataException(Exception):
    pass


def __query(query, args=tuple(), fetchall=False) -> Tuple:
    with sqlite3.connect(lectionary_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall if fetchall else cursor.fetchone()

    if not result or not isinstance(result, tuple):
        raise NoDataException()

    return result


def __get_table_columns(table_name: str) -> List[str]:
    with sqlite3.connect(lectionary_db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in result]


main_columns = __get_table_columns("yocal_main")
lect_columns = __get_table_columns("yocal_lectionary")

app = Flask(__name__)


@app.route("/")
@cross_origin()
def hello():
    return render_template("hello.html")


@app.route("/lectionary", methods=["GET"])
@cross_origin()
def get_date():
    try:
        date = request.args.get("date")

        # Get everything except the readings into a dictionary with table-name keys
        query_result = __query("SELECT * FROM yocal_main WHERE date = ?", (date,))
        main_data = dict(zip(main_columns, query_result))

        # Pass-through these fields
        result = {k: main_data[k] for k in ["fast", "basil"]}

        # Display date
        result["date_str"] = (
            f'{main_data["day_name"]}, {main_data["ord"]}'
            f' {main_data["month"]} {main_data["year"]}'
        )
        result["tone"] = f'{main_data["tone"]} - {main_data["eothinon"]}'

        # Designations
        result["desig"] = ", ".join(
            filter(
                lambda d: d,
                [
                    main_data["desig_a"],
                    main_data["desig_g"],
                    main_data["major_commem"],
                    main_data["fore_after"],
                ],
            )
        )

        # Saints
        result["general_saints"] = main_data["class_5"]
        result["british_saints"] = main_data["british"]

        # Lectionary
        lect_query_text = (
            "SELECT lect_1, lect_2, text_1, text_2 FROM yocal_lections where code = ?"
        )

        # Epistles
        (
            result["a_lect_1"],
            result["a_lect_2"],
            result["a_text_1"],
            result["a_text_2"],
        ) = (
            __query(lect_query_text, (main_data["a_code"],))
            if main_data["a_code"]
            else ["" for _ in range(4)]
        )

        # Gospel
        (
            _,
            result["g_lect"],
            _,
            result["g_text"],
        ) = (
            __query(lect_query_text, (main_data["g_code"],))
            if main_data["g_code"] and main_data["g_code"] != main_data["a_code"]
            else ["" for _ in range(4)]
        )

        # "Extra"
        (
            result["x_lect_1"],
            result["x_lect_2"],
            result["x_text_1"],
            result["x_text_2"],
        ) = (
            __query(lect_query_text, (main_data["x_code"],))
            if main_data["x_code"]
            else ["" for _ in range(4)]
        )

        # Commemorations
        (
            result["c_lect_1"],
            result["c_lect_2"],
            result["c_text_1"],
            result["c_text_2"],
        ) = (
            __query(lect_query_text, (main_data["c_code"],))
            if main_data["c_code"]
            else ["" for _ in range(4)]
        )

        # Bold the readings for the Liturgy when appropriate
        if (main_data["a_code"][0] == "G" and (main_data["a_code"][1] != "S" or main_data["a_code"] == "G7Sat")) or main_data["a_code"] in ["E36Wed", "E36Fri"]:
            # There is no Liturgy Mon-Fri in Lent, or on Holy Saturday, or on Wed and Fri of Cheesefare Week
            pass

        else:
            if main_data["c_code"]:
                if main_data["is_comm_apos"]:
                    result["c_lect_1"] = f"<b>{result['c_lect_1']}</b>"
                else:
                    result["a_lect_1"] = f"<b>{result['a_lect_1']}</b>"

                if main_data["is_comm_gosp"]:
                    result["c_lect_2"] = f"<b>{result['c_lect_2']}</b>"
                elif result['a_lect_2']:
                    result['a_lect_2'] = f"<b>{result['a_lect_2']}</b>"
                elif result['g_lect']:
                    result['g_lect'] = f"<b>{result['g_lect']}</b>"

            else:
                result['a_lect_1'] = f"<b>{result['a_lect_1']}</b>"
                if result['a_lect_2']:
                    result['a_lect_2'] = f"<b>{result['a_lect_2']}</b>"
                if result['g_lect']:
                    result['g_lect'] = f"<b>{result['g_lect']}</b>"

        return jsonify(result)

    except NoDataException:
        return jsonify({"error": "Data not found"}), 404


@app.route("/services", methods=["GET"])
@cross_origin()
def get_services():
    date = request.args.get("date")
    num_services = request.args.get("num_services")

    # Connect to the SQLite database
    with sqlite3.connect(services_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT date_str, commemoration, Group_Concat(d.text, ", ")'
            " FROM services s JOIN descriptions d ON d.service_id = s.id"
            " WHERE timestamp >= ?"
            " GROUP BY s.id"
            " LIMIT ?",
            (date, num_services),
        )
        results = cursor.fetchall()

    result = [dict(zip(["date", "commemoration", "description"], r)) for r in results]
    return jsonify(result)
