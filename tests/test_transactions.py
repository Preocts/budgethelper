#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing for transctions.py

Author: Preocts <preocts@preocts.com>
"""
import random
import unittest
import datetime

from typing import Generator

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
            "date": datetime.datetime.now(),
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
            "date": datetime.datetime.now(),
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
            "date": datetime.datetime.now(),
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

    def test_04_list_rows(self) -> None:
        """ Test listing transactions from a start/end date """
        random.seed()
        dates = TestTransactions.date_gen("2021-01-01")
        for _ in range(100):
            row: transactions.TransRow = {
                "source": random.randint(0, 99),  # nosec
                "amount": round(random.random(), 2),  # nosec
                "description": "Lots of entries",
                "date": next(dates),
            }
            self.dbconn.save_row(row)
        since = datetime.date.fromisoformat("2020-12-01")
        results = self.dbconn.list_trans(since)
        self.assertEqual(len(results), 30)
        since = datetime.date.fromisoformat("1995-12-01")
        results = self.dbconn.list_trans(since)
        self.assertEqual(len(results), 0)
        since = datetime.date.fromisoformat("2020-12-01")
        until = datetime.date.fromisoformat("2020-12-10")
        results = self.dbconn.list_trans(since, until)
        self.assertEqual(len(results), 10)

    @classmethod
    def date_gen(cls, startdate: str) -> Generator:
        """ Generate dates counting backward from the given start """
        idx = 0
        base = datetime.date.fromisoformat(startdate)
        while True:
            idx += 1
            yield base - datetime.timedelta(days=idx)
