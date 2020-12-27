#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class object for handling IO of a sqlite database

Author: Preocts <preocts@preocts.com>
"""
import sqlite3


class SQLiteio:
    """Abstraction for SQLite3 storage

    Args:
        database_name: name of the database file to open

    """

    def __init__(self, database_name: str) -> None:
        """ Initilize class """
        self.database_name = database_name
        self.conn = sqlite3.connect(database=database_name)

    @property
    def changes(self) -> int:
        """ Return the # of changes pending """
        return self.conn.total_changes

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
