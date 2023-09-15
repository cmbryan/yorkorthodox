import marshmallow as mm
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from util import (
    NoDataException,
    build_date_str,
    build_designation,
    get_data_dict,
    lectionary_db_path,
    query,
)

blp = Blueprint("lectionary", __name__, description="Daily saints and readings")


class LectionaryParameterSchema(mm.Schema):
    """The query parameters required for the end-point."""

    date = mm.fields.Date(required=True)


@blp.route("/lectionary")
class Lectionary(MethodView):
    """An end-point to provide upcoming services and events."""

    @blp.arguments(LectionaryParameterSchema, location="query")
    def get(self, params):
        try:
            main_data = get_data_dict(params["date"])

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
                "SELECT lect_1, lect_2, text_1, text_2"
                " FROM yocal_lections where code = ?"
            )

            # Epistles
            (
                result["a_lect_1"],
                result["a_lect_2"],
                result["a_text_1"],
                result["a_text_2"],
            ) = (
                query(lectionary_db_path, lect_query_text, (main_data["a_code"],))
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
                query(lectionary_db_path, lect_query_text, (main_data["g_code"],))
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
                query(lectionary_db_path, lect_query_text, (main_data["x_code"],))
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
                query(lectionary_db_path, lect_query_text, (main_data["c_code"],))
                if main_data["c_code"]
                else ["" for _ in range(4)]
            )

            # Bold the readings for the Liturgy when appropriate
            has_liturgy = True
            if main_data["a_code"]:
                if (
                    main_data["a_code"][0] == "G"
                    and (
                        main_data["a_code"][1] != "S" or main_data["a_code"] == "G7Sat"
                    )
                ) or main_data["a_code"] in ["E36Wed", "E36Fri"]:
                    # There is no Liturgy Mon-Fri in Lent, or on Holy Saturday, or on Wed and Fri of Cheesefare Week
                    has_liturgy = False

            if has_liturgy:
                if main_data["c_code"]:
                    if main_data["is_comm_apos"]:
                        result["c_lect_1"] = f"<b>{result['c_lect_1']}</b>"
                    else:
                        result["a_lect_1"] = f"<b>{result['a_lect_1']}</b>"

                    if main_data["is_comm_gosp"]:
                        result["c_lect_2"] = f"<b>{result['c_lect_2']}</b>"
                    elif result["a_lect_2"]:
                        result["a_lect_2"] = f"<b>{result['a_lect_2']}</b>"
                    elif result["g_lect"]:
                        result["g_lect"] = f"<b>{result['g_lect']}</b>"

                else:
                    result["a_lect_1"] = f"<b>{result['a_lect_1']}</b>"
                    if result["a_lect_2"]:
                        result["a_lect_2"] = f"<b>{result['a_lect_2']}</b>"
                    if result["g_lect"]:
                        result["g_lect"] = f"<b>{result['g_lect']}</b>"

            return jsonify(result)

        except NoDataException:
            abort(404, "Data not found")
