#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for sqlite_io.py

Author: Preocts <preocts@preocts.com>
"""
import unittest

# from unittest.mock import patch

from budgethelper import sqlite_io


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

    def test_transaction_table_made(self) -> None:
        """ Check for correct table """
        self.conn.cursor.execute(
            "SELECT * FROM sqlite_master WHERE type = 'table'"
        )
        results = self.conn.cursor.fetchall()
        table_list = [i[1] for i in results]
        expected = ["transactions"]
        for i in expected:
            self.assertIn(i, table_list)
