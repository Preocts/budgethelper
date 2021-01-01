#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for sqlite_io.py

Author: Preocts <preocts@preocts.com>
"""
import sqlite3
import unittest

from budgethelper import sqlite_io


class TestSQLiteio(unittest.TestCase):
    """ Test cases """

    def setUp(self) -> None:
        """ Setup """
        self.dbconn = sqlite_io.SQLiteio(":memory:")
        self.dbconn.cursor.execute(
            "CREATE TABLE test01 (id INTEGER PRIMARY KEY )"
        )
        self.dbconn.cursor.execute(
            "CREATE TABLE test02 (id INTEGER PRIMARY KEY )"
        )
        self.dbconn.cursor.execute(
            "CREATE TABLE test03 (id INTEGER PRIMARY KEY )"
        )
        return super().setUp()

    def tearDown(self) -> None:
        """ Teardown """
        del self.dbconn
        return super().tearDown()

    def test_opens_database(self) -> None:
        """ Ensure we open database on initialization """
        dbconn = sqlite_io.SQLiteio(":memory:")
        self.assertEqual(dbconn.database_name, ":memory:")
        self.assertIsInstance(dbconn.conn, sqlite3.Connection)
        self.assertIsInstance(dbconn.cursor, sqlite3.Cursor)

    def test_table_creation(self) -> None:
        """ Check for correctly created tables """
        tables = self.dbconn.get_tables()
        expected = ["test01", "test02", "test03"]
        self.assertEqual(tables, expected)
