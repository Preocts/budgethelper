"""
Constant values
"""
import datetime
import pathlib
from typing import Any
from typing import Dict
from typing import TypedDict


class SchemaDict(TypedDict):
    """Custom typing: dict"""

    table_schema: str
    required_cols: Dict[str, Any]


DATABASE_FILE = pathlib.Path(__file__).parent / "database.db"

DATABASE_TABLES = [
    "TRANSACTION_TABLE_SCHEMA",
    "SOURCES_TABLE_SCHEMA",
]

TRANSACTION_TABLE_SCHEMA: SchemaDict = {
    "table_schema": (
        "CREATE TABLE transactions ( "
        "uid INTEGER PRIMARY KEY, "
        "source INTEGER NOT NULL, "
        "amount NUMERIC NOT NULL, "
        "description TEXT NOT NULL, "
        "date DATE NOT NULL, "
        "created_on DATE NOT NULL, "
        "updated_on DATE NOT NULL)"
    ),
    "required_cols": {
        "source": int,
        "amount": float,
        "description": str,
        "date": datetime.date,
        "created_on": datetime.datetime,
        "updated_on": datetime.datetime,
    },
}

SOURCES_TABLE_SCHEMA: SchemaDict = {
    "table_schema": (
        "CREATE TABLE sources ("
        "uid INTEGER PRIMARY KEY, "
        "created_on DATE NOT NUL:, "
        "updated_on DATE NOT NULL, "
        "name TEXT NOT NULL)"
    ),
    "required_cols": {
        "name": str,
        "created_on": datetime.datetime,
        "updated_on": datetime.datetime,
    },
}
