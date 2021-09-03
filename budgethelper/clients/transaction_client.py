"""
Provider class for database Transaction table
"""
import datetime
import logging
import sqlite3
from typing import List
from typing import Optional

from budgethelper.clients.databaseabc import DatabaseABC
from budgethelper.constants import TRANSACTION_TABLE_SCHEMA
from budgethelper.exceptions import TransactionsTableError
from budgethelper.models.database import Database
from budgethelper.models.transaction import Transaction


class TransactionClient(DatabaseABC):
    TABLE_NAME = "transactions"

    def __init__(self, database: Database) -> None:
        """Provisions SQL client to database for transaction table"""
        self.log = logging.getLogger(__name__)
        self.database = database
        self.conn = sqlite3.connect(database=database.name)

        if self.TABLE_NAME not in self.listtables(self.conn):
            raise TransactionsTableError(f"Table missing '{self.TABLE_NAME}'")

        for column in TRANSACTION_TABLE_SCHEMA["required_cols"]:
            if column not in self.listcolumns():
                raise TransactionsTableError(f"Column missing '{column}'")

    def listcolumns(self) -> List[str]:
        """Return column names from given table"""

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT * from transactions where uid = 0")
            self._col_names = [c[0] for c in cursor.description]

        finally:
            cursor.close()

        return self._col_names

    def create(self, row_data: Transaction) -> None:
        """Create a transaction row in the database"""

        sql = (
            "INSERT INTO transactions("
            "source, amount, description, date, created_on, updated_on) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        values = (
            row_data.source,
            row_data.amount,
            row_data.description,
            row_data.date,
            row_data.created_on,
            row_data.updated_on,
        )

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

    def read(self, uid: int) -> Transaction:
        """Returns transaction by uid"""

        cursor = self.conn.cursor()
        sql = (
            "SELECT source, amount, description, date, created_on, updated_on, uid "
            "FROM transactions WHERE uid = ?"
        )

        try:
            cursor.execute(sql, (uid,))
            results = cursor.fetchone()

        finally:
            cursor.close()

        if not results:
            msg = f"Unable to read, UID not found: {uid}"
            self.log.error(msg)
            raise TransactionsTableError(msg)

        return Transaction(*results)

    def getlist(
        self,
        since: datetime.date,
        until: Optional[datetime.date] = None,
    ) -> List[Transaction]:
        """Gets a time-range of transactions, returns them in a list"""

        until = until if until else since + datetime.timedelta(days=29)
        sql = (
            "SELECT source, amount, description, date, created_on, updated_on, uid "
            "FROM transactions WHERE date BETWEEN ? and ? "
            "ORDER BY uid"
        )
        values = (since, until)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            results = cursor.fetchall()

        finally:
            cursor.close()

        return [Transaction(*row) for row in results]

    def update(self, transaction: Transaction) -> None:
        """Update a transactions in the database"""

        sql = (
            "UPDATE transactions "
            "SET source = ?, amount = ?, description = ?, "
            "date = ?, updated_on = ? "
            "WHERE uid = ?"
        )
        values = (
            transaction.source,
            transaction.amount,
            transaction.description,
            transaction.date,
            transaction.updated_on,
            transaction.uid,
        )

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()

    def delete(self, uid: int) -> None:
        """Delete a row from the database, should not have downstream effects"""

        sql = "DELETE FROM transactions WHERE uid = ?"
        values = (uid,)

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql, values)
            self.conn.commit()

        finally:
            cursor.close()
