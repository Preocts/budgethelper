#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class object for handling transactions via SQLiteio

Author: Preocts <preocts@preocts.com>
"""
import logging

from datetime import datetime
from typing import Dict
from typing import TypedDict
from typing import Any
from typing import List

from budgethelper import sqlite_io

logger = logging.getLogger(__name__)


class SchemaDict(TypedDict):
    """ Custom typing: dict """

    table_schema: str
    required_cols: Dict[str, Any]


class TransRow(TypedDict, total=False):
    """ Custom typing: dict """

    uid: int
    source: int
    amount: float
    description: str
    date: datetime


class DBTransactions(sqlite_io.SQLiteio):
    """ Abstraction of SQL CRUD methods for transaction table """

    def __init__(self, database: str) -> None:
        """Creates an transaction table object for CRUD operations

        Aurgs:
            database: path/name of database file to open
        """
        super().__init__(database)
        self._col_names: List[str] = []
        self._schema: SchemaDict = {
            "table_schema": (
                "CREATE TABLE transactions ( "
                "uid INTEGER PRIMARY KEY, "
                "source INTEGER NOT NULL, "
                "amount NUMERIC NOT NULL, "
                "description TEXT NOT NULL, "
                "date DATETIME NOT NULL )"
            ),
            "required_cols": {
                "source": int,
                "amount": float,
                "description": str,
                "date": datetime,
            },
        }

    def init(self) -> None:
        """ Ensures database has the proper schema, builds if needed """
        tables = self.get_tables()
        if "transactions" not in tables:
            self._build_table()
        self._get_column_names()
        for col in self._schema["required_cols"]:
            if col not in self._col_names:
                msg = "Invalid table schema found during initalization."
                logger.error(msg)
                raise Exception(msg)

    def _build_table(self) -> None:
        """ Build table from schema"""
        self.cursor.execute(self._schema["table_schema"])
        self.conn.commit()

    def _get_column_names(self) -> List[str]:
        """ Return column names from given table """
        self.cursor.execute("SELECT * from transactions where uid = 0")
        self._col_names = [c[0] for c in self.cursor.description]
        return self._col_names

    def save_row(self, row_data: TransRow) -> None:
        """ Save a transactions to the database """
        self.cursor.execute(
            "INSERT INTO transactions(source, amount, description, date) "
            "VALUES(?, ?, ?, ?)",
            (
                row_data["source"],
                row_data["amount"],
                row_data["description"],
                row_data["date"],
            ),
        )
        self.conn.commit()

    def get_trans(self, uid: int) -> TransRow:
        """ Returns transaction by uid """
        self.cursor.execute("SELECT * FROM transactions WHERE uid = ?", (uid,))
        results = self.cursor.fetchone()
        if not results:
            msg = f"UID not found: {uid}"
            logger.error(msg)
            raise Exception(msg)
        translated: TransRow = {
            "uid": results[0],
            "source": results[1],
            "amount": results[2],
            "description": results[3],
            "date": results[4],
        }
        return translated

    def update_trans(self, row_data: TransRow) -> None:
        """Update a transactions in the database

        Augs:
            row_data[TransRow]: Transaction data dictionary.
        """
        try:
            self.cursor.execute(
                "UPDATE transactions SET source = ?, amount = ?, "
                "description = ?, date = ? WHERE uid = ?",
                (
                    row_data["source"],
                    row_data["amount"],
                    row_data["description"],
                    row_data["date"],
                    row_data["uid"],
                ),
            )
        except KeyError as err:
            msg = f"Incorrect format for row_data: {err}"
            logger.error(msg)
            raise Exception(msg) from err

    def list_trans(self) -> int:
        """ Read a group of transactions from database """
        return self.changes
