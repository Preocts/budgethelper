#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class object for handling IO of a sqlite database

Author: Preocts <preocts@preocts.com>
"""
import sqlite3

from typing import List


class SQLiteio:
    """Abstraction for SQLite3 storage

    Args:
        database_name: name of the database file to open

    """

    def __init__(self, database_name: str) -> None:
        """ Initilize class """
        self.database_name = database_name
        self.conn = sqlite3.connect(database=database_name)
        self.cursor = self.conn.cursor()
        self._schema_init()

    @property
    def changes(self) -> int:
        """ Return the # of changes pending """
        return self.conn.total_changes

    def _get_tables(self) -> List[str]:
        """ return a list of tables in the database """
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        results = self.cursor.fetchall()
        return [t[1] for t in results]

    def _schema_init(self) -> None:
        """ Ensures database has the proper schema, builds if needed """
        tables = self._get_tables()
        if "transactions" not in tables:
            self._build_transaction_table()

    def _build_transaction_table(self) -> None:
        """ Build transactions table """
        self.cursor.execute(
            "CREATE TABLE transactions "
            "(trns INTEGER PRIMARY KEY, "
            "source INTEGER NOT NULL, "
            "amount NUMERIC)"
        )
        self.conn.commit()

    def save_trans(self) -> int:
        """ Save a transactions to the database """
        return self.changes

    def get_trans(self) -> int:
        """ Read a transactions to the database """
        return self.changes

    def update_trans(self) -> int:
        """ Update a transactions in the database """
        return self.changes

    def list_trans(self) -> int:
        """ Read a group of transactions from database """
        return self.changes
