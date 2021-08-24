"""
Class object for handling IO of a sqlite database

Author: Preocts
"""
import sqlite3
from typing import List


class DBConnection:
    """Abstraction for SQLite3 database level functions"""

    def __init__(self, database_name: str) -> None:
        """
        Initilize class

        Args:
            database: path and name of the database file to open
        """

        self.database_name = database_name
        self.conn = sqlite3.connect(database=database_name)
        self.cursor = self.conn.cursor()

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

        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        results = self.cursor.fetchall()

        return [t[1] for t in results]

    def close(self) -> None:
        """Close connection, must reinitialize to open again"""

        self.conn.close()

    def commit(self) -> None:
        """Commit pending changes to database (write to file)"""

        self.conn.commit()
