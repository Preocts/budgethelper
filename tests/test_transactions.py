#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for transctions.py

Author: Preocts <preocts@preocts.com>
"""
import unittest

from datetime import datetime

from budgethelper import transactions


class TestTransactions(unittest.TestCase):
    """ Tests covering CRUD operations """

    def setUp(self) -> None:
        self.dbconn = transactions.DBTransactions(":memory:")
        self.dbconn.init()
        return super().setUp()

    def tearDown(self) -> None:
        del self.dbconn
        return super().tearDown()

    def test_add_row_transaction(self) -> None:
        """ Add a row to given table, follow schema """
        row: dict = {
            "source": 0,
            "amount": 10.99,
            "date": datetime.now(),
        }
        change_count: int = self.dbconn.changes
        self.dbconn.save_row(row)
        self.assertEqual(self.dbconn.changes, change_count + 1)

        # Breaking type for validation type outside of mypy
        row["source"] = "TestFail"  # type: ignore
        with self.assertRaises(Exception):
            self.dbconn.save_row(row)  # type: ignore

    def test_get_row_transaction(self) -> None:
        """ Get a row from a given table, force schema """
        row: dict = {
            "source": 99,
            "amount": 99.99,
            "date": datetime.now(),
        }
        self.dbconn.save_row(row)
        results = self.dbconn.get_row_by_rid(1)
        self.assertIsInstance(results, dict)
        self.assertEqual(results["uid"], 1)
        self.assertEqual(results["source"], 99)
        self.assertEqual(results["amount"], 99.99)
