"""
Class object for handling transactions via SQLiteio

Author: Preocts
"""
import datetime
import logging
from typing import List
from typing import Optional

from budgethelper.constants import TRANSACTION_TABLE_SCHEMA
from budgethelper.dbconnection import DBConnection
from budgethelper.exceptions import TransactionsTableError
from budgethelper.models.transaction import Transaction


class DBTransactions(DBConnection):
    """Abstraction of SQL CRUD methods for transaction table"""

    log = logging.getLogger(__name__)

    def __init__(self, database: str) -> None:
        """
        Creates an transaction table object for CRUD operations

        If the table is missing from the database, will create.

        Aurgs:
            database: path/name of database file to open

        Raises:
            TransactionsTableError
        """
        super().__init__(database)

        self._col_names: List[str] = []

        tables = self.get_tables()

        if "transactions" not in tables:
            self.log.debug("Transactions table missing... creating")
            self._build_table()

        for col in TRANSACTION_TABLE_SCHEMA["required_cols"]:
            if col not in self._get_column_names():
                msg = "Invalid table schema found during initalization."
                self.log.error(msg)
                raise TransactionsTableError(msg)

    def _build_table(self) -> None:
        """Build table from schema"""

        cursor = self.conn.cursor()

        try:
            cursor.execute(TRANSACTION_TABLE_SCHEMA["table_schema"])
            self.conn.commit()

        finally:
            cursor.close()

    def _get_column_names(self) -> List[str]:
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

    def get(self, uid: int) -> Transaction:
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
            msg = f"Unable to GET, UID not found: {uid}"
            self.log.error(msg)
            raise TransactionsTableError(msg)

        return Transaction(*results)

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

        finally:
            cursor.close()

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
