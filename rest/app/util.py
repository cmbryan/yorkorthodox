import os
import sqlite3
from typing import Dict, List, Tuple


class NoDataException(Exception):
    pass


cwd = os.path.dirname(os.path.realpath(__file__))
lectionary_db_path = f"{cwd}/db/YOCal_Master.db"
services_db_path = f"{cwd}/db/services.db"


def __get_table_columns(table_name: str) -> List[str]:
    with sqlite3.connect(lectionary_db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in result]


main_columns = __get_table_columns("yocal_main")
lect_columns = __get_table_columns("yocal_lectionary")


def build_designation(data_dict: Dict[str, str]) -> str:
    """Concatenate the various descriptions of the day"""
    return ", ".join(
        filter(
            lambda d: d,
            [
                data_dict["desig_a"],
                data_dict["desig_g"],
                data_dict["major_commem"],
                data_dict["fore_after"],
            ],
        )
    )


def build_date_str(data: Dict[str, str]) -> str:
    """Build a printable date"""
    return f'{data["day_name"]}, {data["ord"]} {data["month"]} {data["year"]}'


def query(database: str, query_txt: str, args=tuple(), fetchall=False) -> Tuple:
    """Perform an SQL query and return some data, or throw an exception."""
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(query_txt, args)
        result = cursor.fetchall if fetchall else cursor.fetchone()

    if not result or not isinstance(result, tuple):
        raise NoDataException()

    return result


def get_data_dict(date: str) -> Dict[str, str]:
    """Get the data for everything except the readings into a dictionary with table-name keys"""
    query_result = query(lectionary_db_path, "SELECT * FROM yocal_main WHERE date = ?", (date,))
    data = dict(zip(main_columns, query_result))
    return data


def get_services(date: str, num_services: int) -> List[Dict[str, str]]:
    """Get the next N services"""
    results = (
        query(
            services_db_path,
            'SELECT date_str, commemoration, Group_Concat(d.text, ", ")'
            " FROM services s JOIN descriptions d ON d.service_id = s.id"
            " WHERE timestamp >= ?"
            " GROUP BY s.id"
            " LIMIT ?",
            (date, num_services),
            fetchall=True,
        ),
    )
    return [dict(zip(["date", "commemoration", "description"], str(r))) for r in results]
