#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for sqlite_io.py

Author: Preocts <preocts@preocts.com>
"""
import unittest

from datetime import datetime

# from unittest.mock import patch

from budgethelper import sqlite_io
from budgethelper import sqlite_schema


class TestSQLiteio(unittest.TestCase):
    """ Test cases """

    def setUp(self) -> None:
        """ Setup """
        self.conn = sqlite_io.SQLiteio(":memory:")
        return super().setUp()

    def tearDown(self) -> None:
        """ Teardown """
        del self.conn
        return super().tearDown()

    def test_opens_database(self) -> None:
        """ Ensure we open database on initialization """
        dbconn = sqlite_io.SQLiteio(":memory:")
        self.assertEqual(dbconn.changes, 0)

    def test_table_creation(self) -> None:
        """ Check for correctly created tables """
        self.conn.cursor.execute(
            "SELECT * FROM sqlite_master WHERE type = 'table'"
        )
        results = self.conn.cursor.fetchall()
        table_list = [i[1] for i in results]
        for i in sqlite_schema.database_tables:
            self.assertIn(i, table_list)

    def test_table_schema_matches(self) -> None:
        """ Confirm config schema is being used """
        for table in sqlite_schema.database_tables:
            results = self.conn.get_column_names(table)
            for col in sqlite_schema.database_tables[table]["column_names"]:
                self.assertIn(col, results)

        with self.assertRaises(Exception):
            self.conn.get_column_names("fake_table")

    def test_add_row_transaction(self) -> None:
        """ Add a row to given table, follow schema """
        table: str = "transactions"
        row: sqlite_schema.TransRow = {
            "source": 0,
            "amount": 10.99,
            "date": datetime.now(),
        }
        change_count: int = self.conn.changes
        self.conn.save_row(table, row)
        self.assertEqual(self.conn.changes, change_count + 1)

        # Breaking type for validation type outside of mypy
        row["source"] = "TestFail"  # type: ignore
        with self.assertRaises(Exception):
            self.conn.save_row(table, row)  # type: ignore

    def test_get_row_transaction(self) -> None:
        """ Get a row from a given table, force schema """
        table: str = "transactions"
        row: sqlite_schema.TransRow = {
            "source": 99,
            "amount": 99.99,
            "date": datetime.now(),
        }
        self.conn.save_row(table, row)
        results = self.conn.get_row_by_rid(table, 1)
        self.assertIsInstance(results, dict)
        self.assertEqual(results["rid"], 1)
        self.assertEqual(results["source"], 99)
        self.assertEqual(results["amount"], 99.99)
