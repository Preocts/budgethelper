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

    def test_01_save_row(self) -> None:
        """ Add a row to given table, follow schema """
        row: transactions.TransRow = {
            "source": 0,
            "amount": 10.99,
            "description": "Happy go lucky now",
            "date": datetime.now(),
        }
        change_count: int = self.dbconn.changes
        self.dbconn.save_row(row)
        self.assertEqual(self.dbconn.changes, change_count + 1)

    def test_02_get_row(self) -> None:
        """ Get a row from a given table, force schema """
        row: transactions.TransRow = {
            "source": 99,
            "amount": 99.99,
            "description": "Nine Nine Nine",
            "date": datetime.now(),
        }
        self.dbconn.save_row(row)
        self.dbconn.commit()
        results = self.dbconn.get_trans(1)
        self.assertIsInstance(results, dict)
        self.assertEqual(results["uid"], 1)
        self.assertEqual(results["source"], 99)
        self.assertEqual(results["amount"], 99.99)
        self.assertEqual(results["description"], "Nine Nine Nine")

    def test_03_update_row(self) -> None:
        """ Test updating with valid and invalid data """
        row: transactions.TransRow = {
            "source": 99,
            "amount": 99.99,
            "description": "Nine Nine Nine",
            "date": datetime.now(),
        }
        self.dbconn.save_row(row)
        self.dbconn.commit()
        row["uid"] = 1
        row["source"] = 10
        row["description"] = "Updated"
        self.dbconn.update_trans(row)
        results = self.dbconn.get_trans(1)
        self.assertEqual(results["description"], "Updated")

        del row["description"]
        with self.assertRaises(Exception):
            self.dbconn.update_trans(row)
