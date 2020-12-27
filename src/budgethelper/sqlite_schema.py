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
    list_columns: str
    save_row: str


class TransRow(TypedDict):
    """ Schema for Transaction Types """

    source: int
    amount: float
    date: datetime


database_tables: Dict[str, SchemaDict] = {
    "transactions": {
        "table_schema": (
            "CREATE TABLE transactions "
            "( id INTEGER PRIMARY KEY, "
            "source INTEGER NOT NULL, "
            "amount NUMERIC NOT NULL, "
            "date DATETIME NOT NULL )"
        ),
        "required": {
            "source": int,
            "amount": float,
            "date": datetime,
        },
        "column_names": (
            "id",
            "source",
            "amount",
            "date",
        ),
        "list_columns": "SELECT * FROM transactions WHERE id = 0",
        "save_row": "INSERT INTO transactions(source, amount, date) "
        "VALUES (?, ?, ?)",
    },
}
