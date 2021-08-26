"""
Class object for handling transactions via SQLiteio

Author: Preocts
"""
import dataclasses
import datetime
import logging
from typing import List
from typing import Optional

from budgethelper.constants import TRANSACTION_TABLE_SCHEMA
from budgethelper.dbconnection import DBConnection


@dataclasses.dataclass(frozen=True)
class TransRow:
    """Custom typing: dict"""

    source: int
    amount: float
    description: str
    date: datetime.date
    uid: Optional[int] = None


class TransactionsTableError(Exception):
    ...


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

    def save_row(self, row_data: TransRow) -> None:
        """Save a transactions to the database"""

        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO transactions(source, amount, description, date) "
                "VALUES(?, ?, ?, ?)",
                (
                    row_data.source,
                    row_data.amount,
                    row_data.description,
                    row_data.date,
                ),
            )
            self.conn.commit()

        finally:
            cursor.close()

    def get_trans(self, uid: int) -> TransRow:
        """Returns transaction by uid"""

        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "SELECT uid, source, amount, description, date "
                "FROM transactions WHERE uid = ?",
                (uid,),
            )
            results = cursor.fetchone()

        finally:
            cursor.close()

        if not results:
            msg = f"UID not found: {uid}"
            self.log.error(msg)
            raise Exception(msg)

        return TransRow(
            uid=results[0],
            source=results[1],
            amount=results[2],
            description=results[3],
            date=results[4],
        )

    def update_trans(self, row_data: TransRow) -> None:
        """
        Update a transactions in the database

        Augs:
            row_data[TransRow]: Transaction data dictionary.
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "UPDATE transactions SET source = ?, amount = ?, "
                "description = ?, date = ? WHERE uid = ?",
                (
                    row_data.source,
                    row_data.amount,
                    row_data.description,
                    row_data.date,
                    row_data.uid,
                ),
            )

        finally:
            cursor.close()

    def list_trans(
        self,
        since: datetime.date,
        until: Optional[datetime.date] = None,
    ) -> List[TransRow]:
        """Gets a time-range of transactions, returns them in a list"""

        until = until if until else since + datetime.timedelta(days=29)

        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "SELECT source, amount, description, date, uid "
                "FROM transactions WHERE date BETWEEN ? and ? "
                "ORDER BY uid",
                (since, until),
            )
            results = cursor.fetchall()

        finally:
            cursor.close()

        return [TransRow(*row) for row in results]
