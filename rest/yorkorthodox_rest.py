from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import List, Tuple

from .util import NoDataException, build_date_str, build_designation, get_data_dict, get_services, query





app = Flask(__name__)


@app.route("/")
@cross_origin()
def hello():
    return render_template("hello.html")


@app.route("/lectionary", methods=["GET"])
@cross_origin()
def get_date():
    try:
        date = request.args.get("date") or ""
        main_data = get_data_dict(date)

        # Pass-through these fields
        result = {k: main_data[k] for k in ["fast", "basil"]}

        # Display date
        result["date_str"] = build_date_str(main_data)
        result["tone"] = f'{main_data["tone"]} - {main_data["eothinon"]}'

        # Designations
        result["desig"] = build_designation(main_data)

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
            query(lect_query_text, (main_data["a_code"],))
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
            query(lect_query_text, (main_data["g_code"],))
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
            query(lect_query_text, (main_data["x_code"],))
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
            query(lect_query_text, (main_data["c_code"],))
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
def services():
    date = request.args.get("date") or ""
    num_services = int(request.args.get("num_services") or 0)
    return jsonify(get_services(date, num_services))
