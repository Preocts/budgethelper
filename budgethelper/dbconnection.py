"""
Class object for handling IO of a sqlite database

Author: Preocts
"""
import sqlite3
from typing import List

from models.database import Database


class DBConnection:
    """Abstraction for SQLite3 database level functions"""

    def __init__(self, database: Database) -> None:
        """
        Initilize class

        Args:
            database: path and name of the database file to open
        """

        self.database = database
        self.conn = sqlite3.connect(database=database.name)

    def __del__(self) -> None:
        """Destroy connection, does not commit"""

        if self.conn:
            self.conn.close()

    @property
    def changes(self) -> int:
        """Return the # of changes pending"""

        return self.conn.total_changes

    def get_tables(self) -> List[str]:
        """return a list of tables in the database"""

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
            results = cursor.fetchall()
        finally:
            cursor.close()

        return [t[1] for t in results]

    def close(self) -> None:
        """Close connection, must reinitialize to open again"""

        self.conn.close()

    def commit(self) -> None:
        """Commit pending changes to database (write to file)"""

        self.conn.commit()
