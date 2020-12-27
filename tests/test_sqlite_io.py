#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for sqlite_io.py

Author: Preocts <preocts@preocts.com>
"""
import os
import unittest
import sqlite3

# from unittest.mock import patch

from budgethelper import sqlite_io


class TestSQLiteio(unittest.TestCase):
    """ Test cases """

    def setUp(self) -> None:
        """ Setup """
        conn = sqlite3.connect("./tests/fixtures/testdb")
        conn.close()
        return super().setUp()

    def tearDown(self) -> None:
        """ Teardown """
        os.remove("./tests/fixtures/testdb")
        return super().tearDown()

    def test_opens_database(self) -> None:
        """ Ensure we open database on initialization """
        dbconn = sqlite_io.SQLiteio(":memory:")
        self.assertEqual(dbconn.changes, 0)
