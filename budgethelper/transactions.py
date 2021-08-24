"""
Class object for handling transactions via SQLiteio

Author: Preocts
"""
import datetime
import logging
from typing import List
from typing import Optional
from typing import TypedDict

from budgethelper.constants import TRANSACTION_TABLE_SCHEMA
from budgethelper.dbconnection import DBConnection


class TransRow(TypedDict, total=False):
    """Custom typing: dict"""

    uid: int
    source: int
    amount: float
    description: str
    date: datetime.date


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
            self._build_table()

        for col in TRANSACTION_TABLE_SCHEMA["required_cols"]:
            if col not in self._get_column_names():
                msg = "Invalid table schema found during initalization."
                self.log.error(msg)
                raise TransactionsTableError(msg)

    def _build_table(self) -> None:
        """Build table from schema"""

        self.cursor.execute(TRANSACTION_TABLE_SCHEMA["table_schema"])
        self.conn.commit()

    def _get_column_names(self) -> List[str]:
        """Return column names from given table"""

        self.cursor.execute("SELECT * from transactions where uid = 0")
        self._col_names = [c[0] for c in self.cursor.description]

        return self._col_names

    def save_row(self, row_data: TransRow) -> None:
        """Save a transactions to the database"""

        self.cursor.execute(
            "INSERT INTO transactions(source, amount, description, date) "
            "VALUES(?, ?, ?, ?)",
            (
                row_data["source"],
                row_data["amount"],
                row_data["description"],
                row_data["date"],
            ),
        )

        self.conn.commit()

    def get_trans(self, uid: int) -> TransRow:
        """Returns transaction by uid"""

        self.cursor.execute("SELECT * FROM transactions WHERE uid = ?", (uid,))
        results = self.cursor.fetchone()

        if not results:
            msg = f"UID not found: {uid}"
            self.log.error(msg)
            raise Exception(msg)

        translated: TransRow = {
            "uid": results[0],
            "source": results[1],
            "amount": results[2],
            "description": results[3],
            "date": results[4],
        }

        return translated

    def update_trans(self, row_data: TransRow) -> None:
        """
        Update a transactions in the database

        Augs:
            row_data[TransRow]: Transaction data dictionary.
        """

        try:
            self.cursor.execute(
                "UPDATE transactions SET source = ?, amount = ?, "
                "description = ?, date = ? WHERE uid = ?",
                (
                    row_data["source"],
                    row_data["amount"],
                    row_data["description"],
                    row_data["date"],
                    row_data["uid"],
                ),
            )

        except KeyError as err:
            msg = f"Incorrect format for row_data: {err}"
            self.log.error(msg)
            raise Exception(msg) from err

    def list_trans(
        self,
        since: datetime.date,
        until: Optional[datetime.date] = None,
    ) -> List[TransRow]:
        """Gets a time-range of transactions, returns them in a list"""

        if not until:
            until = since + datetime.timedelta(days=29)
        self.cursor.execute(
            "SELECT * FROM transactions WHERE " "date BETWEEN ? and ?" "ORDER BY uid",
            (since, until),
        )

        return self.cursor.fetchall()
