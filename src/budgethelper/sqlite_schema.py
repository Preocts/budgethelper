#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Schema vars for building SQLite3 database tables

Author: Preocts <preocts@preocts.com>
"""
from typing import Tuple
from typing import Dict
from typing import TypedDict


class SchemaDict(TypedDict):
    """ Custom dict schema """

    table_schema: str
    column_names: Tuple[str, ...]
    list_columns: str


database_tables: Dict[str, SchemaDict] = {
    "transactions": {
        "table_schema": (
            "CREATE TABLE transactions "
            "( id INTEGER PRIMARY KEY, "
            "source INTEGER NOT NULL, "
            "amount NUMERIC NOT NULL, "
            "date DATETIME NOT NULL )"
        ),
        "column_names": (
            "id",
            "source",
            "amount",
            "date",
        ),
        "list_columns": "SELECT * FROM transactions WHERE id = 0",
    },
}
