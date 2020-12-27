#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Schema vars for building SQLite3 database tables

Author: Preocts <preocts@preocts.com>
"""
from datetime import datetime
from typing import Tuple
from typing import Dict
from typing import TypedDict
from typing import Any


class SchemaDict(TypedDict):
    """ Custom dict schema """

    table_schema: str
    column_names: Tuple[str, ...]
    required: Dict[str, Any]
    data_type: Any
    list_columns: str
    save_row: str
    get_row: str


class TransRow(TypedDict, total=False):
    """ Schema for Transaction Types """

    rid: int
    source: int
    amount: float
    date: datetime


database_tables: Dict[str, SchemaDict] = {
    "transactions": {
        "table_schema": (
            "CREATE TABLE transactions "
            "( rid INTEGER PRIMARY KEY, "
            "source INTEGER NOT NULL, "
            "amount NUMERIC NOT NULL, "
            "date DATETIME NOT NULL )"
        ),
        "required": {
            "source": int,
            "amount": float,
            "date": datetime,
        },
        "data_type": TransRow,
        "column_names": (
            "rid",
            "source",
            "amount",
            "date",
        ),
        "list_columns": "SELECT * FROM transactions WHERE rid = 0",
        "save_row": "INSERT INTO transactions(source, amount, date) "
        "VALUES (?, ?, ?)",
        "get_row": "SELECT * FROM transactions WHERE rid = ?",
    },
}
