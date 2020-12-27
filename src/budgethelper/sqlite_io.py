#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Class object for handling IO of a sqlite database

Author: Preocts <preocts@preocts.com>
"""
import sqlite3
import logging

from typing import List

from budgethelper.sqlite_schema import database_tables as schema
from budgethelper.sqlite_schema import TransRow

logger = logging.getLogger(__name__)


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

    def get_column_names(self, table_name) -> List[str]:
        """ return column names from given table """
        if table_name not in schema:
            msg = "Invalid table_name provided. Double check sqlite.schema."
            logger.error(msg)
            raise Exception(msg)
        self.cursor.execute(schema[table_name]["list_columns"])
        return [c[0] for c in self.cursor.description]

    def _schema_init(self) -> None:
        """ Ensures database has the proper schema, builds if needed """
        tables = self._get_tables()
        for table in schema:
            if table not in tables:
                self._build_table(table)

    def _build_table(self, table: str) -> None:
        """ Build table from schema"""
        self.cursor.execute(schema[table]["table_schema"])
        self.conn.commit()

    def save_row(self, table: str, row_data: TransRow) -> None:
        """ Save a transactions to the database """
        for key, value in row_data.items():
            if not isinstance(value, schema[table]["required"][key]):
                msg = (
                    f"Invalid data type for {key}. Found {type(value)}, "
                    f"expecting {schema[table]['required'][key]}"
                )
                logger.error(msg)
                raise Exception(msg)
        values = tuple(row_data.values())
        self.conn.commit()
        self.cursor.execute(schema[table]["save_row"], values)

    def get_trans(self) -> int:
        """ Read a transactions to the database """
        return self.changes

    def update_trans(self) -> int:
        """ Update a transactions in the database """
        return self.changes

    def list_trans(self) -> int:
        """ Read a group of transactions from database """
        return self.changes
