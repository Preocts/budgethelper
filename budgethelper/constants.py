"""
Constant values

Author: Preocts
"""
import datetime
from typing import Any
from typing import Dict
from typing import TypedDict


class SchemaDict(TypedDict):
    """Custom typing: dict"""

    table_schema: str
    required_cols: Dict[str, Any]


TRANSACTION_TABLE_SCHEMA: SchemaDict = {
    "table_schema": (
        "CREATE TABLE transactions ( "
        "uid INTEGER PRIMARY KEY, "
        "source INTEGER NOT NULL, "
        "amount NUMERIC NOT NULL, "
        "description TEXT NOT NULL, "
        "date DATE NOT NULL )"
    ),
    "required_cols": {
        "source": int,
        "amount": float,
        "description": str,
        "date": datetime.date,
    },
}
